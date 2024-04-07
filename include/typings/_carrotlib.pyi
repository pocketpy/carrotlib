from c import int_p
import raylib as rl
from linalg import vec2

def load_asset(name: str) -> bytes:
    """load an asset from the platform's asset directory as bytes."""

def list_assets(root: str) -> list[str]:
    """list the assets in the platform's asset directory."""

def fast_apply(f: callable, a: list | tuple, *args) -> None:
    """Equivalent to `for x in a: f(x, *args)` but much faster."""

def _request_hot_reload():
    ...

def _get_cjk_codepoints() -> tuple[int_p, int]:
    ...

def _rlDrawTextBoxed(render: bool, limitHeight: bool, lineSpacing: float, font: rl.Font, text: str, rec: rl.Rectangle, fontSize: float, spacing: float, wordWrap: bool, tint: rl.Color) -> vec2:
    ...

GRAPHICS_API_OPENGL_33: bool
GRAPHICS_API_OPENGL_ES2: bool
GRAPHICS_API_OPENGL_ES3: bool

def _bake_global_light(image: rl.Image_p, color: rl.Color, intensity: float) -> None:
    ...

def _bake_point_light(image: rl.Image_p, color: rl.Color, intensity: float, x: int, y: int, radius: int, cookie: rl.Image_p = None) -> None:
    ...