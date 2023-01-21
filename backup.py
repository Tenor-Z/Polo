#--------------------------------------------------------
#ANTI PLAGERISM AND CREDITS START BELOW
#IF YOU RECIEVE THIS AND SOME THINGS HAVE BEEN MODIFIED, THEN IT IS OBVIOUSLY BEEN TWEAKED

#WARNING!!
#THIS GAME USES OS DETECTION IN ORDER TO USE SYSTEM COMMANDS!!
#IF YOU ARE RUNNING LINUX OR MAC OS, THE GAME WILL NOT RUN PROPERLY
#===================================================================
#----------------------------------------------------------
#,ggggggggggg,                                
#dP"""88""""""Y8,           ,dPYb,             
#Yb,  88      `8b           IP'`Yb             
# `"  88      ,8P           I8  8I             
#    88aaaad8P"            I8  8'             
#     88"""""    ,ggggg,    I8 dP    ,ggggg,   
#     88        dP"  "Y8ggg I8dP    dP"  "Y8ggg
#     88       i8'    ,8I   I8P    i8'    ,8I  
#     88      ,d8,   ,d8'  ,d8b,_ ,d8,   ,d8'  
#     88      P"Y8888P"    8P'"Y88P"Y8888P"    
#----------------------------------------------------------
#                     POLO
#             Programmed and Written by
#                 Tyler Bifolchi         
#                     2022              
#-------------------------------------------------------- 
# Wow... All these lines of code just for a psuedo Pac-Man replica... But anyway, here is the full source code
                                              
#The following directories are needed:
# -images
# -music

#Without these directories, the game will randomly crash, as it cannot find the files adjacent in neighbouring directories. It is assumed that the following directories are included with this file if you are reverse engineering or viewing this file on Github (coming soon)

import pygame  #Pygame is needed for the entire game!
import sys, time    #Sys is used for os detection and                         time for the time limit

#Random is used to randomize multiple things, such as tips, and item locations
import random

pygame.mixer.init()   #Initialize Pygame's mixer
pygame.init()         #Initialize Pygame

#------------------------------------------------
# The following below is the coordinates of the
# game window. DO NOT MODIFY!
#------------------------------------------------
height = 600          #These are the size of the
width = 600          #window coordinates
gameWindow = pygame.display.set_mode((width, height))
#use the set_mode function to set the window screen to our width and height

#--------------------------------------------------
#Here is the sound and music data
#Each variable holds a different sound or song
#For some reason, the pygame mixer doesn't load properly in replit
#--------------------------------------------------
global start, die, ending
start = pygame.mixer.Sound('music/start.wav')
die = pygame.mixer.Sound('music/die.wav')
ending = pygame.mixer.Sound('music/ending.wav')
greatluck = pygame.mixer.Sound('music/gl.wav')
nothing = pygame.mixer.Sound('music/n.wav')
supacool = pygame.mixer.Sound('music/sc.wav')
ohwow = pygame.mixer.Sound('music/ow.wav')
toughluck = pygame.mixer.Sound('music/tl.wav')
instructions = pygame.mixer.Sound('music/instruction.wav')
levelcomplete = pygame.mixer.Sound('music/lc.wav')
popup = pygame.mixer.Sound('music/popup.wav')
maingame = pygame.mixer.Sound('maingame.mp3')

global gameon   #gameon is used to indicate what section the game is currently running in.


gameon = "Title" #since the game is started up, it goes to the title.

global intro
intro = "NO"


global level   #Indicates what level the game is on
level = 1      #Set it to the first level

global direction
direction = "Down"

#Make these two variables global so they can be used throughout the game. As of 1/13/2022, there is a bug that doesn't allow the lives counter to go past 2.
global lives, livemessage

lives = 3  #lives indicates how much lives the player has


#This is passed off as a visual reminder of the player's lives
livemessage = "You have     lives!"  #message that appears on the introduction screen
nonotification = "No new character introductions to view."
conti = "Please press space to continue"
notification = "1 new character introduction!"
view = "Press space to view!"
reminder = "This game will make your blood boil!"

#The gathered variable is used to record whether the vaccine has been collected, since it's the beginning of the game, set this variable to 0
global gathered
gathered = 0


#Several hexadecimal values for different colors used in pygame, green and blue, however go unused (originally meant for a potential story)
green = (0, 255, 0)  
blue = (0, 0, 128)
white = (255, 255, 255)
black = [  0,  0,  0]      #black is used for MULTIPLE reasons, more about that further down


#The following two variables are different fonts used in game. The small font is used for pop up messages and debugging errors.
font = pygame.font.SysFont("Arial",36)  #This variable holds the displayed font throughout the game.

smallfont = pygame.font.SysFont("System",25)


#Messagetype is used for debugging and on screen messages. Like the name suggests, it sorts the different types of messages
messagetype = "None"


#This is the function that runs when a level has been completed, this is to avoid consistancy and to form somewhat of organization system. The function needs gameon and level in order to modify the two variables
def levelcompleted(gameon, level):
  pygame.mixer.music.load("music/popup.wav")
  pygame.mixer.music.play(-1)
  #The lc variable holds the image for the "LEVEL COMPLETED" text. We have to reform the image into an appropiate size, so it doesn't stretch out the screen.
  levelcomplete.play()
  lc = pygame.image.load("images/flavor_text/lc.png")
  lc = pygame.transform.scale(lc, (400,400))
  none = smallfont.render(str(nonotification),1,white)
  one = smallfont.render(str(notification),1,white)
  contin = smallfont.render(str(conti),1,white)
  viewi = smallfont.render(str(view),1,white)
      

  #You'll notice that this type of subfunction appears a lot in several functions. The purpose of this is to constantly reload the screen with sprites with their updated coordinates.
  def reload():
    gameWindow.fill(black)  #Fill the background black
    gameWindow.blit(lc,(100,100))  #Blit the text
    if level == 3:
     gameWindow.blit(one, (130,0))    #blit them all
     gameWindow.blit(viewi,(130, 50))   #to their
    else:
     gameWindow.blit(none,(130, 0))  #x and y values
     gameWindow.blit(contin,(130, 50))
    pygame.display.flip()    #And display the updated sprites
  while gameon == "Level Completed!": #Make sure that it's the correct game mode, and loop the following
    reload()
    for event in pygame.event.get():#Capture pygame events
      if event.type == pygame.KEYDOWN:#Check if a key was pressed
        if event.key == pygame.K_SPACE: #Was it space?
            level += 1
            gameon = "game loaded"     #Start the next level
            rungame(gameon, level, gathered, messagetype)
              

