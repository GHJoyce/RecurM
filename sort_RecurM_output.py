# This code takes in the output of RecurM and reformats it into a csv file that can be more easily investigated

#!/usr/bin/env python3

import csv
import os.path
from datetime import date
from Bio import SeqIO

today = date.today()

# Set the input location
in_path = "/srv/home/s4479877/python/RecurM_Script/Output"
# Set the output location
out_path = "/srv/home/s4479877/python/RecurM_Sort/"
# Take in a list of the RecurM output clusters

cluster_folders = os.listdir(in_path)

# write to CSV with the filename in the format: day-month-year_RecurM_output.csv
with open(out_path + today.strftime("%d-%b-%Y")+".csv", 'w', newline='') as file:
    # Make File
    w = csv.writer(file)
    #Set the column titles
    w.writerow(["Cluster", "Size", "Contigs", "Average_Length", "Average_Coverage", "Representative_Sequence"])

    # Open the cluster folders
    for (index, folder) in enumerate(cluster_folders):
        print ("Reading folder ", folder)
        # Grabs some useful info from the folder name
        avlen = folder.split("_")[4]
        size = folder.split("_")[2]
        avcov = folder.split("_")[6]
        multifasta = os.listdir(in_path + "/" + folder)
        print ("Collecting sequence information")
        for item in multifasta:
            # Grabs some info about the first sequence in the cluster
            sequences = list(SeqIO.parse("{}/{}/{}".format(in_path, folder, item), "fasta"))
            repseq = sequences[0].seq
            contig_list = ""
            for (i, record) in enumerate(sequences):
                if i == 0:
                    contig_list += record.id
                else:
                    contig_list += "; "+record.id
        print ("Writing row ", index)
        w.writerow([index, size, contig_list, avlen, avcov, repseq])


