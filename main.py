import pygame
import sys

# --- Initialisierung ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24, bold=True)

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
hase_pos = pygame.Rect(400, 300, 50, 50)
garten = pygame.Rect(100, 100, 300, 200)
shop = pygame.Rect(600, 100, 120, 120)

geld = 0
vorrat = 0
pflanzen_timer = 0
karotten_liste = [] #Hier werden die Positionen gespeichert

while True:
    # --- 1.Events (Tastatur / Maus) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Pflanzen mit Taste F
    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_f] and pflanzen_timer == 0:
        #Prüfe ob Hase im Garten
        if hase_pos.colliderect(garten):
            #An Position von Hase pflanzen
            neue_karotte = {"rect": pygame.Rect(hase_pos.x +10, hase_pos.y +10, 30, 30), "wachstum": 0}

            #Cool-Down
            if len(karotten_liste) < 20:
                karotten_liste.append(neue_karotte)
                pflanzen_timer = 15 #Wartezeit von 15 Frames

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

    # --- 3.Logik ---
    # Karotten wachsen lassen & Ernten
    for k in karotten_liste[:]:
        if k["wachstum"] < 100:
            k["wachstum"] += 0.3 #Wachstums-Geschw.

        # Ernten: Wenn Hase die Karotte berührt und reif ist
        if hase_pos.colliderect(k["rect"]) and k["wachstum"] >= 100:
            vorrat += 1
            karotten_liste.remove(k)

    # Verkaufen im Shop (E drücken)
    if hase_pos.colliderect(shop) and tasten[pygame.K_e]:
        geld += vorrat * 5
        vorrat = 0

    # --- 4. Zeichnen ---
    screen.fill((100, 180, 100)) #Gras
    pygame.draw.rect(screen, (139, 69, 19), garten) #Erde
    pygame.draw.rect(screen, (200, 200, 0), shop) #Shop-Hütte

    # Runterzählen des Cooldowns fürs pflanzen
    if pflanzen_timer > 0: pflanzen_timer -= 1

    # Karotten  je nach Status zeichnen
    for k in karotten_liste:
        if k["wachstum"] >= 100:
            #Reife Karotte
            screen.blit(karotte_gross, (k["rect"].x, k["rect"].y))
        else:
            #Solange sie noch wächst
            screen.blit(karotte_klein, (k["rect"].x, k["rect"].y))

    # Hase zeichnen
    screen.blit(hase_img, (hase_pos.x, hase_pos.y))

    # UI Text (Zwei Zeilen)
    geld_anzeige = font.render(f"Money: {geld}", True, (255, 255, 255))
    vorrat_anzeige = font.render(f"Carrots: {vorrat}", True, (255, 255, 255))
    hilfe_anzeige  = font.render("F: plant", True, (255, 255, 0))
    hilfe_anzeige2 = font.render("E: open shop", True, (0, 255, 255))
    screen.blit(geld_anzeige, (20, 20))
    screen.blit(vorrat_anzeige, (20, 50))
    screen.blit(hilfe_anzeige, (20, 80))
    screen.blit(hilfe_anzeige2, (20, 110))

    pygame.display.flip()
    clock.tick(60)