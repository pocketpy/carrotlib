#include "naettw.hpp"

namespace pkpy{
    struct naett_response{
        PY_CLASS(naett_response, naett, Response)

        naettReq* req;
        naettRes* res;
        VM* vm;

        naett_response(naettReq* req, naettRes* res, VM* vm): req(req), res(res), vm(vm) {}

        void check_completed(){
            if(!naettComplete(res)) vm->IOError("request not completed");
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

            vm->bind_property(type, "text: str", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                return VAR(self.text());
            });

            vm->bind_property(type, "content: bytes", [](VM* vm, ArgsView args){
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
                Dict headers(vm);
                if(naettGetStatus(self.res) > 0){
                    naettHeaderLister lister = [](const char* name, const char* value, void* userData){
                        Dict* dict = (Dict*)userData;
                        dict->set(py_var(dict->vm, name), py_var(dict->vm, value));
                        return 0;
                    };
                    naettListHeaders(self.res, lister, &headers);
                }
                return VAR(std::move(headers));
            });

            vm->bind_property(type, "reason: str", [](VM* vm, ArgsView args){
                naett_response& self = PK_OBJ_GET(naett_response, args[0]);
                self.check_completed();
                std::string_view reason;
                switch(naettGetStatus(self.res)){
                    case  0: reason = "naettProcessing"; break; 
                    case -1: reason = "naettConnectionError"; break;
                    case -2: reason = "naettProtocolError"; break;
                    case -3: reason = "naettReadError"; break;
                    case -4: reason = "naettWriteError"; break;
                    case -5: reason = "naettGenericError"; break;
                    case 100: reason = "Continue"; break;
                    case 101: reason = "Switching Protocols"; break;
                    case 200: reason = "OK"; break;
                    case 201: reason = "Created"; break;
                    case 202: reason = "Accepted"; break;
                    case 203: reason = "Non-Authoritative Information"; break;
                    case 204: reason = "No Content"; break;
                    case 205: reason = "Reset Content"; break;
                    case 206: reason = "Partial Content"; break;
                    case 300: reason = "Multiple Choices"; break;
                    case 301: reason = "Moved Permanently"; break;
                    case 302: reason = "Found"; break;
                    case 303: reason = "See Other"; break;
                    case 304: reason = "Not Modified"; break;
                    case 305: reason = "Use Proxy"; break;
                    case 307: reason = "Temporary Redirect"; break;
                    case 400: reason = "Bad Request"; break;
                    case 401: reason = "Unauthorized"; break;
                    case 402: reason = "Payment Required"; break;
                    case 403: reason = "Forbidden"; break;
                    case 404: reason = "Not Found"; break;
                    case 405: reason = "Method Not Allowed"; break;
                    case 406: reason = "Not Acceptable"; break;
                    case 407: reason = "Proxy Authentication Required"; break;
                    case 408: reason = "Request Timeout"; break;
                    case 409: reason = "Conflict"; break;
                    case 410: reason = "Gone"; break;
                    case 411: reason = "Length Required"; break;
                    case 412: reason = "Precondition Failed"; break;
                    case 413: reason = "Request Entity Too Large"; break;
                    case 414: reason = "Request-URI Too Long"; break;
                    case 415: reason = "Unsupported Media Type"; break;
                    case 416: reason = "Requested Range Not Satisfiable"; break;
                    case 417: reason = "Expectation Failed"; break;
                    case 500: reason = "Internal Server Error"; break;
                    case 501: reason = "Not Implemented"; break;
                    case 502: reason = "Bad Gateway"; break;
                    case 503: reason = "Service Unavailable"; break;
                    case 504: reason = "Gateway Timeout"; break;
                    case 505: reason = "HTTP Version Not Supported"; break;
                    default: reason = "";
                }
                return VAR(reason);
            });

            vm->bind__repr__(PK_OBJ_GET(Type, type), [](VM* vm, PyObject* _0){
                naett_response& self = PK_OBJ_GET(naett_response, _0);
                int status_code = naettGetStatus(self.res);
                return VAR(_S("<Response [", status_code, "]>"));
            });

            vm->bind__iter__(PK_OBJ_GET(Type, type), [](VM* vm, PyObject* _0){
                return _0;
            });

            vm->bind__next__(PK_OBJ_GET(Type, type), [](VM* vm, PyObject* _0){
                naett_response& self = PK_OBJ_GET(naett_response, _0);
                if(naettComplete(self.res)) return vm->StopIteration;
                return vm->None;
            });
        }

        ~naett_response(){
            naettClose(res);
            naettFree(req);
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
            return vm->heap.gcnew<naett_response>(naett_response::_type(vm), req, res, vm);
        });
    }
}   // namespace pkpy