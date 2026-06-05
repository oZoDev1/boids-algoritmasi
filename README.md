# Boids Algoritması

Bu proje, Craig Reynolds tarafından 1986'da geliştirilen **Boids (Sürü)** algoritmasının Python ve Pygame kullanılarak 2 boyutlu ortamda sıfırdan simüle edilmiş halidir. Algoritma, kuş sürüleri veya balık sürüleri gibi karmaşık grup davranışlarını basit kurallarla modellemeyi sağlar. 

Projeye ayrıca dinamik engeller (Obstacle) ve bu engellerden kaçınma (Obstacle Avoidance) yeteneği de eklenmiştir.

## Demo Video

Yazdığımız algoritmamızın çalışırken çekilmiş kısa bir demosu:

<video src="BoidsVideo.mp4" controls="controls" muted="muted" style="max-width:100%;"></video>

https://github.com/user-attachments/assets/e73df52e-c77b-4595-850f-b2f6dd64213e

## Kullanılan Teknolojiler

- **Programlama Dili:** Python 3.x
- **Görselleştirme Motoru:** Pygame
- **Yaklaşım:** Nesne Yönelimli Programlama (OOP), SOLID Prensipleri
- **Mimari:** Modüler Dosya Yapısı (Boid'ler, Engeller, Simülasyon Yöneticisi ve Sabitler ayrı dosyalara ayrılmıştır)

## Boids Algoritması Davranış Kuralları (Yöntemler)

Projede Boid'lerin gerçeğe yakın sürü davranışı sergilemesi için aşağıdaki temel yöntemler ağırlıklandırılarak kullanılmıştır:

1. **Separation (Ayrılma / Çarpışmadan Kaçınma):** Sürünün içindeki her bireyin, kendisine çok yaklaşan diğer bireylerden uzaklaşarak bir nevi "kişisel alan" oluşturmasıdır.
2. **Alignment (Yön Hizalama):** Bireylerin, etraflarındaki algılama yarıçapı içerisinde bulunan diğer bireylerin ortalama hareket yönüne ve hızına uyum sağlaması kuralıdır.
3. **Obstacle Avoidance (Engelden Kaçınma):** Klasik Boids kurallarına ek olarak geliştirilen bu kuralda, Boid'ler çevrelerindeki dinamik veya statik engelleri algılar. Engele yakınlığa ters orantılı olacak şekilde sert ve hızlı manevralarla engellerden kaçarlar.

*(Not: İsteğe bağlı olan "Cohesion / Merkeze Çekilme" kuralı bu implementasyona bilinçli olarak eklenmemiştir.)*

## Kontroller & Etkileşim

Kullanıcı simülasyona gerçek zamanlı olarak müdahale edebilir:

- **Fare Sol Tık:** Tıklanan konuma rastgele bir engel (Daire, Kare, Dikdörtgen) ekler.
- **Fare Sağ Tık:** Tıklanan engeli siler.
- **B (Klavye):** Simülasyona rastgele konumda yeni bir Boid ekler.
- **O (Klavye):** Ekrana rastgele bir alanda engel üretir.
- **T (Klavye):** Otomatik rastgele engel oluşturma modunu Açıp/Kapatır.
- **SPACE (Boşluk):** Simülasyonu Duraklatır/Devam ettirir.
- **R (Klavye):** Simülasyonu varsayılan ayarlara sıfırlar.

## Nasıl Çalıştırılır?

Projeyi bilgisayarınızda çalıştırmak için:

1. Python'un bilgisayarınızda yüklü olduğundan emin olun.
2. `pygame` kütüphanesini indirin:
   ```bash
   pip install pygame
   ```
3. Proje dizinine giderek ana dosyayı çalıştırın:
   ```bash
   python main.py
   ```
