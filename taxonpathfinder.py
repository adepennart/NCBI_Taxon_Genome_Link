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

# import modules
# ----------------------------------------------------------------------------------------
import re  # module for using regex
import sys  # module for using terminal
from pathlib import Path  # module for verifying file path
from urllib.request import urlopen  # module to open the url
from lxml import etree  # module to read xml files

# input variables
# taxid_or_taxon=
email = 'adepennart@gmail.com'

# taxon_or_taxid
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def taxon_or_taxid(user_input=None):
    # checks whether user input is taxon or taxid
    try:
        # checks if user input is an integer
        if int(user_input):
            # creates id_flag=True
            id_flag = True
    # if user input is not an integer the ValueError is raised
    except ValueError:
        # creates id_flag=True
        id_flag = False
    # returns whether id_flag is True or False
    return id_flag

# entrez_search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def entrez_search(user_input=None,database=None,next_of_kin=False):
    # assigned variables
    # base url for searching for searching for taxid from taxon
    baseurl_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    if next_of_kin:
        #
        query = f"db={database}&term={user_input}[next%20level]&format=xml&RetMax=100000"
    else:
        #
        query = f"db={database}&term={user_input}&format=xml&RetMax=100000"
    url = baseurl_search + query
    entrez_s = urlopen(url)  # opens the url with urlopen module
    entrez_s_read = entrez_s.read()  # reads the url content
    # print(entrez_s)
    xml_s = etree.XML(entrez_s_read)  # parses the content into xml format
    if xml_s is None:
        print('entrez_search returned empty')
    else:
        print('successful entrez_search')
    return xml_s

# entrez_fetch
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def entrez_fetch(user_input=None,database=None):
    # assigned variables
    # base url for fetching lineage
    baseurl_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    #
    query = f"db={database}&id=[{user_input}]&format=xml&RetMax=100000"
    url = baseurl_fetch + query
    entrez = urlopen(url)  # opens the url with urlopen module
    entrez_read = entrez.read()  # reads the url content
    xml_f = etree.XML(entrez_read)  # parses the content into xml format
    if xml_f is None:
        print('entrez_fetch returned empty')
    else:
        print('successful entrez_fetch')

    return xml_f

# data_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def data_find(xml=None,pattern_search=None,find_first=False):
    #
    data_list=[]
    #
    original=False
    #
    pattern_match = xml.xpath(f"//{pattern_search}")  # search for all tags
    try:
        # with given xpath
        # this is using eran's stuff, could technically new line each value and get what i want(i think)
        #what about if there is only one match?
        for match in pattern_match:
            # print(match.text)
            if find_first:
                # create original, variable for input taxon
                original = match.text
                find_first = False
            elif not find_first:
                # print (match.text)
                # adds taxon to lineage list
                data_list.append(match.text)
                # print(data_list)
        if original:
            data_list.append(original)
            print('original specified')
        else:
            pass
            # print('original unspecified')
    except UnboundLocalError:
        # prints to standard output that taxon or taxid inputted was not found in database
        print("taxid not found or mispelled, please try again")
        # exits script
        exit()
    return data_list

# lineage_search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def lineage_search(user_input=None):
    id_flag=taxon_or_taxid(user_input)
    # checks whether id_flag is True
    if id_flag:
        #database specified to taxonomy
        xml_f=entrez_fetch(user_input,'taxonomy')
        lineage=data_find(xml_f,'ScientificName', find_first=True)
    # checks whether id_flag is False
    elif not id_flag:
        xml_s=entrez_search(user_input,'taxonomy')
        ID=data_find(xml_s,'Id')
        #not verified if single variable
        ID = ID[0]
        # print(ID)
        xml_f = entrez_fetch(ID, 'taxonomy')
        lineage = data_find(xml_f, 'ScientificName', find_first=True)
    # return the list of all taxon and all parent taxon to root
    return lineage

# assembled_genome_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# no inputs

# use:
# Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
# format for said input.

# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# if error shown in url, should escape

