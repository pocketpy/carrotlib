from _carrotlib import *
from ._colors import Colors
from ._node import Node, get_node, build_scene_tree, WaitForEndOfFrame, WaitForSeconds
from ._animation import FramedAnimation, FramedAnimator, load_framed_animation, load_framed_animation_atlas
from ._tween import Tweener, TweenList, Tween
from ._sound import play_sound
# from ._font import SpriteFont
from ._viewport import get_mouse_position, get_mouse_delta, set_camera_transform
from ._event import Event
from ._light import PointLight2D, GlobalLight2D, ParticleLight2D, Lightmap
from ._material import UnlitMaterial, DiffuseMaterial, Material, PureColorMaterial
from ._setup import Game

from ._renderer import *
from ._resources import *
from ._math import *
from ._constants import *

from . import logger, nodes, controls, g, random

from .controls import Control

from raylib import Color, Rectangle

# http request
from typing import Literal

def request(
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        headers=None,
        body: str | bytes = None,
        timeout=None):
    """Send an HTTP request via non-blocking I/O."""
    import naett
    return naett.request(method, url, headers, body, timeout)
