cmake_minimum_required(VERSION 3.11)

include(FetchContent)

#Download a package with sane defaults: ie. download into under build/_deb
#ARGV0 is the name you want to give the package,
#        afterwards two variable will become available: ${ARGV0}_SOURCE_DIR
#                                                       ${ARGV0}_BINARY_DIR
#ARGV1 is the link to the github repo
#ARGV2 in the commit-hash or tag-name of the exact version you want to be on
#Usage:
# >> FetchContent_gitdefaults(googletest
# ..      https://github.com/google/googletest.git
# ..      release-1.8.0)
#
# >> ShowCmakeVariables(googletest)
# --googletest_SOURCE_DIR=/usr/home/.../myproject/build/_dev/googletest-src
# --googletest_BINARY_DIR=/usr/home/.../myproject/build/_dev/googletest-build
#
function(FetchContent_gitdefaults)
  MESSAGE("-- Assure ${ARGV1} as ${ARGV0} with commit/tag ${ARGV2}")
  FetchContent_Declare(${ARGV0}
          GIT_REPOSITORY  ${ARGV1}
          GIT_TAG         ${ARGV2})

  FetchContent_GetProperties(${ARGV0})

  if(NOT ${ARGV0}_POPULATED)
    FetchContent_Populate(${ARGV0})
  endif()

  #the above code creates these lovely vars, but make sure they are
  #put in the parent scopy
  if(${ARGV0}_SOURCE_DIR)
    set(${ARGV0}_SOURCE_DIR "${${ARGV0}_SOURCE_DIR}" PARENT_SCOPE)
    set(${ARGV0}_BINARY_DIR "${${ARGV0}_BINARY_DIR}" PARENT_SCOPE)
  endif()

endfunction()
