# Import tkinter library
import serial
import tkinter as tk
import threading
from time import sleep
import random

from PIL import ImageTk as imtk
from PIL import Image as im


import RPi.GPIO as GPIO



#%%
# Create an instance of tkinter frame or window
root = tk.Tk()
root.attributes('-fullscreen',True)

mainframe = tk.Frame(root,width=1920, height=1080, bg="black")
mainframe.pack()



textFrame = tk.Frame(mainframe, bg="black")
textFrame.place(y=700,height=240,width = 1920)


imageframe = tk.Frame(mainframe, bg="black")
imageframe.place(height=700,width = 1920)


rock = imtk.PhotoImage(im.open('Images/rock.png'))
paper = imtk.PhotoImage(im.open('Images/paper.png'))
scissors = imtk.PhotoImage(im.open('Images/scissors.png'))
three = imtk.PhotoImage(im.open('Images/three.png'))
two = imtk.PhotoImage(im.open('Images/two.png'))
one = imtk.PhotoImage(im.open('Images/one.png'))
go = imtk.PhotoImage(im.open('Images/go.png'))
instruction = imtk.PhotoImage(im.open('Images/instruction.png'))
welcome = imtk.PhotoImage(im.open('Images/welcome.png'))


global move_list 
move_list = ["Rock", "Paper", "Scissors"]





#  IT IS THE GPIO NUMBER NOT THE PIN NUMBER ON THE SCHEMATIC 
#Thumb
# 0.7F, 0.6B 
in1=17 #pin 11
in2=18 #pin 12

#0.7 for both
#Index
in3=7 #pin 26
in4=8 #pin 24

#0.7 for both
#Middle
in5=22 #pin 15
in6=27 #pin 13

#0.6F, 0.9B
#Ring
in7=5 #pin 29
in8=6 #pin 31

#0.6F, 0.7B
#Pinky
in9=19 #pin 35
in10=16 #pin 36

#enable pin
enable =10 #pin 19

gpio=[in1,in2,in3,in4,in5,in6,in6,in7,in8,in9,in10]

#Time delay to determine angle of rotation
delayTime=3

GPIO.setmode(GPIO.BCM)
for i in gpio:
    GPIO.setup(i,GPIO.OUT)

GPIO.setup(enable,GPIO.OUT)

#%%
def move_finger(pin1,pin2):
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)
    # sleep(delayTime)

#%% NEUTRAL TO ROCK, PULL FORWARD ALL 5 FINGERS 
def N_Rock():
    move_finger(in1,in2) #Thumb
    move_finger(in3,in4) #Index
    move_finger(in5,in6) #Middle
    move_finger(in7,in8) #Ring
    move_finger(in9,in10) #pinky
    sleep(0.7)
    stop_finger(in2,in1) #Thumb
    stop_finger(in4,in3) #Index
    stop_finger(in6,in5) #Middle
    stop_finger(in8,in7) #Ring
    stop_finger(in10,in9) #pinky
    pass

#%% NEUTRAL TO PAPER, DO NOTHING
def N_Paper():
    pass

def stop_finger(inp1,inp2):
    GPIO.output(inp1, GPIO.LOW)
    GPIO.output(inp2, GPIO.LOW)

#%% NEUTRAL TO SCISSORS, PULL FORWARD FINGERS 1,4 AND 5

def N_Scissors():
    move_finger(in1,in2) #Thumb
    move_finger(in7,in8) #Ring
    move_finger(in9,in10) #pinky
    sleep(0.7)
    stop_finger(in2,in1) #Thumb
    stop_finger(in8,in7) #Ring
    stop_finger(in10,in9) #pinky
    

#%% PAPER TO NEUTRAL, DO NOTHING
def P_Neutral():
    pass

#%% ROCK TO NEUTRAL, PULL BACKWARD ALL 5 FINGERS

def R_Neutral():
    move_finger(in2,in1) #Thumb
    move_finger(in4,in3) #Index
    move_finger(in6,in5) #Middle
    move_finger(in8,in7) #Ring
    move_finger(in10,in9) #pinky
    sleep(0.8)
    stop_finger(in2,in1) #Thumb
    stop_finger(in4,in3) #Index
    stop_finger(in6,in5) #Middle
    stop_finger(in8,in7) #Ring
    stop_finger(in10,in9) #pinky

