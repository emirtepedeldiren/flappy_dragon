import pygame as py
import random
import json
import os

py.init()
py.mixer.init()

ekran = py.display.set_mode((1000, 700))
py.display.set_caption("Flappy Dragon")
clock = py.time.Clock()

font = py.font.Font("got_font.ttf", 50)
skor_font = py.font.SysFont("Arial", 50, bold=True)
ejderha_up = py.transform.scale(py.image.load("assets/ejderha_kanat_up.png"), (120, 90))
ejderha_down = py.transform.scale(py.image.load("assets/ejderha_kanat_down.png"), (120, 90))
duvar_asset = py.transform.scale(py.image.load("assets/duvar.png"), (70, 500))

winterfell_bg = py.transform.scale(py.image.load("assets/winterfell2.png"), (1000, 700))

arka_planlar = [
    winterfell_bg,
    py.transform.scale(py.image.load("assets/kings_landing.png"), (1000, 700)),
    py.transform.scale(py.image.load("assets/ejder_kayası.png"), (1000, 700)),
    py.transform.scale(py.image.load("assets/dorne.png"), (1000, 700))
]

secili_arka_plan = random.choice(arka_planlar)

app_data_dir = os.path.expanduser("~/.flappy_dragon_data")
os.makedirs(app_data_dir, exist_ok=True)

DATA_FILE = os.path.join(app_data_dir, "high_score.json")

duvarin_hizi = 5
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

def save_data(kaydedilecek_skor):
    data = {"skor": kaydedilecek_skor}

    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"skor": 0}
    
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        return data


en_yuksek_skor_data = load_data()
en_yuksek_skor = en_yuksek_skor_data["skor"]
skor = 0


while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            os._exit(0)
            
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE and not game_over:
                ejderha_y -= 65
                kanat_sayaci = 10
                
            if event.key == py.K_r and game_over:
                game_over = False
                ejderha_y = 350
                duvarlar.clear()
                kanat_sayaci = 0
                secili_arka_plan = random.choice(arka_planlar)
                skor = 0
                duvarin_hizi = 5

    ekran.blit(secili_arka_plan, (0, 0))

    if not game_over:
        ejderha_y += yer_cekimi

        if not duvarlar or duvarlar[-1]["x"] < 600:
            duvarlar.append({"x": 1000, "gap": random.randint(100, 400)})
        
        aktif_duvarlar = []
        ejderha_rect = py.Rect(ejderha_x, ejderha_y, ejderha_up.get_width(), ejderha_up.get_height())
        
        for duvar in duvarlar:
            duvar["x"] -= duvarin_hizi
            
            ust_y = duvar["gap"] - 500
            alt_y = duvar["gap"] + bosluk_mesafesi

            ust_rect = py.Rect(duvar["x"], ust_y, 70, 500)
            alt_rect = py.Rect(duvar["x"], alt_y, 70, 500)
            
            ekran.blit(duvar_asset, (duvar["x"], ust_y))
            ekran.blit(duvar_asset, (duvar["x"], alt_y))
            
            if ejderha_rect.colliderect(ust_rect) or ejderha_rect.colliderect(alt_rect):
                if not game_over:
                    if skor > en_yuksek_skor:
                        en_yuksek_skor = skor
                        save_data(en_yuksek_skor)
                game_over = True


            if ejderha_x > duvar["x"] + duvar_asset.get_width() and not duvar.get("gecildi",False):
                skor+= 1
                duvar["gecildi"] = True
                
                if skor > 0 and skor % 10 == 0:
                    duvarin_hizi += 1
                
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

        if secili_arka_plan == winterfell_bg:
            game_over_text = font.render("WINTER IS COMING", True, (11, 25, 44)) 
            ekran.blit(game_over_text, game_over_text.get_rect(center=(500, 100)))
        else:
            game_over_text = font.render("GAME OVER", True, (138, 3, 3))
            ekran.blit(game_over_text, game_over_text.get_rect(center=(500, 300)))
            
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        ekran.blit(restart_text, restart_text.get_rect(center=(500, 400)))
    
    if game_over:
        
        skor_y = 180 if secili_arka_plan == winterfell_bg else 130
        high_score_y = 240 if secili_arka_plan == winterfell_bg else 190

        skor_yazisi = font.render("Score", True, (255,255,255))
        skor_sayisi = skor_font.render(": " + str(skor), True, (255,255,255))
        skor_genislik = skor_yazisi.get_width() + skor_sayisi.get_width()
        skor_x = 500 - (skor_genislik // 2)
        
        ekran.blit(skor_yazisi, skor_yazisi.get_rect(midleft=(skor_x, skor_y)))
        ekran.blit(skor_sayisi, skor_sayisi.get_rect(midleft=(skor_x + skor_yazisi.get_width(), skor_y)))

        high_score_yazisi = font.render("High Score", True, (255,255,255))
        high_score_sayisi = skor_font.render(": " + str(en_yuksek_skor), True, (255,255,255))
        high_score_genislik = high_score_yazisi.get_width() + high_score_sayisi.get_width()
        high_score_x = 500 - (high_score_genislik // 2)
        
        ekran.blit(high_score_yazisi, high_score_yazisi.get_rect(midleft=(high_score_x, high_score_y)))
        ekran.blit(high_score_sayisi, high_score_sayisi.get_rect(midleft=(high_score_x + high_score_yazisi.get_width(), high_score_y)))
    else:
        
        skor_yazisi = skor_font.render(str(skor), True, (255,255,255))
        yazi_rect = skor_yazisi.get_rect(center=(500, 50))
        ekran.blit(skor_yazisi, yazi_rect)

    py.display.flip()
    clock.tick(60)