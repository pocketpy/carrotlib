#include "raylib.h"
#include "pocketpy.h"

namespace pkpy{

template<typename T0, typename T1>
T1 _struct_cast(T0& v){
    static_assert(sizeof(T0) == sizeof(T1));
    static_assert(std::is_trivially_copyable_v<T0>);
    static_assert(std::is_trivially_copyable_v<T1>);
    return (T1&)v;
}

template<size_t N>
void _bind_enums(VM* vm, PyObject* mod, Str name, const std::pair<const char*, i64> (&enums)[N]){
    Dict d(vm);
    for(auto [k, v]: enums){
        PyObject* int_obj = py_var(vm, v);
        mod->attr().set(k, int_obj);
        d.set(int_obj, py_var(vm, k));
    }
    mod->attr().set(name + "_NAMES", py_var(vm, std::move(d)));
}

PyObject* py_var(VM* vm, Vector2 v){
    return py_var(vm, _struct_cast<Vector2, Vec2>(v));
}
template<>
Vector2 py_cast<Vector2>(VM* vm, PyObject* obj){
    Vec2 v = py_cast<Vec2>(vm, obj);
    return _struct_cast<Vec2, Vector2>(v);
}
template<>
Vector2 _py_cast<Vector2>(VM* vm, PyObject* obj){
    Vec2 v = _py_cast<Vec2>(vm, obj);
    return _struct_cast<Vec2, Vector2>(v);
}

PyObject* py_var(VM* vm, Vector3 v){
    return py_var(vm, _struct_cast<Vector3, Vec3>(v));
}
template<>
Vector3 py_cast<Vector3>(VM* vm, PyObject* obj){
    Vec3 v = py_cast<Vec3>(vm, obj);
    return _struct_cast<Vec3, Vector3>(v);
}
template<>
Vector3 _py_cast<Vector3>(VM* vm, PyObject* obj){
    Vec3 v = _py_cast<Vec3>(vm, obj);
    return _struct_cast<Vec3, Vector3>(v);
}

PyObject* py_var(VM* vm, Vector4 v){
    return py_var(vm, _struct_cast<Vector4, Vec4>(v));
}
template<>
Vector4 py_cast<Vector4>(VM* vm, PyObject* obj){
    Vec4 v = py_cast<Vec4>(vm, obj);
    return _struct_cast<Vec4, Vector4>(v);
}
template<>
Vector4 _py_cast<Vector4>(VM* vm, PyObject* obj){
    Vec4 v = _py_cast<Vec4>(vm, obj);
    return _struct_cast<Vec4, Vector4>(v);
}

/*************** Matrix ***************/
struct wrapped__Matrix{

    Matrix _value;
    wrapped__Matrix() = default;
    wrapped__Matrix(const wrapped__Matrix& other) = default;

    wrapped__Matrix(const Matrix& other){
        memcpy(&_value, &other, sizeof(Matrix));
    }
    bool operator==(const wrapped__Matrix& other) const{
        return memcmp(&_value, &other._value, sizeof(Matrix)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"m0", "m4", "m8", "m12", "m1", "m5", "m9", "m13", "m2", "m6", "m10", "m14", "m3", "m7", "m11", "m15"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 16) vm->TypeError(_S("expected 16 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Matrix)
        PY_FIELD(wrapped__Matrix, "m0", _value.m0)
        PY_FIELD(wrapped__Matrix, "m4", _value.m4)
        PY_FIELD(wrapped__Matrix, "m8", _value.m8)
        PY_FIELD(wrapped__Matrix, "m12", _value.m12)
        PY_FIELD(wrapped__Matrix, "m1", _value.m1)
        PY_FIELD(wrapped__Matrix, "m5", _value.m5)
        PY_FIELD(wrapped__Matrix, "m9", _value.m9)
        PY_FIELD(wrapped__Matrix, "m13", _value.m13)
        PY_FIELD(wrapped__Matrix, "m2", _value.m2)
        PY_FIELD(wrapped__Matrix, "m6", _value.m6)
        PY_FIELD(wrapped__Matrix, "m10", _value.m10)
        PY_FIELD(wrapped__Matrix, "m14", _value.m14)
        PY_FIELD(wrapped__Matrix, "m3", _value.m3)
        PY_FIELD(wrapped__Matrix, "m7", _value.m7)
        PY_FIELD(wrapped__Matrix, "m11", _value.m11)
        PY_FIELD(wrapped__Matrix, "m15", _value.m15)
    }
};

PyObject* py_var(VM* vm, Matrix v){
    return vm->new_user_object<wrapped__Matrix>(v);
}
template<>
Matrix py_cast<Matrix>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Matrix&>(vm, obj)._value;
}
template<>
Matrix _py_cast<Matrix>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Matrix&>(vm, obj)._value;
}
/*************** Color ***************/
struct wrapped__Color{

    Color _value;
    wrapped__Color() = default;
    wrapped__Color(const wrapped__Color& other) = default;

    wrapped__Color(const Color& other){
        memcpy(&_value, &other, sizeof(Color));
    }
    bool operator==(const wrapped__Color& other) const{
        return memcmp(&_value, &other._value, sizeof(Color)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"r", "g", "b", "a"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 4) vm->TypeError(_S("expected 4 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Color)
        PY_FIELD(wrapped__Color, "r", _value.r)
        PY_FIELD(wrapped__Color, "g", _value.g)
        PY_FIELD(wrapped__Color, "b", _value.b)
        PY_FIELD(wrapped__Color, "a", _value.a)
    }
};

PyObject* py_var(VM* vm, Color v){
    return vm->new_user_object<wrapped__Color>(v);
}
template<>
Color py_cast<Color>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Color&>(vm, obj)._value;
}
template<>
Color _py_cast<Color>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Color&>(vm, obj)._value;
}
/*************** Rectangle ***************/
struct wrapped__Rectangle{

    Rectangle _value;
    wrapped__Rectangle() = default;
    wrapped__Rectangle(const wrapped__Rectangle& other) = default;

    wrapped__Rectangle(const Rectangle& other){
        memcpy(&_value, &other, sizeof(Rectangle));
    }
    bool operator==(const wrapped__Rectangle& other) const{
        return memcmp(&_value, &other._value, sizeof(Rectangle)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"x", "y", "width", "height"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 4) vm->TypeError(_S("expected 4 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Rectangle)
        PY_FIELD(wrapped__Rectangle, "x", _value.x)
        PY_FIELD(wrapped__Rectangle, "y", _value.y)
        PY_FIELD(wrapped__Rectangle, "width", _value.width)
        PY_FIELD(wrapped__Rectangle, "height", _value.height)
    }
};

PyObject* py_var(VM* vm, Rectangle v){
    return vm->new_user_object<wrapped__Rectangle>(v);
}
template<>
Rectangle py_cast<Rectangle>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Rectangle&>(vm, obj)._value;
}
template<>
Rectangle _py_cast<Rectangle>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Rectangle&>(vm, obj)._value;
}
/*************** Image ***************/
struct wrapped__Image{

    Image _value;
    wrapped__Image() = default;
    wrapped__Image(const wrapped__Image& other) = default;

    wrapped__Image(const Image& other){
        memcpy(&_value, &other, sizeof(Image));
    }
    bool operator==(const wrapped__Image& other) const{
        return memcmp(&_value, &other._value, sizeof(Image)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"data", "width", "height", "mipmaps", "format"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Image)
        PY_FIELD(wrapped__Image, "data", _value.data)
        PY_FIELD(wrapped__Image, "width", _value.width)
        PY_FIELD(wrapped__Image, "height", _value.height)
        PY_FIELD(wrapped__Image, "mipmaps", _value.mipmaps)
        PY_FIELD(wrapped__Image, "format", _value.format)
    }
};

PyObject* py_var(VM* vm, Image v){
    return vm->new_user_object<wrapped__Image>(v);
}
template<>
Image py_cast<Image>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Image&>(vm, obj)._value;
}
template<>
Image _py_cast<Image>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Image&>(vm, obj)._value;
}
/*************** Texture ***************/
struct wrapped__Texture{

    Texture _value;
    wrapped__Texture() = default;
    wrapped__Texture(const wrapped__Texture& other) = default;

    wrapped__Texture(const Texture& other){
        memcpy(&_value, &other, sizeof(Texture));
    }
    bool operator==(const wrapped__Texture& other) const{
        return memcmp(&_value, &other._value, sizeof(Texture)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"id", "width", "height", "mipmaps", "format"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Texture)
        PY_FIELD(wrapped__Texture, "id", _value.id)
        PY_FIELD(wrapped__Texture, "width", _value.width)
        PY_FIELD(wrapped__Texture, "height", _value.height)
        PY_FIELD(wrapped__Texture, "mipmaps", _value.mipmaps)
        PY_FIELD(wrapped__Texture, "format", _value.format)
    }
};

PyObject* py_var(VM* vm, Texture v){
    return vm->new_user_object<wrapped__Texture>(v);
}
template<>
Texture py_cast<Texture>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Texture&>(vm, obj)._value;
}
template<>
Texture _py_cast<Texture>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Texture&>(vm, obj)._value;
}
/*************** RenderTexture ***************/
struct wrapped__RenderTexture{

    RenderTexture _value;
    wrapped__RenderTexture() = default;
    wrapped__RenderTexture(const wrapped__RenderTexture& other) = default;

    wrapped__RenderTexture(const RenderTexture& other){
        memcpy(&_value, &other, sizeof(RenderTexture));
    }
    bool operator==(const wrapped__RenderTexture& other) const{
        return memcmp(&_value, &other._value, sizeof(RenderTexture)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"id", "texture", "depth"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__RenderTexture)
        PY_FIELD(wrapped__RenderTexture, "id", _value.id)
        PY_FIELD(wrapped__RenderTexture, "texture", _value.texture)
        PY_FIELD(wrapped__RenderTexture, "depth", _value.depth)
    }
};

PyObject* py_var(VM* vm, RenderTexture v){
    return vm->new_user_object<wrapped__RenderTexture>(v);
}
template<>
RenderTexture py_cast<RenderTexture>(VM* vm, PyObject* obj){
    return py_cast<wrapped__RenderTexture&>(vm, obj)._value;
}
template<>
RenderTexture _py_cast<RenderTexture>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__RenderTexture&>(vm, obj)._value;
}
/*************** NPatchInfo ***************/
struct wrapped__NPatchInfo{

    NPatchInfo _value;
    wrapped__NPatchInfo() = default;
    wrapped__NPatchInfo(const wrapped__NPatchInfo& other) = default;

    wrapped__NPatchInfo(const NPatchInfo& other){
        memcpy(&_value, &other, sizeof(NPatchInfo));
    }
    bool operator==(const wrapped__NPatchInfo& other) const{
        return memcmp(&_value, &other._value, sizeof(NPatchInfo)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"source", "left", "top", "right", "bottom", "layout"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 6) vm->TypeError(_S("expected 6 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__NPatchInfo)
        PY_FIELD(wrapped__NPatchInfo, "source", _value.source)
        PY_FIELD(wrapped__NPatchInfo, "left", _value.left)
        PY_FIELD(wrapped__NPatchInfo, "top", _value.top)
        PY_FIELD(wrapped__NPatchInfo, "right", _value.right)
        PY_FIELD(wrapped__NPatchInfo, "bottom", _value.bottom)
        PY_FIELD(wrapped__NPatchInfo, "layout", _value.layout)
    }
};

PyObject* py_var(VM* vm, NPatchInfo v){
    return vm->new_user_object<wrapped__NPatchInfo>(v);
}
template<>
NPatchInfo py_cast<NPatchInfo>(VM* vm, PyObject* obj){
    return py_cast<wrapped__NPatchInfo&>(vm, obj)._value;
}
template<>
NPatchInfo _py_cast<NPatchInfo>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__NPatchInfo&>(vm, obj)._value;
}
/*************** GlyphInfo ***************/
struct wrapped__GlyphInfo{

    GlyphInfo _value;
    wrapped__GlyphInfo() = default;
    wrapped__GlyphInfo(const wrapped__GlyphInfo& other) = default;

    wrapped__GlyphInfo(const GlyphInfo& other){
        memcpy(&_value, &other, sizeof(GlyphInfo));
    }
    bool operator==(const wrapped__GlyphInfo& other) const{
        return memcmp(&_value, &other._value, sizeof(GlyphInfo)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"value", "offsetX", "offsetY", "advanceX", "image"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__GlyphInfo)
        PY_FIELD(wrapped__GlyphInfo, "value", _value.value)
        PY_FIELD(wrapped__GlyphInfo, "offsetX", _value.offsetX)
        PY_FIELD(wrapped__GlyphInfo, "offsetY", _value.offsetY)
        PY_FIELD(wrapped__GlyphInfo, "advanceX", _value.advanceX)
        PY_FIELD(wrapped__GlyphInfo, "image", _value.image)
    }
};

PyObject* py_var(VM* vm, GlyphInfo v){
    return vm->new_user_object<wrapped__GlyphInfo>(v);
}
template<>
GlyphInfo py_cast<GlyphInfo>(VM* vm, PyObject* obj){
    return py_cast<wrapped__GlyphInfo&>(vm, obj)._value;
}
template<>
GlyphInfo _py_cast<GlyphInfo>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__GlyphInfo&>(vm, obj)._value;
}
/*************** Font ***************/
struct wrapped__Font{

    Font _value;
    wrapped__Font() = default;
    wrapped__Font(const wrapped__Font& other) = default;

    wrapped__Font(const Font& other){
        memcpy(&_value, &other, sizeof(Font));
    }
    bool operator==(const wrapped__Font& other) const{
        return memcmp(&_value, &other._value, sizeof(Font)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"baseSize", "glyphCount", "glyphPadding", "texture", "recs", "glyphs"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 6) vm->TypeError(_S("expected 6 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Font)
        PY_FIELD(wrapped__Font, "baseSize", _value.baseSize)
        PY_FIELD(wrapped__Font, "glyphCount", _value.glyphCount)
        PY_FIELD(wrapped__Font, "glyphPadding", _value.glyphPadding)
        PY_FIELD(wrapped__Font, "texture", _value.texture)
        PY_FIELD(wrapped__Font, "recs", _value.recs)
        PY_FIELD(wrapped__Font, "glyphs", _value.glyphs)
    }
};

PyObject* py_var(VM* vm, Font v){
    return vm->new_user_object<wrapped__Font>(v);
}
template<>
Font py_cast<Font>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Font&>(vm, obj)._value;
}
template<>
Font _py_cast<Font>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Font&>(vm, obj)._value;
}
/*************** Camera3D ***************/
struct wrapped__Camera3D{

    Camera3D _value;
    wrapped__Camera3D() = default;
    wrapped__Camera3D(const wrapped__Camera3D& other) = default;

    wrapped__Camera3D(const Camera3D& other){
        memcpy(&_value, &other, sizeof(Camera3D));
    }
    bool operator==(const wrapped__Camera3D& other) const{
        return memcmp(&_value, &other._value, sizeof(Camera3D)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"position", "target", "up", "fovy", "projection"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Camera3D)
        PY_FIELD(wrapped__Camera3D, "position", _value.position)
        PY_FIELD(wrapped__Camera3D, "target", _value.target)
        PY_FIELD(wrapped__Camera3D, "up", _value.up)
        PY_FIELD(wrapped__Camera3D, "fovy", _value.fovy)
        PY_FIELD(wrapped__Camera3D, "projection", _value.projection)
    }
};

PyObject* py_var(VM* vm, Camera3D v){
    return vm->new_user_object<wrapped__Camera3D>(v);
}
template<>
Camera3D py_cast<Camera3D>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Camera3D&>(vm, obj)._value;
}
template<>
Camera3D _py_cast<Camera3D>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Camera3D&>(vm, obj)._value;
}
/*************** Camera2D ***************/
struct wrapped__Camera2D{

    Camera2D _value;
    wrapped__Camera2D() = default;
    wrapped__Camera2D(const wrapped__Camera2D& other) = default;

    wrapped__Camera2D(const Camera2D& other){
        memcpy(&_value, &other, sizeof(Camera2D));
    }
    bool operator==(const wrapped__Camera2D& other) const{
        return memcmp(&_value, &other._value, sizeof(Camera2D)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"offset", "target", "rotation", "zoom"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 4) vm->TypeError(_S("expected 4 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Camera2D)
        PY_FIELD(wrapped__Camera2D, "offset", _value.offset)
        PY_FIELD(wrapped__Camera2D, "target", _value.target)
        PY_FIELD(wrapped__Camera2D, "rotation", _value.rotation)
        PY_FIELD(wrapped__Camera2D, "zoom", _value.zoom)
    }
};

PyObject* py_var(VM* vm, Camera2D v){
    return vm->new_user_object<wrapped__Camera2D>(v);
}
template<>
Camera2D py_cast<Camera2D>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Camera2D&>(vm, obj)._value;
}
template<>
Camera2D _py_cast<Camera2D>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Camera2D&>(vm, obj)._value;
}
/*************** Mesh ***************/
struct wrapped__Mesh{

    Mesh _value;
    wrapped__Mesh() = default;
    wrapped__Mesh(const wrapped__Mesh& other) = default;

    wrapped__Mesh(const Mesh& other){
        memcpy(&_value, &other, sizeof(Mesh));
    }
    bool operator==(const wrapped__Mesh& other) const{
        return memcmp(&_value, &other._value, sizeof(Mesh)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"vertexCount", "triangleCount", "vertices", "texcoords", "texcoords2", "normals", "tangents", "colors", "indices", "animVertices", "animNormals", "boneIds", "boneWeights", "vaoId", "vboId"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 15) vm->TypeError(_S("expected 15 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Mesh)
        PY_FIELD(wrapped__Mesh, "vertexCount", _value.vertexCount)
        PY_FIELD(wrapped__Mesh, "triangleCount", _value.triangleCount)
        PY_FIELD(wrapped__Mesh, "vertices", _value.vertices)
        PY_FIELD(wrapped__Mesh, "texcoords", _value.texcoords)
        PY_FIELD(wrapped__Mesh, "texcoords2", _value.texcoords2)
        PY_FIELD(wrapped__Mesh, "normals", _value.normals)
        PY_FIELD(wrapped__Mesh, "tangents", _value.tangents)
        PY_FIELD(wrapped__Mesh, "colors", _value.colors)
        PY_FIELD(wrapped__Mesh, "indices", _value.indices)
        PY_FIELD(wrapped__Mesh, "animVertices", _value.animVertices)
        PY_FIELD(wrapped__Mesh, "animNormals", _value.animNormals)
        PY_FIELD(wrapped__Mesh, "boneIds", _value.boneIds)
        PY_FIELD(wrapped__Mesh, "boneWeights", _value.boneWeights)
        PY_FIELD(wrapped__Mesh, "vaoId", _value.vaoId)
        PY_FIELD(wrapped__Mesh, "vboId", _value.vboId)
    }
};

PyObject* py_var(VM* vm, Mesh v){
    return vm->new_user_object<wrapped__Mesh>(v);
}
template<>
Mesh py_cast<Mesh>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Mesh&>(vm, obj)._value;
}
template<>
Mesh _py_cast<Mesh>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Mesh&>(vm, obj)._value;
}
/*************** Shader ***************/
struct wrapped__Shader{

    Shader _value;
    wrapped__Shader() = default;
    wrapped__Shader(const wrapped__Shader& other) = default;

    wrapped__Shader(const Shader& other){
        memcpy(&_value, &other, sizeof(Shader));
    }
    bool operator==(const wrapped__Shader& other) const{
        return memcmp(&_value, &other._value, sizeof(Shader)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"id", "locs"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 2) vm->TypeError(_S("expected 2 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Shader)
        PY_FIELD(wrapped__Shader, "id", _value.id)
        PY_FIELD(wrapped__Shader, "locs", _value.locs)
    }
};

PyObject* py_var(VM* vm, Shader v){
    return vm->new_user_object<wrapped__Shader>(v);
}
template<>
Shader py_cast<Shader>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Shader&>(vm, obj)._value;
}
template<>
Shader _py_cast<Shader>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Shader&>(vm, obj)._value;
}
/*************** MaterialMap ***************/
struct wrapped__MaterialMap{

    MaterialMap _value;
    wrapped__MaterialMap() = default;
    wrapped__MaterialMap(const wrapped__MaterialMap& other) = default;

    wrapped__MaterialMap(const MaterialMap& other){
        memcpy(&_value, &other, sizeof(MaterialMap));
    }
    bool operator==(const wrapped__MaterialMap& other) const{
        return memcmp(&_value, &other._value, sizeof(MaterialMap)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"texture", "color", "value"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__MaterialMap)
        PY_FIELD(wrapped__MaterialMap, "texture", _value.texture)
        PY_FIELD(wrapped__MaterialMap, "color", _value.color)
        PY_FIELD(wrapped__MaterialMap, "value", _value.value)
    }
};

PyObject* py_var(VM* vm, MaterialMap v){
    return vm->new_user_object<wrapped__MaterialMap>(v);
}
template<>
MaterialMap py_cast<MaterialMap>(VM* vm, PyObject* obj){
    return py_cast<wrapped__MaterialMap&>(vm, obj)._value;
}
template<>
MaterialMap _py_cast<MaterialMap>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__MaterialMap&>(vm, obj)._value;
}
/*************** Material ***************/
struct wrapped__Material{

    Material _value;
    wrapped__Material() = default;
    wrapped__Material(const wrapped__Material& other) = default;

    wrapped__Material(const Material& other){
        memcpy(&_value, &other, sizeof(Material));
    }
    bool operator==(const wrapped__Material& other) const{
        return memcmp(&_value, &other._value, sizeof(Material)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"shader", "maps", "params"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Material)
        PY_FIELD(wrapped__Material, "shader", _value.shader)
        PY_FIELD(wrapped__Material, "maps", _value.maps)
        PY_READONLY_FIELD(wrapped__Material, "params", _value.params)
    }
};

PyObject* py_var(VM* vm, Material v){
    return vm->new_user_object<wrapped__Material>(v);
}
template<>
Material py_cast<Material>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Material&>(vm, obj)._value;
}
template<>
Material _py_cast<Material>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Material&>(vm, obj)._value;
}
/*************** Transform ***************/
struct wrapped__Transform{

    Transform _value;
    wrapped__Transform() = default;
    wrapped__Transform(const wrapped__Transform& other) = default;

    wrapped__Transform(const Transform& other){
        memcpy(&_value, &other, sizeof(Transform));
    }
    bool operator==(const wrapped__Transform& other) const{
        return memcmp(&_value, &other._value, sizeof(Transform)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"translation", "rotation", "scale"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Transform)
        PY_FIELD(wrapped__Transform, "translation", _value.translation)
        PY_FIELD(wrapped__Transform, "rotation", _value.rotation)
        PY_FIELD(wrapped__Transform, "scale", _value.scale)
    }
};

PyObject* py_var(VM* vm, Transform v){
    return vm->new_user_object<wrapped__Transform>(v);
}
template<>
Transform py_cast<Transform>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Transform&>(vm, obj)._value;
}
template<>
Transform _py_cast<Transform>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Transform&>(vm, obj)._value;
}
/*************** BoneInfo ***************/
struct wrapped__BoneInfo{

    BoneInfo _value;
    wrapped__BoneInfo() = default;
    wrapped__BoneInfo(const wrapped__BoneInfo& other) = default;

    wrapped__BoneInfo(const BoneInfo& other){
        memcpy(&_value, &other, sizeof(BoneInfo));
    }
    bool operator==(const wrapped__BoneInfo& other) const{
        return memcmp(&_value, &other._value, sizeof(BoneInfo)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"name", "parent"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 2) vm->TypeError(_S("expected 2 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__BoneInfo)
        PY_READONLY_FIELD(wrapped__BoneInfo, "name", _value.name)
        PY_FIELD(wrapped__BoneInfo, "parent", _value.parent)
    }
};

PyObject* py_var(VM* vm, BoneInfo v){
    return vm->new_user_object<wrapped__BoneInfo>(v);
}
template<>
BoneInfo py_cast<BoneInfo>(VM* vm, PyObject* obj){
    return py_cast<wrapped__BoneInfo&>(vm, obj)._value;
}
template<>
BoneInfo _py_cast<BoneInfo>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__BoneInfo&>(vm, obj)._value;
}
/*************** Model ***************/
struct wrapped__Model{

    Model _value;
    wrapped__Model() = default;
    wrapped__Model(const wrapped__Model& other) = default;

    wrapped__Model(const Model& other){
        memcpy(&_value, &other, sizeof(Model));
    }
    bool operator==(const wrapped__Model& other) const{
        return memcmp(&_value, &other._value, sizeof(Model)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"transform", "meshCount", "materialCount", "meshes", "materials", "meshMaterial", "boneCount", "bones", "bindPose"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 9) vm->TypeError(_S("expected 9 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Model)
        PY_FIELD(wrapped__Model, "transform", _value.transform)
        PY_FIELD(wrapped__Model, "meshCount", _value.meshCount)
        PY_FIELD(wrapped__Model, "materialCount", _value.materialCount)
        PY_FIELD(wrapped__Model, "meshes", _value.meshes)
        PY_FIELD(wrapped__Model, "materials", _value.materials)
        PY_FIELD(wrapped__Model, "meshMaterial", _value.meshMaterial)
        PY_FIELD(wrapped__Model, "boneCount", _value.boneCount)
        PY_FIELD(wrapped__Model, "bones", _value.bones)
        PY_FIELD(wrapped__Model, "bindPose", _value.bindPose)
    }
};

PyObject* py_var(VM* vm, Model v){
    return vm->new_user_object<wrapped__Model>(v);
}
template<>
Model py_cast<Model>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Model&>(vm, obj)._value;
}
template<>
Model _py_cast<Model>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Model&>(vm, obj)._value;
}
/*************** ModelAnimation ***************/
struct wrapped__ModelAnimation{

    ModelAnimation _value;
    wrapped__ModelAnimation() = default;
    wrapped__ModelAnimation(const wrapped__ModelAnimation& other) = default;

    wrapped__ModelAnimation(const ModelAnimation& other){
        memcpy(&_value, &other, sizeof(ModelAnimation));
    }
    bool operator==(const wrapped__ModelAnimation& other) const{
        return memcmp(&_value, &other._value, sizeof(ModelAnimation)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"boneCount", "frameCount", "bones", "framePoses", "name"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__ModelAnimation)
        PY_FIELD(wrapped__ModelAnimation, "boneCount", _value.boneCount)
        PY_FIELD(wrapped__ModelAnimation, "frameCount", _value.frameCount)
        PY_FIELD(wrapped__ModelAnimation, "bones", _value.bones)
        PY_FIELD(wrapped__ModelAnimation, "framePoses", _value.framePoses)
        PY_READONLY_FIELD(wrapped__ModelAnimation, "name", _value.name)
    }
};

PyObject* py_var(VM* vm, ModelAnimation v){
    return vm->new_user_object<wrapped__ModelAnimation>(v);
}
template<>
ModelAnimation py_cast<ModelAnimation>(VM* vm, PyObject* obj){
    return py_cast<wrapped__ModelAnimation&>(vm, obj)._value;
}
template<>
ModelAnimation _py_cast<ModelAnimation>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__ModelAnimation&>(vm, obj)._value;
}
/*************** Ray ***************/
struct wrapped__Ray{

    Ray _value;
    wrapped__Ray() = default;
    wrapped__Ray(const wrapped__Ray& other) = default;

    wrapped__Ray(const Ray& other){
        memcpy(&_value, &other, sizeof(Ray));
    }
    bool operator==(const wrapped__Ray& other) const{
        return memcmp(&_value, &other._value, sizeof(Ray)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"position", "direction"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 2) vm->TypeError(_S("expected 2 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Ray)
        PY_FIELD(wrapped__Ray, "position", _value.position)
        PY_FIELD(wrapped__Ray, "direction", _value.direction)
    }
};

PyObject* py_var(VM* vm, Ray v){
    return vm->new_user_object<wrapped__Ray>(v);
}
template<>
Ray py_cast<Ray>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Ray&>(vm, obj)._value;
}
template<>
Ray _py_cast<Ray>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Ray&>(vm, obj)._value;
}
/*************** RayCollision ***************/
struct wrapped__RayCollision{

    RayCollision _value;
    wrapped__RayCollision() = default;
    wrapped__RayCollision(const wrapped__RayCollision& other) = default;

    wrapped__RayCollision(const RayCollision& other){
        memcpy(&_value, &other, sizeof(RayCollision));
    }
    bool operator==(const wrapped__RayCollision& other) const{
        return memcmp(&_value, &other._value, sizeof(RayCollision)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"hit", "distance", "point", "normal"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 4) vm->TypeError(_S("expected 4 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__RayCollision)
        PY_FIELD(wrapped__RayCollision, "hit", _value.hit)
        PY_FIELD(wrapped__RayCollision, "distance", _value.distance)
        PY_FIELD(wrapped__RayCollision, "point", _value.point)
        PY_FIELD(wrapped__RayCollision, "normal", _value.normal)
    }
};

PyObject* py_var(VM* vm, RayCollision v){
    return vm->new_user_object<wrapped__RayCollision>(v);
}
template<>
RayCollision py_cast<RayCollision>(VM* vm, PyObject* obj){
    return py_cast<wrapped__RayCollision&>(vm, obj)._value;
}
template<>
RayCollision _py_cast<RayCollision>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__RayCollision&>(vm, obj)._value;
}
/*************** BoundingBox ***************/
struct wrapped__BoundingBox{

    BoundingBox _value;
    wrapped__BoundingBox() = default;
    wrapped__BoundingBox(const wrapped__BoundingBox& other) = default;

    wrapped__BoundingBox(const BoundingBox& other){
        memcpy(&_value, &other, sizeof(BoundingBox));
    }
    bool operator==(const wrapped__BoundingBox& other) const{
        return memcmp(&_value, &other._value, sizeof(BoundingBox)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"min", "max"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 2) vm->TypeError(_S("expected 2 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__BoundingBox)
        PY_FIELD(wrapped__BoundingBox, "min", _value.min)
        PY_FIELD(wrapped__BoundingBox, "max", _value.max)
    }
};

PyObject* py_var(VM* vm, BoundingBox v){
    return vm->new_user_object<wrapped__BoundingBox>(v);
}
template<>
BoundingBox py_cast<BoundingBox>(VM* vm, PyObject* obj){
    return py_cast<wrapped__BoundingBox&>(vm, obj)._value;
}
template<>
BoundingBox _py_cast<BoundingBox>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__BoundingBox&>(vm, obj)._value;
}
/*************** Wave ***************/
struct wrapped__Wave{

