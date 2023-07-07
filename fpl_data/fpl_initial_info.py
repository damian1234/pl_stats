import requests
import json
import os

class FPL_Initial_Info:

    DATA_PATH = '/home/damian/betting_project/football_data/'
    NUM_OF_PLAYERS = 774  #2022/2023 season

    def __init__(self):
        pass

    def get_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_team_info(self):
        team_lookup = []
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        response = self.get_data(url)
        team_data = response.json()['teams']
        for team in team_data:
            team_info = {'id': team['id'], 'name': team['name']}
            team_lookup.append(team_info)

        return {'PLTeams': team_lookup}

    def get_player_info(self):
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        response = self.get_data(url)
        player_data = response.json()['elements']
        return {'PL_Players_Summary':  player_data}


    def get_max_id(self):
        data = self.get_player_info()['PL_Players_Summary']
        max_id = 0
        for player in data:
            if player['id'] > max_id:
                max_id = player['id']
        print(max_id)

    def get_player_info_per_gw(self):
        print('curling')
        url = 'https://fantasy.premierleague.com/api/element-summary/'
        with open(self.DATA_PATH + 'player_summaries.json', 'r') as my_file:
            player_summaries = json.load(my_file)
            for i in range(1, self.NUM_OF_PLAYERS + 1):
                full_url = url + str(i) + '/'
                print('curling')
                response = self.get_data(full_url)
                if response is None:
                    print('missing data')
                    continue
                print('data received')
                player_data = response.json()['history']
                directory_name = None
                for player in player_summaries['PL_Players_Summary']:
                    print(player)
                    if player['id'] == i:
                        directory_name = self.DATA_PATH + 'PlayersGWStats_22-23/' + player['first_name'] + ' ' + player['second_name']
                        # directory_name = directory_name.replace(' ', '_')
                        if not os.path.exists( directory_name):
                            os.makedirs(directory_name)
                count = 1
                for gw_data in player_data:
                    print(gw_data)
                    full_filename = directory_name + '/' + 'GW' + str(count)
                    self.write_json_file(full_filename, gw_data, '.json')
                    count = count + 1




    def write_json_file(self, filename, data, ext):
        print(os.path.isfile(filename+ext))
        if not os.path.isfile(filename+ext):
            print('new file')
            with open(filename+ext, 'w') as my_file:
                my_file.write(json.dumps(data))
