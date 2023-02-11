import json
import logging
from pathlib import Path
from typing import List

from rules_provider.rule import Rule

rules = []


def load_rules(path: Path) -> List[Rule]:
    if rules:
        logging.debug("rules already loaded")
        return rules

    discovered_files = path.glob("**/*.{json}")
    logging.debug(f"discovered rules {discovered_files}")

    for rule_file in discovered_files:
        with open(rule_file, "r") as f:
            rules.append(Rule.parse_obj(json.loads(f.read())))

    return rules
