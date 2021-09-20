#
# Try to find emdw by using the cmake find_package command, e.g.:
#
#   find_package(emdw REQUIRED)
#
# For more details on find_package options, see:
#
#   cmake --help-command find_package
#
# Once done, this will define
#
# EMDW_FOUND - system has emdw
# EMDW_INCLUDE_DIRS - the emdw include directories
# EMDW_LIBRARIES - link these to use emdw
#
# If emdw cannot be found in the locations specified in this
# script, you can manually forward known locations for the emdw
# library and header files, by defining the variables
# EMDW_LIBRARY_SEARCH_PATH and EMDW_INCLUDE_SEARCH_PATH
# respectively, prior to calling find_package, e.g.
#
# set(EMDW_INCLUDE_SEARCH_PATH $ENV{HOME}/Developer/usr/include)
# set(EMDW_LIBRARY_SEARCH_PATH $ENV{HOME}/Developer/usr/lib)
# find_package(emdw REQUIRED)
#

#message("SEARCHING for emdw")

if(EMDW_INCLUDE_DIRS AND EMDW_LIBRARIES)
  set(EMDW_FIND_QUIETLY TRUE)
endif()

# find emdw parent dir for include dirs
find_path(
  EMDW_SOURCE_DIR
    _EMDW_SOURCE_ROOT_
  PATHS
    # look in common install locations first
    /usr/local/include
    /usr/include
    /opt/include
    ${CYGWIN_INSTALL_PATH}/include
    # then in a possible user specified location
    ${EMDW_INCLUDE_SEARCH_PATH}
    # or relative location
    ../emdw
    # or in documented/standard location
    $ENV{HOME}/devel/emdw/src
    )
  #set(EMDW_SOURCE_DIR ~/devel/emdw/src)
  #message(${EMDW_SOURCE_DIR})

# finally the library itself
find_library(
  EMDW_LIBRARY NAMES
    emdw
  PATHS
    # look in common install locations first
    /usr/local/lib
    /usr/lib
    /opt/lib
    ${CYGWIN_INSTALL_PATH}/lib
    # then in a possible user specified location
    ${EMDW_LIBRARY_SEARCH_PATH}
    # or relative locations
    ../emdw
    ../emdw/build/${TARGET_PLATFORM}
    # or in documented/standard locations
    $ENV{HOME}/devel/emdw
    $ENV{HOME}/devel/emdw/build/${TARGET_PLATFORM}
  )

set(EMDW_INCLUDE_DIRS
  ${EMDW_SOURCE_DIR}/emdw-base
  ${EMDW_SOURCE_DIR}/emdw-beliefprop
  ${EMDW_SOURCE_DIR}/emdw-clustering
  ${EMDW_SOURCE_DIR}/emdw-factors
  ${EMDW_SOURCE_DIR}/emdw-graphing
  ${EMDW_SOURCE_DIR}/test
  ${EMDW_SOURCE_DIR}/utils-dependancyglue
  ${EMDW_SOURCE_DIR}/utils-informationtheory
  ${EMDW_SOURCE_DIR}/utils-matrix
  ${EMDW_SOURCE_DIR}/utils-misc
  ${EMDW_SOURCE_DIR}/utils-sigmapoints
  ${EMDW_SOURCE_DIR}/utils-vector
  ${EMDW_SOURCE_DIR}/vmp
  ${EMDW_SOURCE_DIR}/wip
  )
#message(${EMDW_INCLUDE_DIRS})

# handle the QUIETLY and REQUIRED arguments and set EMDW_FOUND to
# TRUE if all listed variables are TRUE
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
  emdw DEFAULT_MSG
  EMDW_LIBRARY EMDW_INCLUDE_DIRS
  )

set(EMDW_LIBRARIES ${EMDW_LIBRARY})

mark_as_advanced(EMDW_LIBRARY EMDW_INCLUDE_DIRS)

#message("DONE finding emdw")
