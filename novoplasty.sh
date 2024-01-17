#!/bin/sh 
#SBATCH --job-name="novo"
#SBATCH -o /data/ssmith/logs/novo_%A_%a.out
#SBATCH -e /data/ssmith/logs/novo_%A_%a.err
#SBATCH -c 16
#SBATCH -p highmem
#SBATCH --mem 126000M
#SBATCH --array=207-214%1
#"$SLURM_ARRAY_TASK_ID"
source /home/ssmith/.bashrc
source activate novo_env

sample_name=$(basename /data2/ssmith/fastqs/"$SLURM_ARRAY_TASK_ID"_*_1.fq.gz _1.fq.gz)

NOVOPlasty.pl -c /data2/ssmith/novo_config_files/"$sample_name"_config.txt
