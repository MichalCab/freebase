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
    cd info
    ${_crawler_path}/others/divide.sh ${entity_type}.info
    sed -i '$s/.$//' ${entity_type}.info.parts.aa
    echo "]" >> ${entity_type}.info.parts.aa
    sed -i '$s/.$//' ${entity_type}.info.parts.ab
    echo "]" >> ${entity_type}.info.parts.ab
    sed -i '1s/^/[/' ${entity_type}.info.parts.ab
    sed -i '1s/^/[/' ${entity_type}.info.parts.ac
    cd -
    echo -e "Run generating freebase.${entity_type}s in background"
      echo ${entity_type}.info.parts.aa
      cat info/${entity_type}.info.parts.aa | python ${_crawler_path}convertJsonToColumns.py -b -t ${entity_type} > freebase/freebase.${entity_type}s.parts.aa &
      sleep 20
      echo ${entity_type}.info.parts.ab
      cat info/${entity_type}.info.parts.ab | python ${_crawler_path}convertJsonToColumns.py -b -t ${entity_type} > freebase/freebase.${entity_type}s.parts.ab &
      sleep 20
      echo ${entity_type}.info.parts.ac
      cat info/${entity_type}.info.parts.ac | python ${_crawler_path}convertJsonToColumns.py -b -t ${entity_type} > freebase/freebase.${entity_type}s.parts.ac 
    if [ $? == 1 ]
    then
      echo -e "error in script convertJsonToColumns.py"
      exit 1
    fi
    echo "Go sleep for some time"
    cat freebase/freebase.${entity_type}s.parts.ac >> freebase/freebase.${entity_type}s.parts.ab
    rm freebase/freebase.${entity_type}s.parts.ac
    cat freebase/freebase.${entity_type}s.parts.ab >> freebase/freebase.${entity_type}s.parts.aa
    rm freebase/freebase.${entity_type}s.parts.ab
    rm info/${entity_type}.info.parts.aa info/${entity_type}.info.parts.ab info/${entity_type}.info.parts.ac
    sleep 15
  fi
done

echo -e "Run generating freebase.nationalities"
####NATIONALITY STAFF
entity_type="nationalitie"
cd info
${_crawler_path}/others/divide.sh location.info
sed -i '$s/.$//' location.info.parts.aa
echo "]" >> location.info.parts.aa
sed -i '$s/.$//' location.info.parts.ab
echo "]" >> location.info.parts.ab
sed -i '1s/^/[/' location.info.parts.ab
sed -i '1s/^/[/' location.info.parts.ac
cd -
cat info/location.info.parts.aa | python ${_crawler_path}convertJsonToColumns.py -b -t nationalities > freebase/freebase.nationalities.parts.aa &
sleep 20
cat info/location.info.parts.ab | python ${_crawler_path}convertJsonToColumns.py -b -t nationalities > freebase/freebase.nationalities.parts.ab &
sleep 20
cat info/location.info.parts.ac | python ${_crawler_path}convertJsonToColumns.py -b -t nationalities > freebase/freebase.nationalities.parts.ac
cat freebase/freebase.${entity_type}s.parts.ac >> freebase/freebase.${entity_type}s.parts.ab
rm freebase/freebase.${entity_type}s.parts.ac
cat freebase/freebase.${entity_type}s.parts.ab >> freebase/freebase.${entity_type}s.parts.aa
rm freebase/freebase.${entity_type}s.parts.ab
rm info/${entity_type}.info.parts.aa info/${entity_type}.info.parts.ab info/${entity_type}.info.parts.ac
###

if [ ! -d ${_data_path}"latest" ]; then
  mkdir ${_data_path}"latest"
fi

mv info/* ${_data_path}"latest"
mv freebase/* ${_data_path}"latest"

echo -e "DONE"
