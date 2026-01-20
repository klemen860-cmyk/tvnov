import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.nowtv.com.tr/"
}

MAX_MISSED_EPISODES = 5 

# Sözlük ve BASE_URLS listesini olduğu gibi koruyoruz
TURKCE_ISIMLER = {
    "Adi-Mutluluk": "Adı Mutluluk", "Adi-Zehra": "Adı Zehra", "Adim-Farah": "Adım Farah",
    "Ask-Evlilik-Bosanma": "Aşk Evlilik Boşanma", "Ask-Mantik-Intikam": "Aşk Mantık İntikam",
    "Ask-Yeniden": "Aşk Yeniden", "Babam-Sinifta-Kaldi": "Babam Sınıfta Kaldı",
    "Bambaska-Biri": "Bambaşka Biri", "Bir-Deli-Ruzgar": "Bir Deli Rüzgar",
    "Bir-Mucize-Olsun": "Bir Mucize Olsun", "Bir-Peri-Masali": "Bir Peri Masalı",
    "Cifte-Saadet": "Çifte Saadet", "Coban-Yildizi": "Çoban Yıldızı",
    "Cocukluk": "Çocukluk", "Deli-Gonul": "Deli Gönül", "Deniz-Yildizi": "Deniz Yıldızı",
    "Doktor-Baska-Hayatta": "Doktor Başka Hayatta", "Dokuz-Oguz": "Dokuz Oğuz",
    "Elbet-Bir-Gun": "Elbet Bir Gün", "Elkizi": "Elkızı", "Esaretim-Sensin": "Esaretim Sensin",
    "Evlilik-Hakkinda-Her-Sey": "Evlilik Hakkında Her Şey", "Fatih-Harbiye": "Fatih Harbiye",
    "Ferhat-ile-Sirin": "Ferhat ile Şirin", "Gizli-Bahce": "Gizli Bahçe",
    "Gizli-Sakli": "Gizli Saklı", "Gulcemal": "Gülcemal", "Gulumse-Kaderine": "Gülümse Kaderine",
    "Halef-Koklerin-Cagrisi": "Halef Köklerin Çağrısı", "Hayat-Sevince-Guzel": "Hayat Sevince Güzel",
    "Hayatimin-Sansi": "Hayatımın Şansı", "Her-Yerde-Sen": "Her Yerde Sen",
    "Inadina-Ask": "İnadına Aşk", "Iyilik": "İyilik", "Kader-Baglari": "Kader Bağları",
    "Kadim-Dostum": "Kadim Dostum", "Kalbim-Yangin-Yeri": "Kalbim Yangın Yeri",
    "Kanunsuz-Topraklar": "Kanunsuz Topraklar", "Karagul": "Karagül", "Kayitdisi": "Kayıtdışı",
    "Kiraz-Mevsimi": "Kiraz Mevsimi", "Kirlangic-Firtinasi": "Kırlangıç Fırtınası",
    "Kirli-Sepeti": "Kirli Sepeti", "Kiskanmak": "Kıskanmak", "Kismet": "Kısmet",
    "Kizil-Goncalar": "Kızıl Goncalar", "Kopuk": "Kopuk", "Kordugum": "Kördüğüm",
    "Korkma-Ben-Yanindayim": "Korkma Ben Yanındayım", "Kotu-Kan": "Kötü Kan",
    "Kusursuz-Kiraci": "Kusursuz Kiracı", "Lale-Devri": "Lale Devri",
    "Leyla-Hayat-Ask-Adalet": "Leyla Hayat Aşk Adalet", "Mahkum": "Mahkum",
    "Masumiyet": "Masumiyet", "Mucize-Doktor": "Mucize Doktor", "Nerdesin-Birader": "Nerdesin Birader",
    "No-309": "No: 309", "Nolur-Ayrilalim": "Nolur Ayrılalım", "Not-Defteri": "Not Defteri",
    "O-Hayat-Benim": "O Hayat Benim", "Ogretmen": "Öğretmen", "Ruhumun-Aynasi": "Ruhumun Aynası",
    "Ruhun-Duymaz": "Ruhun Duymaz", "Ruzgarin-Kalbi": "Rüzgarın Kalbi",
    "Sahane-Hayatim": "Şahane Hayatım", "Sakir-Pasa-Ailesi-Mucizeler-ve-Skandallar": "Şakir Paşa Ailesi",
    "Sana-Bir-Sir-Verecegim": "Sana Bir Sır Vereceğim", "Savasci": "Savaşçı",
    "Sehrin-Melekleri": "Şehrin Melekleri", "Sen-Benimsin": "Sen Benimsin",
    "Sen-Cal-Kapimi": "Sen Çal Kapımı", "Senden-Daha-Guzel": "Senden Daha Güzel",
    "Sevkat-Yerimdar": "Şevkat Yerimdar", "Son-Nefesime-Kadar": "Son Nefesime Kadar",
    "Son-Yaz": "Son Yaz", "Tacsiz-Prenses": "Taçsız Prenses", "Tetikcinin-Oglu": "Tetikçinin Oğlu",
    "Umuda-Kelepce-Vurulmaz": "Umuda Kelepçe Vurulmaz", "Uzak-Sehrin-Masali": "Uzak Şehrin Masalı",
    "Yalancilar-ve-Mumlari": "Yalancılar ve Mumları", "Yalniz-Kalpler": "Yalnız Kalpler",
    "Yaz-Sarkisi": "Yaz Şarkısı", "Yer-Gok-Ask": "Yer Gök Aşk", "Yeralti": "Yeraltı",
    "Zengin-Kiz-Fakir-Oglan": "Zengin Kız Fakir Oğlan", "Zumruduanka": "Zümrüdüanka"
}

