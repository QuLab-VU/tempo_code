# HTS Nextflow Pipeline

## Configuration
### Environment Setup 
Set up the image processing environment using conda
```
conda create -n improc python=3.7.1 opencv=4.1.1 mahotas celery scikit-image pandas

conda activate improc
```
### Segmentation Code Repository
The `MXtasksTempo.py` and `sendMXtempoJobs.py` scripts required to run the image processing is in the following Github repository: https://github.com/QuLab-VU/Segmentation-other.git
Clone or download the repository to provide the location of this script in the configuration file.

### `nextflow.config` File
The configuration file contains variables used by each process in the pipeline. Variables include the locations of input data, processing scripts, and the conda environment. Some variables are specific parameters needed to run certain processes in the pipeline. See the configuration file for more details.

See Nextflow [documentation](https://www.nextflow.io/docs/latest/index.html#) for more configuration options.

## Processess
### get_fileInfo
The first process generates a 'file info' csv file containing information about the images being processed. The output contains the following fields:

 - File name
 - Well
 - Channel
 - Z position
 - Time
 - Experiment name/ID
 - Plate name
 - Date
 - Plate ID

### get_taskArgs
This process uses the fileInfo.csv as input to generate arguments needed to run the image processing. The output is a csv file with the following fields:

 - Image locations (ch1 = nuclear image path for HTS data)
 - Overwrite existing output files (True or False)
 - Plate ID
 - Regional properties (True or False) 
 - Path to save segmentation output
 - Well
### improc
This process handles the image processing. The task arguments are used as input to the Celery workers running the image processing jobs. The outputs of this process are the segmented image masks and the cell counts of each image in individual csv files.
### get_cellcounts
The final process compiles all of the computed cell counts into one csv file. 

## Usage
1. Make sure nexflow is installed (https://www.nextflow.io)
2. Modify `nextflow.config` file with appropriate parameters (see **Configuration** above)
3. Run the pipeline
```
nextflow run hts_pipeline.nf
```

**Note:** Using the `-resume` option will run the pipeline from where an existing execution left off.
```
nextflow run hts_pipeline.nf -resume
```
