import pygmsh

def main(radius, height):
    with pygmsh.occ.Geometry() as geom:
        geom.add_cylinder(x0=[0.0, 0.0, 0.0], axis=[0.0, 0.0, height], radius=radius)
        mesh = geom.generate_mesh()

    return mesh

if __name__ == '__main__':
    mesh = main(radius=0.5, height=1.0)
    mesh.write('cylinder.stl')
