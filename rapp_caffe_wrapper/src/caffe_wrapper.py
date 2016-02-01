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

# Author: Athanassios Kintsakis
# contact: akintsakis@issel.ee.auth.gr

import rospy
import sys

from image_classification import ImageClassification

from rapp_platform_ros_communications.srv import (
  imageClassificationSrv,
  imageClassificationSrvResponse  
  )

from rapp_platform_ros_communications.msg import (
  StringArrayMsg
  )

from std_msgs.msg import (
  String
  )

## @class CognitiveExercise
# @brief The Cognitive exercise ros node
class RappCaffeWrapper:

  ## @brief Default contructor
  #
  # Waits for services the node depends on and declares the callbacks of the node's services
  def __init__(self):    
	  
	# Dependencies


    #Declare Callbacks
    self.serv_topic = rospy.get_param("rapp_caffe_wrapper_image_classification")
    if(not self.serv_topic):
      rospy.logerror("rapp_caffe_wrapper_image_classification")
    self.serv=rospy.Service(self.serv_topic, imageClassificationSrv, self.imageClassificationDataHandler)    


  def imageClassificationDataHandler(self,req):
    res = imageClassificationSrvResponse()
    it = ImageClassification()
    res=it.classifyImage(req)
    return res
 
