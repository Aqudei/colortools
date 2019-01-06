# -*- coding: utf-8 -*-
# AUTHOR Luxion
# VERSION 0.1.2
# Duplicates and randomly scatters an object.
import os
from random import uniform, randint, choice

def randbool():
    return randint(0, 1) == 1

def randaxis():
    return luxmath.Vector(choice([(1, 0, 0), (0, 1, 0), (0, 0, 1)]))

def main():
    # Find objects to choose from.
    objTxt = []
    objRef = []
    root = lux.getSceneTree()
    for n in root.find("", types = (lux.NODE_TYPE_GROUP, lux.NODE_TYPE_OBJECT),
                       depth = 3):
        if n != root:
            objTxt.append("{} ({})".format(str(n.getPath(text = True)[1:]),
                                           n.getMaterial()))
            objRef.append(n)

    if len(objTxt) == 0:
        raise Exception("No objects in the scene!")

    values = [("object", lux.DIALOG_ITEM, "Object:", objTxt[0], objTxt),
              ("dups", lux.DIALOG_INTEGER, "#Duplicates:", 4, (1, 4096)),
              ("tx", lux.DIALOG_CHECK, "Translate by X axis", True),
              ("ty", lux.DIALOG_CHECK, "Translate by Y axis", True),
              ("tz", lux.DIALOG_CHECK, "Translate by Z axis", True),
              ("rot", lux.DIALOG_CHECK, "Rotate", True)]
    opts = lux.getInputDialog(title = "Random Scattering",
                              desc = "Duplicates and randomly scatters an object.",
                              values = values,
                              id = "randomscattering.py.luxion")
    if not opts: return

    obj = objRef[opts["object"][0]]
    amount = opts["dups"]
    tx = opts["tx"]
    ty = opts["ty"]
    tz = opts["tz"]
    rot = opts["rot"]

    dups = obj.duplicate(amount = amount)
    if len(dups) == 0:
        raise Exception("No duplicates could be created!")

    # Randomly scatter the duplicates.
    gbbMin, gbbMax = root.getBoundingBox(world = True)
    for dup in dups:
        bbMin, bbMax = dup.getBoundingBox(world = True)

        cx = 0
        if tx:
            cx = (bbMax.x - bbMin.x) / 2
            if randbool():
                cx = uniform(gbbMin.x, cx) - cx
            else:
                cx = uniform(cx, gbbMax.x) - cx

        cy = 0
        if ty:
            cy = (bbMax.y - bbMin.y) / 2
            if randbool():
                cy = uniform(gbbMin.y, cy) - cy
            else:
                cy = uniform(cy, gbbMax.y) - cy

        cz = 0
        if tz:
            cz = (bbMax.z - bbMin.z) / 2
            if randbool():
                cz = uniform(gbbMin.z, cz) - cz
            else:
                cz = uniform(cz, gbbMax.z) - cz

        mat = luxmath.Matrix().makeIdentity().translate(luxmath.Vector((cx, cy, cz)))
        if rot:
            mat = mat.rotateAroundAxis(randaxis(), uniform(0, 360))
        dup.applyTransform(mat)

main()
