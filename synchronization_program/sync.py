# program to sync a source folder with a replica folder 
# should maintain an identical copy of source
# one way sync, periodically 
# file creation/deletion included in a logger and console 

from pathlib import Path
import logging 
import shutil
import os
import time
from datetime import datetime

# setting the paths
ROOT = Path(__file__).parent
SOURCE_PATH = ROOT / "source_folder"
REPLICA_PATH = ROOT / "replica_folder"

# setting a logger
logging.basicConfig(filename=f"{ROOT}/log.log", level=logging.DEBUG,
                     format="%(asctime)s [%(levelname)s] %(message)s")

def delete(msg):
    """Prints a message on the console. Works parallel with the logger."""
    print(f"[INFO] {msg} deleted.")

def show(msg):
    """Prints a message on the console. Works parallel with the logger."""
    print(f"[INFO] {msg}")

def logging_source(source):
    """Logs the location where the program is running."""
    logging.info(f"Working in {source}.")

# logs each folder that has been copied and created
def copy2_verbose(src, repl):
    for path in os.listdir(src):
        if path not in os.listdir(repl):
            logging.info(f"{path} was created and copied to replica.")
            show(f"{path} was created and copied.")

# copies the content of the source folder to the replica folder
def copy_source_to_replica(source, replica):
    """Copies the content of source to replica."""
    try:
        shutil.copytree(source, replica, dirs_exist_ok=True, ignore=copy2_verbose(source, replica))
    except ValueError as err:
        print(err)

# checks both dirs and deletes what is not a match. logs the details and 
# prints on the console as well
def check_file_integrity(source, replica):
    """Checks if both files have the same content."""
    source_list = os.listdir(source)
    replica_list = os.listdir(replica)
    matches = list(set(source_list).intersection(replica_list))
    for i in replica_list:
        if i not in matches:
            try:
                os.rmdir(f"{replica / i}")
                logging.info(f"{i} was deleted because it doesn't exist anymore in main dir.")
                delete(f"{i}")  
            except NotADirectoryError:
                os.remove(f"{replica / i}")
                logging.info(f"{i} was deleted because it doesn't exist anymore in main dir.")
                delete(f"{i}")  

# runs the program in an infinite loop
def running_program(source, replica):
    logging_source(source)
    while True:
        time.sleep(2)
        copy_source_to_replica(source, replica)
        print("Content synced.")
        time.sleep(0.1)
        check_file_integrity(source, replica)
        print("Integrity checked.")

running_program(SOURCE_PATH, REPLICA_PATH)