"""
boid.py
Boid (Sürü üyesi) sınıfını ve uçuş kurallarını (Separation, Alignment, Obstacle Avoidance) barındırır.
"""
import pygame
from pygame.math import Vector2
import math
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BOID,
    BOID_MAX_SPEED, BOID_MAX_FORCE,
    PERCEPTION_RADIUS, OBSTACLE_AVOIDANCE_RADIUS
)
from obstacle import Obstacle

class Boid:
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(velocity_x, velocity_y)
        if self.velocity.length() == 0:
            self.velocity = Vector2(1, 0) # Hareketsiz olmasını engelle
        self.acceleration = Vector2(0, 0)
        self.max_speed = BOID_MAX_SPEED
        self.max_force = BOID_MAX_FORCE
        
        # Üçgen çizimi için boyut
        self.size = 6

    def update(self) -> None:
        """Boid'in pozisyonunu, hızını ve ivmesini günceller."""
        self.velocity += self.acceleration
        
        # Hız limitini uygula
        if self.velocity.length_squared() > self.max_speed**2:
            self.velocity.scale_to_length(self.max_speed)
            
        self.position += self.velocity
        self.acceleration *= 0 # İvmeyi her karede sıfırla
        
        # Ekranın bir ucundan çıkınca diğer uçtan girmesini sağla (Wrap-around)
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH
            
        if self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = SCREEN_HEIGHT

    def apply_force(self, force: Vector2) -> None:
        """Boid'e bir kuvvet uygular."""
        self.acceleration += force

    def draw(self, surface: pygame.Surface) -> None:
        """Boid'i hareket yönüne bakan bir mavi üçgen olarak çizer."""
        angle = math.atan2(self.velocity.y, self.velocity.x)
        
        # Üçgenin üç köşesi (merkeze göre)
        # Ön nokta (Hareket yönü)
        p1 = Vector2(math.cos(angle) * self.size * 2, math.sin(angle) * self.size * 2)
        # Sol arka nokta
        p2 = Vector2(math.cos(angle + 2.5) * self.size * 1.5, math.sin(angle + 2.5) * self.size * 1.5)
        # Sağ arka nokta
        p3 = Vector2(math.cos(angle - 2.5) * self.size * 1.5, math.sin(angle - 2.5) * self.size * 1.5)
        
        # Ekrana göre konumlandır
        points = [
            self.position + p1,
            self.position + p2,
            self.position + p3
        ]
        
        # Polygon olarak çiz
        pygame.draw.polygon(surface, COLOR_BOID, [(p.x, p.y) for p in points])

    def separate(self, boids: list['Boid']) -> Vector2:
        """
        Separation: Çarpışmadan Kaçınma (Diğer boid'lerden uzaklaşma).
        Çok yakındaki boid'lerden uzağa doğru bir kuvvet hesaplar.
        """
        steer = Vector2(0, 0)
        total = 0
        # Ayrılma mesafe toleransı
        desired_separation = PERCEPTION_RADIUS / 2.0 
        
        for other in boids:
            if other is self:
                continue
                
            distance = self.position.distance_to(other.position)
            if 0 < distance < desired_separation:
                # Ters vektörü hesapla
                diff = self.position - other.position
                diff = diff.normalize() / distance # Yakınsa daha güçlü itilim
                steer += diff
                total += 1
                
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed
                steer -= self.velocity
                if steer.length() > self.max_force:
                    steer.scale_to_length(self.max_force)
                    
        return steer

    def align(self, boids: list['Boid']) -> Vector2:
        """
        Alignment: Yön Hizalama (Yakındaki boid'lerin ortalama yönüne uyum sağlama).
        """
        steer = Vector2(0, 0)
        total = 0
        
        for other in boids:
            if other is self:
                continue
                
            distance = self.position.distance_to(other.position)
            if 0 < distance < PERCEPTION_RADIUS:
                steer += other.velocity
                total += 1
                
        if total > 0:
            steer /= total
            if steer.length() > 0:
                steer = steer.normalize() * self.max_speed
                steer -= self.velocity
                if steer.length() > self.max_force:
                    steer.scale_to_length(self.max_force)
                    
        return steer

    def avoid_obstacles(self, obstacles: list[Obstacle]) -> Vector2:
        """
        Obstacle Avoidance: Engellerden kaçınma.
        Engele ne kadar yakınsa o kadar hızlı yön değiştirir.
        """
        steer = Vector2(0, 0)
        total = 0
        
        for obstacle in obstacles:
            # Engele dair en yakın noktayı buluyoruz
            closest_point = obstacle.get_closest_point(self.position)
            distance = self.position.distance_to(closest_point)
            
            if 0 < distance < OBSTACLE_AVOIDANCE_RADIUS:
                # Engelin en yakın noktasından boid'e doğru bir kaçınma vektörü oluştur
                diff = self.position - closest_point
                diff = diff.normalize() / distance # Mesafe ile ters orantılı etki (yakınsa daha şiddetli)
                steer += diff
                total += 1
                
        if total > 0:
            steer /= total
            if steer.length() > 0:
                # Kaçınma hızı acil olduğu için maksimum hızda uygulanır
                steer = steer.normalize() * self.max_speed
                steer -= self.velocity
                
                # Engellerden kaçınma kuvvetinin limiti, boid'in normal dönme kuvvetinden biraz daha yüksek olabilir,
                # çünkü hayatta kalma önceliği vardır. Oransal olarak 2 katı verebiliriz.
                avoid_force = self.max_force * 2.0
                if steer.length() > avoid_force:
                    steer.scale_to_length(avoid_force)
                    
        return steer
        
    def flock(self, boids: list['Boid'], obstacles: list[Obstacle]) -> None:
        """Tüm sürüş kurallarını uygular ve ağırlıklandırır."""
        separation = self.separate(boids)
        alignment = self.align(boids)
        avoidance = self.avoid_obstacles(obstacles)
        
        # Ağırlıklandırma
        separation *= 1.5
        alignment *= 1.0
        avoidance *= 2.5 # Engelden kaçınma en yüksek önceliğe sahip
        
        self.apply_force(separation)
        self.apply_force(alignment)
        self.apply_force(avoidance)
