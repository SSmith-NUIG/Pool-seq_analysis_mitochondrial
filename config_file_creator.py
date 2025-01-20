#Creating contig files for multiple NOVOplasty runs

import os
import argparse
import textwrap

parser = argparse.ArgumentParser(description='Create config files for NOVOplasty.')
parser.add_argument('-project_name', metavar='-N', nargs='+', default="test",
                    help= textwrap.dedent('''\
                                          Choose a name for your project, it will be used for the output files'''))
parser.add_argument('-type', metavar='-T', nargs='+', default="mito",
                    help=textwrap.dedent('''
                                         (chloro/mito/mito_plant) "chloro" for chloroplast assembly,'
                                         "mito" for mitochondrial assembly and'
                                         "mito_plant" for mitochondrial assembly in plants.'''))

parser.add_argument('-genome_range', metavar='-GR', nargs='+', default='12000-17000', 
                    help=textwrap.dedent('''\
                                         (minimum genome size-maximum genome size) The expected genome size range of the genome.
                                         Default value for mito: 12000-20000 Default value for chloro: 120000-200000
                                         If the expected size is know, you can lower the range, this can be useful when there is a repetiti
ve region,
                                         what could lead to a premature circularization of the genome.'''))

parser.add_argument('-k_mer', metavar='-K', nargs='+',type=int, default=66,
                    help=textwrap.dedent('''\
                                         (integer) This is the length of the overlap between matching reads (Default: 33) 
                                         If reads are shorter then 90 bp or you have low coverage data,
                                         For reads longer then 101 bp, this value can be increased, but this is not necessary.'''))

parser.add_argument('-max_memory', metavar='-MxM', nargs='+', default="",
                    help=textwrap.dedent('''\
                                         You can choose a max memory usage, suitable to automatically subsample the data or when you have l
imited                      
                                         memory capacity. If you have sufficient memory, leave it blank, else write your available memory i
n GB
                                         if you have for example a 8 GB RAM laptop, put down 7 or 7.5 don\'t add the unit in the config fil
e'''))

parser.add_argument('-extended_log', metavar='-ExtLog', nargs='+', default="0",
                    help=textwrap.dedent('''\
                                         Prints out a very extensive log, could be useful to send me when there is a problem  (0/1).'''))

parser.add_argument('-save_assembled_reads', metavar='SaveReads', nargs='+', default="no",
                    help=textwrap.dedent('''
                                         'All the reads used for the assembly will be stored in seperate files (yes/no)'''))

parser.add_argument('-seed_input', metavar='-S', nargs='+',
                    help=textwrap.dedent('''\
                                         The path to the file that contains the seed sequence.\nMust be in Fasta format'''))

parser.add_argument('-extend_seed_directly', metavar='-ExtSeed', nargs='+', default="no",
                    help=textwrap.dedent('''\
                                         This gives the option to extend the seed directly, instead of finding matching reads.
                                         Only use this when your seed originates from the same sample and there are no possible mismatches 
(yes/no)'''))

parser.add_argument('-reference', metavar='-Ref', nargs='+',
                    help=textwrap.dedent('''\
                                         If a reference is available, you can give here the path to the fasta file.
                                         The assembly will still be de novo, but references of the same genus can be used as a guide to res
olve
                                         duplicated regions in the plant mitochondria or the inverted repeat in the chloroplast.
                                         References from different genus haven\'t beeen tested yet.'''))
parser.add_argument('-variance_detection', metavar='-var', nargs='+', default="yes",
                    help=textwrap.dedent('''\
                                         If you select yes, you should also have a reference sequence (-Ref). It will create a vcf file    
          
                                         with all the variances compared to the given reference (yes/no)'''))
parser.add_argument('-chloroplast_sequence', metavar='-Clseq', nargs='+', default="",
                    help=textwrap.dedent('''\
                                         The path to the file that contains the chloroplast sequence (Only for mito_plant mode)
                                         You have to assemble the chloroplast before you assemble the mitochondria of plants!'''))

#Dataset arguments
parser.add_argument('-read_length', metavar='-readlen', nargs='+', default="150",
                    help=textwrap.dedent('''\
                                          The length of your reads'''))

parser.add_argument('-insert_size', metavar='-insrt', nargs='+', default="300",
                    help=textwrap.dedent('''
                                         Total insert size of your paired end reads, it doesn't
                                         have to be accurate but should be close enough.'''))

