

---

# Lab: การแนะนำ Web Scraping ด้วย Python

## 🎯 วัตถุประสงค์การเรียนรู้

หลังจากทำ Lab นี้เสร็จ นักศึกษาจะสามารถ:

* เข้าใจแนวคิดพื้นฐานของ Web Scraping และข้อพิจารณาด้านจริยธรรม/กฎหมาย
* ใช้ไลบรารี `requests` เพื่อดาวน์โหลดเนื้อหาเว็บเพจ
* ใช้ไลบรารี `BeautifulSoup4` เพื่อแปลง (parse) และดึงข้อมูลจาก HTML
* เขียนสคริปต์ scraper พื้นฐานที่ดึงข้อมูลจากเว็บไซต์จริง
* แก้ปัญหา (debug) ที่พบทั่วไปในการทำ web scraping

## ⚠️ ข้อพิจารณาด้านจริยธรรมและกฎหมาย (อ่านก่อนเริ่ม)

ก่อนทำ scraping เว็บไซต์ใดๆ ต้องตรวจสอบเสมอ:

1. **robots.txt** — ไฟล์ที่ระบุว่าเว็บไซต์อนุญาตให้ bot เข้าถึงส่วนใดได้บ้าง ตรวจสอบได้ที่ `https://[ชื่อเว็บไซต์]/robots.txt`
2. **Terms of Service (ข้อกำหนดการให้บริการ)** — บางเว็บไซต์ห้าม scraping โดยชัดแจ้ง
3. **Rate Limiting** — ไม่ควรส่ง requests รัวๆ จนเป็นภาระต่อเซิร์ฟเวอร์
4. **ทรัพย์สินทางปัญญา** — ข้อมูลที่ scrape มาอาจมีลิขสิทธิ์ ห้ามนำไปใช้ในทางละเมิด

> ในเว็บไซต์ที่มี API ให้ใช้งาน **ควรใช้ API แทนการ scrape เสมอ** เพราะเสถียรกว่าและถูกต้องตามกฎกว่า

Lab นี้ใช้เว็บไซต์ [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) ซึ่งเป็นเว็บไซต์เพื่อการศึกษาและอนุญาตให้เข้าถึงเนื้อหาได้แบบเปิด เหมาะสำหรับการฝึกฝนโดยไม่มีปัญหาด้านจริยธรรม

---

## ส่วนที่ 1: การเตรียมความพร้อม

> **หมายเหตุ:** ใครที่มี github desktop และ vscode ที่มี python สามารถข้าม Prerequisites (สิ่งที่ต้องมีก่อนเริ่ม) ได้ และให้เปิด repo อันเก่ามาทำต่อ โดยสร้างโฟลเดอร์ week 7

### 🛠️ Prerequisites (สิ่งที่ต้องมีก่อนเริ่ม)

