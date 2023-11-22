import random

class Warrior:
    lvl_mapping = {
        1: 0,
        2: 48,
        3: 75,
        4: 112,
        5: 159,
        6: 212,
        7: 308,
        8: 324,
        9: 472,
        10: 615
    }
    statistic_mapping = {
        1: {'attack': 9, 'defence': 7, 'health': 108},
        2: {'attack': 11, 'defence': 9, 'health': 138},
        3: {'attack': 14, 'defence': 11, 'health': 170},
        4: {'attack': 17, 'defence': 13, 'health': 205},
        5: {'attack': 21, 'defence': 15, 'health': 235},
        6: {'attack': 24, 'defence': 18, 'health': 270},
        7: {'attack': 28, 'defence': 21, 'health': 320},
        8: {'attack': 32, 'defence': 25, 'health': 380},
        9: {'attack': 37, 'defence': 28, 'health': 470},
        10: {'attack': 42, 'defence': 33, 'health': 540}
    }
    def __init__(self, name):
        self.name = name
        self.attack = 9
        self.defence = 7
        self.health = 108
        self.level = 1
        self.experience = 0
        self.eq = {}

    def check_experience(self, experience):
        self.experience += experience
        if self.level < len(self.lvl_mapping) and self.experience >= self.lvl_mapping[self.level + 1]:
            self.level += 1
            self.update_statistics()

    def update_statistics(self):
        if self.level in self.statistic_mapping.keys():
            previous_stats = self.statistic_mapping[self.level - 1]
            stats = self.statistic_mapping[self.level]
            self.attack = stats['attack']
            self.defence = stats['defence']
            self.health = stats['health']
            print(f'You reached level {self.level}.')
            print('Update statistics:')
            print(f"HP = {self.health} (+{stats['health'] - previous_stats['health']})\n"
                  f"ATK = {self.attack} (+{stats['attack'] - previous_stats['attack']})\n"
                  f"DEF = {self.defence} (+{stats['defence'] - previous_stats['defence']})")

    def attack_moob(self, moob):
        dmg = random.uniform(self.attack - moob.defence / 8 - 5, self.attack - moob.defence / 12)
        moob.health -= dmg
        print(f'Your attack make {dmg:.1f} damage to {moob.name}')
        if moob.health <= 0:
            print(f'You killed {moob.name}')
            print(f'You gained {moob.exp} experience.')
            self.check_experience(moob.exp)


class Moob:
    moob_mapping = {
        'Troll': {'attack': (4, 7), 'defence': (2, 5), 'health': (63, 78), 'exp': (21, 23)},
        'Goblin': {'attack': (5, 9), 'defence': (3, 6), 'health': (70, 82), 'exp': (25, 28)}
    }
    def __init__(self, name):
        self.name = name
        moob_data = self.moob_mapping.get(name, None)
        self.attack = random.randint(*moob_data['attack'])
        self.defence = random.randint(*moob_data['defence'])
        self.health = random.randint(*moob_data['health'])
        self.exp = random.randint(*moob_data['exp'])


    def __repr__(self):
        return self.name

    def display_info(self):
        print(f'Monster: {self.name}, health: {self.health:.1f}, attack: {self.attack}, defence: {self.defence}')

    def attack_player(self, player):
        damage = random.uniform(self.attack - player.defence / 10 - 4, self.attack - player.defence / 10)
        player.health -= damage
        print(f'{self.name} attack you and make {damage:.1f} damages. {player.health:.1f} HP left.')


class Board:
    def __init__(self, player):
        self.player = player
        self.moob = None
    def battle(self, moob):
        self.moob = moob
        while True:
            self.moob.display_info()
            try:
                choice = int(input('What are you do?\n1. Attack\n2. Wait\n3. Escape\n'))
            except ValueError:
                print('Wrong format. Please try again.')
                continue
            if choice == 1:
                self.player.attack_moob(self.moob)
                if self.moob.health > 0:
                    self.moob.attack_player(self.player)
            elif choice == 2:
                self.moob.attack_player(self.player)
                continue
            elif choice == 3:
                print('Escape!')
                return
            else:
                print('Wrong choice.')

            if self.moob.health <= 0:
                return
            elif self.player.health <= 0:
                print('You are dead.')
                return

class Maps:
    def __init__(self):
        self.maps = [
            {'name': 'Forrest', 'moob': 'Troll'},
            {'name': 'Dessert', 'moob': 'Goblin'}
        ]
    def menu(self):
        player = Warrior('Tisuan')
        board = Board(player)
        print(f'Welcome in PIERZAG_GAME, {player.name}!')
        while True:
            print('1. Explore maps\n2. Exit game')
            try:
                choice = int(input('What would you like to do: '))
            except ValueError:
                print('Wrong format. You should enter 1, or 2.')
                continue
            if choice == 1:
                self.explore_map(board)
            elif choice == 2:
                return
            else:
                print('Wrong choice.')
    def initialize_map(self, map_name):
        for map_info in self.maps:
            if map_info['name'] == map_name:
                return map_info
        return None

    def explore_map(self, board):
        maps = [m['name'] for m in self.maps]
        while True:
            print(maps)
            map_name = input('Choose your map or press "X" to exit: ').title()
            if map_name == 'X':
                return
            moob_data = self.initialize_map(map_name)
            if moob_data:
                while True:
                    moob = Moob(moob_data['moob'])
                    print(f'{moob.name}!')
                    choice = input('What do you want to do? Fight or escape?: ').lower()
                    if choice == 'fight':
                        board.battle(moob)
                        return
                    elif choice == 'escape':
                        return
                    else:
                        print('Wrong choice')
                        continue
            else:
                print('Wrong choice, try again.')

class Item:

    items = {
        'weapon': {'name': 'Magic Sword', 'value': 21},
        'armor': {'name': 'Plate Armor', 'value': 19},
        'shield': {'name': 'Tiger Shield', 'value': 11}
    }

    def __init__(self, item_type='Unkown'):
        item_data = self.items.get(item_type, self.items['unkown'])
        self.name = item_data['name']
        self.value = item_data['value']
        self.item_type = item_type






map = Maps()
map.menu()
