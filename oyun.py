import pygame as py
import random
import os

py.init()
py.mixer.init()

ekran = py.display.set_mode((1000, 700))
py.display.set_caption("Flappy Dragon")
clock = py.time.Clock()

font = py.font.Font("Game of Thrones.ttf", 50)

ejderha_up = py.transform.scale(py.image.load("assets/ejderha_kanat_up.png"), (120, 90))
ejderha_down = py.transform.scale(py.image.load("assets/ejderha_kanat_down.png"), (120, 90))
duvar_asset = py.transform.scale(py.image.load("assets/duvar.png"), (70, 500))

arka_planlar = [
    py.transform.scale(py.image.load("assets/winterfell2.png"), (1000, 700)),
    py.transform.scale(py.image.load("assets/kings_landing.png"), (1000, 700)),
    py.transform.scale(py.image.load("assets/ejder_kayası.png"), (1000, 700)),
    py.transform.scale(py.image.load("assets/dorne.png"), (1000, 700))

]

secili_arka_plan = random.choice(arka_planlar)

hiz = 5
yer_cekimi = 3
bosluk_mesafesi = 275

game_over = False
ejderha_x = 50
ejderha_y = 350
kanat_sayaci = 0
duvarlar = []

py.mixer.music.load("got_music.mp3")
py.mixer.music.set_volume(0.1)
py.mixer.music.play(-1)

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            os._exit(0)
            
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE and not game_over:
                ejderha_y -= 65
                kanat_sayaci = 15
                
            if event.key == py.K_r and game_over:
                game_over = False
                ejderha_y = 350
                duvarlar.clear()
                kanat_sayaci = 0
                secili_arka_plan = random.choice(arka_planlar)

    ekran.blit(secili_arka_plan, (0, 0))

    if not game_over:
        ejderha_y += yer_cekimi
        
        if not duvarlar or duvarlar[-1]["x"] < 600:
            duvarlar.append({"x": 1000, "gap": random.randint(100, 400)})
            
        aktif_duvarlar = []
        ejderha_rect = py.Rect(ejderha_x, ejderha_y, ejderha_up.get_width(), ejderha_up.get_height())
        
        for duvar in duvarlar:
            duvar["x"] -= hiz
            
            ust_y = duvar["gap"] - 500
            alt_y = duvar["gap"] + bosluk_mesafesi
            
            ust_rect = py.Rect(duvar["x"], ust_y, 70, 500)
            alt_rect = py.Rect(duvar["x"], alt_y, 70, 500)
            
            ekran.blit(duvar_asset, (duvar["x"], ust_y))
            ekran.blit(duvar_asset, (duvar["x"], alt_y))
            
            if ejderha_rect.colliderect(ust_rect) or ejderha_rect.colliderect(alt_rect):
                game_over = True
                
            if duvar["x"] > -70:
                aktif_duvarlar.append(duvar)
                
        duvarlar = aktif_duvarlar
        
        if kanat_sayaci > 0:
            if 5 < kanat_sayaci <= 10:
                ekran.blit(ejderha_up, (ejderha_x, ejderha_y))
            else:
                ekran.blit(ejderha_down, (ejderha_x, ejderha_y))
            kanat_sayaci -= 1
        else:
            ekran.blit(ejderha_up, (ejderha_x, ejderha_y))
      
        ejderha_y = max(0, min(ejderha_y, 700 - ejderha_up.get_height()))
        ejderha_x = max(0, min(ejderha_x, 1000 - ejderha_up.get_width()))

    else:
        for duvar in duvarlar:
            ust_y = duvar["gap"] - 500
            alt_y = duvar["gap"] + bosluk_mesafesi
            ekran.blit(duvar_asset, (duvar["x"], ust_y))
            ekran.blit(duvar_asset, (duvar["x"], alt_y))

        game_over_text = font.render("GAME OVER", True, (138, 3, 3))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        
        ekran.blit(game_over_text, game_over_text.get_rect(center=(500, 300)))
        ekran.blit(restart_text, restart_text.get_rect(center=(500, 400)))

    py.display.flip()
    clock.tick(60)