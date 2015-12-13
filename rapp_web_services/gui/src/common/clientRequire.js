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

var filePath = path.dirname( module.filename );


function resolve( ){
  var args = arguments;
  var regexp = /~/g;
  var home = process.env.HOME;
  var joinedPaths = "";

  for( var i in args ){
    joinedPaths = path.join(joinedPaths, args[i]);
  }

  return joinedPaths.replace(regexp, home);
}


var _JS = [
  resolve(filePath, '../../js/jquery-1.11.3.js'),
  resolve(filePath, '../../js/jquery-ui-1.11.4/jquery-ui.min.js'),
  resolve(filePath, '../../js/bootstrap.min.js'),
  resolve(filePath, '../../js/bootstrap-select.min.js')
];

var _CSS = [
  resolve(filePath, '../../css/bootstrap.min.css'),
  resolve(filePath, '../../css/bootstrap-theme.min.css'),
  resolve(filePath, '../../js/jquery-ui-1.11.4/jquery-ui.css'),
  resolve(filePath, '../../css/klpanagi.css'),
  resolve(filePath, '../../css/bootstrap-select.min.css')
];



module.exports.CSS = _CSS;
module.exports.JS = _JS;
