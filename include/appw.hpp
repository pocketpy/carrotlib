#pragma once

#include "pocketpy.h"
#include <filesystem>

using namespace pkpy;

namespace ct{
    void patch_module_ct(VM* vm, PyObject* mod);

    // platform interfaces
    void platform_init();
    void platform_log_info(const Str& text);
    void platform_log_error(const Str& text);
    
    unsigned char* platform_load_asset(const char*, int, int*);
    std::vector<std::string> platform_list_assets(std::string_view);
    PyObject* add_module__ct(VM* vm);

    Str get_system_info();
    void setup_imgui_font();
}