#This is the main function of the "GET READY" screen, which transitions into the main game. Gameon is needed for modifying the variable
def ready(gameon):
  gameWindow.fill(white)  #Fill the screen white
  ready = pygame.image.load("images/getready.png") #Use the variable to hold the get ready image
  sayit = font.render(str(reminder),1,black)
  ready = pygame.transform.scale(ready, (300, 300)) #Transform the image to a better size
  gameWindow.blit(ready,(150,180)) #And blit it to the screen
  gameWindow.blit(sayit,(20, 50))
  pygame.display.flip()   #Print it to screen
  pygame.time.wait(3000)   #Wait for a bit
  gameon = "game loaded" #And load the game
  rungame(gameon, level, gathered, messagetype)
    

#This is a pretty complicated function. It is a message handler, used for pop up messages and/or debugging error messages. A DENIED message type is the message that appears when the player doesn't collect the vaccine, a NON EXISTANT LEVEL error is printed when a level that isn't in memory is trying to get loaded (mostly if the reader is modifying game variables)
def msghandler(messagetype):
  #The messagebox variable holds the message BOX that holds the actual message
  messagebox = pygame.image.load("images/msgbox.png")
  gameWindow.blit(messagebox,(30,30)) #and blit it
  pygame.display.flip()   #Print it on screen

  #This is where the function checks for the messaage type
  #Is the messagetype the DENIED type?
  if messagetype == "DENIED":
    pygame.mixer.music.load("music/popup.wav")
    pygame.mixer.music.play(-1)
    message = "Uh oh! It looks like you forgot to collect the vaccine!" #Generate the message
    message2 = "Collect the vaccine and try again!" #And the submessage
    sayit = smallfont.render(str(message),1,white) #Render each message with the fonts specified
    sayit2 = smallfont.render(str(message2),1,white)
    gameWindow.blit(sayit,(100,100))#And blit both of them
    gameWindow.blit(sayit2,(120,125))
    pygame.display.update()     #And print them to screen
    pygame.time.wait(4000)     #Wait a little bit
    messagetype = "None"   #And set the message type to nothing, so that the message doesn't loop over and over

    #Is the message type a NONEXISTANT LEVEL
  elif messagetype == "ERROR - NONEXISTANT LEVEL":
    #Generate the two messages.
    popup.Play()
    message = "GAME RENDERING ERROR! NO LEVEL IN MEMORY!"
    message2 = "Please close this program."
    #Render them
    sayit = smallfont.render(str(message),1,white)
    sayit2 = smallfont.render(str(message2),1,white)
    #blit and print them
    gameWindow.blit(sayit,(50,100))
    gameWindow.blit(sayit2,(120,125))
    pygame.display.update()
  else:
    print("")

#This is the main function for the title screen, it is ran as soon as the game starts, and it carries the gameon variable, so it knows where to set the current scene.
def title(gameon, start):
  pygame.mixer.music.load("music/start.wav")
  pygame.mixer.music.play(0)
  while gameon == "Title":  #Repeat this while the current scene is Title
    print("game title loaded") #debugging feature to let us know it has successfully loaded
    demopolo = pygame.image.load("images/demo1.png")
    demo2 = pygame.image.load("images/demo2.png")
    demopolo = pygame.transform.scale(demopolo, (50, 50))
    demo2 = pygame.transform.scale(demo2, (50, 50))
    titledrop = pygame.image.load("images/justblack.png") #use this variable for the backdrop of the title
    logo = pygame.image.load("images/yee.png")
    #logo holds the logo
    start = pygame.image.load("images/start.png")
    #the flavor text at the bottom
    gameWindow.blit(titledrop, (0,0))
    gameWindow.blit(logo, (0,0))
    gameWindow.blit(start, (0,200))

    #The following for loop is for checking if the space key was pressed. This is using the KEYDOWN function and, some debug inputs should be listed as well. (might get commented out on release)  
     
    pygame.display.flip()    #Update screen display
    for event in pygame.event.get():#Capture pygame events
      if event.type == pygame.KEYDOWN:#Check if a key was pressed
        if event.key == pygame.K_SPACE: #Was it space?
          print("space was pressed") #A debugging thing
          gameon = "Instructions"     #Set the scene to instructions
          instructions(gameon) #and call the function

          #THE FOLLOWING STATEMENTS ARE FOR DEBUGGING ONLY! CERTAIN LETTERS PRESSED WILL PRESENT DIFFERENT SCREENS OF THE GAME, SUCH AS THE ENDING. USE THEM TO NAVIGATE AROUND THE GAME A LOT QUICKER
        elif event.key == pygame.K_p:
          print("DEBUG COMMAND ENTERED")
          ending()
        elif event.key == pygame.K_r:
          print("DEBUG COMMAND ENTERED")
          introprinter(level, lives, livemessage, gameon, gathered)
        elif event.key == pygame.K_z:
          gameon = "game loaded"
          rungame(gameon, level, gathered, messagetype)


#This function is used to display the instructions screen, it is very similar in code with the title screen function
#Gameon needs to be passed in order to modify the game mode without defining it again

def instructions(gameon):
  #loop as the game mode is set to Instructions
  while gameon == "Instructions": #only works on this setting
    print("instructions loaded")  #debug message part 2
    ins = pygame.image.load("images/instructions.png") #the variable that holds the instructions screen
    loadscreen = pygame.image.load("images/justblack.png")
    
    #Load the backdrop in case the instructions page is too small (this was added before testing)
    
    gameWindow.blit(loadscreen, (0,0)) #put it on screen
    gameWindow.blit(ins, (0,0)) #Same with the page
    pygame.display.flip()     #and update the screen
    for event in pygame.event.get():  #gather events
      if event.type == pygame.KEYDOWN: #check for key down events
        if event.key == pygame.K_SPACE: #is it space again
           print("space was pressed again") #debug message: the prisoner of azkaban
           gameon = "Load" #set the game mode to load
           introprinter(level, lives, livemessage, gameon, gathered)
           break #and call the corresponding function


#This function is only used for the little intro stages through some levels introducing the characters. It is also used to show how many lives the player has. If you're not sure where I'm talking about, check out the How High can You Get screen from the Arcade Donkey Kong

