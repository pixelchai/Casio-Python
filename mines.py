from random import *

# Mines - PixelZerg
# constants
W_WIDTH = 21
W_HEIGHT = 7

# internal key constants
K_OTHER, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_FLAG, K_SEL = -1, 0, 1, 2, 3, 4, 5

# misc global variable
directions = [
        (-1,-1),
        (-1,0),
        (-1,1),
        (0,-1),
        (0,1),
        (1,-1),
        (1,0),
        (1,1),
]

# methods
def choice(l):
    i = 1
    for opt in l:
        print(str(i)+") "+str(opt))
        i+=1
    while True:
        try:
            inp = int(input("Choose (1-"+str(len(l))+"): "))
            if inp <= len(l) and inp > 0:
                return inp - 1
        except:
            pass

def inputn(prompt="",lbound=0,ubound=99):
    while True:
        try:
            inp = int(input(prompt+" ("+str(lbound)+"-"+str(ubound)+"): "))
            if inp >= lbound and inp <= ubound:
                return inp
        except:
            pass

def inputk():
    # calculator controls
    keymap_calc = {
        '8': K_UP,
        '2': K_DOWN,
        '4': K_LEFT,
        '6': K_RIGHT,
        '5': K_FLAG,
        '': K_SEL,
    }
    # alternate (keyboard) controls
    keymap_alt = {
        'w': K_UP,
        's': K_DOWN,
        'a': K_LEFT,
        'd': K_RIGHT,
        'z': K_FLAG,
        'x': K_SEL,
    }
    inp = input().strip().lower()
    if len(inp) > 1:
        inp = inp[-1]
    if inp in keymap_calc:
        return keymap_calc[inp]
    elif inp in keymap_alt:
        return keymap_alt[inp]
    else:
        return K_OTHER

def clear():
    for i in range(W_HEIGHT):
        print()

def initarr(width, height, default=0):
    ret = []
    for row in range(height):
        buf = []
        for col in range(width):
            buf.append(default)
        ret.append(buf)
    return ret

def count_around(minefield, x, y):
    num = 0
    for direction in directions:
        curx, cury = x+direction[0], y+direction[1]
        if 0 <= cury < len(minefield) and 0 <= curx < len(minefield[0]):
            if minefield[cury][curx]:
                num+=1
    return num

def viewport(userfield, flagfield, viewx, viewy, curx, cury):
    for j in range(W_HEIGHT-1):
        buf = ""
        for i in range(W_WIDTH):
            if viewy+j == cury and viewx+i == curx:
                buf += 'X'
            elif 0 <= viewy+j < len(userfield) and 0 <= viewx+i < len(userfield[0]):
                if flagfield[viewy+j][viewx+i]:
                    buf += 'P'
                else:
                    if userfield[viewy+j][viewx+i] == 0:
                        buf += ' '
                    else:
                        buf += str(userfield[viewy+j][viewx+i])
            else:
                buf += "#"
        print(buf)

def select(userfield, aroundfield, x, y):
    if 0 <= y < len(userfield) and 0 <= x < len(userfield[0]):
        if aroundfield[y][x] == 0 and userfield[y][x] != 0:
            userfield[y][x] = 0
            # recursive flood fill
            userfield = select(userfield, aroundfield, x-1, y)
            userfield = select(userfield, aroundfield, x+1, y)
            userfield = select(userfield,aroundfield,x,y-1)
            userfield = select(userfield,aroundfield,x,y+1)
        else:
            userfield[y][x] = aroundfield[y][x]
    return userfield

def has_won(flagfield, minefield):
    for row in range(len(minefield)):
        for col in range(len(minefield[0])):
            if minefield[row][col] != flagfield[row][col]:
                return False
    return True

def reveal(aroundfield, minefield):
    ret = aroundfield
    for row in range(len(minefield)):
        for col in range(len(minefield[0])):
            if minefield[row][col]:
                ret[row][col] = '@'
    return ret

def main():
    # welcome screen
    print("  Welcome to Mines!  ")
    print("-"*W_WIDTH)

    # level setup
    width = 21
    height = 6  # 7-1 so a line can be for status
    mines = 5

    level_defaults = [
            (19,4,5),
            (20,7,10),
            (39,11,30)
    ]
    inp = choice(["Easy","Medium","Hard","Custom"])
    if inp == 3:
        width = inputn("Width",21)
        height = inputn("Height",6)
        mines = inputn("No Mines", 0, min(99,width*height))
    else:
        width, height, mines = level_defaults[inp]

    # init fields
    minefield = initarr(width, height) # 0 = no mine, 1 = mine
    aroundfield = initarr(width, height) # numbers of mines around
    userfield = initarr(width, height, '-') # characters
    flagfield = initarr(width, height) # 0 = no flag, 1 = flag

    # init mines
    for i in range(mines):
        while True:
            row = randint(0,height-1)
            col = randint(0,width-1)
            if not minefield[row][col]:
                minefield[row][col] = 1
                break

    # init around
    for row in range(height):
        for col in range(width):
            aroundfield[row][col] = count_around(minefield, col, row)

    viewx = -5
    viewy = -1
    curx = 0
    cury = 1

    steps = 0

    while True:
        viewport(userfield, flagfield, viewx, viewy, curx, cury)

        # controls
        k = inputk()
        if k == K_UP:
            cury-=1
        if k == K_DOWN:
            cury+=1
        if k == K_LEFT:
            curx-=1
        if k == K_RIGHT:
            curx+=1
        if k == K_FLAG:
            flagfield[cury][curx] = not flagfield[cury][curx]
        if k == K_SEL:
            if minefield[cury][curx]:
                # game over

                # reveal full
                userfield = reveal(aroundfield,minefield)
                viewport(userfield, initarr(width,height), viewx, viewy, None, None)
                input("Press EXE")

                # game over screen
                print("      Game Over!     ")
                print("-" * W_WIDTH)
                print("Steps: "+str(steps))
                print()
                break
            else:
                if not has_won(flagfield, minefield):
                    userfield = select(userfield, aroundfield, curx, cury)
                else:
                    # game won

                    # reveal full
                    userfield = reveal(aroundfield, minefield)
                    viewport(userfield, initarr(width, height), viewx, viewy, None, None)
                    input("Press EXE")

                    # game over screen
                    print("       You Win!      ")
                    print("-" * W_WIDTH)
                    print("Steps: " + str(steps))
                    print()
                    break

        # viewport adjustment
        if curx - viewx < 5:
            viewx -= 2
        if curx - viewx > W_WIDTH - 5:
            viewx += 2
        if cury - viewy < 1:
            viewy -= 2
        if viewy + min(W_HEIGHT-1, height) - cury < 2:
            viewy += 2
        steps+=1

    # play again?
    print("Play again?")
    inp = choice(["Yes", "No"])
    if inp == 0:
        main()

main()
