class TilesetDef:
    padding: int
    spacing: int
    tileGridSize: int
    opaqueTiles: list[bool] | None

    def __init__(self, data: dict):
        self.data = data
        self.padding = data['padding']
        self.spacing = data['spacing']
        self.tileGridSize = data['tileGridSize']
        self.relPath = data['relPath']

        opaqueTiles = data.get('cachedPixelData', {}).get('opaqueTiles')
        if opaqueTiles is None:
            self.opaqueTiles = None
        else:
            self.opaqueTiles = [c=='1' for c in opaqueTiles]

    @property
    def cWid(self) -> int:
        return self.data['__cWid']
    
    @property
    def cHei(self) -> int:
        return self.data['__cHei']
    
    def get_tile_id(self, cx: int, cy: int) -> int:
        return cx + cy * self.cWid

    def get_tile_cx(self, tid: int):
        return tid - self.cWid * (tid // self.cWid)
    
    def get_tile_cy(self, tid: int):
        return tid // self.cWid

    def get_tile_source_x(self, tid: int):
        return self.padding + self.get_tile_cx(tid) * ( self.tileGridSize + self.spacing )

    def get_tile_source_y(self, tid: int):
        return self.padding + self.get_tile_cy(tid) * ( self.tileGridSize + self.spacing )

    def is_tile_opaque(self, tid: int):
        if self.opaqueTiles is None:
            return False
        return self.opaqueTiles[tid]
