#!/usr/bin/env python

"""
Thumbnail Generator
This script in intended to be executed by GIMP as a plug-in to generate an image to be used as thumbnail.
Feel free to edit it to fit your needs.
Author: Yuri Delgado (yuridelgado.dev)
"""
from gimpfu import *
import os
import utils as my
    
def thumb_generator(background_path, picture_path, first_line, second_line, third_line, font_face, color=(0.0, 0.0, 0.0)):
    
    pdb.gimp_context_set_foreground(color)

    # Create an show new image window with background
    img = my.load_file(background_path)
    gimp.displays_flush()
    gimp.context_push()
        
    # Add overlay
    overlay = my.create_layer(image=img, width=img.width, height=img.height, image_type=RGB_IMAGE, 
                           name='overlay', opacity=35, mode=NORMAL_MODE, add_to_img=False)
    overlay.fill(FILL_WHITE)
    my.add_layer(img, overlay)
    
    # Add bottom rectangle
    bottom_rect_h = int(round(img.height * .09))
    bottom_rect_layer = my.create_layer(image=img, width=img.width, height=bottom_rect_h, image_type=RGB_IMAGE, 
                                     name='bottom_rect', opacity=100, mode=NORMAL_MODE)
    pdb.gimp_drawable_edit_fill(bottom_rect_layer,FILL_FOREGROUND)
    my.translate_layer(bottom_rect_layer, 0, img.height - bottom_rect_h)
    
    # Load popping out
    if (picture_path):
        picture_layer = my.load_image(img, picture_path)
        picture_w = int(round(img.width) * .47)
        my.scale_layer(picture_layer, picture_w, keep_proportion=True)
        my.translate_layer(picture_layer, img.width - picture_w, img.height - picture_layer.height)
        pdb.script_fu_drop_shadow(img, picture_layer, -4, -4, 20, '#000000', 90, FALSE)
        
    # Create the text lines
    font_size_big = img.height * .24
    font_size_ordinary = img.height * .12
    margin_top = img.height / 7
    margin_left = img.width / 25
    
    first_line_layer = my.add_text(image=img, x=margin_left, y=margin_top, content=first_line, 
                                font_size=font_size_big, font_face=font_face)
    
    second_line_layer = my.add_text(image=img, x=margin_left, y=margin_top + font_size_big, 
                                 content=' ' + second_line + ' ',  font_size=font_size_ordinary, font_face=font_face)
    my.set_layer_text_color(second_line_layer, '#FFF')
    pdb.gimp_selection_all(img)
    pdb.gimp_edit_bucket_fill(second_line_layer, BUCKET_FILL_FG, LAYER_MODE_BEHIND, 100, 0, False, 0, 0)
    
    tl_top = margin_top + font_size_big + font_size_ordinary
    third_line_layer = my.add_text(image=img, x=margin_left, y=tl_top, content=third_line, 
                                font_size=font_size_ordinary, font_face=font_face)
    
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
        (PF_STRING, 'background_path', '* Background path', ''),
        (PF_STRING, 'picture_path', 'Picture path', ''),
        (PF_STRING, 'first_line', 'First line (short)', ''),
        (PF_STRING, 'second_line', 'Second line', ''),
        (PF_STRING, 'third_line', 'Third line', ''),
        (PF_FONT, 'font_face', '* Font face', 'Londrina Solid Heavy'),
        (PF_COLOR, "color", "Color", (0.0, 0.0, 0.0))
    ],
    [],
    thumb_generator, menu="<Image>/File")

main()