find_program(black_BIN NAMES black)
if(NOT black_BIN)
    message(WARNING "### could not find 'black', please run 'pip install black'")
else()    
    message(STATUS "using program '${black_BIN}'")
endif()

# macro to check all python files in CMAKE_CURRENT_SOURCE_DIR
macro(black target_name)
    if(black_BIN)
        add_custom_command(TARGET ${target_name}
            PRE_BUILD 
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            COMMAND ${black_BIN} . --exclude tmp 
            COMMENT "Running black on ${CMAKE_CURRENT_SOURCE_DIR} ...")
    endif()
endmacro()