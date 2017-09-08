# Script to download Drilling Info full updates, loop through the three files,
# parse all the features classes by state and add them to a
# single new file geodatabase for that state

import os
import shutil
import errno
import ftp_download as download  # or scp_download if needed
import update_master as update
import config
import datetime
import logging

# this number is used to determine the folder in which the files will be placed
week = datetime.datetime.now().isocalendar()[1]

# set up logging file (logging scheme adapted from  Stack Overflow post
#  https://stackoverflow.com/questions/9321741/printing-to-screen-and-writing-to-a-file-at-the-same-time)
output_log = "logfile_" + datetime.datetime.now().strftime("%m-%d-%y") + ".txt"
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
                    datefmt="%m-%d %H:%M",
                    filename=output_log,
                    filemode="w")

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger("").addHandler(console)

# file locations are defined in config file
local_destination = config.local_destination
local_archive_destination = config.local_archive_destination
local_db_destination = config.local_db_destination
master_destination = config.master_destination


def check_dir_exists(path):
    try:
        os.makedirs(path)
        logging.info("making directory " + str(path))
    except OSError as e:
        logging.info(" directory exists " + str(path))
        if e.errno != errno.EEXIST:
            raise
    return

# move previous downloads for archive
check_dir_exists(local_archive_destination)
for files in os.listdir(local_destination):
    try:  
        shutil.move(os.path.join(local_destination, files), local_archive_destination)
        logging.info("Moving " + files)
    except:
        logging.error(files + " could not be moved")


# run script to connect to ftp site, retrieve updates and unzip to correct folder
check_dir_exists(local_db_destination)
download.download_and_unpack(local_destination, local_db_destination)
logging.info("Finished with download and unpack")

# run script to process incoming databases and update master files
update.updatenow(local_db_destination, master_destination)
logging.info("Finished processing databases")
logging.getLogger("").handlers[0].close()
