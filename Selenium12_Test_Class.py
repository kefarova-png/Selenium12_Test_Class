#  Импортируем необходимые библиотеки и модули
import time
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


#  Chrome. Добавляем опции браузера: detach, True -- чтобы Chrome не закрывал окно браузера после завершения работы кода
webdriver.ChromeOptions().add_experimental_option("detach",True)
#  Создаём вебдрайвер Chrome c этими опциями и с автоматической проверкой/установкой драйвера
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=webdriver.ChromeOptions()
)

class Test():
    def product_select(self):  #  открытие сайта в окне
        #  Открываем вебдрайвером ссылку
        driver.get('https://saucedemo.com/')
        #  Устанавливаем размер окна
        driver.set_window_size(1080,1080)

    def random_name_enter(self):  #  ввод случайного имени
        #  Генерируем случайное имя
        fake_name = Faker("en_US").first_name()  #  устанавливаем язык генерации -- английский США
        print(f'A random name "{fake_name}" has been generated for use as a login')

        #  Находим элемент для логина, используя XPATH, и вводим в поле логина сгенерированное случайное имя
        driver.find_element(By.XPATH, "//input[@id='user-name']").send_keys(fake_name)
        print(f'Login "{fake_name}" entered')


test_start = Test()  #  экземпляр класса
test_start.product_select()  #  открытие сайта в окне
test_start.random_name_enter()  #  ввод случайного имени

time.sleep(6)
# driver.close()  #  Закрываем браузер