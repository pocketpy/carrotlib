import raylib as rl

#define LIGHTGRAY  CLITERAL(Color){ 200, 200, 200, 255 }   // Light Gray
#define GRAY       CLITERAL(Color){ 130, 130, 130, 255 }   // Gray
#define DARKGRAY   CLITERAL(Color){ 80, 80, 80, 255 }      // Dark Gray
#define YELLOW     CLITERAL(Color){ 253, 249, 0, 255 }     // Yellow
#define GOLD       CLITERAL(Color){ 255, 203, 0, 255 }     // Gold
#define ORANGE     CLITERAL(Color){ 255, 161, 0, 255 }     // Orange
#define PINK       CLITERAL(Color){ 255, 109, 194, 255 }   // Pink
#define RED        CLITERAL(Color){ 230, 41, 55, 255 }     // Red
#define MAROON     CLITERAL(Color){ 190, 33, 55, 255 }     // Maroon
#define GREEN      CLITERAL(Color){ 0, 228, 48, 255 }      // Green
#define LIME       CLITERAL(Color){ 0, 158, 47, 255 }      // Lime
#define DARKGREEN  CLITERAL(Color){ 0, 117, 44, 255 }      // Dark Green
#define SKYBLUE    CLITERAL(Color){ 102, 191, 255, 255 }   // Sky Blue
#define BLUE       CLITERAL(Color){ 0, 121, 241, 255 }     // Blue
#define DARKBLUE   CLITERAL(Color){ 0, 82, 172, 255 }      // Dark Blue
#define PURPLE     CLITERAL(Color){ 200, 122, 255, 255 }   // Purple
#define VIOLET     CLITERAL(Color){ 135, 60, 190, 255 }    // Violet
#define DARKPURPLE CLITERAL(Color){ 112, 31, 126, 255 }    // Dark Purple
#define BEIGE      CLITERAL(Color){ 211, 176, 131, 255 }   // Beige
#define BROWN      CLITERAL(Color){ 127, 106, 79, 255 }    // Brown
#define DARKBROWN  CLITERAL(Color){ 76, 63, 47, 255 }      // Dark Brown

#define WHITE      CLITERAL(Color){ 255, 255, 255, 255 }   // White
#define BLACK      CLITERAL(Color){ 0, 0, 0, 255 }         // Black
#define BLANK      CLITERAL(Color){ 0, 0, 0, 0 }           // Blank (Transparent)
#define MAGENTA    CLITERAL(Color){ 255, 0, 255, 255 }     // Magenta
#define RAYWHITE   CLITERAL(Color){ 245, 245, 245, 255 }   // My own White (raylib logo)

class Colors:
    LightGray = rl.Color(200, 200, 200, 255)
    Gray = rl.Color(130, 130, 130, 255)
    DarkGray = rl.Color(80, 80, 80, 255)
    Yellow = rl.Color(253, 249, 0, 255)
    Gold = rl.Color(255, 203, 0, 255)
    Orange = rl.Color(255, 161, 0, 255)
    Pink = rl.Color(255, 109, 194, 255)
    Red = rl.Color(230, 41, 55, 255)
    Maroon = rl.Color(190, 33, 55, 255)
    Green = rl.Color(0, 228, 48, 255)
    Lime = rl.Color(0, 158, 47, 255)
    DarkGreen = rl.Color(0, 117, 44, 255)
    SkyBlue = rl.Color(102, 191, 255, 255)
    Blue = rl.Color(0, 121, 241, 255)
    DarkBlue = rl.Color(0, 82, 172, 255)
    Purple = rl.Color(200, 122, 255, 255)
    Violet = rl.Color(135, 60, 190, 255)
    DarkPurple = rl.Color(112, 31, 126, 255)
    Beige = rl.Color(211, 176, 131, 255)
    Brown = rl.Color(127, 106, 79, 255)
    DarkBrown = rl.Color(76, 63, 47, 255)

    White = rl.Color(255, 255, 255, 255)
    Black = rl.Color(0, 0, 0, 255)
    Blank = rl.Color(0, 0, 0, 0)
    Magenta = rl.Color(255, 0, 255, 255)
    RayWhite = rl.Color(245, 245, 245, 255)


def Color__repr__(self: rl.Color):
    return f"Color({self.r}, {self.g}, {self.b}, {self.a})"
rl.Color.__repr__ = Color__repr__
