"""
@author: Dáire Campbell <daire.d.campbell@gmail.com>

Description:
    Code to convert gdelt .bz2 files into parquet files.
    The .bz2 are saved every 15 minutesintervales, but the parquet files will be saved in 
    daily intervals

Note:
    Having issues with wildcards (?*) so manually inputting hours and minutes
    
    bz2_to_parquet() is useful as only deletes .bz2 after saing as parquet.
    This is much more effecient to ingestions*.sh, as can stop half way through process, and 
    simply restart process.

"""
import os
from datetime import timedelta, datetime
import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext


hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
         "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
         "20", "21", "22", "23"]
minutes = ["00","15","30","45"]

def gdelt_header(location = "gdelt_header.txt"):
    """
    Function to get the gdelt headers.
    
    ::param location: (string) Location of text file of gdelt columns
    ::return: (list)
    """
    file = open(location, 'r') 
    return file.read().splitlines()


def date_range(start_date, end_date):
    """
    Get a list of dates between two dates.
    
    ::param start_date: (string), in format '%Y%m%d'
    ::param end_date: (string), in format '%Y%m%d'
    ::return: (list[string])
    """
    st = datetime.strptime(start_date, "%Y%m%d").date()
    et = datetime.strptime(end_date, "%Y%m%d").date()
    
    delta = et - st
    
    for i in range(delta.days + 1):
        yield (st + timedelta(days=i)).strftime("%Y%m%d")


def bz2_to_parquet_single(
    spark, bz2, parquet_file, columns
):
    """
    Function to convert bz2 files to a single parquet files.
    
    Note:
        Aim is to convert the gdelt bz2 files split divided into 15 minutes 
        to a daily parquet file. 

    ::param spark: (SparkSession) 
    ::param bz2: (string) Location of the bzip files (can use ?*)
    ::param parquet_file: (string) Location to save to, single location.
    ::param columns: (list[string])
    """
    dataFrame = spark\
    .read\
    .option("delimiter", "\t").csv(bz2, header = False)\
    .toDF(*columns)
    
    dataFrame.write.format("parquet").mode("overwrite").save(parquet_file)
    print(f"Saved {parquet_file}")
    
    
def bz2_to_parquet(
    spark, bz2_folder, parquet_folder,
    start_date, end_date, 
    columns = gdelt_header()
):
    """
    Function to convert bz2 files to a parquet files.
    Does this for a range of dates.
    
    Note:
        Aim is to convert the gdelt bz2 files split divided into 15 minutes 
        to a daily parquet file. 

    ::param spark: (SparkSession) 
    ::param bz2: (string) Location of the bzip files (can use ?*)
    ::param parquet: (string) Location to save to, single location.
    ::param start_date: (string), in format '%Y%m%d'
    ::param end_date: (string), in format '%Y%m%d'
    ::param columns: (list[string]), default is './gdelt_header.txt'
    """
    
    dates = list(date_range(start_date, end_date))
    print(f"{len(list(dates))} dates between {start_date} and {end_date}")
    
    directory = set([bz2_folder +"/"+ file for file in os.listdir(bz2_folder)])
    
    for date in dates:
        output_file = parquet_folder+f"/GDELT_{date}.parquet"
        
        time_ = [[hour+minute for hour in hours] for minute in minutes]
        times = [item for sublist in time_ for item in sublist]
        input_files = [bz2_folder+f"/GDELT_{date}{time_}00.bz2" for time_ in times]
        input_files = [value for value in input_files if value in directory]
        if len(input_files) == 0:
            pass
        else:
            bz2_to_parquet_single(spark, input_files, output_file, columns)
            for file in input_files:
                try:
                    os.remove(file)
                except:
                    print("Error while deleting file : ", filePath)
                    

if __name__ == "__main__":
    
    spark = SparkSession.builder \
            .master("local[10]") \
            .config("spark.driver.memory", "10g") \
            .config("spark.executor.memory", "40g") \
            .appName("GDELTUpdateFiles") \
            .getOrCreate()

    sc = spark.sparkContext
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    
    bz2_to_parquet(
        spark,
        "/mnt/d/data/gdelt/gkg/bzip",
        "/mnt/d/data/gdelt/gkg/parquet",
        "20150101", "20210101")