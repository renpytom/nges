# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


label main_menu:
    return


screen nges_example():
    default d = nges.NGES("game.nes")
    add d at transform:
        zoom 2
        nearest True
        align (0.5, 0.1)

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."


    call screen nges_example()


    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
