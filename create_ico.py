from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QStyleFactory, QMessageBox
from PIL import Image, UnidentifiedImageError
from icon_screen import Ui_Form
import sys


def create_ico():
	"""
	Utility to create ico file from image file
	DPM 04/16/2026
	"""

	class Window(QWidget):
		def __init__(self):
			super().__init__()
			self.ui = Ui_Form()
			self.ui.setupUi(self)

			self.ui.pushButton_selectFile.clicked.connect(self.get_file)
			self.ui.pushButton_convertFile.clicked.connect(self.convert_file)
			self.ui.pushButton_newFile.clicked.connect(self.new_file)

		
		def get_file(self):
			file_path = QFileDialog.getOpenFileName(self,"Open File","","All Files (*)")
			self.ui.lineEdit_filePath.setText(file_path[0])
			file = file_path[0][file_path[0].rfind('/')+1:file_path[0].rfind('.')] + ".ico"
			self.ui.lineEdit_fileName.setText(file)
			self.ui.label_result.setText(f'Selected File: {file_path[0][file_path[0].rfind('/')+1:]}')


		def convert_file(self):
			file = self.ui.lineEdit_filePath.text()
			new_file = file[0:file.rfind("/")+1] + self.ui.lineEdit_fileName.text()
			ico_file_name = self.ui.lineEdit_fileName.text()

			try:
				if not file:
					raise ValueError("No File Selected")
				elif not ico_file_name:
					raise ValueError("No file name given")

				# Load your image (PNG, JPG, etc.)
				img = Image.open(file)

				# Save as ICO with standard sizes
				# If sizes are not specified, it defaults to standard icon sizes
				img.save(new_file, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

				self.ui.label_result.setText(f'File saved as {self.ui.lineEdit_fileName.text()}')

				QMessageBox.information(self, "File Saved", f"File saved as {ico_file_name}")
			except ValueError as e:
				QMessageBox.critical(self, "Error", f"{e}")			
			except UnidentifiedImageError:
				QMessageBox.critical(self, "Error", f"Cannot identify image file: {file}")
			except FileNotFoundError:
				QMessageBox.warning(self, "Error", "The specified file was not found.")
			except Exception as e:
				QMessageBox.critical(self, "Unexpected Error", f"An error occurred: {str(e)}")
			finally:
				self.new_file()
				

		def new_file(self):
			self.ui.lineEdit_filePath.clear()
			self.ui.lineEdit_fileName.clear()
			self.ui.label_result.clear()
	

	app = QApplication(sys.argv)
	app.setStyle("Fusion")
	window = Window()
	window.show()
	sys.exit(app.exec())
