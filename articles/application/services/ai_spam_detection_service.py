# application/services/ai_spam_detection_service.py
from application.interfaces.services.spam_detection_service import SpamDetectionService
from infrastructure.ai_services.spam_detector import AISpamDetector

class AISpamDetectionService(SpamDetectionService):
    def __init__(self, detector: AISpamDetector):
        self._detector = detector

    def is_spam(self, content) -> bool:
        return self._detector.analyze(content.text).get('is_spam', False)

    @classmethod
    def get_provider_info(cls) -> dict:
        return {
            "version": "2.1",
            "algorithm": "CNN-LSTM Hybrid"
        }