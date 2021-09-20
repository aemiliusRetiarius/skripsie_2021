#Print available variables with varname matching ARG0
#Usage:
# >> ShowCmakeVariables(FOO)
# --FOO_DIR=/usr/home/FOO/bla
# --VAL_FOO=BAR
function(ShowCmakeVariables)
  get_cmake_property(_variableNames VARIABLES)
  list (SORT _variableNames)
  foreach (_variableName ${_variableNames})
    if (ARGV0)
      unset(MATCHED)
      string(REGEX MATCH ${ARGV0} MATCHED ${_variableName})
      if (NOT MATCHED)
        continue()
      endif()
    endif()
    message(STATUS "${_variableName}=${${_variableName}}")
  endforeach()
endfunction()
