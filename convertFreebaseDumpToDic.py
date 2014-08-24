#!/usr/bin/env python
#-*- coding: utf-8 -*-
# file convertFreebaseDumpToDic.py

#import cProfile
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
import time
from threading import Thread
import multiprocessing
import random
import re
from time import sleep
from pprint import pprint

from src.binary_search import *
from src.load_file import *
from src.generate_help_files import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_number_when_write_to_file = 8000
global_gzip_filename = "freebase-rdf.gz"
global_api_key = "AIzaSyDnuCxpjjO9Tjz-ONcYfYBB0sjNw42Xu1I"

global_labels = []
global_latitudes = []
global_longitudes = []
global_height_meters = []
global_width_meters = []
global_depth_meters = []
global_citytowns = []
global_countries = []
global_postal_codes = []
global_state_province_regions = []
global_numbers = []
global_locations = []
global_owners = []
global_artwork_location_relationship = []


def load_from_stdin():
  content = sys.stdin.read().splitlines()
  return content

def convert_rdf_to_dic(ids, data_type):
  item = {}
  data = {}
  old_item_id = ""
  item_id = ""
  find_index = -1
  results = []
  
  a = 0

  print "["

  start_time = time.time()
  with gzip.open(global_gzip_filename, 'r') as infile:
    for line in infile:
      
      if not line.startswith("<http://rdf.freebase.com/ns/m."):
        continue

      splited_line = line.split('\t')

      #save part of results to file
      if len(results) >= 100000:
        print_data(results, data_type)

      old_item_id = item_id
      item_id = splited_line[0]
      # if next entity --> save previous entity and clear saving array for new entity
      if old_item_id != item_id:
        #determinate if this id is connect with entity witch we want to extract
        find_index = binary_search(ids, item_id)

        if data_type == "all":
          find_index = 1

        if find_index != -1:
          if len(data) is not 0 and "name" in data:
            item["itemInfo"] = data
            results.append(json.dumps(item, separators=(',',':')))
          item.clear()
          data.clear()
          data["id"] = item_id.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]

      if find_index != -1:
        #bind all thinks starting with actual id (item_id)
        determine_content(splited_line, data, data_type)

  print_data(results, data_type)
  print "{\"itemInfo\":{}}]"

def print_data(_data, data_type):
  for d in _data:
    print "%s," % d
  _data[:] = []

