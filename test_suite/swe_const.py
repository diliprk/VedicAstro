import swisseph as swe

# Global dictionary of celestial bodies
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "Rahu": swe.MEAN_NODE,  # Lunar North Node
    "Ketu": swe.MEAN_NODE
}

RASHIS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 
          'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

## Lords of the 12 Zodiac Signs
SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]          

NAKSHATRAS = ['Ashwini','Bharani','Krittika','Rohini','Mrigashīrsha', 'Ardra', 'Punarvasu', 'Pushya', 'Āshleshā', 
'Maghā', 'PūrvaPhalgunī', 'UttaraPhalgunī', 'Hasta', 'Chitra', 'Svati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 
'PurvaAshadha','UttaraAshadha', 'Shravana', 'Dhanishta','Shatabhisha', 'PurvaBhādrapadā', 'UttaraBhādrapadā', 'Revati']
