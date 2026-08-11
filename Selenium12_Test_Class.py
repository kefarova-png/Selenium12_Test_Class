#  Импортируем необходимые библиотеки и модули
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
#  from selenium.webdriver.common.by import By


class OpenByChrome:
    def __init__(self):  #  создание вебдрайвера Chrome
        options = webdriver.ChromeOptions()  #  настройки Chrome
        options.add_experimental_option("detach", True)  #  в настройки добавлен параметр detach
        print(f'Chrome experimental options = {options._experimental_options}\n')  #  сообщение об опциях Chrome
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),  #  вебдрайвер ChromeDriver скачан/запущен автоматически
            options=options  #  ранее созданные опции вебдрайвера
        )

    def opening_the_site(self):  #  открытие сайта в окне браузера
        #  Открываем вебдрайвером ссылку
        self.driver.get('https://saucedemo.com/')
        #  Устанавливаем размер окна
        self.driver.set_window_size(1080,1080)
        print('The link is open in a Chrome window')


test_start = OpenByChrome()  #  экземпляр класса
test_start.opening_the_site()  #  открытие сайта в окне браузера

time.sleep(6)
test_start.driver.close()  #  закрываем браузер