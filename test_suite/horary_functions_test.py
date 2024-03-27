import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
from vedicastro.horary_chart import find_exact_ascendant_time, get_horary_ascendant_degree

"""
This test takes bout 5 hours, to cycle through 1440 mins * 249 horary numbers for 1 day,
which is about 374,400 combinations. Some combinations take slightly longer because of the cyclical
clockwise procession through linear time across the zodiac, and some take a very short time. 
For quick testing, you can change the `range(24*60)` to something minimal like `range(10)` in `minutes_progress`
Running this script will create a .csv file in this same directory
"""

def run_horary_func_tests():
    # Define the test date and location parameters
    test_date = {"year": 2024, "month": 2, "day": 5, "utc": "+5:30",
                 "latitude": 11.020085773931049, "longitude": 76.98319647719487, "ayan": "Krishnamurti"}

    # Initialize an empty list to store test results
    test_results = []

    # Iterate through all horary numbers from 1 to 249 with a tqdm progress bar
    horary_progress = tqdm(range(1, 250), desc="Horary Ascendant Validation Progress")
    for horary_number in horary_progress:
        start_time = datetime(test_date["year"], test_date["month"], test_date["day"])
        # Test for all the 1440 minutes of the day
        minute_progress = tqdm(range(24*60), desc=f"Processing Horary Number {horary_number}", leave=False)
        for minute in minute_progress:    
            current_time = start_time + timedelta(minutes=minute)
            # Update the description with the current hour and minute
            minute_progress.set_description(f"Processing Horary Number {horary_number} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}", refresh=True)            
            params = test_date.copy()
            params.update({
                "hour": current_time.hour,
                "minute": current_time.minute,
                "secs": current_time.second,
                "horary_number": horary_number
            })

            horary_asc = get_horary_ascendant_degree(horary_number)
            matched_time, houses_chart, houses_data = find_exact_ascendant_time(
                params["year"], params["month"], params["day"], params["utc"],
                params["latitude"], params["longitude"], params["horary_number"], params["ayan"]
            )

            if matched_time and houses_data:
                asc = houses_data[0]
                final_sublord = asc.SubLord
                final_asc_deg = asc.LonDecDeg
                is_sl_match = (horary_asc["SubLord"] == final_sublord)
                is_ascdeg_equal = round(horary_asc["ZodiacDegreeLocation"], 2) == round(final_asc_deg, 2)

                test_results.append({
                    "Horary_Number": horary_number,
                    "Horary_Time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "MatchedTime": matched_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Req_Asc_Deg": horary_asc["ZodiacDegreeLocation"],
                    "Final_Asc_Deg": final_asc_deg,
                    "is_AscDeg_Equal": is_ascdeg_equal,
                    "Req_Asc_SubLord": horary_asc["SubLord"],
                    "Final_Asc_SubLord": final_sublord,
                    "is_SL_Match": is_sl_match,
                })

    # Convert test results to a pandas DataFrame
    df_results = pd.DataFrame(test_results)

    # Optionally, save the DataFrame to a CSV file
    df_results.to_csv("horary_asc_matching_test_results.csv", index=False)

if __name__ == "__main__":
    run_horary_func_tests()