#!/usr/bin/env python3.4
#-*- coding: utf-8 -*-

from datetime import datetime
from bisect import bisect_left

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

class FixedData(object):
  def __init__(self, input, col_sep="\t", finding_column=0, return_column=1):
    self.fixed_data = []
    self.return_column = return_column
    if isinstance(input, str):
      for line in open(input, 'r'):
        splited = line.split(col_sep)
        self.fixed_data.append((splited[0], splited[1].strip()))
    else:
      for e in input:
        self.fixed_data.append((e.freebase_id, e.wikipedia_key))

    self.fixed_data.sort(key=lambda r: r[finding_column])
    self.keys = tuple([r[finding_column] for r in self.fixed_data])

  def index(self, x):
    i = bisect_left(self.keys, x)
    if i != len(self.keys) and self.keys[i] == x:
      return i
    return None

  def search(self, x):
    index = self.index(x)
    if index is not None:
      return self.fixed_data[self.index(x)][self.return_column]
    return None


if __name__ == "__main__":
  fd = FixedData('id_wikikey.tsv')
  url = fd.search('01063t')

"""
  start = datetime.now()
  for i in range(600000):
    res = fd.search('01063t')

  print(datetime.now() - start)
  print(res)
"""
