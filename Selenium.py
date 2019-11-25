""""
使用Selenium模块抓取淘宝网商品信息
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import quote
from pyquery import PyQuery as pq


chrome_options = webdriver.ChromeOptions()
# 创建无界面浏览
chrome_options.add_argument("--headless")
# 禁用Gpu渲染
chrome_options.add_argument("--disable-gpu")
# 禁用图片加载
prefs = {"profile.default_content_setting_values": {"images": 2}}
chrome_options.add_experimental_option("prefs", prefs)
# 创建Chrome浏览器对象
browser = webdriver.Chrome(chrome_options=chrome_options)
# 设置延时时间
waite = WebDriverWait(browser, 10)


def index_page(page, key_word):
    print(f"正在抓取第{page}页")
    try:
        url = "https://s.taobao.com/search?q" + quote(key_word)  # 对key_word进行编码
        browser.get(url)
        if page > 1:
            # 延时定位输入框,在设定时间范围内返回结果,若没有结果抛出异常
            input = waite.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager div.form > input")))
            # 延时定位确认框,在设定时间范围内返回结果,若没有结果抛出异常
            submit = waite.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager div.form > span.btn J_Submit")))
            input.clear()  # 清空输入框内容
            input.send_keys(page)  # 键入页码
            submit.click()  # 点击确定按钮
        waite.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-page li.item.active > span"), str(page)))
        waite.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".m-itemlist .items .item")))
        get_products()  # 调用函数get_products,获取产品信息
    except TimeoutException:  # 超时异常处理
        index_page(page, key_word)


def get_products():
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            "image": item.find(".pic .img").attr("data-src"),
            "price": item.find(".price").text(),
            "title": item.find(".title").text(),
            "shop": item.find(".shop").text(),
            "location": item.find(".location").text()
        }
        print(product)


def main():
    index_page(1, "Ipad")


if __name__ == '__main__':
    main()
