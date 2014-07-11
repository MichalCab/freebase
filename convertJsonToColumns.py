#!/usr/bin/env python
#-*- coding: utf-8 -*-
# python 2.7
# file convertJsonToColumns.py

import json
import argparse
import sys
import re

from src.data_model import *
from src.add_alternative_by_wiki import *
from src.remove_redirections import *
from src.load_file import *
from src.binary_search import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_replace_new_line = re.compile(r'((?<=\.)\s*\\n\s{2,})|[^.](\s+\\n\s+)')
global_replace_backslash = re.compile(r'\\(?=[^n])')

"""
azbuka_vzor = re.compile('[\u0400-\u04ff]+')
arabsky_vzor = re.compile('[\u0600-\u06ff]+')
recky_vzor = re.compile('[\u0370-\u03ff]+')
gruzinsky_vzor = re.compile('[\u10a0-\u10ff]+')
hebrejsky_vzor = re.compile('[\u0590-\u05ff]+')
asijske_vzor = re.compile('[\u3100-\u312f\u4e00-\u9fcc\u1100-\u11ff\u30a0-\u30ff\u3040-\u309f\uac00-\ud7af]+')
armensky_vzor = re.compile('[\u0530-\u058f]+')
"""

global_unwanted_ids = []

def get_wikipedia_url(_wikipedia_url):
  result = ""
  for ew in _wikipedia_url:
    if ew.startswith("http://en.wikipedia.org/wiki/") and ew.find("index.html?curid=") == -1:
      result = ew
      break
  return result

def format_string(_string):
  _string = _string.replace(" \\n", "\\n").replace("\\n ", "\\n") #problem u"\u201D"
  return _string.encode('utf8').replace("\n", " ").replace("\t", " ")

