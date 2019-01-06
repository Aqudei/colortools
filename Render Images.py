# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.6.1
# Renders all models with a chosen extension to images.
import os, re

def cleanExt(ext):
    while ext.startswith("."):
        ext = ext[1:]
    return ext

def main():
    tmpls = ["-- None --"] + lux.getMaterialTemplates()
    info = lux.getSceneInfo()
    values = [("folder", lux.DIALOG_FOLDER, "Folder to import from:", None),
              ("iext", lux.DIALOG_TEXT, "Input file format to read:", "bip"),
              ("oext", lux.DIALOG_TEXT, "Output image format:", "png"),
              ("width", lux.DIALOG_INTEGER, "Output width:", info["width"]),
              ("height", lux.DIALOG_INTEGER, "Output height:", info["height"]),
              (lux.DIALOG_LABEL, "--"),
              ("template", lux.DIALOG_ITEM, "Apply material template on each import (optional):",
               tmpls[0], tmpls),
              (lux.DIALOG_LABEL, "--"),
              ("queue", lux.DIALOG_CHECK, "Add to queue", True),
              ("process", lux.DIALOG_CHECK, "Process queue after running script", False)]
    opts = lux.getInputDialog(title = "Render Images",
                              desc = "Rendes all models with a chosen input extension to images of chosen output extension.",
                              values = values,
                              id = "renderimages.py.luxion")
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]

    if len(opts["iext"]) == 0:
        raise Exception("Input extension cannot be empty!")
    iext = cleanExt(opts["iext"])
    reFiles = re.compile(".*{}".format(iext))
    found = False
    for f in os.listdir(fld):
        if reFiles.match(f):
            found = True
            break
    if not found:
        raise Exception("Could not find any input files matching the extension \"{}\" in \"{}\"!"
                        .format(iext, fld))

    if len(opts["oext"]) == 0:
        raise Exception("Output extension cannot be empty!")
    oext = cleanExt(opts["oext"])

    width = opts["width"]
    height = opts["height"]
    template = opts["template"]
    queue = opts["queue"]
    process = opts["process"]

    # Only set template if one was chosen.
    if template[0] == 0:
        template = None
    else:
        template = template[1]

    opts = lux.getRenderOptions()
    opts.setAddToQueue(queue)

    for f in [f for f in os.listdir(fld) if f.endswith(iext)]:
        path = fld + os.path.sep + f
        lux.newScene()

        print("Importing {}".format(path))
        lux.importFile(path)

        if template:
            print("Setting material template {}".format(template))
            lux.setMaterialTemplate(template)

        path = path + "." + oext
        print("Rendering {}".format(path))
        lux.renderImage(path = path, width = width, height = height, opts = opts)

    if process:
        print("Processing queue")
        lux.processQueue()

main()
