from re import A
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton
from PyQt6.QtGui import QPixmap
import requests
import sys
from PyQt6 import uic
import logging


# я не хочу делать второй запрос, из-за этого упращаю систему сильно
GB_D = {}

def get_img(name, spn):	
	apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
	map_api_server = "https://static-maps.yandex.ru/v1"
	spn = f'{spn},{spn}'
	params = {'geocode': name, 'spn': spn, 'apikey': apikey}
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
		pass

		

	def update_label(self, widget_name: str):
		widget_name = self.tabWidget.currentWidget().objectName()
		if widget_name == 'first_player':
			name = self.chose_1.currentText()
			spn = self.spin_1.value()
		else:
			name = self.chose_2.currentText()
			spn = self.spin_2.value()
		logging.info(f'lol {name}, {spn}')
		dataimg = get_img(name, float(spn) / 1000)
		


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
