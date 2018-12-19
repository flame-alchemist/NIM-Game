import pygame
import sys
import time

BG_color = (220, 255, 255)
box_color = (55, 230, 230)
circle_color = (255, 111, 97)
outline_color = (255, 51, 0)
submit_color = (255, 99, 71)
line_color = (37, 116, 77)

submit = 0
bit_list = [1 for _ in range(25)]

def mouse_pos():
    (mouseX, mouseY) = pygame.mouse.get_pos()
    #print(mouseX, mouseY)
    if(mouseY>=120 and mouseY<=170):
        index = (mouseX-125)/50
        return index
    return -1

def text_objects(text,font):
    textSurface=font.render(text,True,(0,0,0))
    return textSurface, textSurface.get_rect()

def submit_button():
    (mouseX, mouseY) = pygame.mouse.get_pos()
    if(mouseX >= 650 and mouseX<=850 and mouseY>=30 and mouseY<=80):
        print "clicked"
        global submit
        submit = 1

def erase(bit_list):
    for i in range(25):
        if(bit_list[i] == 2):
            pygame.draw.circle (display, (box_color), (150+(i*50), 145),20, 20)
            pygame.display.update()
            bit_list[i] = 0



class NimGame:
    # --------------------------------------------------------- #
    # The game definition class                                 #
    # --------------------------------------------------------- #
    # A nim game is a type of zero sum game played by 2 players #
    # Read more at https://en.wikipedia.org/wiki/Nim            #
    # This class models the game and the methods allow the      #
    # evaluation of state space for different type of solvers   #
    # --------------------------------------------------------- #
    def __init__(self, n):
        # initialize the game - only the number 'n' is required
        # which tells us how many objects are there in a heap
        # this is the variant of the "subtraction game"
        self.n = n

    def startState(self):
        # Starting state - there are n objects in a single heap
        return self.n

    def isEnd(self, state):
        # the game has reached the end state if there are no objects
        return True if state == 0 else False

    def utility(self, state, player):
        # The utility is +inf for the player having won
        # and -inf for the adversary having won
        if state == 0:
            if player == 1:
                # you lost
                return float('-inf')
            else:
                # you won!
                return float('+inf')

    def actions(self, state):
        # the possible actions at a particular state
        if state >= 3:
            return [1,2,3]
        return range(1, state+1)

    def successor(self, state, action):
        # The (distinct) successor state if an action
        # is taken at a particular state
        if action > state:
            return 0
        return state - action


def minimaxPolicy(game, state, player):
    # --------------------------------------------------------- #
    # The minimax solver in state space for a general game      #
    # --------------------------------------------------------- #
    # The minimax solver assumes a zero-sum 2-player game being #
    # played, between a human "player" and an AI "adversary"    #
    # It returns optimal (value, action) at a state.            #
    # It needs to recursively compute the value, therefore      #
    # define the recursion function within this function.       #
    #
    # Read more about minimax here:                             #
    # https://en.wikipedia.org/wiki/Minimax                     #
    # --------------------------------------------------------- #
    i=0
    def recurse(state, player):
        # ----------------------------------------------------------------- #
        # The recursive function checks the sub-tree of a particular state  #
        # and minimizes expected value for the player while maximizing the  #
        # expected value of a player's move, i.e. assuming the player is    #
        # behaving using an optimal strategy
        # ----------------------------------------------------------------- #
        global i
        # start with the base case
        if game.isEnd(state) == True:
            # return the utility of the state, no more actions that can be taken
            return (game.utility(state, player), None)
        if cache.has_key((state, player)):
            return cache[(state, player)]

        # otherwise, look at all possible actions in the game
        # toggle the player each time it is called (since it is a 2-player game)
        # we thus represent the present player by 1 or -1 to ease toggling
        choices = [(recurse(game.successor(state, action), -1*player)[0], action) for action in game.actions(state)]
        #print "PLAYER =",player
        #print "CHOICE "+str(i)+" =",choices
        # return the max of the choice of (utility, optimalAction) if it is the agent and min if it is the opponent
        # the min/max function will only be applied to hte first element of the tuple in the list "choices"
        # This is because we want to maximize/minimize over the expected utility, NOT the action
        # But we want the action as well.
        if player == +1:
            val = max(choices)
        else:
            val = min(choices)
        cache[(state, player)] = val
        #print "CACHE "+str(i)+" =",cache
        #print "VALUE "+str(i)+" =",val
        i=i+1
        return val

    # Recurse over the choices for the state, return the second argument of returned tuple
    # The solver will go all the way till the end of the tree to choose the optimal next action
    #
    # Returned values:
    # value = the optimal value (utility of the end state reached by both players taking a series of optimal actions)
    # action = the optimal action for the adversary to take next to minimize the expected utlity of the player
    value, action = recurse(state, player)
    return (value, action)

# cache values globally to speed up the minimax recursion
# dynamic programming ftw
cache = {}

if __name__ == "__main__":
    # play the nim game on terminal for fun
    pygame.init()
    width = 1500
    height = 300
    #global bit_list
    #global submit
    counter = 0

    #make the pygame window
    display = pygame.display.set_mode((width, height ) )
    display.fill(BG_color)
    pygame.draw.rect(display, (submit_color), [650, 30, 200, 50])

    smallText = pygame.font.Font("freesansbold.ttf",20)
    TextSurf, TextRect = text_objects("Submit", smallText)
    TextRect.center = (750,53)
    display.blit(TextSurf, TextRect)
    pygame.draw.rect(display, (box_color), [125, 120, 1250, 50])
    pygame.draw.line (display, (line_color), (125 , 120), (1375, 120), 2)
    pygame.draw.line (display, (line_color), (125 , 170), (1375, 170), 2)
    for i in range(0,1300,50):
        pygame.draw.line (display, (line_color), (125 +i, 120), (125+i, 170), 2)
    for i in range(0,1250,50):
        pygame.draw.circle (display, (circle_color), (150+i, 145),20, 20)
    pygame.display.update()


    game = NimGame(25)

    state = game.startState()
    print "current state is", state
    while (state > 0):
        action = 0

        running = 1
        while(running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                if event.type is pygame.MOUSEBUTTONDOWN:
                    if(submit != 1):
                        if(counter > 0):
                            submit_button()
                        index = mouse_pos()
                        if(index != -1):
                            counter += 1
                            bit_list[index] = 2
                            pygame.draw.circle (display, (outline_color), (150+(index*50), 145),20, 20)
                            pygame.display.update()
                    else:
                        erase(bit_list)
                        running = 0

        print "you removed ",counter
        submit = 0
        state -= counter
        print "current state is", state
        time.sleep(2)
        counter = 0
        if state <= 0:
            print "You won!"
            break
        val, act = minimaxPolicy(game, state, 1)
        state -= act
        print "computer removed ",act
        x = 0
        i = 0
        while(x != act):
            if(bit_list[i] == 1):
                bit_list[i] = 2
                x += 1
            i += 1

        erase(bit_list)
        pygame.display.update()

        print "computer moves state to", state
        if state == 0:
            print "You Lost!"
