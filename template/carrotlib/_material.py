import raylib as rl
from _carrotlib import GRAPHICS_API_OPENGL_33, GRAPHICS_API_OPENGL_ES2, GRAPHICS_API_OPENGL_ES3

from ._light import Lightmap
from . import g as _g

def _compile_shader(vsCode: str = None, fsCode: str = None):
    FS_INCLUDE = """
vec3 mix(vec3 x, vec3 y, bvec3 a)
{
    return vec3(a.x ? y.x : x.x, a.y ? y.y : x.y, a.z ? y.z : x.z);
}
    
vec3 sRGBToLinear(vec3 rgb)
{
// See https://gamedev.stackexchange.com/questions/92015/optimized-linear-to-srgb-glsl
return mix(pow((rgb + 0.055) * (1.0 / 1.055), vec3(2.4)),
            rgb * (1.0/12.92),
            lessThanEqual(rgb, vec3(0.04045)));
}

vec3 LinearToSRGB(vec3 rgb)
{
// See https://gamedev.stackexchange.com/questions/92015/optimized-linear-to-srgb-glsl
return mix(1.055 * pow(rgb, vec3(1.0 / 2.4)) - 0.055,
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
                '#define _DEFINE_FRAG_OUT_ out vec4 _out_0;',
                '#define _FRAG_OUT_ _out_0',
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
                '#define _DEFINE_FRAG_OUT_',    # nothing
                '#define _FRAG_OUT_ gl_FragColor',
                '#define texture texture2D',
                fsCode
            ])
    else:
        raise RuntimeError("current graphics API not supported")
    return vsCode, fsCode


UNLIT_SHADER = """
// Input vertex attributes
_IN_ vec3 vertexPosition;
_IN_ vec2 vertexTexCoord;
_IN_ vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
_OUT_ vec2 fragTexCoord;
_OUT_ vec4 fragColor;

void main()
{
    fragTexCoord = vertexTexCoord;
    fragColor = vertexColor;
    vec4 clipPos = mvp * vec4(vertexPosition, 1.0);
    gl_Position = clipPos;
}
""", """
// Input vertex attributes (from vertex shader)
_IN_ vec2 fragTexCoord;
_IN_ vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;        // tint color

_DEFINE_FRAG_OUT_

void main()
{
    vec4 texel = texture(texture0, fragTexCoord);
    texel.xyz = sRGBToLinear(texel.xyz);
    vec4 finalColor = texel * colDiffuse * fragColor;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
    _FRAG_OUT_ = finalColor;
}"""

DIFFUSE_SHADER = """
// Input vertex attributes
_IN_ vec3 vertexPosition;
_IN_ vec2 vertexTexCoord;
_IN_ vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
_OUT_ vec4 screenPos;
_OUT_ vec2 fragTexCoord;
_OUT_ vec4 fragColor;

vec4 ComputeScreenPos(vec4 pos){
    vec4 o;
    o.x = 0.5 * (pos.x + pos.w);
    o.y = 0.5 * (pos.y + pos.w);
    o.zw = pos.zw;
    return o;              
}

void main()
{
    fragTexCoord = vertexTexCoord;
    fragColor = vertexColor;

    vec4 clipPos = mvp * vec4(vertexPosition, 1.0);
    screenPos = ComputeScreenPos(clipPos);
    gl_Position = clipPos;
}
""", """
// Input vertex attributes (from vertex shader)
_IN_ vec2 fragTexCoord;
_IN_ vec4 fragColor;
_IN_ vec4 screenPos;

// Input uniform values
uniform sampler2D texture0;
uniform sampler2D texture1;     // lightmap texture
uniform vec4 colDiffuse;        // tint color

_DEFINE_FRAG_OUT_

void main()
{
    vec2 screenCoord = screenPos.xy / screenPos.w;
    vec4 texel = texture(texture0, fragTexCoord);   // Get texel color
    vec4 light = texture(texture1, screenCoord);    // Get light color
    texel.xyz = sRGBToLinear(texel.xyz);
    vec4 finalColor = texel * colDiffuse * fragColor * light;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
    _FRAG_OUT_ = finalColor;
}"""

class Material:
    cached_shaders: dict[type, rl.Shader] = {}

    def __init__(self):
        cls = type(self)
        if cls not in self.cached_shaders:
            self.cached_shaders[cls] = rl.LoadShaderFromMemory(*_compile_shader(*cls.glsl()))
        self.shader = self.cached_shaders[cls]

    @classmethod
    def glsl(cls) -> tuple[str | None, str | None]:
        raise NotImplementedError

class UnlitMaterial(Material):
    @classmethod
    def glsl(cls):
        return UNLIT_SHADER

    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self


class DiffuseMaterial(Material):
    def __init__(self, lightmap: 'Lightmap' = None):
        super().__init__()
        self.lightmap = lightmap or _g.default_lightmap
        self._loc_lightmap = rl.GetShaderLocation(self.shader, "texture1")

    @classmethod
    def glsl(cls):
        return DIFFUSE_SHADER

    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        rl.SetShaderValueTexture(self.shader, self._loc_lightmap, self.lightmap.texture)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self