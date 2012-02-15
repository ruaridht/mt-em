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

There are ASCII problems with some of the foreign words.
"""

import sys
import time

# easy bools
YES=True
NO=False

# Defaults
CONVERGE=5 # Don't know what this should be
PROGRESS_WIDTH=40 # width of the progress bar

class EmAlg(object):
  def __init__(self, dicts):
    self.dicts = dicts
    
    self.eng_dict  = []
    self.eng_words = []
    self.for_dict  = []
    self.for_words = []
    self.sentence_pairs = [] # (english,foreign)
    
    self.possibilities = {} # list of possible initial translations of a word (using a set to remove dupes)
    self.trans_probs   = {} # t(e|f)
    
    self.count_ef = {} # count(e|f)
    self.total_f  = {} # total(f)
    self.total_s  = {} # s_total(e)
    
  # a simple progress bar just incase it all takes too long.
  def _progress(self, prog):
    sys.stdout.write("[%s] %i" % (" " * PROGRESS_WIDTH, prog))
    sys.stdout.flush()
    sys.stdout.write("\b" * (PROGRESS_WIDTH+1)) # return to start of line, after '['

    for i in xrange(PROGRESS_WIDTH):
        time.sleep(0.1) # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("\n")
    
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
  
  # Builds a sentence pair list
  def _sentencePairs(self):
    pairs = []
    for index in range(len(self.eng_dict)):
      pair = (self.eng_dict[index], self.for_dict[index])
      pairs.append(pair)
    
    self.sentence_pairs = pairs
  
  # Initialises the options for the result of a word to be translated.
  def _initPossibilities(self):
    possibilities = {} # a dictionary for key-value pairs (the key is the foreign word)
    #count_ef = {}
    #total = {}
    
    # This is very slow.. and inefficient.. but it does the job
    for word in self.for_words:
      word_poss = []
      
      for sent in self.for_dict:
        if word in sent:
          inSent = self.eng_dict[ self.for_dict.index(sent) ]
          word_poss = word_poss + inSent.split()
      word_poss = list( set(word_poss) )
      possibilities[word] = word_poss
      
      #count = [0 for w in word_poss]
      #count_ef[word] = count
      #total[word] = 0
      
      #self._progress()
    
    #print possibilities['buch']
    #print count_ef['buch']
    #print total['buch']
    self.possibilities = possibilities
    #self.count_ef = count_ef
  
  # Initialises the translation probabilities uniformly.
  def _initUniformTEF(self):
    trans_probs = {}
    
    for word in self.for_words:
      word_poss = self.possibilities[word]
      uniform_prob = 1.0 / len(word_poss)
      
      word_probs = dict( [(w, uniform_prob) for w in word_poss] )
      trans_probs[word] = word_probs
    
    self.trans_probs = trans_probs
  
  # sets the counts of words to zero
  def _zeroCountEF(self):
    count_ef = {}
    total_f = {}
    
    for word in self.for_words:
      word_poss = self.possibilities[word]
      count_zeroed = dict( [(w, 0) for w in word_poss] )
      count_ef[word] = count_zeroed
      
      total_f[word] = 0
      
    self.count_ef = count_ef
    self.total_f = total_f
    
  # Compute probabilities under a while loop
  def _converge(self):
    converged = NO
    cvgd = 0
    
    #print self.trans_probs
    
    while not(converged):
      # Try to converge
      self._zeroCountEF()
      
      for (e_s, f_s) in self.sentence_pairs:
        e_s_split = e_s.split()
        f_s_split = f_s.split()
        """
        for e in self.eng_words:
          self.total_s[e] = 0
        """
        for e in e_s_split:
          self.total_s[e] = 0
          for f in f_s_split:
            f_probs = self.trans_probs[f]
            self.total_s[e] += f_probs[e] # this is the probability of e given f
          
          for f in f_s_split:
            self.count_ef[f][e] += self.trans_probs[f][e] / self.total_s[e]
            self.total_f[f] += self.trans_probs[f][e] / self.total_s[e]
      
      for f in self.for_words:
        f_poss = self.possibilities[f]
        for e in f_poss:
          self.trans_probs[f][e] = self.count_ef[f][e] / self.total_f[f]
        """
        for e in self.eng_words:
          # if the key is not in the list of possibilities then skip (?)
          if (e in f):
            self.trans_probs[f][e] = self.count_ef[f][e] / self.total_f[f]
        """
      
      if (cvgd>=CONVERGE):
        converged = YES
      cvgd += 1
  
  # Prints the translation probabilities
  def _outputTEF(self):
    for key in self.trans_probs:
      print key, " : ", self.trans_probs[key]
  
  # Governs the entire translation process.
  def go(self):
    print ">>> Going.."
    self.eng_dict, self.eng_words = self._loadDict( self.dicts[1] )
    self.for_dict, self.for_words = self._loadDict( self.dicts[2] )
    self._sentencePairs()
    
    print ">>> Dictionaries loaded.."
    
    print ">>> Initialising probabilities.."
    self._initPossibilities()
    print ">>> Initialising t(e|f) uniformly.."
    self._initUniformTEF()
    
    print ">>> Performing convergence loop.."
    self._converge()
    
    print ">>> Printing translation probabilities ..."
    self._outputTEF()

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