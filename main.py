"""
main.py
Programın giriş noktası. Pygame ayarlarını ve olay döngüsünü (Event Loop) içerir.
"""
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BACKGROUND
from simulation import Simulation

def main() -> None:
    # Pygame kütüphanesini başlat
    pygame.init()
    
    # Ekran oluştur
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boids Algoritması - Sürü Simülasyonu")
    
    # FPS kontrolcüsü
    clock = pygame.time.Clock()
    
    # Simülasyon yöneticisi
    sim = Simulation()
    
    running = True
    while running:
        # Olay (Event) Döngüsü
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Fare Tıklamaları
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Sol tık
                    sim.add_obstacle_at(pygame.mouse.get_pos())
                elif event.button == 3: # Sağ tık
                    sim.remove_obstacle_at(pygame.mouse.get_pos())
                    
            # Klavye Girişleri
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sim.reset()
                elif event.key == pygame.K_o:
                    sim.add_random_obstacle()
                elif event.key == pygame.K_b:
                    sim.add_boid()
                elif event.key == pygame.K_SPACE:
                    sim.toggle_pause()
                elif event.key == pygame.K_t:
                    sim.toggle_auto_obstacle()

        # Güncelleme
        sim.update()
        
        # Çizim
        screen.fill(COLOR_BACKGROUND)
        sim.draw(screen)
        
        # UI Bilgileri
        font = pygame.font.SysFont(None, 24)
        info_text = [
            f"Boids: {len(sim.boids)}",
            f"Engeller: {len(sim.obstacles)}",
            f"Duraklatildi: {'Evet' if sim.is_paused else 'Hayir'}",
            f"Oto Engel: {'Açik' if sim.auto_obstacle_enabled else 'Kapali'}",
            "",
            "Kontroller:",
            "Sol Tik: Engel Ekle",
            "Sag Tik: Engel Sil",
            "R: Sifirla",
            "O: Rastgele Engel",
            "B: Boid Ekle",
            "SPACE: Duraklat",
            "T: Oto Engel Ac/Kapa"
        ]
        
        for i, line in enumerate(info_text):
            text_surf = font.render(line, True, (200, 200, 200))
            screen.blit(text_surf, (10, 10 + i * 25))

        # Ekranı Yenile
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
