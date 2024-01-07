from c import int_p
import raylib as rl
from linalg import vec2

def load_asset(name: str) -> bytes:
    """load an asset from the platform's asset directory as bytes."""

def list_assets(root: str) -> list[str]:
    """list the assets in the platform's asset directory."""

def _get_cjk_codepoints() -> tuple[int_p, int]:
    pass

def _rlDrawTextBoxed(render: bool, limitHeight: bool, lineSpacing: float, font: rl.Font, text: str, rec: rl.Rectangle, fontSize: float, spacing: float, wordWrap: bool, tint: rl.Color) -> vec2:
    pass

PIXEL_SNAP_SHADER: str
GLSL_VERSION: int