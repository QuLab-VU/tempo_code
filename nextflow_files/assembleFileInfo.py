import os
import csv
import sys
import re
import os.path as op
import pandas as pd
from datetime import datetime

__author__ = "Monica Del Valle"

# Run file preprocessing to check for missing files 
def preprocessing(imgdir):
    dirs = os.listdir(imgdir)

    # Find directory names with 'Plate*' and convert to int
    p1 = re.compile('Plate[0-9]*')
    plates = list(filter(p1.match, dirs))

    nums = []
    for pid in plates:
        plateId = pid.split('Plate')[-s1]
        nums.append(int(plateId))

    # Find missing directories; compare min and max dir id's
    missing = list(set(range(min(nums), max(nums)))-set(nums))
    
    # TODO: finish steps ..
    
def parseMBK(mbkPath):
    # Read first four lines of header info
    with open(mbkPath) as mbkFile:
        head = [next(mbkFile) for x in range(4)]
        cols = head[2][11:-2].split(',')
        df = pd.read_csv(mbkFile, sep='\t', header=None, names=cols)
    
    df2 = df.dropna(axis=1, how='all')

    mbkFile.close()
    return df2
    
LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
           "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def fixWellName(wellLet, wellNum):
    # Convert wellLet to char using LETTERS
    let = list(map(lambda x: LETTERS[x-1], wellLet))
    num = [str(x).zfill(2) for x in wellNum]
    well = [a+b for a, b in zip(let, num)]
    return well
    
def gen_finfo(outfile, imgdir): # , savedir):
    # print("Finding plate directories...")
    dirs = os.listdir(imgdir)

    # Find directory names with 'Plate*' and convert to int
    p1 = re.compile('Plate[0-9*]')
    plates = list(filter(p1.match, dirs))

    # Empty 'plates' means no matches, so raise exception
    if not plates:
        raise Exception("Could not find plate directories in " + imgdir)
    
    expt_class = []
    expt_id = []
    img_time = []
    plate_name = []
    date = []
    plate_id = []
    filename = []
    well = [] 
    channel = []
    z_pos = []
    # print("Assembling plate info...")
    # Find MBK files in each plate directory
    for plate in plates:
        path = op.join(imgdir, plate)
        if 'PlateInfo.MBK' in os.listdir(path):
            df = parseMBK(op.join(path, 'PlateInfo.MBK'))
            if df.empty:
                raise Exception("Error in generating dataframe for " + path + "PlateInfo.MBK")
            # Check for z-stack data 
            if (df['Z_INDEX'].values > 0).any():
                z_pos.extend(df['Z_INDEX'].replace('ZStep_', '').astype(int))
                ZSTACK=True

            for item in df['DIRECTORY']:
                new = item.split('\\')[1:-1]
                # TODO: add check for missing info ***
                expt_class.append(new[0])
                expt_id.append(new[1])
                trimmed = new[2].replace('-Use Current State--', '').split('-')
                img_time.append(datetime.strptime(trimmed[0] + trimmed[1],
                                                  "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S"))
                plate_name.append(trimmed[2] + '-' + trimmed[3])
                date.append(new[3])
                plate_id.append(new[4])

            # Get filename, well, channel from MBK 'OBJ_SERVER_NAME','well','SOURCE_DESCRIPTION'
            filename.extend(df['OBJ_SERVER_NAME'].tolist())
            well.extend(fixWellName(df['WELL_Y'].tolist(), df['WELL_X'].tolist()))
            channel.extend(df['SOURCE_DESCRIPTION'].tolist())
            # TODO: if no image.time use first one for all
        else:
            raise Exception("Missing 'PlateInfo.MBK' file in " + path)
    
    fInfo = pd.DataFrame({'filename': filename,
                          'well': well,
                          'channel': channel,
                          'z_pos': z_pos,
                          'time': img_time,
                          'expt_class': expt_class,
                          'expt_id': expt_id,
                          'plate_name': plate_name,
                          'date': date,
                          'plate_id': plate_id})
    
    fInfo = fInfo.sort_values(by=['plate_id', 'well'], ignore_index=True)
    # print('Completed assembling FileInfo dataframe.')
    
    # fInfo.to_csv(savedir + '/' + outfile, index=False)
    fInfo.to_csv(outfile, index=False)
    
    
outfile = sys.argv[1]
imgdir = sys.argv[2]
# savedir = sys.argv[3]

gen_finfo(outfile, imgdir) #, savedir)