def assembled_genome_find(user_input=None):
    id_flag=taxon_or_taxid(user_input)
    if id_flag:
        xml_s=entrez_search(user_input,'assembly')
        genomes=data_find(xml_s,'Id')
    # checks whether id_flag is False
    elif not id_flag:
        xml_s = entrez_search(user_input, 'assembly')
        genomes = data_find(xml_s, 'Id')
    # return the list of all taxon and all parent taxon to root
    return len(genomes)


# child_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
# database_input:
# indexable taxonomic database
# index:
# index/line for taxon or taxid in taxonomic database
# input_pattern:
# taxon or taxid user input in regex searchable format
# input_name:
# taxon or taxid user input

# use:
# while loop through each line above and below index/line in taxonomic dictionary
# to find PARENT ID line.
# Once PARENT ID is found, search for PARENT ID as the new ID, moving up lineage.
# Add SCIENTIFIC NAME of taxon to lineage list
# repeat steps, through while loop, till root is found


# return:
# lineage:
# List of taxons from user inputted taxon or taxid to root of all life

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def child_find(user_input=None):
    #variables
    count =0
    child_list=[]
    grandchild_id_list=[]
    child_lineage={}
    rev_child_lineage={}
    id_flag = taxon_or_taxid(user_input)
    # checks whether id_flag is True
    if id_flag:
        # database specified to taxonomy
        xml_f = entrez_fetch(user_input, 'taxonomy')
        lineage = data_find(xml_f, 'ScientificName')
        #be wary of environmental samples
        taxon = lineage[0]
        taxon = taxon.text.replace(" ", "%20")
        xml_s = entrez_search(taxon, 'taxonomy',next_of_kin=True)
        child_id_list = data_find(xml_s, 'Id')
    # checks whether id_flag is False
    elif not id_flag:
        xml_s = entrez_search(user_input, 'taxonomy', next_of_kin=True)
        child_id_list = data_find(xml_s, 'Id')
    while 1:
        for ID in child_id_list:
            # database specified to taxonomy
            xml_f = entrez_fetch(ID, 'taxonomy')
            lineage_list = data_find(xml_f, 'ScientificName')
            # print(data_list)
            taxon = lineage_list[0]
            #do this in function
            taxon = taxon.replace(" ", "%20")
            child_list.append(taxon)
            print(rev_child_lineage.values())
            # if ID in rev_child_lineage.keys():
            # # if re.search(ID,child_lineage.values()):
            #     print(ID)
            #     key=rev_child_lineage[ID]
            #     key=re.search()
            #     print(type(key))
            #     print(str(key))
            #     child_lineage[key]=taxon
        #fix this too
        if 'environmental%20samples' in child_list:
            child_list.remove('environmental%20samples')
        # print(child_list)
        for ID in child_list:
            # print(ID)
            xml_s = entrez_search(ID, 'taxonomy', next_of_kin=True)
            data_list = data_find(xml_s, 'Id')
            for n in data_list:
                grandchild_id_list.append(n)
                print(ID, 'hey')
                rev_child_lineage[n] = ID
            print(grandchild_id_list)
            child_lineage[ID] = data_list
        if not grandchild_id_list:
            count+=1
            print("no next gen")
            # print(grandchild_id_list)
        else:
            print('next gen present')
            # print(grandchild_id_list)
        child_id_list = grandchild_id_list
        # print(child_id_list)
        child_list = []
        grandchild_id_list = []
        if count >=1:
            break
    print(rev_child_lineage)
    return child_lineage

#have to build some system that index's further in dictionary, to add new family
#

# main code
# --------------------------------------------------------------------------------------

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

user_input = input("Input taxa or taxid of interest\n")
# replaces white space with %20, so url can be searched
user_input = user_input.replace(" ", "%20")

# #get regex searchable pattern for user inputted taxon or taxid
# lineage=lineage_search(user_input)
#
# # graphical representation of lineage
# # assigned variables
# tab=""
# count=0
# #for loop through each taxa name
# for taxa in lineage:
#     #print to output
#     print(f'{tab}{taxa}')
#     if count==0:
#         tab+='+---'
#     tab='\t'+tab
#     count+=1

#
child = child_find(user_input)
print(child)

#
# #
# genomes=assembled_genome_find(user_input)
#
#
#
# # # print(lineage)
# print(f'number of assembled genomes for {user_input} is {genomes}')




