import os
import config as config
import createCSV as createCSV
import time
from functools import wraps
import pandas as pd
import summary as summary_func
import shutil
import plots as plots
import database as database_func

# Decorator to calculate the execution time of a function
def calculate_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Execution time for {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper

def clearFolders():
    if (os.path.exists(config.TEST_PATH)):
        print("Deleting test_data folder")
        shutil.rmtree(config.TEST_PATH)
    if (os.path.exists(config.DUMMIES_PATH)):
        print("Deleting dummies_data folder")
        shutil.rmtree(config.DUMMIES_PATH)

# Setting up the environment


def printConfigVariables():
    print("BASE_PATH: "+config.BASE_PATH)
    print("DUMMIES_PATH: "+config.DUMMIES_PATH)
    print("NUM_DUMMIES_FILES: "+str(config.NUM_DUMMIES_FILES))
    print("SIZE_DUMMIES_FILES: "+str(config.SIZE_DUMMIES_FILES))
    print("TEST_PATH: "+config.TEST_PATH)
    print("NUM_TEST_FILES: "+str(config.NUM_TEST_FILES))
    print("SIZE_TEST_FILES: "+str(config.SIZE_TEST_FILES))


def createTestFolders():
    if (os.path.exists(config.TEST_PATH)):
        print("test_data folder already exists")
    else:
        print("Creating test_data folder")
        os.mkdir(config.TEST_PATH)
        calculate_time(createCSV.createData)(config.NUM_TEST_FILES,config.SIZE_TEST_FILES, config.TEST_PATH)


def createDummiesFolders():
    if (os.path.exists(config.DUMMIES_PATH)):
        print("dummies_data folder already exists")
    else:
        print("Creating dummies_data folder")
        os.mkdir(config.DUMMIES_PATH)
        calculate_time(createCSV.createData)(config.NUM_DUMMIES_FILES,config.SIZE_DUMMIES_FILES, config.DUMMIES_PATH)




# Now we will define the functions that use a path with the data and


def count_ones(path, output_file_name):
    print("Creating summary file " + output_file_name + " in " + path)
    failed_files = calculate_time(summary_func.count_ones)(path, output_file_name)
    print(len(os.listdir(path))-len(failed_files),
          "files processed successfully")
    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print(output_file_name, "created")


def count_ones_multithread(path, output_file_name):
    print("Creating summary file multithread " +
          output_file_name + " in " + path)
    failed_files = calculate_time(summary_func.count_ones_multithread)(path, output_file_name)
    print(len(os.listdir(path))-len(failed_files),
          "files processed successfully")
    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print(output_file_name, "created")


def plot_ones(path, ones_csv):
    if not os.path.exists(path):
        print("Error: path does not exist")
        return
    print("Plotting ones from " + ones_csv + " in " + path)
    df = pd.read_csv(os.path.join(path, ones_csv))
    plots.plot_ones(df)
    print("Plot created")


def testVelocity():
    calculate_time(count_ones)(config.TEST_PATH, "test_summary.csv")


def filterFiles(path, ones_csv, output_file_name):
    if not os.path.exists(path):
        print("Error: path does not exist")
        return
    print("Filtering files from " + ones_csv + " in " + path)
    df = pd.read_csv(os.path.join(path, ones_csv))
    df = df.drop(df.columns[0], axis=1)
    df = df[df['ones'] > 0]
    df.to_csv(output_file_name)
    print("Filter created in "+output_file_name)


def redundance(path_folder, filtered_csv, output_file_name):
    if not os.path.exists(path_folder):
        print("Error: path does not exist")
        return
    print("Creating "+output_file_name+" as output")
    print("Calculating redundance from in " + path_folder)
    print("Using "+filtered_csv+" as filter")
    calculate_time(summary_func.redundance_in_folder)(path_folder, filtered_csv, output_file_name)
    print("Redundance calculated")


def plotRedundance(base_path, redundance_csv):
    print("Plotting redundance from " + redundance_csv+ " in " + base_path)
    df = pd.read_csv(os.path.join(base_path, redundance_csv))
    plots.plotRedundance(df)
    print("Plot created")



def filterColumns(header):
    #Always include time that is in the first position
    columns_filter=[header[0]]
    print("Using "+header[0]+" column")
    for i in range(1, len(header), 2):
        print("Use "+header[i]+" ,discard "+header[i+1])
        columns_filter.append(header[i])
    return columns_filter


def uploadToDatabase(folder_path, csv_filter):
    if not os.path.exists(folder_path):
        print("Error: path does not exist")
        return
    print("Filtering columns")
    columns_filter = filterColumns(config.HEADER)
    print("Using "+str(len(columns_filter))+" columns")

    try:
        df_filtered = pd.read_csv(os.path.join(config.BASE_PATH, csv_filter))
    except Exception as e:
        print("Error reading csv filter file: "+str(e))
        return
    list_files = df_filtered['name'].tolist()
    num_files = len(list_files)
    print("Uploading to database")
    failed_files = calculate_time(database_func.uploadToDatabase)(folder_path, columns_filter, list_files)
    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print("Files uploaded to database: "+str(num_files-len(failed_files)))
