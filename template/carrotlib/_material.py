import raylib as rl
from _carrotlib import GRAPHICS_API_OPENGL_33, GRAPHICS_API_OPENGL_ES2, GRAPHICS_API_OPENGL_ES3, load_text_asset

from ._light import Lightmap
from . import g as _g

def _compile_shader(vsCode: str = None, fsCode: str = None):
    FS_INCLUDE = """
vec3 _mix(vec3 x, vec3 y, bvec3 a)
{
    return vec3(a.x ? y.x : x.x, a.y ? y.y : x.y, a.z ? y.z : x.z);
}
    
vec3 sRGBToLinear(vec3 rgb)
{
// See https://gamedev.stackexchange.com/questions/92015/optimized-linear-to-srgb-glsl
return _mix(pow((rgb + 0.055) * (1.0 / 1.055), vec3(2.4)),
            rgb * (1.0/12.92),
            lessThanEqual(rgb, vec3(0.04045)));
}

vec3 LinearToSRGB(vec3 rgb)
{
// See https://gamedev.stackexchange.com/questions/92015/optimized-linear-to-srgb-glsl
return _mix(1.055 * pow(rgb, vec3(1.0 / 2.4)) - 0.055,
            rgb * 12.92,
            lessThanEqual(rgb, vec3(0.0031308)));
}
"""
    if fsCode is not None:
        fsCode = FS_INCLUDE + fsCode

    if GRAPHICS_API_OPENGL_33:
        if vsCode is not None:
            vsCode = '\n'.join([
                '#version 330 core',
                '#define _IN_ in',
                '#define _OUT_ out',
                vsCode
            ])
        if fsCode is not None:
            fsCode = '\n'.join([
                '#version 330 core',
                '#define _IN_ in',
                '#define _OUT_ out',
                '#define _DEFINE_GL_FRAG_COLOR_ out vec4 _out_0;',
                '#define _GL_FRAG_COLOR_ _out_0',
                fsCode
            ])
    elif GRAPHICS_API_OPENGL_ES2 or GRAPHICS_API_OPENGL_ES3:
        if vsCode is not None:
            vsCode = '\n'.join([
                '#version 100',
                'precision mediump float;',
                '#define _IN_ attribute',
                '#define _OUT_ varying',
                '#define texture texture2D',
                vsCode
            ])
        if fsCode is not None:
            fsCode = '\n'.join([
                '#version 100',
                'precision mediump float;',
                '#define _IN_ varying',
                '#define _DEFINE_GL_FRAG_COLOR_',    # nothing
                '#define _GL_FRAG_COLOR_ gl_FragColor',
                '#define texture texture2D',
                fsCode
            ])
    else:
        raise RuntimeError("current graphics API not supported")
    return vsCode, fsCode

class Material:
    cached_shaders: dict[type, rl.Shader] = {}

    def __init__(self):
        cls = type(self)
        if cls not in self.cached_shaders:
            self.cached_shaders[cls] = rl.LoadShaderFromMemory(*_compile_shader(cls.vert(), cls.frag()))
        self.shader = self.cached_shaders[cls]

    @classmethod
    def vert(cls) -> str | None:
        return None
    
    @classmethod
    def frag(cls) -> str | None:
        return None
    
    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self


class UnlitMaterial(Material):
    @classmethod
    def vert(cls) -> str:
        return load_text_asset("carrotlib/assets/shaders/unlit.vert")
    
    @classmethod
    def frag(cls) -> str:
        return load_text_asset("carrotlib/assets/shaders/unlit.frag")


class DiffuseMaterial(Material):
    def __init__(self, lightmap: 'Lightmap' = None):
        super().__init__()
        self.lightmap = lightmap or _g.default_lightmap
        self._loc_lightmap = rl.GetShaderLocation(self.shader, "texture1")

    @classmethod
    def vert(cls) -> str:
        return load_text_asset("carrotlib/assets/shaders/diffuse.vert")
    
    @classmethod
    def frag(cls) -> str:
        return load_text_asset("carrotlib/assets/shaders/diffuse.frag")

    def __enter__(self):
        super().__enter__()
        rl.SetShaderValueTexture(self.shader, self._loc_lightmap, self.lightmap.texture)
        return self


class PureColorMaterial(Material):
    @classmethod
    def frag(cls) -> str:
        return load_text_asset("carrotlib/assets/shaders/pure_color.frag")