#NOTE: gathered is needed in order to reset the value to 0 so that the player needs to collect the vaccine
def introprinter(level, lives, livemessage, gameon, gathered):
  global intro, messagetype
  pygame.mixer.music.load("music/instruction.wav")
  pygame.mixer.music.play(0)
  randomtryagainvalue = 0  #This variable is used for storing the value of which tips screen to show once the player has died. Since the function is starting, set it to zero for now
  print("intro scene is setting up....")  #debug 4: H2O
  if level == 1 or level > 1:  #is the level 1?
    if lives == 0:  #Is there no lives left?
      print("no lives left! quitting...")  #Debug message
      gameon = "Game Over"
      gameover(gameon)  #And call the game over function
    elif level == 1 and lives == 3: #Is the level one and lives are 3?
      livecounter = font.render(str(lives),1,white) #holds the visual amount of lives the player has
      sayit = font.render(str(livemessage),1,white) #the variable containing the message that holds it together
      print("showing level intro") #debug 5: The return of the king
      intro1 = pygame.image.load("images/intro1.png") #set up the first intro screen for first level
      gameWindow.blit(intro1, (0,0))    #blit them all
      gameWindow.blit(livecounter,(310, 50))   #to their
      gameWindow.blit(sayit,(150, 50))  #x and y values
      gathered = 0
      pygame.display.flip()       #and display it
      pygame.time.wait(7000) #wait for a few seconds
      gameon = "Ready?" #set to game play
      ready(gameon)
      #rungame(gameon, level, lives, gathered) #and begin the game
    elif level == 1 and lives < 3:  #This will be modified later to include all levels. 
      randomtryagainvalue = random.randint(1, 6) #Pick a random number between 1 and 6
      print(str(randomtryagainvalue))  #Print it to screen (debug)
      if randomtryagainvalue == 1: #Is the value 1?
      #print all needed info to the screen, along with the corresponding tip
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip1.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 300))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.mixer.music.play(0)
        pygame.display.flip()
        gathered = 0      #Set gathered items to zero
        pygame.time.wait(7000) #And wait
        gameon = "game loaded"  #To load the game
        rungame(gameon, level, gathered, messagetype)
        
        #The next elif statements are alike to the first if statements, they all load needed data and show their corresponding tip screens. (a value of 1 pulls tip 1)
      elif randomtryagainvalue == 2:
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip2.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 300))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.display.flip()
        pygame.time.wait(7000)
        gameon = "game loaded"
        rungame(gameon, level, lives, gathered)
      elif randomtryagainvalue == 3:
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip3.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 300))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.display.flip()
        gathered = 0
        pygame.time.wait(7000)
        gameon = "game loaded"
        rungame(gameon, level, lives, gathered)
      elif randomtryagainvalue == 4:
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip4.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 300))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.display.flip()
        gathered = 0
        pygame.time.wait(7000)
        gameon = "game loaded"
        rungame(gameon, level, lives, gathered)
      elif randomtryagainvalue == 5:
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip5.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 300))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.display.flip()
        gathered = 0
        pygame.time.wait(7000)
        gameon = "game loaded"
        rungame(gameon, level, lives, gathered)
      elif randomtryagainvalue == 6:
        livecounter = font.render(str(lives),1,white)
        sayit = font.render(str(livemessage),1,white) 
        tip = pygame.image.load("images/tip6.png")
        polo = pygame.image.load("images/damagedpolo.png")
        polo2 = pygame.image.load("images/moredamagedpolo.png")
        polo = pygame.transform.scale(polo, (300, 300))
        polo2 = pygame.transform.scale(polo, (300, 00))
        gameWindow.blit(tip, (0,0))
        gameWindow.blit(livecounter,(310, 50))   #to their
        gameWindow.blit(sayit,(150, 50))  #x and y values
        if lives == 2:
          gameWindow.blit(polo,(100,100))
        else:
          gameWindow.blit(polo2,(100,100))
        pygame.display.flip()
        gathered = 0
        pygame.time.wait(7000)
        gameon = "game loaded"
        rungame(gameon, level, lives, gathered)
      else:     #Is there no level loaded (if someone's poking with the code)
        print("ERROR! NO LEVEL SET!!")    #Ha ha!
        messagetype = "ERROR - NONEXISTANT LEVEL"
        msghandler(messagetype)

  if level == 4:
      livecounter = font.render(str(lives),1,white) #holds the visual amount of lives the player has
      sayit = font.render(str(livemessage),1,white) #the variable containing the message that holds it together
      print("showing level intro") #debug 5: The return of the king
      intro2 = pygame.image.load("images/intro2.png") #set up the first intro screen for first level
      gameWindow.blit(intro2, (0,0))    #blit them all
      gameWindow.blit(livecounter,(310, 50))   #to their
      gameWindow.blit(sayit,(150, 50))  #x and y values
      gathered = 0
      pygame.display.flip()       #and display it
      pygame.time.wait(7000) #wait for a few seconds
      gameon = "game loaded" #set to game play
      rungame(gameon, level, lives, gathered) #and begin the game

#This is the main function that runs during gameplay
#and oh boy, it's a big one... This will be further modified later on as main mechanics get programmed.
#----------------------------------------------------
#NOTE TO MR. ROBINSON, THIS IS THE MAIN AND ONLY FUNCTION THAT IS HAVING PROBLEMS RUNNING!!
#----------------------------------------------------
#                   UPDATE
#                  1/13/2022
#  Bugs were fixed, but now the lives and level variables do not change. Completing a level changes the level, but when the player dies, it goes back to the first level.
#----------------------------------------------------

