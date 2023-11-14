import cadquery as cq
from ocp_vscode import *

base_radius = 11
base_thickness = 3
base_chamfer = 0.5
peg_radius = 4
peg_length = 11
peg_split_width = 2
clip_width = 14
clip_depth = 3
clip_height = 3.5
slot_width = 15
slot_depth = 2
slot_height = 2

step_name = "./helmet_clip.step"
stl_name = "./helmet_clip.stl"

# Create initial clip
clip = (
    cq
        .Workplane()
        .circle(base_radius)
        .extrude(base_thickness)
        .chamfer(base_chamfer)
        .faces('>Z')
        .circle(peg_radius)
        .extrude(peg_length)
        .faces('>Z')
        .rect(clip_width,clip_depth)
        # this needs to be negative
        .extrude(0 - clip_height)
        .faces('>Z')
        .rect(peg_split_width,base_radius)
        .cutBlind(0 - peg_length)
        .faces('<Z')
        .rect(slot_width,slot_depth)
        .cutBlind(slot_height)
)

# Cut left hand triangle
clip = (
    clip
        .faces("<Y")
        .vertices(">Z and <X")
        .workplane(centerOption='CenterOfMass')
        .line(0,-1)
        .line(6,1)
        .close()
        .cutThruAll()
)

# Cut right hand triangle
clip = (
    clip
        .faces("<Y")
        .vertices(">Z and >X")
        .workplane(centerOption='CenterOfMass')
        .line(0,-1)
        .line(-6,1)
        .close()
        .cutThruAll()
)

# Export as a step and STL
cq.exporters.export(clip, step_name)
cq.exporters.export(clip, stl_name)

show(clip)