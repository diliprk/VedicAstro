import os
import polars as pl
import swisseph as swe
from datetime import datetime
from .utils import dms_to_decdeg, utc_offset_str_to_float
from .VedicAstro import VedicHoroscopeData

## Global Constants
SWE_AYANAMAS = { "Krishnamurti" : swe.SIDM_KRISHNAMURTI, "Krishnamurti_Senthilathiban": swe.SIDM_KRISHNAMURTI_VP291}

# Determine the absolute path to the directory where this script is located
current_dir = os.path.abspath(os.path.dirname(__file__))
csv_file_path = os.path.join(current_dir, "data", "KP_SL_Divisions.csv")
## Read KP SubLord Divisions CSV File
KP_SL_DMS_DATA = pl.read_csv(csv_file_path)
KP_SL_DMS_DATA = KP_SL_DMS_DATA\
                .with_columns(pl.arange(1, KP_SL_DMS_DATA.height + 1).alias("SL_Div_Nr"))\
                .with_columns([
                    pl.col('From_DMS').map_elements(dms_to_decdeg).alias('From_DecDeg'),
                    pl.col('To_DMS').map_elements(dms_to_decdeg).alias('To_DecDeg'),
                    pl.col("From_DMS").str.replace_all(":", "").cast(pl.Int32).alias("From_DMS_int"),
                    pl.col("To_DMS").str.replace_all(":", "").cast(pl.Int32).alias("To_DMS_int")
                ])

def jd_to_datetime(jdt: float, tz_offset: float):
    utc = swe.jdut1_to_utc(jdt) 
    # Convert UTC to local time - note negative sign before tzoffset to convert from UTC to IST
    year, month, day, hour, minute, seconds  = swe.utc_time_zone(*utc, offset = -tz_offset)
    # Convert the fractional seconds to microseconds
    microseconds = int(seconds % 1 * 1_000_000)
    return datetime(year, month, day, hour, minute, int(seconds), microseconds)

def get_horary_ascendant_degree(horary_number: int):
    """
    Convert a horary number to ascendant degree of the starting subdivision
    """
    if 1 <= horary_number <= 249:
        row = KP_SL_DMS_DATA.filter(pl.col("SL_Div_Nr") == horary_number).select(["Sign", "From_DMS", "From_DecDeg", "SubLord"])
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

def find_exact_ascendant_time(year: int, month: int, day: int, utc_offset: str, lat: float, lon: float, horary_number: int, ayanamsa : str) -> datetime:
    """
    Finds the exact time when the Ascendant is at the desired degree.

    Parameters:
    - year: year of the horary question (prasna)
    - month: month of the horary question
    - day: day of the horary question
    - utc_offset: The UTC offset of the horary question's location, i.e of the predictor (astrologer)
    - lat: Latitude pertaining to the horary question's predictor (astrologer)
    - lon: Longitude pertaining to the horary question's predictor (astrologer).
    - horary_number: The horary number for which to retrieve the ascendant details to match.
    - ayanamsa: The ayanamsa to be used when constructing the chart

    Returns:
    - matched_time: a datetime object, when the Ascendant matches the desired degree.
    If no match is found within the day, returns None.
    """
    ## Retrieve Horary Asc Details from given horary_number
    horary_asc = get_horary_ascendant_degree(horary_number) 
    horary_asc_deg = horary_asc["ZodiacDegreeLocation"]
    req_sublord = horary_asc["SubLord"]   
    utc_float =  utc_offset_str_to_float(utc_offset)

    utc = swe.utc_time_zone(year, month, day, hour = 0, minutes = 0, seconds = 0, offset = utc_float)
    _ , jd_start = swe.utc_to_jd(*utc) ## Unpacks utc tuple
    jd_end = jd_start + 1  # end of the day

    swe.set_sid_mode(SWE_AYANAMAS.get(ayanamsa))  # set the ayanamsa
    current_time = jd_start
    counter = 0
    while current_time <= jd_end:
        cusps, _ = swe.houses_ex(current_time, lat, lon, b'P', flags = swe.FLG_SIDEREAL)
        asc_lon_deg = cusps[0]
        asc_deg_diff = asc_lon_deg - horary_asc_deg
        asc_deg_diff_abs = abs(asc_deg_diff)

        # Adjust increment factor based on the magnitude of degree difference
        if asc_deg_diff_abs > 10:
            inc_factor = 0.005  # largest steps when far away
        elif asc_deg_diff_abs >= 1.0:
            inc_factor = 1  # larger steps when moderately away
        elif asc_deg_diff_abs >= 0.1:
            inc_factor = 10  # smaller steps when getting closer
        else:
            inc_factor = 100  # very small steps when very close

        # Special handling for cyclical transition near 360 degrees for horary_number == 1
        if (asc_lon_deg > 355 and horary_asc_deg == 0.0):
            inc_factor = 100  # Use very small steps to avoid overshooting the target for horary_number == 1

        # For Debugging purpose
        # current_time_dt = jd_to_datetime(current_time, utc_float)
        # print(f"CurrentTimeDT: {current_time_dt}  Itr.Counter: {counter}  Inc.Factor: {inc_factor}  TargetDeg: {horary_asc_deg}   AscLonDeg:{asc_lon_deg}  AscDegDiff: {asc_deg_diff_abs}")

        if 0.0001 < asc_deg_diff <= 0.001:
            matched_time = jd_to_datetime(current_time, utc_float)
            secs_final = matched_time.second + (matched_time.microsecond) / 1_000_000
            vhd_hora = VedicHoroscopeData(year, month, day, matched_time.hour, matched_time.minute, secs_final, utc_offset, lat, lon, ayanamsa, "Placidus")
            houses_chart = vhd_hora.generate_chart()
            houses_data = vhd_hora.get_houses_data_from_chart(houses_chart)
            asc = houses_data[0]
            # print(f"**UNMATCHED**===ReqSubLord: {req_sublord} || CurrentAscSL: {asc.SubLord}")
            if asc.SubLord == req_sublord:
                # print(f"Nr.Iterations: {counter} || Matched Time: {matched_time} || Final Ascendant: {asc_lon_deg} || ReqSL: {req_sublord} || CurrentAscSL: {asc.SubLord}")
                return matched_time, houses_chart, houses_data
            
        
        current_time += 1.0 / (24 * 60 * 60 * inc_factor)  # Adjust time increment based on the factor
        counter += 1

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
    horary_asc = get_horary_ascendant_degree(horary_number) 
    horary_asc_deg = horary_asc["ZodiacDegreeLocation"]
    req_sublord = horary_asc["SubLord"]   
    matched_time, houses_chart, houses_data = find_exact_ascendant_time(year, month, day, utc, latitude, longitude, horary_number, ayan)
    asc = houses_data[0]
    final_sublord = asc.SubLord
    final_asc_deg = asc.LonDecDeg
    print(pl.DataFrame(houses_data))
