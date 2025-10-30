# src/strategies/base_strategy.py
"""
Base strategy interface.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple
from src.models import Flight
import logging

logger = logging.getLogger(__name__)


class ScraperStrategy(ABC):
    """Base class for all scraping strategies"""
    
    def __init__(self):
        self.name = self.__class__.__name__
    
    @abstractmethod
    async def scrape(self) -> Tuple[List[Flight], List[Flight]]:
        """
        Scrape both award and cash flights.
        Returns: (award_flights, cash_flights)
        """
        pass
    
    @abstractmethod
    def get_priority(self) -> int:
        """
        Get strategy priority (lower = higher priority)
        Returns: Priority as integer
        """
        pass