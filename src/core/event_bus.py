"""
Event Bus
Pub/sub system for component communication
"""

import logging
from typing import Dict, List, Callable, Any, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class EventBus:
    """
    Event bus for component communication
    
    Allows components to publish events and subscribe to events
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)
        logger.info("EventBus initialized")
    
    def subscribe(self, event_type: str, callback: Callable[[Any], None]):
        """
        Subscribe to an event type
        
        Args:
            event_type: Event type name (e.g., 'config_changed')
            callback: Callback function to call when event occurs
        """
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable[[Any], None]):
        """
        Unsubscribe from an event type
        
        Args:
            event_type: Event type name
            callback: Callback function to remove
        """
        if callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from event: {event_type}")
    
    def emit(self, event_type: str, data: Any = None):
        """
        Emit an event to all subscribers
        
        Args:
            event_type: Event type name
            data: Event data to pass to subscribers
        """
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event callback for {event_type}: {e}")
        
        logger.debug(f"Emitted event: {event_type}")
    
    def clear_subscribers(self, event_type: Optional[str] = None):
        """
        Clear subscribers for an event type or all events
        
        Args:
            event_type: Event type to clear, or None for all events
        """
        if event_type:
            self.subscribers[event_type].clear()
        else:
            self.subscribers.clear()
        logger.debug(f"Cleared subscribers for: {event_type or 'all events'}")

