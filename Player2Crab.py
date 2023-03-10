import pygame

x = 450
y = 50
width = 40
height = 60
velocity = 5

while True:
    pygame.time.delay(16)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity
    pygame.draw.rect(screen, (0, 0, 180), (x, y, width, height))
    pygame.display.update()