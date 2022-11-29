"""
Merge all the csv files in the given folder into one CSV
"""
import os
import pandas as pd
from sales_records import *


class MergeCsv:
    """
    Class to csv files present in sales_records directory
    """
    def __init__(self):
        """ constructor of the class """
        self.folder = 'sales_records'
        self.csvfile_list = os.listdir(self.folder)
        self.directory = os.getcwd()+'\\'+self.folder
        self.chunk_size = 1000000
        self.output = self.directory+'\\problem2_output.csv'

    def merge_csv(self):
        """
        method to merge five csv files
        from sales_records directory
        """
        first_file = True
        count = 0
        try:
            for csvfile in self.csvfile_list:
                count += 1
                csvfile = self.directory+'\\'+csvfile
                if count > 5:
                    break
                skip_row = [0]
                if first_file:
                    skip_row = []
                    first_file = False
                chunk_container = pd.read_csv(csvfile, chunksize=self.chunk_size, skiprows=skip_row)
                for chunk in chunk_container:
                    chunk.to_csv(self.output, mode='a', index=False)
            print('Merged five CSV files into one CSV file named problem2_output.csv')
        except Exception as exc:
            print('Unable to merge csv files due to below exception \n')
            print(exc)


"""main function"""
if __name__ == "__main__":
    """create object of JsonToCSV class"""
    obj = MergeCsv()
    """calling function to merge files"""
    obj.merge_csv()

