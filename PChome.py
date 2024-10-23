import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_product_title(driver, p_link):
    """
    獲取商品標題
    """
    try:
        css_title = "#ProdBriefing > div > div > div > div.c-boxGrid__item.c-boxGrid__item--prodBriefingArea > div.o-prodMainName.o-prodMainName--prodNick > h1"
        product_title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_title))
        ).text
        print(f"流水商品號: {p_link} 標題: {product_title}")
        return product_title
    except (TimeoutException, NoSuchElementException) as e:
        print(f"獲取商品標題時發生錯誤: {str(e)}")
        return None

def get_product_price(driver):
    """
    獲取商品價格
    """
    try:
        css_price = "#ProdBriefing > div > div > div > div.c-boxGrid__item.c-boxGrid__item--prodBriefingArea > div.c-blockCombine.c-blockCombine--priceGray > div > div > div > div > div.o-prodPrice__price.o-prodPrice__price--xxxl700Primary"
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_price))
        ).text
        print(f"價格: {price}")
        return price
    except (TimeoutException, NoSuchElementException) as e:
        print(f"獲取商品價格時發生錯誤: {str(e)}")
        return None
    
def get_product_specbu(driver):
    """
    獲取規格按鈕並顯示字樣
    """
    try:
        css_button = "#ProdBriefing > div > div > div > div.c-boxGrid__item.c-boxGrid__item--prodBriefingArea > div:nth-child(6) > ul > li > button > span"
        # 使用 WebDriverWait 等待按鈕元素出現
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_button))
        )
        # 直接獲取按鈕的文字內容
        visible_text = button.text
        print(f"按鈕規格: {visible_text}")
        return visible_text
    except TimeoutException:
        print("找不到規格按鈕元素")
        return None
    except NoSuchElementException:
        print("找不到規格按鈕元素")
        return None
    except Exception as e:
        print(f"獲取規格按鈕時發生錯誤: {str(e)}")
        return None

def scrape_pchome():
    driver = webdriver.Chrome()
    try:
        driver.get("https://24h.pchome.com.tw/")
        print(f"連結到: {driver.title}")

        # 找到搜尋框並輸入關鍵字
        search_box = driver.find_element(By.CLASS_NAME, 'c-search__input')
        time.sleep(3)
        search_box.send_keys('手機')
        search_box.send_keys(Keys.RETURN)
        time.sleep(10)

        # 商品編號計數器
        p_link = 1
        
        while True:
            try:
                # 構建商品選擇器
                product_selector = f"body > div.l-layout.l-layout--rwd > main > div.container.container--lg > div > div > section:nth-child(2) > div > div > section > div > div > div.c-boxGrid.c-boxGrid--base > div.c-boxGrid__body.c-boxGrid__body--topBorder > div > div > ul:nth-child(3) > li:nth-child({p_link}) > div > a"
                
                # 等待商品元素出現
                first_product = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, product_selector))
                )

                # 獲取商品網址
                product_url = first_product.get_attribute("href")
                print(f"網址: {product_url}")

                # 點擊商品連結
                first_product.click()
                time.sleep(2)
                

                # 使用方法獲取資訊 
                get_product_title(driver, p_link)
                get_product_price(driver)
                get_product_specbu(driver)

                # 返回上一頁繼續搜尋下一個商品
                driver.back()
                time.sleep(2)
                
                # 增加計數器
                p_link += 1

            except TimeoutException:
                print(f"找不到第 {p_link} 個商品，可能已經到達最後一頁")
                p_link = 1  # 重置計數器，可以選擇是否要重新開始
                continue
            
            except Exception as e:
                print(f"發生未預期的錯誤: {str(e)}")
                continue

    except Exception as e:
        print(f"程式發生錯誤: {str(e)}")
    
    finally:
        # 確保程式結束時關閉瀏覽器
        driver.quit()

if __name__ == "__main__":
    scrape_pchome()