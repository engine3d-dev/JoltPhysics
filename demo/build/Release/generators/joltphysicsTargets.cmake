# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/joltphysics-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${joltphysics_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${joltphysics_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET Jolt::Jolt)
    add_library(Jolt::Jolt INTERFACE IMPORTED)
    message(${joltphysics_MESSAGE_MODE} "Conan: Target declared 'Jolt::Jolt'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/joltphysics-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()