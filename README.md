
mkdir Population_genetics
cd Population_genetics/
conda create -n population_genetics
conda activate population_genetics

#run python script
python taxonpathfinder.py taxonomy.dat
