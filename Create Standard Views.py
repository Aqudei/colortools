# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.1.2
# Creates a new camera for each of the 7 standard views. If the cameras exist
# already then they will be updated.

views = {lux.VIEW_FRONT: "Front",
         lux.VIEW_BACK: "Back",
         lux.VIEW_LEFT: "Left",
         lux.VIEW_RIGHT: "Right",
         lux.VIEW_TOP: "Top",
         lux.VIEW_BOTTOM: "Bottom",
         lux.VIEW_ISOMETRIC: "Isometric"}

for view in views:
    name = "View_" + views[view]
    has = False
    if name in lux.getCameras():
        has = True
        lux.setCamera(name)
    else:
        lux.newCamera(name)
    lux.setStandardView(view)
    lux.saveCamera()
    print("{} camera: {}".format("Updated" if has else "Created", name))
