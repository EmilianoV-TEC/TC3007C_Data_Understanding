import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import config as config
import concurrent.futures

# Obtain the number of ones, zeros, final time and initial time of a file.


def get_file_info(path, file):
    column_name = [config.BOOL_PREDICTION_VAR, "time"]
    path = os.path.join(path, file)
    new_row = {}
    try:
        # Lee el file CSV en un DataFrame de Pandas
        df = pd.read_csv(path, usecols=column_name)
        rows = len(df[column_name[0]])
        ones = (df[column_name[0]] == 1).sum()
        zeros = (df[column_name[0]] == 0).sum()
        # Verifica si hay al menos un 1 en la columna "Stable cruise"
        new_row['name'] = file
        new_row['rows'] = rows
        new_row['ones'] = ones
        new_row['zeros'] = zeros
        new_row['Intial_time'] = df['time'][0]
        new_row['Final_time'] = df['time'][rows-1]

        return new_row
    except Exception as e:
        print(f"Error al procesar el archivi {file}: {str(e)}")
    return {}

# Función que crea un nuevo csv con la información de los archivos de un directorio. Devuelve una lista con los archivos que no se han podido procesar


def count_ones(path, output_file_name):

    file_list = os.listdir(path)
    failedFiles = []
    info = pd.DataFrame(columns=['name', 'rows', 'ones', 'zeros'])
    for file in file_list:
        new_row = get_file_info(path, file)
        if new_row:
            new_row_df = pd.DataFrame([new_row])
            info = pd.concat([info, new_row_df], ignore_index=True)
        else:
            failedFiles.append(file)
    info.to_csv(output_file_name)

    return failedFiles


def count_ones_multithread(path, output_file_name):

    file_list = os.listdir(path)
    failedFiles = []
    info = pd.DataFrame(columns=['name', 'rows', 'ones', 'zeros'])
    num_threads = 6
    print(os.cpu_count())
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = [executor.submit(get_file_info, file) for file in file_list]
        for f in concurrent.futures.as_completed(results):
            new_row = f.result()
            if new_row:
                new_row_df = pd.DataFrame([new_row])
                info = pd.concat([info, new_row_df], ignore_index=True)
            else:
                failedFiles.append(f.result())

    info.to_csv(output_file_name)

    return failedFiles


def redundance_in_folder(path_folder, filtered_csv, output_file_name):
    df_filtered = pd.read_csv(filtered_csv)
    df_list_names = df_filtered['name'].tolist()
    num_files = len(df_list_names)
    df_redundance = pd.DataFrame()
    failed_files = []
    for file in df_list_names:
        try:
            df = pd.read_csv(os.path.join(path_folder, file))
            df.drop(columns=['time', config.BOOL_PREDICTION_VAR,
                    config.BOOL_PREDICTION_VAR+"2"], inplace=True)
            columns = df.columns.values
            if len(columns) != len(config.HEADER)-3:
                print("Error in file "+file+" in number of columns. Expected " +
                      str(len(config.HEADER)-3)+" and found "+str(len(df.columns.values))+" columns")
            # Calculate num of columns
            new_row = {}
            new_row['name'] = file
            new_row['num_columns'] = len(columns)
            total_error = 0
            for i in range(0, len(columns), 2):
                #print("compare "+columns[i]+" with "+columns[i+1])
                current_error = (abs(df[columns[i]]-df[columns[i+1]])).sum()
                new_row[columns[i]+"-"+columns[i+1]] = current_error
                total_error += current_error
            new_row['total_error'] = total_error
            df_redundance = pd.concat(
                [df_redundance, pd.DataFrame([new_row])], ignore_index=True)
        except Exception as e:
            print(f"Error al procesar el archivo {file}: {str(e)}")
            failed_files.append(file)

    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print("Processed the "+str(num_files-len(failed_files))+" files successfully")
    df_redundance.to_csv(output_file_name)
