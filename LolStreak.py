"""
A study to prove that "losers queue" and "winners queue" are not real or significant in league of legends ranked games.
They are a desperate attempt to justify a bad performance.

This uses the riot games api https://euw1.api.riotgames.com
and is by no means beautiful

"""
#%% Imports
import requests
import matplotlib.pyplot  as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np


#%% Methods
def puuid(summoner_name):
    summoner_api_url = f'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}'
    response = requests.get(summoner_api_url)
    summoner_info = response.json()
    puuid = summoner_info['puuid']
    return puuid

def matchIDs(puuid, number_of_games): # Extract match IDs of last ranked solo games
    match_list_api_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count={number_of_games}&api_key={api_key}'
    match_list_response = requests.get(match_list_api_url)
    recent_matches_list = match_list_response.json()
    return recent_matches_list

def determineWinOrLoss(match_id):
    '''
    Takes a match ID and returns the outcome for the summoner.

    Parameters
    ----------
    match_id : string
        match ID

    Returns
    -------
    win : boolean
        True = Win
        False = Loss
    '''
    match_api_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
    match_response = requests.get(match_api_url)
    match = match_response.json()
    index = match['metadata']['participants'].index(puuid)
    outcome = match['info']['participants'][index]['win']
    return outcome

def countStreaks(recent_matches_list):
    streak_counter = 1
    previous_outcome = None
    streak_list = []
    for match in recent_matches_list:
        outcome = determineWinOrLoss(match)
        #print(f'Match_ID: {match} -> {outcome}')
        if outcome == previous_outcome:
            streak_counter += 1
            previous_outcome = outcome
        else:
            # print(streak_counter)
            if previous_outcome == False:
                streak_list.append(-streak_counter)
            else:
                streak_list.append(streak_counter)
            streak_counter = 1
            previous_outcome = outcome
    return streak_list

#%% Main
summoner_name = 'Xanoblade'
number_of_games = 10 # up to 99 with the test version of API
api_key = 'RGAPI-b05cce0f-d21c-4b23-abbd-fcf06105fc3a' # needs to be recreated after 24h

puuid = puuid(summoner_name)
recent_matches_list = matchIDs(puuid, number_of_games)
streak_list = countStreaks(recent_matches_list)

match_api_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{recent_matches_list[0]}?api_key={api_key}'
match_response = requests.get(match_api_url)
match = match_response.json()
index = match['metadata']['participants'].index(puuid)
data_keys = match['info']['participants'][index].keys()
print(data_keys)
print(match['info']['participants'][index]['eligibleForProgression'])




#%% Plotting
fig, ax = plt.subplots()

number_bins = abs(max(np.array(streak_list).max(), np.array(streak_list).min(), key=abs))
ax.hist(streak_list, bins=np.arange(-number_bins - 1, number_bins + 1) + 0.5, alpha=0.7, color='blue', edgecolor='black')

plt.title(summoner_name)
plt.xlabel('Streak')
plt.ylabel('Häufigkeit')
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.show()
"""
"""