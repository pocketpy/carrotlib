#include "appw.hpp"

#if _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
#endif

using namespace pkpy;

namespace ct{
    void platform_log_info(const Str& text){
        std::cout << text;
    }

    void platform_log_error(const Str& text){
        std::cerr << text;
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        return _default_import_handler(name_p, name_size, out_size);
    }

    std::optional<std::vector<Str>> platform_list_assets(const Str& root){
        std::vector<Str> result;

        std::filesystem::path path(root.sv());
        bool exists = std::filesystem::exists(path);
        if(!exists) return std::nullopt;

        for(auto& p: std::filesystem::directory_iterator(path)){
            result.push_back(p.path().string());
        }
        return result;
    }

#if _WIN32
    void set_console_cp_utf8_on_win32(){
        SetConsoleOutputCP(CP_UTF8);
        SetConsoleCP(CP_UTF8);
    }

    void set_input_method_on_win32(){
        // change input method to English
        SendMessage(GetActiveWindow(), WM_INPUTLANGCHANGEREQUEST, 0, (LPARAM)HKL(0x04090409));
    }
#endif
}   // namespace ct