#  Импортируем необходимые библиотеки и модули
import time
#  from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
#  from selenium.webdriver.common.by import By


class OpenAndCloseByChrome:
    #  создание вебдрайвера Chrome
    def __init__(self, detach=True):
        options = webdriver.ChromeOptions()  #  настройки Chrome
        #  применяем аргумент detach
        options.add_experimental_option("detach", bool(detach))
        self.detach = detach  #  сохраняем состояние для использования в дальнейшем
        #  Выведем сообщение об опциях Chrome
        print(f'\nChrome experimental options = {options._experimental_options}\n')

        self.driver = webdriver.Chrome(
            #  драйвер скачан/запущен автоматически
            service=ChromeService(ChromeDriverManager().install()),
            #  ранее созданные опции вебдрайвера
            options=options
        )

    #  открытие сайта в окне браузера не на полный экран
    def opening_the_site(self):
        #  Открываем вебдрайвером ссылку
        self.driver.get('https://saucedemo.com/')

        #  Устанавливаем размер окна в 9/16 ширины экрана с максимальной высотой
        #  Получаем разрешение экрана (ширину и высоту)
        screen_width, screen_height = pyautogui.size()

        reduced_width = int(screen_width*9//16)  #  9/16 ширины

        #  Устанавливаем размер окна в 3/4 ширины
        self.driver.set_window_size(reduced_width, screen_height)

        #  Располагаем окно от левого верхнего угла
        self.driver.set_window_position(0, 0)

        print('The link is open in a Chrome window.')
        if not self.detach:
            print('The browser window will close automatically when the session ends.')

    #  закрытие браузера
    def closing_the_browser(self):
        #  Сначала -- проверка одновременного наличия и непустоты driver в классе
        if hasattr(self, 'driver') and self.driver is not None:
            try:
                print('The browser will close in 5 seconds.')
                time.sleep(5)
                self.driver.quit()
                print('Session terminated. Browser was closed.')
            except Exception as exception:  #  При наличии ошибки запоминаем ошибку
                print(f"Ошибка при закрытии: {exception}")
                quit()  #  Из-за отловленной ошибки завершаем работу
            finally:
                self.driver = None  #  Зануляем ссылку, для очистки памяти
        else:
            print('Browser window not found')


#  1)
#  Создаём экземпляр класса OpenByChrome с неявно заданным
#  параметром detach (по умолчанию detach=True)
test_start1 = OpenAndCloseByChrome()

test_start1.opening_the_site()  #  открытие сайта в окне браузера
time.sleep(3)

test_start1.closing_the_browser()  #  завершим работу скрипта
time.sleep(3)

#  2)
#  Создаём экземпляр класса OpenByChrome с явно заданным
#  параметром detach, отличным от умолчания
test_start2 = OpenAndCloseByChrome(detach=False)

test_start2.opening_the_site()  #  открытие сайта в окне браузера
#  из-за detach не равно True окно браузера закроется по окончании работы скрипта
time.sleep(3)








