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
    3. use argparse to determine whether input is taxid or taxon 
    4. does not work with output file request
    5. input_pattern_generator should reject bad inputs
 """


#import modules
#----------------------------------------------------------------------------------------
import re #module for using regex
import sys #module for using terminal
from pathlib import Path #module for verifying file path
from urllib.request import urlopen #module to open the url 
from lxml import etree #module to read xml files 

#input variables
# taxid_or_taxon=
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
#if error shown in url, should escape

def input_pattern_generator():
    #assigned variables
    #empty list to add taxa from taxa of interest to root
    lineage=[]
    #base url for fetching lineage
    baseurl_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" 
    #base url for searching for searching for taxid from taxon
    baseurl_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" 
    #get taxon or taxid from user
    user_input=input("Input taxa or taxid of interest\n")
    first=True
    # checks whether user input is taxon or taxid    
    try:
        #checks if user input is an integer
        if int(user_input) :
            #if user input is an integer creates input_id variable
            input_id = user_input
            #creates id_flag=True
            id_flag=True
    #if user input is not an integer the ValueError is raised
    except ValueError:
        #if user input is not an integer creates input_taxa variable        
        input_taxa= user_input
        #creates id_flag=True
        id_flag=False
    #checks whether id_flag is True
    if id_flag:
        #if id_flag raised places input_id in input_pattern 
        query = f"db=taxonomy&id=[{input_id}]&format=xml" 
        url = baseurl_fetch+query 
        f = urlopen(url) #opens the url with urlopen module 
        resultxml = f.read() #reads the url content 
        xml = etree.XML(resultxml) #parses the content into xml format 
        resultelements = xml.xpath("//ScientificName") #search for all tags 
        #with given xpath 
        #this is using eran's stuff, could technically new line each value and get what i want(i think)
        for element in resultelements: 
            if first:
                taxon=element.text
                first=False
            elif not first:
                #print (element.text)
                #adds taxon to lineage list
                lineage.append(element.text) 
        lineage.append(taxon) 
    #checks whether id_flag is False
    elif not id_flag:
        #replaces white space with %20, so url can be searched
        input_taxa = input_taxa.replace(" ", "%20")
        #if id_flag raised places input_id in input_pattern 
        query = f"db=taxonomy&term={input_taxa}&format=xml" 
        url = baseurl_search+query 
        f = urlopen(url) #opens the url with urlopen module 
        resultxml = f.read() #reads the url content 
        # print(resultxml)
        xml = etree.XML(resultxml) #parses the content into xml format
        resultelements = xml.xpath("//Id") #search for all tags 
        for element in resultelements: 
                # print(element.text)
                input_id=element.text
        # print(input_id)
        new_query = f"db=taxonomy&id=[{input_id}]&format=xml"
        # print(new_query)
        new_url = baseurl_fetch+new_query 
        entrez = urlopen(new_url) #opens the url with urlopen module 
        resultxml = entrez.read() #reads the url content 
        xml = etree.XML(resultxml) #parses the content into xml format
        resultelements = xml.xpath("//ScientificName") #search for all tags 
        #with given xpath 
        #this is using eran's stuff, could technically new line each value and get what i want(i think)
        for element in resultelements: 
            if first:
                taxon=element.text
                first=False
            elif not first:
                #print (element.text)
                #adds taxon to lineage list
                lineage.append(element.text) 
        lineage.append(taxon) 
    #return the list of all taxon and all parent taxon to root
    return lineage


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

# uses the files specified above in the script
if len(sys.argv) == 1:
    pass

# exits script if unexpected arguments in commandline.
else:
    try:
        raise ArithmeticError
    except:
        print("Looking for one argument, try again")
        exit()

#get regex searchable pattern for user inputted taxon or taxid
lineage=input_pattern_generator()

#find lineage of taxon or taxid 
# lineage=lineage_find(list_and_index[0],list_and_index[1],taxon_and_pattern[1],taxon_and_pattern[0])

# graphical representation of lineage
# assigned variables
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















