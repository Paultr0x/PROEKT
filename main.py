from time import sleep
import flet as ft
from flet import *
from flet_core import AppBar, ButtonStyle
import requests
from bs4 import BeautifulSoup

Results = []

class UniversityPlace():
    code = ""
    name = ""
    price = -1
    universityName = ""

    def __cmp__(self, other):
        if self.price < other.price:
            return -1
        elif self.price == other.price:
            return 0
        else:
            return 1

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    def __str__(self) -> str:
        return self.universityName + "," + self.code + "," + self.name + "," + str(self.price)

    def isValid(self):
        c = self.code.split(".")
        isValidCode = len(c) == 3 and c[1].isdecimal() and c[2].isdecimal() and c[3].isdecimal()
        return self.name != "" and self.price >= -1 and isValidCode and self.universityName != ""

    def __init__(self, UniversityName, code, name, price):
        self.universityName = UniversityName.strip()
        self.code = code.strip()
        self.name = name.strip()
        self.price = int(price)

#Парсинг сайтов вузов
def ParseMTUCI():
    url = "https://mtuci.ru/education/paid/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.findAll('tbody')

    for t in tables:
        for row in t:
            try:
                data = row.findAll('td')
                code = data[0].text.strip()
                name = data[1].text.strip().replace("\n", " ")
                price = data[2].text.strip().replace(" ", "")
                res = UniversityPlace("МТУСИ", code, name, price)
                Results.append(res)
            except Exception as e:
                pass


def ParseMADI():
    url = "https://pk.madi.ru/4501-stoimost-obucheniya-po-programmam.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.findAll('tbody')

    for t in tables:
        for row in t:
            try:
                data = row.findAll('td')
                code = data[1].text.strip()
                name = data[0].text.strip().replace("\n", " ")
                price = data[4].text.strip().replace(" ", "")
                if not price.isdigit():
                    continue
                res = UniversityPlace("МАДИ", code, name, price)
                Results.append(res)
            except Exception as e:
                pass

def ParseMTUCIFREE():
    url = "https://abitur.mtuci.ru/admission/firstcourse_budget/detail.php?ide=4099&ids=356"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for i in soup.findAll(class_="show_bio"):
        try:
            label = i.text.strip().split("-")
            code = label[0]
            name = label[1]
            res = UniversityPlace("МТУСИ", code, name, 0)
            if res.isValid:
                Results.append(res)
        except IndexError:
            pass

def ParseMADIFREE():
    url = "https://pk.madi.ru/46-napravleniya-podgotovki-bakalavriata-i-specialiteta.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.findAll('tbody')

    for t in tables:
        for row in t:
            try:
                data = row.findAll('td')
                code = data[1].text.strip()
                name = data[2].text.strip().replace("\n", " ")
                price = "0"
                if code in "Шифр":
                    continue

                # print(code, name,price)
                res = UniversityPlace("МАДИ", code, name, price)
                # if res.isValid():
                #    print(str(res))
                Results.append(res)
            except Exception as e:
                pass


def ParseMPEI():
    url = "https://pk.mpei.ru/info/speclist.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    tables = soup.findAll(class_="item_spec")
    pricesBlocks = soup.findAll(class_="spec_info center")
    prices = []
    for i in pricesBlocks:
        try:

            if "Стоимость" in i.text:
                if "руб" in i.text:
                    pr = float(i.text.split(" ")[0].replace(",", ".")) * 1000
                    prices.append(pr)
                else:
                    prices.append(-1)

        except:
            pass
    for i in range(len(prices)):
        t = tables[i]
        p = prices[i]
        label = t.text.strip().split("\r\n")
        code = label[0]
        name = label[1]
        Results.append(UniversityPlace("МЭИ", code, name, p))


def CollectResults():
    ParseMPEI()
    ParseMTUCI()
    ParseMTUCIFREE()
    ParseMADI()
    ParseMADIFREE()
    return Results


if __name__ == "__main__":
    ParseMPEI()
    ParseMTUCI()
    ParseMADI()
    ParseMADIFREE()
    ParseMTUCIFREE()

Table: ft.DataTable = None
Results = []

