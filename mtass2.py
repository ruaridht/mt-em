#!/usr/bin/env python
"""
Machine Translation
EM Algorithm for IBM Model 1
Ruaridh Thomson s0786036

Notes:
This program outputs:
1. A table (in the form of a matrix) containing the word translation probabilities that were learned
2. The most likely alignment (Viterbi alignment) for each sentence pair in the training data.

For (1) there is a lot of data and a suitable data structure will need to be used (i.e. not a matrix).

t(e|f) is the translation probability of getting 'e' given 'f'.
First calculate the alignments using the alignment function.

Self notes:
Run using tw (or tweet) to be tweeted when done, i.e.:
> tw python mtass2.py
"""

import sys

# easy bools
YES=True
NO=False

CONVERGE=5

class EmAlg(object):
  def __init__(self, dicts):
    self.dicts = dicts
    
    self.eng_dict  = []
    self.eng_words = []
    self.for_dict  = []
    self.for_words = []
    
    self.possibilities = {} # list of possible initial translations of a word (using a set to remove dupes)
    self.trans_probs   = [] 
    
  # Loads a dictionary of sentences and creates a dict of words.
  def _loadDict(self, dic):
    out_dict  = []
    out_words = []
    f = open(dic, 'r')
    
    for line in f.readlines():
      out_dict.append( line.rstrip() )
      out_words = out_words + line.split()
      
    f.close()
    
    out_words = list( set(out_words) ) # remove dupes
    
    return out_dict, out_words
  
  # Initialises the options for the result of a word to be translated.
  def _initPossibilities(self):
    possibilities = {} # a dictionary for key-value pairs (the key is the foreign word)
    
    # This is very slow.. and inefficient.. but it does the job
    for word in self.for_words:
      word_poss = []
      for sent in self.for_dict:
        if word in sent:
          inSent = self.eng_dict[ self.for_dict.index(sent) ]
          word_poss = word_poss + inSent.split()
      word_poss = list( set(word_poss) )
      possibilities[word] = word_poss
    
    #print possibilities['buch']
    self.possibilities = possibilities
  
  # Initialises the translation probabilities uniformly.
  def _initUniformTEF(self):
    trans_probs = {}
    
    for word in self.for_words:
      word_poss = self.possibilities[word]
      uniform_prob = 1.0 / len(word_poss)
      
      word_probs = dict( [(w, uniform_prob) for w in word_poss] )
      trans_probs[word] = word_probs
    
    self.trans_probs = trans_probs
  
  # Compute probabilities under a while loop
  def _converge(self):
    converged = NO
    cvgd = 0
    
    while not(converged):
      
      # Try to converge
      
      if (cvgd>=CONVERGE):
        converged = YES
      cvgd += 1
    
  # Governs the entire translation process.
  def go(self):
    print ">>> Going.."
    self.eng_dict, self.eng_words = self._loadDict( self.dicts[1] )
    self.for_dict, self.for_words = self._loadDict( self.dicts[2] )
    print ">>> Dictionaries loaded.."
    
    print ">>> Initialising probabilities.."
    self._initPossibilities()
    print ">>> Initialising t(e|f) uniformly.."
    self._initUniformTEF()
    print ">>> Performing convergence loop.."
    #self._converge()

# Just to make sure the dicts are actually there and in the right order
def verifyArgs(args):
  if len(args) < 3:
    print ">>> ERROR: Second dictionary missing. exit()"
    exit()

def main():
  print ">>> Let's go!"
  
  args = sys.argv
  verifyArgs(args)
  
  em = EmAlg(args)
  em.go()
  
  print ">>> Done! Goodbye."

if __name__=="__main__":
  main()