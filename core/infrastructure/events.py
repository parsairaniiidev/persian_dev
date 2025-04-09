from django.conf import settings
from django.core.signals import request_finished
from django.dispatch import receiver

class DjangoEventPublisher:
    """Publishes domain events through Django's signal system"""
    
    def __init__(self):
        self._events = []
        self._published = False
    
    def publish(self, event):
        """Queue an event for publishing"""
        if self._published:
            raise RuntimeError("Events have already been published for this request")
        self._events.append(event)
    
    def dispatch_events(self):
        """Dispatch all queued events"""
        from django.core.signals import Signal
        domain_event = Signal()
        
        for event in self._events:
            domain_event.send(
                sender=event.__class__,
                event=event
            )
        
        self._published = True
        self._events.clear()

# Connect to request finished signal
@receiver(request_finished)
def publish_pending_events(sender, **kwargs):
    """Auto-publish events at the end of each request"""
    if hasattr(sender, '_domain_events'):
        sender._domain_events.dispatch_events()