# работа с интерфейсом
def main(page: ft.Page):
    global Table
    page.title = "Программа для облегчения жизни студента"
    page.add(ft.Stack([ft.Text(spans=[ft.TextSpan("Обучение:", ft.TextStyle(size=40, weight=ft.FontWeight.BOLD,
                                                                            foreground=ft.Paint(
                                                                                color=ft.colors.RED,
                                                                                stroke_width=6,
                                                                                stroke_join=ft.StrokeJoin.ROUND,
                                                                                style=ft.PaintingStyle.STROKE, ), ), ), ], ),
                       ft.Text(spans=[ft.TextSpan("Обучение:", ft.TextStyle(size=40, weight=ft.FontWeight.BOLD,
                                                                            color=ft.colors.BLACK, ), ), ], ), ]))

    page.update()

    # Реализация кнопок
    drop = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Бюджетное"),
            ft.dropdown.Option("Платное"),
        ],
    )
    #Реализация поиска
    searchName = Container(width=320, bgcolor="Red", border_radius=10, padding=8,
                           content=Row(spacing=10, vertical_alignment=CrossAxisAlignment.CENTER, controls=[
                               Icon(name=icons.SEARCH_ROUNDED, size=17, opacity=0.85),
                               TextField(border_color="red", height=20, text_size=14, content_padding=0,
                                         cursor_color="white", cursor_width=1, color="White",
                                         hint_text="Введите аббревиатуру вуза")
                           ], ), )
    searchCode = Container(width=320, bgcolor="Red", border_radius=10, padding=8,
                           content=Row(spacing=10, vertical_alignment=CrossAxisAlignment.CENTER, controls=[
                               Icon(name=icons.SEARCH_ROUNDED, size=17, opacity=0.85),
                               TextField(border_color="red", height=20, text_size=14, content_padding=0,
                                         cursor_color="white", cursor_width=1, color="White",
                                         hint_text="Введите код направления")
                           ], ), )

    # Выбор параметров
    def add_button(e):
        fillTable(drop.value, searchName.content.controls[1].value, searchCode.content.controls[1].value)
        page.update()

    output_text = ft.Text()
    submit_btn = ft.ElevatedButton(text="ОК", on_click=add_button)

    page.add(Row([drop, searchName, searchCode]), submit_btn, output_text)

    # Вывод результатов
    Table = ft.DataTable(width=1000,
                         bgcolor="RED",
                         border=ft.border.all(2, "BLACK"),
                         border_radius=30,
                         vertical_lines=ft.border.BorderSide(2, "BLACK"),
                         horizontal_lines=ft.border.BorderSide(1, "BLACK"),
                         columns=[
                             ft.DataColumn(ft.Text("№")),
                             ft.DataColumn(ft.Text("Университет")),
                             ft.DataColumn(ft.Text("Код")),
                             ft.DataColumn(ft.Text("Направление")),
                             ft.DataColumn(ft.Text("Стоимость")),
                         ],
                         rows=[],
                         )

    page.add(Container(ft.ListView([Table]), border_radius=20, height=300))

    # Добавим выбор фона
    page.theme_mode = "light"
    page.splash = ft.ProgressBar(visible=False)

    def fon_style(e):
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()
        sleep(0.8)
        on_dark.selected = not on_dark.selected
        page.splash.visible = False
        page.update()

    on_dark = IconButton(on_click=fon_style, icon="dark_mode", selected_icon="light_mode",
                         style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}))
    page.add(AppBar(title=Text("Выбери университет своей мечты!"), bgcolor="Purple", leading=IconButton(icon="menu"),
                    actions=[on_dark]))


# Таблица с результатами
def fillTable(cost, universityName, code):
    code = code.replace(",", ".", 10)
    # Сортируем согласно критериям поиска
    sortedResults = []
    for i in Results:
        if cost == "Бюджетное":
            if i.price == 0:
                if universityName != "" and code == "":
                    if i.universityName == universityName:
                        sortedResults.append(i)
                elif code != "" and universityName == "":
                    if i.code == code:
                        sortedResults.append(i)
                elif universityName != "" and code != "":
                    if universityName == i.universityName and code == i.code:
                        sortedResults.append(i)
                else:
                    sortedResults.append(i)

        else:
            if i.price > 0:
                if universityName != "" and code == "":
                    if i.universityName == universityName:
                        sortedResults.append(i)
                elif code != "" and universityName == "":
                    if i.code == code:
                        sortedResults.append(i)
                elif universityName != "" and code != "":
                    if universityName == i.universityName and code == i.code:
                        sortedResults.append(i)
                else:
                    sortedResults.append(i)

    # Добавляем результаты в таблицу
    Table.rows = []
    for i in range(len(sortedResults)):
        try:
            Table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i + 1))),
                    ft.DataCell(ft.Text(sortedResults[i].universityName)),
                    ft.DataCell(ft.Text(sortedResults[i].code)),
                    ft.DataCell(ft.Text(sortedResults[i].name)),
                    ft.DataCell(ft.Text(sortedResults[i].price))
                ]
                ))
        except IndexError:
            break


# Конец
Results = CollectResults()
ft.app(target=main)
