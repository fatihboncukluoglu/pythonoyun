import random
import os # Ekranı temizlemek için

# Tahta boyutu (örneğin 3x3 için 3)
BOYUT = 3
BOS_KARE = 0 # Boş kareyi temsil eden değer

def tahta_olustur():
    """Çözülmüş bir bulmaca tahtası oluşturur."""
    sayilar = list(range(1, BOYUT * BOYUT))
    tahta = []
    for i in range(BOYUT):
        satir = []
        for j in range(BOYUT):
            satir.append(sayilar.pop(0) if sayilar else BOS_KARE)
        tahta.append(satir)
    return tahta

def tahtayi_goster(tahta):
    """Tahtayı konsolda gösterir."""
    print("-" * (BOYUT * 4 + 1)) # Üst çizgi
    for satir in tahta:
        print("| ", end="")
        for hucre in satir:
            if hucre == BOS_KARE:
                print("  | ", end="") # Boş kare için iki boşluk
            else:
                print(f"{hucre:2d}| ", end="") # Sayılar için formatlı yazdırma
        print()
        print("-" * (BOYUT * 4 + 1)) # Ara ve alt çizgiler

def bos_kareyi_bul(tahta):
    """Boş karenin (satır, sütun) konumunu bulur."""
    for r, satir in enumerate(tahta):
        for c, hucre in enumerate(satir):
            if hucre == BOS_KARE:
                return r, c
    return None # Teorik olarak olmamalı

def gecerli_hareketler(tahta):
    """Boş karenin yapabileceği geçerli hareketleri (komşu koordinatları) döndürür."""
    r, c = bos_kareyi_bul(tahta)
    hareketler = []
    # Yukarı
    if r > 0:
        hareketler.append((r - 1, c))
    # Aşağı
    if r < BOYUT - 1:
        hareketler.append((r + 1, c))
    # Sol
    if c > 0:
        hareketler.append((r, c - 1))
    # Sağ
    if c < BOYUT - 1:
        hareketler.append((r, c + 1))
    return hareketler

def tahtayi_karistir(tahta, karistirma_sayisi=100):
    """Tahtayı çözülebilir bir şekilde karıştırır."""
    import copy
    gecici_tahta = copy.deepcopy(tahta) # Orijinal tahtayı bozmamak için kopya al
    
    for _ in range(karistirma_sayisi):
        bos_r, bos_c = bos_kareyi_bul(gecici_tahta)
        mumkun_hareket_yonleri = [] # Boş karenin gidebileceği yönler
        
        # Yukarı
        if bos_r > 0: mumkun_hareket_yonleri.append((-1, 0))
        # Aşağı
        if bos_r < BOYUT - 1: mumkun_hareket_yonleri.append((1, 0))
        # Sol
        if bos_c > 0: mumkun_hareket_yonleri.append((0, -1))
        # Sağ
        if bos_c < BOYUT - 1: mumkun_hareket_yonleri.append((0, 1))
        
        if not mumkun_hareket_yonleri: # Bu durum olmamalı ama güvenlik için
            continue

        dr, dc = random.choice(mumkun_hareket_yonleri)
        
        hedef_r, hedef_c = bos_r + dr, bos_c + dc
        
        # Boş kare ile hedef kareyi değiştir
        gecici_tahta[bos_r][bos_c], gecici_tahta[hedef_r][hedef_c] = \
            gecici_tahta[hedef_r][hedef_c], gecici_tahta[bos_r][bos_c]
            
    return gecici_tahta


def hareket_et(tahta, hareket_edilecek_sayi):
    """Belirtilen sayıyı boş kareye taşır (eğer geçerliyse)."""
    bos_r, bos_c = bos_kareyi_bul(tahta)
    
    # Hareket ettirilecek sayının konumunu bul
    sayi_r, sayi_c = -1, -1
    for r_idx, satir in enumerate(tahta):
        for c_idx, hucre in enumerate(satir):
            if hucre == hareket_edilecek_sayi:
                sayi_r, sayi_c = r_idx, c_idx
                break
        if sayi_r != -1:
            break
            
    if sayi_r == -1: # Sayı tahtada bulunamadı (bu olmamalı)
        print(f"{hareket_edilecek_sayi} sayısı tahtada bulunamadı.")
        return False

    # Sayı boş kareye komşu mu kontrol et
    if (abs(bos_r - sayi_r) == 1 and bos_c == sayi_c) or \
       (abs(bos_c - sayi_c) == 1 and bos_r == sayi_r):
        # Komşu ise yer değiştir
        tahta[bos_r][bos_c], tahta[sayi_r][sayi_c] = tahta[sayi_r][sayi_c], tahta[bos_r][bos_c]
        return True
    else:
        print(f"{hareket_edilecek_sayi} sayısı boş kareye komşu değil. Geçersiz hareket.")
        return False

def cozuldumu(tahta):
    """Tahtanın çözülüp çözülmediğini kontrol eder."""
    beklenen_tahta = tahta_olustur()
    return tahta == beklenen_tahta

def ekran_temizle():
    """Konsol ekranını temizler."""
    os.system('cls' if os.name == 'nt' else 'clear')

def oyun():
    """Ana oyun döngüsü."""
    tahta = tahta_olustur()
    tahta = tahtayi_karistir(tahta, karistirma_sayisi=BOYUT * BOYUT * 10) # Daha iyi karışması için
    
    hamle_sayisi = 0

    while True:
        ekran_temizle()
        print("Kaydırmalı Bulmaca Oyunu!")
        print(f"Hamle Sayısı: {hamle_sayisi8
        }")
        tahtayi_goster(tahta)

        if cozuldumu(tahta):
            print(f"Tebrikler! {hamle_sayisi} hamlede bulmacayı çözdünüz!")
            break

        try:
            girdi = input("Hangi sayıyı boş kareye taşımak istersiniz? (Çıkmak için 'q'): ")
            if girdi.lower() == 'q':
                print("Oyundan çıkılıyor...")
                break
            
            hareket_edilecek_sayi = int(girdi)
            if not (1 <= hareket_edilecek_sayi < BOYUT * BOYUT):
                print(f"Lütfen 1 ile {BOYUT * BOYUT - 1} arasında bir sayı girin.")
                input("Devam etmek için Enter'a basın...")
                continue

            if hareket_et(tahta, hareket_edilecek_sayi):
                hamle_sayisi += 1
            else:
                input("Devam etmek için Enter'a basın...")


        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin veya çıkmak için 'q' yazın.")
            input("Devam etmek için Enter'a basın...")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            input("Devam etmek için Enter'a basın...")


if __name__ == "__main__":
    oyun()