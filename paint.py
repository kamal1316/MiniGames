import pygame

# Dimensions
screen_width = 1600
screen_height = 1000
draw_width = 1200
draw_height = 1000
spacing = 20
little_spacing = 4
toolbox_size = 75
rec_thickness = 4
num_sizes = 4
box_width = 50
box_height = 50
draw = False
cur_thickness = 0
cur_color = 0
size_incre = 10
# Colors
white = (255, 255, 255)
red = (255, 0, 0)
purple = (105, 105, 255)
green = (0, 255, 0)
blue = (0, 0, 255)


class item():
    def __init__(self, color, x, y, w, h):
        self.body_color = color
        self.dim = [x, y, w, h]
        self.state = False


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
    global brush, eraser, size_box, clear_screen, arr_items
    arr_items = []

    x = spacing
    y = spacing

    x += spacing
    brush = item(purple, x, y + spacing, toolbox_size, toolbox_size)
    pygame.draw.rect(window, green, brush.dim, rec_thickness)
    arr_items.append(brush)

    eraser = item(purple, x + 2 * spacing + toolbox_size, y + spacing, toolbox_size, toolbox_size)
    pygame.draw.rect(window, green, eraser.dim, rec_thickness)
    arr_items.append(eraser)

    y += toolbox_size + 3 * spacing
    size_box = []
    for boxno in range(num_sizes):
        cur_x, cur_y = x + boxno * box_width + boxno * spacing, y
        Item = item(purple, cur_x, cur_y, box_width, box_height)
        pygame.draw.rect(window, green, Item.dim, rec_thickness)
        size_box.append(Item)
        arr_items.append(Item)

    y += 2 * spacing + box_height
    clear_screen = item(purple, x, y, 2 * box_width, box_height)
    pygame.draw.rect(window, green, clear_screen.dim, rec_thickness)
    arr_items.append(clear_screen)

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
    global brush, eraser, size_box, clear_screen, arr_items, cur_thickness, cur_color
    x, y, w, h = brush.dim
    if(isSelected(brush.dim, posx, posy)):
        brush.state = True
        eraser.state = False
        cur_color = blue
    elif(isSelected(eraser.dim, posx, posy)):
        brush.state = False
        eraser.state = True
        cur_color = white

    for boxno in range(num_sizes):
        if(isSelected(size_box[boxno].dim, posx, posy)):
            size_box[boxno].state = True
            cur_thickness = (boxno + 1) * size_incre
            for j in range(num_sizes - 1):
                i = (boxno + j + 1) % num_sizes
                size_box[i].state = False

    if(isSelected(clear_screen.dim, posx, posy)):
        x, y = screen_width - draw_width + spacing, screen_height - draw_height + spacing
        w, h = draw_width - 2 * spacing, draw_height - 2 * spacing
        window.fill(white, (x, y, w, h), 0)

    for Item in arr_items:
        x, y = Item.dim[0] + little_spacing, Item.dim[1] + little_spacing
        w, h = Item.dim[2] - 2 * little_spacing, Item.dim[3] - 2 * little_spacing
        if(Item.state == True):
            pygame.draw.rect(window, purple, (x, y, w, h), 0)
        else:
            pygame.draw.rect(window, white, (x, y, w, h), 0)
    pygame.display.update()


def draw_around_cursor(window, x, y):
    pygame.draw.circle(window, cur_color, (x, y), cur_thickness)
    pygame.display.update()


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
                    draw = not (draw)
                else:
                    # Selection Area
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
