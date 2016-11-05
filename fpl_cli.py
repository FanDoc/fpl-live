#!/usr/bin/env python3

#
# Command Line Script to print a live FPL table
#
# Usage: ./fpl_cli.py league_id
#
# Author: David Lillis (dave /at/ lill /dot /is)
#

from pykka_fpl import LeagueFetcher
from collections import OrderedDict
import pykka
import sys

class LeaguePrinter(pykka.ThreadingActor):
   def __init__(self, league_id):
      super(LeaguePrinter, self).__init__()
      self.league_id = league_id
   
   def on_start(self):
      # create new actor instance to gather the data
      self.league_fetcher = LeagueFetcher.start()
      # request data about league_id
      self.league_fetcher.tell({'league-id': self.league_id, 'reply-to': self.actor_ref })
      
   def on_receive(self, message):
      # league data (list of dicts)
      league = message.get('league')

      print('-' * len(message.get('league-name')))
      print(message.get('league-name'))
      print('-' * len(message.get('league-name')))
      for t in league:
         print('{} {} {} '.format(t.get_total_points(), t.get_points(), t.get_manager_name()))
      self.stop()

if __name__ == '__main__':
   if len(sys.argv) != 2:
      print( 'FPL Live League\nUsage:\n{} league-id'.format(sys.argv[0]))
      exit(0)
   else:
      actor_ref = LeaguePrinter.start(league_id=sys.argv[1])
