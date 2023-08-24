import time
import openpyxl
from openpyxl.utils.exceptions import IllegalCharacterError
from selenium.webdriver.common.by import By
from selenium import webdriver
# 创建 ChromeOptions 对象
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # 避免被检测为Selenium驱动
options.add_experimental_option("excludeSwitches",["enable-automation"]) #避免网站检测selenium 开发者模式调用
#options.add_argument("--headless") #无头模式

#采集函数
def main():
    data=[]
    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window() #网页最大化
        driver.implicitly_wait(5) #隐式等待5s
        driver.get('https://y.qq.com/n/ryqq/songDetail/004AivAF25UBQc')
        #循环滚动
        while True:
            #获取评论元素li列表
            ul_elements = driver.find_elements(By.XPATH, '//*[@id="comment_box"]/div[4]/ul/li')
            #滚动到最后一条评论 等待1秒加载后面的评论
            driver.execute_script("arguments[0].scrollIntoView();", ul_elements[-1])
            time.sleep(1)
            #当前页面下评论数量
            datacount=len(ul_elements)
            print(f'当前数据{datacount}条')
            #如果当前评论元素数量大于maxnum，则获取页面数据并跳出循环
            if datacount>maxnum:
                #循环评论li列表，使用xpath获取评论昵称，时间地点，评论内容
                for item in ul_elements:
                    try:
                        #昵称
                        name = item.find_element(By.XPATH, "div/h4").get_attribute('textContent').strip()
                        #时间地点
                        datecontent = item.find_element(By.XPATH, "div/div[contains(@class,'comment__date')]").get_attribute(
                            'textContent').strip().replace('\xa0\xa0', ' ')
                        #拆分时间和地点
                        datetext,place_text = datecontent.split('来自')
                        content = item.find_element(By.XPATH, "div/p").get_attribute('textContent').strip()
                        data.append([name, datetext.strip(),place_text, content])
                        print([name, datetext,place_text, content])
                    except:
                        pass
                break
    return data
#保存数据
def savedata(data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    #设置表格宽度
    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 15
    sheet.column_dimensions['C'].width = 10
    sheet.column_dimensions['D'].width = 40
    #设置表头
    sheet.append(['昵称','时间','地点','内容'])
    for item in data:
        try:
            sheet.append(item)
        except IllegalCharacterError as e:
            print("Error:", e)
    workbook.save(filepath)

if __name__ == '__main__':
    #xlsx存放路径
    filepath= '罗刹海市.xlsx'
    #采集数量
    maxnum=1000
    #主函数
    result = main()
    if result:
        #保存至表格
        savedata(result)