def rungame(gameon, level, gathered, messagetype):
 global power, faster, youfaster, kill, event, lives

 pygame.mixer.music.load("maingame.mp3")
 pygame.mixer.music.play(-1)

 #The event variable holds the powerup events that happens
 #---------------------------------------------
 # 1. Monsters are killed
 # 2. Character moves faster
 # 3. Nothing happens
 # 4. The exit opens up
 # 5. Monsters move faster
 # 6. Player loses a life
 #-------------------------------------------------
 mazepick = random.randint(1,6)
 print("Mazepick selected " + str(mazepick))
 event = 0
 
 borside = pygame.image.load("images/border/bside.png")
 borderRect = borside.get_rect()
 borderW = borderRect.width
 borderH = borderRect.height
 borX = -5
 borY = 0


 borside2 = pygame.image.load("images/border/bside.png")
 borderRect2 = borside2.get_rect()
 border2W = borderRect2.width
 border2H = borderRect2.height
 bor2X = 600
 bor2Y = 0


 bortop = pygame.image.load("images/border/bortop.png")
 bortopRect = bortop.get_rect()
 bortopW = bortopRect.width
 bortopH = bortopRect.height
 bortopX = 0
 bortopY = -30
 
 bortop2 = pygame.image.load("images/border/bortop.png")
 bortop2Rect = bortop2.get_rect()
 bortop2W = bortop2Rect.width
 bortop2H = bortop2Rect.height
 bortop2X = 0
 bortop2Y = 700

 borside2 = pygame.image.load("images/border/bside.png")
 borderRect2 = borside2.get_rect()
 border2W = borderRect2.width
 border2H = borderRect2.height
 bor2X = 0
 bor2Y = 0
 
 #The power variable decides whether the powerup appears on screen. Since the game is beginning, set it to zero (It appears)
 power = 0
 
 #Faster decides whether the enemies move faster. This is set to zero because this is a 1/5 chance when getting the powerup

 faster = 0
 
 if level == 4:
   intro = "YES"
 else:
   print("")

 if level == 4:
   if intro == "YES":
    livecounter = font.render(str(lives),1,white)
    sayit = font.render(str(livemessage),1,white) 
    tip = pygame.image.load("images/intro2.png")
    gameWindow.blit(tip, (0,0))
    gameWindow.blit(livecounter,(310, 50))   #to their
    gameWindow.blit(sayit,(150, 50))  #x and y values
    pygame.display.flip()
    pygame.time.wait(7000)
    intro = "NO"
    gameon = "Level Completed!"
    levelcompleted(gameon, level)
   else:
     intro = "NO"

 
 global Xorigin, Yorigin
 #Same thing applies to this variable, but it decides whether the player moves faster

 youfaster = 0

 #Kill decides whether the enemies are killed. They will not be killed at the beginning
 kill = 0
 
 #print(str(lives) + " left") #Another debugging message

 print("game is starting") #debug message: The Final Insult
 print("This is the level " + str(level))

 WHITE = (255,255,255)  #White is used to fill the background
 gameWindow.fill(WHITE) #Fill the screen

 #Vac is the variable that holds the vaccine
 vac = pygame.image.load("images/vaccine.png") #The main image of the vaccine powerup

 # --------------------------------------------
 # This following variables holds the coordinates for the player. For color collision a small white ball will follow it, it is invisible to the player. 
 #------------------------------------------------
 if level == 1:
   Xorigin = 40  #The X and Y origins are where the ball ALWAYS starts during the start of the level OR after the player dies. This avoids a bug where the player is permantly touching an enemy or wall after dying once.
   Yorigin = 10
 if level == 2 or level == 3 or level == 4:
   Xorigin = 60
   Yorigin = 60
 if level == 5:
   Xorigin = 520
   Yorigin = 200
 if level == 6:
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "1":
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "2":
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "3":
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "4":
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "5":
   Xorigin = 520
   Yorigin = 200
 if level > 6 and mazepick == "6":
   Xorigin = 520
   Yorigin = 200
 ballR = 5 #Set the ball's radius to 8 (fairly small)
 ballX = Xorigin  #Set the REAL x and y coordinates of the ball to the origin axis
 ballY = Yorigin
 ballCLR = WHITE   #Set the ball color to light blue
 stepX = 5          #Step is set to 5, so the player doesn't move too fast
 stepY = 5

 #-----------------------------------------
 #   This is some more variables for the player
 #  The Rectangle variable is for collision, along with       width and height
 #------------------------------------------
 player = pygame.image.load("images/player/pic11.png")
 player = pygame.transform.scale(player, (15, 15))
 shipRect = player.get_rect() #Make rectangle for collision
 shipW = shipRect.width
 shipH = shipRect.height

 #=========================================
 #      The following variables are for the vaccine,       which hold some similarities to player variables 
 #------------------------------------------
 asteroidRect = vac.get_rect() #Make the rectangle
 asteroidW = asteroidRect.width
 asteroidH = asteroidRect.height

 #This is the variable collection for the powerup.
 powerup = pygame.image.load("images/powerup.png") #the variable for the powerup
 powerup = pygame.transform.scale(powerup,(25,25))
 powRect = powerup.get_rect() #make the rectangle for it
 powerW = powRect.width
 powerH = powRect.height
 if level == 1:
   powerX = 430
   powerY = 260
 elif level == 2 or level == 3:
   powerX = 200
   powerY = 400
 elif level == 4:
   powerX = 300
   powerY = 200
 elif level == 5:
   powerX = 300
   powerY = 90
 elif level == 6:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 1:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 2:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 3:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 4:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 5:
   powerX = 300
   powerY = 90
 elif level > 6 and mazepick == 6:
   powerX = 300
   powerY = 90
