#include "appw.hpp"
#include "assets.hpp"

using namespace pkpy;

namespace ct{
    void platform_log_info(const Str& text){
        std::cout << text;
    }

    void platform_log_error(const Str& text){
        std::cerr << text;
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        return _platform_load_asset(name_p, name_size, out_size);
    }

    std::vector<std::string> platform_list_assets(std::string_view root){
        return _platform_list_assets(root);
    }

    Str get_system_info(){
        return _S("sys.platform: ", kPlatformStrings[PK_SYS_PLATFORM]);
    }
}   // namespace ct