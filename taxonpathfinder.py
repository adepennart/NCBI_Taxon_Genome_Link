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
    1. use mispelled as well
    
    
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
inputfile = 'taxonomy.dat'
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
parent_check=False
first=False
count=0
# opening inputfile and outputfile
inputted = open(inputfile, 'r')
output = open(outputfile, 'w')
#for loop through each line in inputted
for n,line in enumerate(inputted):
    #print(line)
    taxonomy.append(line.strip())
    # if re.search('^ID\s+:\s207598', line):#so weird
    #     print("hey")
    #     # break

    if re.search('RANK\s+:\sspecies', line):  # finds line if fasta header
        # print(line)
        rank_s=re.search('RANK\s+:\s(species)', line).group(1)
        flag=True
    elif re.search('SCIENTIFIC NAME', line):
        if flag:
            # print(line)
            #print(f"{rank_s} {line}")
            if re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', line.strip()):
                rank_s=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', line.strip()).group(1,2)        
                species_dict[rank_s[0]]=rank_s[1] 
                flag=False
                #may be able to make last character not be white space/however it did find homo sapiens, try and break
                #also updated to other organisms
                #this was modified, not sure if still works (added$)
                if re.search('SCIENTIFIC NAME\s+:\sHomo\ssapiens$', line):
                    human=re.search('(SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+)', line.strip()).group(1) 
                    index=n
                    print(index)
                    print(human)
                    #break#break when find first sapiens
                else:
                    pass
            else:
                #print(line)
                pass
        else:
            pass
    else:
        pass


'''
[ {
  "taxId" : "9606",
  "scientificName" : "Homo sapiens",
  "commonName" : "human",
  "formalName" : "true",
  "rank" : "species",
  "division" : "HUM",
  "lineage" : "Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini; Catarrhini; Hominidae; Homo; ",
  "geneticCode" : "1",
  "mitochondrialGeneticCode" : "2",
  "submittable" : "true"
} ]
'''

#%%
#temporary location
json_dict={}
first_MGC=True
first_GC=True
first_rank=True
first_ID=True
first_Genebank=True
lineage=""
one_scientific_name=True
#temporary variable
index=63207
count=0

#fix order of this= so it looks good
while 1:
# for n in range(0,10):
    while 1:
        if '//' in taxonomy[index-count]:
            print(taxonomy[index-count])
            break
        #this needs to be updated for other organisms
        if one_scientific_name:
            if re.search('SCIENTIFIC NAME\s+:\sHomo\ssapiens$', taxonomy[index-count]):
                #this is repeated from the for loop through the database
                print(taxonomy[index-count])
                rank_s=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', taxonomy[index-count]).group(1,2)        
                species_dict[rank_s[0]]=rank_s[1] 
                json_dict["scientificName"]=rank_s[0]+' '+rank_s[1]
                lineage+=f'{rank_s[0]} {rank_s[1]}; ' 
                count+=1
                one_scientific_name=False
            else:
                print(taxonomy[index+count])
                count+=1
        elif first_MGC:
            if re.search('^MGC ID\s+:\s[\d]+', taxonomy[index-count]): 
                print(taxonomy[index-count])
                MGC=re.search('^MGC ID\s+:\s([\d]+)', taxonomy[index-count]).group(1)
                json_dict['mitochondrialGeneticCode']=MGC
                first_MGC=False 
                count+=1
            else:
                print(taxonomy[index-count])
                count+=1
        elif first_GC:
            if re.search('^GC ID\s+:\s[\d]+', taxonomy[index-count]): 
                print(taxonomy[index-count])
                GC=re.search('^GC ID\s+:\s([\d]+)', taxonomy[index-count]).group(1)
                json_dict['geneticCode']=GC
                first_GC=False 
                count+=1
            else:
                print(taxonomy[index-count])
                count+=1
        elif first_rank:
            if re.search('^RANK\s+:\s[A-Za-z]+', taxonomy[index-count]): 
                print(taxonomy[index-count])
                rank=re.search('^RANK\s+:\s([A-Za-z]+)', taxonomy[index-count]).group(1)
                json_dict['rank']=rank
                first_rank=False   
                count+=1
            else:
                print(taxonomy[index-count])
                count+=1
        elif re.search('PARENT ID', taxonomy[index-count]):
            print(taxonomy[index-count])
            parent_id=taxonomy[index-count]
            count+=1
        elif first_ID:
            if re.search('^ID', taxonomy[index-count]):
                print(taxonomy[index-count])
                ID=re.search('^ID\s+:\s([\d]+)', taxonomy[index-count]).group(1)
                json_dict['taxId']=ID
                first_ID=False
                count+=1
            else:
                print(taxonomy[index-count])
                count+=1
        else:
            print(taxonomy[index-count])
            count+=1
    count=1
    one_scientific_name=True
    while 1:
        if '//' in taxonomy[index+count]:
            print(taxonomy[index+count])
            break
        elif re.search('PARENT ID', taxonomy[index+count]):
            print(taxonomy[index+count])
            parent_id=taxonomy[index+count]
            count+=1
        #why is this needed
        elif one_scientific_name:
            if re.search('SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+$', taxonomy[index-count]):
                #this is repeated from the for loop through the database
                print(taxonomy[index-count])
                name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)', taxonomy[index-count]).group(1)        
                lineage+=f'{name}; ' 
                count+=1
                one_scientific_name=False
            else:
                print(taxonomy[index+count])
                count+=1
        elif first_Genebank:
            #assuming all names are just letters
            if re.search('^GENEBANK COMMON NAME\s+:\s[A-Za-z\s]+', taxonomy[index-count]): 
                print(taxonomy[index-count])
                Genebank=re.search('^GENEBANK COMMON NAME\s+:\s([A-Za-z\s]+)', taxonomy[index-count]).group(1)
                json_dict['CommonName']=Genebank
                first_Genebank=False
                count+=1
            elif re.search('^COMMON NAME\s+:\s[A-Za-z\s]+', taxonomy[index-count]): 
                print(taxonomy[index-count])
                common=re.search('^COMMON NAME\s+:\s([A-Za-z\s]+)', taxonomy[index-count]).group(1)
                json_dict['CommonName']=common
                first_Genebank=False 
                count+=1
            else:
                print(taxonomy[index-count])
                count+=1
        else:
            print(taxonomy[index+count])
            count+=1
    count=0
    one_scientific_name=True
    print(f'{parent_id} is the parent ID')
    ID=re.search('^PARENT ID\s+:\s([\d]+)', parent_id).group(1)
    ID=f'ID                        : {ID}'
    try:
        index=taxonomy.index(ID)
    except ValueError:
        print("Reached root")
        break
json_dict["Lineage"]=lineage

print(json_dict)       
    

inputted.close()  # closing
output.close()  # closing
