from src.ollama_client import ollama_query
import re


def triage_alert(log: str, persona: str = None) -> str:
    """
    Triage an alert by severity, adjusted by analyst role.
    Uses keyword-based analysis for fast performance.
    
    Args:
        log: The security log
        persona: Analyst role - affects sensitivity
        
    Returns:
        Severity level: High, Medium, or Low
    """
    try:
        # Use keyword-based triage for fast performance
        return _keyword_based_triage(log, persona)
    
    except Exception as e:
        print(f"[ERROR] Triage error: {e}")
        return "Medium"  # Safe default


def _keyword_based_triage(log: str, persona: str = None) -> str:
    """
    Simple keyword-based triage as fallback.
    Sensitivity adjusted by role.
    """
    log_lower = log.lower()
    
    # High severity indicators
    high_keywords = [
        r'\b(critical|severity\s*[:=]\s*critical|critical.*alert)\b',
        r'\b(ransomware|trojan|worm|rootkit|exploit|remote\s+code\s+execution)\b',
        r'\b(multiple.*attempts|brute.*force|credential.*compromise|unauthorized\s+access)\b',
        r'\b(data\s+exfiltration|data\s+leak|data\s+theft|mass\s+deletion)\b',
        r'\b(privilege\s+escalation|domain\s+admin|system\s+compromise)\b',
    ]
    
    # Medium severity indicators
    medium_keywords = [
        r'\b(high|medium|severity\s*[:=]\s*(high|medium))\b',
        r'\b(phishing|malware|suspicious|anomalous|unusual)\b',
        r'\b(failed\s+login|multiple.*access|denied|blocked)\b',
        r'\b(port\s+scan|network\s+scan|enumeration)\b',
    ]
    
    # L3 and CTI have lower threshold (more sensitive)
    is_senior = persona in ["L3 SOC Analyst / IR", "Cyber Threat Intelligence Analyst (CTI)"]
    
    # Check high severity
    for pattern in high_keywords:
        if re.search(pattern, log_lower):
            return "High"
    
    # Check medium severity
    for pattern in medium_keywords:
        if re.search(pattern, log_lower):
            return "Medium" if not is_senior else "High"  # Senior roles flag medium as high
    
    # Default to Low
    return "Low"