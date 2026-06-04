"""
obstacle.py
Bu dosya engelleri ve farklı şekillerdeki engellerin temel davranışlarını barındırır.
"""
from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2

class Obstacle(ABC):
    """
    Tüm engeller için soyut temel sınıf (Abstract Base Class).
    """
    def __init__(self, position: Vector2, color: tuple[int, int, int]):
        self.position = position
        self.color = color

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Engeli ekrana çizer."""
        pass

    @abstractmethod
    def get_closest_point(self, point: Vector2) -> Vector2:
        """
        Verilen bir noktaya (örneğin boid pozisyonuna) en yakın olan 
        engel üzerindeki noktayı döndürür. Çarpışmadan kaçınma için kullanılır.
        """
        pass

    @abstractmethod
    def is_point_inside(self, point: Vector2) -> bool:
        """Bir noktanın engel içinde olup olmadığını kontrol eder (Sağ tık ile silme için)."""
        pass

class CircleObstacle(Obstacle):
    def __init__(self, position: Vector2, radius: float, color: tuple[int, int, int]):
        super().__init__(position, color)
        self.radius = radius

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))

    def get_closest_point(self, point: Vector2) -> Vector2:
        # Çember merkezinden noktaya olan yön vektörü
        direction = point - self.position
        if direction.length_squared() == 0:
            return Vector2(self.position.x + self.radius, self.position.y)
        
        direction = direction.normalize()
        return self.position + direction * self.radius

    def is_point_inside(self, point: Vector2) -> bool:
        return self.position.distance_to(point) <= self.radius

class RectangleObstacle(Obstacle):
    def __init__(self, position: Vector2, width: float, height: float, color: tuple[int, int, int]):
        # position, dikdörtgenin merkezi olacak şekilde ayarlanır.
        super().__init__(position, color)
        self.width = width
        self.height = height
        # Pygame Rect nesnesi merkezden oluşturulur
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (int(position.x), int(position.y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def get_closest_point(self, point: Vector2) -> Vector2:
        # Dikdörtgenin sınırları içinde x ve y koordinatlarını kısıtlayarak en yakın noktayı buluyoruz.
        closest_x = max(self.rect.left, min(point.x, self.rect.right))
        closest_y = max(self.rect.top, min(point.y, self.rect.bottom))
        return Vector2(closest_x, closest_y)

    def is_point_inside(self, point: Vector2) -> bool:
        return self.rect.collidepoint((point.x, point.y))

class SquareObstacle(RectangleObstacle):
    def __init__(self, position: Vector2, side: float, color: tuple[int, int, int]):
        # Kare, en ve boyu eşit olan bir dikdörtgendir.
        super().__init__(position, side, side, color)
