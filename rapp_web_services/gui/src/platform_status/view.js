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

var path = require('path');
var GUIPARTS = require( path.join(__dirname, 'guiParts.js') );


var INDEX = function(){
 return   <HTML>{
    lang: "en",
    GUIPARTS.HEADER(),
    <BODY>{
      GUIPARTS.NAVBAR(),
      <DIV>{
        class: "container",
        <DIV>{
          class: "row-fluid",
          GUIPARTS.PAGE_HEADER()
        }
      },
      <DIV>{
        class: "container",
        <DIV>{
          class: "row-fluid",
          <DIV>{
            class: "col-xs-2 col-sm-2 col-md-2 col-lg-2",
            style: "word-wrap:break-word;",
            GUIPARTS.ROS_NODES_FORM(),
            GUIPARTS.ROS_SERVICES_FORM(),
            GUIPARTS.ROS_TOPICS_FORM(),
            GUIPARTS.HOP_SERVICES_FORM()
          },
          <DIV>{
            class: "col-xs-4 col-sm-4 col-md-4 col-lg-4",
            style: "word-wrap:break-word;",
            GUIPARTS.TEST_PANEL()
          },
          <DIV>{
            class: "col-xs-6 col-sm-6 col-md-6 col-lg-6",
            style: "word-wrap:break-word;",
            GUIPARTS.TEST_RESULTS_PANEL()
          }
        }
      },
      <DIV>{
        class: "container",
        <DIV>{
          class: "row-fluid",
          GUIPARTS.FOOTER()
        }
      }
    }
  }
}

exports.INDEX =  INDEX;