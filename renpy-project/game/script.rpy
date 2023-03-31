# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

define config.allow_skipping = False

screen nges_example():
    default d = nges.NGES("game.nes")
    add d at transform:
        zoom 2
        nearest True
        align (0.5, 0.1)

    frame:
        xalign 1.0
        xoffset -30
        yalign 0.1
        padding (40, 20)

        vbox:

            text "Controls"
            null height 10

            text "Arrow Keys: Move"
            text "Z: Button A"
            text "X: Button B"
            text "Enter: Start"
            text "Right Shift: Select"

            null height 25

            textbutton "Done" action [ With(dissolve), Return(True) ]


# The game starts here.

label start:

    play music magic_escape_room

    scene bg arcade
    show eileen happy

    e "Hello, everyone, and welcome to the big announcement!"

    e "Today, I'm announcing the Next-Generation Enhancement System, which we're calling NGES for short."

    e "Ren'Py is great at making visual novels, but sometimes you want some minigames in your game."

    e "The tutorial has an example of writing minigames in Python - but that's not the only way to do it. At least, not anymore."

    e "The next-generation enhancement system is a virtual machine that lets you run some of the most popular minigames ever created."

    e "This virtual machine uses an 8-bit bytecode that gives access to memory-mapped registers that can display tiles, sprites, and synthesize audio."

    e "It even allows sections of the address space to be replaced, so you can run larger games."

    e "The NGES is a work in progress, but I'm excited to show you what it can do. Here goes..."

    stop music fadeout 0.5
    show eileen at left
    with move

    call screen nges_example() with dissolve
    pause .5

    play music magic_escape_room

    show eileen at center
    with move

    show eileen vhappy

    e "... and now that you've seen that, I invite you to reflect on what day this came out."

    show eileen happy

    "NGES is really the ANESE emulator, by Daniel Prilik, slimmed down and plugged into Ren'Py."

    "The background image is by Arcade Perfect, from Wikimedia Commons. The music is by Kevin MacLeod, from Incompetech."

    "Thanks for putting up with this!"

    return
