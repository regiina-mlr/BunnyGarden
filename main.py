import pygame
import sys

# --- Initialisierung ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24, bold=True)
BORDER_X = 1500
BORDER_Y = 1000

# --- Bilder laden ---
hase_img = pygame.image.load('hase.jpg')
hase_img = pygame.transform.scale(hase_img, (50, 50))

# Bild für die fertige Karotte
karotte_gross = pygame.image.load('karotte.png')
karotte_gross = pygame.transform.scale(karotte_gross, (30, 30))

# Bild für den kleinen Keimling
karotte_klein = pygame.image.load('keimling.jpg')
karotte_klein = pygame.transform.scale(karotte_klein, (30, 30))

# --- Variablen ---
hase_pos = pygame.Rect(700, 500, 50, 50)
garten = pygame.Rect(600, 400, 300, 200)
shop = pygame.Rect(1000, 200, 120, 120)

# --- Tastenbelegung ---
pflanz_taste = pygame.K_f
shop_taste = pygame.K_e

geld = 0
vorrat = 0
pflanzen_timer = 0
karotten_liste = [] #Hier werden die Positionen gespeichert
kamera_x = 0
kamera_y = 0
deadzone = pygame.Rect(300, 225, 200, 150)

# --- Raster erstellen ---
slots = []
for reihe in range(3):
    for spalte in range(4):
        x = garten.x + 30 + (spalte * 70)
        y = garten.y + 20 + (reihe * 65)
        slots.append({"rect": pygame.Rect(x, y, 30, 30), "belegt": False})

while True:
    # --- 1.Events (Tastatur / Maus) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Pflanzen mit Taste F auf Raster
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_f] and pflanzen_timer == 0:
        for s in slots:
            if hase_pos.colliderect(s["rect"]) and not s["belegt"]:
                neue_karotte = {"rect": s["rect"].copy(), "wachstum": 0, "slot_idx": slots.index(s)}
                karotten_liste.append(neue_karotte)
                s["belegt"] = True
                pflanzen_timer = 20 #Wartezeit von 20 Frames
                break

    # --- 2.Steuerung (WASD) ---
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_w]: hase_pos.y -=5
    if tasten[pygame.K_s]: hase_pos.y += 5
    if tasten[pygame.K_a]: hase_pos.x -= 5
    if tasten[pygame.K_d]: hase_pos.x += 5
    # Pfeiltasten
    if tasten[pygame.K_UP]: hase_pos.y -= 5
    if tasten[pygame.K_DOWN]: hase_pos.y += 5
    if tasten[pygame.K_LEFT]: hase_pos.x -= 5
    if tasten[pygame.K_RIGHT]: hase_pos.x += 5
    # Kamera-Logik
    if hase_pos.x -kamera_x > deadzone.right:
        kamera_x = hase_pos.x -deadzone.right

    if hase_pos.x -kamera_x < deadzone.left:
        kamera_x = hase_pos.x -deadzone.left

    if hase_pos.y -kamera_y > deadzone.bottom:
        kamera_y = hase_pos.y -deadzone.bottom

    if hase_pos.y -kamera_y < deadzone.top:
        kamera_y = hase_pos.y -deadzone.top

    if kamera_x < 0: kamera_x = 0
    if kamera_y < 0: kamera_y = 0

    if kamera_x > BORDER_X + hase_img.get_width() - SCREEN_WIDTH : kamera_x = BORDER_X + hase_img.get_width() - SCREEN_WIDTH
    if kamera_y > BORDER_Y +hase_img.get_height() - SCREEN_HEIGHT: kamera_y = BORDER_Y +hase_img.get_height() - SCREEN_HEIGHT


    if hase_pos.x < 0: hase_pos.x = 0
    if hase_pos.y < 0: hase_pos.y = 0

    if hase_pos.x > BORDER_X: hase_pos.x = BORDER_X
    if hase_pos.y > BORDER_Y: hase_pos.y = BORDER_Y

    # --- 3.Logik ---
    # Karotten wachsen lassen & Ernten
    for k in karotten_liste[:]:
        if k["wachstum"] < 100:
            k["wachstum"] += 0.3 #Wachstums-Geschw.

        # Ernten: Wenn Hase die Karotte berührt und reif ist
        if hase_pos.colliderect(k["rect"]) and k["wachstum"] >= 100:
            vorrat += 1
            slots[k["slot_idx"]]["belegt"] = False
            karotten_liste.remove(k)

    # Verkaufen im Shop (E drücken)
    if hase_pos.colliderect(shop) and tasten[shop_taste]:
        geld += vorrat * 5
        vorrat = 0

    # --- 4. Zeichnen ---
    screen.fill((100, 180, 100)) #Gras
    pygame.draw.rect(screen, (139, 69, 19), (garten.x-kamera_x,garten.y-kamera_y, garten.width, garten.height)) #Erde
    pygame.draw.rect(screen, (200, 200, 0), (shop.x-kamera_x, shop.y-kamera_y, shop.width, shop.height)) #Shop-Hütte

    # --- NEU: Plätze im Garten markieren
    for s in slots:
        if not s["belegt"]:
            p_x = s["rect"].centerx - kamera_x
            p_y = s["rect"].centery - kamera_y
            pygame.draw.circle(screen, (80, 50, 30), (p_x, p_y), 4)

    # Runterzählen des Cooldowns fürs pflanzen
    if pflanzen_timer > 0: pflanzen_timer -= 1

    # Karotten je nach Status zeichnen
    for k in karotten_liste:
        k_x = k["rect"].x - kamera_x
        k_y = k["rect"].y - kamera_y
        if k["wachstum"] >= 100:
            #Reife Karotte
            screen.blit(karotte_gross, (k_x, k_y))
        else:
            #Solange sie noch wächst
            screen.blit(karotte_klein, (k_x, k_y))

    # Hase zeichnen
    screen.blit(hase_img, (hase_pos.x-kamera_x, hase_pos.y-kamera_y))
    #pygame.draw.rect(screen, (255, 0, 0), (hase_pos.x-kamera_x, hase_pos.y-kamera_y, 10, 10))

    # UI Text (Zwei Zeilen)
    geld_anzeige = font.render(f"Money: {geld}", True, (255, 255, 255))
    vorrat_anzeige = font.render(f"Carrots: {vorrat}", True, (255, 255, 255))
    hilfe_anzeige  = font.render(f"{chr(pflanz_taste)}: plant", True, (255, 255, 0))
    hilfe_anzeige2 = font.render(f"{chr(shop_taste)}: open shop", True, (0, 255, 255))
    screen.blit(geld_anzeige, (20, 20))
    screen.blit(vorrat_anzeige, (20, 50))
    screen.blit(hilfe_anzeige, (20, 80))
    screen.blit(hilfe_anzeige2, (20, 110))

    cords_anzeige = font.render(f"Cords: {hase_pos.x},{hase_pos.y}", True, (255, 255, 255))
    screen.blit(cords_anzeige, (SCREEN_WIDTH -250, 20))

    pygame.display.flip()
    clock.tick(60)