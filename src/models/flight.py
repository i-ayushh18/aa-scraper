# src/models/flight.py
"""
Flight data models for the AA scraper.
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Flight:
    """Flight data model"""
    flight_number: str
    departure_time: str
    arrival_time: str
    points_required: int = 0
    cash_price_usd: float = 0.0
    taxes_fees_usd: float = 5.60
    cpp: Optional[float] = None
    
    # Additional fields
    duration: Optional[str] = None
    stops: Optional[int] = None
    
    def __post_init__(self):
        """Normalize data on creation"""
        self.flight_number = self._normalize_flight_number(self.flight_number)
        self.departure_time = self._normalize_time(self.departure_time)
        self.arrival_time = self._normalize_time(self.arrival_time)
    
    @staticmethod
    def _normalize_flight_number(fn: str) -> str:
        """Normalize flight number to AA#### format"""
        match = re.search(r'AA\s*(\d+)', fn, re.IGNORECASE)
        if match:
            return f"AA{match.group(1)}"
        return fn
    
    @staticmethod
    def _normalize_time(time_str: str) -> str:
        """Normalize time to HH:MM format"""
        if not time_str:
            return time_str
        
        # Remove extra spaces and normalize
        time_str = time_str.strip()
        
        # Handle various time formats
        match = re.search(r'(\d{1,2}):(\d{2})', time_str)
        if match:
            hour, minute = match.groups()
            return f"{int(hour):02d}:{minute}"
        
        return time_str
    
    def calculate_cpp(self) -> float:
        """Calculate cents per point (CPP)"""
        if self.points_required > 0 and self.cash_price_usd > 0:
            net_cash = self.cash_price_usd - self.taxes_fees_usd
            self.cpp = (net_cash / self.points_required) * 100
            return self.cpp
        return 0.0


@dataclass
class SearchResult:
    """Search result container"""
    award_flights: list[Flight]
    cash_flights: list[Flight]
    search_metadata: dict
    
    def get_merged_flights(self) -> list[Flight]:
        """Get flights with both award and cash pricing"""
        merged = []
        
        # Create lookup for cash flights
        cash_lookup = {f.flight_number: f for f in self.cash_flights}
        
        for award_flight in self.award_flights:
            cash_flight = cash_lookup.get(award_flight.flight_number)
            if cash_flight:
                # Merge award and cash data
                merged_flight = Flight(
                    flight_number=award_flight.flight_number,
                    departure_time=award_flight.departure_time,
                    arrival_time=award_flight.arrival_time,
                    points_required=award_flight.points_required,
                    cash_price_usd=cash_flight.cash_price_usd,
                    taxes_fees_usd=award_flight.taxes_fees_usd,
                    duration=award_flight.duration or cash_flight.duration,
                    stops=award_flight.stops or cash_flight.stops
                )
                merged_flight.calculate_cpp()
                merged.append(merged_flight)
        
        return merged