def load_data(_filename, data_type):
  data = json.load(_filename)

  results = []

  for d in data:
    d = d["itemInfo"]

    if "name" not in d:
      continue

    """
    if ("http://" in d["name"] or (
        not azbuka_vzor.match(d["name"]) and
        not arabsky_vzor.match(d["name"]) and
        not recky_vzor.match(d["name"]) and
        not gruzinsky_vzor.match(d["name"]) and
        not hebrejsky_vzor.match(d["name"]) and
        not asijske_vzor.match(d["name"]) and
        not armensky_vzor.match(d["name"])) or
    """
    if d["id"] in global_unwanted_ids:
      continue
    
    if "object_type" in d and data_type == "location":
      if (not any("location.citytown" in ot for ot in d["object_type"]) and
          not any("location.country" in ot for ot in d["object_type"])):
        if any("organization.organization>" in ot or 
             "metropolitan_transit.transit_stop" in ot or
             "architecture.building" in ot or
             "architecture.structure" in ot 
             for ot in d["object_type"]):
          continue

    name = ""
    nationality_name = "";
    if data_type == "nationalities":
      nationality_name = format_string(d["name"])
    else:
      name = format_string(d["name"])

    freebase_id = format_string(d["id"])

    # all
    alias = []; description = ""; image = [];  wikipedia_url = "";


    # artist, person
    period_or_movement = []; influenced = []; influenced_by = []; place_of_birth = ""; place_of_death = ""; date_of_birth = ""; date_of_death = ""; profession = []; art_form = []; places_lived = []; gender = ""; nationality = []

    # artwork
    artist = []; art_subject = []; art_form = ""; art_genre = []; media = []; support = []; period_or_movement = []; location = []; date_begun = ""; date_completed = ""; owner = []; dimensions = {"height":"", "width":"", "depth":""}

    # location
    latitude = ""; longitude = ""; loc_type = ""; country = ""; population = []

    # museum
    type_of_museum = []; established = ""; director = ""; visitors = ""; address = {"citytown":"", "postal_code":"", "state_province_region":"", "street_address":""}

    # event
    start_date = ""; end_date = ""; locations = []; notable_types = ""

    # country
    short_name = ""; adjectival_form = []
    
    # all
    if "alias" in d:
      fields = d["alias"]
      for f in fields:
        alias.append(re.sub(global_replace_backslash, '\'', format_string(f)))
    if "description" in d:
      description = re.sub(global_replace_new_line, ' ', re.sub(global_replace_backslash, '\'', format_string(d["description"])))
    if "article" in d:
      if description.strip() == "":
        description = re.sub(global_replace_new_line, ' ', re.sub(global_replace_backslash, '\'', format_string(d["article"])))
    if "image" in d:
      fields = d["image"]
      for f in fields:
        image.append("freebase/"+format_string(f["path"]))
    if "key_wikipedia_en" in d:
      wikipedia_url = format_string(d["key_wikipedia_en"])

    # artist, person
    if "associated_periods_or_movements" in d:
      fields = d["associated_periods_or_movements"]
      for f in fields:
        period_or_movement.append(format_string(f))
    if "influenced" in d:
      fields = d["influenced"]
      for f in fields:
        if "value" in f:
          influenced.append(format_string(f["value"]))
    if "influenced_by" in d:
      fields = d["influenced_by"]
      for f in fields:
        if "value" in f:
          influenced_by.append(format_string(f["value"]))
    if "place_of_birth" in d:
      if "value" in d["place_of_birth"]:
        place_of_birth = format_string(d["place_of_birth"]["value"])
    if "place_of_death" in d:
      if "value" in d["place_of_death"]:
        place_of_death = format_string(d["place_of_death"]["value"])
    if "date_of_birth" in d:
      date_of_birth = format_string(d["date_of_birth"])
    if "date_of_death" in d:
      date_of_death = format_string(d["date_of_death"])
    if "profession" in d:
      fields = d["profession"]
      for f in fields:
        profession.append(format_string(f).replace("-GB", ""))
    if "places_lived" in d:
      fields = d["places_lived"]
      for f in fields:
        if "value" in f:
          places_lived.append(format_string(f["value"]))
    if "nationality" in d:
      fields = d["nationality"]
      for f in fields:
        nationality_string = binarySearch(global_nationality_country, format_string(f), cross_columns=True, col_sep="\t")
        if nationality_string == -1:
          nationality_string = f
        try:
          nationality.append(format_string(nationality_string))
        except:
          nationality.append(format_string(f))
    if "gender" in d:
      gender = format_string(d["gender"])

    # artwork
    if "artist" in d:
        fields = d["artist"]
        for f in fields:
          artist.append(format_string(f["value"]))
    if "art_subject" in d:
      fields = d["art_subject"]
      for f in fields:
        art_subject.append(format_string(f))
    if "art_form" in d:
      art_form = format_string(d["art_form"])
    if "art_genre" in d:
      fields = d["art_genre"]
      for f in fields:
        art_genre.append(format_string(f))
    if "media" in d:
      fields = d["media"]
      for f in fields:
        media.append(format_string(f))
    if "support" in d:
      fields = d["support"]
      for f in fields:
        support.append(format_string(f))
    if "period_or_movement" in d:
      fields = d["period_or_movement"]
      for f in fields:
        period_or_movement.append(format_string(f))
    if "location" in d:
      fields = d["location"]
      for f in fields:
        location.append(format_string(f["value"]))
    if "date_begun" in d:
      date_begun = format_string(d["date_begun"])
    if "date_completed" in d:
      date_completed = format_string(d["date_completed"])
    if "wikipedia_url" in d:
      fields = d["wikipedia_url"]
      for f in fields:
        wikipedia_url.append(format_string(f[1:-1]))
    if "owner" in d:
      fields = d["owner"]
      for f in fields:
        owner.append(format_string(f["value"]))
    if "dimensions" in d:
      fields = d["dimensions"]
      if "height" in f:
        dimension["height"] = format_string(f["height"])
      if "width" in f:
        dimension["width"] = format_string(f["width"])
      if "depth" in f:
        dimension["depth"] = format_string(f["depth"])

    # location
    if "population" in d:
      fields = d["population"]
      for f in fields:
        population.append(format_string(f))
    if "latitude" in d:
      latitude =  format_string(d["latitude"])
    if "longitude" in d:
      longitude =  format_string(d["longitude"])
    if "country" in d:
      if "value" in d["country"]:
        country = format_string(d["country"]["value"])
    if "loc_type" in d:
      loc_type = (format_string(d["loc_type"]))

    # museum
    if "type_of_museum" in d:
      fields = d["type_of_museum"]
      for f in fields:
        type_of_museum.append(format_string(f))
    if "established" in d:
      established = format_string(d["established"])
    if "director" in d:
      if "value" in d["director"]:
        director = format_string(d["director"]["value"])
    if "visitors" in d:
      visitors = format_string(d["visitors"])
    if "address" in d:
      if "citytown" in d["address"]:
        if "value" in d["address"]["citytown"]:
          address["citytown"] = format_string(d["address"]["citytmwn"]["value"])
      if "postal_code" in d["address"]:
        address["postal_code"] = format_string(d["address"]["postal_code"])
      if "state_province_region" in d["address"]:
        address["state_province_region"] = format_string(d["address"]["state_province_region"])
      if "street_address" in d["address"]:
        address["street_address"] = format_string(d["address"]["street_address"])

    # event 
    if "start_date" in d:
      start_date = format_string(d["start_date"])
    if "end_date" in d:
      end_date = format_string(d["end_date"])
    if "locations" in d:
      fields = d["locations"]
      for f in fields:
        if "value" in f:
          locations.append(format_string(f["value"]))
    if "notable_types" in d:
      notable_types = format_string(d["notable_types"][0])

    #country
    if "short_name" in d:
      short_name = format_string(d["short_name"][0])
    if "adjectival_form" in d and data_type == "nationalities":
      fields = d["adjectival_form"]
      if len(fields) > 0 and fields[0]:
        name = format_string(fields[0])
      for f in fields:
        adjectival_form.append(format_string(f))

    if name.strip() == "":
      continue

    new_entity = None
    if data_type == "artist":
      new_entity = FreebaseArtist("a:" + freebase_id, name, alias, description, image, period_or_movement, influenced, influenced_by, place_of_birth, place_of_death, date_of_birth, date_of_death, wikipedia_url, profession, art_form, places_lived, gender, nationality)
    elif data_type == "person":
      new_entity = FreebasePerson("p:" + freebase_id, name, alias, description, image, period_or_movement, place_of_birth, place_of_death, date_of_birth, date_of_death, wikipedia_url, profession, places_lived, gender, nationality)
    elif data_type == "artwork":
      new_entity = FreebaseArtwork("w:" + freebase_id, name, alias, description, image, artist, art_subject, art_form, art_genre, media, support, period_or_movement, location, date_begun, date_completed, wikipedia_url, owner, dimensions)
    elif data_type == "location":
      new_entity = FreebaseLocation("l:" + freebase_id, name, alias, description, image, wikipedia_url, latitude, longitude, loc_type, population, adjectival_form)
    elif data_type == "museum":
      new_entity = FreebaseMuseum("c:" + freebase_id, name, alias, description, image, wikipedia_url, type_of_museum, established, director, visitors, address, latitude, longitude)
    elif data_type == "event":
      new_entity = FreebaseEvent("e:" + freebase_id, name, alias, description, image, wikipedia_url, start_date, end_date, locations, notable_types)
    elif data_type == "visual_art_form":
      new_entity = FreebaseEntity("f:" + freebase_id, name, alias, description, image, wikipedia_url)
      new_entity.set_type("visual_art_form")
    elif data_type == "visual_art_genre":
      new_entity = FreebaseEntity("g:" + freebase_id, name, alias, description, image, wikipedia_url)
      new_entity.set_type("visual_art_genre")
    elif data_type == "art_period_movement":
      new_entity = FreebaseEntity("m:" + freebase_id, name, alias, description, image, wikipedia_url)
      new_entity.set_type("art_period_movement")
    elif data_type == "visual_art_medium":
      new_entity = FreebaseEntity("d:" + freebase_id, name, alias, description, image, wikipedia_url)
      new_entity.set_type("visual_art_medium")
    elif data_type == "nationalities":
      new_entity = FreebaseNationality("n:" + freebase_id, name, alias, description, image, wikipedia_url, short_name, adjectival_form, nationality_name)
    elif data_type == "all":
      new_entity = FreebaseEntity("f" + freebase_id, name, alias, description, image, wikipedia_url)

    if new_entity is not None:
      results.append(new_entity)

  return results