* Python 3.8 หรือสูงกว่า ([ดาวน์โหลด](https://www.python.org/downloads/))
* Git ([ดาวน์โหลด](https://git-scm.com/downloads))
* Text Editor เช่น VS Code

ตรวจสอบเวอร์ชัน Python:

```bash
python --version

```

---

## ส่วนที่ 2: ขั้นตอนการ Setup (📦)

**1. Clone หรือสร้างโปรเจกต์**

```bash
git clone https://github.com/[YOUR_USERNAME]/web-scraping-intro.git
cd web-scraping-intro

```

**2. สร้าง Virtual Environment **
## (ข้อ 2 ห้ามข้ามเด็ดขาด)
การใช้ virtual environment ช่วยแยก dependencies ของโปรเจกต์นี้ออกจากโปรเจกต์อื่นในเครื่อง

* **Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1

```


⚠️ **หากเจอ error:** `... cannot be loaded because running scripts is disabled on this system`
ให้เปิด PowerShell แบบ Run as Administrator แล้วรัน (แนะนำให้เปิดก่อนรัน `venv\Scripts\Activate.ps1` ทุกครั้ง เพื่อความสะดวกและไม่ error):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```


พิมพ์ `Y` ยืนยัน แล้วเปิด PowerShell ใหม่และลอง activate อีกครั้ง
* **macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```



เมื่อ activate สำเร็จ จะเห็น `(venv)` ปรากฏหน้า prompt

**3. ติดตั้ง Dependencies**

```bash
pip install requests beautifulsoup4

```

ตรวจสอบว่าติดตั้งสำเร็จ:

```bash
pip list

```

ควรเห็น `requests` และ `beautifulsoup4` ในรายการ

**4. โครงสร้างไฟล์ที่ต้องมี (สร้างเป็นไฟล์เปล่าไว้ก่อน)**

```text
web-scraping-intro/
├── src/
│   ├── __init__.py
│   └── scraper.py
├── main.py
├── .gitignore
└── README.md

```

---

## ส่วนที่ 3: ขั้นตอนการทำ Lab

**Step 1: สร้างไฟล์ `src/__init__.py**`
ไฟล์เปล่า ใช้บ่งบอกว่า `src` เป็น Python package

**Step 2: เขียน `src/scraper.py**`
สร้างคลาส `SimpleWebScraper` ที่มี 2 เมธอดหลัก:

* `_get_html_content()` — ดาวน์โหลด HTML ด้วย `requests.get()` พร้อม error handling
* `scrape_main_titles()` — แปลง HTML ด้วย BeautifulSoup แล้วดึงชื่อหนังสือและชื่อบท

โค้ด `src/scraper.py` (สามารถก็อปวางได้เลย):

```python
# web-scraping-intro/src/scraper.py
import requests
from bs4 import BeautifulSoup


class SimpleWebScraper:
    """
    คลาสสำหรับรวมฟังก์ชันการทำ web scraping พื้นฐาน
    ปรับให้ใช้กับเว็บไซต์ Automate the Boring Stuff (3rd Edition)
    """

    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """
        ดาวน์โหลดเนื้อหา HTML จาก URL เป้าหมาย
        มีการตรวจสอบข้อผิดพลาดพื้นฐาน
        """
        print(f"กำลังดาวน์โหลดเนื้อหาจาก: {self.target_url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.target_url, headers=headers, timeout=30)
            response.raise_for_status()
            print("ดาวน์โหลดเนื้อหาสำเร็จ")
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"เกิดข้อผิดพลาด HTTP: {e} - Status Code: {e.response.status_code}")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"เกิดข้อผิดพลาดการเชื่อมต่อ: {e} - ไม่สามารถเชื่อมต่อกับ {self.target_url}")
            return None
        except requests.exceptions.Timeout:
            print("การ request หมดเวลา")
            return None
        except requests.exceptions.RequestException as e:
            print(f"เกิดข้อผิดพลาด request ที่ไม่คาดคิด: {e}")
            return None

    def scrape_main_titles(self):
        """
        ดึงชื่อหนังสือหลักและรายการชื่อบทต่างๆ
        จากหน้าแรกของ Automate the Boring Stuff (3rd Edition)
        """
        html_content = self._get_html_content()
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # --- ดึงชื่อหนังสือ ---
        # โครงสร้าง: <article> -> <header> -> <h1 itemprop="name headline">
        book_title = "ไม่พบชื่อหนังสือ"
        article_tag = soup.find('article')
        if article_tag:
            header_tag = article_tag.find('header')
            if header_tag:
                h1_tag = header_tag.find('h1')
                if h1_tag:
                    book_title = h1_tag.get_text(strip=True)

        # --- ดึงรายการชื่อบท ---
        # โครงสร้าง: <div class="content-body"> -> <ul> -> <li> -> <a.
        chapter_titles = []
        content_body = soup.find('div', class_='content-body')
        if content_body:
            chapter_links = content_body.select('ul li a')
            for link in chapter_links:
                title = link.get_text(strip=True)
                if title:
                    chapter_titles.append(title)

        return {
            "book_title": book_title,
            "chapter_titles": chapter_titles
        }

```

**Step 4: เขียน `main.py` (สามารถก็อปวางได้เลย)**

```python
# web-scraping-intro/main.py
import sys
import os

# เพิ่มไดเรกทอรี 'src' เข้าไปใน Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scraper import SimpleWebScraper


def main():
    """
    จุดเริ่มต้นหลักสำหรับแอปพลิเคชัน web scraping อย่างง่าย
    """
    target_url = "https://automatetheboringstuff.com/3e/"
    scraper = SimpleWebScraper(target_url)

    scraped_data = scraper.scrape_main_titles()

    if scraped_data:
        print("\n--- ข้อมูลที่ Scrape ได้ ---")
        print(f"ชื่อหนังสือ: {scraped_data['book_title']}")
        print("\nชื่อบทต่างๆ:")
        if scraped_data['chapter_titles']:
            for i, title in enumerate(scraped_data['chapter_titles']):
                print(f"{i+1}. {title}")
        else:
            print("ไม่พบชื่อบทใดๆ")
        print("--------------------")
    else:
        print("ไม่สามารถ scrape ข้อมูลได้")


if __name__ == "__main__":
    main()

```

**Step 5: รันและทดสอบ**
(อย่าลืมให้สิทธ์ Admin ก่อนและ เปิด venv และเช็คตำแหน่ง directory ก่อนรันเสมอ)

```bash
python main.py

```

**ผลลัพธ์ที่คาดหวัง:**

```text
กำลังดาวน์โหลดเนื้อหาจาก: https://automatetheboringstuff.com/3e/
ดาวน์โหลดเนื้อหาสำเร็จ

--- ข้อมูลที่ Scrape ได้ ---
ชื่อหนังสือ: 3rd Edition

ชื่อบทต่างๆ:
1. Introduction
2. Chapter 1 – Python Basics
...

```

---

## 🔧 การแก้ไขปัญหาที่พบทั่วไป (Troubleshooting)

| ปัญหา | สาเหตุที่เป็นไปได้ | วิธีแก้ |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'requests'` | ยังไม่ activate venv หรือยังไม่ติดตั้ง package | รัน `pip install requests beautifulsoup4` อีกครั้งใน venv ที่ activate แล้ว |
| `403 Forbidden` | เว็บไซต์บล็อก request ที่ไม่มี User-Agent | เพิ่ม header `User-Agent` ใน `requests.get()` |
| `AttributeError: 'NoneType' object has no attribute ...` | `find()` หาไม่เจอ element ที่ต้องการ (คืนค่า None) | ตรวจสอบ selector ให้ตรงกับ HTML จริง และเช็คเงื่อนไข `if element:` ก่อนเข้าถึง |
| `SyntaxError: invalid syntax` พร้อมสัญลักษณ์ `<<<<<<<` | มี Git merge conflict markers หลงเหลือในไฟล์ | เปิดไฟล์แล้วลบสัญลักษณ์ `<<<<<<<`, `=======`, `>>>>>>>` และเลือกโค้ดที่ถูกต้องเก็บไว้ |
| PowerShell: `running scripts is disabled` | Execution Policy ของ Windows บล็อกสคริปต์ | รัน `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` แบบ Administrator |