#%% SCISSORS TO NEUTRAL, PULL BACKWARDS FINGERS 1,4 AND 5
def S_Neutral():
    move_finger(in2,in1) #Thumb
    move_finger(in8,in7) #Ring
    move_finger(in10,in9) #pinky
    sleep(0.8)
    stop_finger(in2,in1) #Thumb
    stop_finger(in8,in7) #Ring
    stop_finger(in10,in9) #pinky

#%%
#All TO LOW
def all_to_low():
    for i in gpio:
        GPIO.output(i, GPIO.LOW)

# GPIO.cleanup()



#%%
def hand_movement(move):
   
  
    if move == "Paper":
        N_Paper()
    elif move == "Rock":
        N_Rock()
    elif move== "Scissors":
        N_Scissors()

def reverse_hand_movement(move):
    if move == "Paper":
        P_Neutral()
    elif move == "Rock":
        R_Neutral()
    elif move== "Scissors":
        S_Neutral()
        
        



#%%
def clear_frame(frame):
   for widgets in frame.winfo_children():
      widgets.destroy()


#%%
def change_screen(old_panel, item, name):
    if (name == ""):
        clear_frame(textFrame)
    else:
        text.delete("1.0","end")
        text.insert(tk.INSERT, name)
    old_panel.config(image='')
    new_panel = tk.Label(imageframe, image = item, bg = "black")
    new_panel.pack(side = "top", fill = "both", expand = "yes")
    root.update()
    return new_panel




#%%
def define_winner(robot_move,player_move):
    global w_streak
    global l_streak
    global player_wins
    global robot_wins
    global game_counter

    outcome = ""
    if player_move == robot_move:
           outcome = "draw"
           w_streak = 0
           l_streak = 0
    elif player_move == "Rock" and robot_move == "Scissors" or player_move == "Scissors" and robot_move == "Paper" or player_move == "Paper" and robot_move == "Rock":
           outcome = "winner"
           w_streak += 1
           l_streak = 0
           player_wins +=1
           game_counter += 1
    elif player_move == "Scissors" and robot_move == "Rock" or player_move == "Paper" and robot_move == "Scissors" or player_move == "Rock" and robot_move == "Paper":
           outcome = "loser"
           w_streak = 0
           l_streak += 1
           robot_wins +=1
           game_counter += 1
    elif player_move == "None":
           none_detected()
           outcome = ""
         
    elif player_move == "quit":
           return 
    
    return outcome
          
           


#%%                       
def game_algorithm(outcome, player):
            global w_streak
            global l_streak
            move_list = ["Rock", "Paper", "Scissors"]
            if (outcome == "winner" and w_streak >=2):
                next_move = "Rock"
            elif (outcome == "loser" and l_streak >=2):
                next_move = "Paper"
            elif outcome == "winner" and w_streak ==1:
                if player == "Rock":
                    next_move = "Paper"
                elif player == "Paper":
                    next_move = "Scissors"
                elif player =="Scissors":
                    next_move = "Rock"
            elif outcome == "loser" and l_streak ==1:
                if player == "Rock":
                    next_move = "Scissors"
                elif player == "Paper":
                    next_move = "Rock"
                elif player =="Scissors":
                    next_move = "Paper"
            elif outcome == "draw":
                next_move = random.choice(move_list)
                
            return next_move

#%%
def outcome_screen(outcome):
    global text
    global win
    global lose
    global tie
    response_message=""
    if outcome == "winner":
        response_message = "PLAYER WINS!!"
        screen = random.choice(win)
    elif outcome == "loser":
        response_message = "PLAYER LOSES!"
        screen = random.choice(lose)
    elif outcome == "draw":
        response_message = "IT'S A TIE!"
        screen = random.choice(tie)
        
    text = tk.Text(textFrame, font="Calibri, 40",bd=15)
    text.insert(tk.INSERT, response_message)
    text.insert(tk.INSERT, "\n\nPress the 'z' key to start the next round!")
    text.pack()

    return screen

