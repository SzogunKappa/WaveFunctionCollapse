import pygame
import random

available_tiles = {
    'empty': {'image': pygame.image.load('images/empty.png'), 'top_val': 0, 'left_val': 0, 'right_val': 0,
              'bottom_val': 0},
    'straight': {'image': pygame.image.load('images/up-down.png'), 'top_val': 1, 'left_val': 0, 'right_val': 0,
                 'bottom_val': 1},
    'curve b-r': {'image': pygame.image.load('images/down-right.png'), 'top_val': 0, 'left_val': 0, 'right_val': 1,
                  'bottom_val': 1},
    'curve b-l': {'image': pygame.image.load('images/down-left.png'), 'top_val': 0, 'left_val': 1, 'right_val': 0,
                  'bottom_val': 1},
    'curve t-r': {'image': pygame.image.load('images/up-right.png'), 'top_val': 1, 'left_val': 0, 'right_val': 1,
                  'bottom_val': 0},
    'curve t-l': {'image': pygame.image.load('images/up-left.png'), 'top_val': 1, 'left_val': 1, 'right_val': 0,
                  'bottom_val': 0},
    'intersection': {'image': pygame.image.load('images/intersection.png'), 'top_val': 0, 'left_val': 1, 'right_val': 1,
                     'bottom_val': 1},
}


class Board:

    def __init__(self, width: int = 800, length: int = 800, tile_size=(100, 100)):
        self.width = width
        self.length = length
        self.columns = int(width / tile_size[0])
        self.rows = int(length / tile_size[1])
        self.head = None
        self.number_tiles = 0
        self.head_row = None
        self.tail = None
        self.visualization = []
        self.line = []
        self.is_done = False

    def add_tile(self, tile):
        if self.head == None:  # """If there is no tile in board"""
            tile.coordinates = [0, 0]
            self.head = tile
            self.head_row = tile
            self.tail = tile
            self.line.append(len(tile.possible_tiles))
        else:
            if self.number_tiles % self.columns == 0:  # """If the new tile will go into new line"""
                tile.coordinates = [self.head_row.coordinates[0], self.head_row.coordinates[1] + 1]
                self.head_row.bottom = tile
                tile.top = self.head_row
                self.head_row = tile
                self.head = tile
                self.visualization.append(self.line.copy())
                self.line = [len(tile.possible_tiles)]
            else:  # """if new tile go to the same row as previous tile"""
                tile.coordinates = [self.head.coordinates[0] + 1, self.head.coordinates[1]]
                if self.number_tiles / self.columns >= 1 and self.columns > 1:
                    self.head.top.right.bottom = tile
                    tile.top = self.head.top.right

                self.head.right = tile
                tile.left = self.head
                self.head = tile
                self.line.append(len(tile.possible_tiles))
        self.number_tiles += 1
        if self.rows * self.columns == self.number_tiles:
            self.visualization.append(self.line.copy())

    def navigate(self, position: int):
        current = self.tail
        while position >= self.columns:
            current = current.bottom
            position -= self.columns
        for x in range(int(position)):
            current = current.right
        return current

    def create(self):
        tile_number = self.rows * self.columns
        for tiles in range(int(tile_number)):
            node = Tile()
            x.add_tile(node)

    def random_tile(self):
        print(self.best_to_pick())
        return random.choice(self.best_to_pick())

    def best_to_pick(self):
        global available_tiles
        min_list = []
        min = int(len(available_tiles.keys()))
        for yi, y in enumerate(self.visualization):
            for xi, x in enumerate(y):
                if min > x and x > 0:
                    min = x
                    min_list = [yi * self.columns + xi]
                elif min == x:
                    min_list.append(yi * self.columns + xi)
        return min_list

    def change_tile(self, tile_id):
        tile = self.navigate(tile_id)
        tile.random_pick()

    def check_visualization(self):
        tile = self.tail
        small_tail = self.tail
        big_hold = []
        hold = []
        for y in range(self.rows):
            for x in range(self.columns):
                hold.append(len(tile.possible_tiles))
                tile = tile.right
            small_tail = small_tail.bottom
            tile = small_tail
            big_hold.append(hold.copy())
            hold = []
        self.visualization = big_hold.copy()

    def output(self):
        tile = self.tail
        small_tail = self.tail
        for y in range(self.rows):
            for x in range(self.columns):
                if len(tile.possible_tiles) == 0:
                    tile.display()
                tile = tile.right
            small_tail = small_tail.bottom
            tile = small_tail

class Tile:

    def __init__(self, x=0, y=0, width=100, length=100):
        global available_tiles

        # identities of a tile
        self.coordinates = [x, y]
        self.type = None
        self.image = None
        self.top_value = None
        self.bottom_value = None
        self.right_value = None
        self.left_value = None
        self.possible_tiles = list(available_tiles.keys())
        self.width = width
        self.length = length

        # links with different tiles
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

        # position of tile
        self.x = x
        self.y = y

    def __str__(self):
        return (
            f"type: {self.type}, top: {self.top_value}, bottom: {self.bottom_value}, right: {self.right_value}, left: {self.left_value}")

    def set(self, type):
        if type in self.possible_tiles:
            global available_tiles
            selected_tile = available_tiles[type]
            self.image = selected_tile['image']
            self.type = type
            self.top_value = selected_tile['top_val']
            self.bottom_value = selected_tile['bottom_val']
            self.left_value = selected_tile['left_val']
            self.right_value = selected_tile['right_val']

            # checking if tile have neighbors then change available tiles sets for them
            if self.top != None:
                self.top.check_possible('bottom_val', self.top_value)
            if self.bottom != None:
                self.bottom.check_possible('top_val', self.bottom_value)
            if self.left != None:
                self.left.check_possible('right_val', self.left_value)
            if self.right != None:
                self.right.check_possible('left_val', self.right_value)
        elif len(self.possible_tiles) == 0:
            pass
        else:
            print('something wrong!')
        self.possible_tiles = []

    def check_possible(self, side: str, side_value: int):
        # side: side of a tile that you want base your possible tile set
        # side_value : value of that side
        global available_tiles
        hold = self.possible_tiles.copy()
        for type in self.possible_tiles:
            check = available_tiles[type]
            if side_value != check[side]:
                hold.remove(type)
        self.possible_tiles = hold.copy()

    def display(self):
        self.set_position()
        scrn.blit(self.image, (self.x, self.y))

    def random_pick(self):
        picked = random.choice(self.possible_tiles)
        self.set(picked)

    def set_position(self):
        self.x = self.coordinates[0] * self.width
        self.y = self.coordinates[1] * self.length


if __name__ == "__main__":
    pygame.init()
    scrn = pygame.display.set_mode((800, 800))
    x = Board()
    x.create()
    running = True
    while running:  # loop listening for end of game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        next = input('n: next, r: reset')
        if next == 'n':
            x = Board()
            x.create()
            for i in range(64):
                a = x.random_tile()
                x.change_tile(a)
                x.check_visualization()
                x.output()
                pygame.display.flip()
            print(x.visualization)