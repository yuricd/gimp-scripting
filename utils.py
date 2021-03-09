from gimpfu import *

def log(msg):
    pdb.gimp_message(msg)
    
def load_file(path):
    img = pdb.gimp_file_load(path, path)
    gimp.Display(img)
    return img
  
def add_layer(image, layer, parent=None, position=-1):
    pdb.gimp_image_insert_layer(image, layer, parent, position)

def load_image(image, path, add_to_img=True):
    layer = pdb.gimp_file_load_layer(image, path)
    if add_to_img:
        add_layer(image, layer)
    return layer

def create_layer(image, width, height, image_type, name, opacity, mode, add_to_img=True):
    layer = pdb.gimp_layer_new(image, width, height, image_type, name, opacity, mode)
    if add_to_img:
        add_layer(image, layer)
    return layer

def translate_layer(layer, x, y):
    pdb.gimp_item_transform_translate(layer, x, y)
    
def scale_layer(layer, new_width, new_height=None, keep_proportion=True):
    height = new_height
    if keep_proportion:
        height = int(round(float(layer.height) * (float(new_width) / float(layer.width))))
    return pdb.gimp_layer_scale(layer, new_width, height, False) # false to keep the same coord

def add_text(image, x, y, content, font_size, font_face, drawable=None):
    return pdb.gimp_text_fontname(image, drawable, x, y, content, 0, True, font_size, PIXELS, font_face)

def set_layer_text_color(layer, color):
    return pdb.gimp_text_layer_set_color(layer, color)