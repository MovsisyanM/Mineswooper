from sys import platform
import random
import os

# thanks to https://www.askpython.com/python/examples/create-minesweeper-using-python 
# for guiding us through the implementation of the game
 
def print_map(mine_values, n):
    """Prints the map to the screen"""
 
    print()
    print("Mineswooper by Mher Movsisyan, Diana Sargsyan, and Lilit Beglaryan")
    print()
 
    st = "   "
    for i in range(n):
        st = st + str(i + 1).rjust(6)
    print(st)   
 
    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______" 
            print(st)
 
        st = "     "
        for col in range(n):
            st = st + "|     "
        print(st + "|")
         
        st = str(r + 1).ljust(5)
        for col in range(n):
            st = st + "|  " + str(mine_values[r][col]) + "  "
        print(st + "|") 
 
        st = "     "
        for col in range(n):
            st = st + "|_____"
        print(st + '|')
 
    print()
  
# Function for setting up Mines
def set_mines(numbers, mines_no, n):
    # Track of number of mines already set up
    count = 0
    while count < mines_no:
 
        # Random number from all possible grid positions 
        val = random.randint(0, n*n-1)
 
        # Generating row and column from the number
        r = val // n
        col = val % n
 
        # Place the mine, if it doesn't already have one
        if numbers[r][col] != -1:
            count = count + 1
            numbers[r][col] = -1
            
    return numbers
 
# Function for setting up the other grid values
def set_values(numbers, n):
    # Loop for counting each cell value
    for r in range(n):
        for col in range(n):
 
            # Skip, if it contains a mine
            if numbers[r][col] == -1:
                continue
 
            # Check up  
            if r > 0 and numbers[r-1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check down    
            if r < n-1  and numbers[r+1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check left
            if col > 0 and numbers[r][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check right
            if col < n-1 and numbers[r][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-left    
            if r > 0 and col > 0 and numbers[r-1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-right
            if r > 0 and col < n-1 and numbers[r-1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-left  
            if r < n-1 and col > 0 and numbers[r+1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-right
            if r < n-1 and col < n-1 and numbers[r+1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
                
    return numbers
 
# Recursive function to display all zero-valued neighbours  
def neighbours(r, col):
     
    global mine_values
    global numbers
    global vis
 
    # If the cell already not visited
    if [r,col] not in vis:
 
        # Mark the cell visited
        vis.append([r,col])
 
        # If the cell is zero-valued
        if numbers[r][col] == 0:
 
            # Display it to the user
            mine_values[r][col] = numbers[r][col]
 
            # Recursive calls for the neighbouring cells
            if r > 0:
                neighbours(r-1, col)
            if r < n-1:
                neighbours(r+1, col)
            if col > 0:
                neighbours(r, col-1)
            if col < n-1:
                neighbours(r, col+1)    
            if r > 0 and col > 0:
                neighbours(r-1, col-1)
            if r > 0 and col < n-1:
                neighbours(r-1, col+1)
            if r < n-1 and col > 0:
                neighbours(r+1, col-1)
            if r < n-1 and col < n-1:
                neighbours(r+1, col+1)  
 
        # If the cell is not zero-valued            
        if numbers[r][col] != 0:
                mine_values[r][col] = numbers[r][col]
 
# Function for clearing the terminal
def clear():
    if platform in ["linux", "linux2", "darwin"]:
        os.system("clear")
    elif platform == "win32":
        os.system("cls")   
 
# Function to display the instructions
def instructions():
    print("Instructions:")
    print('1. Enter row and column number to select a cell, Example "2 3"')
    print('2. In order to flag a mine, enter F after row and column numbers, Example "2 3 F"')
 
# Goal check
def check_over():
    global mine_values
    global n
    global mines_no
 
    # Count of all numbered values
    count = 0
 
    # Loop for checking each cell in the grid
    for r in range(n):
        for col in range(n):
 
            # If cell not empty or flagged
            if mine_values[r][col] != ' ' and mine_values[r][col] != 'F':
                count = count + 1
     
    # Count comparison          
    if count == n * n - mines_no:
        return True
    else:
        return False
    
# Display all the mine locations                    
def show_mines(mine_values, numbers, n):
 
    for r in range(n):
        for col in range(n):
            if numbers[r][col] == -1:
                mine_values[r][col] = 'M'
    
    return mine_values
 
 
if __name__ == "__main__":
    #
    # Size of grid
    n = 20
    
    # Number of mines
    mines_no = 40
 
    # The actual values of the grid
    numbers = [[0 for y in range(n)] for x in range(n)] 
    # The apparent values of the grid
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    # The positions that have been flagged
    flags = []
 
    # Set the mines and values
    numbers = set_mines(numbers, mines_no, n)
    numbers = set_values(numbers, n)
 
    # Display the instructions
    instructions()
    incorrect_msg = "Invalid input"
         
    # Game loop
    over = False
    while not over:
        print_map(mine_values, n)
 
        # Input from the user
        inp = input("Enter row number followed by space and column number = ").lower()
        if inp == "exit":
            exit()
            
        inp = inp.split() 
         
        # Standard input
        if len(inp) == 2:
 
            # Try block to handle errant input
            try: 
                val = list(map(int, inp))
            except ValueError:
                clear()
                print(incorrect_msg)
                instructions()
                continue
 
        # Flag input
        elif len(inp) == 3:
            if inp[2] != 'F' and inp[2] != 'f':
                clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # Try block to handle errant input  
            try:
                val = list(map(int, inp[:2]))
            except ValueError:
                clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # Sanity checks 
            if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
                clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # Get row and column numbers
            r = val[0] - 1
            col = val[1] - 1 
 
            # If cell already been flagged
            if [r, col] in flags:
                clear()
                print("Flag already set")
                continue
 
            # If cell already been displayed
            if mine_values[r][col] != ' ':
                clear()
                print("Value already known")
                continue
 
            # Check the number for flags    
            if len(flags) < mines_no:
                clear()
                print("Flag set")
 
                # Adding flag to the list
                flags.append([r, col])
                 
                # Set the flag for display
                mine_values[r][col] = 'F'
                continue
            else:
                clear()
                print("Flags finished")
                continue    
 
        else: 
            clear()
            print(incorrect_msg)   
            instructions()
            continue
             
 
        # Sanity checks
        if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
            clear()
            print(incorrect_msg)
            instructions()
            continue
             
        # Get row and column number
        r = val[0]-1
        col = val[1]-1
 
        # Unflag the cell if already flagged
        if [r, col] in flags:
            flags.remove([r, col])
 
        # If landing on a mine, blow up    
        if numbers[r][col] == -1:
            mine_values[r][col] = 'M'
            mine_values = show_mines(mine_values, numbers, n)
            print_map(mine_values, n)
            print("Landed on a mine, ended up with an arrow to the knee... better luck next time")
            over = True
            continue
 
        # If landing on a cell with 0 mines in neighboring cells
        elif numbers[r][col] == 0:
            vis = []
            mine_values[r][col] = '0'
            neighbours(r, col)
 
        # If selecting a cell with atleast 1 mine in neighboring cells  
        else:   
            mine_values[r][col] = numbers[r][col]
 
        # Check for game completion 
        if(check_over()):
            mine_values = show_mines(mine_values, numbers, n)
            print_map(mine_values, n)
            print("You win, you deserve cookies!")
            over = True
            continue
        clear()