import sys
import os
import re
import pandas as pd

__author__ = "Monica Del Valle"

def assemblePlate(seg_dir, outfile, count_name='cellcount', pid_list='', to_file=False):
    """
    Python version of cell count assembly
    
    Parameters
    ----------
    seg_dir : str or path-like object
        Path to Segmentation directory containing cellcount.csv's
    outfile : str
        Output file
    count_name : str
        Naming convention of the cell count data files to assemble; default 'cellcount'
    pid_list : list 
        Specific plate ids to get cellcounts for; default collects all plate id's in seg_dir
    to_file : bool
        If true, save intermediate output of cellcounts for each plate
    
    Returns
    -------
    None; Saves dataframe of the assembled cell counts to /seg_dir/outfile.csv
    """
    
    # Verify the passed pid_list, if any
    if pid_list != '': 
        # Add base path to plate id's
        plateIds = list(map(lambda x: seg_dir + '/Plate' + str(x), pid_list))
        
        # Get all the plate id's in the seg_dir
        allIds = os.listdir(seg_dir)
        # allIds = list(map(lambda x: seg_dir + x, os.listdir(os.getcwd())))

        # Compare the lists to determine missing pid's, if any
        s = set(allIds)
        dif = [x for x in plateIds if x not in s ]
        if len(dif) != 0:
            raise Exception("Not all plate ids passed as <pids> found in" + seg_dir)
    else:
        plateIds = os.listdir(seg_dir) 
    
    # Parse plateID dirs for the cellcount.csv's and append to output dataframe
    data2 = []
    for pid in plateIds:
        if pid == '.DS_Store':
            continue
        files = os.listdir(seg_dir + '/' + pid)
        p1 = re.compile('.*cellcount.csv')
        plate = pid.split('/')[-1]
        cc = list(filter(p1.match, files))

        data = []
        for x in cc:
            df = pd.read_csv(seg_dir + '/' + pid + '/' + x, index_col=None, header=0)
            data.append(df)
        
        pc = pd.concat(data, axis=0, ignore_index=True)
    
        # Save file 
        if(to_file):
            pc.to_csv(f'{seg_dir}/{plate}/{plate}_cellcounts.csv')
        
        data2.append(pc)

    out = pd.concat(data2, axis=0, ignore_index=True)
    
    # Save final cc file
    out.to_csv(outfile, index=False)

# Read command line arguments
segDir = sys.argv[1]
outfile = sys.argv[2]

assemblePlate(segDir, outfile)

