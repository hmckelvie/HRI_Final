#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_leg_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
right_leg_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
head_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE,
                        gears=[[1, 24], [12, 36]])
color_sensor = ColorSensor(Port.S3)
pet_touch_sensor = TouchSensor(Port.S1)
tail_touch_sensor = TouchSensor(Port.S4)
distance_sensor = UltrasonicSensor(Port.S2)


def intro(speaker):
    speaker.say("Hi I am Fluffy")
    wait(500)
    speaker.say("I know my voice is a bit weird, I am sorry!")
    wait(500)
    speaker.say("I am a robot puppy that will help you learn about robots.")
    wait(200)
    speaker.say("You can play with my sensors.")
    wait(200)
    speaker.say("Sensors tell me about what is happening around me")
    wait(2000)
    speaker.say("Try to find my sensors! They will look like buttons on me")
    wait(500)
    speaker.say("Press button on top of my face to stop me")
    wait(2000)


def color_to_string(color):
    color = str(color)
    idx = color.index('.')
    return color[idx+1:]

def robot_fact(speaker, fact_count):
    robot_facts = [ ['Many people think of robots as machines that look and act like people',  'like C-3PO from Star Wars', 'but this is not always true!'],
                ['Robots are controlled by computers', 'people code what they do!'],
                ['Robots have sensors', 'they tell the computer about what is around the robot.', 'From my sensors, I can see that the surface below me is'],
                ['Robots use motors to move.', 'See I am using my robot to hop!'],
                ['Robots can be built to do jobs,','like the Roomba cleans.'],
                ['You might heard about C-3PO and R-2 D-2 and BB-8 from star wars.', 'They are really cool, but it would be hard to build a robot like them in real life.'],
                ['Even though computers are smart,', 'robots aren\'t perfect and I try my best'],
                ['I am built with special legos']
              ]
    idx = fact_count % len(robot_facts)
    speaker.set_volume(100, "_all_")
    speaker.set_speech_options(voice='m4', speed=130) #f5, m2, m3

    #color of surface
    if idx == 2:
        for chunk in robot_facts[idx]:
            speaker.say(chunk)
            wait(200)
        color = color_sensor.color()
        color = color_to_string(color)
        speaker.say(color)
        wait(500)
        speaker.say("Sometimes I get colors wrong because my sensors aren't perfect")
    #spin
    elif idx == 3:
        for chunk in robot_facts[idx]:
            speaker.say(chunk)
            wait(200)
        #Hop
    else:
        for chunk in robot_facts[idx]:
            speaker.say(chunk)
            wait(200)

def move_head():
    ev3.screen.load_image(ImageFile.NEUTRAL)
    ev3.speaker.say("Look up")
    head_motor.run(20)
    ev3.screen.load_image(ImageFile.UP)
    wait(2000)
    head_motor.stop()
    ev3.speaker.say("The sky looks pretty")
    wait(3000)
    ev3.screen.load_image(ImageFile.NEUTRAL)
    head_motor.run(-20)
    wait(2000)
    head_motor.stop()

def hop():
    #Makes the puppy hop
    ev3.screen.load_image(ImageFile.UP)
    left_leg_motor.run(500)
    right_leg_motor.run(500)
    wait(300)
    left_leg_motor.hold()
    right_leg_motor.hold()
    wait(300)
    left_leg_motor.run(-50)
    right_leg_motor.run(-50)
    wait(300)
    left_leg_motor.stop()
    right_leg_motor.stop()
    ev3.screen.load_image(ImageFile.NEUTRAL)

def stand_up():
    # Makes the puppy stand up.
    left_leg_motor.run_target(100, 25, wait=False)
    right_leg_motor.run_target(100, 25)
    while not left_leg_motor.control.done():
        wait(100)

    left_leg_motor.run_target(50, 65, wait=False)
    right_leg_motor.run_target(50, 65)
    while not left_leg_motor.control.done():
        wait(100)

def sit_down():
    # Makes the puppy sit down.
    left_leg_motor.run(-50)
    right_leg_motor.run(-50)
    wait(1000)
    left_leg_motor.stop()
    right_leg_motor.stop()
    wait(600)

def movement(speaker, move_count):
    move = move_count % 3
    if move == 0:
        ev3.speaker.say("I am pretending to be a bunny!")
        hop()
        hop()
    elif move == 1:
        stand_up()
        ev3.speaker.say("I am standing!")
        sit_down()
        ev3.speaker.say("I am sitting!")
    else:
        move_head()

