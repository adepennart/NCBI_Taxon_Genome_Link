#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: taxonpathparser.py
Date: March 9th, 2022
Author: Auguste de Pennart

Description:
    Finds taxon path from taxid or taxon

List of functions:
    input_pattern_generator:
        takes user input
        creates search pattern to search against database
    
    database_look_up:
        creates database as list
        finds index of taxa of interest

      lineage_look_up:
          while loop through list to find parent ids of taxa of interest, all the way to root
          meanwhile finds each id taxon name as you go up the lineage

List of "non standard modules"
    No "non standard modules" are used in the program.

Procedure:
    1. get database and taxa of interest from input
    2. find taxa of interest in database
    3. run through database as a list to find parent ids from which to find lineage
    4. print lineage to standard output

Usage:
    python taxonpathfinder.py taxonomy.dat

known error:
    1. use mispelled as well
    2. can directly read database from online
    3. use argparse to determine whether input is taxid or taxon(right now just taxon)
    4. does not work with output file request
    5. dictionaries should reject bad inputs
 """

#import packages
#----------------------------------------------------------------------------------------
import re
import sys
from pathlib import Path

#input database
inputfile = 'taxonomy.dat'
#outputfile = 'homo_sapiens.json'

#defined functions:
#----------------------------------------------------------------------------------------

#input_pattern_generator
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#input variables:
    #no inputs

#use:
    #Takes user input as either taxa(word) or taxid(number) and creates a regex searchable 
    #format for said input.

#return:
    #user_input:
        # user input when prompted to input taxa or taxid
    #input_pattern:
        #taxon or taxid in regex searchable format
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def input_pattern_generator():
    #get taxon or taxid from user
    user_input=input("Input taxa or taxid of interest\n")
    # checks whether user input is taxon or taxid
    try:
        #checks if user input is an integer
        if int(user_input) :
            #if user input is an integer creates input_id variable
            input_id = user_input
            #creates id_flag
            id_flag=True
    #if user input is not an integer the ValueError is raised
    except ValueError:
        #if user input is not an integer creates input_taxa variable        
        input_taxa= user_input
    #checks whether id_flag was created
    if id_flag:
        #if id_flag raised places input_id in input_pattern 
        input_pattern=f'^ID\s+:\s{input_id}$'
    #checks whether id_flag was not created
    elif not id_flag:
        #if id_flag not raised places input_taxa in input_pattern
        input_pattern=f'SCIENTIFIC NAME\s+:\s{input_taxa}$'
    #function returns both user input and a regex searchable format of user input
    return user_input, input_pattern


#database_look_up
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#input variables:
    #database:
        #taxonomic database of interest
    #input_pattern:
        #taxon or taxid user input in regex searchable format
    #input_name:
        #taxon or taxid user input
        
#use:
    #Creates searchable database as form of list.
    #Finds index/line in database where taxon or taxid is found.

#return:
    #taxonomy_list:
        # taxonmic database as a list
    #index:
        # index/line where taxon or taxid is found
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def database_look_up(database=None,input_pattern=None,input_name=None):
    #empty taxonomy_list variable
    taxonomy_list=[]
    # opening databse file
    database = open(database, 'r')
    #for loop through each enumerated line in database
    for n,line in enumerate(database):
        #print(line) #debugging
        #adds line of database to taxonomy_list
        taxonomy_list.append(line.strip())
        # print(flag) #debugging
        #searches for taxon or taxid in each line of database
        if re.search(input_pattern, line):
            #creates index variable, the line number for the taxon or taxid is on
            index=n
            #prints to output that the taxon or taxid and its line number were found
            print(f"found {input_name} at line {index}")
            # print(index) #debugging
        else:
            pass
    #checks whether user defined taxon or taxid was found in database
    try:
        #if index is a variable, taxon or taxid was found and the script can be continued
        index
    #if index is not a variable raises UnboundLocalError flag
    except UnboundLocalError:
        #prints to standard output that taxon or taxid inputted was not found in database
        print("taxa not found or mispelled, please try again")
        #exits script
        exit()
    database.close()  # closing
    #function returns the taxonomic database as a list and line number for the taxon or taxid 
    return taxonomy_list, index

#lineage_find
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#input variables:
    #database_input:
        #indexable taxonomic database
    #index:
        #index/line for taxon or taxid in taxonomic database
    #input_pattern:
        #taxon or taxid user input in regex searchable format
    #input_name:
        #taxon or taxid user input
        
#use:
    #while loop through each line above and below index/line in taxonomic dictionary
    #to find PARENT ID line.
    #Once PARENT ID is found, search for PARENT ID as the new ID, moving up lineage.
    #Add SCIENTIFIC NAME of taxon to lineage list
    #repeat steps, through while loop, till root is found


#return:
    #lineage:
        #List of taxons from user inputted taxon or taxid to root of all life

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def lineage_find(database_input=None, index=None,input_pattern=None,input_name=None):
    #assigned variables
    #counter to move to next element in list
    count=0
    #empty list to add taxa from taxa of interest to root
    lineage=[]
    #while loop moving to each parent taxa
    while 1:
        #while loop through each element found before taxon or taxid in taxonomic list 
        while 1:
            #searches for // characters in list element, this defines the uppermost part of each taxon info section
            if '//' in database_input[index-count]:
                # print(database_input[index-count])#debugging
                #while loop broken if // characters found
                break 
            # searches for regex searchable format of user defined the taxon or taxid in list
            elif re.search(input_pattern, database_input[index-count]):
                # print(database_input[index-count])#debugging
                # prints, again, to output that user defined taxon or taxid found at certain element number in list
                print(f"confirmed find of {input_name} at line {index}")
                # searches for SCIENTIFIC NAME in regex searchable format of user defined the taxon or taxid
                if re.search('SCIENTIFIC NAME', input_pattern):
                    # creates variable name, pulling out taxa name for the lineage list
                    name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)$', database_input[index-count]).group(1)        
                    #allows to proceed to next element in list
                    count+=1
                    #adds taxon to lineage list
                    lineage.append(f'{name}')
                else:
                    # print(database_input[index-count]) #debugging
                    #allows to proceed to next element in list
                    count+=1
            #searches for PARENT ID in list element, allowing to find parent taxon
            elif re.search('PARENT ID', database_input[index-count]):
                # print(database_input[index-count]) #debugging
                #creates variable for parent id for searching parent taxa
                parent_id=database_input[index-count]
                #allows to proceed to next element in list
                count+=1
            else:
                # print(database_input[index-count]) #debugging
                #allows to proceed to next element in list
                count+=1
        #ensures index is not reobserved in while loop
        count=1
        #while loop through each element found after taxon or taxid in taxonomic list 
        while 1:
            #searches for // characters in list element, this defines the uppermost part of each taxon info section
            if '//' in database_input[index+count]:
                # print(database_input[index+count]) #debugging
                #while loop broken if // characters found
                break
            #searches for PARENT ID in list element, allowing to find parent taxon
            elif re.search('PARENT ID', database_input[index+count]):
                # print(database_input[index+count]) #debugging
                #creates variable for parent id for searching parent taxa
                parent_id=database_input[index+count]
                #allows to proceed to next element in list
                count+=1
            #searches for GC ID in list element, allowing to find taxon name 1-2 lines after
            elif re.search('^GC ID\s+:\s[\d]+', database_input[index+count]):
                #searches for MGC ID in list element, allowing to find taxon name 1 line after 
                if re.search('^MGC ID\s+:\s[\d]+', database_input[index+count+1]): 
                    # print(database_input[index-count]) #debugging
                    #creates variable of taxon name
                    name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)', database_input[index+count+2]).group(1)  
                    #adds taxon name to lineage list
                    lineage.append(name) 
                    #allows to proceed to next element in list
                    count+=1
                #searches for SCIENTIFIC NAME in list element, to find taxon name 
                elif re.search('SCIENTIFIC NAME\s+:\s[A-Za-z\s\d\-\[\]]+$', database_input[index+count+1]):
                    # print(database_input[index-count]) #debuggigng
                    #creates variable of taxon name
                    name=re.search('SCIENTIFIC NAME\s+:\s([A-Za-z\s\d\-\[\]]+)', database_input[index+count+1]).group(1)        
                    #adds taxon name to lineage list
                    lineage.append(name) 
                    #allows to proceed to next element in list
                    count+=1
                else:
                    # print(database_input[index+count])
                    count+=1
            else:
                # print(database_input[index+count])
                count+=1
        #reset counter for finding parent taxon name and grandparent taxon id
        count=0
        #creates variable ID, to reset the parent id to the new child id 
        ID=re.search('^PARENT ID\s+:\s([\d]+)', parent_id).group(1)
        # print(f'{ID} is the parent ID') #debugging
        #modifies ID varaible to be searchable in taxonomic list
        ID=f'ID                        : {ID}' 
        #checks whether new child id in taxonomic list
        try:
            #creates new index for new child taxon
            index=database_input.index(ID)
        #if new child id out of range of taxonomic list raises ValueError
        except ValueError:
            #prints that the largest parent taxon has been found
            print("Reached root")
            #breaks while loop
            break
    #reverses lineage variable, so largest parent taxon shown first 
    lineage.reverse()  
    #return the list of all taxon and all parent taxon to root
    return lineage

#main code
#--------------------------------------------------------------------------------------

#input file verification
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


#get regex searchable pattern for user inputted taxon or taxid
taxon_and_pattern=input_pattern_generator()

#get database as list and taxon or taxid index
list_and_index=database_look_up(inputfile,taxon_and_pattern[1],taxon_and_pattern[0])

#find lineage of taxon or taxid 
lineage=lineage_find(list_and_index[0],list_and_index[1],taxon_and_pattern[1],taxon_and_pattern[0])

#graphical representation of lineage
#assigned variables
tab=""
count=0
#for loop through each taxa name
for taxa in lineage:
    #print to output
    print(f'{tab}{taxa}')
    if count==0:
        tab+='+---'
    tab='\t'+tab
    count+=1
    
# print(lineage)


#output.close()  # closing
