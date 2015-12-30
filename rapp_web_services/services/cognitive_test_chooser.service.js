/***
 * Copyright 2015 RAPP
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Authors: Konstantinos Panayiotou
 * Contact: klpanagi@gmail.com
 *
 */


/***
 * @fileOverview
 *
 * [Cognitive-Test-Chooser] RAPP Platform front-end web service.
 *
 *  @author Konstantinos Panayiotou
 *  @copyright Rapp Project EU 2015
 */


var __DEBUG__ = false;

var hop = require('hop');
var path = require('path');

var ENV = require( path.join(__dirname, '..', 'env.js') );

var __includeDir = path.join(__dirname, '..', 'modules');
var __configDir = path.join(__dirname,'..', 'config');

var RandStringGen = require ( path.join(__includeDir, 'common',
    'randStringGen.js') );

var ROS = require( path.join(__includeDir, 'RosBridgeJS', 'src',
    'Rosbridge.js') );


/* ------------< Load and set global configuration parameters >-------------*/
var __hopServiceName = 'cognitive_test_chooser';
var __hopServiceId = null;
/* ----------------------------------------------------------------------- */

var rosSrvName = ENV.SERVICES[__hopServiceName].ros_srv_name;

// Initiate communication with rosbridge-websocket-server
var ros = new ROS({hostname: ENV.ROSBRIDGE.HOSTNAME, port: ENV.ROSBRIDGE.PORT,
  reconnect: true, onconnection: function(){
    // .
  }
});

/*----------------< Random String Generator configurations >---------------*/
var stringLength = 5;
var randStrGen = new RandStringGen( stringLength );
/* ----------------------------------------------------------------------- */


/* ------< Set timer values for websocket communication to rosbridge> ----- */
var timeout = ENV.SERVICES[__hopServiceName].timeout; // ms
var maxTries = ENV.SERVICES[__hopServiceName].retries;
/* ----------------------------------------------------------------------- */


// Register communication interface with the master-process
register_master_interface();


/**
 *  [Cognitive-Test-Chooser] RAPP Platform front-end web service.
 *  <p>Serves requests for cognitive-exercise selection</p>
 *
 *  @function cognitive_test_chooser
 *
 *  @param {Object} args - Service input arguments (literal).
 *  @param {String} args.user - Registered username.
 *  @param {String} args.test_type - Exercise test-type to request.
 *
 *  Currently available test types are:
 *  <ul>
 *    <li>ArithmericCts</li>
 *    <li>ReasoningCts</li>
 *    <li>AwarenessCts</li>
 *  </ul>
 *    By passing an empty string (''), the RAPP Platform Cognitive Exercises
 *    System is responsible to return a test based on previous user's
 *    performances.
 *
 *
 *  @returns {Object} response - JSON HTTPResponse Object.
 *    Asynchronous HTTP Response.
 *  @returns {String} response.lang - Language.
 *  @returns {Array} response.questions - Vector of questions, for selected
 *    exercise.
 *  @returns {Array} response.possib_ans - Array of possible answers, for
 *    selected exercise.
 *  @returns {Array} response.correct_ans - Vector of correct answers, for
 *    selected exercise.
 *  @returns {String} response.test_instance - Selected Exercise's
 *    test instance name.
 *  @returns {String} response.test_type - Test-type of selected exercise.
 *  @returns {String} response.test_subtype - Test-subtype of selected
 *    exercise.
 *  @returns {String} response.error - Error message string to be filled
 *    when an error has been occured during service call.
 *
 */
service cognitive_test_chooser( {user: '', test_type: ''} )
{
  // Assign a unique identification key for this service request.
  var unqCallId = randStrGen.createUnique();

  var startT = new Date().getTime();
  var execTime = 0;

  postMessage( craft_slaveMaster_msg('log', 'client-request {' +
    rosSrvName + '}') );


  /***
   * Asynchronous http response
   */
  return hop.HTTPResponseAsync(
    function( sendResponse ) {

      /***
       *  Status flags.
       */
      var respFlag = false;
      var retClientFlag = false;
      var wsError = false;
      var retries = 0;
      /* --------------------------------------------------- */

      // Fill Ros Service request msg parameters here.
      var args = {
        username: user,
        testType: test_type
      };


      /***
       * Declare the service response callback here!!
       * This callback function will be passed into the rosbridge service
       * controller and will be called when a response from rosbridge
       * websocket server arrives.
       */
      function callback(data){
        respFlag = true;
        if( retClientFlag ) { return; }
        // Remove this call id from random string generator cache.
        randStrGen.removeCached( unqCallId );
        //console.log(data);

        // Craft client response using ros service ws response.
        var response = craft_response( data );
        // Asynchronous response to client.
        sendResponse( hop.HTTPResponseJson(response) );
        retClientFlag = true;
      }

      /***
       * Declare the onerror callback.
       * The onerror callack function will be called by the service
       * controller as soon as an error occures, on service request.
       */
      function onerror(e){
        respFlag = true;
        if( retClientFlag ) { return; }
        // Remove this call id from random string generator cache.
        randStrGen.removeCached( unqCallId );
        var response = craft_error_response();
        // Asynchronous response to client.
        sendResponse( hop.HTTPResponseJson(response) );
        retClientFlag = true;
      }


      // Invoke ROS-Service request.
      ros.callService(rosSrvName, args,
        {success: callback, fail: onerror});

      /***
       * Set Timeout wrapping function.
       * Polling in defined time-cycle. Catch timeout connections etc...
       */
      function asyncWrap(){
        setTimeout( function(){

         /***
          *   If received message from rosbridge websocket server or an error
          *   on websocket connection, stop timeout events.
          */
          if ( respFlag || wsError || retClientFlag ) { return; }

          retries += 1;

          var logMsg = 'Reached rosbridge response timeout' + '---> [' +
            timeout.toString() + '] ms ... Reconnecting to rosbridge.' +
            'Retry-' + retries;
          postMessage( craft_slaveMaster_msg('log', logMsg) );

          /***
           * Fail. Did not receive message from rosbridge.
           * Return to client.
           */
          if ( retries >= maxTries )
          {
            logMsg = 'Reached max_retries [' + maxTries + ']' +
              ' Could not receive response from rosbridge...';
            postMessage( craft_slaveMaster_msg('log', logMsg) );

            execTime = new Date().getTime() - startT;
            postMessage( craft_slaveMaster_msg('execTime', execTime) );

            var response = craft_error_response();
            sendResponse( hop.HTTPResponseJson(response));
            retClientFlag = true;
            return;
          }
          /*--------------------------------------------------------*/
          asyncWrap();

        }, timeout);
      }
      asyncWrap();
    }, this );
}


