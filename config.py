# all of your variables go in this file, which is called by the other scripts

# Your file locations are defined here
local_destination = 'local download folder'  # eg 'C:\data\DI\downloads'
local_archive_destination = 'local archive destination'  # "C:\data\DI\archives\\" + str(week -1) + "\\"
local_db_destination = 'local DI GDB destination'  # "C:\data\DI\GDB\\" + str(week) + "\\"
master_destination = 'local processed GDB destination'  # "C:\data\DI\GDB\master\\"

# Your connection details are defined here
user = 'your username'
password = 'your password'
host = 'ftp address'  # in this case 'fileshare.drillinginfo.com'
rmsite = 'remote target directory'  # in this case '/DI_Weekly_GDB/DI_Weekly_GDB_Full'

protocol = 'ftp'  # 'connection protocol'   eg. ftp, sftp
WinSCPloc = "C:\Program Files (x86)\WinSCP\WinSCP.com"
ProxyMethod = 3
ProxyHost = 'your proxy host'
ProxyPort = 8080

# This is the command used to open WinSCP and use it to connect to the remote server.
# More details can be found here https://winscp.net/eng/docs/scripting
conn = """%s /ini=nul /commamd \"open %s://%s:%s@%s -rawsettings ProxyMethod=%s ProxyHost=""%s"" 
ProxyPort=%s\" \"cd %s\" \"lcd %s\" \"get * \"close\" \"exit\"""" % (WinSCPloc, protocol, user, password, host,
                                                str(ProxyMethod), ProxyHost, str(ProxyPort), rmsite, local_destination)

# print local_destination,local_archive_destination,local_db_destination,master_destination
print"\n\n"
print (conn)
