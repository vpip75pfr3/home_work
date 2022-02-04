import os
import sys


class FinishPurchases(Exception):
    pass


class Category:
    all_cat = []

    def __init__(self, name):
        self.name = name
        self.goods = []
        Category.all_cat.append(self)

    def __repr__(self):
        return f'Наимнование раздела: {self.name}'

    def show_products(self):
        print(f'В разделе {self.name} находятся следующие товары:')
        for number, cat in enumerate(self.goods, 1):
            print(' ' * 4, number, ': ', cat)

    @classmethod
    def show_all_categories(cls):
        for number, cat in enumerate(cls.all_cat, 1):
            print(number, ': ', cat)


class Product:
    all_products = []

    def __init__(self, name, price, rating, cat: Category):
        self.name = name
        self.price = price
        self.rating = rating
        self.category = None
        self.check_category(cat)
        Product.all_products.append(self)

    def check_category(self, cat):
        if isinstance(cat, Category):
            cat.goods.append(self)
            self.category = cat
        else:
            raise ValueError('Добавьте категорию товара')

    def __repr__(self):
        return f'Наимeнование: {self.name}, Цена: {self.price}, Категория: {self.category.name}'

    @classmethod
    def show_all_products(cls):
        for number, product in enumerate(cls.all_products, 1):
            print(number, ': ', product)


class Basket:
    def __init__(self):
        self.basket = []


class User:
    users_arr = []

    def __init__(self, login, password, name):
        self.__login = login
        self.__password = password
        self.basket = Basket()
        self.name = name
        User.users_arr.append(self)

    @classmethod
    def autentification(cls, _login, _password):
        for _user in User.users_arr:
            if _login == _user.__login:
                if _password == _user.__password:
                    os.system('CLS')  # очистить консоль
                    print(f'Добро пожаловать {_user.name}')
                    return _user
                else:
                    raise ValueError("Неверный пароль")
        else:
            raise ValueError("Пользователь с таким именем не найден")


class Market(Category):
    @classmethod
    def show_all_categories(cls):
        super().show_all_categories()
        exit_number = len(cls.all_cat) + 1
        print(f'{exit_number} :  Выход')
        cat_number = int(input('Выберить нужную категорию: ')) - 1
        if cat_number == (exit_number - 1):
            raise sys.exit()
        else:
            cat = Category.all_cat[cat_number]
        os.system('CLS')  # очистить консоль
        print(f'Вы выбрали раздел {cat.name}')
        return cat

    @classmethod
    def _show_goods(cls, cat):
        cat.show_products()
        exit_number = len(cls.all_cat) + 1
        print(f'     {exit_number} :  Выход')
        prod_number = int(input('Выберить нужный товар: ')) - 1
        if prod_number == (exit_number - 1):
            raise sys.exit()
        else:
            prod = cat.goods[prod_number]
            print(f'Вы выбрали {prod.name}')
        return prod

    @classmethod
    def buy_prod(cls, prod, user):
        os.system('CLS')  # очистить консоль
        print(f'Хотите ли Вы добавить в корзину {prod}')
        print('1: Да', '\n', '2: Нет', sep='')
        x = int(input('Сделайте выбор: '))
        if x == 2:
            pass
        else:
            user.basket.basket.append(prod)

    @classmethod
    def show_goods(cls, user):
        try:
            while True:
                cat = cls.show_all_categories()
                prod = cls._show_goods(cat)
                cls.buy_prod(prod, user)
                cls.confirm_order(user)
        except FinishPurchases:
            pass

    @classmethod
    def confirm_order(cls, user):
        if user.basket.basket:
            print("Перейти к оформлению покупок?")
            print('1: Да', '\n', '2: Нет', sep='')
            x = int(input('Сделайте выбор: '))
            if x == 2:
                pass
            else:
                os.system('CLS')  # очистить консоль
                print('Вы выбрали: ')
                for number, good in enumerate(user.basket.basket, 1):
                    print(number, ': ', good)
                print(f'C Вас {sum(product.price for product in user.basket.basket)} $')
                raise FinishPurchases


if __name__ == '__main__':
    # Создаем категории
    cat_proc = Category('Процессоры')
    cat_mother_boards = Category('Мат платы')
    cat_hdd = Category('Жесткие диски')

    # Создаем товары
    proc1 = Product('i9', 100, 5, cat_proc)
    proc2 = Product('i7', 75, 4.5, cat_proc)
    proc3 = Product('i5', 50, 4, cat_proc)
    mtb1 = Product('x570', 50, 4.9, cat_mother_boards)
    mtb2 = Product('x470', 30, 4.3, cat_mother_boards)
    mtb3 = Product('x370', 20, 3.8, cat_mother_boards)
    hdd1 = Product('intel', 30, 4.8, cat_hdd)
    hdd2 = Product('wd', 25, 4.6, cat_hdd)
    hdd3 = Product('seagate', 19, 4.4, cat_hdd)

    # Product.show_all_products()  # Посмотреть все товары
    # Market.show_all_categories()  # Посмотреть все товары
    # cat_hdd.show_products()  # Посмотреть все товары категория hdd
    # cat_proc.show_products()  # Посмотреть все товары категория Процессоры
    # cat_mother_boards.show_products()  # Посмотреть все товары категория Мат платы

    ivan = User(login='login', password='password', name='ivan')
    anna = User(login='login1', password='password1', name='anna')
    olga = User(login='login2', password='password2', name='olga')

    login = input('Введите логин: ')
    password = input('Введите пароль: ')
    user = User.autentification(login, password)
    Market.show_goods(user)
