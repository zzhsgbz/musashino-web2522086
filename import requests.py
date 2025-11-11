import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# 目標のウェブサイト（武蔵野大学）
BASE_URL = "https://www.musashino-u.ac.jp/"
visited = set()  # 訪問済みページの集合（重複を避ける）
pages = {}       # 結果を保存する辞書 {URL: タイトル}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MusashinoCrawler/1.0)"}

def crawl(url):
    """同一ドメイン内のウェブページを再帰的にクロールする"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Content-Type が HTML でない場合はスキップ
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            print(f"⚠️ HTML 以外のファイルをスキップ: {url} | Content-Type: {content_type}")
            return

        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, "html.parser")

        # ページタイトルを取得
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "No title"
        pages[url] = title
        print(f"✅ クロール完了: {url} | タイトル: {title}")

        # ページ内のリンクをすべて取得
        for a in soup.find_all("a", href=True):
            link = a["href"].strip()
            full_url = urljoin(url, link)
            parsed = urlparse(full_url)

            # 同一ドメインのページのみクロール
            if parsed.netloc == urlparse(BASE_URL).netloc:
                clean_url = full_url.split("#")[0]  # アンカーを除去
                if clean_url not in visited:
                    visited.add(clean_url)
                    time.sleep(1)  # 1秒間隔でアクセス
                    crawl(clean_url)

    except Exception as e:
        print(f"⚠️ スキップ {url}: {e}")

if __name__ == "__main__":
    print("武蔵野大学ウェブサイトをクロール中、少々お待ちください...\n")
    crawl(BASE_URL)
    print("\n=== クロール結果 ===")
    print(pages)
