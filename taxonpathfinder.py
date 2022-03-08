#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: taxonpathparser.py
Date: March 8th, 2022
Author: Auguste de Pennart

Description:
    Finds taxon path from (taxid or) taxon

List of functions:
    database_look_up:
        creates database as list
        finds index of species of interest

      lineage_look_up:
          while loop through list to find parent ids of species of interest, all the way to root
          meanwhile finds each id taxon name as you go up the lineage

List of "non standard modules"
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
    2. can directly read database from online
    3. use argparse to determine whether input is taxid or taxon(right now just taxon)
    4. only finds species
 """

#import packages
import re
import random
import sys
from pathlib import Path

# allows for different file names to be adjusted easily for user
inputfile = 'taxonomy.dat'
outputfile = 'homo_sapiens.json'

#assigned variables
input_species='Homo sapiens'
input_species_pattern=f'SCIENTIFIC NAME\s+:\s{input_species}$'

#functions
def database_look_up(database=None,species_pattern=None):
    #assigned variables
    flag=False
    taxonomy=[]
    # opening inputfile
    database = open(database, 'r')
    #for loop through each line in inputted
    for n,line in enumerate(database):
        #print(line)
        taxonomy.append(line.strip())
        if re.search('RANK\s+:\sspecies', line):  # finds line if fasta header
            # print(line)
            flag=True
        elif re.search('SCIENTIFIC NAME', line):
            if flag:
                # print(line)
                #print(f"{rank_s} {line}")
                if re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', line.strip()):
                    flag=False
                    #may be able to make last character not be white space/however it did find homo sapiens, try and break
                    #also updated to other organisms
                    #this was modified, not sure if still works (added$)
                    if re.search(species_pattern, line):
                        print(f"found {input_species}")
                        #test=re.search('(SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+)', line.strip()).group(1) 
                        index=n
                        print(index)
                        #print(test)
                    else:
                        pass
                else:
                    #print(line)
                    pass
            else:
                pass
        else:
            pass
    database.close()  # closing
    return taxonomy, index


def lineage_find(database_input=None, index=None):
    #assigned variables
    count=0
    lineage=[]
    while 1:
        while 1:
            if '//' in database_input[index-count]:
                # print(database_input[index-count])
                break
            #this needs to be updated for other organisms
            elif re.search(input_species_pattern, database_input[index-count]):
                #this is repeated from the for loop through the database
                # print(database_input[index-count])
                print(f"found {input_species} at line {index}")
                rank_s=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\d\-\[\]]+)\s([A-Za-z\s\d\-\[\]]+)', database_input[index-count]).group(1,2)        
                count+=1
                #not sure this will work for all searches
                lineage.append(f'{rank_s[0]} {rank_s[1]}')
            elif re.search('PARENT ID', database_input[index-count]):
                # print(database_input[index-count])
                parent_id=database_input[index-count]
                count+=1
            else:
                # print(database_input[index-count])
                count+=1
        count=1
        while 1:
            if '//' in database_input[index+count]:
                # print(database_input[index+count])
                break
            elif re.search('PARENT ID', database_input[index+count]):
                # print(database_input[index+count])
                parent_id=database_input[index+count]
                count+=1
            elif re.search('^GC ID\s+:\s[\d]+', database_input[index-count]): 
                if re.search('^MGC ID\s+:\s[\d]+', database_input[index+count+1]): 
                    # print(database_input[index-count])
                    name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)', database_input[index+count+2]).group(1)  
                    lineage.append(name) 
                    count+=1
                elif re.search('SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+$', database_input[index+count+1]):
                    #this is repeated from the for loop through the database
                    # print(database_input[index-count])
                    name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)', database_input[index+count+1]).group(1)        
                    lineage.append(name) 
                    count+=1
                else:
                    # print(database_input[index+count])
                    count+=1
            else:
                # print(database_input[index+count])
                count+=1
        count=0
        ID=re.search('^PARENT ID\s+:\s([\d]+)', parent_id).group(1)
        # print(f'{ID} is the parent ID')
        ID=f'ID                        : {ID}'
        try:
            index=database_input.index(ID)
        except ValueError:
            print("Reached root")
            break
    lineage.reverse()  
    return lineage

#main code
#___________________________________________________________#

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
database_look_up(inputfile,input_species_pattern)

print(lineage_find(database_look_up(inputfile,input_species_pattern)[0],database_look_up(inputfile,input_species_pattern)[1]))


#output.close()  # closing
