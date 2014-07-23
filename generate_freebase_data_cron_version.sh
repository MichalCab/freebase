#!/bin/bash
#Author: Michal Cab <xcabmi00@stud.fit.vutbr.cz>

#_now=$(date +"%d-%m-%Y")
_now="latest"
_path="/mnt/minerva1/nlp/projects/decipher_freebase/"
_crawler_path=${_path}"crawler/"
_data_path=${_path}"data/"

#init variables
file="freebase-rdf.gz"
entity_types=( artist art_period_movement artwork visual_art_form visual_art_genre visual_art_medium event museum person location )

#make folder
mkdir ${_crawler_path}${_now} 2>/dev/null
cd ${_crawler_path}${_now}

# check if need to download freebase dump
echo -e "Downloading freebase-rdf.gz from http://download.freebaseapps.com... "
pre_size=`du $file 2>/dev/null`
mv freebase-rdf.gz index.html
wget -N http://download.freebaseapps.com #cant use -N with -O (do not know why)
mv index.html freebase-rdf.gz
past_size=`du $file 2>/dev/null`
if [ "$past_size" == "$pre_size" ]
then
  #no changes
  echo -e "no changes"
  exit 0
fi
echo -e "freebase-rdf.gz downloaded"

#control dump
if [ ! -r "${file}" ]
then
	echo "ERROR: File $file have not right format or doesn't exist" 2>&1
	exit 1
fi

#make dirs
if [ ! -d "ids" ]; then
  mkdir ids
fi
if [ ! -d "info" ]; then
  mkdir info
fi
if [ ! -d "help" ]; then
  mkdir help
fi
if [ ! -d "freebase" ]; then
  mkdir freebase
fi

# generate help files to help folder
echo -e "Generating ids files and labels file... "
python ${_crawler_path}convertFreebaseDumpToDic.py -t ids --dump-loc ${file}
if [ $? == 1 ]
then
  echo "error in script convertFreebaseDumpToDic.py -t ids"
  exit 1
fi
echo -e "Ids files and labels files are ready"
echo -e "Generating .info files ..."
for entity_type in "${entity_types[@]}"
do
  if [ -r ids/${entity_type}s_ids ]
  then
    cat ids/${entity_type}s_ids | python ${_crawler_path}convertFreebaseDumpToDic.py -t ${entity_type} --dump-loc ${file} > info/${entity_type}.info
    if [ $? == 1 ]
    then
      echo "error in script convertFreebaseDumpToDic.py"
      exit 1
    fi
  fi
done
echo -e "Info files are ready"

for entity_type in "${entity_types[@]}"
do
  if [ -r info/${entity_type}.info ]
  then
    echo -e "Run generating freebase.${entity_type}s in background"
    cat info/${entity_type}.info | python ${_crawler_path}convertJsonToColumns.py -b -t ${entity_type} > freebase/freebase.${entity_type}s &
    if [ $? == 1 ]
    then
      echo -e "error in script convertJsonToColumns.py"
      exit 1
    fi
    echo "Go sleep for 15s"
    sleep 20
  fi
done
echo -e "Run generating freebase.nationalities"
cat info/location.info | python ${_crawler_path}convertJsonToColumns.py -b -t nationalities > freebase/freebase.nationalities

if [ ! -d {$_data_path}"latest" ]; then
  mkdir {$_data_path}"latest"
fi

mv info/* {$_data_path}"latest"
mv freebase/* {$_data_path}"latest"

echo -e "DONE"