/***
 * Crafts response object.
 *
 *  @param {Object} rosbridge_msg - Return message from rosbridge
 *
 *  @returns {Object} response - Response Object.
 *  @returns {String} response.lang - Language.
 *  @returns {Array} response.questions - Vector of questions, for selected
 *    exercise.
 *  @returns {Array} response.possib_ans - Array of possible answers, for
 *    selected exercise.
 *  @returns {Array} response.correct_ans - Vector of correct answers, for
 *    selected exercise.
 *  @returns {String} response.test_instance - Selected Exercise's
 *    test instance name.
 *  @returns {String} response.test_type - Test-type of selected exercise.
 *  @returns {String} response.test_subtype - Test-subtype of selected
 *    exercise.
 *  @returns {String} response.error - Error message string to be filled
 *    when an error has been occured during service call.
 */
function craft_response(rosbridge_msg)
{
  var trace = rosbridge_msg.trace;
  var success = rosbridge_msg.success;
  var error = rosbridge_msg.error;
  var questions = rosbridge_msg.questions;
  var answers = rosbridge_msg.answers;
  var correctAnswers = rosbridge_msg.correctAnswers;
  var test = rosbridge_msg.test;
  var testType = rosbridge_msg.testType;
  var testSubType = rosbridge_msg.testSubType;
  var language = rosbridge_msg.language;

  var logMsg = 'Returning to client.';


  var response = {
    lang: '', questions: [],
    possib_ans: [], correct_ans: [],
    test_instance: '', test_type: '',
    test_subtype: '', error: ''
  };

  response.questions = questions;
  response.correct_ans = correctAnswers;
  response.test_instance = test;
  response.test_type = testType;
  response.test_subtype = testSubType;
  response.lang = language;

  for (var ii = 0; ii < answers.length; ii++)
  {
    response.possib_ans.push( answers[ii].s );
  }

  if (!success)
  {
    logMsg += ' ROS service [' + rosSrvName + '] error ---> ' + error;
    //console.log(error)
    response.error = (!error && trace.length) ?
      trace[trace.length - 1] : error;
  }
  else
  {
    logMsg += ' ROS service [' + rosSrvName + '] returned with success';
  }

  //console.log(response);
  postMessage( craft_slaveMaster_msg('log', logMsg) );
  return response;
}


/***
 *  Craft service error response object. Used to return to client when an
 *  error has been occured, while processing client request.
 */
function craft_error_response()
{
  var errorMsg = 'RAPP Platform Failure';

  var response = {
    lang: '', questions: [],
    possib_ans: [], correct_ans: [],
    test_instance: '', test_type: '',
    test_subtype: '', error: errorMsg
  };

  var logMsg = 'Return to client with error --> ' + errorMsg;
  postMessage( craft_slaveMaster_msg('log', logMsg) );

  return response;
}


/***
 *  Register interface with the main hopjs process. After registration
 *  this worker service can communicate with the main hopjs process through
 *  websockets.
 *
 *  The global scoped postMessage is used in order to send messages to the main
 *  process.
 *  Furthermore, the global scoped onmessage callback function declares the
 *  handler for incoming messages from the hopjs main process.
 *
 *  Currently log messages are handled by the main process.
 */
function register_master_interface()
{
  // Register onexit callback function
  onexit = function(e){
    console.log("Service [%s] exiting...", __hopServiceName);
    var logMsg = "Received termination command. Exiting.";
    postMessage( craft_slaveMaster_msg('log', logMsg) );
  };

  // Register onmessage callback function
  onmessage = function(msg){
    if (__DEBUG__)
    {
      console.log("Service [%s] received message from master process",
        __hopServiceName);
      console.log("Msg -->", msg.data);
    }

    var logMsg = 'Received message from master process --> [' +
      msg.data + ']';
    postMessage( craft_slaveMaster_msg('log', logMsg) );

    var cmd = msg.data.cmdId;
    var data = msg.data.data;
    switch (cmd)
    {
      case 2055:  // Set worker ID
        __hopServiceId = data;
        break;
      default:
        break;
    }
  };

  // On initialization inform master and append to log file
  var logMsg = "Initiated worker";
  postMessage( craft_slaveMaster_msg('log', logMsg) );
}


/***
 *  Returns master-process comm msg literal.
 */
function craft_slaveMaster_msg(msgId, msg)
{
  var _msg = {
    name: __hopServiceName,
    id:   __hopServiceId,
    msgId: msgId,
    data: msg
  };
  return _msg;
}
