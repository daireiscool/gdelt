"""
@author: Dáire Campbell <daire.d.campbell@gmail.com>

Description:
Code to ingest data and save it to a location (local/cloud)

Note:
Need to find a way to stop the function ending.
    Code pushes the bash script to the background (so can use all resources)
    Since they are in the background, python doesnt detect them and closes.
    This will cause python script to close early, while bash code still running
"""

import os
import subprocess
import time

def run_gdelt_ingestation(number_days=1, save_location="."):
    """
    Function to trigger the bash script gdelt_ingestion.sh.

    ::param number_days: (int) Number of days before today to ingest
    ::param save_location: (string) Location to save to
    """
    subprocess.Popen([
        os.getcwd()+"/gdelt_ingestion.sh",
        f"{number_days}",
        f"{save_location}"
    ])


def run_gdelt_ingestation_range(
    start_date="20180101", end_date="20180102", save_location="."):
    """
    Function to trigger he bash script gdelt_ingestion_range.sh.
    
    Note:
        Appears to work better when start_date and end_date are reversed...

    ::param start_date: (string) Start of dates to ingest (format='yyyymmdd')
    ::param end_date: (string) End of dates to ingest (format='yyyymmdd')
    ::param save_location: (string) Location to save to
    """
    subprocess.Popen([
        os.getcwd()+"/gdelt_ingestion_range.sh",
        f"{start_date}",
        f"{end_date}",
        f"{save_location}"
    ])


if __name__ == "__main__":
    run_gdelt_ingestation()
    time.sleep(1000)