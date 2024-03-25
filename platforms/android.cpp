#include "appw.hpp"

using namespace pkpy;

#include "android_native_app_glue.h"
#include <android/log.h>
#include <sys/system_properties.h>

using namespace pkpy;

extern "C" {
    extern struct android_app *GetAndroidApp(void);
}

static AAssetManager* get_android_asset_manager(){
    return GetAndroidApp()->activity->assetManager;
}

namespace ct{
    void platform_init(){
        // do nothing
    }

    void platform_log_info(const Str& text){
        __android_log_print(ANDROID_LOG_INFO, "Engine", "%s", text.c_str());
    }

    void platform_log_error(const Str& text){
        __android_log_print(ANDROID_LOG_ERROR, "Engine", "%s", text.c_str());
    }

    unsigned char* platform_load_asset(const char* name_p, int name_size, int* out_size){
        std::string name(name_p, name_size);
        AAsset* asset = AAssetManager_open(get_android_asset_manager(), name.c_str(), AASSET_MODE_BUFFER);
        if(!asset) return nullptr;
        int size = AAsset_getLength(asset);
        char* buffer = new char[size];
        AAsset_read(asset, buffer, size);
        AAsset_close(asset);
        *out_size = size;
        return (unsigned char*)buffer;
    }

    std::vector<std::string> platform_list_assets(std::string_view root){
        std::string s_root(root);
        if(s_root == ".") s_root = "";
        if(s_root.size()>2 && s_root[0]=='.' && s_root[1]=='/') s_root = s_root.substr(2);
        AAssetDir* dir = AAssetManager_openDir(get_android_asset_manager(), s_root.c_str());
        if(!dir) return {};
        std::vector<std::string> list;
        const char* name = nullptr;
        while((name = AAssetDir_getNextFileName(dir)) != nullptr){
            list.emplace_back(name);
        }
        AAssetDir_close(dir);
        return list;
    }

    Str get_system_info(){
        char manufacturer[PROP_VALUE_MAX + 1] = {0};
        char model[PROP_VALUE_MAX + 1] = {0};
        char os_version[PROP_VALUE_MAX + 1] = {0};
        /* A length 0 value indicates that the property is not defined */
        __system_property_get("ro.product.manufacturer", manufacturer);
        __system_property_get("ro.product.model", model);
        __system_property_get("ro.build.version.release", os_version);
        int sdk_version = GetAndroidApp()->activity->sdkVersion;
        return _S("Android ", os_version, " - ", manufacturer, " ", model, " - SDK ", sdk_version, " - NDK ", __NDK_MAJOR__, ".", __NDK_MINOR__);
    }
}   // namespace ct