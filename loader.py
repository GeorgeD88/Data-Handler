from log_controller import setup_logger
from time import time
import json
import csv


module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = setup_logger(module_name, 'datahandler_activity.log')


def load_from_csv(csv_filename: str, chunk_size: int or None = 1000000) -> dict:
    """
    Loads data from file of filetype .csv and returns the data as a pack (dict) of chunks (list of dicts)

    If a different chunk size is preferred, use the keyword argument chunk_size with the desired size, e.g.

    loader.load_from_csv("csv_file.csv", chunk_size=1024)

    Args:
        csv_filename (str): The filename of the csv file we're loading in.
        chunk_size (int or None, optional): The size of each chunk, defaults to 1000000 rows,
            but if a size of None is given, the chunk will not limit the number of rows.

    Returns:
        Returns a pack of chunks (dict of elements) and each chunk (list),
        contains many rows (dictionaries), each row from each csv row::
            {
                "csv_file_chunk1":
                    [
                        {'row1': row1},
                        {'row2': row2},
                        {...}
                    ],
                "csv_file_chunk2":
                    [
                        {'row3': row3},
                        {'row4': row4},
                        {...}

                    ],
                    [...]
            }
    """

    start = time()
    with open(csv_filename) as in_csv:
        csv_reader = csv.reader(in_csv, delimiter=',')
        logger.info(f'started reading csv file {csv_filename}')
        header = next(csv_reader)
        parts = 1
        chunk_pack = {}  # the chunk pack is a dict that will store each chunk of data
        chunk_insert = []  # the chunk insert is where the chunk of data is constructed to be inserted into the pack

        # if a chunk size of None was given, it'll keep the data in one chunk instead of splitting it into many chunks
        if not chunk_size:
            for row in csv_reader:
                row_insert = {}
                for key_i in range(len(header)):
                    row_insert[header[key_i]] = row[key_i]
                chunk_insert.append(row_insert)
            key_name = csv_filename[:-4] + '_chunk1'
            chunk_pack[key_name] = chunk_insert.copy()
        # else if a chunk size IS given, it'll split the data into chunks using the given chunk size as a limit
        else:
            counter = 0
            for row in csv_reader:
                # if the row counter reaches the same number as the chunk size limit, it'll start adding to a new chunk
                if counter == chunk_size:
                    logger.info(f'sealed chunk {parts}')
                    key_name = csv_filename[:-4] + '_chunk' + str(parts)
                    chunk_pack[key_name] = chunk_insert.copy()
                    chunk_insert = []
                    counter = 0
                    parts += 1
                row_insert = {}
                for key_i in range(len(header)):
                    row_insert[header[key_i]] = row[key_i]
                chunk_insert.append(row_insert)
                counter += 1
            # the last chunk most likely won't hit the chunk size limit, so at the end we'll just add it manually
            if chunk_insert:
                key_name = csv_filename[:-4] + '_chunk' + str(parts)
                chunk_pack[key_name] = chunk_insert.copy()
    runtime = time() - start
    logger.info(f'extracted csv data from file {csv_filename} into {parts} '
                f'chunk{"s" if parts > 2 else ""} in {round(runtime, 2)} sec')
    return chunk_pack


def load_from_json(json_filename: str) -> dict:
    """
    Loads data from file of filetype .json and returns the data as a chunk pack (dict),
        containing the items from the json file. When loading data from the json file instead of csv,
        the chunk pack is simply a dict of the json file itself with every key value pair being a chunk;
        rather than the chunk pack being a manually constructed dict like with csv data.

    Args:
        json_filename (str): The filename of the json file we're loading in.

    Returns:
        Returns the same data (dict) as the file, nothing fancy or extra::
            {
                "key": value,
                "key": value,
                "key": ...
            }
    """

    start = time()
    # simply opens the json file loads it in
    with open(json_filename) as in_json:
        data = json.load(in_json)
        logger.info(f'started reading json file {json_filename}')
    runtime = time() - start
    logger.info(f'extracted json data from file {json_filename} in {round(runtime, 2)} sec')
    return data
