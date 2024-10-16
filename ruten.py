from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 設定 ChromeDriver 路徑
PATH = r"chromedriver-win64\chromedriver.exe"
driver = webdriver.Chrome()

cateid = ["002100010047", "002100010009", "002100010024", "002100010001", "002100010062", "002100010057", "002100010003",
          "002100010046", "002100010039", "002100010002", "002100010051", "002100010010", "002100010063", "002100010065", "002100010008",
          "002100010061", "002100010064", "002100010036", "002100010066", "002100010060", "002100010067", "002100010048", "002100010068"]

start_time = time.time()
id = 1

try:
    for i in range(len(cateid)):
        driver.get(f"https://www.ruten.com.tw/find/?q=%E6%89%8B%E6%A9%9F&cateid={cateid[i]}&p=1")
        time.sleep(1)  # 等待頁面加載

        # 設定換頁次數
        max_pages = 2
        current_page = 1
        b_id = 1

        while current_page <= max_pages:
            print(f"正在爬取第 {current_page} 頁...")
            
            # 滾動頁面到底部
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # 等待新內容加載
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            products = driver.find_elements(By.CLASS_NAME, "rt-product-card-detail-wrap")
            for product in products:
                if product.text == "":
                    continue
                else:
                    print(f"{id} {b_id} title: {product.text}")

                    # 點擊進入商品詳細頁面
                    product_link = product.find_element(By.CLASS_NAME, "rt-product-card-name-wrap").get_attribute("href")
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(product_link)

                    # 爬取商品規格、庫存、價錢等
                    try:
                        # 檢查是否有規格按鈕
                        spec_buttons = driver.find_elements(By.CLASS_NAME, "item-spec-list-item")

                        if spec_buttons:
                            print(f"商品有 {len(spec_buttons)} 種規格選項。")
                            
                            # 遍歷每個規格按鈕
                            for button in spec_buttons:
                                try:
                                    # 點擊規格按鈕
                                    button.click()
                                    time.sleep(1)  # 確保內容刷新

                                    # 獲取商品規格、價錢、庫存
                                    spec = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "item-spec-name"))
                                    ).text
                                    price = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "rt-text-xx-large.rt-text-important"))
                                    ).text
                                    stock = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, "rt-text-isolated"))
                                    ).text
                                    print(f"規格: {spec}, 價錢: {price}, 庫存: {stock}")

                                except Exception as e:
                                    print(f"無法爬取規格資料: {e}")
                        else:
                            # 若無規格按鈕，直接抓取商品資料
                            spec = ""
                            price = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "rt-text-xx-large.rt-text-important"))
                            ).text
                            stock = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "rt-text-isolated"))
                            ).text
                            print(f"規格: {spec}, 價錢: {price}, 庫存: {stock}")

                    except Exception as e:
                        print(f"商品詳細頁面抓取失敗: {e}")

                    # 關閉商品詳細頁面，回到之前的頁面
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

                    id += 1
                    b_id += 1
                    print("----------------------------------")

            # 檢查是否有下一頁
            try:
                next_button = driver.find_element(By.LINK_TEXT, str(current_page + 1))
                next_button.click()
                time.sleep(1)
                current_page += 1
            except:
                print("找不到下一頁，爬蟲結束。")
                break

finally:
    # 確保所有窗口關閉
    driver.quit()

# 計算總執行時間
end_time = time.time()
elapsed_time = end_time - start_time
print(f"總共執行時間: {elapsed_time:.2f} 秒")

