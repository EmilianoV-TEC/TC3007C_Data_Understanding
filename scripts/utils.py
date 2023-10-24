import os
import pandas as pd
import config as config
import time
from functools import wraps


# Once exists the filter.csv file, append the new filter to
def appendFilter(df, name_new_filter):
    if(not os.path.exists(os.path.join(config.CSV_PATH, "filter.csv"))):
        print("Error: Filter file not found")
        return
    try:
        df_filter = pd.read_csv(os.path.join(config.CSV_PATH, "filter.csv"))
    except Exception as e:
        print("Error reading csv file: "+str(e))
        return

    if( name_new_filter in df_filter.columns):
        print("Error: Filter", name_new_filter, "already exists")
        return
    new_filter=df['name'].tolist()
    df_filter[name_new_filter]=new_filter
    df_filter.to_csv(os.path.join(config.CSV_PATH, "filter.csv"), index=False)
    print("Filter", name_new_filter, "added to filter.csv")


def calculate_time(func):
    @ wraps(func)
    def wrapper(*args, **kwargs):
        start_time=time.time()
        result=func(*args, **kwargs)
        end_time=time.time()
        print(
            f"Execution time for {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper
