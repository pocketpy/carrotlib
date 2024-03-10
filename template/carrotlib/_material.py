import raylib as rl
from ._light import Lightmap
from . import g as _g

FS_INCLUDE = """
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

UNLIT_SHADER = """#version 330 core

// Input vertex attributes
in vec3 vertexPosition;
in vec2 vertexTexCoord;
in vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
out vec2 fragTexCoord;
out vec4 fragColor;

void main()
{
    fragTexCoord = vertexTexCoord;
    fragColor = vertexColor;
    vec4 clipPos = mvp * vec4(vertexPosition, 1.0);
    gl_Position = clipPos;
}
""", '#version 330 core' + FS_INCLUDE + """
// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;        // tint color

// Output fragment color
out vec4 finalColor;

void main()
{
    vec4 texel = texture(texture0, fragTexCoord);
    texel.xyz = sRGBToLinear(texel.xyz);
    finalColor = texel * colDiffuse * fragColor;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
}"""

DIFFUSE_SHADER = """#version 330 core

// Input vertex attributes
in vec3 vertexPosition;
in vec2 vertexTexCoord;
in vec4 vertexColor;

// Input uniform values
uniform mat4 mvp;

// Output vertex attributes (to fragment shader)
out vec4 screenPos;
out vec2 fragTexCoord;
out vec4 fragColor;

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
""", '#version 330 core' + FS_INCLUDE + """
// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;
in vec4 screenPos;

// Input uniform values
uniform sampler2D texture0;
uniform sampler2D texture1;     // lightmap texture
uniform vec4 colDiffuse;        // tint color

// Output fragment color
out vec4 finalColor;
void main()
{
    vec2 screenCoord = screenPos.xy / screenPos.w;
    vec4 texel = texture(texture0, fragTexCoord);   // Get texel color
    vec4 light = texture(texture1, screenCoord);    // Get light color
    texel.xyz = sRGBToLinear(texel.xyz);
    finalColor = texel * colDiffuse * fragColor * light;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
}"""

class Material:
    cached_shaders: dict[type, rl.Shader] = {}

    def __init__(self):
        cls = type(self)
        if cls not in self.cached_shaders:
            self.cached_shaders[cls] = rl.LoadShaderFromMemory(*cls.glsl())
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