from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import random


PATH = "C:/Users/chromedriver.exe"
myOptions = webdriver.ChromeOptions()
myOptions.add_argument("--user-agent=") #反反爬加入user agent
myOptions.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(options=myOptions) #沒有要反反爬蟲，options可以拿掉

driver.get("https://www.momoshop.com.tw/")
time.sleep(6)

threec_link = driver.find_element(By.XPATH, '//*[@id="C11"]/a[1]') #點入手機平板
threec_link.click()
time.sleep(3)

test_kind = []
product_data = []
for i in range(7, 12): #第二層選取物品
    test_kind.append(driver.find_element(By.XPATH,f'//*[@id="bt_category_Content"]/ul/li[{i}]/h2/a'))
    time.sleep(8)

for test_link in test_kind: #點入安卓手機從物品中點入連結進到第三層分類
    try:
        test_link.click()
        time.sleep(random.randint(4,8))
        test_serieses = driver.find_elements(By.CLASS_NAME, 'cates BTDME FuncYN')
        for test_series in test_serieses: #第三層選取每個品牌系列
            test_series.click()
            time.sleep(random.randint(4,8))

            # test_prdpage = []
            #<div class="adjustmentTextArea" style="">很抱歉，沒有篩選到符合條件的商品，您可以調整篩選條件試試看。</div>
            try:
                product_links = driver.find_elements(By.CLASS_NAME, 'prdUrl') #鎖定該頁所有產品url的定位
                for link in product_links:
                    link.click() #點入當頁每個產品頁面
                    time.sleep(random.randint(4,8))
                    try:        
                        product_info = {}
                        product_info['名稱'] = driver.find_element(By.CLASS_NAME, 'productName').text
                        product_info['品牌'] = driver.find_element(By.CLASS_NAME, 'webBrandLink brand-name').text
                        product_info['圖片連結'] = driver.find_element(By.CLASS_NAME, 'jqzoom').get_attribute('src')
                        product_info['促銷價'] = driver.find_element(By.CLASS_NAME, 'seoPrice').text
                        product_info['價格'] = driver.find_element(By.CLASS_NAME, 'seoPrice').text
                        product_info['顏色'] = driver.find_element(By.NAME, 'cart_spec1').text
                        product_info['結帳方式'] = driver.find_element(By.CLASS_NAME, 'payment').text
                        product_info['配送方式'] = driver.find_element(By.CLASS_NAME, 'dely_work').text
                        product_info['總銷量'] = driver.find_element(By.CLASS_NAME, 'productTotalSales').text
                        product_info['商品評價'] = driver.find_element(By.CLASS_NAME, 'indicatorAvgVal').text
                        # print(product_info)
                        product_data.append(product_info)
                        driver.back() #回到第一頁prdurl那頁

                    except:
                        pass #沒東西下一個商品

                try:
                    #如果有第二頁 //*[@id="goodsAttrRoot"]/div[3]/div[5]/ul/li[2]/a
                    xpath = '//*[@id="goodsAttrRoot"]/div[3]/div[5]/ul/li[2]/a'
                    page_two = driver.find_element(By.XPATH, xpath)
                    print("找到指定的 XPath。元素存在。")
                    page_two.click()
                    time.sleep(random.randint(4,8))
                    product_links2 = driver.find_elements(By.CLASS_NAME, 'prdUrl')
                    for link2 in product_links2:
                        link2.click() #點入當頁每個產品頁面
                        time.sleep(random.randint(4,8))
                        product_info2 = {}
                        product_info2['名稱'] = driver.find_element(By.CLASS_NAME, 'productName').text
                        product_info2['品牌'] = driver.find_element(By.CLASS_NAME, 'webBrandLink brand-name').text
                        product_info2['圖片連結'] = driver.find_element(By.CLASS_NAME, 'jqzoom').get_attribute('src')
                        product_info2['促銷價'] = driver.find_element(By.CLASS_NAME, 'seoPrice').text
                        product_info2['價格'] = driver.find_element(By.CLASS_NAME, 'seoPrice').text
                        product_info2['顏色'] = driver.find_element(By.NAME, 'cart_spec1').text
                        product_info2['結帳方式'] = driver.find_element(By.CLASS_NAME, 'payment').text
                        product_info2['配送方式'] = driver.find_element(By.CLASS_NAME, 'dely_work').text
                        product_info2['總銷量'] = driver.find_element(By.CLASS_NAME, 'productTotalSales').text
                        product_info2['商品評價'] = driver.find_element(By.CLASS_NAME, 'indicatorAvgVal').text
                        product_data.append(product_info2)
                        driver.back() #回到第二頁prdurl頁這頁
                    #drive.back() #回到第一頁
                except:
                    print("未找到指定的 XPath。元素不存在。")
                    pass
                    #不用加drive.back() #太早回到安卓手機的個別頁面

                driver.back() #回到安卓手機的頁面去選取其他系列    
                                    
            except:
                driver.back() #點入後沒商品回到上一頁去選其他系列
                pass
        driver.back() #回到第二層選擇ai手機、安卓手機那頁
    except:
        pass

driver.quit()

df = pd.DataFrame(product_data)
df.to_csv('/content/drive/My Drive/test.csv', index=False)