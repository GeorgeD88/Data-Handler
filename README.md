# Data-Handler
**Data-Handler** is a basic library that I made as a personal tool to use in my other projects to simplify handling huge data files.
If you were to open a large CSV file (e.g. 100,000+ rows) and save it to a JSON file, your program would take quite a while
or even worse, your data could easily end up being so big that you wouldnt be able to open the JSON file.
The other day I was attempting to convert a CSV file into a JSON file to be able to easily look through the data and mess around with it.
I kept getting an unresolvable error and it turned out that my JSON file was so big that my program was not able to open it.
My file had 2,431,727 rows!! Almost 2.5 million, which is where **Data-Handler** came in.
Instead of just importing the data and dumping it into a JSON file, **Data-Handler** parses every row of raw data for you and once it reaches a certain limit,
seals that processed data as a "chunk" and moves on. This way you end up with all of your data separated into smaller, easily readable chunks. 
Now that the data is contained in separate chunks, you're able to easily dump each chunk into a JSON file.
**Data-Handler** also implements fail safes and checks to make the data handling process even easier by eliminating the burden of checking for conflicts
_(e.g. checking for existing files when dumping the data to avoid overwriting files/data)._

## How it Works
Before we get into how to use this library, I'm just going to briefly cover what goes on behind the scenes to ensure the usage isn't confusing.
The basic idea of how it processes data is that it splits huge files of data into smaller _**chunks**_, and then returns it as a _**chunk pack**_ containing all the _**chunks**_. for example:   
(pseudocode) `Chunk Pack = {"chunk 1": [{data 1/3}, {data 2/3}, {data 3/3}],"chunk 2": [{data 1/2}, {data 2/2}]}`   
When dumping, the library checks if there are existing chunks with pre-existing data and instead appends the data to the pre-existing chunk. Exception handlers like this make the library even more easy to use, as it does the tedious preparations for you.

## Usage
Now that we have that out of the way, here's how to use it.

Before we start with any of the data handling, I recommend you start with the `log_controller.py` module.
This isn't necessary, but I highly recommend it to get an insight of what's happening with your data.
Use this module to set up a logger so that you can get a log of everything that goes on as your data is being handled.

### Logging
The basic usage is `log_controller.setup_logger(program_filename, log_filename)`   
```python
import log_controller

module_name = __file__.split("/")[-1]  # gets name of the module (filename) from the filepath
logger = log_controller.setup_logger(module_name, 'log_file.log')
```   
The `module_name` step isn't necessary but this is how you automatically get the name of the file you're logging from.

### Loading
After you set up the logger, you usually start with the `loader.py` module. This is used to load CSV or JSON data into your program.   
```python
import loader

# to load in data from a csv file
csv_data = loader.load_from_csv('csv_file.csv')

# to load in data from a json file
json_data = loader.load_from_json('json_file.json')
```

### Dumping
Finally, after messing around with the data you loaded in you usually want to dump it. For that we'll need the `dumper.py` module.   
```python
import dumper

# our data we were just using
data_dump = {'chunk1': [{}, {}]}

dumper.dump_to_json(data_dump)
```   
Optionally we can run `dump_to_json()` with the parameter `folder_name=` set to a folder name. This just puts all files we're dumping to into a folder.   
```python
dumper.dump_to_json(data_dump, folder_name='Data Folder')
```
