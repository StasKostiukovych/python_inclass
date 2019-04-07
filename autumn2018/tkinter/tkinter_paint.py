from tkinter import *
from tkinter.colorchooser import askcolor


class Paint:

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.line_button = Button(self.root, text="line", command=self.use_line)
        self.line_button.grid(row=0, column=1)

        self.square_button = Button(self.root, text="square", command=self.use_square)
        self.square_button.grid(row=0, column=2)

        self.oval_button = Button(self.root, text="oval", command=self.use_oval)
        self.oval_button.grid(row=0, column=3)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=4)

        self.color_bg_button = Button(self.root, text='fill', command=self.choose_color_bg)
        self.color_bg_button.grid(row=0, column=5)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=6)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=6)

        #self.save = Button(self.root, text="save", command=self.save)
        #self.save.grid(row=0,column=7)

        self.c = Canvas(self.root, bg='white', width=900, height=900)
        self.c.grid(row=1, columnspan=7)

        self.color_bg = None
        self.setup()
        self.root.mainloop()


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<ButtonPress-1>', self.onStart)
        self.c.bind('<Double-1>', self.clear)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.draw = None

    def onStart(self, event):
        self.start = event
        self.draw = None

    def use_pen(self):
        self.activate_button(self.pen_button)
        self.c.bind('<B1-Motion>', self.paint)

    def use_line(self):
        self.activate_button(self.line_button)
        self.c.bind('<B1-Motion>', self.paint_line)

    def use_square(self):
        self.activate_button(self.square_button)
        self.c.bind('<B1-Motion>', self.paint_square)

    def use_oval(self):
        self.activate_button(self.oval_button)
        self.c.bind('<B1-Motion>', self.paint_oval)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def choose_color_bg(self):
        self.color_bg = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def paint_line(self, event):

        self.c = event.widget
        self.line_width = self.choose_size_button.get()

        if self.draw:
            self.c.delete(self.draw)
        objectId = self.c.create_line(self.start.x, self.start.y, event.x, event.y,
                               width=self.line_width, fill=self.color)

        self.draw = objectId

    def paint_square(self, event):
        self.c = event.widget
        self.line_width = self.choose_size_button.get()
        if self.draw:
            self.c.delete(self.draw)
        objectId = self.c.create_rectangle(self.start.x, self.start.y, event.x, event.y,
                               width=self.line_width, outline=self.color, fill=self.color_bg)
        self.draw = objectId

    def paint_oval(self, event):
        self.c = event.widget
        self.line_width = self.choose_size_button.get()
        if self.draw:

            self.c.delete(self.draw)
        objectId = self.c.create_oval(self.start.x, self.start.y, event.x, event.y,
                               width=self.line_width, outline=self.color, fill=self.color_bg)
        self.draw = objectId

    def clear(self, event):
        event.widget.delete('all')

    def save(self):
        ps = self.c.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save('/tmp/test.jpg')

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()