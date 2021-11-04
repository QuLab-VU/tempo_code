#!/usr/bin/env nextflow

process get_fileInfo {
    publishDir params.rootDir
    
    output:
    file "${params.expt}ImageFileInfo_${params.exptDate}.csv" into finfo_ch

    script:
    """
    python3 $params.fiScript ${params.expt}ImageFileInfo_${params.exptDate}.csv \
        $params.imgdir
    """
}


process get_taskArgs {
    publishDir params.rootDir
    
    input:
    file finfo from finfo_ch
    
    output:
    file "MXTaskArgs_${params.expt}_${params.exptDate}.csv" into taskargs_ch
    
    script:
    """
    python3 $params.taScript $finfo $params.imgdir $params.segDir \
        MXTaskArgs_${params.expt}_${params.exptDate}.csv $params.ch2Name \
        $params.ch1Name $params.rp $params.owrite
    """
}

process improc {
    conda params.condaEnv
    
    input:
    file taskargs from taskargs_ch
    
    output:
    val true into done_ch
    
    script:
    """
    cd $params.repo
    celery -A MXtasksTempo worker --concurrency=120 --detach
    python3 sendMXtempoJobs.py $params.rootDir/$taskargs
    """
}

process get_cellcounts {
    publishDir params.rootDir
    
    input:
    val flag from done_ch
    
    output:
    file "cellCounts_${params.expt}_${params.exptDate}.csv" into cc_ch
    
    script:
    """
    python3 $params.ccScript $params.segDir cellCounts_${params.expt}_${params.exptDate}.csv
    """
}

