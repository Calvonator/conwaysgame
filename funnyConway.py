import arcade

#Number of rows/columns in the grid
ROW_COUNT = 50
COLUMN_COUNT = 50

#The width, height and margin of individual cells
WIDTH = 15
HEIGHT = 15
MARGIN = 1

SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN

SCREEN_TITLE = "Conway's Game Of Life"

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



#Change to MyBoard after testing (class is used for the actual conway game)
class MyConway(arcade.Window):


    def __init__(self, width, height, grid, title):
        
        super().__init__(width, height, title)

        self.grid = grid


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
                elif self.grid[row][col] == 2:
                    self.grid_sprite_list[pos].color = arcade.color.BLUE

                elif self.grid[row][col] == 3:
                    self.grid_sprite_list[pos].color = arcade.color.RED
                
                else:
                    self.grid_sprite_list[pos].color = arcade.color.GREEN


    def conwayIteration(self):

        _changedGrid = []
        
        for row in range(ROW_COUNT):

            _changedGrid.append([])
            for col in range(COLUMN_COUNT):
                _changedGrid[row].append(0)

        #print(_changedGrid)
        #print("Changed Grid")
        
        for row in range(ROW_COUNT):
            for col in range(COLUMN_COUNT):

                cellStatus = self.findNeighbours(row, col)
                
                #change these to if statements back to 0
                if cellStatus == 'underpopulation':
                    _changedGrid[row][col] = 2

                elif cellStatus == 'overcrowding':
                    _changedGrid[row][col] = 3
                    

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

        if neighbourCount < 2:
            result = 'underpopulation'
        elif neighbourCount == 2:
            result = 'survival'
        elif neighbourCount > 3:
            result = 'overcrowding'
        elif neighbourCount == 3:
            result = 'reproduction' 

        return result #Return int code values instead if speed becomes an issue
               

    def on_draw(self):
        arcade.start_render()
        
        self.grid_sprite_list.draw()
        #arcade.finish_render()

        
def startingBoard():
    grid = MyBoard(SCREEN_WIDTH, SCREEN_HEIGHT, "Conway's Game of Life | Starting Grid")
    arcade.run()
    return grid.grid          
          

def main():

    startingGrid = startingBoard()
        
    board = MyConway(SCREEN_WIDTH, SCREEN_HEIGHT, startingGrid, SCREEN_TITLE)

    
    #board.resync_grid_with_spritelist()
    #arcade.run()
    arcade.start_render()
    for _ in range(3):
    
        board.conwayIteration()
        board.resync_grid_with_spritelist()
        
        
    #arcade.finish_render()
    arcade.run()
    
    


if __name__ == "__main__":
    main()
