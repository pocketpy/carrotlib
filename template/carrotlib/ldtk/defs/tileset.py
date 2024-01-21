class TilesetDef:
    data: dict
    padding: int
    spacing: int
    tileGridSize: int
    relPath: str

    cWid: int
    cHei: int
    
    opaqueTiles: list[bool] | None

    def __init__(self, data: dict):
        self.data = data
        self.padding = data['padding']
        self.spacing = data['spacing']
        self.tileGridSize = data['tileGridSize']
        self.relPath = data['relPath']

        self.cWid = data['__cWid']
        self.cHei = data['__cHei']

        if 'opaqueTiles' not in data:
            self.opaqueTiles = None
        else:
            self.opaqueTiles = [c=='1' for c in data['opaqueTiles']]
    
    def getTileId(self, cx: int, cy: int) -> int:
        return cx + cy * self.cWid

    def getTileCx(self, tid: int):
        return tid - self.cWid * (tid // self.cWid)
    
    def getTileCy(self, tid: int):
        return tid // self.cWid

    def getTileSourceX(self, tid: int):
        return self.padding + self.getTileCx(tid) * ( self.tileGridSize + self.spacing )

    def getTileSourceY(self, tid: int):
        return self.padding + self.getTileCy(tid) * ( self.tileGridSize + self.spacing )

    def isTileOpaque(self, tid: int):
        if self.opaqueTiles is None:
            return False
        return self.opaqueTiles[tid]
