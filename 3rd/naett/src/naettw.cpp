#include "naettw.hpp"

namespace pkpy{
    struct naett_response{
        PY_CLASS(naett_response, naett, Response)

        naettRes* res;

        VM* vm;
        PyObject* headers;

        naett_response(naettRes* res, VM* vm): res(res), vm(vm), headers(nullptr) {}

        void check_completed(){
            if(!naettComplete(res)) vm->IOError("Request not completed");
        }

        std::string_view text() const{
            int body_size;
            const char* body = (const char*)naettGetBody(res, &body_size);
            return std::string_view(body, body_size);
        }

        Bytes content() const{
            int body_size;
            unsigned char* body = (unsigned char*)naettGetBody(res, &body_size);
            return Bytes(body, body_size);
        }

        static void _register(VM* vm, PyObject* mod, PyObject* type){
            vm->bind_notimplemented_constructor<naett_response>(type);

            vm->bind_property(type, "completed: bool", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                return VAR(naettComplete(self.res) != 0);
            });

            vm->bind_property(type, "status_code: int", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                return VAR(naettGetStatus(self.res));
            });

            vm->bind_method<0>(type, "text: str", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                return VAR(self.text());
            });

            vm->bind_method<0>(type, "content: bytes", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                return VAR(self.content());
            });

            vm->bind_method<0>(type, "json", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                CodeObject_ code = vm->compile(self.text(), "<json>", JSON_MODE);
                return vm->_exec(code, vm->top_frame()->_module);
            });

            vm->bind_property(type, "headers: dict", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                if(self.headers == nullptr){
                    // initialize headers
                    self.headers = VAR(Dict(vm));
                    if(naettGetStatus(self.res) > 0){
                        naettHeaderLister lister = [](const char* name, const char* value, void* userData){
                            Dict* dict = (Dict*)userData;
                            dict->set(py_var(dict->vm, name), py_var(dict->vm, value));
                            return 0;
                        };
                        Dict& dict = PK_OBJ_GET(Dict, self.headers);
                        naettListHeaders(self.res, lister, &dict);
                    }
                }
                return self.headers;
            });
        }

        void _gc_mark() const{
            if(headers) PK_OBJ_MARK(headers)
        }

        ~naett_response(){
            naettClose(res);
            naettFree(naettGetRequest(res));
        }
    };

    void add_module_naett(VM* vm){
        PyObject* mod = vm->new_module("naett");
        naett_response::register_class(vm, mod);

        vm->bind(mod, "request(method, url, headers=None, body: str | bytes = None, timeout=None)", [](VM* vm, ArgsView args){
            const Str& method = CAST(Str&, args[0]);
            const Str& url = CAST(Str&, args[1]);

            std::vector<naettOption*> options;
            options.push_back(naettMethod(method.c_str()));
            if(args[2] != vm->None){
                Dict& headers = CAST(Dict&, args[2]);
                headers.apply([&](PyObject* key, PyObject* value){
                    const char* k = CAST(Str&, key).c_str();
                    const char* v = CAST(Str&, value).c_str();
                    options.push_back(naettHeader(k, v));
                });
            }

            if(args[3] != vm->None){
                const char* body;
                int body_size;
                if(is_type(args[3], VM::tp_str)){
                    body = PK_OBJ_GET(Str, args[3]).c_str();
                    body_size = PK_OBJ_GET(Str, args[3]).size;
                }else if(is_type(args[3], VM::tp_bytes)){
                    body = (const char*)PK_OBJ_GET(Bytes, args[3]).data();
                    body_size = PK_OBJ_GET(Bytes, args[3]).size();
                }
                options.push_back(naettBody(body, body_size));
            }

            if(args[4] != vm->None){
                f64 timeout = CAST(f64, args[4]);
                options.push_back(naettTimeout(timeout * 1000));
            }

            naettReq* req = naettRequestWithOptions(
                url.c_str(),
                options.size(),
                const_cast<const naettOption**>(options.data())
            );

            naettRes* res = naettMake(req);
            return vm->heap.gcnew<naett_response>(naett_response::_type(vm), res, vm);
        });
    }
}   // namespace pkpy