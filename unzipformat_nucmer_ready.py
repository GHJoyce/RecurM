# This code sets a fasta file to SPAdes assembly format which is as follows:
#>ASSEMBLY__NODE_3_length_2402_cov_243.207

#!/usr/bin/env python3

#import relevant packages
import sys
import os.path
from Bio import SeqIO
import gzip
import logging

logging.basicConfig(filename='unzipping.log',level=logging.DEBUG)

# Take in a list of fasta files that you type into the terminal using sys.argv
# this works for example by: python nucmer_readyV2.py file1.fna file2.fna, where the list is file1.fna and file2.fna
# fastafiles = sys.argv[1:]


# The following accesses a folder of files
filepath = "/srv/projects3/human_plasmids/ibdmdb-contigs"

fastafiles = os.listdir(filepath)


for item in fastafiles:
    # This is kinda longwinded, but I'm essentially trying to get the filename. The strip is because I don't want the
    # 'gz' which appears at the end of these damned zip files
    assembly = os.path.basename(item).rstrip(".gz")
    # This is to overcome the .gz extension of my downloaded fasta
    handle = gzip.open(filepath + '/' + item, "rt")
    print("Opening ", assembly)
    try:
        # put these records into a new list
        sequences = list(SeqIO.parse(handle, "fasta"))
    except EOFError as e:
        # Output expected EOFErrors.
        print("EOFError occurred on file ", assembly)
        logging.exception(e)
        pass
    else:
        for (index, seq_record) in enumerate(sequences):
            # The following 2 lines are only useful for grabbing the k-mer coverage of multihit fasta header formats. Eg.
            # >k105_5 flag=1 multi=5.0000 len=444, where we are grabbing the 'multi' info.
            grab_kmer_cov = seq_record.description.split(" ")[2]
            kmer_cov = grab_kmer_cov.split("=")[1]
            seq_record.id = assembly+"__NODE_"+str(index+1)+"_length_"+str(len(seq_record))+"_cov_"+kmer_cov
            # the above code seems to turn the previous seq id into the seq description, so lets get rid of that
            seq_record.description = ""

        handle.close()
        # fr. refers to spades ready
        SeqIO.write(sequences, "/srv/projects3/human_plasmids/georgina/ibdmdb-contigs_unzipped2/fr."+assembly, "fasta")