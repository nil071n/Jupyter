@echo off
echo Creating Python script...

> galaxy_script.py (
echo import pygame
echo import math
echo import random
echo.
echo # Initialize pygame
echo pygame.init()
echo.
echo # Constants
echo WIDTH, HEIGHT = 800, 800
echo CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
echo NUM_DOTS = 200
echo MAX_RADIUS = 300
echo MAX_Z = 500
echo TRAIL_LENGTH = 20
echo FPS = 60  ^# Frames per second for smooth animation
echo SPEED = 0.02
echo.
echo # Set up the display
echo screen = pygame.display.set_mode((WIDTH, HEIGHT))
echo pygame.display.set_caption("3D Rotating Galaxy")
echo clock = pygame.time.Clock()
echo.
echo # Particle setup with 3D positions (x, y, z)
echo particles = []
echo for i in range(NUM_DOTS):
echo ^    speed = random.uniform(0.01, 0.05)
echo ^    radius = random.uniform(50, MAX_RADIUS)
echo ^    size = random.randint(2, 5)
echo ^    z = random.uniform(1, MAX_Z)
echo ^    hue_shift = random.uniform(0, 360)
echo ^    particles.append({
echo ^        "angle": random.uniform(0, 2 * math.pi),
echo ^        "speed": speed,
echo ^        "radius": radius,
echo ^        "size": size,
echo ^        "z": z  ^# Depth in 3D space
echo ^        "trail": [],
echo ^        "hue_shift": hue_shift
echo ^    })
echo.
echo # HSL to RGB conversion for vibrant colors
echo def hsl_to_rgb(h, s, l):
echo ^    from colorsys import hls_to_rgb
echo ^    r, g, b = hls_to_rgb(h / 360, l, s)
echo ^    return (int(r * 255), int(g * 255), int(b * 255))
echo.
echo # Perspective projection function
echo def project_3d_to_2d(x, y, z, focal_length=500):
echo ^    # Perspective projection formula
echo ^    factor = focal_length / (focal_length + z)
echo ^    x_2d = x * factor + CENTER_X
echo ^    y_2d = y * factor + CENTER_Y
echo ^    return int(x_2d), int(y_2d)
echo.
echo # Main loop
echo running = True
echo while running:
echo ^    screen.fill((0, 0, 0))  ^# Fill background with black
echo.
echo ^    for event in pygame.event.get():
echo ^        if event.type == pygame.QUIT:
echo
