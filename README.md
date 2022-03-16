
mkdir Population_genetics
cd Population_genetics/
conda create -n population_genetics
conda activate population_genetics

#run python script
python taxonpathfinder.py taxonomy.dat

pip install biopython
pip install xml2dict

#actually use this module
pip install entrezpy
#used this for examples for fecth
https://gitlab.com/ncbipy/entrezpy/-/blob/master/examples/entrezpy-example.efetch.py

#or is it this
pip install lxml

find species
not there?
find genus? *and so forth) till found
pull out first or all species present

then pull out number of genomes or genes

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=taxonomy&term=Homosapiens

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=taxonomy&id=9606&format=xml
=======
