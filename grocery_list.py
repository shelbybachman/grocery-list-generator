"""
grocery_list.py
----------
shelby's final project for code in place 2021
this program takes user input about items to buy at the grocery store
and creates a formatted grocery list
"""

# remaining things to do:
# [] prompt user to add unknown item to database
# [] more decomposition of main() function
# [] warning if list expands beyond image boundaries
# [] make preferences more explicit in program


import os
import csv
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# image dimensions
# (set for iphone 6)
IMAGE_WIDTH = 750
IMAGE_HEIGHT = 1334

# files containing fonts
# (light font will be used for items)
# (bold font will be used for section headings)
FONTFILE_LIGHT = 'utils/Roboto-Light.ttf'
FONTFILE_BOLD = 'utils/Roboto-Bold.ttf'

# RGB values for image background color
BG_R = 187
BG_G = 242
BG_B = 224


def main():

    # welcome message
    print_welcome()

    # create the grocery dictionary from food data files
    csv_dir = 'data/'
    categories = get_grocery_categories(csv_dir)
    grocery_dict = create_grocery_dict(categories, csv_dir)

    # initialize user list as dictionary
    user_dict = initialize_user_dict(categories)

    # prompt user for items & quantities
    while True:

        # prompt user for item
        item = input('Enter the item to buy: ')

        # if blank entry received, break
        if item == '':
            print('-----------------------------')
            break

        # otherwise, find the item category
        item_category = find_key_for_item(item, grocery_dict)

        # if the category was not found, try again
        while True:
            if item_category is None:
                print('Entered item not found.')
                print('Did you enter a typo or plural? Try again!')
                item = input('Enter the item to buy: ')
                item_category = find_key_for_item(item, grocery_dict)
            else:
                break

        # prompt user for item quantity
        quantity = input('Enter the integer quantity of ' + item + ': ')

        # check validity of quantity input
        while True:
            if not check_quantity(quantity):
                print('Integer not detected. Try again!')
                quantity = input('Enter the integer quantity of ' + item + ': ')
            else:
                break

        # store item, category & quantity in dictionary
        user_dict = update_user_list(user_dict, item, item_category, quantity)
        print('-----------------------------')

    # final formatting of grocery list
    user_dict = format_grocery_list(user_dict)

    # print final grocery list
    print_grocery_list(user_dict)

    # save list as image
    create_grocery_list_image(user_dict, IMAGE_WIDTH, IMAGE_HEIGHT,
                              FONTFILE_LIGHT, FONTFILE_BOLD)


def print_welcome():
    """
    displays a brief welcome and a few reminders
    for the grocery list program
    """
    print('----------------------------------------')
    print('Welcome to the grocery list creator!')
    print('----------------------------------------')
    print('A few reminders:')
    print('- Use singular nouns only')
    print('- Enter items separately from quantities')
    print('----------------------------------------')


def get_grocery_categories(csv_dir):
    # create empty list
    categories = []

    # loop over .csv files & extract category names
    for s in os.listdir(csv_dir):
        categories.append(s.split('.')[0])

    # alphabetize category names
    categories.sort()

    # return the list
    return categories


def get_formatted_categories(csv_dir):
    # create empty list
    categories = []

    # loop over .csv files & extract category names
    for s in os.listdir(csv_dir):
        # (this time, replace any underscores with spaces)
        categories.append(s.split('.')[0].replace('_', ' '))

    # alphabetize category names
    categories.sort()

    # return the list
    return categories


def create_grocery_dict(categories, csv_dir):
    """
    read .csv files containing foods organized by category
    and create a single dictionary from the contents
    with keys corresponding to grocery categories
    """
    # initialize empty dictionary
    grocery_dict = {}

    # read files for each grocery category
    # and add items to dictionary
    for category in categories:

        # initialize key in dictionary & corresponding empty list
        grocery_dict[category] = []

        # build filename
        category_filename = csv_dir + category + '.csv'

        # read the file
        with open(category_filename, encoding='utf-8-sig') as f:

            # create reader object
            reader = csv.reader(f)

            # loop over lines & add to dictionary
            for line in reader:
                grocery_dict[category].append(line[0])

    # return grocery dictionary
    return grocery_dict


