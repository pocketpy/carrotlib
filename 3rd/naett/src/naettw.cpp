#include "naettw.hpp"

namespace pkpy{
    struct HttpResponse{
        PY_CLASS(HttpResponse, naett, Response)

        static void _register(VM* vm, PyObject* mod, PyObject* type){
            vm->bind_func<1>(type, __new__, [](VM* vm, ArgsView args){
                Type cls = PK_OBJ_GET(Type, args[0]);
                return vm->heap.gcnew<HttpResponse>(cls);
            });
        }
    };

    void add_module_naett(VM* vm){
        PyObject* mod = vm->new_module("naett");
        HttpResponse::register_class(vm, mod);

        vm->bind(mod, "request(method, url, headers=None, body=None, timeout=None)", [](VM* vm, ArgsView args){
            const Str& method = CAST(Str&, args[0]);
            const Str& url = CAST(Str&, args[1]);
            PyObject* headers = args[2];
            PyObject* body = args[3];
            PyObject* timeout = args[4];
            return vm->None;
        });
    }
}   // namespace pkpy