    Wave _value;
    wrapped__Wave() = default;
    wrapped__Wave(const wrapped__Wave& other) = default;

    wrapped__Wave(const Wave& other){
        memcpy(&_value, &other, sizeof(Wave));
    }
    bool operator==(const wrapped__Wave& other) const{
        return memcmp(&_value, &other._value, sizeof(Wave)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"frameCount", "sampleRate", "sampleSize", "channels", "data"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Wave)
        PY_FIELD(wrapped__Wave, "frameCount", _value.frameCount)
        PY_FIELD(wrapped__Wave, "sampleRate", _value.sampleRate)
        PY_FIELD(wrapped__Wave, "sampleSize", _value.sampleSize)
        PY_FIELD(wrapped__Wave, "channels", _value.channels)
        PY_FIELD(wrapped__Wave, "data", _value.data)
    }
};

PyObject* py_var(VM* vm, Wave v){
    return vm->new_user_object<wrapped__Wave>(v);
}
template<>
Wave py_cast<Wave>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Wave&>(vm, obj)._value;
}
template<>
Wave _py_cast<Wave>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Wave&>(vm, obj)._value;
}
/*************** AudioStream ***************/
struct wrapped__AudioStream{

    AudioStream _value;
    wrapped__AudioStream() = default;
    wrapped__AudioStream(const wrapped__AudioStream& other) = default;

    wrapped__AudioStream(const AudioStream& other){
        memcpy(&_value, &other, sizeof(AudioStream));
    }
    bool operator==(const wrapped__AudioStream& other) const{
        return memcmp(&_value, &other._value, sizeof(AudioStream)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"buffer", "processor", "sampleRate", "sampleSize", "channels"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__AudioStream)
        PY_FIELD(wrapped__AudioStream, "buffer", _value.buffer)
        PY_FIELD(wrapped__AudioStream, "processor", _value.processor)
        PY_FIELD(wrapped__AudioStream, "sampleRate", _value.sampleRate)
        PY_FIELD(wrapped__AudioStream, "sampleSize", _value.sampleSize)
        PY_FIELD(wrapped__AudioStream, "channels", _value.channels)
    }
};

PyObject* py_var(VM* vm, AudioStream v){
    return vm->new_user_object<wrapped__AudioStream>(v);
}
template<>
AudioStream py_cast<AudioStream>(VM* vm, PyObject* obj){
    return py_cast<wrapped__AudioStream&>(vm, obj)._value;
}
template<>
AudioStream _py_cast<AudioStream>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__AudioStream&>(vm, obj)._value;
}
/*************** Sound ***************/
struct wrapped__Sound{

    Sound _value;
    wrapped__Sound() = default;
    wrapped__Sound(const wrapped__Sound& other) = default;

    wrapped__Sound(const Sound& other){
        memcpy(&_value, &other, sizeof(Sound));
    }
    bool operator==(const wrapped__Sound& other) const{
        return memcmp(&_value, &other._value, sizeof(Sound)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"stream", "frameCount"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 2) vm->TypeError(_S("expected 2 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Sound)
        PY_FIELD(wrapped__Sound, "stream", _value.stream)
        PY_FIELD(wrapped__Sound, "frameCount", _value.frameCount)
    }
};

PyObject* py_var(VM* vm, Sound v){
    return vm->new_user_object<wrapped__Sound>(v);
}
template<>
Sound py_cast<Sound>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Sound&>(vm, obj)._value;
}
template<>
Sound _py_cast<Sound>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Sound&>(vm, obj)._value;
}
/*************** Music ***************/
struct wrapped__Music{

    Music _value;
    wrapped__Music() = default;
    wrapped__Music(const wrapped__Music& other) = default;

    wrapped__Music(const Music& other){
        memcpy(&_value, &other, sizeof(Music));
    }
    bool operator==(const wrapped__Music& other) const{
        return memcmp(&_value, &other._value, sizeof(Music)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"stream", "frameCount", "looping", "ctxType", "ctxData"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 5) vm->TypeError(_S("expected 5 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__Music)
        PY_FIELD(wrapped__Music, "stream", _value.stream)
        PY_FIELD(wrapped__Music, "frameCount", _value.frameCount)
        PY_FIELD(wrapped__Music, "looping", _value.looping)
        PY_FIELD(wrapped__Music, "ctxType", _value.ctxType)
        PY_FIELD(wrapped__Music, "ctxData", _value.ctxData)
    }
};

PyObject* py_var(VM* vm, Music v){
    return vm->new_user_object<wrapped__Music>(v);
}
template<>
Music py_cast<Music>(VM* vm, PyObject* obj){
    return py_cast<wrapped__Music&>(vm, obj)._value;
}
template<>
Music _py_cast<Music>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__Music&>(vm, obj)._value;
}
/*************** VrDeviceInfo ***************/
struct wrapped__VrDeviceInfo{

    VrDeviceInfo _value;
    wrapped__VrDeviceInfo() = default;
    wrapped__VrDeviceInfo(const wrapped__VrDeviceInfo& other) = default;

    wrapped__VrDeviceInfo(const VrDeviceInfo& other){
        memcpy(&_value, &other, sizeof(VrDeviceInfo));
    }
    bool operator==(const wrapped__VrDeviceInfo& other) const{
        return memcmp(&_value, &other._value, sizeof(VrDeviceInfo)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"hResolution", "vResolution", "hScreenSize", "vScreenSize", "eyeToScreenDistance", "lensSeparationDistance", "interpupillaryDistance", "lensDistortionValues", "chromaAbCorrection"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 9) vm->TypeError(_S("expected 9 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__VrDeviceInfo)
        PY_FIELD(wrapped__VrDeviceInfo, "hResolution", _value.hResolution)
        PY_FIELD(wrapped__VrDeviceInfo, "vResolution", _value.vResolution)
        PY_FIELD(wrapped__VrDeviceInfo, "hScreenSize", _value.hScreenSize)
        PY_FIELD(wrapped__VrDeviceInfo, "vScreenSize", _value.vScreenSize)
        PY_FIELD(wrapped__VrDeviceInfo, "eyeToScreenDistance", _value.eyeToScreenDistance)
        PY_FIELD(wrapped__VrDeviceInfo, "lensSeparationDistance", _value.lensSeparationDistance)
        PY_FIELD(wrapped__VrDeviceInfo, "interpupillaryDistance", _value.interpupillaryDistance)
        PY_READONLY_FIELD(wrapped__VrDeviceInfo, "lensDistortionValues", _value.lensDistortionValues)
        PY_READONLY_FIELD(wrapped__VrDeviceInfo, "chromaAbCorrection", _value.chromaAbCorrection)
    }
};

PyObject* py_var(VM* vm, VrDeviceInfo v){
    return vm->new_user_object<wrapped__VrDeviceInfo>(v);
}
template<>
VrDeviceInfo py_cast<VrDeviceInfo>(VM* vm, PyObject* obj){
    return py_cast<wrapped__VrDeviceInfo&>(vm, obj)._value;
}
template<>
VrDeviceInfo _py_cast<VrDeviceInfo>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__VrDeviceInfo&>(vm, obj)._value;
}
/*************** VrStereoConfig ***************/
struct wrapped__VrStereoConfig{

    VrStereoConfig _value;
    wrapped__VrStereoConfig() = default;
    wrapped__VrStereoConfig(const wrapped__VrStereoConfig& other) = default;

    wrapped__VrStereoConfig(const VrStereoConfig& other){
        memcpy(&_value, &other, sizeof(VrStereoConfig));
    }
    bool operator==(const wrapped__VrStereoConfig& other) const{
        return memcmp(&_value, &other._value, sizeof(VrStereoConfig)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"projection", "viewOffset", "leftLensCenter", "rightLensCenter", "leftScreenCenter", "rightScreenCenter", "scale", "scaleIn"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 8) vm->TypeError(_S("expected 8 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__VrStereoConfig)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "projection", _value.projection)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "viewOffset", _value.viewOffset)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "leftLensCenter", _value.leftLensCenter)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "rightLensCenter", _value.rightLensCenter)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "leftScreenCenter", _value.leftScreenCenter)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "rightScreenCenter", _value.rightScreenCenter)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "scale", _value.scale)
        PY_READONLY_FIELD(wrapped__VrStereoConfig, "scaleIn", _value.scaleIn)
    }
};

PyObject* py_var(VM* vm, VrStereoConfig v){
    return vm->new_user_object<wrapped__VrStereoConfig>(v);
}
template<>
VrStereoConfig py_cast<VrStereoConfig>(VM* vm, PyObject* obj){
    return py_cast<wrapped__VrStereoConfig&>(vm, obj)._value;
}
template<>
VrStereoConfig _py_cast<VrStereoConfig>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__VrStereoConfig&>(vm, obj)._value;
}
/*************** FilePathList ***************/
struct wrapped__FilePathList{

    FilePathList _value;
    wrapped__FilePathList() = default;
    wrapped__FilePathList(const wrapped__FilePathList& other) = default;

    wrapped__FilePathList(const FilePathList& other){
        memcpy(&_value, &other, sizeof(FilePathList));
    }
    bool operator==(const wrapped__FilePathList& other) const{
        return memcmp(&_value, &other._value, sizeof(FilePathList)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"capacity", "count", "paths"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__FilePathList)
        PY_FIELD(wrapped__FilePathList, "capacity", _value.capacity)
        PY_FIELD(wrapped__FilePathList, "count", _value.count)
        PY_FIELD(wrapped__FilePathList, "paths", _value.paths)
    }
};

PyObject* py_var(VM* vm, FilePathList v){
    return vm->new_user_object<wrapped__FilePathList>(v);
}
template<>
FilePathList py_cast<FilePathList>(VM* vm, PyObject* obj){
    return py_cast<wrapped__FilePathList&>(vm, obj)._value;
}
template<>
FilePathList _py_cast<FilePathList>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__FilePathList&>(vm, obj)._value;
}
/*************** AutomationEvent ***************/
struct wrapped__AutomationEvent{

    AutomationEvent _value;
    wrapped__AutomationEvent() = default;
    wrapped__AutomationEvent(const wrapped__AutomationEvent& other) = default;

    wrapped__AutomationEvent(const AutomationEvent& other){
        memcpy(&_value, &other, sizeof(AutomationEvent));
    }
    bool operator==(const wrapped__AutomationEvent& other) const{
        return memcmp(&_value, &other._value, sizeof(AutomationEvent)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"frame", "type", "params"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__AutomationEvent)
        PY_FIELD(wrapped__AutomationEvent, "frame", _value.frame)
        PY_FIELD(wrapped__AutomationEvent, "type", _value.type)
        PY_READONLY_FIELD(wrapped__AutomationEvent, "params", _value.params)
    }
};

PyObject* py_var(VM* vm, AutomationEvent v){
    return vm->new_user_object<wrapped__AutomationEvent>(v);
}
template<>
AutomationEvent py_cast<AutomationEvent>(VM* vm, PyObject* obj){
    return py_cast<wrapped__AutomationEvent&>(vm, obj)._value;
}
template<>
AutomationEvent _py_cast<AutomationEvent>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__AutomationEvent&>(vm, obj)._value;
}
/*************** AutomationEventList ***************/
struct wrapped__AutomationEventList{

    AutomationEventList _value;
    wrapped__AutomationEventList() = default;
    wrapped__AutomationEventList(const wrapped__AutomationEventList& other) = default;

    wrapped__AutomationEventList(const AutomationEventList& other){
        memcpy(&_value, &other, sizeof(AutomationEventList));
    }
    bool operator==(const wrapped__AutomationEventList& other) const{
        return memcmp(&_value, &other._value, sizeof(AutomationEventList)) == 0;
    }

