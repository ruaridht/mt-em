#!/usr/bin/env python
"""
Machine Translation
EM Algorithm for IBM Model 1
Ruaridh Thomson s0786036

Notes:
There may be ASCII problems with some of the foreign words.
There are word possibility problems when punctuation is removed.
Progress bar code is for sanity.

Notes for self:
> tw python mtass2.py toy.en toy.de
> tw time python mtass2.py test2000.lowercase.en test2000.lowercase.de
"""

import sys
import time
from progressbar import *
import string

# easy bools
YES=True
NO=False

# Defaults
CONVERGE=70 # Don't know what this should be
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
    
  # Loads a dictionary of sentences and creates a dict of words.
  def _loadDict(self, dic):
    out_dict  = []
    out_words = []
    f = open(dic, 'r')
    
    for line in f.readlines():
      #out = line.rstrip() # remove end of line chars
      #outline = line.translate(string.maketrans("",""), string.punctuation) # remove punctuation?
      #out_dict.append(outline)
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
    
    pbar = ProgressBar().start()
    count = 1.0 # not an index
    clen = len(self.for_words)
    
    # This is very slow.. and inefficient.. but it does the job
    for word in self.for_words:
      word_poss = []
      
      for sent in self.for_dict:
        if word in sent:
          inSent = self.eng_dict[ self.for_dict.index(sent) ]
          word_poss = word_poss + inSent.split()
          
      word_poss = list( set(word_poss) )
      possibilities[word] = word_poss
      
      percent_done = count / clen
      percent_done = round(percent_done * 100)
      pbar.update(percent_done)
      count += 1.0
    
    pbar.finish()  
    
    #print possibilities['buch']
    #print count_ef['buch']
    #print total['buch']
    self.possibilities = possibilities
  
  # Initialises the translation probabilities uniformly.
  def _initUniformTEF(self):
    trans_probs = {}
    
    for word in self.for_words:
      word_poss = self.possibilities[word]
      if (len(word_poss)==0):
        print word, word_poss
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
    
    while not(converged):
      pbar = ProgressBar().start()
      pbcount = 1.0
      pblen = len(self.sentence_pairs)
      
      # Try to converge
      self._zeroCountEF()
      
      for (e_s, f_s) in self.sentence_pairs:
        e_s_split = e_s.split()
        f_s_split = f_s.split()
        
        for e in e_s_split:
          self.total_s[e] = 0
          for f in f_s_split:
            f_probs = self.trans_probs[f]
            
            if (e not in f_probs):
              #punctuation problems, though if we remove punctuation we run into a load of new problems
              continue
            
            self.total_s[e] += f_probs[e] # this is the probability of e given f
          
          for f in f_s_split:
            if (e not in self.trans_probs[f]):
              continue
            self.count_ef[f][e] += self.trans_probs[f][e] / self.total_s[e]
            self.total_f[f] += self.trans_probs[f][e] / self.total_s[e]
          
        percent_done = pbcount / pblen
        percent_done = round(percent_done * 100)
        pbar.update(percent_done)
        pbcount += 1.0
      
      for f in self.for_words:
        f_poss = self.possibilities[f]
        for e in f_poss:
          self.trans_probs[f][e] = self.count_ef[f][e] / self.total_f[f]
      
      if (cvgd>=CONVERGE):
        converged = YES
      cvgd += 1
      
      pbar.finish()
      print "    Loop", cvgd, "completed."
  
  # Prints the translation probabilities
  def _outputTEF(self):
    f = open('trans_table.txt','w')
    g = open ('viterbi_align.txt', 'w')
    for word in self.trans_probs:
      word_probs = self.trans_probs[word]
      items = sorted(word_probs.iteritems(), key=lambda (k,v): (v,k))
      items.reverse()
      (top, va) = items[0]
      g.write(word + " = " + top + "\n")
      f.write(word + ":- ")
      for (w, p) in items[:5]:
        f.write("(" + w + ", " + str(p) + ")" + ", ")
      f.write("\n")
    f.close()
    g.close()
  
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