#The following variables are for the vaccine, to create a random location for it on each level.
 global ranX, ranY
 ranX = random.randint(10, 300)
 ranY = random.randint(20, 300)
 resultX = ranX
 resultY = ranY

 #These are the variables for the exit
 if level == 1:
  exitX = 360
  exitY = 0
 elif level == 2 or level == 3:
   exitX = 410
   exitY = 50
 elif level == 4:
   exitX = 30
   exitY = 300
 elif level == 5:
   exitX = 30
   exitY = 300
 elif level == 6:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 1:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 2:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 3:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 4:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 5:
   exitX = 30
   exitY = 300
 elif level > 6 and mazepick == 6:
   exitX = 30
   exitY = 300




 #These variables are for the the Repla character. This includes the Height, Width, Rectangle, X and Y values
 repla = pygame.image.load("images/enemies/e1.png")
 repla = pygame.transform.scale(repla, (25, 25))
 replaRect = repla.get_rect()
 replaW = replaRect.width
 replaH = replaRect.height
 if level == 1:
   replaX = 120
   replaY = 120
 elif level == 2 or level == 3 or level == 4:
   replaX = 120
   replaY = 120
 elif level == 5 or level == 6:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 1:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 2:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 3:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 4:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 5:
   replaX = 200
   replaY = 339
 elif level > 6 and mazepick == 6:
   replaX = 200
   replaY = 339

 #This applies with the same set above, but with the character Cate
 cate = pygame.image.load("images/enemies/e1.png")
 cate = pygame.transform.scale(cate, (25, 25))
 cateRect = cate.get_rect()
 cateW = replaRect.width
 cateH = replaRect.height
 if level == 1:   #Is the current level 1?
   cateX = 0       #Then put the character here
   cateY = 15
 elif level == 2 or level == 3 or level == 4: #Is the level 2 or 3?
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level == 5 or level == 6:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 1:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 2:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 3:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 4:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 5:
   cateX = 0  #Then put the character here instead
   cateY = 15
 elif level > 6 and mazepick == 6:
   cateX = 0  #Then put the character here instead
   cateY = 15

 gelloleg = pygame.image.load("images/enemies/e2.png")
 gelloleg = pygame.transform.scale(gelloleg,(25,25))
 gelloRect = gelloleg.get_rect()
 gelloW = gelloRect.width
 gelloH = gelloRect.height
 if level == 1 or level == 2 or level == 3:
   gellX = 999
   gellY = 999
 else:
   gellX = 350
   gellY = 120

 don = pygame.image.load("images/enemies/e3.png")
 don = pygame.transform.scale(don,(25,25))
 donRect = don.get_rect()
 donW = donRect.width
 donH = donRect.height
 if level == 1 or level == 2 or level == 3:
   donX = 999
   donY = 999
 else:
   donX = 230
   donY = 300

 #I forgot to do this when I defined the vaccine variable
 vac = pygame.transform.scale(vac, (30, 30)) #Reshape the 
 #sprite so it is not too big
 exit = pygame.image.load("images/exit.png") #Load the exit screen
 exit = pygame.transform.scale(exit,(20, 20)) #transform
 exitRect = exit.get_rect()
 exitW = exitRect.width
 exitH = exitRect.height
 

 mazepick = random.randint(1,6)

 #This is the variable that holds the random situation when in contact with the powerup
 randompow = random.randint(1,5)

 #These variables hold the flavor text that appears when the powerup is obtained

 #---------------------------------------------
 # gl - great luck
 # n  - nothing
 # ow - Oh wow
 # sc - supa cool
 # tl - tough luck
 # bp - bad pill
 #---------------------------------------------
 gl = pygame.image.load("images/flavor_text/gl.png")
 n = pygame.image.load("images/flavor_text/n.png")
 ow = pygame.image.load("images/flavor_text/ow.png")
 sc = pygame.image.load("images/flavor_text/sc.png")
 tl = pygame.image.load("images/flavor_text/tl.png")
 bp = pygame.image.load("images/flavor_text/bp.png")
 

 #This function loops itself through the entirity of gameplay. It is responsible for making sure the sprites with their updated coordinates get blitted to the screen, and will blit things depending on the level itself.
 def reloadgraphics(event, power):    
    gameWindow.fill(WHITE) #Fill the background white  
    
    gameWindow.blit(borside,(borX,borY))
    gameWindow.blit(borside2,(bor2X,bor2Y))
    gameWindow.blit(bortop,(bortopX, bortopY))
    gameWindow.blit(bortop2,(bortop2X,bortop2Y))
    #If the current level is 1 or 2 or 3, draw a specific maze. Further on, pick a random value and set that value to the corresponding maze
    if level == 1:
     gameWindow.blit(level1, (0,0))  # redrawing the maze
    elif level == 2 or 3:
      gameWindow.blit(level2,(0,0))
    elif level == 4:
      gameWindow.blit(level3,(0,0))
    elif level == 5:
      gameWindow.blit(level4,(0,0))
    elif level == 6:
      gameWindow.blit(level5,(0,0))
    elif level > 6 and mazepick == 1:
      gameWindow.blit(level,(0,0))
    elif level > 6 and mazepick == 2:
      gameWindow.blit(level2,(0,0))
    elif level > 6 and mazepick == 3:
      gameWindow.blit(level3,(0,0))
    elif level > 6 and mazepick == 4:
      gameWindow.blit(level4,(0,0))
    elif level > 6 and mazepick == 5:
      gameWindow.blit(level5,(0,0))
    elif level > 6 and mazepick == 6:
      gameWindow.blit(levelZ,(0,0))
    else:
      #THIS SHOULD NEVER HAPPEN, BUT IF IT DOES, THE MESSAGE HANDLER COMES INTO PLAY
     print("NO LEVEL LOADED")
     messagetype = "ERROR - NONEXISTANT LEVEL"
     msghandler(messagetype)
    
    #blit the exit
    if level == 1:
     gameWindow.blit(exit,(exitX, exitY))
    elif level > 1:
      gameWindow.blit(exit,(exitX,exitY))
    #Has the vaccine been collected
    if gathered == 0:
      gameWindow.blit(vac,(ranX, ranY))  #Blit the vaccine on screen
      #Is the level 1 and the enemies aren't killed?
    if level == 1 and kill == 0 or not level == 1 and kill == 0:
      gameWindow.blit(repla,(replaX,replaY)) #blit the charaters
      gameWindow.blit(cate,(cateX, cateY))
      if power == 0: #has the power not been collected yet
       gameWindow.blit(powerup,(powerX,powerY)) #then blit it
    if level > 4 and kill == 0:
      gameWindow.blit(gelloleg,(gellX,gellY))
      gameWindow.blit(don,(donX,donY))
    if level > 3:
      gameWindow.blit(repla,(replaX, replaY))
      gameWindow.blit(cate,(cateX, cateY))
      gameWindow.blit(gelloleg,(gellX, gellY))
      gameWindow.blit(don,(donX, donY))

    pygame.draw.circle(gameWindow, ballCLR, (ballX,ballY), ballR,0)  #And draw the player
    if direction == "Down":
     gameWindow.blit(player, (ballX, ballY))
    pygame.display.flip() #Print it all

 
 level1 = pygame.image.load("images/1.png")
 wallCLR = level1.get_at((0,0))
 level2 = pygame.image.load("images/2.png") #load this instead
 wallCLR = level2.get_at((0,10)) #Get wall color
 level3 = pygame.image.load("images/3.png")
 wallCLR = level3.get_at((0,0))
 level4 = pygame.image.load("images/4.png")
 wallCLR = level4.get_at((0,0))
 level5 = pygame.image.load("images/5.png")
 wallCLR = level5.get_at((0,0))
 levelZ = pygame.image.load("images/6.png")
 wallCLR = levelZ.get_at((0,0))
 levelZ = pygame.image.load("images/7.png")
 wallCLR = levelZ.get_at((0,0))      
 levelZ = pygame.image.load("images/8.png")
 wallCLR = levelZ.get_at((0,0))
 levelZ = pygame.image.load("images/9.png")
 wallCLR = levelZ.get_at((0,0))
 levelZ = pygame.image.load("images/10.png")
 wallCLR = levelZ.get_at((0,0))
 levelZ = pygame.image.load("images/11.png")
 wallCLR = levelZ.get_at((0,0))
  
 while gameon == "game loaded":  #While the game is loaded?
    reloadgraphics(event, power) #Reload the graphics
    pygame.event.get() #And constantly listen for key events
   

   #------------------------------------------------
   # THIS IS THE AI SYSTEM FOR repla
   # It's position changes depending on where it
   # currently resides on the screen. This causes it
   # to purposely wander off on levels 2 and 3, which
   # make the player think that the next levels will get
   # easier.
   #------------------------------------------------
    if level == 1 or level > 1:
       if replaX < 160:
        if randompow == 5 and power == 1:
          replaX += 5
        elif level == 2 or level == 3 or level == 4:
          replaX += 3
        else:
          replaX += 1
       if replaX == 160:
         if randompow == 5 and power == 1:
          replaY -= 5
         elif level == 2 or level == 3 or level == 4:
          replaY -= 3
         else:
          replaY -= 1
       if replaY == 30:
         if randompow == 5 and power == 1:
          replaX += 5
         elif level == 2 or level == 3 or level == 4:
          replaX += 3
         else:
          replaX += 1
       if replaX == 240:
         if randompow == 5 and power == 1:
          replaY += 5
         elif level == 2 or level == 3 or level == 4:
          replaY += 3
         else:
          replaY += 1
       if replaY == 120:
         if randompow == 5 and power == 1:
          replaX += 5
         elif level == 2 or level == 3 or level == 4:
          replaX += 3
         else:
           replaX += 1
       if replaX == 360:
         if randompow == 5 and power == 1:
          replaY += 5
         elif level == 2 or level == 3 or level == 4:
          replaY += 3
         else:
          replaY += 1
       if replaY == 210:
         if randompow == 5 and power == 1:
          replaX += 5
         elif level == 2 or level == 3 or level == 4:
          replaX += 3
         else:
          replaX += 1
       if replaX == 490:
         if randompow == 5 and power == 1:
          replaY += 5
         elif level == 2 or level == 3 or level == 4:
          replaY += 3
         else:
          replaY += 1
       if replaY == 500:
         if randompow == 5 and power == 1:
          replaX -= 5
         elif level == 2 or level == 3 or level == 4:
          replaX -= 10
         else:
          replaX -= 10
       if replaX == 20:
         if randompow == 5 and power == 1:
          replaY -= 5
         elif level == 2 or level == 3 or level == 4:
          replaY -= 3
         else:
          replaY -= 1
       if replaY > 500:
         if randompow == 5 and power == 1:
          replaX -= 5
         elif level == 2 or level == 3 or level == 4:
          replaX -= 3
         else:
          replaX -= 1
       if replaX == -10:
         if randompow == 5 and power == 1:
           replaX = 0
           replaY = 0
         elif level == 2 or level == 3 or level == 4:
           replaX = 0
           replaY = 0
         else:
           replaX = 0
           replaY = 0
       if replaX == 10:
        if randompow == 5 and power == 1:
          replaX += 10
          replaY -= 10
        elif level == 2 or level == 3 or level == 4:
          replaX += 3
          replaY -= 3
        else:
          replaX += 1
          replaY -= 1
       if replaX == 20:
        if randompow == 5 and power == 1:
          replaY -= 5
        elif level == 2 or level == 3 or level == 4:
          replaY -= 3
        else:
          replaY -= 1
       if replaY == 400:
         if randompow == 5 and power == 1:
          replaX -= 5
         elif level == 2 or level == 3 or level == 4:
          replaX -= 10
         else:
          replaX -= 1
       if replaY > 159:
         if randompow == 5 and power == 1:
          replaX -= 5
         elif level == 2 or level == 3 or level == 4:
          replaX -= 10
         else:
          replaX -= 10
       if replaY > 161:
         if randompow == 5 and power == 1:
          replaX -= 5
         elif level == 2 or level == 3 or level == 4:
          replaX -= 10
         else:
          replaX -= 10
       if replaX == 0:
         if randompow == 5 and power == 1:
          replaX += 5
         elif level == 2 or level == 3 or level == 4:
          replaX += 3
         else:
          replaX += 1
       if replaX >= width:
         if randompow == 5 and power == 1:
          replaX += 5
         elif level == 2 or level == 3 or level == 4:
          replaX += 3
         else:
          replaX += 3
