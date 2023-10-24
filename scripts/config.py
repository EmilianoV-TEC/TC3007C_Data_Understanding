import os
# Base

CSV_PATH = 'C:\\Users\\e1000\\OneDrive\\Documents\\UNIVERSIDAD\\IA\\Reto_GE\\DataAnalitics_Reto2'
BASE_PATH = 'C:\\Users\\e1000\\OneDrive\\Documents\\UNIVERSIDAD\\IA\\Reto_GE\\DataAnalitics_Reto2'
BOOL_PREDICTION_VAR = 'target_boolean'

HEADER = ['time', 'col1_boolean', 'col2_boolean', 'col3_boolean', 'col4_boolean', 'col5_float', 'col6_float', 'col7_float', 'col8_float', 'col9_float', 'col10_float', 'col11_float', 'col12_float', 'col13_float', 'col14_float', 'col15_float', 'col16_float', 'col17_float',
          'col18_float', 'col19_float', 'col20_float', 'col21_float', 'col22_float', 'col23_float', 'col24_float', 'col25_float', 'col26_float', 'col27_float', 'col28_float', BOOL_PREDICTION_VAR, BOOL_PREDICTION_VAR + ".1", 'col31_integer', 'col32_integer', 'col33_integer', 'col34_integer', 'col35_integer', 'col36_integer']

# Dummies
DUMMIES_PATH = os.path.join(CSV_PATH, 'dummies_data')
NUM_DUMMIES_FILES = 2
SIZE_DUMMIES_FILES = 100

TEST_PATH = os.path.join(CSV_PATH, 'test_data')
NUM_TEST_FILES = 2
SIZE_TEST_FILES = 200

DATA_PATH = os.path.join(BASE_PATH, 'data')


SHOW_PLOTS = True
