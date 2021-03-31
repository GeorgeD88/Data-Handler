from log_controller import setup_logger
from time import time
import json
import os


module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = setup_logger(module_name, 'datahandler_activity.log')


def dump_to_json(chunk_pack: dict, folder_name: str = None, indent: int or None = 2):
    """
    Dumps chunk pack (dict of items) into a json file by adding the data to new files or appending to existing data.

    If you would like the files to be stored in a folder,
        use the keyword argument folder_name with the desired folder name, e.g.

    dumper.dump_to_json(chunk_pack, "folder_name")

    If you want your json files to be indented at each line with an indent other than 2,
        use the keyword argument indent with the preferred indent or None for no indent, e.g.

    dumper.dump_to_json(chunk_pack, indent=4)

    Args:
        chunk_pack (dict): The data to be dumped into json in the form of a chunk pack (dict of items)
        folder_name (str, optional): The name of the folder we're dumping to,
            if left empty will default to None and not store the files in a folder.
        indent (int or None, optional): The indent of each json file being created, defaults to 2, but can be
            overwritten if a different indent is given. if an indent of None is given, the files won't be indented.
    """

    start = time()
    pack_size = len(chunk_pack)
    pack_counter = 1

    # if a folder name is provided (not None) it switches to that directory after making the folder first if needed
    if folder_name:
        if not os.path.isdir(folder_name):
            os.makedirs(folder_name)
        os.chdir(folder_name)
    logger.info(f'started dumping {pack_size} '
                f'chunk{"s" if pack_size > 1 else ""} into json')

    # goes through every chunk in the chunk pack and dumps each one into its own json file,
    # checks if json files with the same name exists and appends to them instead
    for chunk_key, chunk_value in chunk_pack.items():
        logger.info(f'dumping chunk {chunk_key} {pack_counter}/{pack_size}')
        export_file = chunk_key + '.json'

        # if the export file already exists
        if os.path.exists(export_file):
            logger.info(f'file {export_file} already exists, appending chunk to file instead')
            with open(export_file, 'r') as in_json:
                existing_data = json.load(in_json)
            # if our chunk key matches an existing key in the existing file
            if chunk_key in list(existing_data.keys()):
                logger.info(f'chunk key already exists in the file, appending to chunk instead')
                # because the value of our keys will always be lists, we append to the list in the existing key only if
                # the data is also a list, otherwise it's a "dump conflict" and we have to figure that out :/
                if type(existing_data[chunk_key]) is list:
                    existing_data[chunk_key].extend(chunk_pack[chunk_key])
                    with open(export_file, 'w') as out_json:
                        json.dump(existing_data, out_json, indent=indent)
                else:
                    # ¯\_ಠ_ಠ_/¯
                    logger.error('¯\\_ಠ_ಠ_/¯')
            # if our chunk key does not already exist in the existing file
            else:
                with open(export_file, 'w') as out_json:
                    json.dump({chunk_key: chunk_value}, out_json, indent=indent)
        # if the export file doesn't already exist, the file is created and the chunk is added
        else:
            with open(export_file, 'w+') as out_json:
                json.dump({chunk_key: chunk_value}, out_json, indent=indent)
        logger.info(f'dumped chunk {chunk_key} {pack_counter}/{pack_size}')
        pack_counter += 1

    # if new folder was made for the dumping process, it will switch back to the parent directory
    if folder_name:
        os.chdir('..')
    runtime = time() - start
    logger.info(f'dumped {pack_size} chunk{"s" if pack_size > 1 else ""} in {round(runtime, 2)} sec')