def prompt(speaker, prompt_count):
    num = prompt_count % 5
    if num == 0:
        speaker.say("Try touching one of my sensors")
    elif num == 1:
        speaker.say("Try pressing my the sensor on my tail!")
    elif num == 2:
        speaker.say("Do you want to try scratching my chin or feeding me?")
    elif num == 3:
        speaker.say("Press my the button on my tail for a robot fact")
    elif num == 5:
        speaker.say("You can find my sensors on my tail, on my back, and under my chin")
        wait(200)
        speaker.say("I also have a sensor on my side!")
        wait(200)
        speaker.say("Try finding sensor and touching the sensors!")

def directions(speaker):
    ev3.speaker.say("I have four sensors that you can try out")
    ev3.speaker.say("Look at the button on my tail")
    ev3.speaker.say("Press the center button again if you want more help")

def play_song(speaker, song_count):
    song = song_count % 6
    if song == 0:
        speaker.play_file('inf.wav')
    elif song == 1:
        speaker.play_file('monkeys.wav')
    elif song == 2:
        speaker.play_file('snow.wav')
    elif song == 3:
        speaker.play_file('ohno.wav')
    elif song == 4:
        speaker.play_file('dance.wav')
    elif song == 5:
        speaker.play_file('Spongebob.wav')
    
def display_face(screen, speaker, face_count):
    face = face_count % 4
    if face == 0:
        speaker.say("I'm going to sleep")
        screen.load_image(ImageFile.SLEEPING)
        speaker.play_file(SoundFile.SNORING)
        wait(500)
        screen.load_image(ImageFile.DOWN)
    elif face == 1:
        speaker.say("I'm mad!")
        screen.load_image(ImageFile.EVIL)
        speaker.play_file(SoundFile.DOG_BARK_2)
        wait(500)
        screen.load_image(ImageFile.DOWN)
    elif face == 2:
        speaker.play_file(SoundFile.BOING)
        screen.load_image(ImageFile.DIZZY)
        speaker.say("ouch")
        wait(500)
        screen.load_image(ImageFile.DOWN)
    else:
        speaker.say("I am a star")
        screen.load_image(ImageFile.WINKING)
        speaker.play_file(SoundFile.CHEERING)
        wait(500)
        screen.load_image(ImageFile.DOWN)



ev3.screen.load_image(ImageFile.SLEEPING)
wait(2000)
ev3.screen.load_image(ImageFile.TIRED_MIDDLE)
wait(500)
ev3.screen.load_image(ImageFile.DOWN)
intro(ev3.speaker)
robot_fact_count = 0
move_count = 0
song_count = 0
prompt_count = 0
face_count = 0
starting_light = color_sensor.reflection()
while True:
    rand_prompt = random.randint(1,10)
    if tail_touch_sensor.pressed():
        ev3.screen.load_image(ImageFile.NEUTRAL)
        wait(500)
        ev3.screen.load_image(ImageFile.DOWN)
        
        robot_fact(ev3.speaker, robot_fact_count)
        robot_fact_count +=1
    elif pet_touch_sensor.pressed():
        ev3.screen.load_image(ImageFile.NEUTRAL)
        wait(500)
        ev3.screen.load_image(ImageFile.DOWN)

        movement(ev3.speaker, move_count)
        move_count += 1
    elif distance_sensor.distance() < 200:
        ev3.screen.load_image(ImageFile.NEUTRAL)
        wait(500)
        ev3.screen.load_image(ImageFile.DOWN)

        play_song(ev3.speaker, song_count)
        song_count +=1
    elif abs(starting_light - color_sensor.reflection()) > 15:
        ev3.screen.load_image(ImageFile.NEUTRAL)
        wait(500)
        ev3.screen.load_image(ImageFile.DOWN)

        display_face(ev3.screen, ev3.speaker, face_count)
        face_count += 1
    elif (ev3.buttons.pressed() == Button.CENTER):
        ev3.screen.load_image(ImageFile.NEUTRAL)
        wait(500)
        ev3.screen.load_image(ImageFile.DOWN)
        
        directions()
    elif (ev3.buttons.pressed() == Button.UP) | (ev3.buttons.pressed() == Button.DOWN)  \
       | (ev3.buttons.pressed() == Button.LEFT) | (ev3.buttons.pressed() == Button.RIGHT):
        break
    elif rand_prompt < 3:
        prompt(ev3.speaker, prompt_count)
        prompt_count +=1
    wait(2000)

ev3.speaker("Thanks for spending time with me! Hope it was fun!")
wait(1000)
