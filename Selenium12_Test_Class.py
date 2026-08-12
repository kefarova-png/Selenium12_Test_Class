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

    #  открытие сайта в окне браузера
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

    #  закрытие браузера с учетом параметра detach
    def closing_the_browser(self):
        #  Сначала -- проверка одновременного наличия и непустоты driver в классе
        if hasattr(self, 'driver') and self.driver is not None:
            try:
                if not self.detach:  #  При detach=False или при отсутствии параметра detach
                    #  Закроем все вкладки браузера, открытые драйвером в рамках текущей сессии
                    self.driver.quit()
                    print("Script execution terminated. Browser (no Detach mode) was closed.")

                else:  #  При detach=True
                    print('''Detach mode:
    Script execution terminated.
    The browser window is not closed.''')

            except Exception as exception:  #  при наличии ошибки запоминаем ошибку
                print(f"Ошибка при закрытии: {exception}")
            finally:
                self.driver = None  #  Зануляем ссылку, для очистки памяти

    #  безусловное закрытие активного окна
    def unconditional_quitting_the_window(self):
        try:
            #  Закроем активное окно
            pyautogui.hotkey('alt', 'f4')
            print('[Alt] + [F4] have been pressed to close current window.')

        except Exception as exception:  #  при наличии ошибки запоминаем ошибку
            print(f"Ошибка при закрытии: {exception}")

        finally:
            self.driver = None  #  Зануляем ссылку, для очистки памяти


#  1)
#  Создаём экземпляр класса OpenByChrome с неявно заданным
#  параметром detach (по умолчанию detach=True)
test_start1 = OpenAndCloseByChrome()

test_start1.opening_the_site()  #  открытие сайта в окне браузера
time.sleep(3)

#  завершим работу скрипта (но из-за detach=True окно не закроется)
test_start1.closing_the_browser()
time.sleep(3)

#  закрытие текщего окна
#  (не рекомендуется, можно закрыть не то окно при случайном изменении фокуса)
test_start1.unconditional_quitting_the_window()
time.sleep(3)

#  2)
#  Создаём экземпляр класса OpenByChrome с явно заданным
#  параметром detach, отличным от умолчания
test_start2 = OpenAndCloseByChrome(detach=False)

test_start2.opening_the_site()  #  открытие сайта в окне браузера
time.sleep(3)

#  завершим работу скрипта (и из-за detach не равно True окно закроется)
test_start2.closing_the_browser()






