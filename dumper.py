from log_controller import setup_logger
from time import time
import json
import os


module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = setup_logger(module_name, 'datahandler_activity.log')


def dump_to_json(chunk_pack: list, export_name: str, indent=2):
    """
    Dumps chunk pack (list of lists of dicts) into a json file

    Args:
        chunk_pack (list): The data to be dumped into json in the form of a chunk pack (list of lists)
        export_name (str): The filename of the json file we're dumping to.
        indent (int or None, optional): The indent of each json file being created, defaults to 2,
            but if an indent of None is given, the files won't be indented.
    """

    start = time()
    pack_size = len(chunk_pack)

    # checks if there are multiple chunks and makes a folder to store them if true
    if pack_size > 1:
        os.makedirs(export_name)
        os.chdir(export_name)
    logger.info(f'started dumping {pack_size} '
                f'chunk{"s" if pack_size > 1 else ""} into json')

    # goes through every chunk in the chunk pack and dumps each one into its own json file
    for i in range(pack_size):
        constructed_filename = f'{export_name}_({i+1},{pack_size}).json'
        logger.info(f'dumping chunk {i+1}/{pack_size}')
        with open(constructed_filename, 'w+') as out_json:
            json.dump({"chunk": chunk_pack[i]}, out_json, indent=indent)
        logger.info(f'dumped chunk {i+1}/{pack_size}')

    # if new folder was made for dumping process, it will switch back to the parent directory
    if pack_size > 1:
        os.chdir('..')
    runtime = time() - start
    logger.info(f'dumped {pack_size} chunk{"s" if pack_size > 1 else ""} in {round(runtime, 2)} sec')
