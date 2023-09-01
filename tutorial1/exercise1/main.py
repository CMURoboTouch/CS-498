import mitsuba as mi
mi.set_variant("scalar_rgb")
# load scene
scene = mi.load_file("cbox/cbox.xml")
# calculate image
image = mi.render(scene, spp=256)
# write image to computer
mi.util.write_bitmap("cbox.png", image)