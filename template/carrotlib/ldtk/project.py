import json
from .defs.tileset import TilesetDef
from .defs.layer import AutoTiledLayerDef

class Project:
    def __init__(self, data: bytes):
        self.data = json.loads(data)
        assert self.data['jsonVersion'] == '1.5.3'

    def _get_def(self, key: str, uid: int) -> dict:
        for definition in self.data['defs'][key]:
            if definition['uid'] == uid:
                return definition
        raise KeyError(f'{key}:{uid}')

    def get_tileset_def(self, uid: int):
        return TilesetDef(self._get_def('tilesets', uid))
    
    def get_layer_def(self, uid: int):
        return AutoTiledLayerDef(self._get_def('layers', uid))

    def __getitem__(self, key: str):
        return self.data[key]

