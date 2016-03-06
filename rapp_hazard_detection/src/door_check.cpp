/******************************************************************************
Copyright 2015 RAPP

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

  Authors: Maciej Stefańczyk
  contact: m.stefanczyk@elka.pw.edu.pl

******************************************************************************/

#include <hazard_detection/door_check.hpp>

int DoorCheck::process( const std::string & fname, bool debug ) {
  cv::Mat img = cv::imread(fname);
  
  if (img.empty()) return -1;
  
  return 0;
}
