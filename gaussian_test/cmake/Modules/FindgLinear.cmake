#
# Try to find gLinear by using the cmake find_package command, e.g.:
#
#   find_package(gLinear REQUIRED)
#
# For more details on find_package options, see:
#
#   cmake --help-command find_package
# 
# Once done, this will define
#
# GLINEAR_FOUND - system has gLinear
# GLINEAR_INCLUDE_DIRS - the gLinear include directories
# GLINEAR_LIBRARIES - link these to use gLinear
#
# If gLinear cannot be found in the locations specified in this
# script, you can manually forward known locations for the gLinear
# library and header files, by defining the variables
# GLINEAR_LIBRARY_SEARCH_PATH and GLINEAR_INCLUDE_SEARCH_PATH
# respectively, prior to calling find_package, e.g.
#
# set(GLINEAR_INCLUDE_SEARCH_PATH $ENV{HOME}/Developer/usr/include)
# set(GLINEAR_LIBRARY_SEARCH_PATH $ENV{HOME}/Developer/usr/lib)
# find_package(gLinear REQUIRED)
#

if(GLINEAR_INCLUDE_DIRS AND GLINEAR_LIBRARIES)
  set(GLINEAR_FIND_QUIETLY TRUE)
endif()

# include dir
find_path(
  GLINEAR_INCLUDE_DIR
    gLinear/gLinear.h
  PATHS
    # look in common install locations first
    /usr/local/include
    /usr/include
    /opt/include
    ${CYGWIN_INSTALL_PATH}/include
    # then in a possible user specified location
    ${GLINEAR_INCLUDE_SEARCH_PATH}
    # or relative location
    ..
    # or in documented/standard location
    $ENV{HOME}/devel
  )

# finally the library itself
find_library(
  GLINEAR_LIBRARY NAMES
    gLinear
  PATHS
    # look in common install locations first
    /usr/local/lib
    /usr/lib
    /opt/lib
    ${CYGWIN_INSTALL_PATH}/lib
    # then in a possible user specified location
    ${GLINEAR_LIBRARY_SEARCH_PATH}
    # or relative locations
    ../gLinear
    ../gLinear/build/${TARGET_PLATFORM}
    # or in documented/standard locations
    $ENV{HOME}/devel/gLinear
    $ENV{HOME}/devel/gLinear/build/${TARGET_PLATFORM}
  )

# handle the QUIETLY and REQUIRED arguments and set GLINEAR_FOUND to
# TRUE if all listed variables are TRUE
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
  gLinear DEFAULT_MSG
  GLINEAR_LIBRARY GLINEAR_INCLUDE_DIR
  )

set(GLINEAR_LIBRARIES ${GLINEAR_LIBRARY})
set(GLINEAR_INCLUDE_DIRS ${GLINEAR_INCLUDE_DIR})

mark_as_advanced(GLINEAR_LIBRARY GLINEAR_INCLUDE_DIR)
