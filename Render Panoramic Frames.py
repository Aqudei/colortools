# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.4.0
# Renders frames similar to a panoramic VR.
import os
from math import cos, sin, pi

def rotateY(vec, angle, clockwise):
    if clockwise: angle *= -1
    return (vec[0] * cos(angle) + vec[2] * sin(angle),
            vec[1],
            -vec[0] * sin(angle) + vec[2] * cos(angle))

def main():
    info = lux.getSceneInfo()
    values = [("cam", lux.DIALOG_ITEM, "Camera to use:", lux.getCamera(),
               lux.getCameras()),
              ("frames", lux.DIALOG_INTEGER, "#Frames:", 6, (1, 360)),
              ("fmt", lux.DIALOG_TEXT, "Output file format:", "frame.%d.png"),
              ("folder", lux.DIALOG_FOLDER, "Output folder:", None),
              ("width", lux.DIALOG_INTEGER, "Output width:", info["width"]),
              ("height", lux.DIALOG_INTEGER, "Output height:", info["height"]),
              (lux.DIALOG_LABEL, "--"),
              ("queue", lux.DIALOG_CHECK, "Add to queue", True),
              ("process", lux.DIALOG_CHECK, "Process queue after running script", False),
              ("clockwise", lux.DIALOG_CHECK, "Rotate clockwise", True)]
    opts = lux.getInputDialog(title = "Render Panoramic Frames",
                              desc = "Renders frames similar to a panoramic VR. This script assumes the camera is already positioned correctly.",
                              values = values,
                              id = "renderpanframes.py.luxion")
    if not opts: return

    cam = opts["cam"][1]
    frames = opts["frames"]

    fmt = opts["fmt"]
    if len(fmt) == 0:
        raise Exception("Output format cannot be empty!")
    if fmt.find("%d") == -1:
        raise Exception("Output format must contain '%d'!")

    folder = opts["folder"]
    if len(folder) == 0:
        raise Exception("Folder cannot be empty!")

    width = opts["width"]
    height = opts["height"]
    clockwise = opts["clockwise"]
    queue = opts["queue"]
    process = opts["process"]

    oldcam = lux.getCamera()
    angle = (360 / frames) * pi / 180 # radians

    cancelled = False
    lux.setCamera(cam)
    for i in range(frames):
        # Rotate around Y-axis by angle.
        lux.setCameraDirection(rotateY(lux.getCameraDirection(), angle, clockwise))
        lux.setCameraUp(rotateY(lux.getCameraUp(), angle, clockwise))

        path = os.path.join(folder, fmt.replace("%d", str(i)))
        print("Rendering {} of {} frames: {}".format(i+1, frames, path))
        opts = lux.getRenderOptions()
        opts.setAddToQueue(queue)
        if not lux.renderImage(path = path, width = width, height = height, opts = opts):
            print("Cancelled script!")
            cancelled = True
            break

    # Reset to old camera.
    lux.setCamera(oldcam)

    if process and not cancelled:
        print("Processing queue")
        lux.processQueue()

main()
