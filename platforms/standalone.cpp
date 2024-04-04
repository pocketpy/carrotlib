#include "appw.hpp"

#if _WIN32
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
#endif

using namespace pkpy;

namespace ct{
    void platform_init(){
#if _WIN32
        SetConsoleOutputCP(CP_UTF8);
        SetConsoleCP(CP_UTF8);
#endif
        setvbuf(stdout, nullptr, _IONBF, 0);
        setvbuf(stderr, nullptr, _IONBF, 0);
    }

    void platform_log_info(const Str& text){
        std::cout << text;
    }

    void platform_log_error(const Str& text){
        std::cerr << text;
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        return _default_import_handler(name_p, name_size, out_size);
    }

    std::vector<std::string> platform_list_assets(std::string_view root){
        std::vector<std::string> result;
        std::filesystem::path path(root);
        bool exists = std::filesystem::exists(path);
        if(!exists) return {};
        for(auto& p: std::filesystem::directory_iterator(path)){
            result.push_back(p.path().string());
        }
        return result;
    }

    Str get_system_info(){
        return _S("sys.platform: ", kPlatformStrings[PK_SYS_PLATFORM]);
    }
}   // namespace ct
