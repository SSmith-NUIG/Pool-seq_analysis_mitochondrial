#!/bin/sh 
#SBATCH --job-name="novoseed"
#SBATCH -o /data/ssmith/logs/novseed_%A_%a.out
#SBATCH -e /data/ssmith/logs/novseed_%A_%a.err
#SBATCH -N 1
#SBATCH -n 6
source /home/ssmith/.bashrc
source activate pdetc

Dir=/data2/ssmith/mito_only

rm /data2/ssmith/mito_only/*.txt

python /data/ssmith/scripts/colony_analysis/jan_analysis/mito_analysis/novo_seed_extraction.py
