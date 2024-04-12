cmake_minimum_required(VERSION 3.10)

project(3rdparty)

set(CMAKE_CXX_STANDARD 17)

aux_source_directory(imgui IMGUI_SRC)
aux_source_directory(rlImGui RLIMGUI_SRC)

option(CUSTOMIZE_BUILD "Customize build" ON)
option(SUPPORT_MODULE_RMODELS "" OFF)
option(SUPPORT_SSH_KEYBOARD_RPI "" OFF)
option(SUPPORT_GIF_RECORDING "" OFF)

option(SUPPORT_FILEFORMAT_DDS "" OFF)
option(SUPPORT_FILEFORMAT_HDR "" OFF)
option(SUPPORT_FILEFORMAT_QOI "" OFF)
option(SUPPORT_FILEFORMAT_FNT "" OFF)

option(SUPPORT_FILEFORMAT_OBJ "" OFF)
option(SUPPORT_FILEFORMAT_MTL "" OFF)
option(SUPPORT_FILEFORMAT_IQM "" OFF)
option(SUPPORT_FILEFORMAT_GLTF "" OFF)
option(SUPPORT_FILEFORMAT_VOX "" OFF)
option(SUPPORT_FILEFORMAT_M3D "" OFF)
option(SUPPORT_MESH_GENERATION "" OFF)

option(SUPPORT_FILEFORMAT_XM "" OFF)
option(SUPPORT_FILEFORMAT_MOD "" OFF)
option(SUPPORT_FILEFORMAT_QOA "" OFF)

option(SUPPORT_STANDARD_FILEIO "" OFF)

option(PK_ENABLE_OS "" ON)
option(PK_NO_EXPORT_C_API "" ON)
add_subdirectory(pocketpy)

add_subdirectory(box2d)

if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /utf-8 /O2")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fexceptions -frtti -O2")

    # disable -Wshorten-64-to-32 for apple
    if(APPLE)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-shorten-64-to-32")
    endif()
endif()

add_library(
    ${PROJECT_NAME}
    STATIC
    ${IMGUI_SRC}
    ${RLIMGUI_SRC}
)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "iOS")
    add_subdirectory(raylib)
    target_link_libraries(
        ${PROJECT_NAME}
        pocketpy
        box2d
        raylib
    )
else()
    target_link_libraries(
        ${PROJECT_NAME}
        pocketpy
        box2d
    )
endif()

target_include_directories(
    ${PROJECT_NAME}
    PUBLIC
    imgui
    rlImGui
    raylib/src
    box2d/include
    pocketpy/include
)