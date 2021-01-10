#### GDELT  

Project to explore GDELT data.  
Need at least 2.5TB storage.

#### ingestion\  
Bash scripts to ingest raw gkg gdelt files from the url http://data.gdeltproject.org/gdeltv2/*.gkg.csv.zip, and saves them as .bzip files in a given location.  

However this can be slow, as we encounter Sparks small file issue.  
I have created a file called bz2_to_parquet.py, that saves the .bz2 files into parquet files.  
Thee parquet files are on a date level, which reduces the file numbers from 200'000 to around 2'400 folders, and saves the headers.  
This increases the compute time massively (less decoding), however, saving as parquet doubles the storage needed.  
Hence I am only looking at the data since 2017 (opposed to GDELTs minimum date of 2015)  


#### analytics\
TBC
