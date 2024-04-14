from dataclasses import dataclass
import json, os

@dataclass
class Config:
    project: str = "examples/01_HelloWorld"
    use_precompile: bool = False
    use_playground_console: bool = True

if os.path.exists("playground.json"):
    with open("playground.json", "rt", encoding='utf-8') as f:
        config = Config(**json.load(f))
else:
    config = Config()
