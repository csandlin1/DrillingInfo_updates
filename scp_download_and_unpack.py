# script to retrieve files from the server and unzip them into the proper directory

import os
import zipfile
import subprocess
import config
import logging
log = logging.getLogger(__name__)

user = config.user
password = config.password
host = config.host
conn = config.conn
local_destination = config.local_destination
local_db_destination = config.local_db_destination


def downloadFiles(connection):
    proc = subprocess.Popen(connection)
    proc.wait()
    log.info("Downloaded Files")
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
                log.error(e)
    return


def download_and_unpack(destination, db_destination):
    downloadFiles(conn)
    unzipFiles(destination, db_destination)
    return
