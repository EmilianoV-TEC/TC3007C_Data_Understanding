import functions as f
import config

# f.printConfigVariables()
f.clearFolders()
f.createTestFolders()
f.createDummiesFolders()

#Name of the file that will contain the summary of the files
ones_summary_file = "test_summary_ones.csv"
ones_summary_file_filtered = "test_summary_ones_filtered.csv"
redundance_file = "test_redundance.csv"

f.count_ones(config.TEST_PATH, ones_summary_file)
#f.plot_ones(config.BASE_PATH, "test_summary_ones.csv")
""""
Con estas gráficas hay que responder a las preguntas:
¿Cuántos archivos tienen al menos un 1?
¿Cuántos archivos tienen al menos un 0?
¿Cuál es el tamaño medio de los archivos?
¿Cuál es el tiempo medio de los archivos?
¿Existe alguna relación entre tener un 1 y el tamaño del archivo?

Con base en eso completar la función para filtrar los archivos útiles.

Hay dos opciones de filtrado: Unicamente quedarnos con aquellos que tengan al menos un 1 o quedarnos con aquellos mayores a un tamaño, 
tal que existan archivos que de ese tamaño que tienen al menos un 1 o no tienen ninguno.
"""

f.filterFiles(config.BASE_PATH, ones_summary_file, ones_summary_file_filtered)
#f.plot_ones(config.BASE_PATH, "test_summary_ones_filtered.csv")

"""Con nuestros arvhivos filtrados volveremos a responder ¿Cuántos archivos tienen al menos un 1?
¿Cuántos archivos tienen al menos un 0?
¿Cuál es el tamaño medio de los archivos?
¿Cuál es el tiempo medio de los archivos?
"""
#Path folder is the path where the files are located, and filtered_csv is the name of the csv file that contains the filtered files
f.redundance(config.TEST_PATH, ones_summary_file_filtered, redundance_file)
#f.plotRedundance(config.BASE_PATH,redundance_file)

"""Con la gráfica de redundancia responder ¿Cuántos archivos tienen redundancia?
    ¿Cuál es el error medio de la redundancia en cada archivo?
    ¿La redundancia presenta diferencia significativa?
"""
"""Una vez sabemos si la redundancia es significativa o no, podemos proceder a eliminar las columnas redundantes de los archivos.
    Para esto podemos crear

"""
##HACER LA CONEXIÓN CON LA BASE DE DATOS.
#f.uploadToDatabase(config.TEST_PATH, ones_summary_file_filtered)