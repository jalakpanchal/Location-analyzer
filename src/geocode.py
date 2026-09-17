"""
geocode.py
----------
Static latitude/longitude lookup table for locations appearing in the
sample dataset. A static table is used instead of a live geocoding API
so the app works fully offline and demos reliably without network
dependency during evaluation/viva.

To extend: add new "City": (lat, lon) entries below, or swap this out
for geopy.geocoders.Nominatim if live geocoding is desired.
"""

CITY_COORDS = {
    "Mumbai": (19.0760, 72.8777),
    "Tokyo": (35.6762, 139.6503),
    "Ankara": (39.9334, 32.8597),
    "Kathmandu": (27.7172, 85.3240),
    "London": (51.5072, -0.1276),
    "Sao Paulo": (-23.5505, -46.6333),
    "Nairobi": (-1.2921, 36.8219),
    "Cairo": (30.0444, 31.2357),
    "Sydney": (-33.8688, 151.2093),
    "Lagos": (6.5244, 3.3792),
    "New York City": (40.7128, -74.0060),
    "Caracas": (10.4806, -66.9036),
    "Berlin": (52.5200, 13.4050),
    "Chennai": (13.0827, 80.2707),
    "Toronto": (43.6532, -79.3832),
    "Amman": (31.9454, 35.9284),
    "Paris": (48.8566, 2.3522),
    "Manila": (14.5995, 120.9842),
    "Seoul": (37.5665, 126.9780),
    "Rome": (41.9028, 12.4964),
    "Melbourne": (-37.8136, 144.9631),
    "Baghdad": (33.3152, 44.3661),
    "Buenos Aires": (-34.6037, -58.3816),
    "Jakarta": (-6.2088, 106.8456),
    "Boston": (42.3601, -71.0589),
    "Beirut": (33.8938, 35.5018),
    "Bangalore": (12.9716, 77.5946),
    "Dhaka": (23.8103, 90.4125),
    "Chicago": (41.8781, -87.6298),
    "Kinshasa": (-4.4419, 15.2663),
    "Geneva": (46.2044, 6.1432),
    "Houston": (29.7604, -95.3698),
    "Athens": (37.9838, 23.7275),
    "Detroit": (42.3314, -83.0458),
    "Hong Kong": (22.3193, 114.1694),
    "Fukuoka": (33.5904, 130.4017),
    "Tel Aviv": (32.0853, 34.7818),
    "Dakar": (14.7167, -17.4677),
    "Los Angeles": (34.0522, -118.2437),
    "Warsaw": (52.2297, 21.0122),
    "Cape Town": (-33.9249, 18.4241),
    "Singapore": (1.3521, 103.8198),
    "Ho Chi Minh City": (10.8231, 106.6297),
    "Moscow": (55.7558, 37.6173),
    "Madrid": (40.4168, -3.7038),
    "Bangkok": (13.7563, 100.5018),
    "Tehran": (35.6892, 51.3890),
}


def get_coords(location: str):
    """Return (lat, lon) tuple for a location, or None if unknown."""
    return CITY_COORDS.get(location)
