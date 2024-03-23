import tkinter as tk
from tkinter import colorchooser
from tkinter import Button
from PIL import Image, ImageDraw
import cv2 as cv
import numpy as np

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("绘图应用")
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='white')
        self.canvas.pack()

        self.image = Image.new("RGB", (400, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.fill_grid= np.zeros((20,20),dtype=np.uint8)

        self.setup()
        self.bind_events()
        self.draw_grid(20, 20)  # 绘制20行20列的网格

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 2
        self.color = 'black'
        self.eraser_on = False
        self.active_button = Button(self.master, text='保存', command=self.save)
        self.active_button.pack(side=tk.LEFT)
        self.color_button = Button(self.master, text='颜色', command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        self.eraser_button = Button(self.master, text='橡皮擦', command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)

    def bind_events(self):
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            self.draw.line([self.old_x, self.old_y, event.x, event.y], fill=paint_color, width=self.line_width)

        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None
    
    def judge_inside(self,x, y):

        l=False 
        l_first=0
        r=False
        r_first=0
        u=False
        u_first=0
        d=False
        for i in range(x-1, -1, -1):
            if self.fill_grid[i,y]==1:
                l=True
                l_first=i
                break
        for i in range(x+1, 20):
            if self.fill_grid[i,y]==1:
                r=True
                r_first=i
                break
        for j in range(y-1, -1, -1):
            if self.fill_grid[x,j]==1:
                u=True
                u_first=j
                break
        for j in range(y+1, 20):
            if self.fill_grid[x,j]==1:
                d=True
                d_first=j
                break
        if l and r and u and d:
            for i in range(l_first, r_first):
                self.fill_grid[i,y]=1

            for j in range(u_first, d_first):
                self.fill_grid[x,j]=1

            return True
                
 

    def save(self):
        grid_size = 20
        new_size = (20, 20)  # 结果图像的尺寸
        result_image = Image.new("RGB", new_size, "white")
        fill_image = Image.new("RGB", new_size, "white")
        draw = ImageDraw.Draw(result_image)
        draw_filled = ImageDraw.Draw(fill_image)

        # Step 1: Mark cells with traces
        for i in range(0, 400, grid_size):
            for j in range(0, 400, grid_size):
                has_mark = False
                for x in range(i, min(i + grid_size, 400)):
                    for y in range(j, min(j + grid_size, 400)):
                        if self.image.getpixel((x, y)) != (255, 255, 255):
                            has_mark = True
                            break
                    if has_mark:
                        break
                if has_mark:
                    draw.rectangle([(i // grid_size, j // grid_size), ((i + grid_size) // grid_size - 1, (j + grid_size) // grid_size - 1)], fill="black")
                    self.fill_grid[i // grid_size, j // grid_size] = 1

        # Temporary save to check marked cells
        filename = "drawing.png"
        result_image.save(filename)
        print(f"图像已保存为: {filename}")


        self.fill_grid=self.fill_grid.T
        print(self.fill_grid)

        # Step 2: Reload the image and find a black pixel for flood fill
        for j in range(20):
            for i in range(20):
                self.judge_inside(i,j)

        print(self.fill_grid)
                    

        for i in range (20):
            for j in range (20):
                if self.fill_grid[i,j]==1:

                    draw_filled.point((j, i), fill="black")

        print(self.fill_grid)          

        
        # Save the final result
        filename1 = "filled.png"
        fill_image.save(filename1)
        print(f"图像已保存为: {filename1}")
                        
        


    def choose_color(self):
        self.eraser_on = False
        self.color = colorchooser.askcolor(color=self.color)[1]

    def use_eraser(self):
        self.eraser_on = True

    def draw_grid(self, rows, cols):
        grid_width, grid_height = 400 // cols, 400 // rows
        for i in range(rows + 1):
            self.canvas.create_line(0, i * grid_height, 400, i * grid_height, fill='black')
        for j in range(cols + 1):
            self.canvas.create_line(j * grid_width, 0, j * grid_width, 400, fill='black')


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