BASE_URLS = [
    "https://www.nowtv.com.tr/4N1K/bolum/{}", "https://www.nowtv.com.tr/Adi-Mutluluk/bolum/{}",
    "https://www.nowtv.com.tr/Adi-Zehra/bolum/{}", "https://www.nowtv.com.tr/Adim-Farah/bolum/{}",
    "https://www.nowtv.com.tr/Ask-Evlilik-Bosanma/bolum/{}", "https://www.nowtv.com.tr/Ask-Mantik-Intikam/bolum/{}",
    "https://www.nowtv.com.tr/Ask-Yeniden/bolum/{}", "https://www.nowtv.com.tr/Babam-Sinifta-Kaldi/bolum/{}",
    "https://www.nowtv.com.tr/Bambaska-Biri/bolum/{}", "https://www.nowtv.com.tr/Baraj/bolum/{}",
    "https://www.nowtv.com.tr/Ben-Leman/bolum/{}", "https://www.nowtv.com.tr/Ben-Onun-Annesiyim/bolum/{}",
    "https://www.nowtv.com.tr/Benim-Hala-Umudum-Var/bolum/{}", "https://www.nowtv.com.tr/Bir-Deli-Ruzgar/bolum/{}",
    "https://www.nowtv.com.tr/Bir-Mucize-Olsun/bolum/{}", "https://www.nowtv.com.tr/Bir-Peri-Masali/bolum/{}",
    "https://www.nowtv.com.tr/Bu-Sayilmaz/bolum/{}", "https://www.nowtv.com.tr/Cifte-Saadet/bolum/{}",
    "https://www.nowtv.com.tr/Coban-Yildizi/bolum/{}", "https://www.nowtv.com.tr/Cocukluk/bolum/{}",
    "https://www.nowtv.com.tr/Darmaduman/bolum/{}", "https://www.nowtv.com.tr/Dayan-Yuregim/bolum/{}",
    "https://www.nowtv.com.tr/Deli-Gonul/bolum/{}", "https://www.nowtv.com.tr/Deniz-Yildizi/bolum/{}",
    "https://www.nowtv.com.tr/Doktor-Baska-Hayatta/bolum/{}", "https://www.nowtv.com.tr/Dokuz-Oguz/bolum/{}",
    "https://www.nowtv.com.tr/EGO/bolum/{}", "https://www.nowtv.com.tr/Elbet-Bir-Gun/bolum/{}",
    "https://www.nowtv.com.tr/Elkizi/bolum/{}", "https://www.nowtv.com.tr/Emanet/bolum/{}",
    "https://www.nowtv.com.tr/Esaretim-Sensin/bolum/{}", "https://www.nowtv.com.tr/Evlilik-Hakkinda-Her-Sey/bolum/{}",
    "https://www.nowtv.com.tr/Familya/bolum/{}", "https://www.nowtv.com.tr/Fatih-Harbiye/bolum/{}",
    "https://www.nowtv.com.tr/Ferhat-ile-Sirin/bolum/{}", "https://www.nowtv.com.tr/Gaddar/bolum/{}",
    "https://www.nowtv.com.tr/Gizli-Bahce/bolum/{}", "https://www.nowtv.com.tr/Gizli-Sakli/bolum/{}",
    "https://www.nowtv.com.tr/Gulcemal/bolum/{}", "https://www.nowtv.com.tr/Gulumse-Kaderine/bolum/{}",
    "https://www.nowtv.com.tr/Halef-Koklerin-Cagrisi/bolum/{}", "https://www.nowtv.com.tr/Harem/bolum/{}",
    "https://www.nowtv.com.tr/Hayat-Sevince-Guzel/bolum/{}", "https://www.nowtv.com.tr/Hayatimin-Sansi/bolum/{}",
    "https://www.nowtv.com.tr/Her-Yerde-Sen/bolum/{}", "https://www.nowtv.com.tr/Hudutsuz-Sevda/bolum/{}",
    "https://www.nowtv.com.tr/Inadina-Ask/bolum/{}", "https://www.nowtv.com.tr/Iyilik/bolum/{}",
    "https://www.nowtv.com.tr/Kader-Baglari/bolum/{}", "https://www.nowtv.com.tr/Kadim-Dostum/bolum/{}",
    "https://www.nowtv.com.tr/Kalbim-Yangin-Yeri/bolum/{}", "https://www.nowtv.com.tr/Kalbimdeki-Deniz/bolum/{}",
    "https://www.nowtv.com.tr/Kanunsuz-Topraklar/bolum/{}", "https://www.nowtv.com.tr/Karagul/bolum/{}",
    "https://www.nowtv.com.tr/Kayitdisi/bolum/{}", "https://www.nowtv.com.tr/Kefaret/bolum/{}",
    "https://www.nowtv.com.tr/Kiraz-Mevsimi/bolum/{}", "https://www.nowtv.com.tr/Kirlangic-Firtinasi/bolum/{}",
    "https://www.nowtv.com.tr/Kirli-Sepeti/bolum/{}", "https://www.nowtv.com.tr/Kiskanmak/bolum/{}",
    "https://www.nowtv.com.tr/Kismet/bolum/{}", "https://www.nowtv.com.tr/Kizil-Goncalar/bolum/{}",
    "https://www.nowtv.com.tr/Kopuk/bolum/{}", "https://www.nowtv.com.tr/Kordugum/bolum/{}",
    "https://www.nowtv.com.tr/Korkma-Ben-Yanindayim/bolum/{}", "https://www.nowtv.com.tr/Kotu-Kan/bolum/{}",
    "https://www.nowtv.com.tr/Kusursuz-Kiraci/bolum/{}", "https://www.nowtv.com.tr/Lale-Devri/bolum/{}",
    "https://www.nowtv.com.tr/Leyla-Hayat-Ask-Adalet/bolum/{}", "https://www.nowtv.com.tr/Mahkum/bolum/{}",
    "https://www.nowtv.com.tr/Masumiyet/bolum/{}", "https://www.nowtv.com.tr/Misafir/bolum/{}",
    "https://www.nowtv.com.tr/Mucize-Doktor/bolum/{}", "https://www.nowtv.com.tr/Nerdesin-Birader/bolum/{}",
    "https://www.nowtv.com.tr/No-309/bolum/{}", "https://www.nowtv.com.tr/Nolur-Ayrilalim/bolum/{}",
    "https://www.nowtv.com.tr/Not-Defteri/bolum/{}", "https://www.nowtv.com.tr/O-Hayat-Benim/bolum/{}",
    "https://www.nowtv.com.tr/Ogretmen/bolum/{}", "https://www.nowtv.com.tr/Ruhumun-Aynasi/bolum/{}",
    "https://www.nowtv.com.tr/Ruhun-Duymaz/bolum/{}", "https://www.nowtv.com.tr/Ruzgarin-Kalbi/bolum/{}",
    "https://www.nowtv.com.tr/Sahane-Hayatim/bolum/{}", "https://www.nowtv.com.tr/Sahtekarlar/bolum/{}",
    "https://www.nowtv.com.tr/Sakincali/bolum/{}", "https://www.nowtv.com.tr/Sakir-Pasa-Ailesi-Mucizeler-ve-Skandallar/bolum/{}",
    "https://www.nowtv.com.tr/Sana-Bir-Sir-Verecegim/bolum/{}", "https://www.nowtv.com.tr/Savasci/bolum/{}",
    "https://www.nowtv.com.tr/Sehrin-Melekleri/bolum/{}", "https://www.nowtv.com.tr/Sen-Benimsin/bolum/{}",
    "https://www.nowtv.com.tr/Sen-Cal-Kapimi/bolum/{}", "https://www.nowtv.com.tr/Senden-Daha-Guzel/bolum/{}",
    "https://www.nowtv.com.tr/Sevkat-Yerimdar/bolum/{}", "https://www.nowtv.com.tr/Son-Nefesime-Kadar/bolum/{}",
    "https://www.nowtv.com.tr/Son-Yaz/bolum/{}", "https://www.nowtv.com.tr/Tacsiz-Prenses/bolum/{}",
    "https://www.nowtv.com.tr/Tetikcinin-Oglu/bolum/{}", "https://www.nowtv.com.tr/Tozluyaka/bolum/{}",
    "https://www.nowtv.com.tr/Umuda-Kelepce-Vurulmaz/bolum/{}", "https://www.nowtv.com.tr/Unutma-Beni/bolum/{}",
    "https://www.nowtv.com.tr/Uzak-Sehrin-Masali/bolum/{}", "https://www.nowtv.com.tr/Vurgun/bolum/{}",
    "https://www.nowtv.com.tr/Yabani/bolum/{}", "https://www.nowtv.com.tr/Yalancilar-ve-Mumlari/bolum/{}",
    "https://www.nowtv.com.tr/Yalniz-Kalpler/bolum/{}", "https://www.nowtv.com.tr/Yasak-Elma/bolum/{}",
    "https://www.nowtv.com.tr/Yaz-Sarkisi/bolum/{}", "https://www.nowtv.com.tr/Yer-Gok-Ask/bolum/{}",
    "https://www.nowtv.com.tr/Yeralti/bolum/{}", "https://www.nowtv.com.tr/Zengin-Kiz-Fakir-Oglan/bolum/{}",
    "https://www.nowtv.com.tr/Zumruduanka/bolum/{}"
]

