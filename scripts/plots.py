import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import dict_filter as dict_filter


def plot_ones(df):

    print("Number of rows", df["rows"].sum())
    print("Number of ones", df["ones"].sum())
    print("Number of zeros", df["zeros"].sum())
    print("Percentage of ones", df["ones"].sum()/df["rows"].sum())

    df["contains_ones"] = df["ones"] > 0
    df["weightOnes"] = df["ones"] / df["rows"]
    print(df.describe())

    # Plot a histogram of weight ones
    plt.figure(figsize=(8, 6))
    sns.histplot(df['weightOnes'])
    # Customize the plot (optional)
    plt.title('Histogram of weight ones')
    plt.xlabel('Weight ones')
    plt.ylabel('Frequency')
    # Show the plot
    plt.show()

    # Plot a histogram of weight ones vs num of rows
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="weightOnes", y="rows", hue="contains_ones")
    # Customize the plot (optional)
    plt.title('Scatterplot of weight ones vs num of rows')
    plt.xlabel('Weight ones')
    plt.ylabel('Num of rows')
    # Show the plot
    plt.show()

    # plot line time vs row
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="Final_time", y="rows")
    # Customize the plot (optional)
    plt.title('Lineplot of time vs rows')
    plt.xlabel('Time')
    plt.ylabel('Num of rows')
    # Show the plot
    plt.show()

    # plot zeros files distribution by rows size
    plt.figure(figsize=(8, 6))
    sns.histplot(df[df['contains_ones'] == False]['rows'])
    # Customize the plot (optional)
    plt.title('Histogram of zeros files distribution by rows size')
    plt.xlabel('Rows')
    plt.ylabel('Frequency')
    # Show the plot
    plt.show()

    # plot ones files distribution by rows size
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df[df['contains_ones'] == True],
                    x="rows", y="ones", hue="weightOnes")
    # Customize the plot (optional)
    plt.title('Histogram of ones files distribution by rows size')
    plt.xlabel('Rows')
    plt.ylabel('Frequency')
    # Show the plot
    
'''
def plotDescriptiveStatistics(df):
    unique_files = df.index.get_level_values(0).unique()
    unique_vars = df.index.get_level_values(1).unique()
    num_files = len(unique_files)

    num_vars = len(unique_vars)
    ncols = -(-num_vars // 3)
    nrows = 3

    random_files = random.choices(selected_files, k=10)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 5 * nrows))


    if num_vars == 1:
        axes = np.array([[axes]])

    for i, var in enumerate(unique_vars):
        # Extrae los datos de la variable específica
        subset = df.xs(var, level=1)
        subset = subset.loc[random_files]
        subset.drop(['count', 'max', 'min'], axis=1, inplace=True)

        row = i // ncols
        col = i % ncols

        subset.plot(kind='bar', ax=axes[row, col], legend=True)
        axes[row, col].set_title(var)
        axes[row, col].set_ylabel('Estadísticas Descriptivas')
        axes[row, col].set_xlabel('Archivo')

    plt.tight_layout()
    plt.legend(loc='upper left', bbox_to_anchor=(1,1))
    plt.show()
'''

def plotRedundance(df):
    # Plot error per pair of columns
    print("Original columns", df.columns)
    print("deleting columns", df.columns[[0, 1, 2, -1]])
    df_temp = df.drop(df.columns[[0, 1, 2, -1]], axis=1)

    plt.figure(figsize=(8, 6))
    sns.histplot(df['total_error'])
    # Customize the plot (optional)
    plt.title('Histogram of total error')
    plt.xlabel('Total error')
    plt.ylabel('Frequency')
    # Show the plot
    plt.show()

    print("Columns to plot pair of columns", df_temp.columns)
    df_temp = df_temp.describe().T
    df_temp["mean"]
    plt.figure(figsize=(8, 6))
    sns.barplot(x=df_temp.index, y=df_temp['mean'])
    plt.title('Erro per pair of column', fontsize=16)
    plt.xlabel('Columns', fontsize=14)
    plt.ylabel('Mean error', fontsize=14)
    plt.xticks(rotation=90)
    plt.show()

def plotRedundanceCounts(df):
    df_counts = df.groupby(['columns']).sum()

    # We get only errors caused by non-missing values
    df_counts['total_errors'] -= (df_counts['left_missing_errors'] + df_counts['right_missing_errors']) 
    df_counts.rename(columns={"total_errors" : "other_errors"}, inplace = True)

    sns.set(rc={'figure.figsize':(15,5)})

    # Change datafreme format for barplot
    df_counts = pd.melt(df_counts.reset_index(), id_vars = 'columns', var_name = 'error_type', value_name = 'error_count')
    
    sns.catplot(data = df_counts, x = 'columns', y = 'error_count', hue = 'error_type', kind = 'bar', height = 2, aspect = 4)

    plt.title('Error counts per pair of columns', fontsize=12)
    plt.xlabel('Columns', fontsize = 2)
    plt.ylabel('Error counts', fontsize = 8)
    plt.xticks(rotation = 90)
    plt.show()
    
'''
def visualizeRedundance(df):
    columns = (df.columns).to_numpy()
    n_plots = len(columns) // 2
    ncols = -(-n_plots // 3)
    nrows = 3

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 5 * nrows))

    if n_plots == 1:
        axes = [[axes]]

    for i in range(0, len(columns)-1, 2):
        row = (i // 2) // ncols
        col = (i // 2) % ncols

        axes[row][col].scatter(df.index, df1[columns[i]], label=columns[i], color='mediumvioletred')
        axes[row][col].scatter(df.index, df1[columns[i+1]], label=columns[i+1], color='darkslateblue')
        axes[row][col].set_title(columns[i] + ' & ' + columns[i+1])
        axes[row][col].set_xlabel('Time')
        axes[row][col].legend(loc='upper left')


    plt.tight_layout()
    plt.show()
'''

def plotInconsistenciesPer(df):
    
    # Selecciona la columna 'Porcentaje de Diferencia' para graficarla
    porcentaje_diferencia_columna = df['Porcentaje de Diferencia']

    # Crea un gráfico de barras para visualizar los porcentajes de diferencia
    plt.figure(figsize=(10, 6))
    porcentaje_diferencia_columna.plot(kind='bar', legend=False)
    plt.xlabel('No. Columnas')
    plt.ylabel('Diferencia')
    plt.title('Porcentaje de Diferencia entre Columnas')
    plt.xticks(rotation=45)  # Rota las etiquetas del eje x para mayor legibilidad
    plt.tight_layout()
    plt.show()
