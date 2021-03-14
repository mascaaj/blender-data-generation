"""
File to manipulate cad alphabets and generate training data
"""
import time
import math
import random
from mathutils import Euler, Color
from pathlib import Path
import bpy
# Functions to rotate the object & change color

def randomly_rotate_object(object_to_rotate):
    """
    Takes in object and rotates it randomly about its origin
    """
    random_rotation = [random_angle(),random_angle(),random_angle()]
    object_to_rotate.rotation_euler = Euler(random_rotation, 'XYZ')

def random_angle():
    """
    Returns random angle between 0 -> 360 in radians
    """
    return random.random()*2*math.pi

def randomly_change_color(material_to_change):
    """ 
    Takes in object and changes its color using hsv
    """
    color = Color()
    hue = random.random()
    color.hsv = (hue, 1,1)
    rgba = [color.r,color.g,color.b,1]
    material_to_change.node_tree.nodes["Principled BSDF"].inputs[0].default_value=rgba

# Identify objects to generate images for
obj_names = ['A','B','C']
obj_count = len(obj_names)

# Tuple to hold quantities of train test and val datasets
obj_renders_per_split = [('train',3),('val',2),('test',1)]

# Set output path
output_path = Path('/dev_ssd/blender/blender-data-generation/data/alphabet_data')

# Use inline python function, get total number of renders
total_render_count = sum([obj_count * r[1] for r in obj_renders_per_split])

#set render for all objects to false
for name in obj_names:
    bpy.context.scene.objects[name].hide_render = True

start_idx = 0

start_time = time.time()

for split_name, renders_per_object in obj_renders_per_split:
    print(f'Starting split : {split_name} | Total Renders : {renders_per_object * obj_count}')
    print('========================')
    
    for obj_name in obj_names:
        print(f'Starting object : {split_name}/{obj_name}')
        print('................................')
        
        # Get object and make visible to render
        obj_to_render = bpy.context.scene.objects[obj_name]
        obj_to_render.hide_render = False
        
        for i in range(start_idx, start_idx+renders_per_object):
            randomly_rotate_object(obj_to_render)
            randomly_change_color(obj_to_render.material_slots[0].material)
            
            print(f'Rendering image {i+1} of {total_render_count}')
            seconds_for_render = (time.time() - start_time)/(i+1)
            seconds_remaining = ((total_render_count-i-1)*seconds_for_render)
            print(f'Estimated time remaining : {time.strftime("%H:%M:%S", time.gmtime(seconds_remaining))}')
            
            bpy.context.scene.render.filepath= str(output_path / split_name / obj_name / f'{str(i).zfill(6)}.png')
            bpy.ops.render.render(write_still=True)
            
        obj_to_render.hide_render = True

#        Increment the start image index    
        start_idx += renders_per_object

for name in obj_names:
    bpy.context.scene.objects[name].hide_render = False