def dizi_tara(base_url, session):
    """Her bir dizi için ayrı çalışacak olan fonksiyon"""
    results = []
    episode = 1
    missed_count = 0
    url_slug = base_url.split("/")[3]
    dizi_adi = TURKCE_ISIMLER.get(url_slug, url_slug.replace("-", " "))
    
    while missed_count < MAX_MISSED_EPISODES:
        urls_to_check = [base_url.format(episode), base_url.format(f"{episode}/ozel-bolum")]
        found_in_round = False
        
        for url in urls_to_check:
            try:
                # Session kullanarak bağlantıyı açık tutuyoruz
                r = session.get(url, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    html = r.text
                    source_match = re.search(r"source:\s*['\"]([^'\"]+\.m3u8[^'\"]*)['\"]", html)
                    
                    if source_match:
                        poster_match = re.search(r"poster:\s*['\"]([^'\"]+\.(?:jpg|png)[^'\"]*)['\"]", html)
                        poster = poster_match.group(1) if poster_match else ""
                        source = source_match.group(1)
                        label = f"{dizi_adi} - Bölüm {episode}" if "ozel-bolum" not in url else f"{dizi_adi} - Bölüm {episode} (Özel)"
                        
                        entry = f'#EXTINF:-1 tvg-logo="{poster}" group-title="{dizi_adi}",{label}\n{source}\n'
                        results.append(entry)
                        print(f"{label} OK")
                        found_in_round = True
            except Exception:
                pass
        
        if found_in_round:
            missed_count = 0
        else:
            missed_count += 1
        
        episode += 1
    return results

def main():
    # Dosyayı tek seferde açıp yazmak için sonuçları toplayacağız
    with open("Now_Diziler.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        # requests.Session() ile TCP bağlantısını optimize ediyoruz
        with requests.Session() as session:
            # max_workers=15 aynı anda 15 dizinin taranacağı anlamına gelir
            with ThreadPoolExecutor(max_workers=15) as executor:
                # Tüm dizileri havuzumuza ekliyoruz
                future_to_url = {executor.submit(dizi_tara, url, session): url for url in BASE_URLS}
                
                for future in future_to_url:
                    try:
                        dizi_sonuclari = future.result()
                        for satir in dizi_sonuclari:
                            f.write(satir)
                            f.flush()
                    except Exception as e:
                        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- Tarama {time.time() - start_time:.2f} saniyede tamamlandı ---")