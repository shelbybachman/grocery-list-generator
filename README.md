## grocery list generator

this repository contains code for **shelby's code in place 2021 final project**.  it is a python program which creates a nicely-formatted grocery list based on user input in the console.

you can view a demo of the grocery list generator [here]().

### dependencies

to use the generator yourself, you'll need:
- Python 3 installed
- the Python Imaging Library `Pillow` installed: `python -m pip install --upgrade Pillow`

### using the generator

to use the generator yourself, follow these steps:

- clone the repo: `git clone https://github.com/shelbybachman/grocery-list-generator.git`
- navigate into the directory: `cd grocery-list-generator`
- run the program: `python grocery_list.py`
- when prompted, enter items and quantities
    - use single nouns only (e.g. `banana` rather than `bananas`)
    - enter integer quantities only
- when done entering all your items, press `Enter`
- your grocery list will be saved in two ways:
    - as plain text in the console, which can be copied to list manager of your choice
    - as an image, in the subdirectory `lists/`

### customization

the grocery list generator has a number of customization options:

- list of foods in grocery database
- image font family
- image background color