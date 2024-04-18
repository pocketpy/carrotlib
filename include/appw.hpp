#pragma once

#include "pocketpy.h"
#include "naettw.hpp"

#include <filesystem>

using namespace pkpy;

namespace ct{
    inline const char* SourceCodePro_Medium = "carrotlib/assets/SourceCodePro-Medium.otf";

    void set_template_path(const char*);
    const char* get_template_path();

    void patch_module_ct(VM* vm, PyObject* mod);

    // platform interfaces
    void platform_init();
    void platform_log_info(const Str& text);
    void platform_log_error(const Str& text);
    
    unsigned char* platform_load_asset(const char*, int, int*);
    std::vector<std::string> platform_list_assets(std::string_view);

    Str platform_system_info();
    void platform_vibrate(i64 milliseconds, int amplitude);

    Str platform_caches_directory();
    Str platform_documents_directory();

    PyObject* add_module__ct(VM* vm);
    void setup_imgui_font();
}
