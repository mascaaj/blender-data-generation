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
    pass

# Functions to loop through iterations

# Functions to output data

#Test Functions
randomly_rotate_object(bpy.context.scene.objects['B'])
randomly_change_color(bpy.data.materials["Letter Material"])