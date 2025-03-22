from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from PyQt6.QtGui import QPixmap
import requests
import sys
from PyQt6 import uic
import logging
from random import uniform


# я не хочу делать второй запрос, из-за этого упращаю систему сильно
GB_D = {
    "Париж": "2.3522,48.8566",    # Долгота: 2.3522, Широта: 48.8566
    "Москва": "37.6176,55.7558",  # Долгота: 37.6176, Широта: 55.7558
    "Лондон": "0.1276,51.5074",  # Долгота: -0.1276, Широта: 51.5074
    "Тула": "37.6184,54.1931"     # Долгота: 37.6184, Широта: 54.1931
}


def get_img(name, spn):
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    map_api_server = "https://static-maps.yandex.ru/v1?"
    spn = f'{spn},{spn}'

    kk = list(map(float, GB_D[name].split(',')))
    x = uniform(kk[0] - 0.5, kk[0] + 0.5)
    y = uniform(kk[1] - 0.5, kk[1] + 0.5)
    a = f'{x},{y}'
    
    params = {'ll': a, 'spn': spn, 'apikey': apikey, 'lang': 'ru_Ru'}
    response = requests.get(map_api_server, params=params)
    print(response.url)
    return response.content


class MainWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        uic.loadUi('findsity.ui', self)
        
        # coonnect button
        self.check.clicked.connect(self.info)
        self.send.clicked.connect(self.update_label)

    def info(self):
        widget_name = self.tabWidget.currentWidget().objectName()
        if widget_name == 'first_player':
            check = self.chose_2.currentText()
            answer = self.chose_1.currentText()
            if check == answer:
                self.res_1.setText("You Win")
            else:
                self.res_1.setText("You lose")
        else:
            check = self.chose_1.currentText()
            answer = self.chose_2.currentText()
            if check == answer:
                self.res_2.setText("You Win")
            else:
                self.res_2.setText("You lose")
      
    def update_label(self):
        widget_name = self.tabWidget.currentWidget().objectName()
        if widget_name == 'first_player':
            name = self.chose_1.currentText()
            spn = self.spin_1.value()
        else:
            name = self.chose_2.currentText()
            spn = self.spin_2.value()
        logging.info(f'lol {name}, {spn}')
        dataimg = get_img(name, float(spn) / 5000)
        image = QPixmap()
        image.loadFromData(dataimg)

        if widget_name == 'first_player':
            self.img_2.setPixmap(image)
        else:
            self.img_1.setPixmap(image)
        self.res_1.setText('')
        self.res_2.setText('')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]  %(lineno)d %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding='utf-8'),
            logging.StreamHandler()]
    )
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
