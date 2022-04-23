import pandas as pd
import os

class BlessCSV:

    ''''this is a little program I wrote to update column name in excel file in a directory
    When I am ready to make this program public, I will add the ncessary error checking.
    '''

    # open each file in the directory
    # food original data path
    orig_data_dir = 'C:/Users\Ed-Ryzen-Desktop/OneDrive - The University of Montana\Data Analytics/Famine Impact/Original Data/Food Production'
    modified_output_dir = 'C:/Users\Ed-Ryzen-Desktop/OneDrive - The University of Montana\Data Analytics/Famine Impact/Modified Data/Food Production Updated Col Names/'
    df_list = {}

# try/exception for non existing directories and make directories if that is the case
    def __init__(self, input_director, output_directory):
        self.orig_data_dir = input_director
        self.modified_output_dir = output_directory
        print("hereeeeeeeeeeeee")
        self.df_list = self.prepared_df_list()

    # might use func later to change paths from default one
    # if the element contains character that will be escape char, replace it
# try/except for non existen directories and make directories if needed

    def set_input_dir_path(self, dir):
        if ('\\' in dir):
            orig_data_dir = dir.replace('\\', '/')
        else:
            orig_data_dir = dir
        return orig_data_dir

    # try/except for non existen directories and make directories if needed
    def set_output_dir_path(self, dir):
        if ('\\' in dir):
            modified_output_dir = dir.replace('\\', '/')
        else:
            modified_output_dir = dir
        return self.orig_data_dir

    # returns a list of all files in a directory
    # filter the files so that only .bin are returned
    def files_in_dir(self):
        return os.listdir(self.orig_data_dir)

    ''' 
    By default, the col will be renamed with a string that is the name of the file + "(in tons)
    To name the col something else, pass in file name, and the string one desires to see for Col Number
    '''
    ## try except for non.csv file or operation not opening
    # !!!! Suggested improvement: give user other ways to name the col and error check
    def col_name(self, filename, default_naming=True, name_string = ''):
        #print(type(filename))
        if (default_naming):
            col_name_prep = filename.split('.')
            col_name = col_name_prep[0].replace('-', ' ').title() + " (in tons)"
        else:
            col_name = name_string
        return col_name
    def file_name(self, filename, default_naming=True, name_string = ''):
        if (default_naming):
            file_name_prep = filename.split('.')
            file_name = file_name_prep[0].replace('-', ' ').title() + " (in tons)"+'.csv'
        else:
            filename = name_string
        return file_name

    def open_file(self, file_name):
        file_path = self.orig_data_dir + '/' + file_name
        file_df = pd.read_csv(file_path)
        return file_df
    '''This function stores a list of pointers to all the open files. This is done for DRY coding principles and 
    so a file needs to only be opened once, even though multiple changes are done to it.
    For example, if a file needs to have col name changed but also, other things performed on it, all the pointers to opened files are stored
    in an array for each successive function, rather than reopening the files.
    Possible improvement: set a streamed buffer
    '''
    def prepared_df_list(self):
        files = self.files_in_dir()
        for file in files:
            file_df = self.open_file(file)
            self.df_list[file] = file_df
            #print(self.df_list)
        return self.df_list
    '''
    This function opens each file in the input_directory (input_dir arguement), changes the col name, saves
    the file to the output_dir
    '''
    # rename df col and save as a file in a specified directory
    # suggested improvement: function that allows other naming ways so we are not statically tied to "entitiy, entitiy_code, etc)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!! fix it to be in compliance with DRY with prepared_df_list
    def change_col_name(self, col_number = 3):
        #print("got here succesffully")
        for entry in self.df_list.items():
            file_name = entry[0]
            file_df = entry[1]
            file_df.columns = ['Entity', 'Entity_Code', 'Year', self.col_name(file_name)]
            file_name = self.modified_output_dir + file_name
            file_df.to_csv(file_name, index=False)
            print("Updating and saving file" + file_name)

    #df0 = df_list[0]
    #df0= df0.join(df_list[1], on = ('Entity', 'Year'))
    #print(df0)
    # Suggested improvements!! can make the first file to be selectable
    def inner_join_files_in_dir(self, joined_name = 'joined_file', join_on = ('Entity', 'Year')):
        print(self.df_list)
        df0 = self.df_list[0]
        for df in self.df_list[1:]:
            df0 = df0.join(df, on = join_on)
        return df0


    def print_hi(name):
        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

        ## Other improvements: make sure join all files on something
        ## after done with something return an open df
        ##


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    orig_data_dir = 'C:/Users\Ed-Ryzen-Desktop/OneDrive - The University of Montana\Data Analytics/Famine Impact/Original Data/Food Production'
    modified_output_dir = 'C:/Users\Ed-Ryzen-Desktop/OneDrive - The University of Montana\Data Analytics/Famine Impact/Modified Data/Food Production Updated Col Names/'
    test1 = BlessCSV(orig_data_dir, modified_output_dir)
    test1.change_col_name(3)
#change_col_name(orig_data_dir, modified_output_dir, '../Modified Data/Food Production Updated Col Names/')
    test2 = BlessCSV(orig_data_dir, modified_output_dir)

   #print(test2.inner_join_files_in_dir())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
