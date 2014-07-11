#!/bin/env python
#-*- coding: utf-8 -*-

import fileinput
import os
import os.path
import sys 
import gzip
import time
import urllib
import time
import json

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"
global_gzip_filename = "freebase-rdf.gz"

def remove_language_tags(string):
  return string.replace('@en', '')

def get_wikipedia_url(_wikipedia_url):
  result = ""
  _wikipedia_url = _wikipedia_url.replace("$","\u")
  _wikipedia_url = json.loads('"{0}"'.format(_wikipedia_url)).encode("utf-8")
  if _wikipedia_url:
    result = urllib.unquote(_wikipedia_url)
  return result

def print_freebase_list():
  old_item_id = ""
  item_id = ""
  fb_id = 0
  wiki_url = 0
  
  start_time = time.time()
  with gzip.open(global_gzip_filename, 'r') as infile:
    for line in infile:
      if not line.startswith("<http://rdf.freebase.com/ns/m."):
        continue

      splited_line = line.split('\t')

      #save part of results to file

      old_item_id = item_id
      item_id = splited_line[0]

      if old_item_id != item_id:
        if wiki_url and fb_id:
          print "%s\t%s" % (fb_id, wiki_url)
        wiki_url = ""
        fb_id = ""
        fb_id = item_id.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
          
      if splited_line[1] == "<http://rdf.freebase.com/key/key.wikipedia.en_title>":
        value = str(splited_line[2]).replace('"', '')
        value = value.replace("%13", "–")
        value = remove_language_tags(value)
        if "%" in value:
          try:
           value = urllib.unquote(value).decode('cp1250')
          except:
            pass
        wiki_url = get_wikipedia_url(value)

if __name__ == "__main__":
  print_freebase_list()
