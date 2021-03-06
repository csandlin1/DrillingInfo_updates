# Script to download Drilling Info full updates, loop through the three files,
# parse all the features classes by state and add them to a
# single new file geodatabase for that state

import os
import shutil
import errno
import ftp_download_and_unpack as download  # or scp_download_and_unpack if needed
import update_master as update
import config
import logging

# make a directory for the logfiles
try:
    os.makedirs(os.path.join(os.getcwd(), "logs"))
    print("Making logging directory")
except OSError as e:
    print("logs directory exists")
    if e.errno != errno.EEXIST:
        raise


# set up logging(scheme adapted from  Stack Overflow post
# https://stackoverflow.com/questions/9321741/printing-to-screen-and-writing-to-a-file-at-the-same-time)
output_log = config.output_log
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
connection = config.conn

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
    except Exception as er:
        logging.error(files + " could not be moved")
        logging.error("Exception: %s" % str(er))


# run script to connect to ftp site, retrieve updates and unzip to correct folder
check_dir_exists(local_db_destination)
download.download_and_unpack(local_destination, local_db_destination)
logging.info("DI files unpacked")

# run script to process incoming databases and update master files
update.updatenow(local_db_destination, master_destination)
logging.info("Finished processing databases")
logging.getLogger("").handlers[0].close()
