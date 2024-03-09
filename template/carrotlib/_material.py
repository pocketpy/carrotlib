import raylib as rl
from ._light import Lightmap

UNLIT_SHADER = """#version 330

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
""", """#version 330

// Input vertex attributes (from vertex shader)
in vec2 fragTexCoord;
in vec4 fragColor;

// Input uniform values
uniform sampler2D texture0;
uniform vec4 colDiffuse;        // tint color

// Output fragment color
out vec4 finalColor;

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

void main()
{
    vec4 texel = texture(texture0, fragTexCoord);
    // convert to linear color space
    texel.xyz = sRGBToLinear(texel.xyz);
    finalColor = texel * colDiffuse * fragColor;
    // convert back to sRGB
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
}"""

DIFFUSE_SHADER = """#version 330

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
""", """#version 330

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

void main()
{
    vec2 screenCoord = screenPos.xy / screenPos.w;
    vec4 texel = texture(texture0, fragTexCoord);   // Get texel color
    vec4 light = texture(texture1, screenCoord);    // Get light color
    // convert to linear color space
    texel.xyz = sRGBToLinear(texel.xyz);
    finalColor = texel * colDiffuse * fragColor * light;
    // convert back to sRGB
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
}"""

class UnlitMaterial:
    shader: rl.Shader = None

    def __init__(self):
        if type(self).shader is None:
            type(self).shader = rl.LoadShaderFromMemory(*UNLIT_SHADER)

    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self
    

class DiffuseMaterial:
    shader: rl.Shader = None

    def __init__(self, lightmap: 'Lightmap'):
        self.lightmap = lightmap
        if type(self).shader is None:
            type(self).shader = rl.LoadShaderFromMemory(*DIFFUSE_SHADER)
        self.loc_lightmap = rl.GetShaderLocation(self.shader, "texture1")

    def __enter__(self):
        rl.BeginShaderMode(self.shader)
        rl.SetShaderValueTexture(self.shader, self.loc_lightmap, self.lightmap.texture)
        return self
    
    def __exit__(self, *args):
        rl.EndShaderMode()
        return self