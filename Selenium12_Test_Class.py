#  Импортируем необходимые библиотеки и модули
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from selenium.webdriver.common.by import By


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
    def opening_the_site(self, ):
        #  Открываем вебдрайвером ссылку
        self.driver.get('https://saucedemo.com/')

        #  Устанавливаем размер окна в 9/16 ширины экрана с максимальной высотой
        #  Получаем разрешение экрана (ширину и высоту)
        screen_width, screen_height = pyautogui.size()

        reduced_width = int(screen_width*9//16)  #  9/16 ширины

        #  Устанавливаем размер окна в 9/16 ширины
        self.driver.set_window_size(reduced_width, screen_height)

        #  Располагаем окно от левого верхнего угла
        self.driver.set_window_position(0, 0)

        print('The link is trying to open in a Chrome window.')
        if not self.detach:
            print('The browser window will close automatically when the session ends.')

    def authorization(self, site_loading_time=30, authorization_waiting_time=5):
        #  В течение site_loading_time сек ждём появления кликабельной кнопки [Login],
        #  и сразу после её появления начинаем ввод логина и пароля
        mistakes = 0  #  Счетчик ошибок
        try:
            WebDriverWait(self.driver, site_loading_time).until(
                EC.element_to_be_clickable(
                    (By.ID, "login-button")
                )
            )
        except TimeoutException:
            print(f'The login button did not become clickable in {authorization_waiting_time} seconds')
            mistakes += 1  # Увеличим значение на 1
        #  Вводим user-name и password (верные для этого сайта) в поля ввода
        mistakes = 0  #  Счетчик ошибок
        try:
            self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        except NoSuchElementException:  #  если поле не найдено
            print('User-name input field not found')
            mistakes += 1  #  Увеличим значение на 1
        try:
            self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        except NoSuchElementException:  #  если поле не найдено
            print('Password input field not found')
            mistakes += 1  #  Увеличим значение на 1
        if mistakes != 0:
            return False

        print('The username and the password have been entered.')

        self.driver.find_element(By.ID, "login-button").click()
        print('The login button has been pressed.')
        time.sleep(5)

        #  Жмём клавишу ESCAPE для закрытия всплывшего окна браузера
        #  с предупреждением о смене пароля
        pyautogui.press('escape')
        print('''The ESC key was pressed to close the pop-up window 
(which may have appeared) warning about the password change.\n''', '_' * 20, sep='')

        try:
            #  Проверка успешной авторизации по наличию
            #  элемента с текстом "Products".
            #  В течение authorization_waiting_time секунд ждём появления
            #  элемента с ожидаемым текстом "Products",
            WebDriverWait(self.driver, authorization_waiting_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[text()='Products']")
                )
            )
            print('Authorization is successful!')
            return True
        except TimeoutException:  #  если элемент с текстом "Products" отсутствует
            print('Element with the text "Products" not found')
            return False

    #  закрытие браузера
    def closing_the_browser(self):
        #  Сначала -- проверка одновременного наличия и непустоты driver в классе
        if hasattr(self, 'driver') and self.driver is not None:
            try:
                print('The browser will close in 5 seconds.')
                time.sleep(5)
                self.driver.quit()
                print('Session terminated. Browser was closed.')
            finally:
                self.driver = None  #  Зануляем ссылку, для очистки памяти
        else:
            print('Browser session not found.')


#  Создаём экземпляр класса OpenByChrome с неявно заданным
#  параметром detach (по умолчанию detach=True),
test_start = OpenAndCloseByChrome()

test_start.opening_the_site()  #  открытие сайта в окне браузера

#  ТЕСТ № 1
#  Проверка авторизации
#  после нажатия кнопки [Login] при введённых логине, пароле.
#  Явно задаём site_loading_time и authorization_waiting_time --
#  -- это необязательно. (По умолчанию они 30 и 5 сек соответственно)
assert test_start.authorization(
    site_loading_time=60,
    authorization_waiting_time=10
) == True, 'Authorization did not occur'

time.sleep(3)
test_start.closing_the_browser()  #  закроем браузер