def initialize_user_dict(categories):
    """
    initialize empty dictionary
    with grocery categories as keys
    which will contain user's grocery items
    """
    # create empty dictionary
    user_dict = {}

    # loop over elements of list and add keys
    for i in categories:
        user_dict[i] = []

    # return dictionary
    return user_dict


def find_key_for_item(item, grocery_dict):
    """
    within the provided grocery dictionary,
    returns the key for which item is contained in value
    (if it exists)
    """
    for k, v in grocery_dict.items():
        if item in v or item == v:
            return k


def check_quantity(quantity):
    """
    determine whether inputted quantity can be converted to an integer
    """
    try:
        int(quantity)
    except ValueError:
        return False

    return True


def update_user_list(user_dict, item, item_category, quantity):
    """
    updates user dictionary containing grocery list
    with a specified item from a specified category & its desired quantity
    """

    # append dictionary entry for this category
    # with quantity + item as a string
    user_dict[item_category].append(item + ' x' + str(quantity))

    # make sure list for this key is in alphabetical order
    user_dict[item_category].sort()

    return user_dict


def format_grocery_list(user_dict):
    """
    final formatting of grocery list,
    specifically removal of keys with no values
    """
    # identify empty categories in dictionary
    empty_categories = []
    for k, v in user_dict.items():
        if not v:
            empty_categories.append(k)

    # remove them from the dictionary
    for cat in empty_categories:
        del user_dict[cat]

    # return the updated dictionary
    return user_dict


def print_grocery_list(user_dict):
    """
    print nicely formatted dictionary containing grocery list
    """

    print('')
    today = date.today()
    print('grocery list ' + today.strftime('%Y-%m-%d'))
    for category, list_items in user_dict.items():

        # print category name
        category_name = category.lower()
        category_name.replace('_', ' ')
        print('\n{}'.format(category_name))

        # print items in category
        for i in list_items:
            print('[] {}'.format(i))

    print('-----------------------------')


def create_grocery_list_image(user_dict, IMAGE_WIDTH, IMAGE_HEIGHT,
                              BG_R, BG_G, BG_B,
                              fontfile_light, fontfile_bold):
    """
    create an image showing grocery list as text
    """
    # create image object
    image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT),
                      (BG_R, BG_G, BG_B))

    # initialize drawing context
    draw = ImageDraw.Draw(image)

    # create font objects
    font_light = ImageFont.truetype(fontfile_light, size=28)
    font_bold = ImageFont.truetype(fontfile_bold, size=28)
    font_header = ImageFont.truetype(fontfile_bold, size=48)
    font_date = ImageFont.truetype(fontfile_light, size=28)

    # set font color
    color = 'rgb(0, 0, 0)'

    # draw header
    (x, y) = (50, 50)
    draw.text((x, y), 'grocery list', fill=color, font=font_header)

    # draw date
    today = date.today()
    (x, y) = (50, 120)
    draw.text((x, y), today.strftime('%Y-%m-%d'), fill=color, font=font_date)

    # set starting positions for drawing list text
    current_x = 50
    current_y = 120

    # loop over dictionary and draw list
    for k, v in user_dict.items():

        current_y += 70

        # figure out how much y-space is needed for this category
        y_needed = 32 + 32*len(v)
        if current_y + y_needed + 50 >= IMAGE_HEIGHT:
            current_x = (IMAGE_WIDTH / 2) + 50
            current_y = 190

        # draw category label
        (x, y) = (current_x, current_y)
        draw.text((x, y), k, fill=color, font=font_bold)

        # draw category items
        for i in v:
            current_y += 32
            (x, y) = (current_x, current_y)
            draw.text((x, y), i, fill=color, font=font_light)

    # save the image
    file_to_save = 'lists/grocery_list_' + today.strftime('%Y-%m-%d') + '.png'
    image.save(file_to_save)


if __name__ == '__main__':
    main()