#%%
def instruction_screen():
    instructionFrame = tk.Frame(mainframe)
    instructionFrame.place(x=0,y=0,height=1920,width = 1080)
    instruc_panel = tk.Label(instructionFrame, image = instruction,bg = "black")
    instruc_panel.pack()
    root.update()
    sleep(5)
    
    clear_frame(instructionFrame)
    instructionFrame.place_forget()
    root.update()

#%%
def final_screen(outcome):
    global text
    global win_img
    global lose
    global panel
    
   
    
    if (outcome == "win"):
        text = tk.Text(textFrame, font="Calibri, 40",bd=15)
        text.insert(tk.INSERT, "OH NO I CAN'T BELIEVE YOU BEAT ME \n")
        text.insert(tk.INSERT, "You win! Press the 'z' key to play again! \n")
        text.pack()
        panel = tk.Label(imageframe, image = random.choice(win_img),bg = "black")
        panel.pack(side = "top", fill = "both", expand = "yes")
    elif(outcome == "lose"):
        text = tk.Text(textFrame, font="Calibri, 40",bd=15)
        text.insert(tk.INSERT, "HA HA OF COURSE I WON \n")
        text.insert(tk.INSERT, "You lose! Press the 'z' key to play again! \n")
        text.pack()
        panel = tk.Label(imageframe, image = random.choice(lose),bg = "black")
        panel.pack(side = "top", fill = "both", expand = "yes")

#%%
def number_to_move(buffer):
    buffer = buffer.decode('UTF-8')

    response = {'-1':"None", '0':'Rock', '1':'Paper', '2':'Scissors'}
    return response[buffer]


#%%

def detections_thread():
    serial_1 = serial.Serial(port = '/dev/ttyS0',baudrate= 460800, bytesize=8, timeout = 1)
    global buffer
    buffer = None
    while(True):
        serial_1.write(b"RXed")
        print("waiting to RX input...")
        buffer = serial_1.read()
        sleep(0.03)
        data_left = serial_1.inWaiting()
        buffer+= serial_1.read(data_left)
        print(buffer)


#%%
def main():
    all_to_low()
    GPIO.output(enable,GPIO.HIGH)
    
    #tie
    global tie
    annoyed = imtk.PhotoImage(im.open('Images/annoyed.png'))
    annoyed2 = imtk.PhotoImage(im.open('Images/annoyed2.png'))
    confused = imtk.PhotoImage(im.open('Images/confused.png'))
    confused2 = imtk.PhotoImage(im.open('Images/confused2.png'))
    tie = [annoyed, annoyed2, confused, confused2]
    
    #win
    global win
    angry = imtk.PhotoImage(im.open('Images/angry.png'))
    angry2= imtk.PhotoImage(im.open('Images/angry2.png'))
    cry = imtk.PhotoImage(im.open('Images/cry.png'))
    cry2 = imtk.PhotoImage(im.open('Images/cry2.png'))
    sad = imtk.PhotoImage(im.open('Images/sad.png'))
    sad2 = imtk.PhotoImage(im.open('Images/sad2.png'))
    win = [angry, angry2, cry, cry2,sad,sad2]
    
    #lose
    global lose
    smug = imtk.PhotoImage(im.open('Images/smug.png'))
    smug2 = imtk.PhotoImage(im.open('Images/smug2.png'))
    happy = imtk.PhotoImage(im.open('Images/happy.png'))
    happy2 = imtk.PhotoImage(im.open('Images/happy2.png'))
    happy3 = imtk.PhotoImage(im.open('Images/happy3.png'))
    happy4 = imtk.PhotoImage(im.open('Images/happy4.png'))
    lose = [smug, smug2,happy,happy2,happy3,happy4]
 
    global win_img
    win_img = [annoyed,annoyed2, cry, cry2,sad,sad2]
    
    global panel
    panel = tk.Label(imageframe, image = welcome,bg = "black")
    panel.pack(side = "top", fill = "both", expand = "yes")
    
    global player_wins
    player_wins = 0
    
    global robot_wins
    robot_wins =0
    
    global w_streak 
    w_streak = 0
    global l_streak
    l_streak = 0
            
    global game_counter
    game_counter =1
    global text
    global move_list
    
    
    rx = threading.Thread(target = detections_thread, daemon= True)
    rx.start()

    text = tk.Text(textFrame, font="Calibri, 40",bd=15)
    text.insert(tk.INSERT, "Welcome! Press the 'z' Key to Play")
    text.pack()

    global response
    response = random.choice(move_list)
    
    
    root.bind('<KeyPress>',key_press)
    root.mainloop()



