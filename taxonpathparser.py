#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: taxonpathparser.py
Date: November 29th, 2021
Author: Auguste de Pennart

Description:
    BLANK

List of functions:
    dictionarylookup(from module functions.py):
        function to find associated value or key, in dictionary, to specified value or key

    sortedrandom(from module functions.py):
        function to create a sorted list of randomly chosen numbers

    forloopthroughseq(from module functions.py):
        function to get amount of matches from two sequences

    load_dict_from_file(from module functions.py):
        function that makes a dictionary from the specficied input file

    No user defined functions are used in the program.

List of "non standard modules"
    functions.py
        has a list of functions that can be used in script.

    No "non standard modules" are used in the program.

Procedure:
    1. open input file
    2. create list of genus and species
    3. create list of every line
    4. use user input to getermine species of interest
    5. find lin genus species list
    6. pull out genus species

Usage:
    python mini_tax.dat homo_sapiends.json

known error:
    1. reverse list is longer than original list
    2. may not find all species names

 """

#import packages
import re
import random
import sys
from pathlib import Path
#from functions import *

# allows for different file names to be adjusted easily for user
inputfile = 'mini_tax.dat'
outputfile = 'homo_sapiens.json'
# Here we are looking for 2 arguments (script, input file[1]) placed in the command line.
# we are also making sure the input is valid
if len(sys.argv) == 2 and Path(sys.argv[1]).is_file():
    inputfile = sys.argv[1]
# here the line accounts for missing input file
elif len(sys.argv) == 2 and not Path(sys.argv[1]).is_file():
    try:
        # this line raises an error if no file exists
        if len(sys.argv) == 2 and not Path(sys.argv[1]).is_file():
            raise FileExistsError
        # for some reason something else goes wrong this error is raised
        else:
            raise FileNotFoundError
    except FileExistsError:
        print("Input file does not exist in directory or mispelled")
        exit()
    except FileNotFoundError:
        print("some other error")
        exit()


# uses the files specified above in the script
elif len(sys.argv) == 1:
    inputfile = inputfile
    outputfile = outputfile


# exits script if unexpected arguments in commandline.
else:
    try:
        raise ArithmeticError
    except:
        print("Looking for 2 argument, try again")
        exit()
#assigned variables
flag=False
taxonomy=[]
taxonomy_rev=[]
species_dict={}
# opening inputfile and outputfile
inputted = open(inputfile, 'r')
output = open(outputfile, 'w')
#for loop through each line in inputted
for line in inputted:
    #print(line)
    taxonomy.append(line.strip())
    if re.search('RANK\s+:\sspecies', line):  # finds line if fasta header
        # print(line)
        rank_s=re.search('RANK\s+:\s(species)', line).group(1)
        flag=True
    elif re.search('SCIENTIFIC NAME', line):
        if flag:
            # print(line)
            #print(f"{rank_s} {line}")
            if re.search('sapiens', line):
                print(line)
            if re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', line.strip()):
                rank_s=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', line.strip()).group(1,2)        
                species_dict[rank_s[0]]=rank_s[1] 
                flag=False
            else:
                #print(line)
                pass
        else:
            pass
    else:
        pass
    
for line in range(1,len(taxonomy)+1):
    # print(taxonomy[-line])
    taxonomy_rev.append(taxonomy[-line])
    
#print(species_dict)
for n,line in enumerate(taxonomy_rev):
    species=species_dict['Anolis']
    genus_species=f'Anolis {species}'
    if genus_species in line:
        print(line)
        print(n)
        index_n=n
        #figure out how to fix this
        # index=(taxonomy_rev.index(genus_species))
 #       print(index)
        

print(taxonomy_rev[index_n])        
print(taxonomy_rev[index_n+1]) 
print(taxonomy_rev[index_n+2]) 
print(taxonomy_rev[index_n+3]) 
print(taxonomy_rev[index_n+4]) 
print(taxonomy_rev[index_n+5]) 


#print(species_dict['Anolis'])

    # if re.search('SCIENTIFIC NAME', line):
    #     if 
    
    
    # if re.search('^>[^?*]+$', line): #finds line if fasta header
    #     print(line)
    #     pass
    # elif not re.search('^>[^?*]+$', line): #finds line if not fasta header
    #     print(line)
    #     pass
    # else:
    #     print("something went wrong") # prints if some else goes wrong
    #     pass
inputted.close()  # closing
output.close()  # closing
