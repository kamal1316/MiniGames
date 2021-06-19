import pygame

width, height = 500, 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
clientNumber = 0


class Player():
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect = (x, y, w, h)
        self.val = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.val
        if keys[pygame.K_RIGHT]:
            self.x += self.val
        if keys[pygame.K_UP]:
            self.y -= self.val
        if keys[pygame.K_DOWN]:
            self.y += self.val
        self.rect = (self.x, self.y, self.w, self.h)


def redrawWindow(win, player):
    win.fill((255, 255, 255))
    player.draw(win)
    pygame.display.update()


def main():
    p = Player(50, 50, 100, 100, (0, 255, 0))
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run  = False

        p.move()
        redrawWindow(win, p)

    pygame.quit()

main()