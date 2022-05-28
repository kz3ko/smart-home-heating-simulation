from os import listdir
from math import floor

from pandas import DataFrame, read_csv
from matplotlib import pyplot as plt


def get_data_from_csv_file(file_path: str, sep: str = ',', quotechar: str = '"') -> DataFrame:
    return read_csv(file_path, sep=sep, quotechar=quotechar)


def get_dataframes_from_directory(directory_path: str) -> dict[str, DataFrame]:
    dataframes = dict()
    for file in listdir(directory_path):
        dataframes[file] = get_data_from_csv_file(f'{directory_path}/{file}')

    return dataframes


def get_timestamp(dataframes: dict[str, DataFrame]) -> DataFrame:
    return list(dataframes.values())[0]['timestamp']


def get_ticks_positions(df: DataFrame, n: int) -> list:
    tick_step = floor(len(df)/n)
    return df.iloc[::tick_step]


def main():
    logs_directory = input('Please, provide name of logs directory that you want to use: ')
    log_dataframes = get_dataframes_from_directory(logs_directory)

    fig, ax = plt.subplots()
    timestamp = get_timestamp(log_dataframes)
    for room_uid, room_data in log_dataframes.items():
        ax.plot(timestamp, room_data['currentTemperature'], label=room_uid.split('-')[-1])
    ax.legend()
    plt.grid()
    ticks_positions = get_ticks_positions(timestamp, 3)
    plt.xticks(ticks_positions)
    plt.title('Rooms temperature')
    plt.xlabel('Timestamp [HH:MM dd:mm:yyyy]')
    plt.ylabel('Temperature [°C]')
    plt.show()


if __name__ == '__main__':
    main()