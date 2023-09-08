import mitsuba as mi
mi.set_variant("scalar_rgb")
# load scene
scene = mi.load_file("cbox/cbox_translatedx0.5.xml")
# calculate image
image = mi.render(scene)
# write image to computer
mi.util.write_bitmap("cbox.png", image)