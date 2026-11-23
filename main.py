## Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# pip install selenium

# import json
from time import sleep

from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_element(browser, delay=5, by=By.CSS_SELECTOR, value=None):
    return WebDriverWait(browser, delay).until(
        EC.presence_of_element_located((by, value))
    )


driver = Edge()
driver.get('https://habr.com/ru/all/')
sleep(5)

# class="tm-articles-list" - коробка со статьями
# class="article-snippet" - коробочка с одной статьей

article_block = wait_element(driver, value='div.tm-articles-list')
article_list = article_block.find_elements(By.CSS_SELECTOR, 'div.article-snippet')


links = []
for article in article_list:
    div_with_link = wait_element(article, value='h2.tm-title.tm-title_h2')
    link = wait_element(div_with_link, value='a').get_attribute('href')
    links.append(link)

parsed_data = []
for link in links:
    driver.get(link)
    title = wait_element(driver, value='h1').text.strip()
    time = wait_element(driver, value='time').get_attribute('title')
    text = wait_element(driver, value='div.article-formatted-body_version-2').text.strip()
    tags = wait_element(driver, value='div.tm-publication-hubs').text.strip()

    title_lower = title.lower()
    text_lower = text.lower()
    tags_lower = tags.lower()
    
    if any(key in title_lower or key in text_lower or key in tags_lower for key in KEYWORDS):
        parsed_data.append({
            'time': time,
            'title': title,
            'link': link,
        })


# with open('articles2.json', 'w', encoding='utf-8') as file:
#     json.dump(parsed_data, file, ensure_ascii=False, indent=2)

#  Замена вывода с json-файла на консоль

for item in parsed_data:
    print(f"{item['time']} - {item['title']} - {item['link']}")

driver.quit()