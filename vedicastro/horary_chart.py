import os
import math
import polars as pl
from typing import Tuple
from datetime import datetime
from flatlib import const
from flatlib.chart import Chart
from .VedicAstro import VedicHoroscopeData
from .utils import pretty_data_table, dms_to_decdeg

## Read KP SubLord Divisions CSV File
# Determine the absolute path to the directory where this script is located
current_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(current_dir, "data", "KP_SL_Divisions.csv")
KP_SL_DMS_DATA = pl.read_csv(csv_file_path)
KP_SL_DMS_DATA = KP_SL_DMS_DATA\
                .with_columns(pl.arange(1, KP_SL_DMS_DATA.height + 1).alias("SL_Div_Nr"))\
                .with_columns([
                    pl.col('From_DMS').map_elements(dms_to_decdeg).alias('From_DecDeg'),
                    pl.col('To_DMS').map_elements(dms_to_decdeg).alias('To_DecDeg'),
                    pl.col("From_DMS").str.replace_all(":", "").cast(pl.Int32).alias("From_DMS_int"),
                    pl.col("To_DMS").str.replace_all(":", "").cast(pl.Int32).alias("To_DMS_int")
                ])

def calculate_asc_speed(chart_start: Chart, start_dt: datetime, utc: str, lat: float, lon: float, ayan: str, house_system: str):
    """Calculates the ascendant speed between two datetime objects."""
    
    # Generate asc data for the start moment
    asc_start = chart_start.get(const.ASC)
    asc_start_lon_deg = asc_start.lon
    
    # Generate asc data for the end moment
    vhd = VedicHoroscopeData(start_dt.year, start_dt.month, start_dt.day, start_dt.hour, start_dt.minute, start_dt.second + 59, 
                             utc, lat, lon, ayan, house_system)
    end_dt = datetime(vhd.year, vhd.month, vhd.day, vhd.hour, vhd.minute, vhd.second)
    chart_end = vhd.generate_chart()
    asc_end = chart_end.get(const.ASC)
    asc_end_lon_deg = asc_end.lon
    
    # Calculate the change in Ascendant position
    delta_degrees = (asc_end_lon_deg - asc_start_lon_deg) % 360
    # Calculate the time difference in seconds
    diff_seconds = (end_dt - start_dt).total_seconds()
    
    # Calculate the speed in degrees per second
    asc_speed = delta_degrees / diff_seconds
    # print(f"**Delta Degrees: {delta_degrees}°")
    # print(f"Time Delta for Asc Speed Calc: {diff_seconds} seconds")
    print(f"Asc Speed for {start_dt.date()} is {asc_speed}° per second")
    return round(asc_speed, 7)

def get_horary_ascendant_degree(horary_number: int):
    """
    Convert a horary number to ascendant degree of the starting subdivision
    """
    if 1 <= horary_number <= 249:
        row = KP_SL_DMS_DATA.filter(pl.col("SL_Div_Nr") == horary_number).select(["Sign", "From_DMS", "From_DecDeg"])
        data = row.to_dicts()[0]

        # Convert the sign to its starting degree in the zodiac circle
        sign_order = {'Aries': 0, 'Taurus': 30, 'Gemini': 60, 'Cancer': 90,
                    'Leo': 120, 'Virgo': 150, 'Libra': 180, 'Scorpio': 210,
                    'Sagittarius': 240, 'Capricorn': 270, 'Aquarius': 300, 'Pisces': 330 
                    }
        
        sign_start_degree = sign_order[data['Sign']]

        # Convert From_DecDeg to zodiac degree location
        zodiac_degree_location = sign_start_degree + data['From_DecDeg']
        data['ZodiacDegreeLocation'] = zodiac_degree_location
        return data
    else:
        return "SL Div Nr. out of range. Please provide a number between 1 and 249."



