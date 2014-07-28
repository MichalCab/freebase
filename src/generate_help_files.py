#!/bin/env python
#-*- coding: utf-8 -*-
# file generateIdsList.py

import urllib
import os
import sys 
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
import datetime

#from src.binary_search import *

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

global_number_when_write_to_file = 12500
global_gzip_filename = "freebase-rdf.gz"

def generate_help_files():
  artists_ids = []
  artworks_ids = []
  persons_ids = []
  locations_ids = []
  events_ids = []
  museums_ids = []
  art_period_movements_ids = []
  visual_art_forms_ids = []
  visual_art_genres_ids = []
  visual_art_mediums_ids = []
  labels = []
  latitudes = []
  longitudes = []
  height_meters = []
  width_meters = []
  depth_meters = []
  citytowns = []
  countries = []
  postal_codes = []
  state_province_regions = []
  numbers = []  
  locations = []
  owners = []
  artwork_location_relationship = []
    
  a = 0
  start_time = time.time()  
  with gzip.open(global_gzip_filename, 'r') as infile:
     for line in infile:
      splited_line = line.split('\t')
      a = a + 1
      if splited_line[1] == "<http://rdf.freebase.com/ns/type.object.type>":
        if splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.visual_artist>":
          artists_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.artwork>":
          artworks_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/people.person>":
          persons_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/location.location>":
          locations_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/time.event>":
          events_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/architecture.museum>":
          museums_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.art_period_movement>":
          art_period_movements_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.visual_art_form>":
          visual_art_forms_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.visual_art_genre>":
          visual_art_genres_ids.append(splited_line[0])
        elif splited_line[2] == "<http://rdf.freebase.com/ns/visual_art.visual_art_medium>":
          visual_art_mediums_ids.append(splited_line[0])

      foringe_key = splited_line[0].replace("<http://rdf.freebase.com/ns/m.", "")[:-1] + "\t" + splited_line[2]

      if ((splited_line[1] == "<http://rdf.freebase.com/ns/type.object.name>" 
          or splited_line[1] == "<http://rdf.freebase.com/ns/common.document.text>") and 
          "@en" in splited_line[2] and "<http://rdf.freebase.com/ns/m." in splited_line[0]):
        labels.append(splited_line[0].replace("<http://rdf.freebase.com/ns/m.", "")[:-1] + "\t" + splited_line[2].replace("@en", "").replace('"', ''))

      if splited_line[1] == "<http://rdf.freebase.com/ns/location.geocode.latitude>":
        latitudes.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/location.geocode.longitude>":
        longitudes.append(foringe_key)

      if splited_line[1] == "<http://rdf.freebase.com/ns/measurement_unit.dimensions.height_meters>":
        height_meters.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/measurement_unit.dimensions.width_meters>":
        width_meters.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/measurement_unit.dimensions.depth_meters>":
        depth_meters.append(foringe_key)

      if splited_line[1] == "<http://rdf.freebase.com/ns/location.mailing_address.citytown>":
        citytowns.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/location.mailing_address.country>":
        countries.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/location.mailing_address.postal_code>":
        postal_codes.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/location.mailing_address.state_province_region>":
        state_province_regions.append(foringe_key)
      
      if splited_line[1] == "<http://rdf.freebase.com/ns/measurement_unit.dated_integer.number>":
        numbers.append(foringe_key)
  
      if splited_line[1] == "<http://rdf.freebase.com/ns/people.place_lived.location>":
        locations.append(foringe_key)

      if splited_line[1] == "<http://rdf.freebase.com/ns/visual_art.artwork_owner_relationship.owner>":
        owners.append(foringe_key)
      if splited_line[1] == "<http://rdf.freebase.com/ns/visual_art.artwork_location_relationship.location>":
        artwork_location_relationship.append(foringe_key)
      
      if a % 250000 == 0:
        os.system('clear')
        print "Entry checked (%s)" % a
        print "Writing artists_ids (%s)" % len(artists_ids)
        print "Writing artworks_ids (%s)" % len(artworks_ids)
        print "Writing persons_ids (%s)" % len(persons_ids)
        print "Writing locations_ids (%s)" % len(locations_ids)
        print "Writing events_ids (%s)" % len(events_ids)
        print "Writing museums_ids (%s)" % len(museums_ids)
        print "Writing art_period_movements_ids (%s)" % len(art_period_movements_ids)
        print "Writing visual_art_forms_ids (%s)" % len(visual_art_forms_ids)
        print "Writing visual_art_genres_ids (%s)" % len(visual_art_genres_ids)
        print "Writing visual_art_mediums_ids (%s)" % len(visual_art_mediums_ids)
        print "Writing labels (%s)" % len(labels)
        print "Writing latitudes (%s)" % len(latitudes)
        print "Writing longitudes (%s)" % len(longitudes)
        print "Writing height_meters (%s)" % len(height_meters)
        print "Writing width_meters (%s)" % len(width_meters)
        print "Writing depth_meters (%s)" % len(depth_meters)
        print "Writing citytowns (%s)" % len(citytowns)
        print "Writing countries (%s)" % len(countries)
        print "Writing postal_codes (%s)" % len(postal_codes)
        print "Writing state_province_regions (%s)" % len(state_province_regions)
        print "Writing numbers (%s)" % len(numbers)
        print "Writing locations (%s)" % len(locations)
        ts = (time.time() - start_time)
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print "Generating took ", st, " to run"

        if len(artists_ids) >= global_number_when_write_to_file:
          write_to_file("ids/artists_ids", artists_ids)
          artists_ids[:] = []
        if len(artworks_ids) >= global_number_when_write_to_file:
          write_to_file("ids/artworks_ids", artworks_ids)
          artworks_ids[:] = []
        if len(persons_ids) >= global_number_when_write_to_file:
          write_to_file("ids/persons_ids", persons_ids)
          persons_ids[:] = []
        if len(locations_ids) >= global_number_when_write_to_file:
          write_to_file("ids/locations_ids", locations_ids)
          locations_ids[:] = []
        if len(events_ids) >= global_number_when_write_to_file:
          write_to_file("ids/events_ids", events_ids)
          events_ids[:] = []
        if len(museums_ids) >= global_number_when_write_to_file:
          write_to_file("ids/museums_ids", museums_ids)
          museums_ids[:] = []
        if len(art_period_movements_ids) >= global_number_when_write_to_file:
          write_to_file("ids/art_period_movements_ids", art_period_movements_ids)
          art_period_movements_ids[:] = []
        if len(visual_art_forms_ids) >= global_number_when_write_to_file:
          write_to_file("ids/visual_art_forms_ids", visual_art_forms_ids)
          visual_art_forms_ids[:] = []
        if len(visual_art_genres_ids) >= global_number_when_write_to_file:
          write_to_file("ids/visual_art_genres_ids", visual_art_genres_ids)
          visual_art_genres_ids[:] = []
        if len(visual_art_mediums_ids) >= global_number_when_write_to_file:
          write_to_file("ids/visual_art_mediums_ids", visual_art_mediums_ids)
          visual_art_mediums_ids[:] = []
        if len(labels) >= global_number_when_write_to_file:
          write_to_file("help/labels", labels)
          labels[:] = []
        if len(latitudes) >= global_number_when_write_to_file:
          write_to_file("help/latitudes", latitudes)
          latitudes[:] = []
        if len(longitudes) >= global_number_when_write_to_file:
          write_to_file("help/longitudes", longitudes)
          longitudes[:] = []

        if len(height_meters) >= global_number_when_write_to_file:
          write_to_file("help/height_meters", height_meters)
          height_meters[:] = []
        if len(width_meters) >= global_number_when_write_to_file:
          write_to_file("help/width_meters", width_meters)
          width_meters[:] = []
        if len(depth_meters) >= global_number_when_write_to_file:
          write_to_file("help/depth_meters", depth_meters)
          depth_meters[:] = []
        if len(citytowns) >= global_number_when_write_to_file:
          write_to_file("help/citytowns", citytowns)
          citytowns[:] = []
        if len(countries) >= global_number_when_write_to_file:
          write_to_file("help/countries", countries)
          countries[:] = []
        if len(postal_codes) >= global_number_when_write_to_file:
          write_to_file("help/postal_codes", postal_codes)
          postal_codes[:] = []
        if len(state_province_regions) >= global_number_when_write_to_file:
          write_to_file("help/state_province_regions", state_province_regions)
          state_province_regions[:] = []
        if len(numbers) >= global_number_when_write_to_file:
          write_to_file("help/numbers", numbers)
          numbers[:] = []
        if len(locations) >= global_number_when_write_to_file:
          write_to_file("help/locations", locations)
          locations[:] = []
        if len(owners) >= global_number_when_write_to_file:
          write_to_file("help/owners", owners)
          owners[:] = []
        if len(artwork_location_relationship) >= global_number_when_write_to_file:
          write_to_file("help/owners", artwork_location_relationship)
          artwork_location_relationship[:] = []

  write_to_file("ids/artists_ids", artists_ids)
  write_to_file("ids/artworks_ids", artworks_ids)
  write_to_file("ids/persons_ids", persons_ids)
  write_to_file("ids/locations_ids", locations_ids)
  write_to_file("ids/events_ids", events_ids)
  write_to_file("ids/museums_ids", museums_ids)
  write_to_file("ids/art_period_movements_ids", art_period_movements_ids)
  write_to_file("ids/visual_art_forms_ids", visual_art_forms_ids)
  write_to_file("ids/visual_art_genres_ids", visual_art_genres_ids)
  write_to_file("ids/visual_art_mediums_ids", visual_art_mediums_ids)
  write_to_file("help/labels", labels)
  write_to_file("help/latitudes", latitudes)
  write_to_file("help/longitudes", longitudes)
  write_to_file("help/height_meters", height_meters)
  write_to_file("help/width_meters", width_meters)
  write_to_file("help/depth_meters", depth_meters)
  write_to_file("help/citytowns", citytowns)
  write_to_file("help/countries", countries)
  write_to_file("help/postal_codes", postal_codes)
  write_to_file("help/state_province_regions", state_province_regions)
  write_to_file("help/numbers", numbers)
  write_to_file("help/locations", locations)
  write_to_file("help/owners", owners)
  write_to_file("help/artwork_location_relationship", artwork_location_relationship)

def write_to_file(filename, data):
  f = open(filename, 'a')
  for item in data:
    f.write("%s\n" % item)
  f.close()
