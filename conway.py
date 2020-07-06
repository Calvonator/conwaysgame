import arcade, json

#Number of rows/columns in the grid
ROW_COUNT = 100
COLUMN_COUNT = 100

#The width, height and margin of individual cells
WIDTH = 15
HEIGHT = 15
MARGIN = 1

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

SCREEN_TITLE = "Conway's Game Of Life"


class TextButton:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False




#Class used for generating the starting grid used by the Conway game class
class MyBoard(arcade.Window):


    def __init__(self, width, height, title):
        
        super().__init__(width, height, title)

        self.grid = [] #[[[] for row in range(ROW_COUNT)] for col in range(COLUMN_HEIGHT)]



        for row in range(ROW_COUNT):

            self.grid.append([])
            for col in range(COLUMN_COUNT):
                self.grid[row].append(0)

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()

        for row in range(COLUMN_COUNT):
            for col in range(ROW_COUNT):
                x = col * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)

        

    def resync_grid_with_spritelist(self):
        self.shape_list = arcade.ShapeElementList()
        
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + col
        
                if self.grid[row][col] == 0:
                    
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN


    def on_mouse_press(self, x, y, button, modifiers):

        col = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        #Ensure the location is within the grid
        if row < ROW_COUNT and col < COLUMN_COUNT:

            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            else:
                self.grid[row][col] = 0

        self.resync_grid_with_spritelist()
        
                
        


    def on_draw(self):
        arcade.start_render()
        
        self.grid_sprite_list.draw()


def startingBoard():
    grid = MyBoard(SCREEN_WIDTH, SCREEN_HEIGHT, "Conway's Game of Life | Starting Grid")
    arcade.run()
    return grid.grid


class NextButton(TextButton):
    
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Start", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


#Button Stuff
def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class ConwayWindow(arcade.Window):
    

    def __init__(self, width, height, grid, title):
        
        super().__init__(width, height, title)

        self.grid = grid
        self.gen = 1
        self.button_list = []

        next_button = NextButton(60, 570, self.display_generations)
        self.button_list.append(next_button)

        arcade.set_background_color(arcade.color.BLACK)

        self.grid_sprite_list = arcade.SpriteList()


        for row in range(COLUMN_COUNT):
            for col in range(ROW_COUNT):
                x = col * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, arcade.color.WHITE)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)


    def resync_generation_with_spritelist(self, gen):
        self.shape_list = arcade.ShapeElementList()
        
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):
                pos = row * COLUMN_COUNT + col
        
                if self.grid[gen][row][col] == 0:
                    self.grid_sprite_list[pos].color = arcade.color.WHITE
                elif self.grid[gen][row][col] == 1:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN

    def display_generations(self):     
        self.resync_generation_with_spritelist(self.gen)
        self.gen += 1
     
        
    def on_draw(self):
        arcade.start_render()
        
        self.grid_sprite_list.draw()
        for button in self.button_list:
            button.draw()
        
    #Button stuff
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        check_mouse_release_for_buttons(x, y, self.button_list)






class Conway():

    def __init__(self, grid):
        self.grid = grid


    def conwayIteration(self):

        _changedGrid = []
        
        for row in range(ROW_COUNT):

            _changedGrid.append([])
            for _ in range(COLUMN_COUNT):
                _changedGrid[row].append(0)

        #print(_changedGrid)
        #print("Changed Grid")
        
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):

                cellStatus = self.findNeighbours(row, col)
                
                #change these to if statements back to 0
                if cellStatus == 'underpopulation':
                    _changedGrid[row][col] = 0

                elif cellStatus == 'overcrowding':
                    _changedGrid[row][col] = 0
                    

                elif cellStatus == 'reproduction' or cellStatus == 'survival':
                    _changedGrid[row][col] = 1
                    
        self.grid = _changedGrid
        
        #for row in range(25):
        
            #print(self.grid[row])

        #for row in range(25):
        
            #print(_changedGrid[row])

        
        
    def findNeighbours(self, row, col):
        neighbourCount = 0
        try:
            if self.grid[row - 1][col - 1] == 1:
                neighbourCount += 1
                
            if self.grid[row - 1][col] == 1:
                neighbourCount += 1
                
            if self.grid[row - 1][col + 1] == 1:
                neighbourCount += 1

            if self.grid[row][col - 1] == 1:
                neighbourCount += 1
            
            if self.grid[row][col + 1] == 1:
                neighbourCount += 1

            if self.grid[row + 1][col - 1] == 1:
                neighbourCount += 1
                
            if self.grid[row + 1][col] == 1:
                neighbourCount += 1
                
            if self.grid[row + 1][col + 1] == 1:
                neighbourCount += 1
        except:
            pass



        if self.grid[row][col] == 1 and neighbourCount == 2 or neighbourCount == 3:
            result = 'survival'

        elif self.grid[row][col] == 1 and neighbourCount > 3:
            result = 'overpopulation'

        elif self.grid[row][col] == 0 and neighbourCount == 3:
            result = 'reproduction'

        else:
            result = 'underpopulation'

    
        return result #Return int code values instead if speed becomes an issue
    
def iterGen(grid, noOfGen):

    conwayGenerations = []

    game = Conway(grid)

    for _ in range(int(noOfGen)):
        game.conwayIteration()
        conwayGenerations.append(game.grid)

    
    return conwayGenerations


def displayMatrix(grid, gens, noOfColumns):

    for gen in range(int(gens)):
        print("\n\nGeneration: " + str(gen) + "\n\n")
        for row in range(int(noOfColumns)):
            print(grid[gen][row])

def importStartingGrid(location):
    grid = []

    with open(location, "r") as file:
        grid = json.load(file)
            
    return grid

def saveStartingGrid(grid):
        with open("file.txt", "w") as f:
            json.dump(grid, f, indent=2)


def main():

    while True:
        choice = input("Would you like [1] import or [2] generate a starting grid?")
        if choice == '1':
            fileLocation = input("Please enter the file locaiton: ")
            startingGrid = importStartingGrid(fileLocation)
            break

        elif choice == '2':
            startingGrid = startingBoard()
            saveStartingGrid(startingGrid)

            break
    





    noOfGens = input("Please input the number of generations: ") 
    #noOfGens = 6
    generations = iterGen(startingGrid, noOfGens)
    #displayMatrix(generations, noOfGens, ROW_COUNT)
    board = ConwayWindow(SCREEN_WIDTH, SCREEN_HEIGHT, generations, SCREEN_TITLE)


    
    #board.resync_generation_with_spritelist(0)
    arcade.run()
         
    


        


if __name__ == "__main__":
    main()
