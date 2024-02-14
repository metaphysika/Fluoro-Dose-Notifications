# Fluoroscopy Dose Notification System

## Overview

This Python script automates the monitoring of fluoroscopy dose metrics by querying a local SQLite database for recent exams, identifying those that exceed specified dose limits, and sending automated notifications to a predefined list of recipients. It is designed to support radiology departments in maintaining dose levels within safe limits, facilitating prompt review and response to high-dose incidents.
Features

- Automated extraction of fluoroscopy dose data from a local SQLite database.
- Identification of exams exceeding predefined dose limits for Reference Air Kerma and Fluoroscopy Time.
- Automated email notifications to specified recipients regarding high-dose incidents.
- Archival of notification events for compliance and quality improvement efforts.

## Prerequisites

- Python 3.x
- Access to a local SQLite database with fluoroscopy dose data.
- Python libraries: sqlite3, pandas, openpyxl, py, datetime.
- An email sender module (emailsender.py) properly configured for SMTP email dispatch.
- Microsoft Outlook installed on the system for email dispatch (if using emailsender with Outlook integration).

## Installation

Ensure all the required libraries are installed. You can install any missing libraries using pip:

pip install pandas openpyxl py sqlite3

Note: sqlite3 and datetime are included in the standard Python library.

## Configuration


- Update the fileDb path to the location of your local SQLite database.
- Set is_email to True to enable the sending of email notifications.
- Configure the emailsender module with appropriate SMTP settings or Outlook integration as per your environment.
- Modify the query within the script to match your database schema if different from the provided example.
- Customize the dose limit check in the dose_limit function according to your department's standards.


## Running the Script

Execute the script in your Python environment. The script will:

- Connect to the specified SQLite database.
- Query for fluoroscopy exams based on the configured SQL query.
- Analyze the dose metrics against the predefined limits.
- Send email notifications for any exams exceeding those limits.
- Record details of these notifications for archival purposes.

## How It Works

- The script initializes a connection to the local SQLite database and fetches recent fluoroscopy exams.
- It processes the fetched data, identifying exams with dose metrics exceeding set thresholds.
- For each identified high-dose incident, it compiles relevant details and sends an automated notification email.
- The script records all such notifications in an Excel workbook, providing a persistent record for review and analysis.


## Output

- Email notifications detailing the high-dose incidents are sent to the configured recipients.
- A record of these notifications is saved in an Excel workbook located at the script's specified path.

## Notes


- Ensure the script has read and write permissions for the specified database and Excel workbook paths.
- Verify the email sending functionality adheres to your organization's IT and email policies.
- Regularly review and adjust the dose limits and notification settings to align with evolving clinical practices and safety standards.


## Disclaimer

This script is provided "as is" without warranty of any kind. It is meant to assist in the monitoring of fluoroscopy dose metrics within radiology departments. The responsibility for the appropriate use and configuration of the script lies with the user. Always test the script in a non-production environment before deploying it in a clinical setting.