def print_knowledge_base(_data):
  for d in _data:
    print d

def print_list(_data):
  for d in _data:
    if d.name not in d.alias:
      if d.name.strip() != "":
        print str(d.name) + "\t" + d.freebase_id
    for a in d.alias:
      if a.strip() != "":
        print str(a) + "\t" + d.freebase_id

if __name__ == "__main__": 
  # argument parsing
  parser = argparse.ArgumentParser()
  parser.add_argument('-l', '--list', action='store_true', default=False, dest='list', help='Print list for an automaton.')
  parser.add_argument('-b', '--knowledge-base', action='store_true', default=False, dest='knowledge_base', help='Print knowledge base.')
  parser.add_argument('-t', '--data-type', default=False, dest='data_type', type=str, help='Select data type to convert.', nargs=1)
  parser.add_argument('-i', '--input-file', default=False, dest='input_file', type=str, help='Input file.', nargs=1)
  args = parser.parse_args()

  global_unwanted_ids = load_file("/mnt/minerva1/nlp/projects/decipher_freebase/crawler/help/unwanted_ids")
  global_nationality_country = load_file("/mnt/minerva1/nlp/projects/decipher_freebase/crawler/help/nationality_country")
  global_nationality_country.sort()

  if args.data_type:
    data = load_data(sys.stdin, args.data_type[0])
    add_alternative_by_wiki(data)
    remove_redirections(data)
  if args.knowledge_base:
    print_knowledge_base(data)
  if args.list:
    print_list(data)

