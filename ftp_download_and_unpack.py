# this module uses ftplib to connect to the default port of an ftp server, changes to a target source (remote)
# and destination (local) directory to download the entire contents of the remote directory.  It then loops through the
#  downloaded files and unzips any .zip files to another folder, assigned in the main script.
# For other ftp commands or connection variables, see https://docs.python.org/2/library/ftplib.html
############
import sys
import ftplib
import os
import zipfile
import config
import logging  # to send log messages to main script
log = logging.getLogger(__name__)

# set your user parameters here
ftp = ftplib.FTP(config.host)


def downloadFiles(path, dest):
    ftp.login(config.user, config.password)  # connect to the sever
    log.info("connected to server")
    try:
        ftp.cwd(path)  # change to correct remote folder
        log.info("switched to" + path)
        os.chdir(dest)  # change to correct local folder
    except OSError:     
        pass
    except ftplib.error_perm:       
        log.error("could not change to " + path)
        sys.exit("Ending Application")
    
    filelist = ftp.nlst()  # lists files in remote directory

    for files in filelist:
        try:  # writes the remote file to local destination
            ftp.retrbinary("RETR " + files, open(os.path.join(dest, files), "wb").write)
            log.info("Downloaded: " + files)
        except ftplib.all_errors:
            log.error("File could not be downloaded " + files)
    return


def unzipFiles(source, dest):
    log.info(source)
    # loops through all files and folders in local download folder
    for (dirpath, dirnames, filenames) in os.walk(source):
        log.info(str(dirpath) + str(dirnames) + str(filenames))
        for files in filenames:
            try:
                if files.endswith(".zip"):  # looks only for zip files
                    log.info("Extracting " + os.path.join(source, files))
                    zipped = zipfile.ZipFile(os.path.join(source, files), 'r')
                    zipped.printdir()
                    zipped.extractall(dest)  # extracts the zip files to dest folder
            except Exception as e:
                log.error("couldn't unzip the files")
                log.error(e)
    return


# function called from main script
def download_and_unpack(destination, db_destination):
    downloadFiles(config.rmsite, destination)
    ftp.quit()
    unzipFiles(destination, db_destination)
    return
