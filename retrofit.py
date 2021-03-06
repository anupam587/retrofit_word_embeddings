# -*- coding: utf-8 -*-
import numpy
from copy import deepcopy
import re
import sys
import os

# retrofitting word vectors using semantic lexicon
def retrofit_model(word_vec_data, lexicon_data, total_iteration):
  retrofit_wordvecs = deepcopy(word_vec_data)
  wordvec_vocab = set(retrofit_wordvecs.keys())
  neighbour_words = wordvec_vocab.intersection(set(lexicon_data.keys()))

  for i in range(total_iteration):
    for word in neighbour_words:
      neighbours = set(lexicon_data[word]).intersection(wordvec_vocab)
      neighbours_len = len(neighbours)
      
      if neighbours_len == 0:
        continue
      
      final_vec = neighbours_len * word_vec_data[word]
      
      for nbr_word in neighbours:
        final_vec += retrofit_wordvecs[nbr_word]
      retrofit_wordvecs[word] = final_vec/(neighbours_len*2)
      
  return retrofit_wordvecs

# write output retrofit word vector file
def write_retrofit_vectors(retrofit_vectors, output_file):
  sys.stderr.write('\noutput file is '+output_file+'\n')

  outfile_obj = open(output_file, 'w')  
  for word, values in retrofit_vectors.items():
    outfile_obj.write(word+' ')
    for val in retrofit_vectors[word]:
      outfile_obj.write('%.5f' %(val)+' ')
    outfile_obj.write('\n')      
  outfile_obj.close()

# read sample word vector file and normalize it
def read_word_vector_file(filename):
  sys.stderr.write("sample word vector file is: "+filename+" \n")

  file_obj = open(filename, 'r')
  word_vectors = {}
  
  for line in file_obj:
    line = line.strip().lower()
    word = line.split()[0]
    word_vectors[word] = numpy.zeros(len(line.split())-1, dtype=float)
    for index, vecVal in enumerate(line.split()[1:]):
      word_vectors[word][index] = float(vecVal)
    
    norm = numpy.linalg.norm(word_vectors[word])
    word_vectors[word] /= norm
    
  return word_vectors
  

isNumber = re.compile(r'\d+.*')
def normalize_word(word):
  if isNumber.search(word.lower()):
    return '$$number$$'
  elif re.sub(r'\W+', '', word) == '':
    return '$$punct$$'
  else:
    return word.lower()

# read lexicon file in dictionary format
def read_lexicon_file(filename):
  lexicon = {}
  for line in open(filename, 'r'):
    words = line.lower().strip().split()
    lexicon[normalize_word(words[0])] = [normalize_word(word) for word in words[1:]]
  return lexicon

cwd = os.getcwd()

word_vec_data = read_word_vector_file(cwd + "/sample_word_vec.txt")
lexicon_data = read_lexicon_file(cwd + "/framenet_lexicon.txt")
num_iteration = 10
output_file = cwd + "/retrofit_word_vec.txt"
  
retrofit_vectors = retrofit_model(word_vec_data, lexicon_data, num_iteration) 
write_retrofit_vectors(retrofit_vectors, output_file)