#--------------------------------------------
# THIS IS THE AI SYSTEM FOR CATE.
# It is very similar to Repla
#--------------------------------------------

    if level == 1 or level > 1:      
      if cateX == 0:
        if randompow == 5 and power == 1:
          cateY += 5
        elif level == 2 or level == 3 or level == 4:
          cateY += 3
        else:
          cateY += 1
      if cateY == 110:
        if randompow == 5 and power == 1:
          cateX += 5
        elif level == 2 or level == 3 or level == 4:
          cateX += 3
        else:
          cateX += 1
      if cateX == 40:
        if randompow == 5 and power == 1:
          cateY += 5
        elif level == 2 or level == 3 or level == 4:
          cateY += 3
        else:
          cateY += 1
      if cateY == 240:
        if randompow == 5 and power == 1:
          cateX += 5
        elif level == 2 or level == 3 or level == 4:
          cateX += 3
        else:
          cateX += 1
      if cateY == 240:
        if randompow == 5 and power == 1:
          cateX += 5
        elif level == 2 or level == 3 or level == 4:
          cateX += 3
        else:
          cateX += 1
      if cateX == 700:
        if randompow == 5 and power == 1:
          cateX = 0
          cateY = 15
        elif level == 2 or level == 3 or level == 4:
          cateX = 0
          cateY = 15
        else:
          cateX = 0
          cateY = 15
      if cateX == 340:
        if randompow == 5 and power == 1:
          cateY += 5
        elif level == 2 or level == 3 or level == 4:
          cateY += 3
        else:
          cateY += 1
      if cateY == 500:
        if randompow == 5 and power == 1:
          cateX += 5
        elif level == 2 or level == 3 or level == 4:
          cateX += 3
        else:
          cateX += 1


