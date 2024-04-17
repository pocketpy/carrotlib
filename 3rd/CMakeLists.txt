cmake_minimum_required(VERSION 3.10)

project(3rdparty)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

aux_source_directory(imgui IMGUI_SRC)
aux_source_directory(rlImGui RLIMGUI_SRC)

aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/box2d/src/collision BOX2D_SRC_0)
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/box2d/src/common BOX2D_SRC_1)
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/box2d/src/dynamics BOX2D_SRC_2)
aux_source_directory(${CMAKE_CURRENT_LIST_DIR}/box2d/src/rope BOX2D_SRC_3)

option(PK_ENABLE_OS "" ON)
option(PK_NO_EXPORT_C_API "" ON)
add_subdirectory(pocketpy)

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
    ${BOX2D_SRC_0} ${BOX2D_SRC_1} ${BOX2D_SRC_2} ${BOX2D_SRC_3}
)

if(NOT CMAKE_SYSTEM_NAME STREQUAL "iOS")
    add_subdirectory(raylib)
    target_link_libraries(
        ${PROJECT_NAME}
        pocketpy
        raylib
    )
else()
    target_link_libraries(
        ${PROJECT_NAME}
        pocketpy
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