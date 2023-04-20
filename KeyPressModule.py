import pygame


# This function Initializes pygame window
def init():
    pygame.init()
    win = pygame.display.set_mode((400, 600))


# Function searches for when a key is pressed
def getKey(keyName):
    ans = False
    # Check for event
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, "K_{}".format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans


# Main function test
def main():
    # print(getKey("a"))
    if getKey("LEFT"):
        print("Left key pressed")
    if getKey("RIGHT"):
        print("Right key pressed")


# If I run this file as a main file
if __name__ == "__main__":
    init()
    # While file is running (Keep pygame window open
    while True:
        main()
