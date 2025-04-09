from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from core.domain.exceptions import EmailSendingError

class IEmailService(ABC):
    """
    Interface for email service operations.
    """
    
    @abstractmethod
    def send_email(
        self,
        to: str | List[str],
        subject: str,
        body: str,
        cc: Optional[str | List[str]] = None,
        bcc: Optional[str | List[str]] = None,
        attachments: Optional[Dict[str, bytes]] = None,
    ) -> bool:
        """
        Sends an email to one or more recipients.
        
        Args:
            to: Recipient email address(es)
            subject: Email subject
            body: Email body (can be plain text or HTML)
            cc: CC recipient(s) (optional)
            bcc: BCC recipient(s) (optional)
            attachments: Dictionary of attachment names and their binary content (optional)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
            
        Raises:
            EmailSendingError: If there's an error while sending the email
        """
        pass
    
    @abstractmethod
    def send_template_email(
        self,
        to: str | List[str],
        template_id: str,
        template_data: Dict[str, str],
        cc: Optional[str | List[str]] = None,
        bcc: Optional[str | List[str]] = None,
    ) -> bool:
        """
        Sends an email using a predefined template.
        
        Args:
            to: Recipient email address(es)
            template_id: Identifier for the email template
            template_data: Data to populate the template placeholders
            cc: CC recipient(s) (optional)
            bcc: BCC recipient(s) (optional)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
            
        Raises:
            EmailSendingError: If there's an error while sending the email
        """
        pass