"""
Configuration and utility functions for Smart Property Finder
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class PropertyConfig:
    """Configuration for property search parameters"""
    DEFAULT_MIN_PRICE = 400
    DEFAULT_MAX_PRICE = 2000
    DEFAULT_MIN_BEDROOMS = 1
    DEFAULT_RADIUS = 5
    MAX_PROPERTIES_PER_PAGE = 24
    SORT_BY_PRICE_LOWEST = 1
    SORT_BY_PRICE_HIGHEST = 2
    SORT_BY_NEWEST = 6

@dataclass
class UIConfig:
    """Configuration for UI elements"""
    MAX_PROPERTIES_DISPLAY = 6
    CHART_HEIGHT = 400
    CHART_WIDTH = 600
    SIDEBAR_WIDTH = 300

class PropertyTypes:
    """Available property types"""
    ANY = "any"
    FLAT = "flat"
    HOUSE = "house"
    APARTMENT = "apartment"
    STUDIO = "studio"
    MAISONETTE = "maisonette"
    BUNGALOW = "bungalow"
    COTTAGE = "cottage"
    TOWNHOUSE = "townhouse"
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """Get all available property types"""
        return [
            cls.ANY, cls.FLAT, cls.HOUSE, cls.APARTMENT, cls.STUDIO,
            cls.MAISONETTE, cls.BUNGALOW, cls.COTTAGE, cls.TOWNHOUSE
        ]

class FurnishTypes:
    """Available furnish types"""
    ANY = "any"
    FURNISHED = "furnished"
    UNFURNISHED = "unfurnished"
    PART_FURNISHED = "partFurnished"

class PropertyStatus:
    """Property status options"""
    AVAILABLE = "available"
    LET_AGREED = "letAgreed"
    SOLD = "sold"
    SOLD_SUBJECT_TO_CONTRACT = "soldSubjectToContract"

def get_api_config() -> Dict:
    """Get API configuration"""
    return {
        "base_url": "https://api.rightmove.co.uk/v1/properties",
        "headers": {
            "X-API-KEY": os.getenv("RIGHTMOVE_API_KEY"),
            "Content-Type": "application/json"
        }
    }

def validate_location(location: str) -> bool:
    """Validate location input"""
    if not location or len(location.strip()) < 2:
        return False
    return True

def validate_price_range(min_price: int, max_price: int) -> bool:
    """Validate price range"""
    if min_price < 0 or max_price < 0:
        return False
    if min_price > max_price:
        return False
    return True

def format_price(price: float) -> str:
    """Format price for display"""
    if price >= 1000:
        return f"£{price/1000:.1f}k"
    return f"£{price:.0f}"

def calculate_price_per_bedroom(price: float, bedrooms: int) -> float:
    """Calculate price per bedroom"""
    if bedrooms <= 0:
        return price
    return price / bedrooms

def get_money_saving_tips() -> List[str]:
    """Get money-saving tips for renters"""
    return [
        "Consider studios for 1-person households",
        "Look for properties with bills included",
        "Negotiate longer-term contracts",
        "Check for student discounts",
        "Ask about referral bonuses",
        "Consider sharing with roommates",
        "Look for properties outside peak rental months",
        "Check for council tax exemptions",
        "Ask about deposit alternatives",
        "Consider properties with parking included"
    ]

def get_market_insights() -> List[str]:
    """Get market insights and tips"""
    return [
        "Best time to rent: January-March (lower demand)",
        "Peak rental season: June-September",
        "Properties are typically 5-10% cheaper in winter",
        "New builds often have higher rents but better facilities",
        "Older properties may be cheaper but check maintenance costs",
        "Properties near transport links command premium rents",
        "Look for up-and-coming areas for better value",
        "Check local development plans for future value",
        "Properties with gardens/balconies cost 10-15% more",
        "Furnished properties typically cost 15-20% more"
    ]

def get_property_amenities() -> List[str]:
    """Get common property amenities"""
    return [
        "Parking",
        "Garden/Balcony",
        "En-suite",
        "Furnished",
        "Bills included",
        "Gym",
        "Concierge",
        "Security",
        "Pet friendly",
        "Student friendly",
        "Disabled access",
        "Lift",
        "Storage",
        "Bike storage",
        "Communal areas"
    ]

def get_location_insights() -> Dict[str, str]:
    """Get insights about different locations"""
    return {
        "Manchester": "Great for young professionals, good transport links, vibrant nightlife",
        "London": "High rents but excellent job opportunities and cultural scene",
        "Birmingham": "Affordable alternative to London, growing tech scene",
        "Leeds": "Good value for money, strong student population",
        "Liverpool": "Historic city with affordable rents and good culture",
        "Bristol": "Creative city with good job market, slightly higher rents",
        "Newcastle": "Very affordable, friendly people, good nightlife",
        "Sheffield": "Great for students and families, very affordable",
        "Nottingham": "Good balance of affordability and amenities",
        "Cardiff": "Welsh capital with good job market and reasonable rents"
    }

# Configuration instances
PROPERTY_CONFIG = PropertyConfig()
UI_CONFIG = UIConfig()