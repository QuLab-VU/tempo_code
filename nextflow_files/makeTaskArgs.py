import sys
import os
import csv
import time
import pandas as pd
import numpy as np

__author__ = "Monica Del Valle"

class TaskArgs(object):
    def __init__(self, file_info, img_dir, rp=False, ch1_name='Cy3', 
                 ch2_name=None, save_path=None, owrite=False, verbose=False):

        # Verbose can be used for additional process output
        self.__verbose        = verbose

        if self.__verbose:
            print('*** Task Args *** \n\tInitialization')

        self.__fileInfo       = pd.read_csv(file_info)
        self.__imgDir         = img_dir
        self.__rp             = rp
        self.__ch1Name        = ch1_name
        self.__ch2Name        = ch2_name
        self.__savePath       = save_path
        self.__owrite         = owrite

    def getTaskArgs(self):
        """
        Generate task arguments data frame for image processing.
        
        Parameters
        ----------
        self : TaskArgs object 
            Initialized with user input for task arguments
        
        Returns
        -------
        Pandas dataframe 
            Task args w/ following columns/data saved to csv in save_path
               - channel 2 image path
               - nuclear image path
               - overwrite existing data, if found
               - plate ID
               - regprops T or F python bool
               - path of directory to save file in
               - well name
        """

        if self.__verbose:
            print(" * Running getTaskArgs() * ")

        plateId = self.__fileInfo[self.__fileInfo['channel']==self.__ch1Name]['plate_id'].astype(int)
        plateId = plateId.reset_index(drop=True)
        nucImgFname = self.__fileInfo[self.__fileInfo['channel']==self.__ch1Name]['filename']
        nucImgFname = nucImgFname.reset_index(drop=True)
        well = self.__fileInfo[self.__fileInfo['channel']==self.__ch1Name]['well']
        well = well.reset_index(drop=True)
        nucPath = self.__imgDir + '/Plate' + plateId.astype(str) + '/' + nucImgFname.astype(str)

        if self.__ch2Name != None:
            ch2ImgFname = self.__fileInfo[self.__fileInfo['channel']==self.__ch2Name]['filename']
            ch2ImgFname = ch2ImgFname.reset_index(drop=True)
            ch2Path = self.__imgDir + '/Plate' + plateId.astype(str) + '/' + ch2ImgFname.astype(str)
        else:
            ch2Path = 'None'
        
        taskdf = pd.DataFrame({
            'ch2_im_path':ch2Path,
            'nuc_im_path':nucPath,
            'overwrite':str(self.__owrite),
            'plate_id':plateId.astype(str),
            'regprops':str(self.__rp),
            'save_path':str(self.__savePath),
            'well':well
        })

        if self.__verbose:
            print(" * Returning from getTaskArgs() * ")
            print(self.__savePath)
        return taskdf

    # ACDC get filename function
    def get_unique_filename(self, filename):
        """ 
        Generate a filename which does not exist yet on the filesystem.

        Parameters
        ----------
        self : TaskArgs object 
            Initialized with user input for task arguments
        filename : string
            Filename to add unique suffix to

        Returns
        -------
        None
            Updates self.ta_csv filename
        """
        # sample of using this function:
        # cc_fn = cc_fn.format('') if owrite else self.get_unique_filename(cc_fn)
        
        if '{}' not in filename:
            raise ValueError('Filename must contain {} for numeric plateholder')
        filename_candidate = filename.format('')
        i = 1
        while True:
            try:
                with open(filename_candidate, 'x'):
                    return filename_candidate
            except FileExistsError:
                filename_candidate = filename.format('_{}'.format(i))
            i += 1
    

def makeTaskArgs(fileInfo, img_dir, outfile, rp=False, owrite=False, 
                 ch1_name='Cy3', ch2_name=None, save_path=''):
    """ 
    Wrapper function to create TaskArgs object.
    
    Creates a task argument csv.

    Parameters
    ----------
    fileInfo : csv file 
        File info for each image
    img_dir : str
        Path to image files
    outfile : file or path
        Filename to save task arguments
    rp : bool
        Set 'reg props' to True or False in task args
    owrite : bool
        Set 'overwrite' to True or False in task args
    ch1_name : str
        Name of channel 1
    ch2_name : str
        Name of channel 2
    save_path : str
        Location to save output files
    
    Returns
    -------
    None; Saves task argument csv as /savepath/outfile.csv
    """
    # startTime = time.time()
    task_args = TaskArgs(fileInfo, img_dir, rp, ch1_name, ch2_name, save_path, owrite)
    ta_df = task_args.getTaskArgs()
    # endTime = time.time()
    # print("Execution time: {}".format(endTime - startTime))
    
    ta_df.to_csv(outfile, index=False)

# TODO: make some arguments optional* infer from passed args
finfoFile = open(sys.argv[1], 'r')
imgdir=sys.argv[2]
segDir=sys.argv[3]
outfile = sys.argv[4]
ch2Name = sys.argv[5]
ch1Name=sys.argv[6]
rp = sys.argv[7]
owrite=sys.argv[8]

makeTaskArgs(finfoFile, imgdir, outfile, rp=rp, owrite=owrite,
             ch1_name=ch1Name, ch2_name=ch2Name, save_path=segDir)