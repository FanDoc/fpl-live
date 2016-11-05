#!/usr/bin/env python3

#
# Actor-based system to gather live scores for an FPL league table.
#
# Author: Dave Lillis (dave /at/ lill /dot/ is)
#

import fpl
import pykka

# actor to get data about a single team
class TeamFetcher(pykka.ThreadingActor):
   def on_receive(self,message):
      t = fpl.Team(message.get('team_id'), message.get('gameweek'))
      message.get('reply-to').tell({'team' : t })
      self.stop()

# actor to get data about a league
#   spawns a TeamFetcher for each team in the league and combines their replies
class LeagueFetcher(pykka.ThreadingActor):
   def trigger_team_check(self,team_id,gameweek):
      fetcher_ref = TeamFetcher.start(coordinator=self)
      fetcher_ref.tell({'team_id' : team_id, 'gameweek' : gameweek, 'reply-to' : self.actor_ref } )
   
   def on_receive(self, message):
      if message.get('league-id') is not None:
         self.league_id = message.get('league-id') 
         self.printer = message.get('reply-to')
         self.gameweek = fpl.Game().get_current_gameweek()
         self.league = fpl.League(self.league_id)
         self.participants = self.league.get_team_ids()
         self.received = 0
         self.league_table = []
         for p in self.participants:
            self.trigger_team_check(p,self.gameweek)
      else:
         self.league_table.append( message.get('team') )
         self.received += 1
         if self.received == len(self.participants):
            sorted_league = sorted( self.league_table, key=lambda x: x.get_total_points(), reverse=True )
            self.printer.tell({'league' : sorted_league, 'league-name' : self.league.get_name()})
            self.stop()
