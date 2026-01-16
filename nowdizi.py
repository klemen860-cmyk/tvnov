import requests
import re

# ---------------- AYARLAR ----------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.nowtv.com.tr/"
}

BASE_URLS = [
    "https://www.nowtv.com.tr/4N1K/bolum/{}",
    "https://www.nowtv.com.tr/Adi-Mutluluk/bolum/{}",
    "https://www.nowtv.com.tr/Adi-Zehra/bolum/{}",
    "https://www.nowtv.com.tr/Adim-Farah/bolum/{}",
    "https://www.nowtv.com.tr/Ask-Evlilik-Bosanma/bolum/{}",
    "https://www.nowtv.com.tr/Ask-Mantik-Intikam/bolum/{}",
    "https://www.nowtv.com.tr/Ask-Yeniden/bolum/{}",
    "https://www.nowtv.com.tr/Babam-Sinifta-Kaldi/bolum/{}",
    "https://www.nowtv.com.tr/Bambaska-Biri/bolum/{}",
    "https://www.nowtv.com.tr/Baraj/bolum/{}",
    "https://www.nowtv.com.tr/Ben-Leman/bolum/{}",
    "https://www.nowtv.com.tr/Ben-Onun-Annesiyim/bolum/{}",
    "https://www.nowtv.com.tr/Benim-Hala-Umudum-Var/bolum/{}",
    "https://www.nowtv.com.tr/Bir-Deli-Ruzgar/bolum/{}",
    "https://www.nowtv.com.tr/Bir-Mucize-Olsun/bolum/{}",
    "https://www.nowtv.com.tr/Bir-Peri-Masali/bolum/{}",
    "https://www.nowtv.com.tr/Bu-Sayilmaz/bolum/{}",
    "https://www.nowtv.com.tr/Cifte-Saadet/bolum/{}",
    "https://www.nowtv.com.tr/Coban-Yildizi/bolum/{}",
    "https://www.nowtv.com.tr/Cocukluk/bolum/{}",
    "https://www.nowtv.com.tr/Darmaduman/bolum/{}",
    "https://www.nowtv.com.tr/Dayan-Yuregim/bolum/{}",
    "https://www.nowtv.com.tr/Deli-Gonul/bolum/{}",
    "https://www.nowtv.com.tr/Deniz-Yildizi/bolum/{}",
    "https://www.nowtv.com.tr/Doktor-Baska-Hayatta/bolum/{}",
    "https://www.nowtv.com.tr/Dokuz-Oguz/bolum/{}",
    "https://www.nowtv.com.tr/EGO/bolum/{}",
    "https://www.nowtv.com.tr/Elbet-Bir-Gun/bolum/{}",
    "https://www.nowtv.com.tr/Elkizi/bolum/{}",
    "https://www.nowtv.com.tr/Emanet/bolum/{}",
    "https://www.nowtv.com.tr/Esaretim-Sensin/bolum/{}",
    "https://www.nowtv.com.tr/Evlilik-Hakkinda-Her-Sey/bolum/{}",
    "https://www.nowtv.com.tr/Familya/bolum/{}",
    "https://www.nowtv.com.tr/Fatih-Harbiye/bolum/{}",
    "https://www.nowtv.com.tr/Ferhat-ile-Sirin/bolum/{}",
    "https://www.nowtv.com.tr/Gaddar/bolum/{}",
    "https://www.nowtv.com.tr/Gizli-Bahce/bolum/{}",
    "https://www.nowtv.com.tr/Gizli-Sakli/bolum/{}",
    "https://www.nowtv.com.tr/Gulcemal/bolum/{}",
    "https://www.nowtv.com.tr/Gulumse-Kaderine/bolum/{}",
    "https://www.nowtv.com.tr/Halef-Koklerin-Cagrisi/bolum/{}",
    "https://www.nowtv.com.tr/Harem/bolum/{}",
    "https://www.nowtv.com.tr/Hayat-Sevince-Guzel/bolum/{}",
    "https://www.nowtv.com.tr/Hayatimin-Sansi/bolum/{}",
    "https://www.nowtv.com.tr/Her-Yerde-Sen/bolum/{}",
    "https://www.nowtv.com.tr/Hudutsuz-Sevda/bolum/{}",
    "https://www.nowtv.com.tr/Inadina-Ask/bolum/{}",
    "https://www.nowtv.com.tr/Iyilik/bolum/{}",
    "https://www.nowtv.com.tr/Kader-Baglari/bolum/{}",
    "https://www.nowtv.com.tr/Kadim-Dostum/bolum/{}",
    "https://www.nowtv.com.tr/Kalbim-Yangin-Yeri/bolum/{}",
    "https://www.nowtv.com.tr/Kalbimdeki-Deniz/bolum/{}",
    "https://www.nowtv.com.tr/Kanunsuz-Topraklar/bolum/{}",
    "https://www.nowtv.com.tr/Karagul/bolum/{}",
    "https://www.nowtv.com.tr/Kayitdisi/bolum/{}",
    "https://www.nowtv.com.tr/Kefaret/bolum/{}",
    "https://www.nowtv.com.tr/Kiraz-Mevsimi/bolum/{}",
    "https://www.nowtv.com.tr/Kirlangic-Firtinasi/bolum/{}",
    "https://www.nowtv.com.tr/Kirli-Sepeti/bolum/{}",
    "https://www.nowtv.com.tr/Kiskanmak/bolum/{}",
    "https://www.nowtv.com.tr/Kismet/bolum/{}",
    "https://www.nowtv.com.tr/Kizil-Goncalar/bolum/{}",
    "https://www.nowtv.com.tr/Kopuk/bolum/{}",
    "https://www.nowtv.com.tr/Kordugum/bolum/{}",
    "https://www.nowtv.com.tr/Korkma-Ben-Yanindayim/bolum/{}",
    "https://www.nowtv.com.tr/Kotu-Kan/bolum/{}",
    "https://www.nowtv.com.tr/Kusursuz-Kiraci/bolum/{}",
    "https://www.nowtv.com.tr/Lale-Devri/bolum/{}",
    "https://www.nowtv.com.tr/Leyla-Hayat-Ask-Adalet/bolum/{}",
    "https://www.nowtv.com.tr/Mahkum/bolum/{}",
    "https://www.nowtv.com.tr/Masumiyet/bolum/{}",
    "https://www.nowtv.com.tr/Misafir/bolum/{}",
    "https://www.nowtv.com.tr/Mucize-Doktor/bolum/{}",
    "https://www.nowtv.com.tr/Nerdesin-Birader/bolum/{}",
    "https://www.nowtv.com.tr/No-309/bolum/{}",
    "https://www.nowtv.com.tr/Nolur-Ayrilalim/bolum/{}",
    "https://www.nowtv.com.tr/Not-Defteri/bolum/{}",
    "https://www.nowtv.com.tr/O-Hayat-Benim/bolum/{}",
    "https://www.nowtv.com.tr/Ogretmen/bolum/{}",
    "https://www.nowtv.com.tr/Ruhumun-Aynasi/bolum/{}",
    "https://www.nowtv.com.tr/Ruhun-Duymaz/bolum/{}",
    "https://www.nowtv.com.tr/Ruzgarin-Kalbi/bolum/{}",
    "https://www.nowtv.com.tr/Sahane-Hayatim/bolum/{}",
    "https://www.nowtv.com.tr/Sahtekarlar/bolum/{}",
    "https://www.nowtv.com.tr/Sakincali/bolum/{}",
    "https://www.nowtv.com.tr/Sakir-Pasa-Ailesi-Mucizeler-ve-Skandallar/bolum/{}",
    "https://www.nowtv.com.tr/Sana-Bir-Sir-Verecegim/bolum/{}",
    "https://www.nowtv.com.tr/Savasci/bolum/{}",
    "https://www.nowtv.com.tr/Sehrin-Melekleri/bolum/{}",
    "https://www.nowtv.com.tr/Sen-Benimsin/bolum/{}",
    "https://www.nowtv.com.tr/Sen-Cal-Kapimi/bolum/{}",
    "https://www.nowtv.com.tr/Senden-Daha-Guzel/bolum/{}",
    "https://www.nowtv.com.tr/Sevkat-Yerimdar/bolum/{}",
    "https://www.nowtv.com.tr/Son-Nefesime-Kadar/bolum/{}",
    "https://www.nowtv.com.tr/Son-Yaz/bolum/{}",
    "https://www.nowtv.com.tr/Tacsiz-Prenses/bolum/{}",
    "https://www.nowtv.com.tr/Tetikcinin-Oglu/bolum/{}",
    "https://www.nowtv.com.tr/Tozluyaka/bolum/{}",
    "https://www.nowtv.com.tr/Umuda-Kelepce-Vurulmaz/bolum/{}",
    "https://www.nowtv.com.tr/Unutma-Beni/bolum/{}",
    "https://www.nowtv.com.tr/Uzak-Sehrin-Masali/bolum/{}",
    "https://www.nowtv.com.tr/Vurgun/bolum/{}",
    "https://www.nowtv.com.tr/Yabani/bolum/{}",
    "https://www.nowtv.com.tr/Yalancilar-ve-Mumlari/bolum/{}",
    "https://www.nowtv.com.tr/Yalniz-Kalpler/bolum/{}",
    "https://www.nowtv.com.tr/Yasak-Elma/bolum/{}",
    "https://www.nowtv.com.tr/Yaz-Sarkisi/bolum/{}",
    "https://www.nowtv.com.tr/Yer-Gok-Ask/bolum/{}",
    "https://www.nowtv.com.tr/Yeralti/bolum/{}",
    "https://www.nowtv.com.tr/Zengin-Kiz-Fakir-Oglan/bolum/{}",
    "https://www.nowtv.com.tr/Zumruduanka/bolum/{}",
]

# ---------------- DOSYA AÇ ----------------
with open("Now_Diziler.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    # ---------------- TARAYICI ----------------
    for BASE_URL in BASE_URLS:
        episode = 1
        dizi_adi = BASE_URL.split("/")[3].replace("-", " ")

        print(f"\n📺 Dizi: {dizi_adi}")

        while True:
            url = BASE_URL.format(episode)
            print(f"  ▶ Bölüm {episode}")

            r = requests.get(url, headers=HEADERS)
            if r.status_code != 200:
                break

            html = r.text

            poster_match = re.search(r"poster:\s*'([^']+\.jpg)'", html)
            source_match = re.search(r"source:\s*'([^']+\.m3u8[^']*)'", html)

            if not poster_match or not source_match:
                break

            poster = poster_match.group(1)
            source = source_match.group(1)

            title = f"{dizi_adi} Bölüm {episode:02d}"

            f.write(
                f'#EXTINF:-1 tvg-logo="{poster}" group-title="{dizi_adi}",{title}\n{source}\n'
            )
            f.flush()  # 🔥 anında diske yaz

            episode += 1

print("\n✅ Now_Diziler.m3u OLUŞTURULDU (ANLIK YAZIM)")
