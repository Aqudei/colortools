# AUTHOR Francis
# VERSION 0.0.0
# Write description of the script here, and put your code after these lines.

import lux
import os
import re

model_id_regex =re.compile(r'^\d\d\-\d\d\d_.+')

# lux.setEnvironmentImage('E:\\dev\\upwork\\forkeyshot\\Sample Files\\APP MODELS\\KeyShot_Lightscape1.hdz')

def setEnvironmentImage(envImage):
    lux.setEnvironmentImage(envImage)

def winpath(path):
    return os.path.abspath(path)

def ensure_folder(folder, with_file=False):
    try:
        if with_file:
            head, tail  = os.path.split(folder)
            os.makedirs(head)
        else:
            os.makedirs(folder)
    except Exception as e:
        print(e)

app_folder = lux.getInputFolder(
    title='Select "APP MODELS" Folder Location',
    folder='E:\\dev\\upwork\\forkeyshot\\')

files = os.listdir(app_folder)
for f in files:
    if not model_id_regex.match(f):
        continue
    
    model_folder = winpath(os.path.join(app_folder,f)) 
    
    var_env_image = winpath(os.path.join(app_folder,'KeyShot_Lightscape1.hdz'))
    var_env_image_gloss = winpath( os.path.join(app_folder,'KeyShot_Lightscape_Gloss.hdz'))
    print(var_env_image)
    setEnvironmentImage(var_env_image)
    
    var_clay_bip = os.path.join(model_folder, 'KeyShot','Scenes')
    var_clay_bip = winpath(os.path.join(var_clay_bip, os.listdir(var_clay_bip)[0])) 
    lux.importFile(var_clay_bip)

    opts = lux.getRenderOptions()
    opts.setOutputAlphaChannel(enable=False)

    var_clay_render_location = os.path.join(model_folder,'Keyshot','Renders','Z_SOURCE')
    ensure_folder(var_clay_render_location)
    
    # Clay Render
    lux.renderFrames(
        folder=var_clay_render_location, 
        width=1200, 
        height=1322,
        frameFiles='Clay1.%d.png',
        fps = 15
    )

#     # print('Processing {}'.format(model_folder))
#     # var_clay_bip = os.path.join(model_folder, 'KeyShot','Scenes')
#     # var_clay_bip = winpath(os.path.join(var_clay_bip, os.listdir(var_clay_bip)[0])) 
#     # print('Clay bip: {}'.format(var_clay_bip))

#     # lux.importFile(var_clay_bip)
