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


var os = require('os');
var hop = require('hop');
var path = require('path');
var Fs = require( path.join(__dirname, 'modules', 'common', 'fileUtils.js') );

var ifaces = os.networkInterfaces();
var HOME = process.env.HOME;

var rosEnv = require( path.join(__dirname, 'config', 'env', 'rosbridge.json') );
var srvEnv = require( path.join(__dirname, 'config', 'env',
    'hop-services.json') );
var pathsEnv = require( path.join(__dirname, 'config', 'env', 'paths.json') );

var env = {
  SERVER: {
    PORT: hop.port,
    HOSTNAME: hop.hostname
  },
  ROSBRIDGE: {
    HOSTNAME: rosEnv.ip_addr,
    PORT: rosEnv.port
  },
  SERVICES: srvEnv,
  PATHS: {
    SERVER_CACHE_DIR: Fs.resolvePath( pathsEnv.cache_dir_server ),
    SERVICES_CACHE_DIR: Fs.resolvePath( pathsEnv.cache_dir_services ),
    LOG_DIR: Fs.resolvePath( pathsEnv.log_dir ),
    LOG_DIR_SRVS: Fs.resolvePath( pathsEnv.log_dir_services )
  }
};

module.exports = env;
