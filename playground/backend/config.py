from dataclasses import dataclass, asdict
import json, os

@dataclass
class Config:
    project: str = "examples/01_HelloWorld"
    use_precompile: bool = False
    use_playground_console: bool = True
    use_release_build: bool = False
    use_profile_build: bool = False

    def save(self):
        with open('playground.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(asdict(self)))

if os.path.exists("playground.json"):
    with open("playground.json", "rt", encoding='utf-8') as f:
        config = Config(**json.load(f))
else:
    config = Config()
