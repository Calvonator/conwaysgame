from matplotlib import pyplot, animation
import numpy

#First step is to setup the figure, axis and plot element we want to animate
fig = pyplot.figure()
axis = pyplot.axes(xlim = (0, 100), ylim = (-50, 50))
line, = axis.plot([],[], lw = 2)


#initialisation program to plot the background for each frame
#Use this function to somehow ask the user to enter in the cells they want to be active.
def init():
    line.set_data([],[])
    return line,


def animate(i):
    x = numpy.linspace(0, 2, 1000)
    y = numpy.sin(2 * numpy.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,


#Call the animator. blit = True means ony re-draw parts that have changed.

anim = animation.FuncAnimation(fig, animate, init_func = init, frames = 200, interval = 20, blit = True)

anim.save("First_anim.avi", fps = 30, extra_args=['-vcodec', 'libx264']) #

pyplot.show()
