import maya.cmds as cmds
from vray.utils import *
import threading
import time
import os
import subprocess

RENDERING = True
ON = False
SCENE = ''
TIMESTAMP_START = 0

def get_scene_name():
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    rawname, ext = os.path.splitext(filename)
    return rawname


def save_image():
    global RENDERING
    global SCENE
    print(SCENE)
    current = 10000;
    while RENDERING:
        vrayFile = 'C:/Users/vr/Desktop/VRayRenderingPreview/images/render%s_'%current  +  SCENE + '.jpg' 
        cmds.vray('vfbControl', '-saveimage', vrayFile)
        subprocess.Popen(['python', 'C:/Users/vr/Desktop/VRayRenderingPreview/scripts/publishImage.py', vrayFile], shell=True)
        current += 1
        print('saving')
        time.sleep(1)

def pre_render():
    global SCENE
    global RENDERING
    
    SCENE = get_scene_name()
    RENDERING = True
    print('pre render')
    t = threading.Thread(target=save_image)
    t.start()

def post_render():
    global RENDERING
    RENDERING = False
    print('post render')
      
def stop_collecting():
    print("DONE")
    ON = False

