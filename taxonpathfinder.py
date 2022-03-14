#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: taxonpathparser.py
Date: March 13th, 2022
Author: Auguste de Pennart
Description:
    Finds taxon path from taxid or taxon
List of functions:
    entrez_search:

    entrez_fetch:

    data_find:

    taxon_or_taxid:

    lineage_search:

    assembled_genome_find:

    child_find:

List of "non standard modules"
    No "non standard modules" are used in the program.
Procedure:
    1. get database and taxa of interest from input
    2. find taxa of interest in database
    3. run through database as a list to find parent ids from which to find lineage
    4. print lineage to standard output
Usage:
    python taxonpathfinder.py
known error:
    2. lineage is obsolete right now, hopefully can get parent taxa not genome assembled
    4. does not work with output file request
 """

# import modules
# ----------------------------------------------------------------------------------------
import re  # module for using regex
import sys  # module for using terminal
from pathlib import Path  # module for verifying file path
from urllib.request import urlopen  # module to open the url
from lxml import etree  # module to read xml files
# ----------------------------------------------------------------------------------------
#functions
# ----------------------------------------------------------------------------------------
# entrez_search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # user_input:
        #user input as either taxa(word) or taxid(number)
    #database:
        #NCBI database to find user_input
    #next_of_kin:
        #finds children taxon on NCBI taxonomy database

# use:
    #

# return:
    # xml_s:
        # xml parsed url search

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def entrez_search(user_input=None,database=None,next_of_kin=False):
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
        # print('entrez_search returned empty')
        pass
    else:
        # print('successful entrez_search')
        pass
    return xml_s


# entrez_fetch
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # user_input:
        # user input as either taxa(word) or taxid(number)
    # database:
        # NCBI database to find user_input

# use:
    #

# return:
    # xml_f:
        # xml parsed url search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
        # print('entrez_fetch returned empty')
        pass
    else:
        # print('successful entrez_fetch')
        pass
    return xml_f

# data_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # xml:
        #parsed xml variable
    #pattern_search:
        # element of xml variable of interest
    #tree_build:
        #builds lineage for taxon of interest
    #first_data:
        # pulls out first instance of pattern_search

# use:
    #

# return:
    # data_list:
        #pattern_match(es) from xml variable
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def data_find(xml=None,pattern_search=None,tree_build=False,first_data=False):
    #
    data_list=[]
    #
    original=False
    #
    pattern_match = xml.xpath(f"//{pattern_search}")  # search for all tags
    # with given xpath
    # this is using eran's stuff, could technically new line each value and get what i want(i think)
    #what about if there is only one match?
    for match in pattern_match:
        # print(match.text)
        if tree_build:
            # create original, variable for input taxon
            original = match.text
            tree_build = False
        elif not tree_build:
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
    if first_data:
        data_list = data_list[0]
        data_list = data_list.replace(" ", "%20")
        data_list = '\"' + data_list + '\"'
    elif not first_data:
        pass
    return data_list

# taxon_or_taxid
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # user_input:
        #

# use:
    #

# return:
    # species:
        #
    # ID:
        #
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def taxon_or_taxid(user_input=None):
    # checks whether user input is taxon or taxid
    try:
        # checks if user input is an integer
        if int(user_input):
            ID=user_input
            xml_f = entrez_fetch(user_input, 'taxonomy')
            species = data_find(xml_f, 'ScientificName',first_data=True)
    # if user input is not an integer the ValueError is raised
    except ValueError:
        species=user_input
        xml_s = entrez_search(user_input, 'taxonomy')
        ID = data_find(xml_s, 'Id')
    try:
        test=species[0]+ ID[0]
    except IndexError:
        # prints to standard output that taxon or taxid inputted was not found in database
        print("taxid not found in NCBI taxonomy database or misspelled, please try again")
        # exits script
        exit()
    # returns whether id_flag is True or False
    return species, ID


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
def lineage_search(user_input=None):
    user_input=taxon_or_taxid(user_input)
    #database specified to taxonomy
    xml_f=entrez_fetch(user_input[1],'taxonomy')
    lineage=data_find(xml_f,'ScientificName', tree_build=True)
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
    user_input=taxon_or_taxid(user_input)
    xml_s=entrez_search(user_input[0],'assembly')
    genomes=data_find(xml_s,'Id')
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
    counter = 0
    child_list=[]
    grandchild_id_list=[]
    child_lineage={}
    generations = {}
    is_species = {}
    #
    user_input = taxon_or_taxid(user_input)
    # database specified to taxonomy
    xml_f = entrez_fetch(user_input[1], 'taxonomy')
    taxon = data_find(xml_f, 'ScientificName',first_data=True)
    species_limit = data_find(xml_f, 'Rank',first_data=True)
    is_species[taxon] = species_limit
    print(f'{taxon.replace("%20", " ")} is  of rank {species_limit}')
    #maybe not needed
    if species_limit == 'species':
        count += 1
    xml_s = entrez_search(taxon, 'taxonomy',next_of_kin=True)
    child_id_list = data_find(xml_s, 'Id')
    child_lineage[taxon] = child_id_list
    generations[counter] = child_lineage
    counter+=1
    child_lineage = {}
    if count ==0 :
        while 1:
            for ID in child_id_list:
                # database specified to taxonomy
                xml_f = entrez_fetch(ID, 'taxonomy')
                taxon = data_find(xml_f, 'ScientificName',first_data=True)
                species_limit = data_find(xml_f, 'Rank',first_data=True)
                print(f'{taxon.replace("%20", " ")} is  of rank {species_limit}')
                child_list.append(taxon)
                is_species[taxon]=species_limit
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
                    # print(ID)
                child_lineage[ID] = data_list
            if not grandchild_id_list:
                count+=1
                print("no next gen")
            else:
                print('next gen present')
            print(f'found {len(grandchild_id_list)} children taxon')
            child_id_list = grandchild_id_list
            # print(child_id_list)
            generations[counter] = child_lineage
            child_list = []
            grandchild_id_list = []
            child_lineage={}
            counter += 1
            if count >=1:
                break
    return generations, is_species

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

email = 'adepennart@gmail.com'
# email = input("Input email for NCBI database access\n")
user_input = input("Input taxa or taxid of interest\n")
# replaces white space with %20, so url can be searched
user_input = user_input.replace(" ", "%20")
user_input = '\"'+ user_input + '\"'

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
output = child_find(user_input)
generations=output[0]
is_species=output[1]
# print(is_species)
# print(child[len(child)-1])
for generation, species in generations.items():
    #could coome up with a way to not forloop through each generation if not needed
    for name, id in species.items():
        # print(name)
        # if is_species[name]== 'species':
        if is_species[name] == '\"'+'species'+'\"':
            genomes = assembled_genome_find(name)
            name=name.replace('%20', ' ')
            print(f'number of assembled genomes for {name} is {genomes}')
        else:
            pass




