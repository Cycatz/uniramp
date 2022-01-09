find_program(flake8_BIN NAMES flake8)
if(NOT flake8_BIN)
    message(WARNING "### could not find 'flake8', please run 'pip install flake8'")
else()    
    if(FLAKE8_CONFIG)  
        message(STATUS "using program '${flake8_BIN}' with ${FLAKE8_CONFIG}")
    else()
        message(STATUS "using program '${flake8_BIN}' with default config")
    endif()
endif()

# macro to check all python files in CMAKE_CURRENT_SOURCE_DIR
macro(flake8 target_name)
    if(flake8_BIN)
        if(FLAKE8_CONFIG)  
            add_custom_command(TARGET ${target_name}
                PRE_BUILD 
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                COMMAND ${flake8_BIN} . --config ${FLAKE8_CONFIG} --exclude tmp 
                COMMENT "Running flake8 on ${CMAKE_CURRENT_SOURCE_DIR} ...")
        else()
            add_custom_command(TARGET ${target_name}
                PRE_BUILD 
                WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                COMMAND ${flake8_BIN} . --exclude tmp 
                COMMENT "Running flake8 on ${CMAKE_CURRENT_SOURCE_DIR} ...")
        endif()
    endif()
endmacro()
