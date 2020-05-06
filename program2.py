import sys
import os
import glob
import ftplib
from ftplib import FTP
import xlrd
import MySQLdb
ftp = FTP("remote server ip")
ftp.login("ftp_user", "ftp_password")


def downloadFiles(path, destination):
    try:
        ftp.cwd(path)
        os.chdir(destination)
        os.mkdir(destination[0:len(destination)-1]+path)
        print destination[0:len(destination)-1]+path+" built"
    except OSError:
        pass
    except ftplib.error_perm:
        print "error: could not change to "+path
        sys.exit("ending session")
    filelist = ftp.nlst() # list out the files from ftp server path
    for file in filelist:
        try:
            ftp.cwd(path+file+"/")
            downloadFiles(path+file+"/", destination)
        except ftplib.error_perm:
            os.chdir(destination[0:len(destination)-1]+path)
            ftp.retrbinary("RETR " +file, open(os.path.join(destination,file), "wb").write)
            print (file + " downloaded")
    return

source="/ftp/gowthami/files"
dest= "C:\Users\gowthami.kandru/"
downloadFiles(source,dest)


# Inserting the data into the mysql call_info table based on the data which we got from files stored on ftp server
for csv_file in [file_name for file_name in glob.glob("{}/*.csv".format(dest))]:
    book = xlrd.open_workbook(csv_file)
    sheet = book.sheet_by_name("source")

    database = MySQLdb.connect(host="localhost", user="root", passwd="mysql_password", db="mysql_db")
    cursor = database.cursor()
    query = """INSERT INTO call_info (ResultTime, GranularityPeriod, ObjectName,  CellID, CallAttemps) VALUES (%s, %s, %s, %s, %s)"""

    for r in range(1, sheet.nrows):
        result_time = sheet.cell(r,0).value
        granularity_period	= sheet.cell(r,1).value
        object_name	= sheet.cell(r,2).value
        cell_id	= sheet.cell(r,3).value
        call_attemps = sheet.cell(r,4).value
        values = (result_time, granularity_period, object_name, cell_id, call_attemps)
        cursor.execute(query, values)
    cursor.close()
    database.commit()
    database.close()

