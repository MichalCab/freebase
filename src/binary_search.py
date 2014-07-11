#!/bin/env python
#-*- coding: utf-8 -*-

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

def binary_search(a, x, lo=0, hi=None, cross_columns=False, col_sep=" ", finding_column=0, return_column=1):
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = (lo+hi)//2
    midval = a[mid]
    if cross_columns:
      splited_line = midval.split(col_sep)
      midval = splited_line[finding_column].replace("\t", "").replace("\n", "")
      #print ":%s:%s:" % (midval, x)
    if midval < x:
      lo = mid + 1
    elif midval > x:
      hi = mid
    else:
      if cross_columns:
        return splited_line[return_column]
      return mid
  return -1

