from dataclasses import dataclass
import json, os

@dataclass
class Config:
    project: str = "examples/01_HelloWorld"

if os.path.exists("playground.json"):
    with open("playground.json", "rt") as f:
        config = Config(**json.load(f))
else:
    config = Config()
