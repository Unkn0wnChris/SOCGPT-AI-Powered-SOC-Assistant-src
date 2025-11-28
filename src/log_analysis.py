import re
import json
from collections import Counter
from typing import List, Dict

# ------------------------------
# Load MITRE mapping JSON
# ------------------------------
with open("mitre.json", "r") as f:
    MITRE_MAPPING_DICT = json.load(f)

# ------------------------------
# Functions
# ------------------------------

def load_logs(filepath: str) -> List[str]:
    """Load logs from a specified file."""
    with open(filepath, 'r') as file:
        return file.readlines()

def parse_log_line(line: str) -> Dict[str, str]:
    """
    Parse a single line of the log and return a dictionary of its components.
    Example log: "2025-11-28 16:00:00 ALERT Failed password for admin Severity=70"
    """
    log_pattern = r'(?P<timestamp>\S+ \S+) (?P<level>\S+) (?P<message>.*)'
    match = re.match(log_pattern, line)
    if match:
        return match.groupdict()
    return {}

def parse_severity_from_line(line: str) -> int:
    """
    Extract numeric severity from log line (NetWitness-style logs).
    Returns 0 if no severity found.
    """
    match = re.search(r"Severity=(\d+)", line)
    if match:
        return int(match.group(1))
    return 0

def severity_label(score: int) -> str:
    """Map numeric severity to High/Medium/Low labels."""
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"

def map_mitre(log_message: str) -> str:
    """
    Map a log message to MITRE ATT&CK techniques using keyword matching.
    Returns a comma-separated string of matched techniques.
    """
    log_lower = log_message.lower()
    matches = []

    for keyword, value in MITRE_MAPPING_DICT.items():
        if re.search(rf"\b{re.escape(keyword)}\b", log_lower):
            technique_id = value.get("id", "Unknown ID")
            technique_name = value.get("name", "Unknown Technique")
            tactic = value.get("tactic", "Unknown Tactic")
            matches.append(f"{technique_id}: {technique_name} ({tactic})")
    
    return ", ".join(set(matches)) if matches else "No MITRE ATT&CK technique identified"

def analyze_logs(log_lines: List[str]) -> List[Dict[str, str]]:
    """
    Analyze logs and return a list of dictionaries with:
    - timestamp
    - level
    - message
    - severity_score
    - severity_label
    - MITRE techniques
    """
    analyzed_logs = []

    for line in log_lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            message = parsed_line["message"]
            severity_score = parse_severity_from_line(line)
            parsed_line["severity_score"] = severity_score
            parsed_line["severity_label"] = severity_label(severity_score)
            parsed_line["mitre"] = map_mitre(message)
            analyzed_logs.append(parsed_line)

    return analyzed_logs

# ------------------------------
# Main function
# ------------------------------
def main(filepath: str):
    log_lines = load_logs(filepath)
    analyzed_logs = analyze_logs(log_lines)

    print("Timestamp | Level | Message | Severity | MITRE ATT&CK")
    print("-" * 100)
    for log in analyzed_logs:
        print(
            f"{log['timestamp']} | {log['level']} | {log['message']} | "
            f"{log['severity_label']} ({log['severity_score']}) | {log['mitre']}"
        )

# ------------------------------
# Example usage
# ------------------------------
if __name__ == "__main__":
    log_file_path = "path/to/your/logfile.log"
    main(log_file_path)
