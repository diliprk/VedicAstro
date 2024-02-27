from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from VedicAstro.VedicAstro import VedicHoroscopeData

app = FastAPI()

class ChartInput(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    utc: str
    latitude: float
    longitude: float
    ayanamsa: str = "Lahiri"
    house_system: str = "Equal"
    return_style: Optional[str] = None

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to VedicAstro FastAPI Service!",
            "info": "Visit http://127.0.0.1:8088/docs to test the API functions"}

@app.post("/get_planets_data_from_chart")
async def get_planets_data(input: ChartInput):
    """Generates planetary positions data for a given time and location, based on the selected ayanamsa and house system"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    planets_data = horoscope.get_planets_data_from_chart(chart)
    return [planet._asdict() for planet in planets_data]

@app.post("/get_houses_data_from_chart")
async def get_houses_data(input: ChartInput):
    """Generates house positions data for a given time and location, based on the selected ayanamsa and house system"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    houses_data = horoscope.get_houses_data_from_chart(chart)
    return [house._asdict() for house in houses_data]

@app.post("/get_planet_significators")
async def get_planet_significators(input: ChartInput):
    """Generates ABCD Significators Table for planets"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    return horoscope.get_planet_wise_significators(chart)

@app.post("/get_planetary_aspects")
async def get_planetary_aspects(input:ChartInput):
    """Generates a table of planetary aspects"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    return horoscope.get_planetary_aspects(chart)      
    
@app.post("/get_house_significators")
async def get_house_significators(input: ChartInput):
    """Generates ABCD Significators Table for houses"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    return horoscope.get_house_wise_significators(chart)

@app.post("/get_vimshottari_dasa_table")
async def get_vimshottari_dasa_table(input: ChartInput):
    """Computes the Vimshottari Dasa for the chart"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    return horoscope.compute_vimshottari_dasa(chart)


@app.post("/get_consolidated_chart_data")
async def get_consolidated_chart_data(input: ChartInput):
    """Generates consolidated data of houses and planets, sign(rasi)wise for a given time and location"""
    horoscope = VedicHoroscopeData(input.year, input.month, input.day, input.hour, input.minute, input.second, 
                                   input.utc, input.latitude, input.longitude, input.ayanamsa, input.house_system)
    chart = horoscope.generate_chart()
    return horoscope.get_consolidated_chart_data(chart, return_style = input.return_style)