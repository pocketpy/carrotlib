import raylib as rl

from ._node import WaitForSeconds
from ._resources import load_sound

_managed_sounds: list[rl.Sound] = []

def _update_managed_sounds_coro():
    global _managed_sounds
    while True:
        yield WaitForSeconds(8)
        living_sounds = []
        for sound in _managed_sounds:
            if rl.IsSoundPlaying(sound):
                living_sounds.append(sound)
            else:
                rl.UnloadSoundAlias(sound)
        _managed_sounds = living_sounds

def _count_managed_sounds():
    return len(_managed_sounds)

def _unload_all_sound_aliases():
    for sound in _managed_sounds:
        rl.StopSound(sound)
        rl.UnloadSoundAlias(sound)
    _managed_sounds.clear()

def play_sound(sound: rl.Sound | str) -> rl.Sound:
    if isinstance(sound, str):
        sound = load_sound(sound)
    assert rl.IsSoundReady(sound)
    sound = rl.LoadSoundAlias(sound)
    rl.PlaySound(sound)
    assert rl.IsSoundPlaying(sound)
    _managed_sounds.append(sound)
    return sound
