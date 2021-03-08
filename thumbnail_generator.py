#!/usr/bin/env python

# https://stackoverflow.com/questions/12662676/writing-a-gimp-python-script
# https://www.gimp.org/docs/python/index.html#INTRODUCTION
# https://tanyaschlusser.github.io/slides/Python-Fu-in-GIMP.slides.html
# <span>Photo by <a href="https://unsplash.com/@baileyzindel?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Bailey Zindel</a> on <a href="https://unsplash.com/s/photos/landscape?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>
# <span>Photo by <a href="https://unsplash.com/@sharonmccutcheon?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Sharon McCutcheon</a> on <a href="https://unsplash.com/s/photos/money?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>
from gimpfu import *
import os

def log(msg):
    pdb.gimp_message(msg)

def thumb_generator(background_path, picture_path, first_line, second_line, third_line, font_face) :

    # Create an show new image window with background
    img = pdb.gimp_file_load(background_path, background_path)
    gimp.Display(img)
    gimp.displays_flush()
    gimp.context_push()
    
    img.undo_group_start()
    
    # Add overlay
    overlay = gimp.Layer(img, 'overlay', img.width, img.height, RGB_IMAGE, 35, NORMAL_MODE)
    overlay.fill(FILL_WHITE)
    img.add_layer(overlay, 0)
    
    # Add bottom rectangle
    bottom_rect_h = int(round(img.height * .09))
    bottom_rect_layer = gimp.Layer(img, 'bottom_rect', img.width, bottom_rect_h, RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, bottom_rect_layer, None, -1)
    bottom_rect_layer.translate(0, img.height - bottom_rect_h)
    
    # Load guy
    if (picture_path):
        picture_layer = pdb.gimp_file_load_layer(img, picture_path)
        img.add_layer(picture_layer, 0)
        picture_w = int(round(img.width) * .47)
        picture_h = int(round(float(picture_layer.height) * (float(picture_w) / float(picture_layer.width))))
        pdb.gimp_layer_scale(picture_layer, picture_w, picture_h, False) # false to keep the same coord
        picture_layer.translate(img.width - picture_w, img.height - picture_h)
        pdb.script_fu_drop_shadow(img, picture_layer, -4, -4, 20, "#000000", 90, FALSE)
        
    # Create the text lines
    font_size_big = img.height * .24
    font_size_ordinary = img.height * .12
    margin_top = img.height / 7
    margin_left = img.width / 25
    
    first_line_layer = pdb.gimp_text_fontname(img, None, margin_left, margin_top, first_line, 0, True, font_size_big, PIXELS, font_face)
    
    second_line_layer = pdb.gimp_text_fontname(img, None, margin_left, margin_top + font_size_big, ' ' + second_line + ' ', 0, True, font_size_ordinary, PIXELS, font_face)
    pdb.gimp_text_layer_set_color(second_line_layer, '#FFF')
    pdb.gimp_selection_all(img)
    pdb.gimp_edit_bucket_fill(second_line_layer, BUCKET_FILL_FG, LAYER_MODE_BEHIND, 100, 0, False, 0, 0)
    
    tl_top = margin_top + font_size_big + font_size_ordinary
    third_line_layer = pdb.gimp_text_fontname(img, None, margin_left, tl_top, third_line, 0, True, font_size_ordinary, PIXELS, font_face)
    
    img.undo_group_end()
    gimp.context_pop()

register(
    "python_fu_thumb_generator",
    "Thumb generator",
    "Create a thumbnail",
    "Yuri Delgado",
    "Yuri Delgado",
    "2021",
    "Thumbnail Generator",
    "",     
    [
        (PF_STRING, 'background_path', '* Background path', '/home/yuridelgado/Pictures/landscape.jpg'),
        (PF_STRING, 'picture_path', 'Picture path', '/home/yuridelgado/Pictures/travel-guy.png'),
        (PF_STRING, 'first_line', 'First line (short)', 'BEST'),
        (PF_STRING, 'second_line', 'Second line', 'LAKES TO VISIT'),
        (PF_STRING, 'third_line', 'Third line', 'IN SOUTH AMERICA'),
        (PF_FONT, 'font_face', '* Font face', 'Londrina Solid Heavy'),
    ],
    [],
    thumb_generator, menu="<Image>/File")

main()