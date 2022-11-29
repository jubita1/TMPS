"""
Script to validate column of two json files.
concatenate one to another and convert to a CSV file.
"""
import pandas as pd


class JsonToCSV:
    """
    Class to accept two json filenames as argument
    and create required csv file
    """
    def __init__(self, file1, file2):
        """ constructor of the class """
        self.file1 = file1
        self.file2 = file2

    def validate_columns(self):
        """method to compare columns of two json files"""
        resp = 0
        try:
            df1 = pd.read_json("File1.json")
            df2 = pd.read_json("File2.json")
            headers1 = [column1 for column1 in df1]
            headers2 = [column2 for column2 in df2]

            if headers2 == headers1:
                final_data = pd.concat([df1, df2], axis=0)
                resp = self.create_csv(final_data)
        except Exception as e:
            print(e)
        return resp

    def create_csv(self, final_data):
        """method to create csv file from dataframe
        if file exists, append data in the same file
        """
        try:
            final_data.to_csv('output.csv', header=True, index=False)
            return 1
        except Exception as ex:
            print(ex)
            return 0


"""main function"""
if __name__ == "__main__":
    """create object of JsonToCSV class"""
    file1 = 'File1.json'
    file2 = 'File2.json'
    obj = JsonToCSV(file1, file2)
    result = obj.validate_columns()
    if result:
        print('CSV file is created')
    else:
        print('CSV file is not created')
