import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- AYARLAR ---
BASE_URL = "https://www.hdfilmizle.life/yabanci-dizi-izle-3/page"
M3U_FILE = "hd_diziler.m3u"
PAGE_TRACKER = "last_page.txt"

def append_to_m3u(entry_text):
    """Bulduğu an dosyaya yazar ve kapatır (Anında kayıt)."""
    file_exists = os.path.exists(M3U_FILE)
    with open(M3U_FILE, "a", encoding="utf-8") as f:
        if not file_exists or os.stat(M3U_FILE).st_size == 0:
            f.write("#EXTM3U\n")
        f.write(entry_text)
        f.flush() # İşletim sistemi tamponunu zorla boşaltır

def get_last_page():
    if os.path.exists(PAGE_TRACKER):
        try:
            with open(PAGE_TRACKER, "r") as f:
                return int(f.read().strip())
        except: return 1
    return 1

def save_last_page(page):
    with open(PAGE_TRACKER, "w") as f:
        f.write(str(page))

def run_bot():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Mevcut m3u dosyasını oku (Tekrar kaydı önlemek için)
    saved_urls = set()
    if os.path.exists(M3U_FILE):
        with open(M3U_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("http"):
                    saved_urls.add(line.strip())

    page_num = get_last_page()

    try:
        while True:
            print(f"\n--- 📄 SAYFA {page_num} İŞLENİYOR ---")
            driver.get(f"{BASE_URL}/{page_num}/")
            time.sleep(2)
            
            dizi_links = [a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, "#moviesListResult a.poster")]
            if not dizi_links: 
                print("🏁 Liste bitti.")
                break

            for main_link in dizi_links:
                print(f"📂 Dizi: {main_link}")
                driver.get(main_link)
                time.sleep(2)

                # Dizi ana sayfasından logo ve ismi al
                try:
                    raw_name = driver.title.split('|')[0].split('izle')[0].strip()
                    logo = driver.find_element(By.CSS_SELECTOR, 'meta[property="og:image"]').get_attribute('content')
                except: logo = ""

                # Bölüm linklerini topla ve sırala (S01E01, S01E02...)
                all_eps = []
                try:
                    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/sezon-"][href*="/bolum-"]')
                    for l in links:
                        href = l.get_attribute('href')
                        if href and href not in all_eps:
                            all_eps.append(href)
                    all_eps.sort(key=lambda x: [int(y) for y in re.search(r'sezon-(\d+)/bolum-(\d+)', x).groups()])
                except: continue

                # Bölümleri çek ve ANINDA dosyaya yaz
                for ep_url in all_eps:
                    try:
                        # İsimden kontrol (Daha hızlıdır)
                        match_info = re.search(r'sezon-(\d+)/bolum-(\d+)', ep_url)
                        s, e = match_info.groups()
                        display_title = f"{raw_name} S{int(s):02d}E{int(e):02d}"

                        # Eğer bu isim veya URL zaten varsa atla
                        if any(display_title in line for line in saved_urls): continue 

                        driver.get(ep_url)
                        # vidrame ID'sini bulduğumuz an m3u8'i yapıştır
                        match = re.search(r'vidrame\.pro/vr/([a-zA-Z0-9]+)', driver.page_source)
                        
                        if match:
                            v_id = match.group(1)
                            final_url = f"https://vidrame.pro/vr/get/{v_id}/master.m3u8"
                            
                            if final_url not in saved_urls:
                                entry = f'#EXTINF:-1 tvg-logo="{logo}" group-title="DİZİLER",{display_title}\n{final_url}\n'
                                append_to_m3u(entry) # ANINDA YAZAR
                                saved_urls.add(final_url)
                                print(f"  ✅ {display_title} KAYDEDİLDİ")
                    except: continue

            page_num += 1
            save_last_page(page_num)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()