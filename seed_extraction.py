#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:17:55 2020

@author: stephen
"""

import pandas as pd
import os

#This is a script for extracting a random 150bp read from
#the reads which aligned to the apis mellifera reference genomes mitochondria
#
#This is required as input for NovoPlasty as a seed read to begin the assembler

def extract_seed_sequence(sam_file):
    #Read the file into pandas giving it column names from 0-19
    df = pd.read_csv(sam_file, sep="\t",header=None,usecols=[9],nrows=10000, error_bad_lines=False)
    #Create a new column which has the length of each read
    df.columns= ['seq']
    df["length"] = df['seq'].apply(lambda x: len(x))
    #Subset the dataframe so that it only includes reads which are 150bp
    df_subset = df[df.length==150]
    #delete the dataframe
    del df
    #Extract a random read from this database 
    #(may need to update to include quality? Possibly not needed as the reads have already passed QC)
    seed_read=df_subset.sample().iloc[0,0]
    print(seed_read)
    return seed_read

dir_path = "/data2/ssmith/mito_only/"

for file in os.listdir(dir_path):
    if file.endswith(".sam"):
        my_file = os.path.join(dir_path, file)
        base = os.path.basename(my_file)
	print(base)
        name = os.path.splitext(base)[0]
        complete_new_file = os.path.join(dir_path,name+".txt")        
        outfile = open(complete_new_file,"w")
        seq= extract_seed_sequence(my_file)
        outfile.write(">"+name+"\n"+seq)
        outfile.close()
