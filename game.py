import random

class Warrior:
    lvl_mapping = {
        1: 0,
        2: 31,
        3: 65,
        4: 107,
        5: 159,
        6: 212,
        7: 308,
        8: 412,
        9: 563,
        10: 750
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
        self.eq = set()

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

            for item in self.eq:
                if item.attack_value is not None:
                    self.attack += item.attack_value
                if item.defend_value is not None:
                    self.defence += item.defend_value

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
            print(f'You killed {moob.name}.')
            print(f'You gained {moob.exp} experience.')
            self.check_experience(moob.exp)

    def add_to_inventory(self, item):
        if isinstance(item, Item):
            print(f'You dropped {item.name}')
            if item.name not in self.eq:
                self.eq.add(item)
                print(f'Added {item.name} to inventory.')
                if item.attack_value is not None:
                    self.attack += item.attack_value
                if item.defend_value is not None:
                    self.defence += item.defend_value
            else:
                print(f'You already have {item.name}')
        else:
            print('Error')

    def check_stats(self):
        print(f'Attack: {self.attack}\n'
              f'Defence: {self.defence}\n'
              f'Health: {self.health}')

class Moob:
    moob_mapping = {
        'Troll': {'attack': (4, 7), 'defence': (2, 5), 'health': (63, 78), 'exp': (21, 23)},
        'Goblin': {'attack': (5, 9), 'defence': (3, 6), 'health': (70, 82), 'exp': (25, 28)},
        'Orc': {'attack': (9, 11), 'defence': (9, 10), 'health': (80, 93), 'exp': (31, 38)}
    }
    def __init__(self, name):
        self.name = name
        moob_data = self.moob_mapping.get(name)
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

    def drop(self):
        if random.random() < 0.1:
            item_type = random.choice(['weapon', 'armor', 'shield'])
            item_date = Item.items.get(item_type)
            if item_date:
                return Item(item_type)
        else:
            return None



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
                else:
                    dropped_item = moob.drop()
                    if dropped_item:
                        self.player.add_to_inventory(dropped_item)
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
            {'name': 'Dessert', 'moob': 'Goblin'},
            {'name': 'Swamp', 'moob': 'Orc'}
        ]
    def menu(self):
        player = Warrior('Tisuan')
        board = Board(player)
        print(f'Welcome in PIERZAG_GAME, {player.name}!')
        while True:
            print('1. Explore maps\n2. Check stats\n3. Exit game')
            try:
                choice = int(input('What would you like to do: '))
            except ValueError:
                print('Wrong format. You should enter 1, or 2.')
                continue
            if choice == 1:
                self.explore_map(board)
            elif choice == 2:
                player.check_stats()
            elif choice == 3:
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
        'weapon': {'name': 'Magic Sword', 'attack_value': 21},
        'armor': {'name': 'Plate Armor', 'defend_value': 19},
        'shield': {'name': 'Tiger Shield', 'defend_value': 11}
    }

    def __init__(self, item_type='Unknown'):
        item_data = self.items.get(item_type)
        self.name = item_data['name']
        self.item_type = item_type
        self.attack_value = item_data.get('attack_value')
        self.defend_value = item_data.get('defend_value')







map = Maps()
map.menu()
