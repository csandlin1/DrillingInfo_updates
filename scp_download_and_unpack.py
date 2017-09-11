# script to retrieve files from the server and unzip them into the proper directory

import os
import sys
import zipfile
import subprocess
import logging
import config
log = logging.getLogger(__name__)

connection = config.conn

def downloadFiles(connection):
    log.info("Sending command to winscp")
    try:
        proc = subprocess.Popen(connection)
        proc.wait()
        log.info("connected successfully")
    except Exception as e:
        log.error("Exception: %s" % str(e))
        log.info("exiting program")
        sys.exit(1)
    return


def unzipFiles(source, dest):
    log.info(source)
    for (dirpath, dirnames, filenames) in os.walk(source):
        log.info(str(dirpath) + str(dirnames) + str(filenames))
        for files in filenames:
            try:
                if files.endswith(".zip"):
                    log.info("Extracting " + os.path.join(source, files))
                    zipped = zipfile.ZipFile(os.path.join(source, files), 'r')
                    zipped.printdir()
                    zipped.extractall(dest)
            except Exception as e:
                log.error("couldn't unzip the files")
                log.error("Exception: %s" % str(e))
    return


# function called from main script
def download_and_unpack(destination, db_destination):
    downloadFiles(connection)
    unzipFiles(destination, db_destination)
    return
