#!/bin/env python
#-*- coding: utf-8 -*-

import sys

from binary_search import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_source_of_alternate_names = "/mnt/minerva1/nlp/projects/decipher_freebase/crawler/help/wikipedia-redirects-filtered.tsv"
global_array_separator = "|"

def load_file(fname):
  with open(fname) as f:
    content = f.read().splitlines()
  return content

def add_alternative_by_wiki(freebase):
  original_alternatives = load_file(global_source_of_alternate_names)

  alternatives = []

  for a in original_alternatives:
    a_array = a.split("\t")
    alternatives.append("%s\t%s" % (a_array[0], a_array[1]))

  alternatives.sort()

  for f in freebase:
    alt_ames = binary_search(alternatives, f.wikipedia_url, cross_columns=True, col_sep="\t")

    if alt_ames and alt_ames is not -1:
      new = alt_ames.split(global_array_separator)

      for n in new:
        if n.strip() and n not in f.alias:
          f.alias.append(n)
