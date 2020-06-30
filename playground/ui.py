from svg import Parser, Rasterizer

import pygame

WIDTH=512
HEIGHT=512

running = True

def start_ui():
    global running
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess UI")
    screen.fill((0,255,255))
    
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(15)
        for event in pygame.events():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        pygame.display.flip()
    
def update(done=False):
    if (done):
        pygame.quit()
        return

    
def load_svg(filename, scale=None, size=None, clip_from=None, fit_to=None):
    """Returns Pygame Image object from rasterized SVG
    If scale (float) is provided and is not None, image will be scaled.
    If size (w, h tuple) is provided, the image will be clipped to specified size.
    If clip_from (x, y tuple) is provided, the image will be clipped from specified point.
    If fit_to (w, h tuple) is provided, image will be scaled to fit in specified rect.
    """
    svg = Parser.parse_file(filename)
    tx, ty = 0, 0
    if size is None:
        w, h = svg.width, svg.height
    else:
        w, h = size
        if clip_from is not None:
            tx, ty = clip_from
    if fit_to is None:
        if scale is None:
            scale = 1
    else:
        fit_w, fit_h = fit_to
        scale_w = float(fit_w) / svg.width
        scale_h = float(fit_h) / svg.height
        scale = min([scale_h, scale_w])
    rast = Rasterizer()
    req_w = int(w * scale)
    req_h = int(h * scale)
    buff = rast.rasterize(svg, req_w, req_h, scale, tx, ty)
    image = pygame.image.frombuffer(buff, (req_w, req_h), 'ARGB')
    return image

def main():
    start_ui()
    while True:
        command = input("type 'exit' to leave")
        if command == 'exit':
            update(True)
            exit()
        else:
            update(True)

if __name__ == "__main__":
    main()