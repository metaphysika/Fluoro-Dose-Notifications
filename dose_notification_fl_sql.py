import sqlite3
import pandas as pd
import openpyxl
import py
from emailsender import *
from datetime import datetime
import atexit
from time import time, strftime, localtime
from datetime import timedelta
import datetime

# This will help display run time for script
def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

# calls run time functions for script
start = time()
atexit.register(endlog)
log("Start Program")



# set to True to send emails.  False to not send emails.
is_email = True

# path for local database
fileDb = py.path.local(path goes here])


# make a copy of databse file on my computer.
# This script will then perform operations on that file.
if fileDb.isfile():
    fileDb.remove()
py.path.local([path goes here]).copy(fileDb)

# Checks if outlook is open.  If not, opens it.
EmailSender().check_outlook()

# Connect to the database. Need .strpath to work.
db = sqlite3.connect(fileDb.strpath)

# selects data from database.  LIMIT will  limit results to specified number.
queries = ("""SELECT remapp_generalstudymoduleattr.study_description as study,
              remapp_accumprojxraydose.dose_rp_total as ref_air_kerma,
              remapp_accumprojxraydose.total_acquisition_time as fluoro_time,
              remapp_generalstudymoduleattr.study_date,
              remapp_generalstudymoduleattr.accession_number as acc,
              remapp_generalequipmentmoduleattr.institution_name as site,
              remapp_generalequipmentmoduleattr.station_name as station,
              remapp_generalstudymoduleattr.study_instance_uid as uid
              FROM remapp_accumprojxraydose, remapp_accumxraydose, remapp_projectionxrayradiationdose,
              remapp_generalstudymoduleattr, remapp_generalequipmentmoduleattr
              WHERE remapp_accumprojxraydose.accumulated_xray_dose_id = remapp_accumxraydose.id
              AND remapp_accumxraydose.projection_xray_radiation_dose_id = remapp_projectionxrayradiationdose.id
              AND remapp_projectionxrayradiationdose.general_study_module_attributes_id = remapp_generalstudymoduleattr.id
              AND remapp_projectionxrayradiationdose.general_study_module_attributes_id = remapp_generalequipmentmoduleattr.id
              """)


df = pd.read_sql_query(queries, db)
df['study'] = df['study'].astype(str)
# print(df.head(10))

# # looks for air kerma values above a set threshold of 5 Gy.
# # appends outlier data to a file and emails the physics email with study data.
def dose_limit():
    for idx, row in df.iterrows():
        if row.at['ref_air_kerma'] >= 5:
            # list for adding data to spreadsheet for tracking notifications.
            nt = []
            # TODO: change to physics@sanfordhealth.org
            emailname = [emails go here]
            study = str(row.at["study"])
            nt.append(study)
            ak = str(row.at["ref_air_kerma"])
            nt.append(ak)
            fltime = str(row.at["fluoro_time"])
            nt.append(fltime)
            studydate = str(row.at["study_date"])
            nt.append(studydate)
            acc = str(row.at["acc"])
            nt.append(acc)
            site = str(row.at["site"])
            nt.append(site)
            station = str(row.at["station"])
            nt.append(station)
            uid = str(row.at["uid"])
            nt.append(uid)
            # write the notifications to a file.
            # TODO move file to a permanent place
            wb = openpyxl.load_workbook([path goes here])
            sheet = wb['Sheet1']
            # check if UID is already in file.  If so, pass.  If not, append and send notification.
            olduid = []
            for col in sheet['H']:
                olduid.append(col.value)
            if uid in olduid:
                pass
            else:
                sheet.append(nt)
                wb.save(path goes here])
                wb.close()
                # calls the module that sends the email with these variables data.
                # if is_email is true, the email will get sent.  If false, it will not send email.
                if is_email:
                    EmailSender().send_email(emailname, "Fluoro Dose Notification Trigger",
                                             "Hello, \r\n \r\nThis is an automated message.  No reply is necessary."
                                             "  \r\n \r\nAn exam was performed that exceeded our dose Notification limits.  \r\n \r\nExam: "
                                             +study + "\r\n \r\nAccession #: " + acc + "\r\n \r\nRef Air Kerma (Gy): " + ak +
                                             "\r\n \r\nFluoro Time (min): " + fltime + "\r\n \r\nStudy Date: " +
                                             studydate + "\r\n \r\nSite: " + site + "\r\n \r\nStation name: " + station)
                else:
                    pass
                wb.close()
                continue



# Global setting for fluoro of 5 Gy
dose_limit()
db.close()
