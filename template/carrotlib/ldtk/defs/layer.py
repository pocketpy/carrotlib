from ..defs.rule import AutoLayerRuleDef

class AutoTiledLayerDef:
    data: dict
    autoSourceLayerDefUid: int | None

    def __init__(self, data: dict) -> None:
        assert 'autoRuleGroups' in data
        self.data = data
        self.autoSourceLayerDefUid = data['autoSourceLayerDefUid']

    def get_active_rules(self) -> list[AutoLayerRuleDef]:
        ret = []
        for group in self.data['autoRuleGroups']:
            if not group['active']:
                continue
            for rule in group['rules']:
                if not rule['active']:
                    continue
                ret.append(AutoLayerRuleDef(rule))
        return ret
