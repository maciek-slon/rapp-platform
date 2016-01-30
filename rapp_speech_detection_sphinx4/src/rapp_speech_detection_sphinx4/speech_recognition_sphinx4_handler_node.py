#!/usr/bin/env python
# -*- encode: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Authors: Aris Thallas
# contact: aris.thallas@{iti.gr, gmail.com}

import rospy
import sys
import time
import hashlib
import threading

from speech_recognition_sphinx4 import *

from rapp_utilities import RappUtilities


from rapp_platform_ros_communications.srv import (
  SpeechRecognitionSphinx4TotalSrv,
  SpeechRecognitionSphinx4TotalSrvResponse
  )

## @class SpeechRecognitionSphinx4HandlerNode
# @brief Maintains Sphinx instances to perform speech recognition
#
# Maintains a number of child processes to perform speech recognition utilizing
# Sphinx4
# (rapp_speech_detection_sphinx4.speech_recognition_sphinx4.SpeechRecognitionSphinx4).
# Provides ros services and handles the requests according to the child
# processes' status.
class SpeechRecognitionSphinx4HandlerNode():

  ## @brief Initializes the subprocesses and the services (constructor)
  def __init__(self):

    ## The number of child subprocesses.
    self._threads = \
        rospy.get_param("rapp_speech_detection_sphinx4_threads")

    if rospy.get_param("rapp_speech_detection_sphinx4_preconfigure"):
      configurations = self._getPreconfigurationNames()
      ## The subprocesses structure that contains information used for the
      # subprocess handling
      self._availableProcesses = [{
        'sphinx': SpeechRecognitionSphinx4(configurations[i]), \
        'running': False, \
        'configuration_hash': 0\
        } for i in range(self._threads)]
      for proc in self._availableProcesses:
        proc['configuration_hash'] = proc['sphinx'].getConfigurationHash()
    else:
      self._availableProcesses = [{
        'sphinx': SpeechRecognitionSphinx4(), \
        'running': False, \
        'configuration_hash': 0\
        } for i in range(self._threads)]

    ## Thread conditional variable used for the subprocess scheduling
    self._lock = threading.Condition()
    ## Total service callback threads waiting to execute
    self._threadCounter = 0

    serv_batch_topic = \
        rospy.get_param("rapp_speech_detection_sphinx4_total_topic")
    if(not serv_batch_topic):
      rospy.logerror("Sphinx4 Speech detection batch topic param not found")

    ## Ros service server for sphinx speech recognition
    self._speech_recognition_batch_service = rospy.Service( \
        serv_batch_topic, SpeechRecognitionSphinx4TotalSrv, \
        self.handleSpeechRecognitionCallback)


  ## @brief Specifies the requested preconfiguration names
  #
  # Reads and creates a matrix with the configuration name requested from
  # rapp_speech_detection_sphinx4::cfg::sphinx4_wrapper_params.yaml
  #
  # @return preconf [ list<string> ] The preconfiguration names for all subprocesses
  def _getPreconfigurationNames(self):
    preconf = []

    RappUtilities.rapp_print( 'Fetcing preconfiguration names' )
    # Get number of requested preconfigurations
    confNumber = \
       rospy.get_param("rapp_speech_detection_sphinx4_preconfigure_number")

    # Too many configurations
    if confNumber > self._threads:
      RappUtilities.rapp_print("Sphinx preconfigurations requested exceed " + \
          "Sphinx processes. Truncating", 'WARN')
      confNumber = self._threads

    # Check actual unique configurations provided
    if rospy.has_param("rapp_speech_detection_sphinx4_preconfiguration"):
        confDict = \
            rospy.get_param("rapp_speech_detection_sphinx4_preconfiguration")
        uniqueConfigurations = len( confDict )
        if uniqueConfigurations > confNumber:
          uniqueConfigurations = confNumber
    else:
      RappUtilities.rapp_print("Preconfigurations requested, but none was " + \
          "provided", 'ERROR')
      for it in range(self._threads):
        preconf.append(None)
      return preconf

    for confIter in range(confNumber):
      preconf.append(confDict[ str(confIter % uniqueConfigurations) ])

    for it in range(self._threads - confNumber):
      preconf.append(None)

    RappUtilities.rapp_print(str(preconf), 'DEBUG')
    return preconf


  ## @brief The callback to perform speech recognition
  #
  # @param req  [rapp_platform_ros_communications::SpeechDetectionSphinx4Wrapper::SpeechRecognitionSphinx4TotalSrvRequest] The service request
  # @return res [rapp_platform_ros_communications::SpeechDetectionSphinx4Wrapper::SpeechRecognitionSphinx4TotalSrvResponse] The service response
  def handleSpeechRecognitionCallback(self, req):

    RappUtilities.rapp_print("Received service request", 'DEBUG')
    res = SpeechRecognitionSphinx4TotalSrvResponse()

    request_hash = self._calculateRequestHash( req )

    self._lock.acquire()
    self._threadCounter += 1
    if self._threadCounter > self._threads:
      self._lock.wait()

    # Search for available Sphinx with similar configuration
    for proc in self._availableProcesses:
      if proc['running'] == False and \
         proc['configuration_hash'] == request_hash:

        RappUtilities.rapp_print("Found Sphinx process with same configuration",\
            'DEBUG')
        proc['running'] = True
        self._lock.release()
        res = proc['sphinx'].speechRecognitionBatch( req )

        self._lock.acquire()
        proc['running'] = False
        self._threadCounter -= 1
        if self._threadCounter >= self._threads:
          self._lock.notify()
        self._lock.release()

        return res

    # Search for available Sphinx
    for proc in self._availableProcesses:
      if proc['running'] == False:

        proc['configuration_hash'] = request_hash
        proc['running'] = True

        RappUtilities.rapp_print("Found Sphinx process", 'DEBUG')
        self._lock.release()
        res = proc['sphinx'].speechRecognitionBatch( req )

        self._lock.acquire()
        proc['running'] = False
        self._threadCounter -= 1
        if self._threadCounter >= self._threads:
          self._lock.notify()
        self._lock.release()

        return res

  ## @brief Calculates the service request sha1 hash for process handling purposes
  #
  # Hash is used to identify common request configurations for proper subprocess selection.
  # (Requests with common requests do not require reconfiguration reducing computation time)
  #
  # @param req [rapp_platform_ros_communications::SpeechDetectionSphinx4Wrapper::SpeechRecognitionSphinx4TotalSrvRequest] The service request
  #
  # @return hexdigest [string] The hash digest containing only hexadecimal digits
  def _calculateRequestHash(self, req):
    hash_object = hashlib.sha1()
    hash_object.update( req.language )
    for word in req.words:
      hash_object.update( word )
    for gram in req.grammar:
      hash_object.update( gram )
    for sent in req.sentences:
      hash_object.update( sent )
    return hash_object.hexdigest()


if __name__ == "__main__":
  rospy.init_node('SpeechRecognitionSphinx4')
  SpeechRecognitionSphinx4HandlerNode = SpeechRecognitionSphinx4HandlerNode()
  RappUtilities.rapp_print("Sphinx4 Handler node initialized", 'DEBUG')
  rospy.spin()

