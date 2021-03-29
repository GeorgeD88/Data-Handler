from log_controller import setup_logger
from time import time
import json
import os


module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = setup_logger(module_name, 'datahandler_activity.log')


def dump_to_json(chunk_pack: list, export_name: str, indent=2):
    """
    Dumps chunk pack (list of lists of dictionaries) into a json file

    Args:
        chunk_pack (list): The data to be dumped into json in the form of a chunk pack (list of lists)
        export_name (str): The filename of the json file we're dumping to.
        indent (int or None, optional): The indent of each json file being created, defaults to 2,
            but if an indent of None is given, the files won't be indented.
    """

    start = time()  # start timer for runtime, for logging purposes
    pack_size = len(chunk_pack)  # gets size of the chunk pack
    if pack_size > 1:  # checks for pack size of more than one chunk
        os.makedirs(export_name)  # makes folder to dump the many json chunks in
        os.chdir(export_name)  # switches to new directory
    # goes through every chunk in the chunk pack and dumps each one into its own json file
    logger.info(f'started dumping {pack_size} '
                f''
                f'chunk{"s" if pack_size > 1 else ""} into json')  # logs that the dumping process has started
    for i in range(pack_size):
        constructed_filename = f'{export_name}_({i+1},{pack_size}).json'  # makes the json filename for the chunk
        logger.info(f'dumping chunk {i+1}/{pack_size}')  # logs the chunk being dumped
        with open(constructed_filename, 'w+') as out_json:
            json.dump({"chunk": chunk_pack[i]}, out_json, indent=indent)  # dumps the chunk
        logger.info(f'dumped chunk {i+1}/{pack_size}')  # logs the chunk finished dumping
    os.chdir('..')  # switches back to parent directory or else the main program will now be in the new directory
    runtime = time() - start
    logger.info(f'dumped {pack_size} chunk{"s" if pack_size > 1 else ""} in {round(runtime, 2)} sec')
