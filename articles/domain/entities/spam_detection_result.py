# domain/entities/spam_detection_result.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SpamDetectionResult:
    is_spam: bool
    confidence: float
    detected_patterns: List[str]
    metadata: Dict[str, Any] = None