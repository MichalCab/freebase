#!/bin/env python
#-*- coding: utf-8 -*-

import fileinput
import urllib
import os
import os.path
import sys
import getopt
import json
import argparse
import gzip
import time
import urllib

from binary_search import *
#from fixed_data import FixedData
from load_file import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_file_with_redirection = "/mnt/minerva1/nlp/projects/decipher_freebase/crawler/help/wikipedia-redirects.tsv"

def remove_redirections(data):
  redirections = [] 
  redirections0 = []
  original_redirections = load_file(global_file_with_redirection)

  for r in original_redirections:
    red_array = r.split("\t")
    redirection_names = red_array[1].split("|")
    for rn in redirection_names:
      redirections.append("%s\t%s" % (rn.strip(), red_array[0]))
      redirections.append("%s\t%s" % (rn.strip().lower(), red_array[0]))
      redirections0.append(red_array[0])

  redirections0.sort()
  redirections.sort()

  original_redirections[:] = []
      
  for d in data:
    if d.wikipedia_url.strip() == "":
      continue
    not_redirection = binary_search(redirections0, d.wikipedia_url)
    if not_redirection is -1:
      wiki_key = d.wikipedia_url.replace("http://en.wikipedia.org/wiki/", "").replace("_", "")
      final_url = binary_search(redirections, wiki_key, cross_columns=True, col_sep="\t", finding_column=0, return_column=1)
      if final_url is not -1:
        d.wikipedia_url = final_url
        return
      wiki_key = d.wikipedia_url.replace("http://en.wikipedia.org/wiki/", "").replace("_", "").lower()
      final_url = binary_search(redirections, wiki_key, cross_columns=True, col_sep="\t", finding_column=0, return_column=1)
      if final_url is not -1:
        d.wikipedia_url = final_url
        return

