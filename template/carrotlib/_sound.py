import raylib as rl

_managed_sounds: list[rl.Sound] = []
_swap: list[rl.Sound] = []

def _update_managed_sounds():
    global _managed_sounds, _swap
    if not _managed_sounds:
        return
    for sound in _managed_sounds:
        if rl.IsSoundPlaying(sound):
            _swap.append(sound)
        else:
            rl.UnloadSoundAlias(sound)
    _managed_sounds, _swap = _swap, _managed_sounds
    _swap.clear()
    return _managed_sounds

def _unload_all_sound_aliases():
    for sound in _managed_sounds:
        rl.StopSound(sound)
        rl.UnloadSoundAlias(sound)
    _managed_sounds.clear()

def play_sound(sound: rl.Sound) -> rl.Sound:
    assert rl.IsSoundReady(sound)
    sound = rl.LoadSoundAlias(sound)
    rl.PlaySound(sound)
    assert rl.IsSoundPlaying(sound)
    _managed_sounds.append(sound)
    return sound
