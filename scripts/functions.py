import os
import config as config
import createCSV as createCSV
import pandas as pd
import summary as summary_func
import shutil
import plots as plots
import database as database_func
import utils as utils_func
import dict_filter as dict_filter
# Decorator to calculate the execution time of a function


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
        utils_func.calculate_time(createCSV.createData)(
            config.NUM_TEST_FILES, config.SIZE_TEST_FILES, config.TEST_PATH)


def createDummiesFolders():
    if (os.path.exists(config.DUMMIES_PATH)):
        print("dummies_data folder already exists")
    else:
        print("Creating dummies_data folder")
        os.mkdir(config.DUMMIES_PATH)
        utils_func.calculate_time(createCSV.createData)(
            config.NUM_DUMMIES_FILES, config.SIZE_DUMMIES_FILES, config.DUMMIES_PATH)


# Now we will define the functions that use a path with the data and


def summary_count_ones(path, output_file_name):
    print("Creating summary file " + output_file_name + " in " + path)
    failed_files = utils_func.calculate_time(
        summary_func.summary_count_ones)(path, output_file_name)
    print("Failed files: "+str(failed_files))


def plot_ones(ones_csv, filter_name=None):
    path = config.CSV_PATH
    if not os.path.exists(path):
        print("Error: path does not exist")
        return
    print("Plotting ones from " + ones_csv + " in " + path)
    try:
        df = pd.read_csv(os.path.join(path, ones_csv))
        print("Read csv file successfully")
    except Exception as e:
        print("Error reading csv file: "+str(e))
        return

    if filter_name:
        filter = dict_filter.getFilter(filter_name)
        print("Using filter", filter_name)
        df = df[df['name'].isin(filter)]
        print("Filter", filter_name, "applied")

    print(df.columns)
    plots.plot_ones(df)
    print("Plot created")


def restartFilter(folder_path):
    print("Restarting filter in "+folder_path)
    dict_filter.restartFilter(folder_path)
    print("Filter restarted")


def AddFilterOnes(csv_file):
    print("Adding filter of ones in from "+csv_file)
    try:
        df = pd.read_csv(os.path.join(config.CSV_PATH, csv_file))
    except Exception as e:
        print("Error reading csv file: "+str(e))
        return
    # Filter the ones
    df_temp = df[df['ones'] > 0]
    # Add the filter
    dict_filter.addFilter(df_temp, "onlyOnes")
    # Filter the zeros
    df_temp = df[df['ones'] == 0]
    dict_filter.addFilter(df_temp, "onlyZeros")
    # Filter the zeros


def summaryRedundance(path_folder, output_file_name):
    if not os.path.exists(path_folder):
        print("Error: path does not exist")
        return
    print("Creating "+output_file_name+" as output")
    print("Calculating redundance in "+path_folder)
    utils_func.calculate_time(summary_func.summary_redundance)(
        path_folder, output_file_name)
    print("Redundance calculated")

def summaryRedundanceCounts(path_folder, output_file_name):
    if not os.path.exists(path_folder):
        print("Error: path does not exist")
        return
    print("Creating "+output_file_name+" as output")
    print("Calculating redundance counts in "+path_folder)
    utils_func.calculate_time(summary_func.summary_redundance_counts)(
        path_folder, output_file_name)
    print("Redundance counts calculated")


def plotRedundance(redundance_csv):
    print("Plotting redundance from " +
          redundance_csv + " in " + config.CSV_PATH)
    df = pd.read_csv(os.path.join(config.CSV_PATH, redundance_csv))
    plots.plotRedundance(df)
    print("Plot created")

def plotRedundanceCounts(redundance_counts_csv):
    print("Plotting redundance counts from " +
          redundance_counts_csv + " in " + config.CSV_PATH)
    df = pd.read_csv(os.path.join(config.CSV_PATH, redundance_counts_csv))
    plots.plotRedundanceCounts(df)
    print("Plot created")


def filterColumns(header):
    # Always include time that is in the first position
    columns_filter = [header[0]]
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
    failed_files = utils_func.calculate_time(database_func.uploadToDatabase)(
        folder_path, columns_filter, list_files)
    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print("Files uploaded to database: "+str(num_files-len(failed_files)))


def summaryDescriptiveStats(path, output_file_name):
    print("Creating descriptive stats in path "+path)
    utils_func.calculate_time(summary_func.summary_descriptive_stats)(
        path, output_file_name)
    print("Creating "+output_file_name+" as output")


def deleteFilter(name_filter):
    dict_filter.deleteFilter(name_filter)
    print("Filter", name_filter, "deleted")


def AddFilterBySize(csv_file):
    print("Adding filter of ones in from "+csv_file)
    try:
        df = pd.read_csv(os.path.join(config.CSV_PATH, csv_file))
    except Exception as e:
        print("Error reading csv file: "+str(e))
        return
    # Filter the ones
    df = df[df['ones'] > 0]
    # Add the filter

    dict_filter.addFilter(df, "SmallFiles")

def summaryInconInconsistencies(path, output_file_name):
    ##Pepe
    print("Creating Inconsistencies stats in path "+path)
    utils_func.calculate_time(summary_func.summary_inconsistencies)(
        path, output_file_name)
    print("Creating "+output_file_name+" as output")

def plotInconsistencies(redundance_csv):
    print("Plotting inconsistencies from " +
            redundance_csv + " in " + config.CSV_PATH)
    df = pd.read_csv(os.path.join(config.CSV_PATH, redundance_csv))
    plots.plotInconsistenciesPer(df)
    print("Plot created")