def find_exact_ascendant_time(year: int, month: int, day: int, hour: int, minute: int, second: int, utc: str, 
                              lat: float, lon: float, horary_ascendant: dict, house_system: str, ayan : str) -> Tuple:
    """
    Finds the exact time when the Ascendant is at the desired degree.

    Parameters:
    - year: year of the horary question (prasna)
    - month: month of the horary question
    - day: day of the horary question
    - hour: hour of the horary question
    - minute: minute of the horary question
    - second: second of the horary question
    - utc: The UTC offset of the horary question's location, i.e of the predictor (astrologer)
    - lat: Latitude pertaining to the horary question's predictor (astrologer)
    - lon: Longitude pertaining to the horary question's predictor (astrologer).
    - horary_ascendant: The desired Ascendant degree and sign to match.
    - house_system: The house system to use, as a byte string (e.g., b'P' for Placidus).
    - ayan: The ayanamsa to be used when constructing the chart


    Returns:
    Tuple of (matched_time), planets_data and houses_data, when the Ascendant matches the desired degree.
    If no match is found within the day, returns None.
    """
    horary_asc_lon_dec_deg = horary_ascendant["ZodiacDegreeLocation"]
    hora_horoscope = VedicHoroscopeData(year, month, day, hour, minute, second, utc, lat, lon, ayan, house_system)
    hora_chart = hora_horoscope.generate_chart()


    # Initial horoscope to get the midnight ascendant degree
    midnight_horoscope = VedicHoroscopeData(year, month, day, 0, 0, 0, utc, lat, lon, ayan, house_system)
    midnight_chart = midnight_horoscope.generate_chart()
    midnight_planets_data = midnight_horoscope.get_planets_data_from_chart(midnight_chart)
    midnight_asc_deg = midnight_planets_data[0].LonDecDeg

    # Calculate the degree difference correctly, considering the zodiac as a loop
    delta_degrees = (horary_asc_lon_dec_deg - midnight_asc_deg) % 360
    print(f"Midnight Asc Deg: {midnight_asc_deg} \nDegree Difference: {delta_degrees}")
    time_difference_in_seconds = delta_degrees / 0.00431 ## random val arrived by manually calculating the difference in asc pos over 2 datetimes for the same day

    ## Calculate Asc Speed for this particular day
    # start_time =  datetime(year, month, day, 0, 0, 0)
    # asc_speed = calculate_asc_speed(midnight_chart, start_time, utc, lat, lon, ayan, house_system)
    # time_difference_in_seconds = delta_degrees / asc_speed
    
    # Calculate approx hours and remaining seconds
    adj_hour, remaining_seconds = divmod(time_difference_in_seconds, 3600)

    # Calculate approx minutes and seconds (with seconds as a float for precision)
    adj_minute, adj_second = divmod(remaining_seconds, 60)

    # matched_time = f"{year}-{month}-{day} {int(adj_hour):02d}:{int(adj_minute):02d}:{adj_second:.3f}"
    # horoscope = VedicHoroscopeData(year, month, day, adj_hour, adj_minute, adj_second, utc, lat, lon, ayan, house_system)
    # final_chart = horoscope.generate_chart()
    # horary_planets_data = hora_horoscope.get_planets_data_from_chart(hora_chart, new_houses_chart = final_chart)
    # houses_data = horoscope.get_houses_data_from_chart(final_chart)
    # return matched_time, final_chart, horary_planets_data, houses_data

    # Start checking 5 minutes (300 seconds) before the calculated time
    start_hour = adj_hour
    start_minute = adj_minute        

    # Adjust for iterating over the rest of the day
    total_seconds = int((start_hour * 3600) + (start_minute * 60) ) # + adj_second 
    day_end_seconds = 24 * 3600  # Total seconds in a day


    for current_second in range(total_seconds, day_end_seconds):
        adjusted_hour = current_second // 3600
        remaining = current_second % 3600
        adjusted_minute = remaining // 60
        adjusted_second = remaining % 60
        horoscope = VedicHoroscopeData(year, month, day, adjusted_hour, adjusted_minute, adjusted_second, utc, lat, lon, ayan, house_system)
        chart_itr = horoscope.generate_chart()
        planets_data = horoscope.get_planets_data_from_chart(chart_itr)
        asc = planets_data[0]
        asc_lon_deg = asc.LonDecDeg

        if math.isclose(asc_lon_deg, horary_asc_lon_dec_deg, abs_tol=0.0018):
            horoscope = VedicHoroscopeData(year, month, day, adjusted_hour, adjusted_minute, adjusted_second+0.5, utc, lat, lon, ayan, house_system)
            final_chart = horoscope.generate_chart()       
            matched_time = f"{year:04d}-{month:02d}-{day:02d} {horoscope.hour}:{horoscope.minute}:{horoscope.second}"
            houses_data = horoscope.get_houses_data_from_chart(final_chart)
            horary_planets_data = hora_horoscope.get_planets_data_from_chart(hora_chart, new_houses_chart = final_chart)
            return matched_time, final_chart, horary_planets_data, houses_data

    print("No matching Ascendant time found for the given input")
    return None    

if __name__== "__main__":
    year = 2024
    month = 2
    day = 5
    hour = 9
    minute = 5
    secs = 0
    horary_number = 34
    latitude, longitude, utc = 11.020085773931049, 76.98319647719487, "+5:30" ## Coimbatore
    ayan = "Krishnamurti"
    house_system = "Placidus" ## Default House for KP system


    horary_asc = get_horary_ascendant_degree(horary_number)
    desired_asc = horary_asc["ZodiacDegreeLocation"]
    print(f'Ascendant Degrees: {desired_asc} degrees')
    matched_time, final_chart, planets_data, houses_data = find_exact_ascendant_time(year, month, day, hour, minute, secs, utc,
                                                                        latitude, longitude, horary_asc, house_system, ayan)

    if matched_time:
        print(f'The Ascendant is at {houses_data[0].LonDecDeg} degrees on {matched_time}')
        print("Planets Data:\n",pretty_data_table(planets_data))
        print("\nHouses Data:\n", pretty_data_table(houses_data))