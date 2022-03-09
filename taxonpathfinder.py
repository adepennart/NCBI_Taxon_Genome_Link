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
    1. get database and species of interest from input
    2. find species of interest in database
    3. run through database as a list to find parent ids from which to find lineage
    4. print lineage to output

Usage:
    python taxonpathfinder.py taxonomy.dat homo_sapiends.json

known error:
    1. use mispelled as well
    2. can directly read database from online
    3. use argparse to determine whether input is taxid or taxon(right now just taxon)
    4. only finds species
    5. does not work with output file request
 """

#import packages
import re
import random
import sys
from pathlib import Path

# allows for different file names to be adjusted easily for user
inputfile = 'taxonomy.dat'
#outputfile = 'homo_sapiens.json'

#assigned variables
#input_species='Homo sapiens'
#input_species_pattern=f'SCIENTIFIC NAME\s+:\s{input_species}$'

#assigned variables
def input_pattern_generator():
    inputted=input("Input Species of Interest\n")
    try:
        if int(inputted) :
            input_id = inputted
            id_flag=True
    except ValueError:
        input_species= inputted
        id_flag=False
    #input_species[0]=input_species.capitalize()[0]
    if id_flag:
        input_pattern=f'^ID\s+:\s{input_id}$'
    elif not id_flag:
        input_pattern=f'SCIENTIFIC NAME\s+:\s{input_species}$'
    return input_pattern, inputted

#functions
def database_look_up(database=None,input_pattern=None,input_name=None):
    #assigned variables
    taxonomy=[]
    # opening inputfile
    database = open(database, 'r')
    #for loop through each line in inputted
    for n,line in enumerate(database):
        #print(line)
        taxonomy.append(line.strip())
        # print(flag)
        if re.search(input_pattern, line):
            print(f"found {input_name}")
            #test=re.search('(SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+)', line.strip()).group(1) 
            index=n
            print(index)
            #print(test)
        else:
            pass
    try:
        print(index)
    except UnboundLocalError:
        print("Species not found or mispelled, please try again")
        exit()
    database.close()  # closing
    return taxonomy, index


def lineage_find(database_input=None, index=None,input_pattern=None):
    #assigned variables
    count=0
    lineage=[]
    while 1:
        while 1:
            if '//' in database_input[index-count]:
                # print(database_input[index-count])
                break
            #this needs to be updated for other organisms
            elif re.search(input_pattern, database_input[index-count]):
                #this is repeated from the for loop through the database
                # print(database_input[index-count])
                print(f"found {input_pattern} at line {index}")
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
    # outputfile = outputfile


# exits script if unexpected arguments in commandline.
else:
    try:
        raise ArithmeticError
    except:
        print("Looking for 2 argument, try again")
        exit()


#get searchable pattern
input_pattern_generator_output=input_pattern_generator()
#get index and database as lsit
database_look_up_output=database_look_up(inputfile,input_pattern_generator_output[0],input_pattern_generator_output[1])

#find lineage
lineage_find_output=lineage_find(database_look_up_output[0],database_look_up_output[1],input_pattern_generator_output[0])
print(lineage_find_output)


#output.close()  # closing
