# infrastructure/services/spam_detection.py
import logging
from typing import Dict, Any
from domain.value_objects.content import Content
from domain.entities.spam_detection_result import SpamDetectionResult

logger = logging.getLogger(__name__)

class SimpleSpamDetectionService:
    """Basic spam detection service implementation"""
    
    def __init__(self, spam_keywords: list[str] = None):
        self.spam_keywords = spam_keywords or [
            'خرید', 'فوری', 'تخفیف', 'ویزا', 'ارز'
        ]
        logger.info("Initialized SimpleSpamDetectionService")

    def detect(self, content: Content) -> SpamDetectionResult:
        """Check content for spam patterns"""
        spam_count = sum(
            keyword in content.text 
            for keyword in self.spam_keywords
        )
        
        is_spam = spam_count > 2  # More than 2 spam keywords
        confidence = min(spam_count / 5, 1.0)  # Scale confidence 0-1
        
        return SpamDetectionResult(
            is_spam=is_spam,
            confidence=confidence,
            detected_patterns=self.spam_keywords,
            metadata={
                'spam_keywords_found': spam_count,
                'service': 'SimpleSpamDetection'
            }
        )