#-----------------------------------------------
#      THIS IS THE AI SYSTEM FOR GELLOLEG
#-----------------------------------------------
    if level == 5 or level > 5:      
      if gellX == 350:
        if randompow == 5 and power == 1:
          gellY += 5
        elif level == 2 or level == 3 or level == 4:
          gellY += 3
        else:
          gellY += 1
      if gellY == 220:
        if randompow == 5 and power == 1:
          gellX -= 5
        elif level == 2 or level == 3 or level == 4:
          gellX -= 3
        else:
          gellX -= 1
      if gellX == 40:
        if randompow == 5 and power == 1:
          gellY += 5
        elif level == 2 or level == 3 or level == 4:
          gellY += 3
        else:
          gellY += 1
      if gellY == 440:
        if randompow == 5 and power == 1:
          gellX += 5
        elif level == 2 or level == 3 or level == 4:
          gellX += 3
        else:
          gellX += 1
      if gellX == 640:
        if randompow == 5 and power == 1:
          gellY -= 5
        elif level == 2 or level == 3 or level == 4:
          gellY -= 3
        else:
          gellY -= 1
      if gellY == 10:
        if randompow == 5 and power == 1:
          gellX -= 5
        elif level == 2 or level == 3 or level == 4:
          gellX -= 3
        else:
          gellX -= 1


    if level == 5 or level > 5:      
      if donY == 300:
        if randompow == 5 and power == 1:
          donX -= 5
        elif level == 2 or level == 3 or level == 4:
          donX -= 3
        else:
          donX -= 1
      if donX == 180:
        if randompow == 5 and power == 1:
          donY += 5
        elif level == 2 or level == 3 or level == 4:
          donY += 3
        else:
          donY += 1
      if donY == 140:
        if randompow == 5 and power == 1:
          donX -= 5
        elif level == 2 or level == 3 or level == 4:
          donX -= 3
        else:
          donX -= 1
      if donX == 4:
        if randompow == 5 and power == 1:
          donY -= 5
        elif level == 2 or level == 3 or level == 4:
          donY -= 3
        else:
          donX -= 1
      if donY == 12:
        if randompow == 5 and power == 1:
          donX += 5
        elif level == 2 or level == 3 or level == 4:
          donX += 3
        else:
          donX += 1
      if donX == 500:
        if randompow == 5 and power == 1:
          donY += 5
        elif level == 2 or level == 3 or level == 4:
          donY += 3
        else:
          donY += 1



    keys = pygame.key.get_pressed()#Check for key down events
    if keys[pygame.K_LEFT] and ballX > ballR + stepX: #Was the left arrow key pressed and the x axis is greater than the radius and the added step?
        ballX = ballX - stepX  #Then decrease it (character moves left)
    if keys[pygame.K_RIGHT] and ballX < width - ballR - stepX:  #Was the right arrow key pressed and the width combined with the radius and previous step is still greater than the x axis?
        ballX = ballX + stepX #Then move a step forward (character moves right)
    
    #The next two statments were VERY DIFFICULT to program efficiently!!
    #Nonetheless, with a little help from examples, it's all here!
    if keys[pygame.K_UP] and ballY > ballR + stepY: #Was the up arrow key pressed and the Y axis is greater than the vertical step and the radius?
        ballY = ballY - stepY  #Then move one vertical step upwards by decreasing the Y axis and the vertical step
    if keys[pygame.K_DOWN] and ballY < height - ballR - stepY:   #Was the down arrow key pressed and the Y axis less than the height and radius combined?
        ballY = ballY + stepY #Then move one vertical step downwards by increasing the step axis
    shipRect = pygame.Rect(ballX,ballY,shipW,shipH)
    asteroidRect = pygame.Rect(resultX,resultY,asteroidW,asteroidH)
    if asteroidRect.colliderect(shipRect):
        gathered += 1
        pygame.mixer.music.load("music/collected.mp3")
        pygame.mixer.music.play(0)
    exitRect = pygame.Rect(exitX,exitY,exitW,exitH)
    if exitRect.colliderect(shipRect):
      if gathered > 0:
        if level == 1:
          ending()
        else:
          print("Exit enabled...")
          print("Level complete...")
          gameon = "Level Completed!"
          levelcompleted(gameon, level)
      else:
        messagetype = "DENIED"
        msghandler(messagetype)
    replaRect = pygame.Rect(replaX,replaY,replaW,replaH)
    cateRect = pygame.Rect(cateX, cateY, cateW, cateH)
    gellRect = pygame.Rect(gellX, gellY, gelloW, gelloH)
    donRect = pygame.Rect(donX, donY, donW, donH)
    borderRect = pygame.Rect(borX, borY, borderW, borderH)
    border2Rect = pygame.Rect(bortop2X, bortop2Y, bortop2W, bortop2H)
    if replaRect.colliderect(shipRect):
        print("died!")  #debug message: the cursed child
        #lives -= 1  #decrease lives by 1
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(400)  #Wait a few seconds to let the sweet Contra sound play
        lives  = died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
        return(lives)
    if cateRect.colliderect(shipRect):
        print("died!")  #debug message: the cursed child
        #lives -= 1  #decrease lives by 1
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(4000)  #Wait a few seconds to let the sweet Contra sound play
        lives = died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
        return(lives)
    if gellRect.colliderect(shipRect):
        print("died!")  #debug message: the cursed child
        #lives -= 1  #decrease lives by 1
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(4000)  #Wait a few seconds to let the sweet Contra sound play
        lives = died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
        return(lives)
    if donRect.colliderect(shipRect):
        print("died!")  #debug message: the cursed child
        #lives -= 1  #decrease lives by 1
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(4000)  #Wait a few seconds to let the sweet Contra sound play
        lives = died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
        return(lives)

    if borderRect.colliderect(replaRect):
      replaX = 120
      replaY = 120
    if border2Rect.colliderect(replaRect):
      replaX = 120
      replaY = 120
    if bortopRect.colliderect(replaRect):
      replaX = 120
      replaY = 120
    if bortop2Rect.colliderect(replaRect):
      replaX = 120
      replaY = 120
    if borderRect.colliderect(gellRect):
      gellX = 350
      gellY = 120
    if border2Rect.colliderect(gellRect):
      gellX = 350
      gellY = 120
    if bortopRect.colliderect(gellRect):
      gellX = 350
      gellY = 120
    if bortop2Rect.colliderect(gellRect):
      gellX = 350
      gellY = 120
    if borderRect.colliderect(donRect):
      donX = 230
      donY = 300
    if border2Rect.colliderect(donRect):
      donX = 230
      donY = 300
    if bortopRect.colliderect(donRect):
      donX = 230
      donY = 300
    if bortop2Rect.colliderect(donRect):
      donX = 230
      donY = 300


    powRect = pygame.Rect(powerX,powerY,powerW,powerH)
    if powRect.colliderect(shipRect):
      print("Powerup obtained!!")
      print("determining value for powerup...")
      if randompow == 1:
       print("Wow! Fantastic luck!")
       print("All monsters are now killed!")
       pygame.mixer.music.load("music/gl.wav")
       pygame.mixer.music.play(0)
       gameWindow.blit(gl,(0,0))
       pygame.display.flip()
       pygame.time.wait(2000)
       event = 1
       kill = 1
       powerY = 999
       powerX = 999
      if randompow == 2:
       print("Super cool stuff!")
       print("Your character runs faster!")
       pygame.mixer.music.load("music/sc.wav")
       pygame.mixer.music.play(0)
       gameWindow.blit(sc,(0,0))
       pygame.display.flip()
       pygame.time.wait(2000)
       stepX = 15
       stepY = 15
       youfaster = 1
       event = 2
       powerY = 999
       powerX = 999
      if randompow == 3:
       gameWindow.blit(n,(0,0))
       pygame.display.flip()
       pygame.time.wait(2000)
       print("Nothing...")
       print("It's just a normal pill...")
       pygame.mixer.music.load("music/n.wav")
       pygame.mixer.music.play(0)
       event = 3
       power = 1
       powerY = 999
       powerX = 999
      if randompow == 4:
       gameWindow.blit(ow,(0,0))
       pygame.display.flip()
       pygame.time.wait(2000)
       print("Oh wow!")
       print("The exit is wide open!")
       pygame.mixer.music.load("music/ow.wav")
       pygame.mixer.music.play(0)
       gathered += 1
       event = 4
       power = 1
       powerY = 999
       powerX = 999
      if randompow == 5:
       gameWindow.blit(tl,(0,0))
       pygame.display.flip()
       pygame.time.wait(2000)
       print("Oh great...")
       print("Monsters are 10 times faster.")
       pygame.mixer.music.load("music/tl.wav")
       pygame.mixer.music.play(0)
       faster = 1
       event = 5
       power = 1
       powerY = 999
       powerX = 999

    #This set of statements are for collision, specifically for the walls. They are color-based, and will activate when the player touches the walls
    
    #Is the player's X and Y plus the radius positive and the color is the wall color? Is the player's X and radius negative and color touching is he wall color? Is the X axis Y axis AND radius positive and touching the wall?Is everything negative (moving up or left)? Then kill the player
    #if level == 1: 
    #if level1.get_at((ballX+ballR+1, ballY)) == wallCLR or \
       #level1.get_at((ballX - ballR - 1, ballY)) == wallCLR or \
       #level1.get_at((ballX, ballY + ballR + 1)) == wallCLR or \
       #level1.get_at((ballX, ballY - ballR - 1)) == wallCLR:
        #print("died!")  #debug message: the cursed child
        #lives -= 1  #decrease lives by 1
        #gameon = "Died"     #Set the game mode to dead
        #pygame.time.wait(400)  #Wait a few seconds to let the sweet Contra sound play
        #died(ballX, ballY, Xorigin, Yorigin, gameon, lives)  #and call the dead function
    #if level == 5:
     # if level1.get_at((ballX+ballR+1, ballY)) == wallCLR or \
      # level1.get_at((ballX - ballR - 1, ballY)) == wallCLR or \
       #level1.get_at((ballX, ballY + ballR + 1)) == wallCLR or \
       #level1.get_at((ballX, ballY - ballR - 1)) == wallCLR:
        #print("died!")  #debug message: the cursed child
        #pygame.mixer.music.load("music/die.wav")
        #pygame.mixer.music.play(0)
        #gameon = "Died"     #Set the game mode to dead
        #pygame.time.wait(400)  #Wait a few seconds to let the sweet Contra sound play
        #died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
    if level == 6:
      if level5.get_at((ballX+ballR+1, ballY)) == wallCLR or \
       level5.get_at((ballX - ballR - 1, ballY)) == wallCLR or \
       level5.get_at((ballX, ballY + ballR + 1)) == wallCLR or \
       level5.get_at((ballX, ballY - ballR - 1)) == wallCLR:
        print("died!")  #debug message: the cursed child
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(4000)  #Wait a few seconds to let the sweet Contra sound play
        died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function
    if level > 6:
      if levelZ.get_at((ballX+ballR+1, ballY)) == wallCLR or \
       levelZ.get_at((ballX - ballR - 1, ballY)) == wallCLR or \
       levelZ.get_at((ballX, ballY + ballR + 1)) == wallCLR or \
       levelZ.get_at((ballX, ballY - ballR - 1)) == wallCLR:
        print("died!")  #debug message: the cursed child
        pygame.mixer.music.load("music/die.wav")
        pygame.mixer.music.play(0)
        gameon = "Died"     #Set the game mode to dead
        pygame.time.wait(4000)  #Wait a few seconds to let the sweet Contra sound play
        died(ballX, ballY, Xorigin, Yorigin, gameon)  #and call the dead function




