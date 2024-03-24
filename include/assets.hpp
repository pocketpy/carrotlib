#pragma once

#include <map>
#include <string>
#include <string_view>

static std::map<
    std::string_view,
    std::pair<const unsigned char*, int>,
    std::less<>
> _Assets;

extern void init_hardcoded_assets(decltype(_Assets)& assets);

inline unsigned char* _platform_load_asset(const char* name_p, int name_size, int* out_size){
    if(_Assets.empty()) init_hardcoded_assets(_Assets);
    auto it = _Assets.find(std::string_view(name_p, name_size));
    if(it == _Assets.end()) return nullptr;
    *out_size = it->second.second;
    unsigned char* out = new unsigned char[*out_size];
    memcpy(out, it->second.first, *out_size);
    return out;
}

inline std::vector<std::string> _platform_list_assets(std::string_view root){
    if(_Assets.empty()) init_hardcoded_assets(_Assets);
    std::vector<std::string> result;
    for(auto& kv: _Assets){
        if(kv.first.substr(0, root.size()) == root){
            result.push_back(std::string(kv.first));
        }
    }
    return result;
}
