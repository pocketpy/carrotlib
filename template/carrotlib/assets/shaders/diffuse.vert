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