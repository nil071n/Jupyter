@echo off
echo Creating Python script...

:: Create the Python script as a .py file
(
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
echo ^            running = False
echo.
echo ^    # Update and draw particles with 3D rotation
echo ^    for p in particles:
echo ^        # Update the angle for 3D rotation (rotate around y-axis)
echo ^        p["angle"] += p["speed"]
echo ^        p["z"] -= 1  ^# Move the particle forward in 3D space
echo ^        if p["z"] < 1:  ^# Reset the particle to the back once it's too close
echo ^            p["z"] = MAX_Z
echo.
echo ^        # 3D to 2D conversion (for the visual effect)
echo ^        x = p["radius"] * math.cos(p["angle"])
echo ^        y = p["radius"] * math.sin(p["angle"])
echo.
echo ^        # Apply perspective projection (simulate depth)
echo ^        x_2d, y_2d = project_3d_to_2d(x, y, p["z"])
echo.
echo ^        # Update trail
echo ^        p["trail"].append((x_2d, y_2d))
echo ^        if len(p["trail"]) > TRAIL_LENGTH:
echo ^            p["trail"].pop(0)
echo.
echo ^        # Draw the trail with fading effect
echo ^        for i, (tx, ty) in enumerate(p["trail"]):
echo ^            opacity = i / TRAIL_LENGTH  ^# Fading effect
echo ^            color = hsl_to_rgb((p["hue_shift"] + i * 10) % 360, 1, 0.5)
echo ^            pygame.draw.circle(screen, color, (tx, ty), p["size"])
echo.
echo pygame.display.flip()
echo clock.tick(FPS)  ^# Control the frame rate
echo.
echo pygame.quit()
) > galaxy_script.py

:: Check if Python is installed and available in PATH
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not available in your PATH.
    pause
    exit /b
)

:: Run the Python script (assuming python is in the PATH)
echo Running the Python script...
python galaxy_script.py

:: End of script
pause
