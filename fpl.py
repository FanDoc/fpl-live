import requests
import time
   
#
# Simple library to wrap some Fantasy Premier League (FPL) API requests.
# FPL is located at https://fantasy.premierleague.com
#   
# Author: Dave Lillis (dave /at/ lill /dot/ is)
#

# wrapper for HTTP requests to quit if something goes wrong
#   (or game is updating)
def request(url):
   r = requests.get(url)
   if len(r.history) > 0:
      if r.url == 'https://fantasy.premierleague.com/updating/':
         print( 'Game is updating' )
         exit(1)
      else:
         print('Error fetching URL {}'.format(url))
         exit(1)
   return r
   
   
class Game:
   def __init__(self):
      r = request('https://fantasy.premierleague.com/drf/bootstrap-static')
      self.data = r.json();

   # find the current gameweek number
   def get_current_gameweek(self):
      i = 0
      while self.data['events'][i]['is_current'] is False:
         i += 1
         if i == 38:
            print( 'Game Over' )
            exit(1)
      return self.data['events'][i]['id']

class League:
   def __init__(self,league_id):
      r = request('https://fantasy.premierleague.com/drf/leagues-classic-standings/{}'.format(league_id))
      self.data = r.json()
      
   # get the IDs of the teams in this league
   def get_team_ids(self):
      ret = []
      for team in self.data['standings']['results']:
         ret.append( team['entry'] )
      return ret
      
   # get league name
   def get_name(self):
      return self.data['league']['name']

class Team:
   def __init__(self,team_id,gameweek):
      r = request('https://fantasy.premierleague.com/drf/entry/{}/event/{}'.format(team_id,gameweek))
      self.data = r.json()
      
   # get (live) points for this gameweek
   def get_points(self):
      return self.data['points']
      
   # get (live) total points
   def get_total_points(self):
      # total points already calculated by FPL + live points this gameweek - gameweek points already included in total
      return self.data['entry_history']['total_points'] + self.data['points'] - self.data['entry_history']['points']
      
   def get_manager_name(self):
      return '{} {}'.format(self.data['entry']['player_first_name'], self.data['entry']['player_last_name'])
      
   # get the name of the team   
   def get_name(self):
      return self.data['entry']['name']

         
      