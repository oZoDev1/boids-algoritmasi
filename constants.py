"""
constants.py
Bu dosya simülasyonda kullanılan sabit değerleri (Magic Numbers) içerir.
"""

# Ekran Ayarları
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60

# Renkler (RGB formatında)
COLOR_BACKGROUND = (20, 20, 30)
COLOR_BOID = (50, 150, 255)       # Mavi tonu
COLOR_OBSTACLE = (200, 50, 50)    # Kırmızı tonu

# Boid Parametreleri
BOID_START_COUNT = 50
BOID_MAX_SPEED = 4.0
BOID_MAX_FORCE = 0.1

# Algılama ve Davranış Yarıçapları
PERCEPTION_RADIUS = 50.0
OBSTACLE_AVOIDANCE_RADIUS = 80.0

# Engeller
OBSTACLE_MIN_SIZE = 20
OBSTACLE_MAX_SIZE = 60
