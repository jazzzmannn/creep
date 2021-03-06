"""
 Title: Excel I/O
 Description: For reading and writing to .xlsx files
 Author: Janzen Choi

"""

# Libraries
import os
import pandas as pd

# Constants
DEFAULT_PATH    = './'
DEFAULT_FILE    = 'excel'
DEFAULT_SHEET   = 'info'

# Class for reading and writing to .xlsx files
class Excel:

    # Constructor
    def __init__(self, path = DEFAULT_PATH, file = DEFAULT_FILE, sheet = DEFAULT_SHEET):
        self.path   = path
        self.file   = file
        self.sheet  = sheet

    # Sets the default values if empty
    def set_default(self, path, file, sheet):
        path = self.path if path == '' else path        
        file = self.file if file == '' else file
        sheet = self.sheet if sheet == '' else sheet
        return path, file, sheet

    # Reads a column of data and returns it in the form of a list
    def read_column(self, column, path = '', file = '', sheet = ''):
        path, file, sheet = self.set_default(path, file, sheet)
        data = pd.read_excel(io = path + file + '.xlsx', sheet_name = sheet, usecols = [column])
        data = data.dropna()
        data = data.values.tolist()
        data = [d[0] for d in data]
        return data

    # Reads multuple columns of data
    def read_columns(self, columns, path = '', file = '', sheet = ''):
        path, file, sheet = self.set_default(path, file, sheet)
        data = [self.read_column(column = column) for column in columns]
        data = [[column[i] for column in data] for i in range(0, len(data[0]))]
        return data

    # Gets a list of data only for the included tests
    def read_included(self, column, test_names):
        info_list = self.read_column(column = column, sheet = 'info')
        test_list = self.read_column(column = 'test', sheet = 'info')
        info_list = [info_list[i] for i in range(0,len(test_list)) if test_list[i] in test_names]
        return info_list

    # Writes to an excel (appends a number if the filename already exists)
    def write_data(self, data, columns, path = '', file = '', sheet = '', max_files = 100, override = False):
        path, file, sheet = self.set_default(path, file, sheet)
        df = pd.DataFrame(data, columns = columns)
        target_file = path + file + '.xlsx'
        if override:
            df.to_excel(target_file, sheet_name = sheet)
        else:
            for file_num in range(1, max_files):
                try:
                    if os.path.isfile(target_file):
                        target_file = path + file + ' (' + str(file_num) + ').xlsx'
                    df.to_excel(target_file, sheet_name = sheet)
                    break
                except:
                    continue
    
    # Appends to an existing excel
    def append_data(self, data, columns, path = '', file = '', sheet = ''):
        path, file, sheet = self.set_default(path, file, sheet)

        # Read old data
        if os.path.isfile(path + file + '.xlsx'):
            old_data = [self.read_column(column, path, file, sheet) for column in columns]
            old_data = [[column[i] for column in old_data] for i in range(len(old_data[0]))]
            data = old_data + data

        # Append new data to old data and write
        df = pd.DataFrame(data, columns = columns)
        df.to_excel(path + file + '.xlsx', sheet_name = sheet)

# Prepends a column to a 2D list (assumes same number of rows)
def prepend_column(list_2D, column):
    list_2D = [[column[i] + list_2D[i]] for i in range(0, len(list_2D))]
    return list_2D

# Appends a column to a 2D list (assumes same number of rows)
def append_column(list_2D, column):
    list_2D = [list_2D[i] + [column[i]] for i in range(0, len(list_2D))]
    return list_2D