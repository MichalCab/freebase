#!/bin/env python
#-*- coding: utf-8 -*-
#Python 2.7.3
#File: data_model.py

import json
import urllib

__author__ = "Michal Cab <xcabmi00@stud.fit.vutbr.cz>"

class FreebaseEntity:
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url):
    self.freebase_id = _freebase_id
    self.name = _name
    self.alias = _alias
    self.description = _description
    self.image = _image
    self.key_wikipedia_en = _wikipedia_url
    self.wikipedia_url = get_wikipedia_url(self.key_wikipedia_en)
    self.freebase_url = "http://www.freebase.com/m/" + _freebase_id[2:]
    self.entity_type = ""

  def set_type(self, _entity_type):
    self.entity_type = _entity_type

  def __str__(self):
    return self.freebase_id + "\t" + self.entity_type + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

class FreebasePerson(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _period_or_movement, _place_of_birth, _place_of_death, _date_of_birth, _date_of_death, _wikipedia_url, _profession, _places_lived, _gender, _nationality):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.period_or_movement = _period_or_movement
    self.place_of_birth = _place_of_birth
    self.place_of_death = _place_of_death
    self.date_of_birth = _date_of_birth
    self.date_of_death = _date_of_death
    self.profession = _profession
    self.places_lived = _places_lived
    self.gender = _gender
    self.nationality = _nationality

  def __str__(self):
    return self.freebase_id + "\t" + "person" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + "|".join(map(str, self.period_or_movement)) + "\t" + self.place_of_birth + "\t" + self.place_of_death+"\t"+self.date_of_birth+"\t"+self.date_of_death+"\t"+"|".join(map(str, self.profession))+"\t"+"|".join(map(str, self.places_lived))+"\t"+self.gender+"\t"+"|".join(map(str, self.nationality))+"\t"+ self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseArtist(FreebasePerson):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _period_or_movement, _influenced, _influenced_by, _place_of_birth, _place_of_death, _date_of_birth, _date_of_death, _wikipedia_url, _profession, _art_form, _places_lived, _gender, _nationality):
    FreebasePerson.__init__(self, _freebase_id, _name, _alias, _description, _image, _period_or_movement, _place_of_birth, _place_of_death, _date_of_birth, _date_of_death, _wikipedia_url, _profession, _places_lived, _gender, _nationality)
    self.influenced = _influenced
    self.influenced_by = _influenced_by
    self.art_form = _art_form

  def __str__(self):
    return self.freebase_id + "\t" + "artist" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + "|".join(map(str, self.period_or_movement)) + "\t" + "|".join(map(str, self.influenced)) + "\t" + "|".join(map(str, self.influenced_by)) + "\t" + self.place_of_birth + "\t" + self.place_of_death + "\t"+self.date_of_birth + "\t" + self.date_of_death + "\t" + "|".join(map(str, self.profession)) + "\t" + "|".join(map(str, self.art_form))+"\t" + "|".join(map(str, self.places_lived)) + "\t" + self.gender + "\t" + "|".join(map(str, self.nationality))+"\t"+ self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseArtwork(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _artist, _art_subject, _art_form, _art_genre, _media, _support, _period_or_movement, _location, _date_begun, _date_completed, _wikipedia_url, _owner, _dimensions):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.artist = _artist
    self.art_subject = _art_subject
    self.art_form = _art_form
    self.art_genre = _art_genre
    self.media = _media
    self.support = _support
    self.period_or_movement = _period_or_movement
    self.location = _location
    self.date_begun = _date_begun
    self.date_completed = _date_completed
    self.owner = _owner
    self.dimensions = _dimensions

  def __str__(self):
    return self.freebase_id + "\t" + "artwork" + "\t" + self.name+"\t"+"|".join(map(str, self.alias))+"\t"+self.description+"\t"+"|".join(map(str, self.image))+"\t"+"|".join(map(str, self.artist))+"\t"+"|".join(map(str, self.art_subject))+"\t"+self.art_form+ "\t" + "|".join(map(str, self.art_genre)) + "\t" + "|".join(map(str, self.media)) + "\t" + "|".join(map(str, self.support)) + "\t" + "|".join(map(str, self.period_or_movement)) + "\t" + "|".join(map(str, self.location)) + "\t" + self.date_begun + "\t" + self.date_completed + "\t" + "|".join(map(str, self.owner)) + "\t" + self.dimensions["height"] + "\t" + self.dimensions["width"] + "\t" + self.dimensions["depth"] + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseLocation(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url, _latitude, _longitude, _loc_type, _population, _nationalities):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.latitude = _latitude
    self.longitude = _longitude
    self.loc_type = _loc_type
    self.nationalities = _nationalities
    self.population = _population

  def __str__(self):
    return self.freebase_id + "\t" + "location" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + self.latitude + "\t" + self.longitude + "\t" + self.loc_type + "\t" + "|".join(map(str, self.nationalities)) + "\t" + "|".join(map(str, self.population)) + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseMuseum(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url, _type_of_museum, _established, _director, _visitors, _address, _latitude, _longitude):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.type_of_museum = _type_of_museum
    self.established = _established
    self.director = _director
    self.visitors = _visitors 
    self.address = _address
    self.latitude = _latitude
    self.longitude = _longitude

  def __str__(self):
    return self.freebase_id + "\t" + "museum" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + "|".join(map(str, self.type_of_museum)) + "\t" + self.established + "\t" + self.director + "\t" + self.visitors + "\t" + self.address["citytown"] + "\t" + self.address["postal_code"] + "\t" + self.address["state_province_region"] + "\t" + self.address["street_address"] + "\t" + self.latitude + "\t" + self.longitude + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseEvent(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url, _start_date, _end_date, _locations, _notable_types):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.start_date = _start_date
    self.end_date = _end_date
    self.locations = _locations
    self.notable_types = _notable_types

  def __str__(self):
    return self.freebase_id + "\t" + "event" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + self.start_date + "\t" + self.end_date + "\t" + "|".join(map(str, self.locations)) + "\t" + self.notable_types + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

class FreebaseNationality(FreebaseEntity):
  def __init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url, _short_name, _adjectival_form, _nationality_name):
    FreebaseEntity.__init__(self, _freebase_id, _name, _alias, _description, _image, _wikipedia_url)
    self.short_name = _short_name
    self.nationality_name = _nationality_name
    self.adjectival_form = _adjectival_form

  def __str__(self):
    return self.freebase_id + "\t" + "nationality" + "\t" + self.name + "\t" + "|".join(map(str, self.alias)) + "\t" + self.description + "\t" + "|".join(map(str, self.image)) + "\t" + self.short_name + "\t" + self.nationality_name + "\t" + "|".join(map(str, self.adjectival_form)) + "\t" + self.freebase_url  + "\t" + self.wikipedia_url

def get_wikipedia_url(_wikipedia_url):
  result = ""
  _wikipedia_url = _wikipedia_url.replace("$","\u")
  _wikipedia_url = json.loads('"{0}"'.format(_wikipedia_url)).encode("utf-8")
  if _wikipedia_url:
    result = "http://en.wikipedia.org/wiki/" + urllib.unquote(_wikipedia_url)
  return result

