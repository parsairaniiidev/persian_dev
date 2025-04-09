# domain/services/spam_detection_service.py
from abc import ABC, abstractmethod
from domain.value_objects.content import Content
from domain.entities.spam_detection_result import SpamDetectionResult

class SpamDetectionService(ABC):
    @abstractmethod
    def detect(self, content: Content) -> SpamDetectionResult:
        pass