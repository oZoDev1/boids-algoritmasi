"""
simulation.py
Simülasyonun genel akışını, boid'lerin ve engellerin yönetimini gerçekleştirir.
"""
import random
import pygame
from pygame.math import Vector2
from boid import Boid
from obstacle import CircleObstacle, SquareObstacle, RectangleObstacle, Obstacle
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_OBSTACLE, 
    BOID_START_COUNT, OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE
)

class Simulation:
    def __init__(self):
        self.boids: list[Boid] = []
        self.obstacles: list[Obstacle] = []
        self.is_paused: bool = False
        self.auto_obstacle_enabled: bool = False
        
        self.reset()
        
    def reset(self) -> None:
        """Simülasyonu başlangıç haline getirir."""
        self.boids.clear()
        self.obstacles.clear()
        for _ in range(BOID_START_COUNT):
            self.add_boid()
            
    def add_boid(self) -> None:
        """Rastgele bir konuma ve hıza sahip yeni bir boid ekler."""
        x = random.uniform(0, SCREEN_WIDTH)
        y = random.uniform(0, SCREEN_HEIGHT)
        
        # -1 ile 1 arasında rastgele bir yön
        vel_x = random.uniform(-1, 1)
        vel_y = random.uniform(-1, 1)
        
        self.boids.append(Boid(x, y, vel_x, vel_y))
        
    def add_random_obstacle(self) -> None:
        """Ekranda rastgele bir konuma, rastgele tipte bir engel ekler."""
        x = random.uniform(0, SCREEN_WIDTH)
        y = random.uniform(0, SCREEN_HEIGHT)
        pos = Vector2(x, y)
        
        shape_type = random.choice(['circle', 'square', 'rectangle'])
        
        if shape_type == 'circle':
            radius = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
            self.obstacles.append(CircleObstacle(pos, radius, COLOR_OBSTACLE))
        elif shape_type == 'square':
            side = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 2
            self.obstacles.append(SquareObstacle(pos, side, COLOR_OBSTACLE))
        elif shape_type == 'rectangle':
            width = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 2
            height = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 3
            self.obstacles.append(RectangleObstacle(pos, width, height, COLOR_OBSTACLE))

    def add_obstacle_at(self, pos_tuple: tuple[int, int]) -> None:
        """Belirtilen fare pozisyonuna rastgele tipli bir engel ekler."""
        pos = Vector2(pos_tuple[0], pos_tuple[1])
        shape_type = random.choice(['circle', 'square', 'rectangle'])
        
        if shape_type == 'circle':
            radius = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
            self.obstacles.append(CircleObstacle(pos, radius, COLOR_OBSTACLE))
        elif shape_type == 'square':
            side = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 2
            self.obstacles.append(SquareObstacle(pos, side, COLOR_OBSTACLE))
        elif shape_type == 'rectangle':
            width = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 2
            height = random.uniform(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE) * 3
            self.obstacles.append(RectangleObstacle(pos, width, height, COLOR_OBSTACLE))

    def remove_obstacle_at(self, pos_tuple: tuple[int, int]) -> None:
        """Belirtilen noktaya denk gelen engelleri siler."""
        pos = Vector2(pos_tuple[0], pos_tuple[1])
        # Noktayı içeren engelleri filtreliyoruz
        self.obstacles = [obs for obs in self.obstacles if not obs.is_point_inside(pos)]
        
    def toggle_pause(self) -> None:
        self.is_paused = not self.is_paused
        
    def toggle_auto_obstacle(self) -> None:
        self.auto_obstacle_enabled = not self.auto_obstacle_enabled

    def update(self) -> None:
        """Simülasyon durumunu günceller."""
        if self.is_paused:
            return
            
        # Otomatik engel üretimi (%1 ihtimalle her frame için)
        if self.auto_obstacle_enabled and random.random() < 0.01:
            self.add_random_obstacle()
            
        # Boid'leri güncelle
        for boid in self.boids:
            # Algoritma kural setini uygula
            boid.flock(self.boids, self.obstacles)
            boid.update()

    def draw(self, surface: pygame.Surface) -> None:
        """Tüm elemanları ekrana çizer."""
        for obstacle in self.obstacles:
            obstacle.draw(surface)
            
        for boid in self.boids:
            boid.draw(surface)