#%%
def game_code():
     
    global response
    global game_counter
    global panel
    global buffer
    global player_wins
    global robot_wins
    global mode
        
        
    print(game_counter)
   
    three_panel = change_screen(panel,three, "")
    sleep(1)
    two_panel = change_screen(three_panel,two, "")

    sleep(1)

    one_panel = change_screen(two_panel,one, "")
    sleep(1)
    clear_frame(textFrame)
    clear_frame(imageframe)
    goFrame = tk.Frame(mainframe, bg="black")
    goFrame.place(x=540,height=700,width = 1080)
    new_panel = tk.Label(goFrame, image = go, bg = "black")
    new_panel.pack(side = "bottom", fill = "none", expand = "yes")

  
    text = tk.Text(textFrame, font="Calibri, 40",bd=15)
    move_message = "Robot Played: " + response 
    text.insert(tk.INSERT, move_message)
    text.pack()

    root.update()
    
    sleep(1)
    
    player=number_to_move(buffer)
    
    if (mode == "party"):
        if (player == "Rock"):
            response = "Paper"
        elif (player == "Paper"):
            response = "Scissors"
        elif (player == "Scissors"):
            response = "Rock"

 
    hand_movement(response)

    clear_frame(goFrame)
    clear_frame(textFrame)
    goFrame.place_forget()
    root.update()
    
    

    result = define_winner(response,player)
    if (result == ""):
        reverse_hand_movement(response)
        return
    
    
    if (player_wins >2):
        final_screen("win")
        sleep(2)
        reverse_hand_movement(response)
        return
    elif (robot_wins > 2):
        final_screen("lose")
        sleep(2)
        reverse_hand_movement(response)
        return
    else:
        screen = outcome_screen(result) 

    

    panel = tk.Label(imageframe, image = screen,bg = "black")
    panel.pack(side = "top", fill = "both", expand = "yes")
    root.update()

    sleep(2)
    reverse_hand_movement(response)


    if game_counter >4:
        response = random.choice(move_list)
    else:
        response = game_algorithm(result, player)
        
    

#%%
   
def none_detected():
    global panel
    global text
    global tie
    
    im = tie[2]
    text = tk.Text(textFrame, font="Calibri, 40",bd=15)
    text.insert(tk.INSERT, "Oh no I didn't see anything! \n")
    text.insert(tk.INSERT, "Press the 'z' key to try again")
    text.pack()
    panel = tk.Label(imageframe, image = im,bg = "black")
    panel.pack(side = "top", fill = "both", expand = "yes")





#%%
def key_press(e): 
    global player_wins
    global robot_wins
    global mode

    if (player_wins >2 or robot_wins >2):
        clear_frame(textFrame)
        clear_frame(imageframe)
        main()
        
    if (e.keysym =='i'):
        instruction_screen()
    elif (e.keysym =='z'):
        mode = "game"
        game_code()
  

  
    elif (e.keysym =='s'):
        mode = "party"
        game_code()


    elif (e.keysym =='p'):
        N_Scissors()
    elif (e.keysym =='o'):
        S_Neutral()
    elif (e.keysym =='y'):
        N_Rock()
    elif (e.keysym =='u'):
        R_Neutral()

#  IT IS THE GPIO NUMBER NOT THE PIN NUMBER ON THE SCHEMATIC 
#Thumb
# 0.7F, 0.6B 
# in1=17 #pin 11
# in2=18 #pin 12

# #0.7 for both
# #Index
# in3=7 #pin 26
# in4=8 #pin 24

# #0.7 for both
# #Middle
# in5=22 #pin 15
# in6=27 #pin 13

# #0.6F, 0.9B
# #Ring
# in7=5 #pin 29
# in8=6 #pin 31

# #0.6F, 0.7B
# #Pinky
# in9=19 #pin 35
# in10=16 #pin 36
    


#%%
main()