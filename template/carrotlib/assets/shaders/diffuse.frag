// Input vertex attributes (from vertex shader)
_IN_ vec2 fragTexCoord;
_IN_ vec4 fragColor;
_IN_ vec4 screenPos;

// Input uniform values
uniform sampler2D texture0;
uniform sampler2D texture1;     // lightmap texture
uniform vec4 colDiffuse;        // tint color

_DEFINE_GL_FRAG_COLOR_

void main()
{
    vec2 screenCoord = screenPos.xy / screenPos.w;
    vec4 texel = texture(texture0, fragTexCoord);   // Get texel color
    vec4 light = texture(texture1, screenCoord);    // Get light color
    texel.xyz = sRGBToLinear(texel.xyz);
    vec4 finalColor = texel * colDiffuse * fragColor * light;
    finalColor.xyz = LinearToSRGB(finalColor.xyz);
    _GL_FRAG_COLOR_ = finalColor;
}