parser.add_argument('-platform', metavar='-P', nargs='+', default="illumina",
                    help=textwrap.dedent('''\
                                         illumina/ion - The performance on Ion Torrent data is significantly lower'''))

parser.add_argument('-single_paired', metavar='-SP', nargs='+', default="PE",
                    help=textwrap.dedent('''\
                                         For the moment only paired end reads are supported.'''))

parser.add_argument('-merged_reads', metavar='-merged', nargs='+', default="",
                    help=textwrap.dedent('''\
                                         The path to the file that contains the combined reads (forward and reverse in 1 file)'''))
                    
parser.add_argument('-forward_reads', metavar='-F', nargs='+', 
                    help=textwrap.dedent('''\
                                         The path to the file that contains the forward reads (not necessary when there is a merged file)''
'))

parser.add_argument('-reverse_reads', metavar='-R', nargs='+',
                    help=textwrap.dedent('''\
                                         The path to the file that contains the reverse reads (not necessary when there is a merged file)''
'))

#Heteroplasmy arguments

parser.add_argument('-maf', metavar='-MAF', nargs='+', default='',
                    help=textwrap.dedent('''\
                                         (0.007-0.49) Minor Allele Frequency: If you want to detect heteroplasmy, first assemble the genome
 without this option. 
                                         Then give the resulting sequence as a reference and as a seed input. 
                                         And give the minimum minor allele frequency for this option 
                                         (0.01 will detect heteroplasmy of >1%)'''))

parser.add_argument('-hp_exclude_list', metavar='-HPX', nargs='+',default='',
                    help=textwrap.dedent('''\
                                         Option not yet available'''))

parser.add_argument('-pcr_free', metavar='-PCRF', nargs='+', default='',
                    help=textwrap.dedent('''\
                                         The path to the file that contains the reverse reads (not necessary when there is a merged file)''
'))
 
#Optional arguments 

parser.add_argument('-insert_size_auto', metavar='-insert_auto', nargs='+',default='yes',
                    help=textwrap.dedent('''\
                                         (yes/no) This will finetune your insert size automatically (Default: yes)  '''))

parser.add_argument('-use_quality_scores', metavar='-QS', nargs='+',default='no',
                    help=textwrap.dedent('''\
                                          It will take in account the quality scores, only use this when reads have low quality, like with 
the    
                                          300 bp reads of Illumina (yes/no)'''))

parser.add_argument('-output_path', metavar='-OP', nargs='+',default='/data2/ssmith/novo_output/',
                    help=textwrap.dedent('''\
                                          Give path to output directory'''))

options = parser.parse_args()
        
root_dir = "/data2/ssmith/fastqs/" 
script_dir = "/data2/ssmith/novo_config_files"

#create configfile for each directory
config_file_name = options.project_name[0]
config_file_path = os.path.join(script_dir,config_file_name+"_config.txt")
config_outfile = open(config_file_path,"w")
config_outfile.write(textwrap.dedent(textwrap.dedent(f'''Project:
-------------------------
Project name          = {str(options.project_name[0])}
Type                  = {options.type}
Genome Range          = {options.genome_range}
K-mer                 = {options.k_mer}
Max memory            = {options.max_memory}
Extended log          = {options.extended_log}
Save assembled reads  = {options.save_assembled_reads}
Seed Input            = {options.seed_input[0]}
Extend seed directly  = {options.extend_seed_directly[0]}
Reference sequence    = {options.reference[0]}
Variance detection    = {options.variance_detection}
Chloroplast sequence  = {options.chloroplast_sequence}

Dataset 1:
-----------------------
Read Length           = {options.read_length}
Insert size           = {options.insert_size}
Platform              = {options.platform}
Single/Paired         = {options.single_paired}
Combined reads        = {options.merged_reads}
Forward reads         = {options.forward_reads[0]}
Reverse reads         = {options.reverse_reads[0]}

Heteroplasmy:
-----------------------
MAF                   = {options.maf}
HP exclude list       = {options.hp_exclude_list}
PCR-free              = {options.pcr_free}

Optional:
-----------------------
Insert size auto      = {options.insert_size_auto}
Use Quality Scores    = {options.use_quality_scores}
Output path           = {options.output_path[0]}
''')))
