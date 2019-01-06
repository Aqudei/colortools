# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.3.0
# Encodes video from separate frame range.
import os, re

def main():
    values = [("folder", lux.DIALOG_FOLDER, "Folder with frames:", None),
              ("fmt", lux.DIALOG_TEXT, "Frame file format:", "frame.%d.jpg"),
              ("start", lux.DIALOG_INTEGER, "Start frame:", 1, (1, 4096)),
              ("end", lux.DIALOG_INTEGER, "End frame:", 10, (1, 4096)),
              ("fps", lux.DIALOG_INTEGER, "FPS:", 10, (1, 1024)),
              ("name", lux.DIALOG_TEXT, "Video name:", "video.mp4")]
    opts = lux.getInputDialog(title = "Encode Video",
                              desc = "Encode video from separate frames of a specified range.",
                              values = values,
                              id = "encodevideo.py.luxion")
    if not opts: return

    if len(opts["folder"]) == 0:
        raise Exception("Folder cannot be empty!")
    fld = opts["folder"]

    files = opts["fmt"]
    if len(files) == 0:
        raise Exception("Frame format cannot be empty!")
    if files.find("%d") == -1:
        raise Exception("Frame format must contain '%d'!")
    reDigits = re.compile(files.replace("%d", "\d+"))
    found = False
    for f in os.listdir(fld):
        if reDigits.match(f):
            found = True
            break
    if not found:
        raise Exception("Could not find any frames matching the frame format \"{}\" in \"{}\"!"
                        .format(files, fld))

    start = opts["start"]
    end = opts["end"]
    if start > end:
        raise Exception("Start frame cannot be larger than end frame!")

    fps = opts["fps"]

    if len(opts["name"]) == 0:
        raise Exception("Video name cannot be empty!")
    name = opts["name"]

    path = os.path.join(fld, name)
    print("Encoding video {}".format(path))
    res = lux.encodeVideo(folder = fld, frameFiles = files, videoName = name,
                          fps = fps, firstFrame = start, lastFrame = end)
    if not res: raise Exception("Failed to encode video!")

main()
