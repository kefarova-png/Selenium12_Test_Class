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
import random


class SmokeTestByChrome:
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

    #  открытие сайта в окне браузера НЕ на полный экран
    def opening_the_site(self):
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

    def press_escape_button(self):
        #  Жмём клавишу ESCAPE для закрытия всплывшего окна браузера
        #  с предупреждением о смене пароля
        pyautogui.press('escape')
        print('_' * 26, '''\nThe ESC key was pressed 
to close the pop-up window 
(which might have appeared) 
warning about the password change\n''', '_' * 26, sep = '')

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
            print('Authorization error(s)')
            return False

        print('The username and the password have been entered')

        self.driver.find_element(By.ID, "login-button").click()
        print('The login button has been pressed')
        time.sleep(8)

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

    def add_to_cart(self, page_loading_time=5):
        products = {
            "1": ("Sauce Labs Backpack", ".inventory_item_name", ".inventory_item_price"),
            "2": ("Sauce Labs Bike Light", ".inventory_item_name", ".inventory_item_price"),
            "3": ("Sauce Labs Bolt T-Shirt", ".inventory_item_name", ".inventory_item_price"),
            "4": ("Sauce Labs Fleece Jacket", ".inventory_item_name", ".inventory_item_price"),
            "5": ("Sauce Labs Onesie", ".inventory_item_name", ".inventory_item_price"),
            "6": ("Test.allTheThings() T-Shirt (Red)", ".inventory_item_name", ".inventory_item_price")
        }  # Сопоставление выбора с названием товара, селектором кнопки его выбора и селектором его цены
        print("""List of products to choose:
        1 - Sauce Labs Backpack
        2 - Sauce Labs Bike Light
        3 - Sauce Labs Bolt T-Shirt
        4 - Sauce Labs Fleece Jacket
        5 - Sauce Labs Onesie
        6 - Test.allTheThings() T-Shirt (Red)""")  # Список товаров
        choice = str(random.randint(1, 6))  # Случайный выбор номера продукта
        print(f'Product No. {choice} has been selected')

        #  Зададим переменные для элементов кортежа:
        #  product_name — первый элемент кортежа (имя товара),
        #  name_locator — второй элемент кортежа (CSS-селектор для названия товара),
        #  price_locator — третий элемент кортежа (CSS-селектор для цены).
        product_name, name_locator, price_locator = products[choice]

        self.press_escape_button()
        time.sleep(1)
        #  На странице товаров находим нужный товар по имени и добавляем в корзину:
        #  Сделаем список всех WebElement’ов, у которых класс (class) равен "inventory_item"
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        selected_item = None

        for item in items:  #  Ищем элемент, совпадающий с product_name
            name_element = item.find_element(By.CSS_SELECTOR, name_locator)
            if name_element.text == product_name:  #  При совпадении текущий item -> selected_item
                selected_item = item
                break

        if not selected_item:  #  Если элемент, соответствующий товару, не нашёлся
            print("Product not found")
            exit()

        #  Проверяем кликабельность элемента перед нажатием

        #  Добавляем в корзину (ищем внутри выбранного элемента кнопку с классом btn_inventory и кликаем её)
        selected_item.find_element(By.CLASS_NAME, "btn_inventory").click()
        time.sleep(2)

    def go_to_cart(self, page_loading_time=5):
        #  В течение site_loading_time секунд ждём появления кнопки-значка Корзины
        try:
            WebDriverWait(self.driver, page_loading_time).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "shopping_cart_link")
                )
            )
        except TimeoutException:
            print(f'Cart button not found in {page_loading_time} second')
        #  Переходим к корзине (находим и кликаем кнопку-значок Корзины)
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(3)

        #  Проверяем, что находимся в корзине
            #  Проверка успешной авторизации по наличию
            #  элемента с текстом "Your Cart".
            #  В течение site_loading_time секунд ждём появления
            #  элемента с ожидаемым текстом "Your Cart",
        try:
            WebDriverWait(self.driver, page_loading_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[contains(text(), 'Your Cart')]")
                )
            )
            print('The Cart Page has loaded!')
            return True
        except TimeoutException:  #  если элемент с текстом "Your Cart" отсутствует
            return False

    #  закрытие браузера
    def closing_the_browser(self):
        #  Сначала -- проверка одновременного наличия и непустоты driver в классе
        if hasattr(self, 'driver') and self.driver is not None:
            try:
                print('The browser will close in 5 seconds')
                time.sleep(5)
                self.driver.quit()
                print('Session terminated. Browser was closed')
            finally:
                self.driver = None  #  Зануляем ссылку, для очистки памяти
        else:
            print('Browser session not found')


#  Создаём экземпляр класса OpenByChrome с неявно заданным
#  параметром detach (по умолчанию detach=True),
test = SmokeTestByChrome()

test.opening_the_site()  #  открытие сайта в окне браузера

#  ТЕСТ
#  Проверка возможности перейти на страницу корзины
#  после нажатия кнопки [Login] при введённых логине, пароле,
#  после нажатия кнопки-значка корзины при выбранном товаре

test.authorization()
test.add_to_cart()
assert test.go_to_cart() == True, 'Element with the text "Your Cart" not found'

time.sleep(3)
test.closing_the_browser()  #  закроем браузер