    static void _register(VM* vm, PyObject* mod, PyObject* type){
        vm->bind_func(type, __init__, -1, [](VM* vm, ArgsView args){
            const StrName _fields_[] = {"capacity", "count", "events"};
            if(args.size() == 1) return vm->None;
            if(args.size()-1 != 3) vm->TypeError(_S("expected 3 arguments, got ", args.size()-1));
            for(int i=1; i<args.size(); i++){
                vm->setattr(args[0], _fields_[i-1], args[i]);
            }
            return vm->None;
        });
        PY_STRUCT_LIKE(wrapped__AutomationEventList)
        PY_FIELD(wrapped__AutomationEventList, "capacity", _value.capacity)
        PY_FIELD(wrapped__AutomationEventList, "count", _value.count)
        PY_FIELD(wrapped__AutomationEventList, "events", _value.events)
    }
};

PyObject* py_var(VM* vm, AutomationEventList v){
    return vm->new_user_object<wrapped__AutomationEventList>(v);
}
template<>
AutomationEventList py_cast<AutomationEventList>(VM* vm, PyObject* obj){
    return py_cast<wrapped__AutomationEventList&>(vm, obj)._value;
}
template<>
AutomationEventList _py_cast<AutomationEventList>(VM* vm, PyObject* obj){
    return _py_cast<wrapped__AutomationEventList&>(vm, obj)._value;
}
////////////////////////////////////////
void add_module_raylib(VM* vm){
    PyObject* mod = vm->new_module("raylib");

    // defines
    mod->attr().set("RAYLIB_VERSION_MAJOR", py_var(vm, 5));
    mod->attr().set("RAYLIB_VERSION_MINOR", py_var(vm, 1));
    mod->attr().set("RAYLIB_VERSION_PATCH", py_var(vm, 0));
    mod->attr().set("RAYLIB_VERSION", py_var(vm, "5.1-dev"));
    mod->attr().set("PI", py_var(vm, 3.141592653589793));
    // ConfigFlags
    _bind_enums(vm, mod, "ConfigFlags", {{"FLAG_VSYNC_HINT", 64}, {"FLAG_FULLSCREEN_MODE", 2}, {"FLAG_WINDOW_RESIZABLE", 4}, {"FLAG_WINDOW_UNDECORATED", 8}, {"FLAG_WINDOW_HIDDEN", 128}, {"FLAG_WINDOW_MINIMIZED", 512}, {"FLAG_WINDOW_MAXIMIZED", 1024}, {"FLAG_WINDOW_UNFOCUSED", 2048}, {"FLAG_WINDOW_TOPMOST", 4096}, {"FLAG_WINDOW_ALWAYS_RUN", 256}, {"FLAG_WINDOW_TRANSPARENT", 16}, {"FLAG_WINDOW_HIGHDPI", 8192}, {"FLAG_WINDOW_MOUSE_PASSTHROUGH", 16384}, {"FLAG_BORDERLESS_WINDOWED_MODE", 32768}, {"FLAG_MSAA_4X_HINT", 32}, {"FLAG_INTERLACED_HINT", 65536}});
    // TraceLogLevel
    _bind_enums(vm, mod, "TraceLogLevel", {{"LOG_ALL", 0}, {"LOG_TRACE", 1}, {"LOG_DEBUG", 2}, {"LOG_INFO", 3}, {"LOG_WARNING", 4}, {"LOG_ERROR", 5}, {"LOG_FATAL", 6}, {"LOG_NONE", 7}});
    // KeyboardKey
    _bind_enums(vm, mod, "KeyboardKey", {{"KEY_NULL", 0}, {"KEY_APOSTROPHE", 39}, {"KEY_COMMA", 44}, {"KEY_MINUS", 45}, {"KEY_PERIOD", 46}, {"KEY_SLASH", 47}, {"KEY_ZERO", 48}, {"KEY_ONE", 49}, {"KEY_TWO", 50}, {"KEY_THREE", 51}, {"KEY_FOUR", 52}, {"KEY_FIVE", 53}, {"KEY_SIX", 54}, {"KEY_SEVEN", 55}, {"KEY_EIGHT", 56}, {"KEY_NINE", 57}, {"KEY_SEMICOLON", 59}, {"KEY_EQUAL", 61}, {"KEY_A", 65}, {"KEY_B", 66}, {"KEY_C", 67}, {"KEY_D", 68}, {"KEY_E", 69}, {"KEY_F", 70}, {"KEY_G", 71}, {"KEY_H", 72}, {"KEY_I", 73}, {"KEY_J", 74}, {"KEY_K", 75}, {"KEY_L", 76}, {"KEY_M", 77}, {"KEY_N", 78}, {"KEY_O", 79}, {"KEY_P", 80}, {"KEY_Q", 81}, {"KEY_R", 82}, {"KEY_S", 83}, {"KEY_T", 84}, {"KEY_U", 85}, {"KEY_V", 86}, {"KEY_W", 87}, {"KEY_X", 88}, {"KEY_Y", 89}, {"KEY_Z", 90}, {"KEY_LEFT_BRACKET", 91}, {"KEY_BACKSLASH", 92}, {"KEY_RIGHT_BRACKET", 93}, {"KEY_GRAVE", 96}, {"KEY_SPACE", 32}, {"KEY_ESCAPE", 256}, {"KEY_ENTER", 257}, {"KEY_TAB", 258}, {"KEY_BACKSPACE", 259}, {"KEY_INSERT", 260}, {"KEY_DELETE", 261}, {"KEY_RIGHT", 262}, {"KEY_LEFT", 263}, {"KEY_DOWN", 264}, {"KEY_UP", 265}, {"KEY_PAGE_UP", 266}, {"KEY_PAGE_DOWN", 267}, {"KEY_HOME", 268}, {"KEY_END", 269}, {"KEY_CAPS_LOCK", 280}, {"KEY_SCROLL_LOCK", 281}, {"KEY_NUM_LOCK", 282}, {"KEY_PRINT_SCREEN", 283}, {"KEY_PAUSE", 284}, {"KEY_F1", 290}, {"KEY_F2", 291}, {"KEY_F3", 292}, {"KEY_F4", 293}, {"KEY_F5", 294}, {"KEY_F6", 295}, {"KEY_F7", 296}, {"KEY_F8", 297}, {"KEY_F9", 298}, {"KEY_F10", 299}, {"KEY_F11", 300}, {"KEY_F12", 301}, {"KEY_LEFT_SHIFT", 340}, {"KEY_LEFT_CONTROL", 341}, {"KEY_LEFT_ALT", 342}, {"KEY_LEFT_SUPER", 343}, {"KEY_RIGHT_SHIFT", 344}, {"KEY_RIGHT_CONTROL", 345}, {"KEY_RIGHT_ALT", 346}, {"KEY_RIGHT_SUPER", 347}, {"KEY_KB_MENU", 348}, {"KEY_KP_0", 320}, {"KEY_KP_1", 321}, {"KEY_KP_2", 322}, {"KEY_KP_3", 323}, {"KEY_KP_4", 324}, {"KEY_KP_5", 325}, {"KEY_KP_6", 326}, {"KEY_KP_7", 327}, {"KEY_KP_8", 328}, {"KEY_KP_9", 329}, {"KEY_KP_DECIMAL", 330}, {"KEY_KP_DIVIDE", 331}, {"KEY_KP_MULTIPLY", 332}, {"KEY_KP_SUBTRACT", 333}, {"KEY_KP_ADD", 334}, {"KEY_KP_ENTER", 335}, {"KEY_KP_EQUAL", 336}, {"KEY_BACK", 4}, {"KEY_MENU", 5}, {"KEY_VOLUME_UP", 24}, {"KEY_VOLUME_DOWN", 25}});
    // MouseButton
    _bind_enums(vm, mod, "MouseButton", {{"MOUSE_BUTTON_LEFT", 0}, {"MOUSE_BUTTON_RIGHT", 1}, {"MOUSE_BUTTON_MIDDLE", 2}, {"MOUSE_BUTTON_SIDE", 3}, {"MOUSE_BUTTON_EXTRA", 4}, {"MOUSE_BUTTON_FORWARD", 5}, {"MOUSE_BUTTON_BACK", 6}});
    // MouseCursor
    _bind_enums(vm, mod, "MouseCursor", {{"MOUSE_CURSOR_DEFAULT", 0}, {"MOUSE_CURSOR_ARROW", 1}, {"MOUSE_CURSOR_IBEAM", 2}, {"MOUSE_CURSOR_CROSSHAIR", 3}, {"MOUSE_CURSOR_POINTING_HAND", 4}, {"MOUSE_CURSOR_RESIZE_EW", 5}, {"MOUSE_CURSOR_RESIZE_NS", 6}, {"MOUSE_CURSOR_RESIZE_NWSE", 7}, {"MOUSE_CURSOR_RESIZE_NESW", 8}, {"MOUSE_CURSOR_RESIZE_ALL", 9}, {"MOUSE_CURSOR_NOT_ALLOWED", 10}});
    // GamepadButton
    _bind_enums(vm, mod, "GamepadButton", {{"GAMEPAD_BUTTON_UNKNOWN", 0}, {"GAMEPAD_BUTTON_LEFT_FACE_UP", 1}, {"GAMEPAD_BUTTON_LEFT_FACE_RIGHT", 2}, {"GAMEPAD_BUTTON_LEFT_FACE_DOWN", 3}, {"GAMEPAD_BUTTON_LEFT_FACE_LEFT", 4}, {"GAMEPAD_BUTTON_RIGHT_FACE_UP", 5}, {"GAMEPAD_BUTTON_RIGHT_FACE_RIGHT", 6}, {"GAMEPAD_BUTTON_RIGHT_FACE_DOWN", 7}, {"GAMEPAD_BUTTON_RIGHT_FACE_LEFT", 8}, {"GAMEPAD_BUTTON_LEFT_TRIGGER_1", 9}, {"GAMEPAD_BUTTON_LEFT_TRIGGER_2", 10}, {"GAMEPAD_BUTTON_RIGHT_TRIGGER_1", 11}, {"GAMEPAD_BUTTON_RIGHT_TRIGGER_2", 12}, {"GAMEPAD_BUTTON_MIDDLE_LEFT", 13}, {"GAMEPAD_BUTTON_MIDDLE", 14}, {"GAMEPAD_BUTTON_MIDDLE_RIGHT", 15}, {"GAMEPAD_BUTTON_LEFT_THUMB", 16}, {"GAMEPAD_BUTTON_RIGHT_THUMB", 17}});
    // GamepadAxis
    _bind_enums(vm, mod, "GamepadAxis", {{"GAMEPAD_AXIS_LEFT_X", 0}, {"GAMEPAD_AXIS_LEFT_Y", 1}, {"GAMEPAD_AXIS_RIGHT_X", 2}, {"GAMEPAD_AXIS_RIGHT_Y", 3}, {"GAMEPAD_AXIS_LEFT_TRIGGER", 4}, {"GAMEPAD_AXIS_RIGHT_TRIGGER", 5}});
    // MaterialMapIndex
    _bind_enums(vm, mod, "MaterialMapIndex", {{"MATERIAL_MAP_ALBEDO", 0}, {"MATERIAL_MAP_METALNESS", 1}, {"MATERIAL_MAP_NORMAL", 2}, {"MATERIAL_MAP_ROUGHNESS", 3}, {"MATERIAL_MAP_OCCLUSION", 4}, {"MATERIAL_MAP_EMISSION", 5}, {"MATERIAL_MAP_HEIGHT", 6}, {"MATERIAL_MAP_CUBEMAP", 7}, {"MATERIAL_MAP_IRRADIANCE", 8}, {"MATERIAL_MAP_PREFILTER", 9}, {"MATERIAL_MAP_BRDF", 10}});
    // ShaderLocationIndex
    _bind_enums(vm, mod, "ShaderLocationIndex", {{"SHADER_LOC_VERTEX_POSITION", 0}, {"SHADER_LOC_VERTEX_TEXCOORD01", 1}, {"SHADER_LOC_VERTEX_TEXCOORD02", 2}, {"SHADER_LOC_VERTEX_NORMAL", 3}, {"SHADER_LOC_VERTEX_TANGENT", 4}, {"SHADER_LOC_VERTEX_COLOR", 5}, {"SHADER_LOC_MATRIX_MVP", 6}, {"SHADER_LOC_MATRIX_VIEW", 7}, {"SHADER_LOC_MATRIX_PROJECTION", 8}, {"SHADER_LOC_MATRIX_MODEL", 9}, {"SHADER_LOC_MATRIX_NORMAL", 10}, {"SHADER_LOC_VECTOR_VIEW", 11}, {"SHADER_LOC_COLOR_DIFFUSE", 12}, {"SHADER_LOC_COLOR_SPECULAR", 13}, {"SHADER_LOC_COLOR_AMBIENT", 14}, {"SHADER_LOC_MAP_ALBEDO", 15}, {"SHADER_LOC_MAP_METALNESS", 16}, {"SHADER_LOC_MAP_NORMAL", 17}, {"SHADER_LOC_MAP_ROUGHNESS", 18}, {"SHADER_LOC_MAP_OCCLUSION", 19}, {"SHADER_LOC_MAP_EMISSION", 20}, {"SHADER_LOC_MAP_HEIGHT", 21}, {"SHADER_LOC_MAP_CUBEMAP", 22}, {"SHADER_LOC_MAP_IRRADIANCE", 23}, {"SHADER_LOC_MAP_PREFILTER", 24}, {"SHADER_LOC_MAP_BRDF", 25}});
    // ShaderUniformDataType
    _bind_enums(vm, mod, "ShaderUniformDataType", {{"SHADER_UNIFORM_FLOAT", 0}, {"SHADER_UNIFORM_VEC2", 1}, {"SHADER_UNIFORM_VEC3", 2}, {"SHADER_UNIFORM_VEC4", 3}, {"SHADER_UNIFORM_INT", 4}, {"SHADER_UNIFORM_IVEC2", 5}, {"SHADER_UNIFORM_IVEC3", 6}, {"SHADER_UNIFORM_IVEC4", 7}, {"SHADER_UNIFORM_SAMPLER2D", 8}});
    // ShaderAttributeDataType
    _bind_enums(vm, mod, "ShaderAttributeDataType", {{"SHADER_ATTRIB_FLOAT", 0}, {"SHADER_ATTRIB_VEC2", 1}, {"SHADER_ATTRIB_VEC3", 2}, {"SHADER_ATTRIB_VEC4", 3}});
    // PixelFormat
    _bind_enums(vm, mod, "PixelFormat", {{"PIXELFORMAT_UNCOMPRESSED_GRAYSCALE", 1}, {"PIXELFORMAT_UNCOMPRESSED_GRAY_ALPHA", 2}, {"PIXELFORMAT_UNCOMPRESSED_R5G6B5", 3}, {"PIXELFORMAT_UNCOMPRESSED_R8G8B8", 4}, {"PIXELFORMAT_UNCOMPRESSED_R5G5B5A1", 5}, {"PIXELFORMAT_UNCOMPRESSED_R4G4B4A4", 6}, {"PIXELFORMAT_UNCOMPRESSED_R8G8B8A8", 7}, {"PIXELFORMAT_UNCOMPRESSED_R32", 8}, {"PIXELFORMAT_UNCOMPRESSED_R32G32B32", 9}, {"PIXELFORMAT_UNCOMPRESSED_R32G32B32A32", 10}, {"PIXELFORMAT_UNCOMPRESSED_R16", 11}, {"PIXELFORMAT_UNCOMPRESSED_R16G16B16", 12}, {"PIXELFORMAT_UNCOMPRESSED_R16G16B16A16", 13}, {"PIXELFORMAT_COMPRESSED_DXT1_RGB", 14}, {"PIXELFORMAT_COMPRESSED_DXT1_RGBA", 15}, {"PIXELFORMAT_COMPRESSED_DXT3_RGBA", 16}, {"PIXELFORMAT_COMPRESSED_DXT5_RGBA", 17}, {"PIXELFORMAT_COMPRESSED_ETC1_RGB", 18}, {"PIXELFORMAT_COMPRESSED_ETC2_RGB", 19}, {"PIXELFORMAT_COMPRESSED_ETC2_EAC_RGBA", 20}, {"PIXELFORMAT_COMPRESSED_PVRT_RGB", 21}, {"PIXELFORMAT_COMPRESSED_PVRT_RGBA", 22}, {"PIXELFORMAT_COMPRESSED_ASTC_4x4_RGBA", 23}, {"PIXELFORMAT_COMPRESSED_ASTC_8x8_RGBA", 24}});
    // TextureFilter
    _bind_enums(vm, mod, "TextureFilter", {{"TEXTURE_FILTER_POINT", 0}, {"TEXTURE_FILTER_BILINEAR", 1}, {"TEXTURE_FILTER_TRILINEAR", 2}, {"TEXTURE_FILTER_ANISOTROPIC_4X", 3}, {"TEXTURE_FILTER_ANISOTROPIC_8X", 4}, {"TEXTURE_FILTER_ANISOTROPIC_16X", 5}});
    // TextureWrap
    _bind_enums(vm, mod, "TextureWrap", {{"TEXTURE_WRAP_REPEAT", 0}, {"TEXTURE_WRAP_CLAMP", 1}, {"TEXTURE_WRAP_MIRROR_REPEAT", 2}, {"TEXTURE_WRAP_MIRROR_CLAMP", 3}});
    // CubemapLayout
    _bind_enums(vm, mod, "CubemapLayout", {{"CUBEMAP_LAYOUT_AUTO_DETECT", 0}, {"CUBEMAP_LAYOUT_LINE_VERTICAL", 1}, {"CUBEMAP_LAYOUT_LINE_HORIZONTAL", 2}, {"CUBEMAP_LAYOUT_CROSS_THREE_BY_FOUR", 3}, {"CUBEMAP_LAYOUT_CROSS_FOUR_BY_THREE", 4}, {"CUBEMAP_LAYOUT_PANORAMA", 5}});
    // FontType
    _bind_enums(vm, mod, "FontType", {{"FONT_DEFAULT", 0}, {"FONT_BITMAP", 1}, {"FONT_SDF", 2}});
    // BlendMode
    _bind_enums(vm, mod, "BlendMode", {{"BLEND_ALPHA", 0}, {"BLEND_ADDITIVE", 1}, {"BLEND_MULTIPLIED", 2}, {"BLEND_ADD_COLORS", 3}, {"BLEND_SUBTRACT_COLORS", 4}, {"BLEND_ALPHA_PREMULTIPLY", 5}, {"BLEND_CUSTOM", 6}, {"BLEND_CUSTOM_SEPARATE", 7}});
    // Gesture
    _bind_enums(vm, mod, "Gesture", {{"GESTURE_NONE", 0}, {"GESTURE_TAP", 1}, {"GESTURE_DOUBLETAP", 2}, {"GESTURE_HOLD", 4}, {"GESTURE_DRAG", 8}, {"GESTURE_SWIPE_RIGHT", 16}, {"GESTURE_SWIPE_LEFT", 32}, {"GESTURE_SWIPE_UP", 64}, {"GESTURE_SWIPE_DOWN", 128}, {"GESTURE_PINCH_IN", 256}, {"GESTURE_PINCH_OUT", 512}});
    // CameraMode
    _bind_enums(vm, mod, "CameraMode", {{"CAMERA_CUSTOM", 0}, {"CAMERA_FREE", 1}, {"CAMERA_ORBITAL", 2}, {"CAMERA_FIRST_PERSON", 3}, {"CAMERA_THIRD_PERSON", 4}});
    // CameraProjection
    _bind_enums(vm, mod, "CameraProjection", {{"CAMERA_PERSPECTIVE", 0}, {"CAMERA_ORTHOGRAPHIC", 1}});
    // NPatchLayout
    _bind_enums(vm, mod, "NPatchLayout", {{"NPATCH_NINE_PATCH", 0}, {"NPATCH_THREE_PATCH_VERTICAL", 1}, {"NPATCH_THREE_PATCH_HORIZONTAL", 2}});

    vm->register_user_class<wrapped__Matrix>(mod, "Matrix");
    vm->register_user_class<wrapped__Color>(mod, "Color");
    vm->register_user_class<wrapped__Rectangle>(mod, "Rectangle");
    vm->register_user_class<wrapped__Image>(mod, "Image");
    vm->register_user_class<wrapped__Texture>(mod, "Texture");
    vm->register_user_class<wrapped__RenderTexture>(mod, "RenderTexture");
    vm->register_user_class<wrapped__NPatchInfo>(mod, "NPatchInfo");
    vm->register_user_class<wrapped__GlyphInfo>(mod, "GlyphInfo");
    vm->register_user_class<wrapped__Font>(mod, "Font");
    vm->register_user_class<wrapped__Camera3D>(mod, "Camera3D");
    vm->register_user_class<wrapped__Camera2D>(mod, "Camera2D");
    vm->register_user_class<wrapped__Mesh>(mod, "Mesh");
    vm->register_user_class<wrapped__Shader>(mod, "Shader");
    vm->register_user_class<wrapped__MaterialMap>(mod, "MaterialMap");
    vm->register_user_class<wrapped__Material>(mod, "Material");
    vm->register_user_class<wrapped__Transform>(mod, "Transform");
    vm->register_user_class<wrapped__BoneInfo>(mod, "BoneInfo");
    vm->register_user_class<wrapped__Model>(mod, "Model");
    vm->register_user_class<wrapped__ModelAnimation>(mod, "ModelAnimation");
    vm->register_user_class<wrapped__Ray>(mod, "Ray");
    vm->register_user_class<wrapped__RayCollision>(mod, "RayCollision");
    vm->register_user_class<wrapped__BoundingBox>(mod, "BoundingBox");
    vm->register_user_class<wrapped__Wave>(mod, "Wave");
    vm->register_user_class<wrapped__AudioStream>(mod, "AudioStream");
    vm->register_user_class<wrapped__Sound>(mod, "Sound");
    vm->register_user_class<wrapped__Music>(mod, "Music");
    vm->register_user_class<wrapped__VrDeviceInfo>(mod, "VrDeviceInfo");
    vm->register_user_class<wrapped__VrStereoConfig>(mod, "VrStereoConfig");
    vm->register_user_class<wrapped__FilePathList>(mod, "FilePathList");
    vm->register_user_class<wrapped__AutomationEvent>(mod, "AutomationEvent");
    vm->register_user_class<wrapped__AutomationEventList>(mod, "AutomationEventList");

    vm->bind(mod, "InitWindow(width: int, height: int, title: str) -> None", &InitWindow);
    vm->bind(mod, "CloseWindow() -> None", &CloseWindow);
    vm->bind(mod, "WindowShouldClose() -> bool", &WindowShouldClose);
    vm->bind(mod, "IsWindowReady() -> bool", &IsWindowReady);
    vm->bind(mod, "IsWindowFullscreen() -> bool", &IsWindowFullscreen);
    vm->bind(mod, "IsWindowHidden() -> bool", &IsWindowHidden);
    vm->bind(mod, "IsWindowMinimized() -> bool", &IsWindowMinimized);
    vm->bind(mod, "IsWindowMaximized() -> bool", &IsWindowMaximized);
    vm->bind(mod, "IsWindowFocused() -> bool", &IsWindowFocused);
    vm->bind(mod, "IsWindowResized() -> bool", &IsWindowResized);
    vm->bind(mod, "IsWindowState(flag: int) -> bool", &IsWindowState);
    vm->bind(mod, "SetWindowState(flags: int) -> None", &SetWindowState);
    vm->bind(mod, "ClearWindowState(flags: int) -> None", &ClearWindowState);
    vm->bind(mod, "ToggleFullscreen() -> None", &ToggleFullscreen);
    vm->bind(mod, "ToggleBorderlessWindowed() -> None", &ToggleBorderlessWindowed);
    vm->bind(mod, "MaximizeWindow() -> None", &MaximizeWindow);
    vm->bind(mod, "MinimizeWindow() -> None", &MinimizeWindow);
    vm->bind(mod, "RestoreWindow() -> None", &RestoreWindow);
    vm->bind(mod, "SetWindowIcon(image: Image) -> None", &SetWindowIcon);
    vm->bind(mod, "SetWindowIcons(images: 'Image_p', count: int) -> None", &SetWindowIcons);
    vm->bind(mod, "SetWindowTitle(title: str) -> None", &SetWindowTitle);
    vm->bind(mod, "SetWindowPosition(x: int, y: int) -> None", &SetWindowPosition);
    vm->bind(mod, "SetWindowMonitor(monitor: int) -> None", &SetWindowMonitor);
    vm->bind(mod, "SetWindowMinSize(width: int, height: int) -> None", &SetWindowMinSize);
    vm->bind(mod, "SetWindowMaxSize(width: int, height: int) -> None", &SetWindowMaxSize);
    vm->bind(mod, "SetWindowSize(width: int, height: int) -> None", &SetWindowSize);
    vm->bind(mod, "SetWindowOpacity(opacity: float) -> None", &SetWindowOpacity);
    vm->bind(mod, "SetWindowFocused() -> None", &SetWindowFocused);
    vm->bind(mod, "GetWindowHandle() -> void_p", &GetWindowHandle);
    vm->bind(mod, "GetScreenWidth() -> int", &GetScreenWidth);
    vm->bind(mod, "GetScreenHeight() -> int", &GetScreenHeight);
    vm->bind(mod, "GetRenderWidth() -> int", &GetRenderWidth);
    vm->bind(mod, "GetRenderHeight() -> int", &GetRenderHeight);
    vm->bind(mod, "GetMonitorCount() -> int", &GetMonitorCount);
    vm->bind(mod, "GetCurrentMonitor() -> int", &GetCurrentMonitor);
    vm->bind(mod, "GetMonitorPosition(monitor: int) -> vec2", &GetMonitorPosition);
    vm->bind(mod, "GetMonitorWidth(monitor: int) -> int", &GetMonitorWidth);
    vm->bind(mod, "GetMonitorHeight(monitor: int) -> int", &GetMonitorHeight);
    vm->bind(mod, "GetMonitorPhysicalWidth(monitor: int) -> int", &GetMonitorPhysicalWidth);
    vm->bind(mod, "GetMonitorPhysicalHeight(monitor: int) -> int", &GetMonitorPhysicalHeight);
    vm->bind(mod, "GetMonitorRefreshRate(monitor: int) -> int", &GetMonitorRefreshRate);
    vm->bind(mod, "GetWindowPosition() -> vec2", &GetWindowPosition);
    vm->bind(mod, "GetWindowScaleDPI() -> vec2", &GetWindowScaleDPI);
    vm->bind(mod, "GetMonitorName(monitor: int) -> str", &GetMonitorName);
    vm->bind(mod, "SetClipboardText(text: str) -> None", &SetClipboardText);
    vm->bind(mod, "GetClipboardText() -> str", &GetClipboardText);
    vm->bind(mod, "EnableEventWaiting() -> None", &EnableEventWaiting);
    vm->bind(mod, "DisableEventWaiting() -> None", &DisableEventWaiting);
    vm->bind(mod, "ShowCursor() -> None", &ShowCursor);
    vm->bind(mod, "HideCursor() -> None", &HideCursor);
    vm->bind(mod, "IsCursorHidden() -> bool", &IsCursorHidden);
    vm->bind(mod, "EnableCursor() -> None", &EnableCursor);
    vm->bind(mod, "DisableCursor() -> None", &DisableCursor);
    vm->bind(mod, "IsCursorOnScreen() -> bool", &IsCursorOnScreen);
    vm->bind(mod, "ClearBackground(color: Color) -> None", &ClearBackground);
    vm->bind(mod, "BeginDrawing() -> None", &BeginDrawing);
    vm->bind(mod, "EndDrawing() -> None", &EndDrawing);
    vm->bind(mod, "BeginMode2D(camera: Camera2D) -> None", &BeginMode2D);
    vm->bind(mod, "EndMode2D() -> None", &EndMode2D);
    vm->bind(mod, "BeginMode3D(camera: Camera3D) -> None", &BeginMode3D);
    vm->bind(mod, "EndMode3D() -> None", &EndMode3D);
    vm->bind(mod, "BeginTextureMode(target: RenderTexture2D) -> None", &BeginTextureMode);
    vm->bind(mod, "EndTextureMode() -> None", &EndTextureMode);
    vm->bind(mod, "BeginShaderMode(shader: Shader) -> None", &BeginShaderMode);
    vm->bind(mod, "EndShaderMode() -> None", &EndShaderMode);
    vm->bind(mod, "BeginBlendMode(mode: int) -> None", &BeginBlendMode);
    vm->bind(mod, "EndBlendMode() -> None", &EndBlendMode);
    vm->bind(mod, "BeginScissorMode(x: int, y: int, width: int, height: int) -> None", &BeginScissorMode);
    vm->bind(mod, "EndScissorMode() -> None", &EndScissorMode);
    vm->bind(mod, "BeginVrStereoMode(config: VrStereoConfig) -> None", &BeginVrStereoMode);
    vm->bind(mod, "EndVrStereoMode() -> None", &EndVrStereoMode);
    vm->bind(mod, "LoadVrStereoConfig(device: VrDeviceInfo) -> VrStereoConfig", &LoadVrStereoConfig);
    vm->bind(mod, "UnloadVrStereoConfig(config: VrStereoConfig) -> None", &UnloadVrStereoConfig);
    vm->bind(mod, "LoadShader(vsFileName: str, fsFileName: str) -> Shader", &LoadShader);
    vm->bind(mod, "LoadShaderFromMemory(vsCode: str, fsCode: str) -> Shader", &LoadShaderFromMemory);
    vm->bind(mod, "IsShaderReady(shader: Shader) -> bool", &IsShaderReady);
    vm->bind(mod, "GetShaderLocation(shader: Shader, uniformName: str) -> int", &GetShaderLocation);
    vm->bind(mod, "GetShaderLocationAttrib(shader: Shader, attribName: str) -> int", &GetShaderLocationAttrib);
    vm->bind(mod, "SetShaderValue(shader: Shader, locIndex: int, value: void_p, uniformType: int) -> None", &SetShaderValue);
    vm->bind(mod, "SetShaderValueV(shader: Shader, locIndex: int, value: void_p, uniformType: int, count: int) -> None", &SetShaderValueV);
    vm->bind(mod, "SetShaderValueMatrix(shader: Shader, locIndex: int, mat: Matrix) -> None", &SetShaderValueMatrix);
    vm->bind(mod, "SetShaderValueTexture(shader: Shader, locIndex: int, texture: Texture2D) -> None", &SetShaderValueTexture);
    vm->bind(mod, "UnloadShader(shader: Shader) -> None", &UnloadShader);
    vm->bind(mod, "GetScreenToWorldRay(position: vec2, camera: Camera) -> Ray", &GetScreenToWorldRay);
    vm->bind(mod, "GetScreenToWorldRayEx(position: vec2, camera: Camera, width: float, height: float) -> Ray", &GetScreenToWorldRayEx);
    vm->bind(mod, "GetWorldToScreen(position: vec3, camera: Camera) -> vec2", &GetWorldToScreen);
    vm->bind(mod, "GetWorldToScreenEx(position: vec3, camera: Camera, width: int, height: int) -> vec2", &GetWorldToScreenEx);
    vm->bind(mod, "GetWorldToScreen2D(position: vec2, camera: Camera2D) -> vec2", &GetWorldToScreen2D);
    vm->bind(mod, "GetScreenToWorld2D(position: vec2, camera: Camera2D) -> vec2", &GetScreenToWorld2D);
    vm->bind(mod, "GetCameraMatrix(camera: Camera) -> Matrix", &GetCameraMatrix);
    vm->bind(mod, "GetCameraMatrix2D(camera: Camera2D) -> Matrix", &GetCameraMatrix2D);
    vm->bind(mod, "SetTargetFPS(fps: int) -> None", &SetTargetFPS);
    vm->bind(mod, "GetFrameTime() -> float", &GetFrameTime);
    vm->bind(mod, "GetTime() -> float", &GetTime);
    vm->bind(mod, "GetFPS() -> int", &GetFPS);
    vm->bind(mod, "SwapScreenBuffer() -> None", &SwapScreenBuffer);
    vm->bind(mod, "PollInputEvents() -> None", &PollInputEvents);
    vm->bind(mod, "WaitTime(seconds: float) -> None", &WaitTime);
    vm->bind(mod, "SetRandomSeed(seed: int) -> None", &SetRandomSeed);
    vm->bind(mod, "GetRandomValue(min: int, max: int) -> int", &GetRandomValue);
    vm->bind(mod, "LoadRandomSequence(count: int, min: int, max: int) -> int_p", &LoadRandomSequence);
    vm->bind(mod, "UnloadRandomSequence(sequence: int_p) -> None", &UnloadRandomSequence);
    vm->bind(mod, "TakeScreenshot(fileName: str) -> None", &TakeScreenshot);
    vm->bind(mod, "SetConfigFlags(flags: int) -> None", &SetConfigFlags);
    vm->bind(mod, "OpenURL(url: str) -> None", &OpenURL);
    vm->bind(mod, "SetTraceLogLevel(logLevel: int) -> None", &SetTraceLogLevel);
    vm->bind(mod, "MemAlloc(size: int) -> void_p", &MemAlloc);
    vm->bind(mod, "MemRealloc(ptr: void_p, size: int) -> void_p", &MemRealloc);
    vm->bind(mod, "MemFree(ptr: void_p) -> None", &MemFree);
    vm->bind(mod, "LoadFileData(fileName: str, dataSize: int_p) -> uchar_p", &LoadFileData);
    vm->bind(mod, "UnloadFileData(data: uchar_p) -> None", &UnloadFileData);
    vm->bind(mod, "SaveFileData(fileName: str, data: void_p, dataSize: int) -> bool", &SaveFileData);
    vm->bind(mod, "ExportDataAsCode(data: uchar_p, dataSize: int, fileName: str) -> bool", &ExportDataAsCode);
    vm->bind(mod, "LoadFileText(fileName: str) -> char_p", &LoadFileText);
    vm->bind(mod, "UnloadFileText(text: char_p) -> None", &UnloadFileText);
    vm->bind(mod, "SaveFileText(fileName: str, text: char_p) -> bool", &SaveFileText);
    vm->bind(mod, "FileExists(fileName: str) -> bool", &FileExists);
    vm->bind(mod, "DirectoryExists(dirPath: str) -> bool", &DirectoryExists);
    vm->bind(mod, "IsFileExtension(fileName: str, ext: str) -> bool", &IsFileExtension);
    vm->bind(mod, "GetFileLength(fileName: str) -> int", &GetFileLength);
    vm->bind(mod, "GetFileExtension(fileName: str) -> str", &GetFileExtension);
    vm->bind(mod, "GetFileName(filePath: str) -> str", &GetFileName);
    vm->bind(mod, "GetFileNameWithoutExt(filePath: str) -> str", &GetFileNameWithoutExt);
    vm->bind(mod, "GetDirectoryPath(filePath: str) -> str", &GetDirectoryPath);
    vm->bind(mod, "GetPrevDirectoryPath(dirPath: str) -> str", &GetPrevDirectoryPath);
    vm->bind(mod, "GetWorkingDirectory() -> str", &GetWorkingDirectory);
    vm->bind(mod, "GetApplicationDirectory() -> str", &GetApplicationDirectory);
    vm->bind(mod, "ChangeDirectory(dir: str) -> bool", &ChangeDirectory);
    vm->bind(mod, "IsPathFile(path: str) -> bool", &IsPathFile);
    vm->bind(mod, "LoadDirectoryFiles(dirPath: str) -> FilePathList", &LoadDirectoryFiles);
    vm->bind(mod, "LoadDirectoryFilesEx(basePath: str, filter: str, scanSubdirs: bool) -> FilePathList", &LoadDirectoryFilesEx);
    vm->bind(mod, "UnloadDirectoryFiles(files: FilePathList) -> None", &UnloadDirectoryFiles);
    vm->bind(mod, "IsFileDropped() -> bool", &IsFileDropped);
    vm->bind(mod, "LoadDroppedFiles() -> FilePathList", &LoadDroppedFiles);
    vm->bind(mod, "UnloadDroppedFiles(files: FilePathList) -> None", &UnloadDroppedFiles);
    vm->bind(mod, "GetFileModTime(fileName: str) -> int", &GetFileModTime);
    vm->bind(mod, "CompressData(data: uchar_p, dataSize: int, compDataSize: int_p) -> uchar_p", &CompressData);
    vm->bind(mod, "DecompressData(compData: uchar_p, compDataSize: int, dataSize: int_p) -> uchar_p", &DecompressData);
    vm->bind(mod, "EncodeDataBase64(data: uchar_p, dataSize: int, outputSize: int_p) -> char_p", &EncodeDataBase64);
    vm->bind(mod, "DecodeDataBase64(data: uchar_p, outputSize: int_p) -> uchar_p", &DecodeDataBase64);
    vm->bind(mod, "LoadAutomationEventList(fileName: str) -> AutomationEventList", &LoadAutomationEventList);
    vm->bind(mod, "UnloadAutomationEventList(list: AutomationEventList) -> None", &UnloadAutomationEventList);
    vm->bind(mod, "ExportAutomationEventList(list: AutomationEventList, fileName: str) -> bool", &ExportAutomationEventList);
    vm->bind(mod, "SetAutomationEventList(list: 'AutomationEventList_p') -> None", &SetAutomationEventList);
    vm->bind(mod, "SetAutomationEventBaseFrame(frame: int) -> None", &SetAutomationEventBaseFrame);
    vm->bind(mod, "StartAutomationEventRecording() -> None", &StartAutomationEventRecording);
    vm->bind(mod, "StopAutomationEventRecording() -> None", &StopAutomationEventRecording);
    vm->bind(mod, "PlayAutomationEvent(event: AutomationEvent) -> None", &PlayAutomationEvent);
    vm->bind(mod, "IsKeyPressed(key: int) -> bool", &IsKeyPressed);
    vm->bind(mod, "IsKeyPressedRepeat(key: int) -> bool", &IsKeyPressedRepeat);
    vm->bind(mod, "IsKeyDown(key: int) -> bool", &IsKeyDown);
    vm->bind(mod, "IsKeyReleased(key: int) -> bool", &IsKeyReleased);
    vm->bind(mod, "IsKeyUp(key: int) -> bool", &IsKeyUp);
    vm->bind(mod, "GetKeyPressed() -> int", &GetKeyPressed);
    vm->bind(mod, "GetCharPressed() -> int", &GetCharPressed);
    vm->bind(mod, "SetExitKey(key: int) -> None", &SetExitKey);
    vm->bind(mod, "IsGamepadAvailable(gamepad: int) -> bool", &IsGamepadAvailable);
    vm->bind(mod, "GetGamepadName(gamepad: int) -> str", &GetGamepadName);
    vm->bind(mod, "IsGamepadButtonPressed(gamepad: int, button: int) -> bool", &IsGamepadButtonPressed);
    vm->bind(mod, "IsGamepadButtonDown(gamepad: int, button: int) -> bool", &IsGamepadButtonDown);
    vm->bind(mod, "IsGamepadButtonReleased(gamepad: int, button: int) -> bool", &IsGamepadButtonReleased);
    vm->bind(mod, "IsGamepadButtonUp(gamepad: int, button: int) -> bool", &IsGamepadButtonUp);
    vm->bind(mod, "GetGamepadButtonPressed() -> int", &GetGamepadButtonPressed);
    vm->bind(mod, "GetGamepadAxisCount(gamepad: int) -> int", &GetGamepadAxisCount);
    vm->bind(mod, "GetGamepadAxisMovement(gamepad: int, axis: int) -> float", &GetGamepadAxisMovement);
    vm->bind(mod, "SetGamepadMappings(mappings: str) -> int", &SetGamepadMappings);
    vm->bind(mod, "SetGamepadVibration(gamepad: int, leftMotor: float, rightMotor: float) -> None", &SetGamepadVibration);
    vm->bind(mod, "IsMouseButtonPressed(button: int) -> bool", &IsMouseButtonPressed);
    vm->bind(mod, "IsMouseButtonDown(button: int) -> bool", &IsMouseButtonDown);
    vm->bind(mod, "IsMouseButtonReleased(button: int) -> bool", &IsMouseButtonReleased);
    vm->bind(mod, "IsMouseButtonUp(button: int) -> bool", &IsMouseButtonUp);
    vm->bind(mod, "GetMouseX() -> int", &GetMouseX);
    vm->bind(mod, "GetMouseY() -> int", &GetMouseY);
    vm->bind(mod, "GetMousePosition() -> vec2", &GetMousePosition);
    vm->bind(mod, "GetMouseDelta() -> vec2", &GetMouseDelta);
    vm->bind(mod, "SetMousePosition(x: int, y: int) -> None", &SetMousePosition);
    vm->bind(mod, "SetMouseOffset(offsetX: int, offsetY: int) -> None", &SetMouseOffset);
    vm->bind(mod, "SetMouseScale(scaleX: float, scaleY: float) -> None", &SetMouseScale);
    vm->bind(mod, "GetMouseWheelMove() -> float", &GetMouseWheelMove);
    vm->bind(mod, "GetMouseWheelMoveV() -> vec2", &GetMouseWheelMoveV);
    vm->bind(mod, "SetMouseCursor(cursor: int) -> None", &SetMouseCursor);
    vm->bind(mod, "GetTouchX() -> int", &GetTouchX);
    vm->bind(mod, "GetTouchY() -> int", &GetTouchY);
    vm->bind(mod, "GetTouchPosition(index: int) -> vec2", &GetTouchPosition);
    vm->bind(mod, "GetTouchPointId(index: int) -> int", &GetTouchPointId);
    vm->bind(mod, "GetTouchPointCount() -> int", &GetTouchPointCount);
    vm->bind(mod, "SetGesturesEnabled(flags: int) -> None", &SetGesturesEnabled);
    vm->bind(mod, "IsGestureDetected(gesture: int) -> bool", &IsGestureDetected);
    vm->bind(mod, "GetGestureDetected() -> int", &GetGestureDetected);
    vm->bind(mod, "GetGestureHoldDuration() -> float", &GetGestureHoldDuration);
    vm->bind(mod, "GetGestureDragVector() -> vec2", &GetGestureDragVector);
    vm->bind(mod, "GetGestureDragAngle() -> float", &GetGestureDragAngle);
    vm->bind(mod, "GetGesturePinchVector() -> vec2", &GetGesturePinchVector);
    vm->bind(mod, "GetGesturePinchAngle() -> float", &GetGesturePinchAngle);
    vm->bind(mod, "UpdateCamera(camera: 'Camera_p', mode: int) -> None", &UpdateCamera);
    vm->bind(mod, "UpdateCameraPro(camera: 'Camera_p', movement: vec3, rotation: vec3, zoom: float) -> None", &UpdateCameraPro);
    vm->bind(mod, "SetShapesTexture(texture: Texture2D, source: Rectangle) -> None", &SetShapesTexture);
    vm->bind(mod, "GetShapesTexture() -> Texture2D", &GetShapesTexture);
    vm->bind(mod, "GetShapesTextureRectangle() -> Rectangle", &GetShapesTextureRectangle);
    vm->bind(mod, "DrawPixel(posX: int, posY: int, color: Color) -> None", &DrawPixel);
    vm->bind(mod, "DrawPixelV(position: vec2, color: Color) -> None", &DrawPixelV);
    vm->bind(mod, "DrawLine(startPosX: int, startPosY: int, endPosX: int, endPosY: int, color: Color) -> None", &DrawLine);
    vm->bind(mod, "DrawLineV(startPos: vec2, endPos: vec2, color: Color) -> None", &DrawLineV);
    vm->bind(mod, "DrawLineEx(startPos: vec2, endPos: vec2, thick: float, color: Color) -> None", &DrawLineEx);
    vm->bind(mod, "DrawLineStrip(points: 'vec2_p', pointCount: int, color: Color) -> None", &DrawLineStrip);
    vm->bind(mod, "DrawLineBezier(startPos: vec2, endPos: vec2, thick: float, color: Color) -> None", &DrawLineBezier);
    vm->bind(mod, "DrawCircle(centerX: int, centerY: int, radius: float, color: Color) -> None", &DrawCircle);
    vm->bind(mod, "DrawCircleSector(center: vec2, radius: float, startAngle: float, endAngle: float, segments: int, color: Color) -> None", &DrawCircleSector);
    vm->bind(mod, "DrawCircleSectorLines(center: vec2, radius: float, startAngle: float, endAngle: float, segments: int, color: Color) -> None", &DrawCircleSectorLines);
    vm->bind(mod, "DrawCircleGradient(centerX: int, centerY: int, radius: float, color1: Color, color2: Color) -> None", &DrawCircleGradient);
    vm->bind(mod, "DrawCircleV(center: vec2, radius: float, color: Color) -> None", &DrawCircleV);
    vm->bind(mod, "DrawCircleLines(centerX: int, centerY: int, radius: float, color: Color) -> None", &DrawCircleLines);
    vm->bind(mod, "DrawCircleLinesV(center: vec2, radius: float, color: Color) -> None", &DrawCircleLinesV);
    vm->bind(mod, "DrawEllipse(centerX: int, centerY: int, radiusH: float, radiusV: float, color: Color) -> None", &DrawEllipse);
    vm->bind(mod, "DrawEllipseLines(centerX: int, centerY: int, radiusH: float, radiusV: float, color: Color) -> None", &DrawEllipseLines);
    vm->bind(mod, "DrawRing(center: vec2, innerRadius: float, outerRadius: float, startAngle: float, endAngle: float, segments: int, color: Color) -> None", &DrawRing);
    vm->bind(mod, "DrawRingLines(center: vec2, innerRadius: float, outerRadius: float, startAngle: float, endAngle: float, segments: int, color: Color) -> None", &DrawRingLines);
    vm->bind(mod, "DrawRectangle(posX: int, posY: int, width: int, height: int, color: Color) -> None", &DrawRectangle);
    vm->bind(mod, "DrawRectangleV(position: vec2, size: vec2, color: Color) -> None", &DrawRectangleV);
    vm->bind(mod, "DrawRectangleRec(rec: Rectangle, color: Color) -> None", &DrawRectangleRec);
    vm->bind(mod, "DrawRectanglePro(rec: Rectangle, origin: vec2, rotation: float, color: Color) -> None", &DrawRectanglePro);
    vm->bind(mod, "DrawRectangleGradientV(posX: int, posY: int, width: int, height: int, color1: Color, color2: Color) -> None", &DrawRectangleGradientV);
    vm->bind(mod, "DrawRectangleGradientH(posX: int, posY: int, width: int, height: int, color1: Color, color2: Color) -> None", &DrawRectangleGradientH);
    vm->bind(mod, "DrawRectangleGradientEx(rec: Rectangle, col1: Color, col2: Color, col3: Color, col4: Color) -> None", &DrawRectangleGradientEx);
    vm->bind(mod, "DrawRectangleLines(posX: int, posY: int, width: int, height: int, color: Color) -> None", &DrawRectangleLines);
    vm->bind(mod, "DrawRectangleLinesEx(rec: Rectangle, lineThick: float, color: Color) -> None", &DrawRectangleLinesEx);
    vm->bind(mod, "DrawRectangleRounded(rec: Rectangle, roundness: float, segments: int, color: Color) -> None", &DrawRectangleRounded);
    vm->bind(mod, "DrawRectangleRoundedLines(rec: Rectangle, roundness: float, segments: int, lineThick: float, color: Color) -> None", &DrawRectangleRoundedLines);
    vm->bind(mod, "DrawTriangle(v1: vec2, v2: vec2, v3: vec2, color: Color) -> None", &DrawTriangle);
    vm->bind(mod, "DrawTriangleLines(v1: vec2, v2: vec2, v3: vec2, color: Color) -> None", &DrawTriangleLines);
    vm->bind(mod, "DrawTriangleFan(points: 'vec2_p', pointCount: int, color: Color) -> None", &DrawTriangleFan);
    vm->bind(mod, "DrawTriangleStrip(points: 'vec2_p', pointCount: int, color: Color) -> None", &DrawTriangleStrip);
    vm->bind(mod, "DrawPoly(center: vec2, sides: int, radius: float, rotation: float, color: Color) -> None", &DrawPoly);
    vm->bind(mod, "DrawPolyLines(center: vec2, sides: int, radius: float, rotation: float, color: Color) -> None", &DrawPolyLines);
    vm->bind(mod, "DrawPolyLinesEx(center: vec2, sides: int, radius: float, rotation: float, lineThick: float, color: Color) -> None", &DrawPolyLinesEx);
    vm->bind(mod, "DrawSplineLinear(points: 'vec2_p', pointCount: int, thick: float, color: Color) -> None", &DrawSplineLinear);
    vm->bind(mod, "DrawSplineBasis(points: 'vec2_p', pointCount: int, thick: float, color: Color) -> None", &DrawSplineBasis);
    vm->bind(mod, "DrawSplineCatmullRom(points: 'vec2_p', pointCount: int, thick: float, color: Color) -> None", &DrawSplineCatmullRom);
    vm->bind(mod, "DrawSplineBezierQuadratic(points: 'vec2_p', pointCount: int, thick: float, color: Color) -> None", &DrawSplineBezierQuadratic);
    vm->bind(mod, "DrawSplineBezierCubic(points: 'vec2_p', pointCount: int, thick: float, color: Color) -> None", &DrawSplineBezierCubic);
    vm->bind(mod, "DrawSplineSegmentLinear(p1: vec2, p2: vec2, thick: float, color: Color) -> None", &DrawSplineSegmentLinear);
    vm->bind(mod, "DrawSplineSegmentBasis(p1: vec2, p2: vec2, p3: vec2, p4: vec2, thick: float, color: Color) -> None", &DrawSplineSegmentBasis);
    vm->bind(mod, "DrawSplineSegmentCatmullRom(p1: vec2, p2: vec2, p3: vec2, p4: vec2, thick: float, color: Color) -> None", &DrawSplineSegmentCatmullRom);
    vm->bind(mod, "DrawSplineSegmentBezierQuadratic(p1: vec2, c2: vec2, p3: vec2, thick: float, color: Color) -> None", &DrawSplineSegmentBezierQuadratic);
    vm->bind(mod, "DrawSplineSegmentBezierCubic(p1: vec2, c2: vec2, c3: vec2, p4: vec2, thick: float, color: Color) -> None", &DrawSplineSegmentBezierCubic);
    vm->bind(mod, "GetSplinePointLinear(startPos: vec2, endPos: vec2, t: float) -> vec2", &GetSplinePointLinear);
    vm->bind(mod, "GetSplinePointBasis(p1: vec2, p2: vec2, p3: vec2, p4: vec2, t: float) -> vec2", &GetSplinePointBasis);
    vm->bind(mod, "GetSplinePointCatmullRom(p1: vec2, p2: vec2, p3: vec2, p4: vec2, t: float) -> vec2", &GetSplinePointCatmullRom);
    vm->bind(mod, "GetSplinePointBezierQuad(p1: vec2, c2: vec2, p3: vec2, t: float) -> vec2", &GetSplinePointBezierQuad);
    vm->bind(mod, "GetSplinePointBezierCubic(p1: vec2, c2: vec2, c3: vec2, p4: vec2, t: float) -> vec2", &GetSplinePointBezierCubic);
    vm->bind(mod, "CheckCollisionRecs(rec1: Rectangle, rec2: Rectangle) -> bool", &CheckCollisionRecs);
    vm->bind(mod, "CheckCollisionCircles(center1: vec2, radius1: float, center2: vec2, radius2: float) -> bool", &CheckCollisionCircles);
    vm->bind(mod, "CheckCollisionCircleRec(center: vec2, radius: float, rec: Rectangle) -> bool", &CheckCollisionCircleRec);
    vm->bind(mod, "CheckCollisionPointRec(point: vec2, rec: Rectangle) -> bool", &CheckCollisionPointRec);
    vm->bind(mod, "CheckCollisionPointCircle(point: vec2, center: vec2, radius: float) -> bool", &CheckCollisionPointCircle);
    vm->bind(mod, "CheckCollisionPointTriangle(point: vec2, p1: vec2, p2: vec2, p3: vec2) -> bool", &CheckCollisionPointTriangle);
    vm->bind(mod, "CheckCollisionPointPoly(point: vec2, points: 'vec2_p', pointCount: int) -> bool", &CheckCollisionPointPoly);
    vm->bind(mod, "CheckCollisionLines(startPos1: vec2, endPos1: vec2, startPos2: vec2, endPos2: vec2, collisionPoint: 'vec2_p') -> bool", &CheckCollisionLines);
    vm->bind(mod, "CheckCollisionPointLine(point: vec2, p1: vec2, p2: vec2, threshold: int) -> bool", &CheckCollisionPointLine);
    vm->bind(mod, "GetCollisionRec(rec1: Rectangle, rec2: Rectangle) -> Rectangle", &GetCollisionRec);
    vm->bind(mod, "LoadImage(fileName: str) -> Image", &LoadImage);
    vm->bind(mod, "LoadImageRaw(fileName: str, width: int, height: int, format: int, headerSize: int) -> Image", &LoadImageRaw);
    vm->bind(mod, "LoadImageSvg(fileNameOrString: str, width: int, height: int) -> Image", &LoadImageSvg);
    vm->bind(mod, "LoadImageAnim(fileName: str, frames: int_p) -> Image", &LoadImageAnim);
    vm->bind(mod, "LoadImageAnimFromMemory(fileType: str, fileData: uchar_p, dataSize: int, frames: int_p) -> Image", &LoadImageAnimFromMemory);
    vm->bind(mod, "LoadImageFromMemory(fileType: str, fileData: uchar_p, dataSize: int) -> Image", &LoadImageFromMemory);
    vm->bind(mod, "LoadImageFromTexture(texture: Texture2D) -> Image", &LoadImageFromTexture);
    vm->bind(mod, "LoadImageFromScreen() -> Image", &LoadImageFromScreen);
    vm->bind(mod, "IsImageReady(image: Image) -> bool", &IsImageReady);
    vm->bind(mod, "UnloadImage(image: Image) -> None", &UnloadImage);
    vm->bind(mod, "ExportImage(image: Image, fileName: str) -> bool", &ExportImage);
    vm->bind(mod, "ExportImageToMemory(image: Image, fileType: str, fileSize: int_p) -> uchar_p", &ExportImageToMemory);
    vm->bind(mod, "ExportImageAsCode(image: Image, fileName: str) -> bool", &ExportImageAsCode);
    vm->bind(mod, "GenImageColor(width: int, height: int, color: Color) -> Image", &GenImageColor);
    vm->bind(mod, "GenImageGradientLinear(width: int, height: int, direction: int, start: Color, end: Color) -> Image", &GenImageGradientLinear);
    vm->bind(mod, "GenImageGradientRadial(width: int, height: int, density: float, inner: Color, outer: Color) -> Image", &GenImageGradientRadial);
    vm->bind(mod, "GenImageGradientSquare(width: int, height: int, density: float, inner: Color, outer: Color) -> Image", &GenImageGradientSquare);
    vm->bind(mod, "GenImageChecked(width: int, height: int, checksX: int, checksY: int, col1: Color, col2: Color) -> Image", &GenImageChecked);
    vm->bind(mod, "GenImageWhiteNoise(width: int, height: int, factor: float) -> Image", &GenImageWhiteNoise);
    vm->bind(mod, "GenImagePerlinNoise(width: int, height: int, offsetX: int, offsetY: int, scale: float) -> Image", &GenImagePerlinNoise);
    vm->bind(mod, "GenImageCellular(width: int, height: int, tileSize: int) -> Image", &GenImageCellular);
    vm->bind(mod, "GenImageText(width: int, height: int, text: str) -> Image", &GenImageText);
    vm->bind(mod, "ImageCopy(image: Image) -> Image", &ImageCopy);
    vm->bind(mod, "ImageFromImage(image: Image, rec: Rectangle) -> Image", &ImageFromImage);
    vm->bind(mod, "ImageText(text: str, fontSize: int, color: Color) -> Image", &ImageText);
    vm->bind(mod, "ImageTextEx(font: Font, text: str, fontSize: float, spacing: float, tint: Color) -> Image", &ImageTextEx);
    vm->bind(mod, "ImageFormat(image: 'Image_p', newFormat: int) -> None", &ImageFormat);
    vm->bind(mod, "ImageToPOT(image: 'Image_p', fill: Color) -> None", &ImageToPOT);
    vm->bind(mod, "ImageCrop(image: 'Image_p', crop: Rectangle) -> None", &ImageCrop);
    vm->bind(mod, "ImageAlphaCrop(image: 'Image_p', threshold: float) -> None", &ImageAlphaCrop);
    vm->bind(mod, "ImageAlphaClear(image: 'Image_p', color: Color, threshold: float) -> None", &ImageAlphaClear);
    vm->bind(mod, "ImageAlphaMask(image: 'Image_p', alphaMask: Image) -> None", &ImageAlphaMask);
    vm->bind(mod, "ImageAlphaPremultiply(image: 'Image_p') -> None", &ImageAlphaPremultiply);
    vm->bind(mod, "ImageBlurGaussian(image: 'Image_p', blurSize: int) -> None", &ImageBlurGaussian);
    vm->bind(mod, "ImageKernelConvolution(image: 'Image_p', kernel: float_p, kernelSize: int) -> None", &ImageKernelConvolution);
    vm->bind(mod, "ImageResize(image: 'Image_p', newWidth: int, newHeight: int) -> None", &ImageResize);
    vm->bind(mod, "ImageResizeNN(image: 'Image_p', newWidth: int, newHeight: int) -> None", &ImageResizeNN);
    vm->bind(mod, "ImageResizeCanvas(image: 'Image_p', newWidth: int, newHeight: int, offsetX: int, offsetY: int, fill: Color) -> None", &ImageResizeCanvas);
    vm->bind(mod, "ImageMipmaps(image: 'Image_p') -> None", &ImageMipmaps);
    vm->bind(mod, "ImageDither(image: 'Image_p', rBpp: int, gBpp: int, bBpp: int, aBpp: int) -> None", &ImageDither);
    vm->bind(mod, "ImageFlipVertical(image: 'Image_p') -> None", &ImageFlipVertical);
    vm->bind(mod, "ImageFlipHorizontal(image: 'Image_p') -> None", &ImageFlipHorizontal);
    vm->bind(mod, "ImageRotate(image: 'Image_p', degrees: int) -> None", &ImageRotate);
    vm->bind(mod, "ImageRotateCW(image: 'Image_p') -> None", &ImageRotateCW);
    vm->bind(mod, "ImageRotateCCW(image: 'Image_p') -> None", &ImageRotateCCW);
    vm->bind(mod, "ImageColorTint(image: 'Image_p', color: Color) -> None", &ImageColorTint);
    vm->bind(mod, "ImageColorInvert(image: 'Image_p') -> None", &ImageColorInvert);
    vm->bind(mod, "ImageColorGrayscale(image: 'Image_p') -> None", &ImageColorGrayscale);
    vm->bind(mod, "ImageColorContrast(image: 'Image_p', contrast: float) -> None", &ImageColorContrast);
    vm->bind(mod, "ImageColorBrightness(image: 'Image_p', brightness: int) -> None", &ImageColorBrightness);
    vm->bind(mod, "ImageColorReplace(image: 'Image_p', color: Color, replace: Color) -> None", &ImageColorReplace);
    vm->bind(mod, "LoadImageColors(image: Image) -> 'Color_p'", &LoadImageColors);
    vm->bind(mod, "LoadImagePalette(image: Image, maxPaletteSize: int, colorCount: int_p) -> 'Color_p'", &LoadImagePalette);
    vm->bind(mod, "UnloadImageColors(colors: 'Color_p') -> None", &UnloadImageColors);
    vm->bind(mod, "UnloadImagePalette(colors: 'Color_p') -> None", &UnloadImagePalette);
    vm->bind(mod, "GetImageAlphaBorder(image: Image, threshold: float) -> Rectangle", &GetImageAlphaBorder);
    vm->bind(mod, "GetImageColor(image: Image, x: int, y: int) -> Color", &GetImageColor);
    vm->bind(mod, "ImageClearBackground(dst: 'Image_p', color: Color) -> None", &ImageClearBackground);
    vm->bind(mod, "ImageDrawPixel(dst: 'Image_p', posX: int, posY: int, color: Color) -> None", &ImageDrawPixel);
    vm->bind(mod, "ImageDrawPixelV(dst: 'Image_p', position: vec2, color: Color) -> None", &ImageDrawPixelV);
    vm->bind(mod, "ImageDrawLine(dst: 'Image_p', startPosX: int, startPosY: int, endPosX: int, endPosY: int, color: Color) -> None", &ImageDrawLine);
    vm->bind(mod, "ImageDrawLineV(dst: 'Image_p', start: vec2, end: vec2, color: Color) -> None", &ImageDrawLineV);
    vm->bind(mod, "ImageDrawCircle(dst: 'Image_p', centerX: int, centerY: int, radius: int, color: Color) -> None", &ImageDrawCircle);
    vm->bind(mod, "ImageDrawCircleV(dst: 'Image_p', center: vec2, radius: int, color: Color) -> None", &ImageDrawCircleV);
    vm->bind(mod, "ImageDrawCircleLines(dst: 'Image_p', centerX: int, centerY: int, radius: int, color: Color) -> None", &ImageDrawCircleLines);
    vm->bind(mod, "ImageDrawCircleLinesV(dst: 'Image_p', center: vec2, radius: int, color: Color) -> None", &ImageDrawCircleLinesV);
    vm->bind(mod, "ImageDrawRectangle(dst: 'Image_p', posX: int, posY: int, width: int, height: int, color: Color) -> None", &ImageDrawRectangle);
    vm->bind(mod, "ImageDrawRectangleV(dst: 'Image_p', position: vec2, size: vec2, color: Color) -> None", &ImageDrawRectangleV);
    vm->bind(mod, "ImageDrawRectangleRec(dst: 'Image_p', rec: Rectangle, color: Color) -> None", &ImageDrawRectangleRec);
    vm->bind(mod, "ImageDrawRectangleLines(dst: 'Image_p', rec: Rectangle, thick: int, color: Color) -> None", &ImageDrawRectangleLines);
    vm->bind(mod, "ImageDraw(dst: 'Image_p', src: Image, srcRec: Rectangle, dstRec: Rectangle, tint: Color) -> None", &ImageDraw);
    vm->bind(mod, "ImageDrawText(dst: 'Image_p', text: str, posX: int, posY: int, fontSize: int, color: Color) -> None", &ImageDrawText);
    vm->bind(mod, "ImageDrawTextEx(dst: 'Image_p', font: Font, text: str, position: vec2, fontSize: float, spacing: float, tint: Color) -> None", &ImageDrawTextEx);
    vm->bind(mod, "LoadTexture(fileName: str) -> Texture2D", &LoadTexture);
    vm->bind(mod, "LoadTextureFromImage(image: Image) -> Texture2D", &LoadTextureFromImage);
    vm->bind(mod, "LoadTextureCubemap(image: Image, layout: int) -> TextureCubemap", &LoadTextureCubemap);
    vm->bind(mod, "LoadRenderTexture(width: int, height: int) -> RenderTexture2D", &LoadRenderTexture);
    vm->bind(mod, "IsTextureReady(texture: Texture2D) -> bool", &IsTextureReady);
    vm->bind(mod, "UnloadTexture(texture: Texture2D) -> None", &UnloadTexture);
    vm->bind(mod, "IsRenderTextureReady(target: RenderTexture2D) -> bool", &IsRenderTextureReady);
    vm->bind(mod, "UnloadRenderTexture(target: RenderTexture2D) -> None", &UnloadRenderTexture);
    vm->bind(mod, "UpdateTexture(texture: Texture2D, pixels: void_p) -> None", &UpdateTexture);
    vm->bind(mod, "UpdateTextureRec(texture: Texture2D, rec: Rectangle, pixels: void_p) -> None", &UpdateTextureRec);
    vm->bind(mod, "GenTextureMipmaps(texture: 'Texture2D_p') -> None", &GenTextureMipmaps);
    vm->bind(mod, "SetTextureFilter(texture: Texture2D, filter: int) -> None", &SetTextureFilter);
    vm->bind(mod, "SetTextureWrap(texture: Texture2D, wrap: int) -> None", &SetTextureWrap);
    vm->bind(mod, "DrawTexture(texture: Texture2D, posX: int, posY: int, tint: Color) -> None", &DrawTexture);
    vm->bind(mod, "DrawTextureV(texture: Texture2D, position: vec2, tint: Color) -> None", &DrawTextureV);
    vm->bind(mod, "DrawTextureEx(texture: Texture2D, position: vec2, rotation: float, scale: float, tint: Color) -> None", &DrawTextureEx);
    vm->bind(mod, "DrawTextureRec(texture: Texture2D, source: Rectangle, position: vec2, tint: Color) -> None", &DrawTextureRec);
    vm->bind(mod, "DrawTexturePro(texture: Texture2D, source: Rectangle, dest: Rectangle, origin: vec2, rotation: float, tint: Color) -> None", &DrawTexturePro);
    vm->bind(mod, "DrawTextureNPatch(texture: Texture2D, nPatchInfo: NPatchInfo, dest: Rectangle, origin: vec2, rotation: float, tint: Color) -> None", &DrawTextureNPatch);
    vm->bind(mod, "ColorIsEqual(col1: Color, col2: Color) -> bool", &ColorIsEqual);
    vm->bind(mod, "Fade(color: Color, alpha: float) -> Color", &Fade);
    vm->bind(mod, "ColorToInt(color: Color) -> int", &ColorToInt);
    vm->bind(mod, "ColorNormalize(color: Color) -> vec4", &ColorNormalize);
    vm->bind(mod, "ColorFromNormalized(normalized: vec4) -> Color", &ColorFromNormalized);
    vm->bind(mod, "ColorToHSV(color: Color) -> vec3", &ColorToHSV);
    vm->bind(mod, "ColorFromHSV(hue: float, saturation: float, value: float) -> Color", &ColorFromHSV);
    vm->bind(mod, "ColorTint(color: Color, tint: Color) -> Color", &ColorTint);
    vm->bind(mod, "ColorBrightness(color: Color, factor: float) -> Color", &ColorBrightness);
    vm->bind(mod, "ColorContrast(color: Color, contrast: float) -> Color", &ColorContrast);
    vm->bind(mod, "ColorAlpha(color: Color, alpha: float) -> Color", &ColorAlpha);
    vm->bind(mod, "ColorAlphaBlend(dst: Color, src: Color, tint: Color) -> Color", &ColorAlphaBlend);
    vm->bind(mod, "GetColor(hexValue: int) -> Color", &GetColor);
    vm->bind(mod, "GetPixelColor(srcPtr: void_p, format: int) -> Color", &GetPixelColor);
    vm->bind(mod, "SetPixelColor(dstPtr: void_p, color: Color, format: int) -> None", &SetPixelColor);
    vm->bind(mod, "GetPixelDataSize(width: int, height: int, format: int) -> int", &GetPixelDataSize);
    vm->bind(mod, "GetFontDefault() -> Font", &GetFontDefault);
    vm->bind(mod, "LoadFont(fileName: str) -> Font", &LoadFont);
    vm->bind(mod, "LoadFontEx(fileName: str, fontSize: int, codepoints: int_p, codepointCount: int) -> Font", &LoadFontEx);
    vm->bind(mod, "LoadFontFromImage(image: Image, key: Color, firstChar: int) -> Font", &LoadFontFromImage);
    vm->bind(mod, "LoadFontFromMemory(fileType: str, fileData: uchar_p, dataSize: int, fontSize: int, codepoints: int_p, codepointCount: int) -> Font", &LoadFontFromMemory);
    vm->bind(mod, "IsFontReady(font: Font) -> bool", &IsFontReady);
    vm->bind(mod, "LoadFontData(fileData: uchar_p, dataSize: int, fontSize: int, codepoints: int_p, codepointCount: int, type: int) -> 'GlyphInfo_p'", &LoadFontData);
    vm->bind(mod, "GenImageFontAtlas(glyphs: 'GlyphInfo_p', glyphRecs: void_p, glyphCount: int, fontSize: int, padding: int, packMethod: int) -> Image", &GenImageFontAtlas);
    vm->bind(mod, "UnloadFontData(glyphs: 'GlyphInfo_p', glyphCount: int) -> None", &UnloadFontData);
    vm->bind(mod, "UnloadFont(font: Font) -> None", &UnloadFont);
    vm->bind(mod, "ExportFontAsCode(font: Font, fileName: str) -> bool", &ExportFontAsCode);
    vm->bind(mod, "DrawFPS(posX: int, posY: int) -> None", &DrawFPS);
    vm->bind(mod, "DrawText(text: str, posX: int, posY: int, fontSize: int, color: Color) -> None", &DrawText);
    vm->bind(mod, "DrawTextEx(font: Font, text: str, position: vec2, fontSize: float, spacing: float, tint: Color) -> None", &DrawTextEx);
    vm->bind(mod, "DrawTextPro(font: Font, text: str, position: vec2, origin: vec2, rotation: float, fontSize: float, spacing: float, tint: Color) -> None", &DrawTextPro);
    vm->bind(mod, "DrawTextCodepoint(font: Font, codepoint: int, position: vec2, fontSize: float, tint: Color) -> None", &DrawTextCodepoint);
    vm->bind(mod, "DrawTextCodepoints(font: Font, codepoints: int_p, codepointCount: int, position: vec2, fontSize: float, spacing: float, tint: Color) -> None", &DrawTextCodepoints);
    vm->bind(mod, "SetTextLineSpacing(spacing: int) -> None", &SetTextLineSpacing);
    vm->bind(mod, "MeasureText(text: str, fontSize: int) -> int", &MeasureText);
    vm->bind(mod, "MeasureTextEx(font: Font, text: str, fontSize: float, spacing: float) -> vec2", &MeasureTextEx);
    vm->bind(mod, "GetGlyphIndex(font: Font, codepoint: int) -> int", &GetGlyphIndex);
    vm->bind(mod, "GetGlyphInfo(font: Font, codepoint: int) -> GlyphInfo", &GetGlyphInfo);
    vm->bind(mod, "GetGlyphAtlasRec(font: Font, codepoint: int) -> Rectangle", &GetGlyphAtlasRec);
    vm->bind(mod, "LoadUTF8(codepoints: int_p, length: int) -> char_p", &LoadUTF8);
    vm->bind(mod, "UnloadUTF8(text: char_p) -> None", &UnloadUTF8);
    vm->bind(mod, "LoadCodepoints(text: str, count: int_p) -> int_p", &LoadCodepoints);
    vm->bind(mod, "UnloadCodepoints(codepoints: int_p) -> None", &UnloadCodepoints);
    vm->bind(mod, "GetCodepointCount(text: str) -> int", &GetCodepointCount);
    vm->bind(mod, "GetCodepoint(text: str, codepointSize: int_p) -> int", &GetCodepoint);
    vm->bind(mod, "GetCodepointNext(text: str, codepointSize: int_p) -> int", &GetCodepointNext);
    vm->bind(mod, "GetCodepointPrevious(text: str, codepointSize: int_p) -> int", &GetCodepointPrevious);
    vm->bind(mod, "CodepointToUTF8(codepoint: int, utf8Size: int_p) -> str", &CodepointToUTF8);
    vm->bind(mod, "TextCopy(dst: char_p, src: str) -> int", &TextCopy);
    vm->bind(mod, "TextIsEqual(text1: str, text2: str) -> bool", &TextIsEqual);
    vm->bind(mod, "TextLength(text: str) -> int", &TextLength);
    vm->bind(mod, "TextSubtext(text: str, position: int, length: int) -> str", &TextSubtext);
    vm->bind(mod, "TextReplace(text: str, replace: str, by: str) -> char_p", &TextReplace);
    vm->bind(mod, "TextInsert(text: str, insert: str, position: int) -> char_p", &TextInsert);
    vm->bind(mod, "TextJoin(textList: void_p, count: int, delimiter: str) -> str", &TextJoin);
    vm->bind(mod, "TextSplit(text: str, delimiter: int, count: int_p) -> void_p", &TextSplit);
    vm->bind(mod, "TextAppend(text: char_p, append: str, position: int_p) -> None", &TextAppend);
    vm->bind(mod, "TextFindIndex(text: str, find: str) -> int", &TextFindIndex);
    vm->bind(mod, "TextToUpper(text: str) -> str", &TextToUpper);
    vm->bind(mod, "TextToLower(text: str) -> str", &TextToLower);
    vm->bind(mod, "TextToPascal(text: str) -> str", &TextToPascal);
    vm->bind(mod, "TextToInteger(text: str) -> int", &TextToInteger);
    vm->bind(mod, "TextToFloat(text: str) -> float", &TextToFloat);
    vm->bind(mod, "InitAudioDevice() -> None", &InitAudioDevice);
    vm->bind(mod, "CloseAudioDevice() -> None", &CloseAudioDevice);
    vm->bind(mod, "IsAudioDeviceReady() -> bool", &IsAudioDeviceReady);
    vm->bind(mod, "SetMasterVolume(volume: float) -> None", &SetMasterVolume);
    vm->bind(mod, "GetMasterVolume() -> float", &GetMasterVolume);
    vm->bind(mod, "LoadWave(fileName: str) -> Wave", &LoadWave);
    vm->bind(mod, "LoadWaveFromMemory(fileType: str, fileData: uchar_p, dataSize: int) -> Wave", &LoadWaveFromMemory);
    vm->bind(mod, "IsWaveReady(wave: Wave) -> bool", &IsWaveReady);
    vm->bind(mod, "LoadSound(fileName: str) -> Sound", &LoadSound);
    vm->bind(mod, "LoadSoundFromWave(wave: Wave) -> Sound", &LoadSoundFromWave);
    vm->bind(mod, "LoadSoundAlias(source: Sound) -> Sound", &LoadSoundAlias);
    vm->bind(mod, "IsSoundReady(sound: Sound) -> bool", &IsSoundReady);
    vm->bind(mod, "UpdateSound(sound: Sound, data: void_p, sampleCount: int) -> None", &UpdateSound);
    vm->bind(mod, "UnloadWave(wave: Wave) -> None", &UnloadWave);
    vm->bind(mod, "UnloadSound(sound: Sound) -> None", &UnloadSound);
    vm->bind(mod, "UnloadSoundAlias(alias: Sound) -> None", &UnloadSoundAlias);
    vm->bind(mod, "ExportWave(wave: Wave, fileName: str) -> bool", &ExportWave);
    vm->bind(mod, "ExportWaveAsCode(wave: Wave, fileName: str) -> bool", &ExportWaveAsCode);
    vm->bind(mod, "PlaySound(sound: Sound) -> None", &PlaySound);
    vm->bind(mod, "StopSound(sound: Sound) -> None", &StopSound);
    vm->bind(mod, "PauseSound(sound: Sound) -> None", &PauseSound);
    vm->bind(mod, "ResumeSound(sound: Sound) -> None", &ResumeSound);
    vm->bind(mod, "IsSoundPlaying(sound: Sound) -> bool", &IsSoundPlaying);
    vm->bind(mod, "SetSoundVolume(sound: Sound, volume: float) -> None", &SetSoundVolume);
    vm->bind(mod, "SetSoundPitch(sound: Sound, pitch: float) -> None", &SetSoundPitch);
    vm->bind(mod, "SetSoundPan(sound: Sound, pan: float) -> None", &SetSoundPan);
    vm->bind(mod, "WaveCopy(wave: Wave) -> Wave", &WaveCopy);
    vm->bind(mod, "WaveCrop(wave: 'Wave_p', initSample: int, finalSample: int) -> None", &WaveCrop);
    vm->bind(mod, "WaveFormat(wave: 'Wave_p', sampleRate: int, sampleSize: int, channels: int) -> None", &WaveFormat);
    vm->bind(mod, "LoadWaveSamples(wave: Wave) -> float_p", &LoadWaveSamples);
    vm->bind(mod, "UnloadWaveSamples(samples: float_p) -> None", &UnloadWaveSamples);
    vm->bind(mod, "LoadMusicStream(fileName: str) -> Music", &LoadMusicStream);
    vm->bind(mod, "LoadMusicStreamFromMemory(fileType: str, data: uchar_p, dataSize: int) -> Music", &LoadMusicStreamFromMemory);
    vm->bind(mod, "IsMusicReady(music: Music) -> bool", &IsMusicReady);
    vm->bind(mod, "UnloadMusicStream(music: Music) -> None", &UnloadMusicStream);
    vm->bind(mod, "PlayMusicStream(music: Music) -> None", &PlayMusicStream);
    vm->bind(mod, "IsMusicStreamPlaying(music: Music) -> bool", &IsMusicStreamPlaying);
    vm->bind(mod, "UpdateMusicStream(music: Music) -> None", &UpdateMusicStream);
    vm->bind(mod, "StopMusicStream(music: Music) -> None", &StopMusicStream);
    vm->bind(mod, "PauseMusicStream(music: Music) -> None", &PauseMusicStream);
    vm->bind(mod, "ResumeMusicStream(music: Music) -> None", &ResumeMusicStream);
    vm->bind(mod, "SeekMusicStream(music: Music, position: float) -> None", &SeekMusicStream);
    vm->bind(mod, "SetMusicVolume(music: Music, volume: float) -> None", &SetMusicVolume);
    vm->bind(mod, "SetMusicPitch(music: Music, pitch: float) -> None", &SetMusicPitch);
    vm->bind(mod, "SetMusicPan(music: Music, pan: float) -> None", &SetMusicPan);
    vm->bind(mod, "GetMusicTimeLength(music: Music) -> float", &GetMusicTimeLength);
    vm->bind(mod, "GetMusicTimePlayed(music: Music) -> float", &GetMusicTimePlayed);
    vm->bind(mod, "LoadAudioStream(sampleRate: int, sampleSize: int, channels: int) -> AudioStream", &LoadAudioStream);
    vm->bind(mod, "IsAudioStreamReady(stream: AudioStream) -> bool", &IsAudioStreamReady);
    vm->bind(mod, "UnloadAudioStream(stream: AudioStream) -> None", &UnloadAudioStream);
    vm->bind(mod, "UpdateAudioStream(stream: AudioStream, data: void_p, frameCount: int) -> None", &UpdateAudioStream);
    vm->bind(mod, "IsAudioStreamProcessed(stream: AudioStream) -> bool", &IsAudioStreamProcessed);
    vm->bind(mod, "PlayAudioStream(stream: AudioStream) -> None", &PlayAudioStream);
    vm->bind(mod, "PauseAudioStream(stream: AudioStream) -> None", &PauseAudioStream);
    vm->bind(mod, "ResumeAudioStream(stream: AudioStream) -> None", &ResumeAudioStream);
    vm->bind(mod, "IsAudioStreamPlaying(stream: AudioStream) -> bool", &IsAudioStreamPlaying);
    vm->bind(mod, "StopAudioStream(stream: AudioStream) -> None", &StopAudioStream);
    vm->bind(mod, "SetAudioStreamVolume(stream: AudioStream, volume: float) -> None", &SetAudioStreamVolume);
    vm->bind(mod, "SetAudioStreamPitch(stream: AudioStream, pitch: float) -> None", &SetAudioStreamPitch);
    vm->bind(mod, "SetAudioStreamPan(stream: AudioStream, pan: float) -> None", &SetAudioStreamPan);
    vm->bind(mod, "SetAudioStreamBufferSizeDefault(size: int) -> None", &SetAudioStreamBufferSizeDefault);

    CodeObject_ co = vm->compile("from linalg import *", "raylib.py", EXEC_MODE);
    vm->_exec(co, mod);
    mod->attr().set("Quaternion", mod->attr("vec4"));
    mod->attr().set("Texture2D", mod->attr("Texture"));
    mod->attr().set("TextureCubemap", mod->attr("Texture"));
    mod->attr().set("RenderTexture2D", mod->attr("RenderTexture"));
    mod->attr().set("Camera", mod->attr("Camera3D"));
}
}  // namespace pkpy