#This is the function that runs when the player loses a life, no matter what reason that could be.

def died(ballX, ballY, Xorigin, Yorigin, gameon):
  global lives
  lives -= 1
  pygame.mixer.music.load("music/static.wav")
  pygame.mixer.music.play(0)
  static = pygame.image.load("images/static/pic0.jpg")
  static2 = pygame.image.load("images/static/pic1.jpg")
  static3 = pygame.image.load("images/static/pic2.jpg")
  static4 = pygame.image.load("images/static/pic3.gif")
  gameWindow.blit(static,(0,0))
  pygame.display.flip()
  gameWindow.blit(static2,(0,0))
  pygame.display.flip()
  gameWindow.blit(static3,(0,0))
  pygame.display.flip()
  gameWindow.blit(static4,(0,0))
  pygame.display.flip()
  gameWindow.blit(static,(0,0))
  pygame.display.flip()
  gameWindow.blit(static2,(0,0))
  pygame.display.flip()
  gameWindow.blit(static3,(0,0))
  pygame.display.flip()
  gameWindow.blit(static4,(0,0))
  pygame.display.flip()
  gameWindow.blit(static,(0,0))
  pygame.display.flip()
  gameWindow.blit(static2,(0,0))
  pygame.display.flip()
  gameWindow.blit(static3,(0,0))
  pygame.display.flip()
  gameWindow.blit(static4,(0,0))
  pygame.display.flip()
  gameWindow.blit(static,(0,0))
  pygame.display.flip()
  gameWindow.blit(static2,(0,0))
  pygame.display.flip()
  gameWindow.blit(static3,(0,0))
  pygame.display.flip()
  
  while gameon == "Died":  #While the game mode is dead
    ballX = Xorigin                                         # put ball back at starting location
    ballY = Yorigin
    pygame.time.wait(7000)  #Wait a bit
    print("returning back one step...") #and return 
    gameon = "Lives Screen"     #to the lives screen
    introprinter(level, lives, livemessage, gameon, gathered)
    return(lives, level)


#The game over function
def gameover(gameon):
  print("The game is over")
  while gameon == "Game Over":
    print("End Screen enabled") #debugging feature to let us know it has successfully loaded
    game = pygame.image.load("images/gameover.png")
    gameWindow.blit(game, (0,0))
    pygame.display.flip()    #Update screen display
    for event in pygame.event.get():#Capture pygame events
      if event.type == pygame.KEYDOWN:#Check if a key was pressed
        if event.key == pygame.K_ESCAPE: #Was it space?
          print("escape was pressed") #A debugging thing
          exit()


#This is the function that runs after the boss is defeated at level 1462
def ending():
  hang = False
  pygame.mixer.music.load("music/ending.wav")
  pygame.mixer.music.play(0)
  print("Ending in progress...") #debugging feature
  text1 = pygame.image.load("images/ye.png")#load the backdrop
  gameWindow.blit(text1, (0,0))  #Load the first text
  pygame.display.update()     #print to the screen
  pygame.time.wait(3000)       #wait a few miliseconds
  pologuy = pygame.image.load("images/blue.png")
  polX = 0
  end = pygame.image.load("images/end.png")
  while polX < 480:
    polX += 40
    gameWindow.blit(text1, (0,0))
    gameWindow.blit(pologuy, (polX, 0))
    pygame.display.update()
  complete = pygame.image.load("images/you.png")
  poloend = pygame.image.load("images/poloend.png")
  gameWindow.blit(text1, (0,0))
  gameWindow.blit(complete, (10,10))
  pygame.display.update()
  endX = 480
  pygame.time.wait(7000)
  while endX > 0:
    endX += -20
    gameWindow.blit(end, (endX, 0))
    pygame.display.update()
  pygame.time.wait(2000)
  endX = 48000
  while endX > 0:
    endX += -20
    hang = True
  while hang == True:
    gameWindow.blit(poloend, (endX, 110))
    pygame.display.update()

def cutscene1(gameon):
  global level
  intro = pygame.image.load("images/intro2.png")
  livecounter = font.render(str(lives),1,white)
  sayit = font.render(str(livemessage),1,white)
  gameWindow.blit(intro, (0,0))
  gameWindow.blit(livecounter,(310, 50))   #to their
  gameWindow.blit(sayit,(150, 50))  #x and y values
  pygame.display.flip()
  pygame.time.wait(9000)
  gameon = "game loaded"
  rungame(gameon, level, lives, gathered)
  return(level)
title(gameon, start)