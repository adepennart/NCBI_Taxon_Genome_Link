#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 15:14:12 2022

@author: inf-49-2021
"""

#import packages
#----------------------------------------------------------------------------------------
import re
import sys
from pathlib import Path
import entrezpy.efetch.efetcher


#input database
inputfile = 'taxonomy.dat'
#outputfile = 'homo_sapiens.json'
email='adepennart@gmail.com'


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
        input_pattern={'db' : 'taxonomy', 'id' : [input_id], 'retmode': 'xml'}
    #checks whether id_flag was not created
    elif not id_flag:
        print('not a taxid, but taxon')
        exit()
        #if id_flag not raised places input_taxa in input_pattern
        input_pattern=f'SCIENTIFIC NAME\s+:\s{input_taxa}$'
    #function returns both user input and a regex searchable format of user input
    return user_input, input_pattern


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


ef = entrezpy.efetch.efetcher.Efetcher('efetcher', email)

# examples= {'db': 'nucleotide', 'id': [5]}
# examples={'db' : 'taxonomy', 'id' : [1232345], 'retmode': 'xml'}
# examples2={'db' : 'taxonomy', 'term':'Actinobacteria', 'retmode': 'xml'}


a = ef.inquire(examples)
# a = ef.inquire(examples2)

#get regex searchable pattern for user inputted taxon or taxid
taxon_and_pattern=input_pattern_generator()

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

# import entrezpy.conduit
# c = entrezpy.conduit.Conduit(email)
# fetch_influenza = c.new_pipeline()
# sid = fetch_influenza.add_search({'db' : 'nucleotide', 'term' : 'H3N2 [organism] AND HA', 'rettype':'count', 'sort' : 'Date Released', 'mindate': 2000, 'maxdate':2019, 'datetype' : 'pdat'})
# fid = fetch_influenza.add_fetch({'retmax' : 10, 'retmode' : 'text', 'rettype': 'fasta'}, dependency=sid)
# c.run(fetch_influenza)

# import entrezpy.conduit
# c = entrezpy.conduit.Conduit(email)
# fetch_influenza = c.new_pipeline()
# sid = fetch_influenza.add_search({'db' : 'taxonomy', 'term' : 'Homo sapiens[SCIENTIFICNAME]'})
# fid = fetch_influenza.add_fetch({ 'retmode' : 'text', 'rettype': 'xml'}, dependency=sid)
# c.run(fetch_influenza)