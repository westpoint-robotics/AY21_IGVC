# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "velodyne_ll: 3 messages, 0 services")

set(MSG_I_FLAGS "-Ivelodyne_ll:/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg;-Igeometry_msgs:/opt/ros/kinetic/share/geometry_msgs/cmake/../msg;-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(velodyne_ll_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_custom_target(_velodyne_ll_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "velodyne_ll" "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" "geometry_msgs/TransformStamped:std_msgs/Header:geometry_msgs/Quaternion:velodyne_ll/Slice:geometry_msgs/Vector3:geometry_msgs/Transform"
)

get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_custom_target(_velodyne_ll_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "velodyne_ll" "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" "geometry_msgs/TransformStamped:std_msgs/Header:velodyne_ll/Chunk:geometry_msgs/Quaternion:velodyne_ll/Slice:geometry_msgs/Vector3:geometry_msgs/Transform"
)

get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_custom_target(_velodyne_ll_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "velodyne_ll" "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll
)
_generate_msg_cpp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll
)
_generate_msg_cpp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll
)

### Generating Services

### Generating Module File
_generate_module_cpp(velodyne_ll
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(velodyne_ll_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(velodyne_ll_generate_messages velodyne_ll_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_cpp _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_cpp _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_cpp _velodyne_ll_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(velodyne_ll_gencpp)
add_dependencies(velodyne_ll_gencpp velodyne_ll_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS velodyne_ll_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll
)
_generate_msg_eus(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll
)
_generate_msg_eus(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll
)

### Generating Services

### Generating Module File
_generate_module_eus(velodyne_ll
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(velodyne_ll_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(velodyne_ll_generate_messages velodyne_ll_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_eus _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_eus _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_eus _velodyne_ll_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(velodyne_ll_geneus)
add_dependencies(velodyne_ll_geneus velodyne_ll_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS velodyne_ll_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll
)
_generate_msg_lisp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll
)
_generate_msg_lisp(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll
)

### Generating Services

### Generating Module File
_generate_module_lisp(velodyne_ll
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(velodyne_ll_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(velodyne_ll_generate_messages velodyne_ll_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_lisp _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_lisp _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_lisp _velodyne_ll_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(velodyne_ll_genlisp)
add_dependencies(velodyne_ll_genlisp velodyne_ll_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS velodyne_ll_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll
)
_generate_msg_nodejs(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll
)
_generate_msg_nodejs(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll
)

### Generating Services

### Generating Module File
_generate_module_nodejs(velodyne_ll
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(velodyne_ll_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(velodyne_ll_generate_messages velodyne_ll_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_nodejs _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_nodejs _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_nodejs _velodyne_ll_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(velodyne_ll_gennodejs)
add_dependencies(velodyne_ll_gennodejs velodyne_ll_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS velodyne_ll_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll
)
_generate_msg_py(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/TransformStamped.msg;/opt/ros/kinetic/share/std_msgs/cmake/../msg/Header.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Quaternion.msg;/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Vector3.msg;/opt/ros/kinetic/share/geometry_msgs/cmake/../msg/Transform.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll
)
_generate_msg_py(velodyne_ll
  "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll
)

### Generating Services

### Generating Module File
_generate_module_py(velodyne_ll
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(velodyne_ll_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(velodyne_ll_generate_messages velodyne_ll_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Chunk.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_py _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Raw.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_py _velodyne_ll_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/user1/code/rtk/src/TARDEC/tardec_drivers/velodyne_ll/msg/Slice.msg" NAME_WE)
add_dependencies(velodyne_ll_generate_messages_py _velodyne_ll_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(velodyne_ll_genpy)
add_dependencies(velodyne_ll_genpy velodyne_ll_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS velodyne_ll_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/velodyne_ll
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(velodyne_ll_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(velodyne_ll_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/velodyne_ll
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(velodyne_ll_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(velodyne_ll_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/velodyne_ll
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(velodyne_ll_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(velodyne_ll_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/velodyne_ll
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(velodyne_ll_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(velodyne_ll_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll)
  install(CODE "execute_process(COMMAND \"/usr/bin/python\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/velodyne_ll
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(velodyne_ll_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(velodyne_ll_generate_messages_py std_msgs_generate_messages_py)
endif()
