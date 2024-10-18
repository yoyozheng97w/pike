from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 設定 ChromeDriver 路徑
PATH = r"chromedriver\chromedriver.exe"
driver = webdriver.Chrome()

driver.get("https://ec-w.shopping.friday.tw/")

  # 找到相應的label名稱
search = driver.find_element(By.NAME, "keyword")
search.send_keys("手機")
time.sleep(1)
# 按下enter鍵
search.send_keys(Keys.RETURN)
time.sleep(3)

try:
    # 等待 "更多產品" 按鈕可點擊，並點擊
    # 使用更具體的選擇器
    more_products_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'更多品牌')]"))
    )
    more_products_button.click()

    # 等待 checkbox 出現
    # 假設 checkbox 在特定容器內，加上容器的選擇器
    checkboxes = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH,"//label[contains(text(),'vivo')]//input[@type='checkbox']"))
    )#body > div > div._2c5a3d6bb126 > div > div.wrap > div.categoryFilter > div.categoryFilter__filter > ul > li:nth-child(1) > div > i

    # # 依序點擊所有未被選中的 checkbox
    # for checkbox in checkboxes:
    #     # 加入 try-except 以處理可能的 StaleElementReferenceException
    #     try:
    #         if not checkbox.is_selected():
    #             # 使用 JavaScript 點擊，避免元素被其他元素遮擋
    #             driver.execute_script("arguments[0].click();", checkbox)
    #         time.sleep(1)
    #     except Exception as e:
    #         print(f"Error clicking checkbox: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 等待 5 秒觀察結果，然後關閉瀏覽器
    time.sleep(5)
    driver.quit()