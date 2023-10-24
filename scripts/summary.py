import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import config as config
import dict_filter


def createSummary(folder_path, create_new_row_from_file_function, header, output_file_name, filter_name=None):
    # Apply the filter if exists
    if filter_name:
        df_list_names = dict_filter.getFilter(filter_name)
        print("Filter used: "+filter_name)
    else:
        df_list_names = os.listdir(folder_path)
        print("No filter used")

    num_files = len(df_list_names)
    failed_files = []
    print("Creating summary with the function " +
          create_new_row_from_file_function.__name__)
    df = pd.DataFrame(columns=header)
    for file in df_list_names:
        try:
            current_df = pd.read_csv(os.path.join(folder_path, file))
            new_row = create_new_row_from_file_function(current_df)
            new_row['name'] = file

            df = pd.concat([df, new_row],
                           ignore_index=True)

        except Exception as e:
            print(f"Error al procesar el archivo {file}: {str(e)}")
            failed_files.append(file)
    if failed_files:
        print("Failed files: "+str(failed_files))
    else:
        print("No failed files")
    print("Processed the "+str(num_files-len(failed_files)) +
          " files successfully using the function "+create_new_row_from_file_function.__name__)
    df.to_csv(os.path.join(config.CSV_PATH, output_file_name), index=False)
    print("Summary created in "+output_file_name)


# Función que crea un nuevo csv con la información de los archivos de un directorio. Devuelve una lista con los archivos que no se han podido procesar


def summary_count_ones(path, output_file_name):
    header = ['name', 'rows', 'ones', 'zeros', 'Intial_time', 'Final_time']
    result = createSummary(path, summary_file_get_ones,
                           header, output_file_name)
    return result


def summary_file_get_ones(df):
    new_row = {}
    ones_variable = config.BOOL_PREDICTION_VAR
    rows = df.shape[0]
    ones = (df[ones_variable] == 1).sum()
    zeros = (df[ones_variable] == 0).sum()
    # Verifica si hay al menos un 1 en la columna "Stable cruise"
    new_row['rows'] = rows
    new_row['ones'] = ones
    new_row['zeros'] = zeros
    new_row['Intial_time'] = df['time'][0]
    new_row['Final_time'] = df['time'][rows-1]
    return new_row


def summary_redundance(path_folder, output_file_name):
    header = ['name', 'num_columns', 'total_error']
    result = createSummary(path_folder, summary_file_get_redundance,
                           header, output_file_name)
    return result


def summary_file_get_redundance(df):
    new_row = {}
    df.drop(columns=['time', config.BOOL_PREDICTION_VAR,
                     config.BOOL_PREDICTION_VAR+".1"], inplace=True)
    columns = df.columns.values

    new_row['num_columns'] = len(columns)
    total_error = 0
    for i in range(0, len(columns), 2):
        #print("compare "+columns[i]+" with "+columns[i+1])
        left_col_normalized = (df[columns[i]] - df[columns[i]].min()) / (df[columns[i]].max() - df[columns[i]].min())
        right_col_normalized = (df[columns[i+1]] - df[columns[i+1]].min()) / (df[columns[i+1]].max() - df[columns[i+1]].min())

        current_error = (abs(left_col_normalized - right_col_normalized)).sum()
        new_row[columns[i]+"-"+columns[i+1]] = current_error
        total_error += current_error
        new_row['total_error'] = total_error
    return new_row

def summary_redundance_counts(path_folder, output_file_name):
    header = []
    result = createSummary(path_folder, summary_file_get_redundance_counts,
                           header, output_file_name)
    return result

def summary_file_get_redundance_counts(df):
    new_data = pd.DataFrame(columns = ['columns', 'left_missing_errors', 'right_missing_errors', 'total_errors'])
    df.drop(columns=['time', config.BOOL_PREDICTION_VAR,
                     config.BOOL_PREDICTION_VAR+".1"], inplace=True)
    
    columns = df.columns.values

    for i in range(0, len(columns), 2):
        #print("compare "+columns[i]+" with "+columns[i+1])
        left_missing_errors = len(df[(df[columns[i]] == 0) & (df[columns[i+1]] != 0)])
        right_missing_errors = len(df[(df[columns[i]] != 0) & (df[columns[i+1]] == 0)])
        total_errors = len(df[df[columns[i]] != df[columns[i+1]]])

        new_row = {}
        new_row['columns'] = columns[i] + "-" + columns[i+1]
        new_row['left_missing_errors'] = left_missing_errors
        new_row['right_missing_errors'] = right_missing_errors
        new_row['total_errors'] = total_errors

        new_data.loc[len(new_data)] = new_row

    return new_data


def summary_descriptive_stats(path_folder, output_file_name):
    header = []
    result = createSummary(path_folder, summary_file_descriptive_stats,
                           header, output_file_name)
    return result


def summary_file_descriptive_stats(df):

    df = df.describe().T
    df.reset_index(level=0, inplace=True)
    print(df)
    return df

def summary_inconsistencies_stats(df):
    ##pp
    # Elimina la columna 'time' si existe
    if 'time' in df.columns:
        df = df.drop('time', axis=1)

    num_columnas = len(df.columns)

    # Crear un diccionario para almacenar los porcentajes de diferencia
    diferencias = {}

    for i in range(0, num_columnas, 2):
        col1 = df.iloc[:, i]
        col2 = df.iloc[:, i + 1]

        # Calcular la diferencia entre las columnas
        diferencia = (col1 - col2).abs()

        # Calcular el porcentaje de diferencia
        porcentaje_diferencia = (diferencia.sum() / len(df)) * 100

        # Almacenar el porcentaje de diferencia en el diccionario
        diferencias[f'Columnas {i} y {i + 1}'] = porcentaje_diferencia

    # Crear un nuevo DataFrame a partir del diccionario de resultados
    resultados_df = pd.DataFrame.from_dict(diferencias, orient='index', columns=['Porcentaje de Diferencia'])
    return resultados_df

def summary_inconsistencies(path_folder, output_file_name):
    header = []
    result = createSummary(path_folder, summary_inconsistencies_stats,
                           header, output_file_name)
    return result