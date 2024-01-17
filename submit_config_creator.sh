#!/bin/sh 
#SBATCH --job-name="conti_sub"
#SBATCH -o /data/ssmith/logs/cntsub_%A_%a.out
#SBATCH -e /data/ssmith/logs/cntsub_%A_%a.err
#SBATCH --array=207-214
#SBATCH -N 1
#SBATCH -n 6
source /home/ssmith/.bashrc
source activate pdetc

seed_file=/data2/ssmith/mito_only/"$SLURM_ARRAY_TASK_ID"_mito_only.txt

sample_name=$(basename /data2/ssmith/bams/"$SLURM_ARRAY_TASK_ID"_*_indels.bam _indels.bam)

python3 /data/ssmith/scripts/colony_analysis/jan_analysis/mito_analysis/config_file_creator.py -project_name "$sample_name" -reference /dat
a/ssmith/c_l_genome/cmito/chrMT.fna -seed_input "$seed_file" -forward_reads /data2/ssmith/fastqs/"$SLURM_ARRAY_TASK_ID"_*_1.fq.gz -reverse_
reads /data2/ssmith/fastqs/"$SLURM_ARRAY_TASK_ID"_*_2.fq.gz -extend_seed_directly no -output_path /data2/ssmith/novo_output/
