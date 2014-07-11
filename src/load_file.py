#!/bin/env python
#-*- coding: utf-8 -*-
# python 2.7

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

def load_file(fname):
  with open(fname) as f:
    content = f.read().splitlines()
  return content

