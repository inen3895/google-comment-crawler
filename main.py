from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_google_reviews(place_url, max_reviews=10):
    # 設定 Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # 先關閉 headless 測試
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    # 啟動 WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(place_url)
    time.sleep(5)  # 等待頁面加載

    # 捲動頁面，確保評論完全載入
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(3)  # 增加等待時間
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 滾動到底部，結束
        last_height = new_height

    # 等待評論區塊出現 "div .MyEned span.wiI7pd"  "span.wiI7pd"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.MyEned span.wiI7pd"))
    )

    # 爬取評論
    reviews = driver.find_elements(By.CSS_SELECTOR, "div.MyEned span.wiI7pd")

    # 只取前 max_reviews 筆評論
    review_texts = [review.text for review in reviews[:max_reviews]]

    driver.quit()
    return review_texts

# 測試爬取 Google 地圖上某個地點的評論
place_url = "https://www.google.com.tw/maps/place/國立成功大學/data=!4m7!3m6!1s0x346e76ed290820d3:0xe0ee028be207a19e!8m2!3d22.998955!4d120.2171461!16zL20vMDF2dHNm!19sChIJ0yAIKe12bjQRnqEH4osC7uA?authuser=0&hl=zh-TW&rclk=1"
reviews = get_google_reviews(place_url, max_reviews=50)

# 印出評論
with open("output.txt", "w", encoding="utf-8") as file:
    for i, review in enumerate(reviews, start=1):
        file.write(f"評論 {i}: {review}\n")