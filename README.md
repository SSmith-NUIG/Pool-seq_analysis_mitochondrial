# Pool-seq_analysis_mitochondrial  
Pipeline to assemble and annotation honey bee mitochondrial genomes from pool seq data  

## First step  
Run ``submit_config_creator.sh``` to create unique config files for each of our samples  

## Second step
Extract seed sequences for NOVOplasty using ```seed_extraction.py```  
This script extracts a random 150bp seed from the reads that aligned to the reference MT  

## Third step  
Run ```novoplasty.sh``` which uses the NOVOplasty software to assemble the honey bees mitochondrial genome  
The output of this needs heavy manual curation. Each sample could have multiple possible MT assemblies.  
I applied a length criteria of 14kbp and I required it to be continuous, you may modify this if you wish.  

## Fourth step 
We now reorder the assembly and annotate it using MitoZ with the ```mitoz_annotate.sh``` script  


You should now have assembled and annotated genomes. This was not successful for every sample, most actually failed but 100+  
MT genomes were assembled and annotated successfully
