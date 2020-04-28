# -*- coding: utf-8 -*-
"""
For use in RepeatM. See: github.com/wwood/RepeatM
Main pipeline for Nucmer_Matching from .delta files to cluster generation


author: Daniel Rawlinson, ACE
email: daniel.rawlinson@uqconnect.edu.au
"""

#TODO - implement cluster graphing into pipe
#		- make as actual name = main python script.
'''imports'''

import single_linkage_cluster
import delta_parse
import os
import pickle
import union_find_cluster
import sys
import csv
import profiler

'''constants'''

#set locaiton of delta files
delta_dir = '/srv/home/s4479877/python/RecurM_v2/nucmer_feed_out'

#set location of assemblies
assembly_dir = '/srv/home/s4479877/python/RecurM_v2/Test2'

#set location of bam files
bam_dir = ''


#set empty vector of all nucmer_matches that pass threshold (=0.90 by default)
collated_sig_matches = []
sigmatch_set = set()
#set empty vector to collect all nucmer_matches that are fragments of larger assemblies
fragments = []

'''-------------------------begin pipe-------------------------------------'''


#read in nucmer matches of each deltafile
#@profiler.profile
def main_pipe():
     for file in os.listdir(delta_dir):
         if file.endswith('.delta'):
             print('parsing {}'.format(file))
             delta = delta_parse.deltaread(delta_dir+'/'+file)
             #exit type is dictionary

             #threshold all matches and collate
             print('thresholding {}'.format(file))
             firstpass_fragments = []
             for m in next(iter(delta.values())):
                 if m.seqs[0] ==m.seqs[1]:
                     continue #it's a self match
                 else:
                     stats = m.gen_statistics()
                     if m.apply_threshold(threshold = 0.90, stats = stats) == True:
                         collated_sig_matches.append(m)
                         sigmatch_set.update(set(m.seqs))
                     elif m.is_fragment(upperthreshold = 0.90, lowerthreshold = 0.90, stats = stats):
                         firstpass_fragments.append(m)

             #all match objects are read in. keep only those fragments that map to full matches
             for m in firstpass_fragments:
                 if m.seqs[0] in sigmatch_set:
                     fragments.append(m)
                 elif m.seqs[1] in sigmatch_set:
                     fragments.append(m)
             sys.stdout.flush()
             #exit type is list of Nucmer_Match objects (sig_matches) + list of Nucmer_Match objects (fragments) that map to the sig_match objects
main_pipe()

#save progress
f = open('pickled_sigmatches', 'wb')
pickle.dump(collated_sig_matches, f)
f.close()

f = open('pickled_fragmatches', 'wb')
pickle.dump(fragments, f)
f.close()


print('clustering...')
#cluster all significant matches & sort
clusters = single_linkage_cluster.cluster_nucmer_matches(collated_sig_matches)

#sort clusters
single_linkage_cluster.sort_clusters(clusters)

#further refine fragments to find those only that map to the trimmed clusters (ie. size >2)
cluster_nodes = []
for c in clusters:
    cluster_nodes +=c.nodes
cluster_node_set = set(cluster_nodes)

cluster_frags = []

print('extracting fragments...')
for m in fragments:
    if m.seqs[0] in cluster_node_set:
        cluster_frags.append(m)
    elif m.seqs[1] in cluster_node_set:
        cluster_frags.append(m)

#pickle the clusters
print('pickling clusters...')
f = open('pickled_clusters', 'wb')
pickle.dump(clusters, f)
f.close()
#exit type is list of Contig_Cluster objects

print('pickling fragments...')
f = open('pickled_fragments', 'wb')
pickle.dump(cluster_frags, f)
f.close()
#exit type is list of match objects connecting clusters together.

#run analysis on clusters
print('retrieving cluster sequences...')
for c in clusters:
   c.retrieve_seqs(assembly_dir = assembly_dir) #locations set at beginning of script. Does not return anything

circular = []
perfect = []

#label clusters

print('labelling clusters...')
for c in clusters:
    labs = c.label_cluster()
    n_matches = len(labs)
    n_perfect=0
    for l in labs:
        if 'circular' in l: #if any labels are circular, mark as circular
            circular.append(c)
            break
        elif 'perfect' in l: # if > half of labels are 'perfect', mark as perfect
            n_perfect+=1
            if n_perfect >= n_matches/2:
                perfect.append(c)
                break

#summaries of circular and perfect clusters
print('producing summaries...')

with open('circular_summary.csv', 'w',  newline='') as f:
    w = csv.writer(f)
    w.writerow(['Record','Contigs','Size', 'Length', 'Coverage'])
    for (index, c) in enumerate(circular):
        nodes_list = ""
        for n in c.nodes:
            nodes_list += n + '; '
        w.writerow([index+1, nodes_list, c.size, c.av_length, c.av_cov])
        
with open('linear_summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Record','Contigs','Size', 'Length', 'Coverage'])
    for (index, c) in enumerate(perfect):
        nodes_list = ""
        for n in c.nodes:
            nodes_list += n + '; '
        w.writerow([index+1, nodes_list, c.size, c.av_length, c.av_cov])

print('complete!')
'''-------------------------------------end pipe---------------------------'''
