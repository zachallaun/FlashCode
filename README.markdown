# FlashCode
### Interactive Python Tutorial

#### About
This was created as a small academic project. Please do not expect any particular level of quality in this code. I am aware of a plethora of shortcomings and weak points, but anyone should feel free to point out shitty code if they feel compelled.

#### Usage
    $ python3.2 run.py
    =======================================================================
    Welcome to FlashCode (FC), the interactive Python learning environment.
    =======================================================================

    Please choose your module by inputting the number below.

    (1) Beginnings
    (2) Variables

    Module number (or 'q' to quit): 1
    ===============
    (1) Beginnings
    ===============

    (FC) ">>>" is your Python prompt. This means the Python interpreter is
    ready to accept code. Try typing your name surrounded by quotes,
    like "Zach".

    (1)>>> "Zach"
    'Zach'

    (FC) See that? Python returned your name to you. What you created was
    a string, which is a series of characters surrounded by single or
    double quotes. Your name has a length, too. Try passing your name to
    the function len(), as in len("name").

    (2)>>> len("Zach")
    4

#### Extensibility
Modules live in `data/`, and are declared in `data/manifest.txt`. Format your manifest module declarations as seen in the file. Manifest supports full-line comments with `#`. You can surround
code with `||` for added formatting, as in "Try entering ||len(myName)||".

Format modules as seen in `data/begtut.txt`. Regular expressions used for input and output validation. Currently, the validation hook will only run on some kind of output. (This is why the variables module requires declared variables to be printed.)