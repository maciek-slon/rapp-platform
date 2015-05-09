cmake_minimum_required(VERSION 2.8.3)
project(rapp_platform_ros_communications)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  message_runtime
  std_msgs
  geometry_msgs  
)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate messages in the 'msg' folder
add_message_files( 
  FILES 
  StringArrayMsg.msg 
) 

## Generate services in the 'srv' folder
add_service_files(
  FILES

  /DbWrapper/DbWrapperSrv.srv
  /DbWrapper/fetchDataSrv.srv
  /DbWrapper/updateDataSrv.srv
  /DbWrapper/writeDataSrv.srv
  /DbWrapper/deleteDataSrv.srv
  
  /OntologyWrapper/createInstanceSrv.srv
  /OntologyWrapper/ontologySubSuperClassesOfSrv.srv
  /OntologyWrapper/ontologyLoadDumpSrv.srv
  /OntologyWrapper/ontologyInstancesOfSrv.srv 
  /OntologyWrapper/assertRetractAttributeSrv.srv
  
  FaceDetectionRosSrv.srv
  
  QrDetectionRosSrv.srv
  
  SpeechToTextSrv.srv  
  
  MailSend.srv
  
  /SpeechDetectionSphinx4Wrapper/SpeechRecognitionSphinx4Srv.srv
  /SpeechDetectionSphinx4Wrapper/SpeechRecognitionSphinx4ConfigureSrv.srv
  /SpeechDetectionSphinx4Wrapper/SpeechRecognitionSphinx4TotalSrv.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs  # Or other packages containing msgs
  geometry_msgs
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES rapp_platform_ros_communications
#  CATKIN_DEPENDS other_catkin_pkg
  CATKIN_DEPENDS 
    message_generation
    message_runtime
    std_msgs
    geometry_msgs
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)

## Declare a cpp library
# add_library(rapp_platform_ros_communications
#   src/${PROJECT_NAME}/rapp_platform_ros_communications.cpp
# )

## Declare a cpp executable
# add_executable(rapp_platform_ros_communications_node src/rapp_platform_ros_communications_node.cpp)

## Add cmake target dependencies of the executable/library
## as an example, message headers may need to be generated before nodes
# add_dependencies(rapp_platform_ros_communications_node rapp_platform_ros_communications_generate_messages_cpp)

## Specify libraries to link a library or executable target against
# target_link_libraries(rapp_platform_ros_communications_node
#   ${catkin_LIBRARIES}
# )

#############
## Install ##
#############

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
# install(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark executables and/or libraries for installation
# install(TARGETS rapp_platform_ros_communications rapp_platform_ros_communications_node
#   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
#   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
# )

## Mark cpp header files for installation
# install(DIRECTORY include/${PROJECT_NAME}/
#   DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
#   FILES_MATCHING PATTERN "*.h"
#   PATTERN ".svn" EXCLUDE
# )

## Mark other files for installation (e.g. launch and bag files, etc.)
# install(FILES
#   # myfile1
#   # myfile2
#   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
# )

#############
## Testing ##
#############

## Add gtest based cpp test target and link libraries
# catkin_add_gtest(${PROJECT_NAME}-test test/test_rapp_platform_ros_communications.cpp)
# if(TARGET ${PROJECT_NAME}-test)
#   target_link_libraries(${PROJECT_NAME}-test ${PROJECT_NAME})
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)