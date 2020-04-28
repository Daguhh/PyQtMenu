from numpy import *
from numpy import matlib
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib
from PIL import Image, ImageTk
from scipy import misc
from scipy.interpolate import interp2d
import skimage.transform
#from colormap import Colormap
import numpy as np
#plt.ion()

def get_background(size=(100,1000)):

    size_x=size[0]
    size_y=size[1]
    size_turb_x=size[0]
    size_turb_y=size[1]
    lambdax = 8
    lambday = 200
    xpower = 20
    ypower = 100

    a=0
    l=0

    fig=plt.figure()

    while l<2 :
        mat0=random.rand(size_turb_x,size_turb_x)
        x0=arange(size_turb_x)
        y0=arange(size_turb_x)
        grids=[]
        pts=vstack((x0,y0))

        for j in arange(1,7,1) :
            i=2**j
            x1=arange(0,size_turb_x,i)
            y1=arange(0,size_turb_x,i)
            f = interp2d(x0, y0, mat0)
            grid_z1=f(x1,y1)
            grids.append(grid_z1)
        per=1
        perlin_mat=empty((size_turb_x,size_turb_x))

        for mat in grids :
            mat=skimage.transform.resize(mat,(size_turb_x,size_turb_x))
            per=per/0.7
            perlin_mat = perlin_mat + mat*per
        perlin_mat=perlin_mat/amax(perlin_mat)
        perlin_cut=perlin_mat.copy()
        l=l+1
        perlin_cut=skimage.transform.resize(perlin_cut,(size_y,size_x))
        perlin_cut=perlin_cut/amax(perlin_cut)

        if a == 0 :
            turb_x0=perlin_cut
            a=1
        else :
            turb_y0=perlin_cut

    x0=arange(size_x)
    y0=arange(size_y)
    X,Y=meshgrid(x0,y0)
    mat0=sin(((X+turb_x0*xpower)/lambdax)*2*pi)
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["saddlebrown","maroon"])

    im_plt = plt.imshow(mat0,cmap=cmap)
    image = Image.fromarray(np.uint8( im_plt.get_cmap()(im_plt.get_array())*255))
    im = ImageTk.PhotoImage('RGB', image.size)
    im.paste(image)

#    plt.close(fig)
    return im


if __name__ == '__main__':

    root=Tk()
    canvas = Canvas(root)
    canvas.pack(expand = YES, fill = BOTH)

    im_plt = get_background()
    image = Image.fromarray(np.uint8( im_plt.get_cmap()(im_plt.get_array())*255))
    im = ImageTk.PhotoImage('RGB', image.size)
    im.paste(image)

    test = canvas.create_image(0, 0, image=im)
    mainloop()

