import pandas as pd
import os
#from pymongo import MongoClient

"""  
CODIGO DE EJEMPLO PARA SUBIR LOS DATOS
"""


def uploadToDatabase(folder_path, columns_filter, list_files):
    """
    # Conectar a tu base de datos MongoDB local
    client = MongoClient('localhost', 27017)
    db = client['tu_base_de_datos']
    collection = db['tu_coleccion']
    num_files = len(list_files)
    """
    # DATAFRME VERSION
    failed_files = []

    df_database = pd.DataFrame(columns=columns_filter)
    for file in list_files:
        # Leer el archivo CSV
        try:
            df = pd.read_csv(os.path.join(folder_path, file),
                             usecols=columns_filter)
            df["id"] = file
            df_database = pd.concat([df_database, df], ignore_index=True)
        except Exception as e:
            print(f"Error al procesar el archivo {file}: {str(e)}")
            failed_files.append(file)
    # Cerrar la conexión con la base de datos
    df_database.to_csv("database.csv")
    print("Database created")
    print(df_database.describe())
    return failed_files


"""
#from pymongo import MongoClient
def uploadToDatabase(folder_path, columns_filter, list_files):
    
    # Conectar a tu base de datos MongoDB local
    client = MongoClient('localhost', 27017)
    db = client['tu_base_de_datos']
    collection = db['tu_coleccion']
    failed_files = []
    num_files = len(list_files)
    for file in list_files:
        # Leer el archivo CSV
        try:
            df = pd.read_csv(file, usecols=columns_filter)
            # Convertir el DataFrame a formato de diccionario
            data = df.to_dict(orient='records')
            # Insertar los datos en la colección de MongoDB
            collection.insert_many(data)
        except Exception as e:
            failed_files.append(file)
    # Cerrar la conexión con la base de datos
    client.close()
    return failed_files

    """
