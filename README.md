# Installation
This program can be directly installed from github. (green code button, top right)

## environment
Due to the software versions of python and the application's dependencies, creating a conda enviroment will be most useful.

If you have conda skip, otherwise refer to online resources on how to install conda.

Once installed, we can make a conda environment

```bash=
conda create -n population_genetics
conda activate population_genetics
```
change directories into created NCBI_Taxon_Genome_Link-master directory 
```bash=
cd NCBI_Taxon_Genome_Link-master
```
## Python version

The python version for running this script is python=3.9.9

```bash=
conda install python=3.9.9
```

## Dependencies
The script runs with python depencies, lxml\==4.8.0 and urllib3\==1.26.8.

If not already installed, they can be isntalled as such.
```bash=
pip install lxml==4.8.0
pip install urllib3==1.26.8
```

The script should be all ready to run.

# Usage
## input

The code can be run as follows
```bash=
python NCBI_Taxon_Genome_link.py [-h] [-v] [-s] -e EMAIL -i USER_INPUT [USER_INPUT ...] [-o OUTPUT]

```

The help page can be accessed with the -h or --help flag
```bash=
python NCBI_Taxon_Genome_link.py -h
python NCBI_Taxon_Genome_link.py --help
```

The program version can be accessed with the -v or --version flag
```bash=
python NCBI_Taxon_Genome_link.py -v
python NCBI_Taxon_Genome_link.py --version
```

There are two required fields for running  NCBI_Taxon_Genome_link.py, EMAIL and USER_INPUT. 
Email is required for accessing NCBI's databases remotely.
USER_INPUT is your taxon/TaxID of interest.
Both can be typed out directly on the terminal.

```bash=
python NCBI_Taxon_Genome_link.py -e EMAIL -i USER_INPUT
```

There are two optional fields, SUB_SPECIES and OUTPUT.

The SUB_SPECIES tag does not take any input.
```bash=
python NCBI_Taxon_Genome_link.py -e EMAIL -i USER_INPUT -s
```

The OUTPUT tag takes a desired output file name

```bash=
python NCBI_Taxon_Genome_link.py -e EMAIL -i USER_INPUT -o assembled_genomes.txt
```


## example inputs
Various ways of searching for humans.

With scientific species name.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i Homo sapiens
```

With TaxID.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i 9606
```

With common name.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i human
```


With taxonomic rank family.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i Hominidae
```

## output
The number of assembled genomes are printed directly out to the standard output. However, specifying the output flag, prints the species and assembled genomes to an output file.

an example output for Homo sapiens without outputfile.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i Homo sapiens
#Homo sapiens is of rank species
#found 0 children taxon
#number of assembled genomes for Homo sapiens is 1220
```

an example output for Homo sapiens with outputfile.
```bash=
python NCBI_Taxon_Genome_link.py -e researcher@fake_email.com -i Homo sapiens -o example_outputfile.txt
#Homo sapiens is of rank species
#found 0 children taxon
#number of assembled genomes for Homo sapiens is 1220
```
refer to example_outputfile.txt in folder for format.
