from log_controller import setup_logger
from time import time
import json
import csv


module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = setup_logger(module_name, 'datahandler_activity.log')


def load_from_csv(csv_filename: str, chunk_size=1000000) -> list:
    """
    Loads data from file of filetype .csv and returns the data

    If a different chunk size is preferred, use the keyword argument chunk_size with the desired size, e.g.

    loader.load_from_csv("csv_file.csv", chunk_size=1024)

    Args:
        csv_filename (str): The filename of the csv file we're loading in.
        chunk_size (int or None, optional): The size of each chunk, defaults to 1000000 rows,
            but if a size of None is given, the chunk will not have a limited amount of rows.

    Returns:
        Returns a pack of chunks (list of lists) and each chunk (list of dictionaries),
        contains many rows (dictionaries), each row from each csv row::
            [
                [
                    {'row1': row1},
                    {'row2': row2}
                ],
                [
                    {'row3': row3},
                    {'row4': row4},
                    {...}

                ],
                [...]
            ]
    """

    start = time()  # start timer for runtime, for logging purposes
    with open(csv_filename) as in_csv:
        csv_reader = csv.reader(in_csv, delimiter=',')  # defines csv reader with the delimiter as ","
        logger.info(f'started reading csv file {csv_filename}')  # logs that the loading process has started
        header = next(csv_reader)  # defines the header as the first line
        parts = 1  # defines part as 1 because there's always at least 1 chunk
        chunk_pack = []  # defines a list of lists to store the different chunks of data
        chunk_insert = []  # defines a chunk insert so once a chunk is completed, it's added to the chunk pack
        if not chunk_size:  # loads everything into 1 chunk, regardless of number of rows, for ease of traversal
            for row in csv_reader:
                insert = {}  # defines an empty dictionary to fill with row info and append to chunk
                for key_i in range(len(header)):
                    insert[header[key_i]] = row[key_i]  # defines the key with data from the corresponding csv column
                chunk_insert.append(insert)
            chunk_pack.append(chunk_insert.copy())  # adds newly created chunk to the chunk pack
        else:  # for standard csv processing, splits into chunks
            counter = 0  # defines a counter to count the line of the current chunk
            for row in csv_reader:
                if counter == chunk_size:  # checks if current chunk being built is as big as the max chunk size
                    logger.info(f'sealed chunk {len(chunk_pack)}')  # logs the chunk being sealed
                    chunk_pack.append(chunk_insert.copy())  # adds the newly finished chunk to the chunk pack
                    chunk_insert = []  # resets chunk to empty to prepare for a new chunk
                    counter = 0  # resets the counter to 0 cause it's onto a new chunk
                    parts += 1  # adds to the part counter
                insert = {}  # defines an empty dictionary to fill with row info and append to chunk
                for key_i in range(len(header)):
                    insert[header[key_i]] = row[key_i]  # defines the key with data from the corresponding csv column
                chunk_insert.append(insert)  # adds converted row to chunk pack
                counter += 1  # increments the counter for next row
            if chunk_insert:  # checks if the chunk_insert contains something
                chunk_pack.append(chunk_insert.copy())  # adds final chunk to the chunk pack
    runtime = time() - start
    logger.info(f'extracted csv data from file {csv_filename} into {parts} '
                f'chunk{"s" if parts > 2 else ""} in {round(runtime, 2)} sec')
    return chunk_pack


def load_from_json(json_filename: str, simple_json: bool = False):
    """
    Loads data from file of filetype .json and returns the data

    To remove redundant outer json shell because all the data is in one key,
        use the keyword argument simple_json with True value, e.g.

    loader.load_from_json("json_file.json", simple_json=True)

    Args:
        json_filename (str): The filename of the csv file we're loading in.
        simple_json (bool, optional): The simple status of the file defaults to False,
            but if status of True is given, the redundant outer json shell will be removed.

    Returns:
        Returns the data (dictionary), nothing fancy or extra::
            {
                "key": value,
                "key": value,
                "key": ...
            }
    """

    start = time()  # start timer for runtime, for logging purposes
    with open(json_filename) as in_json:
        data = json.load(in_json)  # loads json from file
        logger.info(f'started reading json file {json_filename}')  # logs that loading process has started
        if simple_json:  # ignores the redundant outer json shell
            only_key = list(data.keys())[0]  # gets the only key in the json data
            data = data[only_key]  # redefines data as the only json object in it
    runtime = time() - start
    logger.info(f'extracted json data from file {json_filename} in {round(runtime, 2)} sec')
    return data
