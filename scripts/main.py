import functions as f
import config

# f.printConfigVariables()
# f.clearFolders()

# Name of the file that will contain the summary of the files
ones_summary_file = "summary_ones.csv"
csv_names_filtered = "filtered.csv"
redundance_file = "redundance.csv"
descriptive_file = "descriptive.csv"

DATA_FOLDER_PATH = config.TEST_PATH


f.createTestFolders()
f.restartFilter(DATA_FOLDER_PATH)

f.summary_count_ones(DATA_FOLDER_PATH, ones_summary_file)
# f.plot_ones(ones_summary_file)  # Revisar que se esté en csv PATH

# f.deleteFilter("only_ones")

f.AddFilterOnes(ones_summary_file) #Required once summary file


#f.plot_ones(ones_summary_file, "only_ones")


# Path folder is the path where the files are located, and filtered_csv is the name of the csv file that contains the filtered files
#f.redundance(DATA_FOLDER_PATH, csv_names_filtered, redundance_file)
# f.plotRedundance(redundance_file)

#f.summaryRedundance(DATA_FOLDER_PATH, redundance_file)
# f.plotRedundance(redundance_file)

f.summaryDescriptiveStats(DATA_FOLDER_PATH, descriptive_file)

#f.plotRedundance(redundance_file)
#f.summaryRedundanceCounts(DATA_FOLDER_PATH, redundance_counts_file)
#f.plotRedundanceCounts(redundance_counts_file)

#f.summaryDescriptiveStats(DATA_FOLDER_PATH,descriptive_file)

#f.summaryInconInconsistencies(DATA_FOLDER_PATH, redundance_file)
f.plotInconsistencies(redundance_file)

"""Con la gráfica de redundancia responder ¿Cuántos archivos tienen redundancia?
    ¿Cuál es el error medio de la redundancia en cada archivo?
    ¿La redundancia presenta diferencia significativa?
    ¿Qué tipo de diferencias existen entre los pares de columnas? ¿Son desviaciones o valores faltantes?
"""
"""Una vez sabemos si la redundancia es significativa o no, podemos proceder a eliminar las columnas redundantes de los archivos.
    Para esto podemos crear una serie de resumenes que indiquen la medida de este error o desviación entre variables, así
    como el tipo de errores.
"""
# HACER LA CONEXIÓN CON LA BASE DE DATOS.
#f.uploadToDatabase(DATA_FOLDER_PATH, csv_names_filtered)

# Upload to database time execution 42 seg. 305 files, 17 columnw +- 2000 rows
# Aprox 21 segundos por 100 archivos con 17 columnas y 3000 filas
# Aprox 300 archivos de 17 columnas y 3000 filas por minuto
