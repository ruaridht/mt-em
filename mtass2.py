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

Self notes:
Run using tw (or tweet) to be tweeted when done, i.e.:
> tw python mtass2.py
"""

class EmAlg(object):
  def __init__(self):
    self.amItrue = YES #failsafe
  
  def _initUniform(self):
    print ">>> Initialising t(e|f) uniformly."

def main():
  print ">>> Let's go!"
  
  em = EmAlg()
  
  print ">>> Done! Goodbye."

if __name__=="__main__":
  main()