import csv
import datetime
import os

from common import delimiters
from converter import exchange
from repository.processed_file import Forex_db


class Transaction:
    def __init__(self):
        self.final_data = []
        self.sql_obj = None
        self.sql_obj = Forex_db()
        self.sql_obj.create_tables()

    def process_file(self, folder):
        try:
            file_processed = 0
            if folder:
                csvfile_list = os.listdir(str(folder))
                processed_files = self.check_processedfile(folder)
                print(f"processed_files: {processed_files}")
                for csvfile in csvfile_list:
                    print(f"Provided csvfile :{csvfile}")
                    if csvfile not in processed_files:
                        file_processed += 1
                        filedata = []
                        currDateTime = datetime.datetime.utcnow()
                        filedata.append(csvfile)
                        filedata.append(folder)
                        filedata.append(currDateTime)
                        file_id = self.update_filetable(filedata)
                        self.readfile(file_id, csvfile, folder)
                if file_processed:
                    self.update_transactiontable(self.final_data)
                    return True
                else:
                    print(f'File(s) in {folder} is/are already processed')
                    return False
            else:
                print('Please pass valid folder name as parameter')
                return False


        except Exception as e:
            print('Please pass valid folder name as parameter')
            print(e)
            return False

    def check_processedfile(self, directory):
        """
        This method is to fetch list of processed files of given folder name
        return type: set of processed files
        """
        processed = self.sql_obj.fetch_filedetails(directory)
        return processed

    def readfile(self, file_id, filename, folder):
        # opening the CSV file
        directory = os.getcwd() + '\\' + folder
        file = directory + '\\' + filename
        with open(file, mode='r') as f:
            # reading the CSV file
            delim = delimiters[folder]
            csvFile = csv.reader(f, delimiter=delim)
            headings = next(csvFile)

            # displaying the contents of the CSV file
            for lines in csvFile:
                data = []
                for info in lines:
                    info = info.strip()
                    data.append(info)
                data.append(file_id)
                self.forex_tranc(data)

    def forex_tranc(self, forex_data):
        """
        This method is to get amount in destination currency
        """
        source = forex_data[1].upper()
        destination = forex_data[2].upper()
        sourceamount = forex_data[3]
        dest_curr = exchange[source][destination]
        destination_amount = float(sourceamount) * dest_curr
        forex_data.append(destination_amount)
        forex_data.append(dest_curr)
        currentDateTime = str(datetime.datetime.utcnow())
        forex_data.append(currentDateTime)
        self.final_data.append(forex_data)

    def update_filetable(self, file_data):
        id = self.sql_obj.files_insert(file_data)
        return id

    def update_transactiontable(self, trans_data):
        self.sql_obj.transaction_insert(trans_data)

    def display(self):
        """Preparing response json"""
        response = {}
        count = 1
        for row in self.final_data:
            f_name = self.sql_obj.fetch_filename(row[4])
            key = f_name + '_' + str(count)
            response[key] = {'Source Currency': row[1],
                                 'Destination Currency': row[2],
                                 'Source Amount': row[3],
                                 'Destination Amount': row[5],
                                 'FX Rate': row[6]}
            count += 1
        return response
