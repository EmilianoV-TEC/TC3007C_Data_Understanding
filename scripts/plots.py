import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_ones(df):
    df["contains_ones"] = df["ones"] > 0
    df["weightOnes"] = df["ones"] / df["rows"]
    print(df.describe())

    # Plot a histogram of weight ones
    plt.figure(figsize=(8,6))
    sns.histplot(df['weightOnes'])
    # Customize the plot (optional)
    plt.title('Histogram of weight ones')
    plt.xlabel('Weight ones')
    plt.ylabel('Frequency')
    # Show the plot
    plt.show()

    # Plot a histogram of weight ones vs num of rows
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x="weightOnes", y="rows", hue="contains_ones")
    # Customize the plot (optional)
    plt.title('Scatterplot of weight ones vs num of rows')
    plt.xlabel('Weight ones')
    plt.ylabel('Num of rows')
    # Show the plot
    plt.show()

    # plot line time vs row
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x="Final_time", y="rows")
    # Customize the plot (optional)
    plt.title('Lineplot of time vs rows')
    plt.xlabel('Time')
    plt.ylabel('Num of rows')
    # Show the plot
    plt.show()


def plotRedundance(df):
    # Plot error per pair of columns
    print("Original columns", df.columns)
    df_temp = df.drop(df.columns[[0, 1, 2, -1]], axis=1)

    plt.figure(figsize=(8,6))
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
    plt.figure(figsize=(8,6))
    sns.barplot(x=df_temp.index, y=df_temp['mean'])
    plt.title('Erro per pair of column', fontsize=16)
    plt.xlabel('Columns', fontsize=14)
    plt.ylabel('Mean error', fontsize=14)
    plt.xticks(rotation=90)
    plt.show()
