import mitsuba as mi
mi.set_variant("scalar_rgb")
# load scene
scene = mi.load_file("cbox/cbox_final.xml")
# calculate image
image = mi.render(scene, spp=256)
# extract normals
if image.shape[2] < 6:
    raise Exception("Expected at least 6 channels in the image!")
normals = image[:,:,3:6]
# convert normals [-1,1] -> [0,1]
normals = (normals+1.0)/2.0
# write image to computer
mi.util.write_bitmap("normals.png", normals)