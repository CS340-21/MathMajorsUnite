# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
from argparse import ArgumentParser, Action
import os

class Parameters(Action):
    @staticmethod
    def parse_parameters():
        # required = True, then if no arguments then throws error and shows help
        parser = ArgumentParser(description='all things about the files')
        parser.add_argument("--dir", default='./CarData.csv',
                            help="please upload or attach the file or dir")
        return vars(parser.parse_args())


class Read(object):
    def __init__(self):
        self.params = Parameters.parse_parameters()
        return
    
    def read_files(self, dirname, num=0):
        # IF ONLY ONE FILE
        if num == 1:
            files = pd.read_csv(dirname)
            return files
        
        # ELSE ALL FILES
        files = []
        for file in os.listdir(dirname):
            files.append(pd.read_csv(file))
        
        # MERGE
        merge = input("Do you want to merge files?\n")
        if merge == "Yes":
            files = pd.concat(files)
        else:
            pass
        
        return files
    
    def read_pathname(self, pathname):
        # IS DIR
        if os.path.isdir(pathname): 
            data = self.read_files(pathname)
        # IS FILE
        elif os.path.isfile(pathname):
            data = self.read_files(pathname, 1)
        # IS UNRECOGNIZED
        else:
            print("The uploaded data is not a file or folder.")
            raise Exception
        return data
    
    def get_new_columns(self, columns):
        new_columns = {columns[i]: columns[i] for i in range(len(columns))} 
        edit = input("Edit or continue?\n")
        if edit == "Continue":
            return new_columns
        
        for col in new_columns.keys():
            new_name = input("Input new column name or keep name {}.\n".format(col))
            if new_name != None:
                new_columns[col] = new_name
        
        return new_columns
    
    def rename_columns(self, data):
        
        try:
            column_names = self.get_new_columns(data.columns)
            data = data.rename(columns = column_names)

        except:
            for df in data:
                column_names = self.get_new_columns(df.columns)
                df = df.rename(columns = column_names)
        return data
    
    def to_drop(self, columns):
        to_drop = []
        edit = input("Would you like to drop any columns? Yes or No\n")
        if edit == "No":
            return None
        else:
            for col in columns:
                drop = input("Drop {}?\n".format(col))
                if drop == "Yes":
                    to_drop.append(col)
        return to_drop
    
    def drop_columns(self, data):
        try:
            columns_to_drop = self.to_drop(data.columns)
            if columns_to_drop:
                data = data.drop(columns_to_drop, axis=1)
        except:
            for df in data:
                columns_to_drop = self.to_drop(df.columns)
                if columns_to_drop:
                    df = df.drop(columns_to_drop, axis=1)
        return data
    
    def histogram(self, data, name):
        if not name in data.columns:
            return -1
        '''if not data[name].str:
            return 1'''
        try:
            data[name] = data[name].astype(float)
        except:
            return 1

        pic, ax = plt.subplots()
        data.hist(column=name, ax=ax)
        pic.savefig('hist.png')
        exe = 'hist.png'
        return(os.path.abspath(exe))
    
    def main(self):
        pathname = self.params['dir']
        data = self.read_pathname(pathname)
        data.to_csv(self.params['dir'])
        data = self.drop_columns(data)
        data.to_csv(self.params['dir'])
        data = self.rename_columns(data)
        data.to_csv(self.params['dir'])
        print("Congratulations!  You're dataset is ready for learning!\n")
        col_name = input("Would you like a histogram of any of your columns?")
        location = self.histogram(data, col_name)
        print(location)
        return
    
if __name__ == "__main__":
    app = Read()
    app.main()
        
        
        
        
        
        



    
        
        
        
        
