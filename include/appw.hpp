#pragma once

#include "pocketpy.h"

#include <optional>

using namespace pkpy;

namespace ct{
    void patch_module_ct(VM* vm, PyObject* mod);

    // platform interfaces
    void platform_log_info(const Str& text);
    void platform_log_error(const Str& text);
    
    unsigned char* platform_load_asset(const char*, int, int*);
    std::optional<std::vector<Str>> platform_list_assets(const Str& root);

    void set_console_cp_utf8_on_win32();
    void set_input_method_on_win32();

    void add_module__ct(VM* vm);
}

#ifdef __ANDROID__
#include "android_native_app_glue.h"

extern "C" {
    struct android_app *GetAndroidApp(void);
}
#endif