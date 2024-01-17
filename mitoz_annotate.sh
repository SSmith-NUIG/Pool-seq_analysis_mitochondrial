#!/bin/sh 
#SBATCH --job-name="MitoZ"
#SBATCH -o /data/ssmith/logs/MitoZ_%A_%a.out
#SBATCH -e /data/ssmith/logs/MitoZ_%A_%a.err
#SBATCH -N 1
#SBATCH --array=33-206%15
#"$SLURM_ARRAY_TASK_ID"


source /home/ssmith/mitoz3.4/bin/activate
cd /data2/ssmith/novo_output/final_assemblies/
file_1=$(ls /data2/ssmith/fastqs/"$SLURM_ARRAY_TASK_ID"_*_1.fq.gz)
file_2=$(ls /data2/ssmith/fastqs/"$SLURM_ARRAY_TASK_ID"_*_2.fq.gz)
sample_name=$(basename "$file_1" _1.fq.gz)

mkdir /data2/ssmith/novo_output/"$sample_name"
cd /data2/ssmith/novo_output/"$sample_name"


python3 /home/ssmith/Mitogenome_reorder.py \
-f /data2/ssmith/novo_output/final_assemblies/"$SLURM_ARRAY_TASK_ID"_final.fasta \
-r /data/ssmith/c_l_genome/apis_c_l_MT.fa

mitoz findmitoscaf --genetic_code 5 --clade Arthropoda --outprefix "$sample_name" \
--requiring_taxa Arthropoda \
--filter_by_taxa \
--min_abundance 0 \
--fastafile "$SLURM_ARRAY_TASK_ID"_final.fasta.reorder

mitoz annotate \
--genetic_code 5 \
--clade Arthropoda \
--species_name "Apis mellifera" \
--outprefix "$sample_name" \
--fastafile "$sample_name".mitogenome.fa
