import pygame
import math

pygame.init()
pantalla = pygame.display.set_mode([1000, 600])
pygame.display.set_caption('Trump Clicker')

audio = pygame.mixer.Sound("C:/PYGAME/assets/usaanthem.mp3")
audio.play(-1)
audio.set_volume(0.5)

score = 0
autoclicker_cost = 50
autoclickers = 0
autoclick_rate = 1
last_autoclick_time = 0

nukebomb_cost = 100
nukebomb = 0
nukebomb_rate = 2
last_nukebomb_time = 0

power_click_cost = 200
power_click_active = False


# Posición del círculo (Trump estará a la izquierda)
circle_center = (200, 300)  # Cambiado para que esté centrado verticalmente pero a la izquierda
circle_radius = 150

# Animacion click
animation_start_time = None
animation_duration = 200
animation_scale_factor = 1.1
animated_circle_radius = circle_radius  

# Declarar fuente
font = pygame.font.Font("C:/PYGAME/assets/Teko-Regular.ttf", 64)
small_font = pygame.font.Font("C:/PYGAME/assets/Teko-Regular.ttf", 26)

# Declarar imagen y cambiarle tamaño
imgTrump = pygame.image.load("C:/PYGAME/assets/trumpmugshoot.png")
imgTrump = pygame.transform.scale(imgTrump, (circle_radius * 2, circle_radius * 2))

cursor_trump = pygame.image.load("C:/PYGAME/assets/cursortrump.png")
pygame.display.set_icon(cursor_trump)

fondoTrump = pygame.image.load("C:/PYGAME/assets/trumpShoot.jpg")
fondoTrump = pygame.transform.scale(fondoTrump, (1000, 600)) 

fondoFlag = pygame.image.load("C:/PYGAME/assets/flag.png")
fondoFlag = pygame.transform.scale(fondoFlag, (400, 600))

# Posición y centrar círculo con la foto de Trump
imagen_rect = imgTrump.get_rect(center=circle_center)

game_started = False
running = True
cursor_hover = False

# Pantalla de inicio
while not game_started:
    pantalla.blit(fondoTrump, (0, 0))  # Fondo ajustado a la nueva resolución
    start_text = font.render("Click to Start", True, (255, 255, 255))
    pantalla.blit(start_text, (400, 500))  # Centrado horizontalmente
    titulo_text = font.render("TRUMP CLICKER", True, (255, 255, 255))
    pantalla.blit(titulo_text, (350, 50))  # Título centrado
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_started = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                audio.stop()
                game_started = True

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                distance = math.hypot(mouse_pos[0] - circle_center[0], mouse_pos[1] - circle_center[1])
                if distance <= circle_radius:
                    animation_start_time = pygame.time.get_ticks()
                    if power_click_active:
                        score += 2
                    else:
                        score += 1
                # Detectar clic en el botón de autoclicker
                if 500 <= mouse_pos[0] <= 650 and 500 <= mouse_pos[1] <= 550:
                    if score >= autoclicker_cost:
                        score -= autoclicker_cost
                        autoclickers += 1
                        autoclicker_cost = int(autoclicker_cost * 1.25)
                if 690 <= mouse_pos[0] <= 840 and 500 <= mouse_pos[1] <= 550:
                    if score >= nukebomb_cost:
                        score -= nukebomb_cost
                        nukebomb += 1
                        nukebomb_cost = int(nukebomb_cost * 1.75)
                if 500 <= mouse_pos[0] <= 650 and 430 <= mouse_pos[1] <= 480:
                    if score >= power_click_cost:
                        score -= power_click_cost
                        power_click_active = True

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            distance = math.hypot(mouse_pos[0] - circle_center[0], mouse_pos[1] - circle_center[1])
            cursor_hover = distance <= circle_radius

    # Fondo
    pantalla.fill((0, 0, 0))
    pantalla.blit(fondoFlag, (0, 0))

    # Mostrar puntuación
    score_text = font.render("Votes: " + str(score), True, (255, 255, 255))
    pantalla.blit(score_text, (510, 75))  # Movido a la parte derecha

    # Animación de ampliación de la imagen de Trump
    current_time = pygame.time.get_ticks()
    # Si se ha hecho click , iniciado el tiempo de animación
    if animation_start_time and current_time - animation_start_time <= animation_duration:
        scale_factor = 1 + (animation_scale_factor - 1) * (current_time - animation_start_time) / animation_duration
        imgTrump_scaled = pygame.transform.scale(imgTrump, (int(circle_radius * 2 * scale_factor), int(circle_radius * 2 * scale_factor)))
    else:
        imgTrump_scaled = pygame.transform.scale(imgTrump, (circle_radius * 2, circle_radius * 2))
        animation_start_time = None  # Reset

    # Mostrar la imagen de Trump (con escala si se está animando)
    imagen_rect = imgTrump_scaled.get_rect(center=circle_center)
    pantalla.blit(imgTrump_scaled, imagen_rect)

    # Botón de compra autoclicker
    button_color = (0, 128, 255) if score >= autoclicker_cost else (128, 128, 128)
    pygame.draw.rect(pantalla, button_color, (500, 500, 150, 50))
    voter_text = small_font.render(f"Buy Voters ({autoclicker_cost})", True, (255, 255, 255))
    pantalla.blit(voter_text, (510, 510))
    
    # Botón de compra nuke
    nuke_color = (0, 128, 255) if score >= nukebomb_cost else (128, 128, 128)
    pygame.draw.rect(pantalla, nuke_color, (690, 500, 150, 50))
    nuke_text = small_font.render(f"Buy Nukes ({nukebomb_cost})", True, (255, 255, 255))
    pantalla.blit(nuke_text, (700, 510))
    
    # Botón de Power Click, quitarlo si ya se ha hecho click
    if not power_click_active:
        power_color = (0, 128, 255) if score >= power_click_cost else (128, 128, 128)
        pygame.draw.rect(pantalla, power_color, (500, 430, 150, 50))
        power_text = small_font.render(f"Elon Boost ({power_click_cost})", True, (255, 255, 255))
        pantalla.blit(power_text, (510, 440))

    # Mostrar autoclickers
    autoclicker_text = small_font.render(f"Voters: {autoclickers}", True, (255, 255, 255))
    pantalla.blit(autoclicker_text, (510, 150))

    # Mostrar nukebomb
    nukebomb_text = small_font.render(f"Nukes: {nukebomb}", True, (255, 255, 255))
    pantalla.blit(nukebomb_text, (600, 150))

    # Mostrar el cursor diferente si esta en el círculo
    if cursor_hover:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pantalla.blit(cursor_trump, (mouse_x, mouse_y))
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    # Lógica de autoclickers y nukebombs
    if autoclickers > 0 and current_time - last_autoclick_time >= 1000:
        score += autoclickers * autoclick_rate
        last_autoclick_time = current_time
    
    if nukebomb > 0 and current_time - last_nukebomb_time >= 2000:
        score += nukebomb * nukebomb_rate
        last_nukebomb_time = current_time

    pygame.display.flip()

pygame.quit()