#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: taxonpathparser.py
Date: March 14th, 2022
Author: Auguste de Pennart
Description:
    This program finds number of genome assemblies for user-specified taxid or taxon
    
List of functions:
    entrez_search:
        parses NCBI database entrez search to xml
    entrez_fetch:
        parses NCBI database entrez fetch to xml
    data_find:
        populates a list with elements of interest from a xml variable
    taxon_or_taxid:
        searches database for reciprocal taxid or taxon
    lineage_search:
        creates a list of the lineage of taxon of interest from root to taxon
    lineage_visualisation:
        graphical representation of lineage
    child_find:
        while loop through each child taxa,
        adding taxa to generations dictionary
        and whether its a species to is_species dictionary
    species_find:
        find species by for looping through nested generations dictionary and creating a list of species
    assembled_genome_find:
        Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
        format for said input.

List of "non standard modules"
    No "non standard modules" are used in the program.

Procedure:
    1. get database and taxa of interest from input
    2. find taxa of interest in database
    3. run through database as a list to find parent ids from which to find lineage
    4. print lineage to standard output

Usage:
    python taxonpathfinder.py [-h] [-v] USER_INPUT [USER_INPUT ...]

known error:
    1. lineage_search and lineage_visualisation are obsolete right now, finding parent could be of use in program development
    2. does not produce an output file
    3. removes environmental samples from search, an argparse option could be available
    4. only searches assemblies, searching other population genetics information could be of use
    5. forloops through each generation, even if not needed
    6. species find could be more general, to nested dictionary pattern matcher
    7. mus is a species and genus, but just takes first instance in file
    8. heavy reliance on xpath and other dependencies without through knowledge
    9. first_data in data_find could be more efficient
    10. uncultured and environmental not removed
 """

# import modules
# ----------------------------------------------------------------------------------------
import re  # module for using regex
import argparse #module for terminal use
from urllib.request import urlopen  # module to open the url
from lxml import etree  # module to read xml files

#argparse
# ----------------------------------------------------------------------------------------
#program description
usage='This program finds number of genome assemblies for user-specified taxid or taxon'
parser=argparse.ArgumentParser(description=usage)#create an argument parser
req_arg= parser.add_argument_group(title="required arguments")
#creates the argument for program version
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 2.0')
#creates the argument where email will be inputed
req_arg.add_argument('-e', '--email',
                    metavar='EMAIL',
                    dest='email',
                    required=True,
                    help="email required to access NCBI's databases")
#creates the argument where taxon or taxid will be inputed
req_arg.add_argument('-i', '--input',
                    metavar='USER_INPUT',
                    dest='user_input',
                    nargs='+',
                    required=True,
                    help='user-specified taxid or taxon')
args=parser.parse_args()#parses command line

#functions
# ----------------------------------------------------------------------------------------

# entrez_search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # input_species:
        #user input as either taxa(word) or taxid(number)
    #database:
        #NCBI database to find input_species
    #next_of_kin:
        #finds children taxon on NCBI taxonomy database
# use:
    # parses NCBI database entrez search to xml
# return:
    # xml_s:
        # xml parsed url search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def entrez_search(input_species=None,database=None,next_of_kin=False):
    baseurl_search = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" # base url for using esearch module against NCBI databases
    if next_of_kin: #next_of_kin used for displaying children taxa with esearch, database and input species can be manipulated in query
        query = f"db={database}&term={input_species}[next%20level]&format=xml&RetMax=100000"
    else: #database and input species can be manipulated in query
        query = f"db={database}&term={input_species}&format=xml&RetMax=100000"
    url = baseurl_search + query#add to form one url
    # print(url)
    entrez_s = urlopen(url)  # opens the url with urlopen module
    entrez_s_read = entrez_s.read()  # reads the url content
    # print(entrez_s)
    xml_s = etree.XML(entrez_s_read)  # parses the content into xml format
    return xml_s

# entrez_fetch
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # input_ID:
        # user input as either taxa(word) or taxid(number)
    # database:
        # NCBI database to find input_ID
# use:
    # parses NCBI database entrez fetch to xml
# return:
    # xml_f:
        # xml parsed url search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def entrez_fetch(input_ID=None,database=None):
    # print(input_ID)
    baseurl_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" # base url for using esearch module against NCBI databases
    query = f"db={database}&id=[{input_ID}]&format=xml&RetMax=100000" #database and input species can be manipulated in query
    url = baseurl_fetch + query #add to form one url
    entrez = urlopen(url)  # opens the url with urlopen module
    entrez_read = entrez.read()  # reads the url content
    xml_f = etree.XML(entrez_read)  # parses the content into xml format
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
    # populates a list with elemt of interest from a xml variable
# return:
    # data_list:
        #pattern_match(es) from xml variable
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def data_find(xml=None,pattern_search=None,tree_build=False,first_data=False):
    data_list=[] #assigned list for pattern matches
    original=False #flag for determining user inputted taxon/taxid
    pattern_match = xml.xpath(f"//{pattern_search}")  # search for all matches
    for match in pattern_match: #for loop through pattern_match to convert all elements into text format
        # print(match.text)
        if tree_build:#for lineage list, hold onto user inputted taxon/taxid for appending at end
            original = match.text #user inputted taxon/taxid
            tree_build = False #remaining lineage elements added as appears xml file
        elif not tree_build:
            # print (match.text)
            data_list.append(match.text) # adds taxon to lineage list
            # print(data_list)
    if original: #appends user inputted taxon/taxid to end of list
        data_list.append(original)
        # print('original specified') #prints to standard output that lineage being created
    if first_data:# pulls out only first element of data_list to be returned
        data_list = data_list[0]
        data_list = '\"'+ data_list.replace(" ", "%20") + '\"' # replaces white space with %20 and adds double quotes, so url can be searched
    return data_list

# taxon_or_taxid
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # user_input:
        #user input, as list, of either taxa(word) or taxid(number)
# use:
    # searches database for reciprocal taxid or taxon
# return:
    # species:
        # scientific name of taxon
    # ID:
        # taxid for taxon
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def taxon_or_taxid(user_input=None):
    species_ID = "" #string variable to be changed to from lost
    for n, element in enumerate(user_input):#changes datatype from list to string
        if n != 0: #adds space between elements in string variable
            species_ID+=' ' + element
        elif n == 0:
            species_ID=element
    # print(species_ID)
    try:  # raises exception if inputted taxon/taxid not in database
        if re.search('^[\d]+$', species_ID):  # checks if user input is an ID
            ID=species_ID #change user input to ID
            xml_f = entrez_fetch(species_ID, 'taxonomy') #create xml of taxid from taxonomy database
            species = data_find(xml_f, 'ScientificName',first_data=True) #find taxon name for user input
        elif not re.search('^[\d]+$', species_ID): # checks if user input is a taxon
            species_ID = '\"'+ species_ID.replace(" ", "%20") + '\"' ## replaces white space with %20, and adds double quotes so url can be searched
            species=species_ID #changes user input to taxon
            # print(species)
            xml_s = entrez_search(species_ID, 'taxonomy') #create xml of taxon from taxonomy database
            ID = data_find(xml_s, 'Id',first_data=True) #find taxid for user input
        test=species[0]+ ID[0] #checks whether taxon/taxid in database
    except IndexError: # prints to standard output that taxon or taxid inputted was not found in database
        print(f'''{species_ID.replace("%20", " ").replace('"', "")} not found in NCBI taxonomy database or misspelled, please try again''')
        exit() # exits script
    return species, ID

# lineage_search
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # user_input:
        #user input, as list, of either taxa(word) or taxid(number)
# use:
    # creates a list of the lineage of taxon of interest from root to taxon
# return:
    # lineage:
        # lineage of taxon as list
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lineage_search(user_input=None):
    user_input=taxon_or_taxid(user_input) # searches database for reciprocal taxid or taxon
    xml_f=entrez_fetch(user_input[1],'taxonomy') #create xml of taxid from taxonomy database
    lineage=data_find(xml_f,'ScientificName', tree_build=True) #creates list of all taxon in lineage for taxid
    return lineage

# lineage_visualisation
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # lineage:
        # lineage of taxon as list
# use:
    # graphical representation of lineage
# return:
    # no return
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lineage_visualisation(lineage=None):
    tab="" # tab variable
    count=0 # counter
    for taxa in lineage: #for loop through each taxa name
        print(f'{tab}{taxa}') #prints to standard output
        if count==0: #root taxon no tab added
            tab+='+---'
        tab='\t'+tab #subsequent taxon, tabs added
        count+=1 #adds 1 to counter

# child_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    #user_input:
        # user input, as list, of either taxa(word) or taxid(number)
# use:
    #while loop through each child taxa,
    #adding taxa to generations dictionary
    # and whether its a species to is_species dictionary
# return:
    # generations:
        # nested dictionary of each generation through while loop
        #with nested dictionary having taxon name and respective child taxids
    #is_species:
        #dictionary of taxon name and taxonomic rank
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def child_find(user_input=None):
    count =0 #last child taxon counter
    counter = 0 #generation counter
    child_list=[] #list of children taxa
    grandchild_id_list=[] #list of grandchildren taxids
    child_lineage={} #dictionary of taxon and its children taxids
    generations = {} #dictionary of generation and nested child_lineage dictionary
    is_species = {} #dictionary of taxon and taxonomic rank
    user_input = taxon_or_taxid(user_input) # searches database for reciprocal taxid or taxon
    child_id_list=[user_input[1]] #pulls out taxid into a list
    # print(user_input)
    # #fix this
    # if species_limit == '"species"':
    #     count += 1
    while 1: #while loop that breaks when no next children taxa exists
        for ID in child_id_list: #for every taxid
            xml_f = entrez_fetch(ID, 'taxonomy') #create xml of taxid from taxonomy database
            taxon = data_find(xml_f, 'ScientificName',first_data=True) #finds taxon from xml
            species_limit = data_find(xml_f, 'Rank',first_data=True) #finds taxonomic rank from xml
            #prints to standard output taxon and taxonomic rank
            print(f'''{taxon.replace("%20", " ").replace('"', "")} is of rank {species_limit.replace("%20", " ").replace('"', "")}''')
            child_list.append(taxon) #adds taxon to taxon list, which will be for looping through later to determine taxids
            is_species[taxon]=species_limit #adds taxon and taxonomic rank to is_species dictionary
        #fix this too
        if '"environmental%20samples"' in child_list: #does not loop through environmental samples
            child_list.remove('"environmental%20samples"')
        # print(child_list)
        for ID in child_list: #for loop through all newly determined taxons to pull out taxids
            # print(ID)
            xml_s = entrez_search(ID, 'taxonomy', next_of_kin=True) #create xml of next of kin taxids from taxonomy database
            data_list = data_find(xml_s, 'Id') #finds taxid from xml
            #is this needed
            for n in data_list: #creates new list with children taxids
                grandchild_id_list.append(n)
                # print(ID)
            child_lineage[ID] = data_list #adds id and all children taxids to child lineage dictionary
        if not grandchild_id_list: #if grandchild_id_list empty while loop breaks
            count+=1
        print(f'found {len(grandchild_id_list)} children taxon') #prints to standard output how many taxa in next generation
        child_id_list = grandchild_id_list #change variable names in preparation for next while loop
        # print(child_id_list)
        generations[counter] = child_lineage #child_lineage added to generations dictionary along with current generation
        child_list = [] #reset child_list
        grandchild_id_list = [] #reset grandchild_list
        child_lineage={} #reset child_lineage
        counter += 1 #set up next generation number
        if count >=1: #break if no next generation
            break
    return generations, is_species

# species_find change to dictionary searcher
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # generations:
        # nested dictionary of each generation through while loop
        # with nested dictionary having taxon name and respective child taxids
    # is_species:
        # dictionary of taxon name and taxonomic rank
# use:
    #find species by for looping through nested generations dictionary and creating a list of species
# return:
    # species_list:
        # list of user specificied species
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def species_find(generations=None,is_species=None):
    species_list=[]  #preparing list of species
    for generation, species in generations.items(): #open up generations dictionary
        for name, id in species.items(): #open nested dictionary child_lineage
            # print(name,id)
            if is_species[name]== '\"'+'species'+'\"': #pull out species from child_lineage dictionary
                species_list.append(name) #add to list
    #print(species_list)
    return species_list

# assembled_genome_find
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# input variables:
    # species_list:
        # list of species of interest to user
# use:
    # Takes user input as either taxa(word) or taxid(number) and creates a regex searchable
    # format for said input.
# return:
# user_input:
# user input when prompted to input taxa or taxid
# input_pattern:
# taxon or taxid in regex searchable format
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def assembled_genome_find(species_list=None):
    for species in species_list: #for loop through species
        list_species=[species]
        # print(species)
        # species_ID=taxon_or_taxid(list_species)
        # print(species_ID)
        xml_s=entrez_search(species,'assembly') #create xml of genome assembly ids from asembly database
        # xml_s=entrez_search(species_ID[0],'assembly')
        genomes=data_find(xml_s,'Id') #pull out genomes
        # print(xml_s)
        # print(f"""number of assembled genomes for {species_ID[0].replace('%20', ' ').replace('"', "")} is {len(genomes)}""")
        #print to standard output species and number of genomes
        print(f"""number of assembled genomes for {species.replace('%20', ' ').replace('"', "")} is {len(genomes)}""")
    return genomes

# main code
# --------------------------------------------------------------------------------------
#two dictionaries created from child_find function
output = child_find(args.user_input)
# print(is_species)
#dictionaries looped through to output species_list
species_list=species_find(output[0],output[1])
#number of assembled genomes printed out for each species
genomes = assembled_genome_find(species_list)
# print(genomes)
