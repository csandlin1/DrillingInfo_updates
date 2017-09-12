# DrillingInfo Updates
Python scripts to download and unzip DrillingInfo GDBs and parse by state.  
Co-presented by me and Phil Lampe at Houston Regional PUG on August 10th. The presentation can be viewed 
**[here](https://puginc651-my.sharepoint.com/personal/houston_pugonline_org/_layouts/15/guestaccess.aspx?docid=1b8e1ecc75b9c48c5bb2c740951456089&authkey=AcbqgsbbkPEdrwHIVXfmgTA)**

Usage
=====

In order to make this set of scripts easier to customize for your own use, 
I've moved the file location and server variables into a separate configuration file, config.py.
Depending on your ftp connection, you may use either ftp_download_and_unpack.py or scp-download_and_unpack.py by importing the correct module into DI_update.py.
Information on ftplib can be found **[here](https://docs.python.org/2/library/ftplib.html)**, and you can learn more
 about WinSCP **[here](https://winscp.net/eng/docs/introduction)**. 