import pygame
import os
import random
import tkinter as tk
from tkinter import messagebox

# Global Variables
screen_width = 1600
screen_height = 1000
draw_width = 1200
draw_height = 1000
spacing = 20
little_spacing = 4
toolbox_size = 75
rec_thickness = 4
num_sizes = 4
num_colors = 4
box_width = 50
box_height = 50
size_mul = 2
folder_name = "saveimg/"
text_font = "Bold"
text_scale = 60
# Dynamic Variables
draw = False
cur_thickness = 0
cur_color = 0
# Colors
white = (255, 255, 255)
red = (255, 0, 0)
purple = (105, 105, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
colors = [black, red, blue, green]


class item():
    def __init__(self, color, x, y, w, h, state = False):
        self.body_color = color
        self.dim = [x, y, w, h]
        self.state = state


def create_drawing_area(window):
    x = screen_width - draw_width
    y = screen_height - draw_height

    pygame.draw.rect(window, red, (x + spacing, y + spacing,draw_width - 2 * spacing, draw_height - 2 * spacing), rec_thickness)

    x = spacing
    y = spacing
    width = screen_width - draw_width
    height = screen_height
    pygame.draw.rect(window, red, (x, y, width - 2 * spacing, height - 2 * spacing), rec_thickness)

    pygame.display.update()


def create_tools_area(window):
    global brush, eraser, size_box, clear_screen, arr_items, color_box, save_img
    arr_items = []
    x = y = 2 * spacing
    font = pygame.font.SysFont(text_font, text_scale)

    brush = item(purple, x, y, toolbox_size, toolbox_size)
    arr_items.append(brush)
    label = font.render("B", True, black)
    tx, ty , tw, th = brush.dim[0] + spacing, brush.dim[1] + spacing, brush.dim[2] - spacing, brush.dim[3] - spacing
    window.blit(label, (tx, ty, tw, th))

    eraser = item(purple, x + 2 * spacing + toolbox_size, y, toolbox_size, toolbox_size)
    arr_items.append(eraser)
    label = font.render("E", True, black)
    tx, ty, tw, th = eraser.dim[0] + spacing, eraser.dim[1] + spacing, eraser.dim[2] - spacing, eraser.dim[3] - spacing
    window.blit(label, (tx, ty, tw, th))

    y += toolbox_size + 2 * spacing
    size_box = []
    for boxno in range(num_sizes):
        cur_x, cur_y = x + boxno * box_width + boxno * spacing, y
        Item = item(purple, cur_x, cur_y, box_width, box_height)
        size_box.append(Item)
        arr_items.append(Item)
        label = font.render(str(boxno + 1), True, black)
        tx, ty, tw, th = Item.dim[0] + spacing // 2, Item.dim[1] + spacing // 2, Item.dim[2] - spacing // 2, Item.dim[3] - spacing // 2
        window.blit(label, (tx, ty, tw, th))

    y += 2 * spacing + box_height
    clear_screen = item(purple, x, y, 3 * box_width, box_height)
    arr_items.append(clear_screen)
    label = font.render("Clear", True, black)
    tx, ty, tw, th = clear_screen.dim[0] + spacing // 2, clear_screen.dim[1] + spacing // 2, clear_screen.dim[2] - spacing // 2, clear_screen.dim[3] - spacing // 2
    window.blit(label, (tx, ty, tw, th))

    y += 2 * spacing + box_height
    color_box = []
    for boxno in range(num_colors):
        cur_x, cur_y = x + boxno * box_width + boxno * spacing, y
        Item = item(purple, cur_x, cur_y, box_width, box_height)
        pygame.draw.rect(window, colors[boxno], Item.dim, 0)
        color_box.append(Item)
        arr_items.append(Item)

    y += 2 * spacing + box_height
    save_img = item(purple, x, y, 3 * box_width, box_height)
    arr_items.append(save_img)
    label = font.render("Save", True, black)
    tx, ty, tw, th = save_img.dim[0] + spacing // 2, save_img.dim[1] + spacing // 2, save_img.dim[2] - spacing // 2, save_img.dim[3] - spacing // 2
    window.blit(label, (tx, ty, tw, th))

    pygame.display.update()


def identify_area(posx, posy):
    # Drawing Area
    if posx >= screen_width - draw_width and posx <= screen_width:
        return 1
    # Selection Area
    return 0


def isSelected(dim, posx, posy):
    if posx >= dim[0] and posx <= dim[0] + dim[2] and posy >= dim[1] and posy <= dim[1] + dim[3]:
        return True
    return False


def update_select_tools(window, posx, posy):
    global brush, eraser, size_box, clear_screen, arr_items, cur_thickness, cur_color, color_box, save_img
    x, y, w, h = brush.dim
    if(isSelected(brush.dim, posx, posy)):
        brush.state = True
        eraser.state = False
        cur_color = black
    elif(isSelected(eraser.dim, posx, posy)):
        brush.state = False
        eraser.state = True
        cur_color = white

    for boxno in range(num_sizes):
        if(isSelected(size_box[boxno].dim, posx, posy)):
            size_box[boxno].state = True
            cur_thickness = (boxno + 2) ** size_mul
            for j in range(num_sizes - 1):
                i = (boxno + j + 1) % num_sizes
                size_box[i].state = False

    if(isSelected(clear_screen.dim, posx, posy)):
        x, y = screen_width - draw_width + spacing, screen_height - draw_height + spacing
        w, h = draw_width - 2 * spacing, draw_height - 2 * spacing
        window.fill(white, (x, y, w, h), 0)

    for boxno in range(num_colors):
        if(isSelected(color_box[boxno].dim, posx, posy)):
            color_box[boxno].state = True
            cur_color = colors[boxno]
            for j in range(num_sizes - 1):
                i = (boxno + j + 1) % num_sizes
                color_box[i].state = False

    if (isSelected(save_img.dim, posx, posy)):
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        Filename = folder_name + str((random.randint(10, 100))) + ".jpeg"
        message_box("Image saved as: ", Filename)
        pygame.image.save(window, Filename)


    for Item in arr_items:
        if(Item.state == True):
            pygame.draw.rect(window, green, Item.dim, rec_thickness)
        else:
            pygame.draw.rect(window, white, Item.dim, rec_thickness)

    pygame.display.update()


def draw_around_cursor(window, x, y):
    pygame.draw.circle(window, cur_color, (x, y), cur_thickness)
    pygame.display.update()


def message_box(subject, content) :
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try :
        root.destroy()
    except :
        pass


def main(window):
    global draw, cur_color
    cur_color = white
    draw = False
    window.fill(white)
    create_tools_area(window)
    run = True

    while run:
        create_drawing_area(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                posy = event.pos[1]
                if(identify_area(posx, posy)):
                    # Drawing Area
                    draw = not(draw)

                else:
                    # Selection Area
                    draw = False
                    update_select_tools(window, posx, posy)

            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                posy = event.pos[1]
                if draw and identify_area(posx, posy) == 1:
                    draw_around_cursor(window, posx, posy)


        pygame.display.update()

    pygame.display.quit()


pygame.init()
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paint")
main(win)
