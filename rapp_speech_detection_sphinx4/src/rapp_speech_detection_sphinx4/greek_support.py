#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright 2015 RAPP

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

    #http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

# Authors: Athanassios Kintsakis, Aris Thallas, Manos Tsardoulias
# contact: akintsakis@issel.ee.auth.gr, aris.thallas@{iti.gr, gmail.com}, etsardou@iti.gr


import rospy
import sys
import re
import mmap

from global_parameters import GlobalParams
from rapp_exceptions import RappError
from english_support import *
from limited_vocabulary_creator import *
from rapp_tools import *

## @class GreekSupport
# @brief Allows the creation of configuration files for Greek Sphinx speech recognition
#
# Also supports multilanguage words (English/Greek) by utilizing
# english_support.EnglishSupport
class GreekSupport(GlobalParams):

  ## Performs initializations
  def __init__(self):
    GlobalParams.__init__(self)

    ## The limited vocabulary creator
    #
    # Instantiates limited_vocabulary_creator.LimitedVocabularyCreator
    self._vocabulary = LimitedVocabularyCreator()
    # TODO: Split the rapp_sphinx4_java_libraries package into libraries and
    # language models
    # NOTE: This does not exist yet
    #self._greek_dictionary = self._language_models_url + \
        #"/englishPack/cmudict-en-us.dict"

    jar_path = ".:" + self._sphinx_jar_files_url + "/" + \
        self._sphinx_jar_file + ":" \
            + self._sphinx_package_url + "/src"

    ## The generic Sphinx configuration
    #
    # Grammar is dummy here..
    # @todo Fix this according to the generic Greek model
    self._generic_sphinx_configuration = { \
      'jar_path' : jar_path, \
      'configuration_path' : self._language_models_url + "/greekPack/default.config.xml", \
      'acoustic_model' : self._acoustic_models_url + "/acoustic_model/", \
      'grammar_name' : 'hello', \
      'grammar_folder' : self._language_models_url + "/greekPack/", \
      'dictionary' : self._language_models_url +  "/englishPack/cmudict-en-us.dict", \
      'language_model' : self._language_models_url + "/englishPack/en-us.lm.bin", \
      'grammar_disabled' : True
      }

    ## Allows the creation of configuration files for English words
    #
    # Instantiates english_support.EnglishSupport to identify english words
    self._english_support = EnglishSupport()
    # Open the generic english dictionary file
    # NOTE: Fix this according to the Greek generic dictionary
    #try:
      #self.english_dict_file = open(self.english_dictionary, 'r')
    #except IOError:
      #print "English dictionary could not be opened!"
    # Create a mapping of the file
    #self.english_dict_mapping = mmap.mmap(self.english_dict_file.fileno(), 0, \
        #access = mmap.ACCESS_READ)

    ## Greek uppercase to lowercase mapping
    self._capital_letters = {}
    ## Greek words->English standard phonemes mapping
    self._phonemes = {}
    ## Two digit Greek letters->English phonemes mapping
    self._two_digit_letters = {}
    ## Special two digit Greek letter->English phonemes mapping
    self._special_two_digit_letters = []
    ## All special two digit Greek letter->English phonemes mapping
    self._all_special_two_digit_letters = {}
    ## Special Greek words ->English phonemes mapping
    self._s_specific_rules = {}
    ## Standard Greek letter->English phonemes mapping
    self._letters = {}
    ## Greek letters->English letters mapping
    self._literal_letters = {}

    self._configureLetters()

  ## Creates the basic Greek letter to English configuration
  def _configureLetters(self):

    f_base_pre = [u'π', u'τ', u'κ', u'θ', u'χ', u'σ', u'ξ', u'ψ']
    f_base = []
    for l in f_base_pre:
      f_base.append(l.encode('utf-8'))

    v_base_pre = [u'δ', u'γ', u'ζ', u'λ', u'ρ', u'μ', u'ν', u'α', u'ά', u'ε',\
        u'έ', u'η', u'ή', u'ι', u'ί', u'ϊ', u'ΐ', u'ο', u'ό', u'υ', u'ύ', u'ϋ'\
        u'ΰ', u'ω', u'ώ']
    v_base = []
    for l in v_base_pre:
      v_base.append(l.encode('utf-8'))

    self._capital_letters[(u'Α').encode('utf-8')] = (u'α').encode('utf-8')
    self._capital_letters[(u'Ά').encode('utf-8')] = (u'ά').encode('utf-8')
    self._capital_letters[(u'Β').encode('utf-8')] = (u'β').encode('utf-8')
    self._capital_letters[(u'Γ').encode('utf-8')] = (u'γ').encode('utf-8')
    self._capital_letters[(u'Δ').encode('utf-8')] = (u'δ').encode('utf-8')
    self._capital_letters[(u'Ε').encode('utf-8')] = (u'ε').encode('utf-8')
    self._capital_letters[(u'Έ').encode('utf-8')] = (u'έ').encode('utf-8')
    self._capital_letters[(u'Ζ').encode('utf-8')] = (u'ζ').encode('utf-8')
    self._capital_letters[(u'Η').encode('utf-8')] = (u'η').encode('utf-8')
    self._capital_letters[(u'Ή').encode('utf-8')] = (u'ή').encode('utf-8')
    self._capital_letters[(u'Θ').encode('utf-8')] = (u'θ').encode('utf-8')
    self._capital_letters[(u'Ι').encode('utf-8')] = (u'ι').encode('utf-8')
    self._capital_letters[(u'Ί').encode('utf-8')] = (u'ί').encode('utf-8')
    self._capital_letters[(u'Ϊ').encode('utf-8')] = (u'ϊ').encode('utf-8')
    self._capital_letters[(u'Κ').encode('utf-8')] = (u'κ').encode('utf-8')
    self._capital_letters[(u'Λ').encode('utf-8')] = (u'λ').encode('utf-8')
    self._capital_letters[(u'Μ').encode('utf-8')] = (u'μ').encode('utf-8')
    self._capital_letters[(u'Ν').encode('utf-8')] = (u'ν').encode('utf-8')
    self._capital_letters[(u'Ξ').encode('utf-8')] = (u'ξ').encode('utf-8')
    self._capital_letters[(u'Ο').encode('utf-8')] = (u'ο').encode('utf-8')
    self._capital_letters[(u'Ό').encode('utf-8')] = (u'ό').encode('utf-8')
    self._capital_letters[(u'Π').encode('utf-8')] = (u'π').encode('utf-8')
    self._capital_letters[(u'Ρ').encode('utf-8')] = (u'ρ').encode('utf-8')
    self._capital_letters[(u'Σ').encode('utf-8')] = (u'σ').encode('utf-8')
    self._capital_letters[(u'Τ').encode('utf-8')] = (u'τ').encode('utf-8')
    self._capital_letters[(u'Υ').encode('utf-8')] = (u'γ').encode('utf-8')
    self._capital_letters[(u'Ύ').encode('utf-8')] = (u'ύ').encode('utf-8')
    self._capital_letters[(u'Ϋ').encode('utf-8')] = (u'ϋ').encode('utf-8')
    self._capital_letters[(u'Φ').encode('utf-8')] = (u'φ').encode('utf-8')
    self._capital_letters[(u'Χ').encode('utf-8')] = (u'χ').encode('utf-8')
    self._capital_letters[(u'Ψ').encode('utf-8')] = (u'ψ').encode('utf-8')
    self._capital_letters[(u'Ω').encode('utf-8')] = (u'ω').encode('utf-8')
    self._capital_letters[(u'Ώ').encode('utf-8')] = (u'ώ').encode('utf-8')

    self._phonemes[(u'ου').encode('utf-8')] = 'UW '
    self._phonemes[(u'ού').encode('utf-8')] = 'UW '
    self._phonemes[(u'μπ').encode('utf-8')] = 'B '
    self._phonemes[(u'ντ').encode('utf-8')] = 'D '
    self._phonemes[(u'γκ').encode('utf-8')] = 'G ' #?
    self._phonemes[(u'γγ').encode('utf-8')] = 'G ' #?
    self._phonemes[(u'τσ').encode('utf-8')] = 'CH ' #?
    self._phonemes[(u'τζ').encode('utf-8')] = 'JH ' #?
    self._phonemes[(u'σσ').encode('utf-8')] = 'S ' #?
    self._phonemes[(u'κκ').encode('utf-8')] = 'K '
    self._phonemes[(u'ββ').encode('utf-8')] = 'V '
    self._phonemes[(u'λλ').encode('utf-8')] = 'L '
    self._phonemes[(u'μμ').encode('utf-8')] = 'M '
    self._phonemes[(u'νν').encode('utf-8')] = 'N '
    self._phonemes[(u'ππ').encode('utf-8')] = 'P '
    self._phonemes[(u'ρρ').encode('utf-8')] = 'R '
    self._phonemes[(u'ττ').encode('utf-8')] = 'T '

    self._two_digit_letters[(u'αι').encode('utf-8')] = 'EH '
    self._two_digit_letters[(u'αί').encode('utf-8')] = 'EH '
    self._two_digit_letters[(u'ει').encode('utf-8')] = 'IH '
    self._two_digit_letters[(u'εί').encode('utf-8')] = 'IH '
    self._two_digit_letters[(u'οι').encode('utf-8')] = 'IH '
    self._two_digit_letters[(u'οί').encode('utf-8')] = 'IH '
    self._two_digit_letters[(u'υι').encode('utf-8')] = 'IH '
    self._two_digit_letters[(u'υί').encode('utf-8')] = 'IH '

    self._special_two_digit_letters.append((u'αυ').encode('utf-8'))
    self._special_two_digit_letters.append((u'αύ').encode('utf-8'))
    self._special_two_digit_letters.append((u'ευ').encode('utf-8'))
    self._special_two_digit_letters.append((u'εύ').encode('utf-8'))
    special_two_digit_letters_v = {}
    special_two_digit_letters_v[(u'αυ').encode('utf-8')] = (u'αβ').encode('utf-8')
    special_two_digit_letters_v[(u'αύ').encode('utf-8')] = (u'άβ').encode('utf-8')
    special_two_digit_letters_v[(u'ευ').encode('utf-8')] = (u'εβ').encode('utf-8')
    special_two_digit_letters_v[(u'εύ').encode('utf-8')] = (u'έβ').encode('utf-8')
    special_two_digit_letters_f = {}
    special_two_digit_letters_f[(u'αυ').encode('utf-8')] = (u'αφ').encode('utf-8')
    special_two_digit_letters_f[(u'αύ').encode('utf-8')] = (u'άφ').encode('utf-8')
    special_two_digit_letters_f[(u'ευ').encode('utf-8')] = (u'εφ').encode('utf-8')
    special_two_digit_letters_f[(u'εύ').encode('utf-8')] = (u'έφ').encode('utf-8')

    for tdl in self._special_two_digit_letters:
      for fb in f_base:
        self._all_special_two_digit_letters[tdl + fb] = \
            special_two_digit_letters_f[tdl] + fb
    for tdl in self._special_two_digit_letters:
      for vb in v_base:
        self._all_special_two_digit_letters[tdl + vb] = \
            special_two_digit_letters_v[tdl] + vb

    self._s_specific_rules[(u'σγ').encode('utf-8')] = 'Z W '
    self._s_specific_rules[(u'σβ').encode('utf-8')] = 'Z V '
    self._s_specific_rules[(u'σδ').encode('utf-8')] = 'Z DH '
    self._s_specific_rules[(u'σμ').encode('utf-8')] = 'Z M '
    self._s_specific_rules[(u'σν').encode('utf-8')] = 'Z N '
    self._s_specific_rules[(u'σλ').encode('utf-8')] = 'Z L '
    self._s_specific_rules[(u'σρ').encode('utf-8')] = 'Z R '
    self._s_specific_rules[(u'σμπ').encode('utf-8')] = 'Z B '
    self._s_specific_rules[(u'σντ').encode('utf-8')] = 'Z D '

    self._letters[(u'α').encode('utf-8')] = 'AA ' # when AE?
    self._letters[(u'ά').encode('utf-8')] = 'AA '
    self._letters[(u'β').encode('utf-8')] = 'V '
    self._letters[(u'γ').encode('utf-8')] = 'W '
    self._letters[(u'δ').encode('utf-8')] = 'DH '
    self._letters[(u'ε').encode('utf-8')] = 'EH '
    self._letters[(u'έ').encode('utf-8')] = 'EH '
    self._letters[(u'ζ').encode('utf-8')] = 'Z '
    self._letters[(u'η').encode('utf-8')] = 'IH '
    self._letters[(u'ή').encode('utf-8')] = 'IH '
    self._letters[(u'θ').encode('utf-8')] = 'TH '
    self._letters[(u'ι').encode('utf-8')] = 'IH '
    self._letters[(u'ί').encode('utf-8')] = 'IH '
    self._letters[(u'ϊ').encode('utf-8')] = 'IH '
    self._letters[(u'ΐ').encode('utf-8')] = 'IH '
    self._letters[(u'κ').encode('utf-8')] = 'K '
    self._letters[(u'λ').encode('utf-8')] = 'L '
    self._letters[(u'μ').encode('utf-8')] = 'M '
    self._letters[(u'ν').encode('utf-8')] = 'N '
    self._letters[(u'ξ').encode('utf-8')] = 'K S '
    self._letters[(u'ο').encode('utf-8')] = 'OW '
    self._letters[(u'ό').encode('utf-8')] = 'OW '
    self._letters[(u'π').encode('utf-8')] = 'P '
    self._letters[(u'ρ').encode('utf-8')] = 'R '
    self._letters[(u'σ').encode('utf-8')] = 'S '
    self._letters[(u'τ').encode('utf-8')] = 'T '
    self._letters[(u'υ').encode('utf-8')] = 'IH '
    self._letters[(u'ύ').encode('utf-8')] = 'IH '
    self._letters[(u'ϋ').encode('utf-8')] = 'IH '
    self._letters[(u'ΰ').encode('utf-8')] = 'IH '
    self._letters[(u'φ').encode('utf-8')] = 'F '
    self._letters[(u'χ').encode('utf-8')] = 'HH '
    self._letters[(u'ψ').encode('utf-8')] = 'P S '
    self._letters[(u'ω').encode('utf-8')] = 'OW '
    self._letters[(u'ώ').encode('utf-8')] = 'OW '
    self._letters[(u'ς').encode('utf-8')] = 'S '

    self._literal_letters[(u'α').encode('utf-8')] = 'a' # when AE?
    self._literal_letters[(u'ά').encode('utf-8')] = 'a\''
    self._literal_letters[(u'β').encode('utf-8')] = 'b'
    self._literal_letters[(u'γ').encode('utf-8')] = 'g'
    self._literal_letters[(u'δ').encode('utf-8')] = 'd'
    self._literal_letters[(u'ε').encode('utf-8')] = 'e'
    self._literal_letters[(u'έ').encode('utf-8')] = 'e\''
    self._literal_letters[(u'ζ').encode('utf-8')] = 'z'
    self._literal_letters[(u'η').encode('utf-8')] = 'h'
    self._literal_letters[(u'ή').encode('utf-8')] = 'h\''
    self._literal_letters[(u'θ').encode('utf-8')] = 'th'
    self._literal_letters[(u'ι').encode('utf-8')] = 'i'
    self._literal_letters[(u'ί').encode('utf-8')] = 'i\''
    self._literal_letters[(u'ϊ').encode('utf-8')] = 'i:'
    self._literal_letters[(u'ΐ').encode('utf-8')] = 'i\':'
    self._literal_letters[(u'κ').encode('utf-8')] = 'k'
    self._literal_letters[(u'λ').encode('utf-8')] = 'l'
    self._literal_letters[(u'μ').encode('utf-8')] = 'm'
    self._literal_letters[(u'ν').encode('utf-8')] = 'n'
    self._literal_letters[(u'ξ').encode('utf-8')] = 'ks'
    self._literal_letters[(u'ο').encode('utf-8')] = 'o'
    self._literal_letters[(u'ό').encode('utf-8')] = 'o\''
    self._literal_letters[(u'π').encode('utf-8')] = 'p'
    self._literal_letters[(u'ρ').encode('utf-8')] = 'r'
    self._literal_letters[(u'σ').encode('utf-8')] = 's'
    self._literal_letters[(u'ς').encode('utf-8')] = 's\''
    self._literal_letters[(u'τ').encode('utf-8')] = 't'
    self._literal_letters[(u'υ').encode('utf-8')] = 'u'
    self._literal_letters[(u'ύ').encode('utf-8')] = 'u\''
    self._literal_letters[(u'ϋ').encode('utf-8')] = 'u:'
    self._literal_letters[(u'ΰ').encode('utf-8')] = 'u\':'
    self._literal_letters[(u'φ').encode('utf-8')] = 'f'
    self._literal_letters[(u'χ').encode('utf-8')] = 'x'
    self._literal_letters[(u'ψ').encode('utf-8')] = 'ps'
    self._literal_letters[(u'ω').encode('utf-8')] = 'w'
    self._literal_letters[(u'ώ').encode('utf-8')] = 'w\''


  ## Transforms the Greek words into phonemes for the Sphinx configuration
  #
  # @param words [list::string] The set of Greek words
  #
  # @return enhanced_words  [dictionary] The Greek word->phonemes mapping
  # @return englified_words [dictionary] The Greek word->Englified Greek word mapping
  def _transformWords(self, words):
    enhanced_words = {}
    englified_words = {}
    for word in words:
      initial_word = word
      rapp_print ("Initial word: " + initial_word)
      # transform capital _letters
      for cap in self._capital_letters:
        initial_word = initial_word.replace(cap, self._capital_letters[cap])
      rapp_print ("Caps to small: " + initial_word)
      # fix english version of _letters
      eng_w = initial_word
      for lit in self._literal_letters:
        eng_w = eng_w.replace(lit, self._literal_letters[lit])
      englified_words[eng_w] = word
      rapp_print ("Englified: " + eng_w)
      # check _phonemes
      for ph in self._phonemes:
        initial_word = initial_word.replace(ph, self._phonemes[ph])
      rapp_print ("Phonemes: " + initial_word)
      # check special two digit letters
      for stdl in self._all_special_two_digit_letters:
        initial_word = initial_word.replace(stdl, \
            self._all_special_two_digit_letters[stdl])
      rapp_print ("Special 2 digit letters: " + initial_word)
      # check two-digit letters
      for let in self._two_digit_letters:
        initial_word = initial_word.replace(let, self._two_digit_letters[let])
      rapp_print ("2 digit letters: " + initial_word)
      # check specific rules
      for sr in self._s_specific_rules:
        initial_word = initial_word.replace(sr, self._s_specific_rules[sr])
      rapp_print ("specific rules: " + initial_word)
      # check the rest of the letters
      for l in self._letters:
        initial_word = initial_word.replace(l, self._letters[l])
      rapp_print ("rest of letters: " + initial_word)

      enhanced_words[eng_w] = []
      temp = initial_word.split(' ')
      if len(temp) > 0:
        temp = temp[:-1]
      enhanced_words[eng_w] = temp

    return [enhanced_words, englified_words]

  ## Englify Greek words
  #
  # @param words [list::string] The set of Greek words
  def _englify_words(self, words):
    englified_words = []
    for word in words:
      eng_w = word
      # First transform the Capitals
      for cap in self._capital_letters:
        eng_w = eng_w.replace(cap, self._capital_letters[cap])
      for lit in self._literal_letters:
        eng_w = eng_w.replace(lit, self._literal_letters[lit])
      englified_words.append(eng_w)
    return englified_words


  ## Separates English from Greek words
  #
  # @param words      [list::string] The set of words to be identified
  # @param grammar    [list::string] The Sphinx grammar parameter
  # @param sentences  [list::string] The Sphinx sentences parameter
  #
  # @return english_words     [list::string] The set of English words
  # @return english_grammar   [list::string] The set of English grammar
  # @return english_sentences [list::string] The set of English sentences
  # @return greek_words       [list::string] The set of Greek words
  # @return greek_grammar     [list::string] The set of Greek words
  # @return greek_sentences   [list::string] The set of Greek words
  def _separateEngGrWords(self, words, grammar, sentences):

    english_words = []
    english_grammar = []
    english_sentences = []
    greek_words = []
    greek_grammar = []
    greek_sentences = []

    for word in words:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English word: " + str(word) )
        english_words.append( word )
      else:
        rapp_print( "Greek word: " + str(word) )
        greek_words.append( word )

    for word in grammar:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English grammar: " + str(word) )
        english_grammar.append( word )
      else:
        rapp_print( "Greek grammar: " + str(word) )
        greek_grammar.append( word )

    for word in sentences:
      if re.match('[a-zA-Z\-]', word):
        rapp_print( "English sentence: " + str(word) )
        english_sentences.append( word )
      else:
        rapp_print( "Greek sentence: " + str(word) )
        greek_sentences.append( word )

    return [ english_words, english_grammar, english_sentences, greek_words, \
    greek_grammar, greek_sentences ]



  ## Computes the Limited Greek Configuration
  #
  # @param words      [list::string] The set of words to be identified
  # @param grammar    [list::string] The Sphinx grammar parameter
  # @param sentences  [list::string] The Sphinx sentences parameter
  #
  # @return limited_sphinx_configuration [dictionary] The Limited Greek configuration
  # @return englified_to_greek_dict      [dictionary] A dictionary to transform the englified greek words to actual greek words
  def getLimitedVocebularyConfiguration(self, words, grammar, sentences):

    # Separate English from Greek words
    [ english_words, english_grammar, english_sentences, \
      greek_words, greek_grammar, greek_sentences ] = \
      self._separateEngGrWords( words, grammar, sentences )

    # Get phonemes for Greek words and dictionary for Englified->Greek mapping
    [englified_phonems_dict, englified_to_greek_dict] = \
        self._transformWords( greek_words )

    # Append english words to Englified->Greek mapping dictionary
    for word in english_words:
      englified_to_greek_dict.update( {word: word} )

    # Get phonemes for English words
    english_phonem_dict = self._english_support.getWordPhonemes( english_words )

    # Englify Greek grammar and sentences
    englified_grammar = self._englify_words(greek_grammar)
    englified_sentences = self._englify_words(greek_sentences)


    # Join English and Greek processed files
    final_phoneme_dict = english_phonem_dict
    final_phoneme_dict.update(englified_phonems_dict)
    final_sentences = englified_sentences + english_sentences
    final_grammar = english_grammar + englified_grammar

    try:
        limited_sphinx_configuration = \
            self._vocabulary.createConfigurationFiles( \
              final_phoneme_dict, final_grammar, final_sentences
            )
    except RappError as e:
        raise RappError(e.value)

    return [limited_sphinx_configuration, englified_to_greek_dict]

  ## Returns the Generic Greek Configuration
  #
  # @return #_generic_sphinx_configuration [dictionary] The Generic Greek configuration
  def getGenericConfiguration(self):
    return self._generic_sphinx_configuration