def determine_content(splited_line, data, data_type):
  bind("<http://rdf.freebase.com/ns/type.object.type>", "object_type", 
       splited_line, data, 
       is_foreign_key=False)
  bind_language_data("<http://rdf.freebase.com/ns/type.object.name>", "name", 
                   splited_line, data, 
                   save_like_array=False)
  bind_language_data("<http://rdf.freebase.com/ns/common.topic.description>", "description", 
                   splited_line, data, 
                   save_like_array=False)
  bind_language_data("<http://rdf.freebase.com/ns/common.topic.alias>", "alias", 
                   splited_line, data)
  bind("<http://rdf.freebase.com/ns/common.topic.article>", "article", 
       splited_line, data, 
       is_foreign_key=True, save_like_array=False)
  bind("<http://rdf.freebase.com/key/wikipedia.en_title>", "key_wikipedia_en", 
       splited_line, data, 
       is_foreign_key=False, save_like_array=False)

  if (data_type == "person" or data_type == "artist"):
    bind("<http://rdf.freebase.com/ns/influence.influence_node.influenced_by>", "influenced_by",
         splited_line, data, 
         save_id=True)
    bind("<http://rdf.freebase.com/ns/influence.influence_node.influenced>", "influenced",
         splited_line, data, 
         save_id=True)
    bind("<http://rdf.freebase.com/ns/people.person.gender>", "gender",
         splited_line, data,
         save_like_array=False, only_first_letter=True)
    bind("<http://rdf.freebase.com/ns/visual_art.visual_artist.artworks>", "artworks",
         splited_line, data,
         save_id=True)
    bind("<http://rdf.freebase.com/ns/people.person.profession>", "profession", 
         splited_line, data, 
         is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/people.person.places_lived>", "places_lived", 
         splited_line, data, 
         save_id=True, is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/visual_art.visual_artist.associated_periods_or_movements>", "associated_periods_or_movements", 
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/people.person.nationality>", "nationality",
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/visual_art.visual_artist.art_forms>", "art_forms",
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/people.person.place_of_birth>", "place_of_birth",
         splited_line, data,
         save_id=True, save_like_array=False)
    bind("<http://rdf.freebase.com/ns/people.deceased_person.place_of_death>", "place_of_death", 
         splited_line, data,
         save_id=True, save_like_array=False)
    bind("<http://rdf.freebase.com/ns/people.deceased_person.date_of_death>", "date_of_death",
         splited_line, data,
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/people.person.date_of_birth>", "date_of_birth",
         splited_line, data,
         save_like_array=False, is_foreign_key=False)
    
  elif (data_type == "artwork"):
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.period_or_movement>", "period_or_movement", 
         splited_line, data, 
         save_like_array=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.date_begun>", "date_begun", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.date_completed>", "date_completed", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.artist>", "artist", 
         splited_line, data, 
         save_id=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.media>", "media", 
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.support>", "support", 
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.dimensions_meters>", "width", 
         splited_line, data, 
         group_name="dimensions", is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.dimensions_meters>", "depth", 
         splited_line, data, 
         group_name="dimensions", is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.dimensions_meters>", "height", 
         splited_line, data, 
         group_name="dimensions", is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.art_subject>", "art_subject", 
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.art_form>", "art_form", 
         splited_line, data, 
         save_like_array=False)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.art_genre>", "art_genre", 
         splited_line, data)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.owners>", "owner", 
         splited_line, data, 
         is_foreign_key=True, save_id=True)
    bind("<http://rdf.freebase.com/ns/visual_art.artwork.locations>", "location", 
         splited_line, data, 
         is_foreign_key=True, save_id=True)
    
  elif (data_type == "location"):
    bind("<http://rdf.freebase.com/ns/base.biblioness.bibs_location.country>", "country", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=True, save_id=True)
    bind("<http://rdf.freebase.com/ns/location.location.geolocation>", "longitude", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/location.location.geolocation>", "latitude", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=True)
    bind_language_data("<http://rdf.freebase.com/ns/base.biblioness.bibs_location.loc_type>", "loc_type", 
                     splited_line, data, 
                     save_like_array=False)
    bind_language_data("<http://rdf.freebase.com/ns/location.location.adjectival_form>", "adjectival_form", 
                     splited_line, data)
    bind("<http://rdf.freebase.com/ns/location.statistical_region.population>", "population", 
         splited_line, data,
         is_foreign_key=True)
    
  elif (data_type == "museum"):
    bind("<http://rdf.freebase.com/ns/architecture.museum.type_of_museum>", "type_of_museum", 
         splited_line, data, 
         is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/architecture.museum.established>", "established", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/architecture.museum.director>", "director", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=True, save_id=True)
    bind("<http://rdf.freebase.com/ns/architecture.museum.visitors>", "visitors", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/architecture.museum.address>", "citytown", 
         splited_line, data, 
         is_foreign_key=True, group_name="address", save_id=True)
    bind("<http://rdf.freebase.com/ns/architecture.museum.address>", "postal_code", 
         splited_line, data, 
         is_foreign_key=True, group_name="address")
    bind("<http://rdf.freebase.com/ns/architecture.museum.address>", "state_province_region", 
         splited_line, data, 
         is_foreign_key=True, group_name="address")
    bind("<http://rdf.freebase.com/ns/location.location.street_address>", "street_address", 
         splited_line, data, 
         is_foreign_key=True, group_name="address")
    
  elif (data_type == "event"):
    bind("<http://rdf.freebase.com/ns/time.event.start_date>", "start_date", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/time.event.end_date>", "end_date", 
         splited_line, data, 
         save_like_array=False, is_foreign_key=False)
    bind("<http://rdf.freebase.com/ns/time.event.locations>", "locations", 
         splited_line, data, 
         save_id=True, is_foreign_key=True)
    bind("<http://rdf.freebase.com/ns/common.topic.notable_types>", "notable_types", 
         splited_line, data, 
         is_foreign_key=True, save_like_array=False)
  
  bind_image(splited_line, data, data_type)

def remove_language_tags(string):
  return string.replace('@en', '')

def search_in_labels(label_id):
  return binary_search(global_labels, label_id, cross_columns=True, col_sep="\t")

def bind(
    original_key, key, splited_line, data, save_id=False, 
    save_like_array=True, only_first_letter=False, is_foreign_key=True,
    group_name=None, language_data=False):

  if splited_line[1] != original_key:
    return
    
  FK = splited_line[2]
  
  FK = str(FK).replace('"', '')
  if group_name is not None:
    if group_name not in data:
      data[group_name] = []
    if is_foreign_key:
      FK = FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
      if key == "height":
        FK = binary_search(global_height_meters, FK, cross_columns=True, col_sep="\t")
      elif key == "width":
        FK = binary_search(global_width_meters, FK, cross_columns=True, col_sep="\t")
      elif key == "depth":
        FK = binary_search(global_depth_meters, FK, cross_columns=True, col_sep="\t")
      elif key == "citytown":
        next_FK = binary_search(global_citytowns, FK, cross_columns=True, col_sep="\t")
        if next_FK != -1:
          next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
          FK = search_in_labels(str(next_FK))
      elif key == "postal_code":
        next_FK = binary_search(global_postal_codes, FK, cross_columns=True, col_sep="\t")
        if next_FK != -1:
          next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
          FK = search_in_labels(str(next_FK))
      elif key == "state_province_region":
        next_FK = binary_search(global_state_province_regions, FK, cross_columns=True, col_sep="\t")
        if next_FK != -1:
          next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
          FK = search_in_labels(str(next_FK))
      else:
        FK = search_in_labels(FK)
    if FK == -1:
      return
    
    FK = remove_language_tags(FK)
    data[group_name].append({key : FK})
    return

  if key not in data and save_like_array:
    data[key] = []

  if is_foreign_key: 
    label = -1
    next_FK = -1
    FK = FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
    if key == "latitude":
      label = binary_search(global_latitudes, FK, cross_columns=True, col_sep="\t")
    elif key == "longitude":
      label = binary_search(global_longitudes, FK, cross_columns=True, col_sep="\t")
    elif key == "country":
      next_FK = binary_search(global_countries, FK, cross_columns=True, col_sep="\t")
      if next_FK != -1:
        next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
        label = search_in_labels(str(next_FK))
    elif key == "population":
      label = binary_search(global_numbers, FK, cross_columns=True, col_sep="\t")
    elif key == "places_lived":
      next_FK = binary_search(global_locations, FK, cross_columns=True, col_sep="\t")
      if next_FK != -1:
        next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
        label = search_in_labels(str(next_FK))
    elif key == "owner":
      next_FK = binary_search(global_owners, FK, cross_columns=True, col_sep="\t")
      if next_FK != -1:
        next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
        label = search_in_labels(str(next_FK))
    elif original_key == "<http://rdf.freebase.com/ns/visual_art.artwork.locations>":
      next_FK = binary_search(global_artwork_location_relationship, FK, cross_columns=True, col_sep="\t")
      if next_FK != -1:
        next_FK = next_FK.replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
        label = search_in_labels(str(next_FK))
    else:
      label = search_in_labels(FK)
    if label == -1:
      return

    label = remove_language_tags(label)
    if save_id:
      if save_like_array:
        data[key].append({'value': label, 'id': splited_line[2].replace("<http://rdf.freebase.com/ns/m.", "")[:-1]})
      else:
        data[key] = {'value': label, 'id': splited_line[2].replace("<http://rdf.freebase.com/ns/m.", "")[:-1]}
    else:
      if only_first_letter:
        label = label[0]
      if save_like_array:
        data[key].append(label)
      else:
        data[key] = label
    return
  else:
    value = FK.replace("%13", "–")
    value = remove_language_tags(value)
    if save_like_array:
      if "en.wikipedia.org" in value and "%" in value:
        try:
          value = urllib.unquote(value).decode('cp1250')
        except:
          pass
      data[key].append(value)
    else:
      value = value.replace("^^<http://www.w3.org/2001/XMLSchema", "").replace("#gYear>", "").replace("#date>", "").replace("#gYearMonth>", "").replace(">","")
      data[key] = value

def bind_language_data(original_key, key, splited_line, data, save_like_array=True):
  if (splited_line[1] == original_key):
    if '"@en' in splited_line[2]:
      if key not in data:
        data[key] = []
      value = splited_line[2].replace('"', '').replace('@en','')
      if save_like_array:
        data[key].append(value)
      else:
        data[key] = value

def bind_image(splited_line, data, data_type):
  if (splited_line[1] == "<http://rdf.freebase.com/ns/common.topic.image>"):
    if "image" not in data:
      data["image"] = []

    splited_line[2] = splited_line[2].replace("<http://rdf.freebase.com/ns/m.", "")[:-1]
    #google freebase api key 

    image_path = '/mnt/data/kb/images/freebase/%s.jpg' % (splited_line[2])

    if not os.path.isfile(image_path) or (os.path.isfile(image_path) and os.path.getsize(image_path) < 500):
      url = "https://usercontent.googleapis.com/freebase/v1/image/m/%s?key=%s&maxheight=4096" % (splited_line[2], global_api_key)
      #save image
      image_data = urllib.urlopen(url).read()
      if not "dailyLimitExceeded" in image_data:
        with open(image_path, 'wb') as f:
          f.write(image_data)
      
    if os.path.isfile(image_path):
      b = os.path.getsize(image_path)
      if b < 500:
        try:
          os.remove(image_path)
        except Exception:
          pass
    if os.path.isfile(image_path):
      image = {}
      image["path"] = "%s.jpg" % splited_line[2]
      image["id"] = splited_line[2]
      data["image"].append(image)

def load_global_list(name):
  path = "help/"
  if not os.path.isfile(path + name):
    print "ERROR: File \"%s\" not found" % name
    exit(1)
  dial = []
  dial = load_file(path + name)
  dial.sort()
  return dial

def main():
  global global_labels
  global global_numbers
  global global_latitudes
  global global_longitudes
  global global_height_meters
  global global_width_meters
  global global_depth_meters
  global global_citytowns
  global global_countries
  global global_postal_codes
  global global_state_province_regions
  global global_locations
  global global_owners
  global global_artwork_location_relationship

  argument_types = ["art_period_movement", "artist", "artwork", "event", "museum", "location", "visual_art_form", "visual_art_genre", "visual_art_medium"]
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--data-type', default=False, dest='data_type', type=str, help='Select data type to convert. (artist, artwork, person, location)', nargs=1)
  parser.add_argument('-l', '--dump-loc', default=False, dest='dump_loc', type=str, help='Location of freebase-rdf.gz', nargs=1)
  arguments = parser.parse_args()

  if arguments.dump_loc:
    global_gzip_filename = arguments.dump_loc[0]

  if not arguments.data_type:
    parser.error('No action requested, add -t <artist|artwork|person|location|all|...>')
  
  if (arguments.data_type[0] == "help_files" or 
      arguments.data_type[0] == "ids" or
      arguments.data_type[0] == "help"):
    generate_help_files()  
  else:
    global_labels = load_global_list("labels")
    global_numbers = load_global_list("numbers")
    global_latitudes = load_global_list("latitudes")
    global_longitudes = load_global_list("longitudes")
    global_height_meters = load_global_list("height_meters")
    global_width_meters = load_global_list("width_meters")
    global_depth_meters = load_global_list("depth_meters")
    global_citytowns = load_global_list("citytowns")
    global_countries = load_global_list("countries")
    global_postal_codes = load_global_list("postal_codes")
    global_state_province_regions = load_global_list("state_province_regions")
    global_locations = load_global_list("locations")
    if arguments.data_type[0] == "artwork":
      global_owners = load_global_list("owners")
      global_artwork_location_relationship = load_global_list("artwork_location_relationship")
    if arguments.data_type[0] == "all":
      convert_rdf_to_dic(ids_list, "all")
    else:
      ids_list = load_from_stdin()
      ids_list.sort()
      convert_rdf_to_dic(ids_list, arguments.data_type[0])

if __name__ == "__main__":
  main()
