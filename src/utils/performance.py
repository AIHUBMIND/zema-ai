"""
Performance Monitoring
Tracks system and component performance metrics
"""

import time
import psutil
import logging
from typing import Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Single performance metric"""
    component: str
    operation: str
    duration_ms: float
    timestamp: datetime
    memory_mb: float
    cpu_percent: float


class PerformanceMonitor:
    """Monitor system and component performance"""
    
    def __init__(self, alert_threshold_ms: float = 1000.0):
        """
        Initialize performance monitor
        
        Args:
            alert_threshold_ms: Alert threshold in milliseconds
        """
        self.metrics: List[PerformanceMetric] = []
        self.alert_threshold_ms = alert_threshold_ms
        self.component_stats = defaultdict(list)
        logger.info("PerformanceMonitor initialized")
    
    def record(self, component: str, operation: str, duration_ms: float):
        """
        Record a performance metric
        
        Args:
            component: Component name
            operation: Operation name
            duration_ms: Duration in milliseconds
        """
        metric = PerformanceMetric(
            component=component,
            operation=operation,
            duration_ms=duration_ms,
            timestamp=datetime.now(),
            memory_mb=psutil.virtual_memory().used / 1024 / 1024,
            cpu_percent=psutil.cpu_percent()
        )
        
        self.metrics.append(metric)
        self.component_stats[component].append(duration_ms)
        
        # Alert on slow operations
        if duration_ms > self.alert_threshold_ms:
            logger.warning(
                f"Slow operation detected: {component}.{operation} "
                f"took {duration_ms:.2f}ms"
            )
        
        # Keep only last 1000 metrics
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def get_component_stats(self, component: str) -> Dict[str, float]:
        """
        Get statistics for a component
        
        Args:
            component: Component name
            
        Returns:
            Statistics dictionary
        """
        if component not in self.component_stats:
            return {}
        
        durations = self.component_stats[component]
        return {
            'count': len(durations),
            'avg_ms': sum(durations) / len(durations),
            'min_ms': min(durations),
            'max_ms': max(durations),
            'p95_ms': sorted(durations)[int(len(durations) * 0.95)] if durations else 0
        }
    
    def get_system_stats(self) -> Dict[str, float]:
        """
        Get current system statistics
        
        Returns:
            System stats dictionary
        """
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_mb': psutil.virtual_memory().used / 1024 / 1024,
            'disk_percent': psutil.disk_usage('/').percent
        }

