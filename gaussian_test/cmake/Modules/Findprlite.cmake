#
# Try to find prlite by using the cmake find_package command, e.g.:
#
#   find_package(prlite REQUIRED)
#
# For more details on find_package options, see:
#
#   cmake --help-command find_package
#
# Once done, this will define
#
# PRLITE_FOUND - system has prlite
# PRLITE_INCLUDE_DIRS - the prlite include directories
# PRLITE_LIBRARIES - link these to use prlite
#
# If prlite cannot be found in the locations specified in this
# script, you can manually forward known locations for the prlite
# library and header files, by defining the variables
# PRLITE_LIBRARY_SEARCH_PATH and PRLITE_INCLUDE_SEARCH_PATH
# respectively, prior to calling find_package, e.g.
#
# set(PRLITE_INCLUDE_SEARCH_PATH $ENV{HOME}/Developer/usr/include)
# set(PRLITE_LIBRARY_SEARCH_PATH $ENV{HOME}/Developer/usr/lib)
# find_package(prlite REQUIRED)
#

#message("SEARCHING for prlite")

if(PRLITE_INCLUDE_DIRS AND PRLITE_LIBRARIES)
  set(PRLITE_FIND_QUIETLY TRUE)
endif()

# find prlite parent dir for include dirs
find_path(
  PRLITE_INCLUDE_DIR
    prlite_genvec.hpp
  PATHS
    # look in common install locations first
    /usr/local/include
    /usr/include
    /opt/include
    ${CYGWIN_INSTALL_PATH}/include
    # then in a possible user specified location
    ${PRLITE_INCLUDE_SEARCH_PATH}
    # or relative location
    ../prlite
    # or in documented/standard location
    $ENV{HOME}/devel/prlite/src
    )
  set(PRLITE_INCLUDE_DIRS ${PRLITE_INCLUDE_DIR})
  #message(${PRLITE_INCLUDE_DIRS})

# finally the library itself
find_library(
  PRLITE_LIBRARY NAMES
    prlite
  PATHS
    # look in common install locations first
    /usr/local/lib
    /usr/lib
    /opt/lib
    ${CYGWIN_INSTALL_PATH}/lib
    # then in a possible user specified location
    ${PRLITE_LIBRARY_SEARCH_PATH}
    # or relative locations
    ../prlite
    ../prlite/build/${TARGET_PLATFORM}
    # or in documented/standard locations
    $ENV{HOME}/devel/prlite
    $ENV{HOME}/devel/prlite/build/src
  )
  #message(${PRLITE_LIBRARY})

# handle the QUIETLY and REQUIRED arguments and set PRLITE_FOUND to
# TRUE if all listed variables are TRUE
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
  prlite DEFAULT_MSG
  PRLITE_LIBRARY PRLITE_INCLUDE_DIR
  )

set(PRLITE_LIBRARIES ${PRLITE_LIBRARY})

mark_as_advanced(PRLITE_LIBRARY PRLITE_INCLUDE_DIRS)

#message("DONE with prlite")
