import json
import os
import re

# Load MITRE technique mappings from JSON file
json_path = os.path.join(os.path.dirname(__file__), "mitre1.json")

with open(json_path, "r") as f:
    MITRE_Mapping_Dict = json.load(f)

def MITRE_Mapping(log: str) -> str:
    """
    Maps log content to potential MITRE ATT&CK techniques based on keyword matching.
    Returns multiple results if matched.
    """
    log_lower = log.lower()
    matches = []

    for keyword, value in MITRE_Mapping_Dict.items():
        if re.search(rf"\b{re.escape(keyword)}\b", log_lower):
            technique_id = value.get("id", "Unknown ID")
            technique_name = value.get("name", "Unknown Technique")
            tactic = value.get("tactic", "Unknown Tactic")
            matches.append(f"{technique_id}: {technique_name} ({tactic})")

    return ", ".join(set(matches)) if matches else "No MITRE ATT&CK technique identified"
