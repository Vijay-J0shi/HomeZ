import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QComboBox, QLineEdit, QFrame, QTableView, QSpacerItem, 
    QSizePolicy, QStackedWidget
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from pandas_model import PandasModel
from logging_setup import setup_logging

# Add parent directory to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import custom modules
from home_range.kde_img_ploter import kde, dist
from home_range.minimum_convex_polygon import MCP

class MainWindow(QWidget):
    img_day = None
    img_night = None
    conf_val = 95

    def __init__(self):
        super().__init__()
        self.logger = setup_logging()
        self.setWindowTitle("Home Range Analyzer")
        self.file_path = None
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
        main_layout = QVBoxLayout(self)

        pixmap = QPixmap(r"homez/src/images/HomeZ_bg1.jpg")
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.background_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        screen_geometry = QGuiApplication.primaryScreen().geometry()
        self.background_label.resize(screen_geometry.size())
        self.setGeometry(screen_geometry)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        self.file_selection_widget = QWidget()
        self.init_file_selection_ui()
        self.stacked_widget.addWidget(self.file_selection_widget)

        self.processing_widget = QWidget()
        self.init_processing_ui()
        self.stacked_widget.addWidget(self.processing_widget)

        self.showMaximized()

    def init_file_selection_ui(self):
        file_label = QLabel("Selected File:")
        file_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #fff")
        self.selected_file_label = QLabel("None")
        self.selected_file_label.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.7); color: #333; padding: 5px; border-radius: 5px"
        )
        select_button = QPushButton("Select File")
        select_button.clicked.connect(self.select_file)
        select_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px"
        )

        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.switch_to_processing)
        self.process_button.setEnabled(False)
        self.process_button.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px"
        )

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        file_label_widget = QWidget()
        file_label_layout = QHBoxLayout(file_label_widget)
        file_label_layout.addWidget(file_label)
        file_label_layout.addWidget(self.selected_file_label)
        file_label_layout.addWidget(select_button)
        file_label_layout.setSpacing(10)
        file_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        process_button_widget = QWidget()
        process_button_layout = QHBoxLayout(process_button_widget)
        process_button_layout.addWidget(self.process_button)
        process_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        error_label_widget = QWidget()
        error_label_layout = QHBoxLayout(error_label_widget)
        error_label_layout.addWidget(self.error_label)
        error_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox = QVBoxLayout(self.file_selection_widget)
        vbox.addStretch(1)
        vbox.addWidget(file_label_widget)
        vbox.addWidget(process_button_widget)
        vbox.addWidget(error_label_widget)
        vbox.addStretch(1)
        vbox.setContentsMargins(20, 20, 20, 20)

    def init_processing_ui(self):
        self.select_text = ""
        self.processing_widget.setStyleSheet("background-color: grey;")

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        layout = QHBoxLayout(self.processing_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        select_frame = QFrame()
        select_frame.setStyleSheet("background-color: black;")
        select_frame.setFixedWidth(int(screen_width * 0.2))

        select_layout = QVBoxLayout(select_frame)
        select_layout.setContentsMargins(int(screen_width * 0.02), 0, int(screen_width * 0.02), 0)
        select_layout.setSpacing(10)
        select_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        margin_spacer = QSpacerItem(int(screen_width * 0.1), int(screen_height * 0.20), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        select_layout.addItem(margin_spacer)

        select_algorithm = QComboBox()
        select_algorithm.addItem("Choose your algorithm")
        select_algorithm.addItems(["MCP", "KDE"])
        select_algorithm.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Enter bandwidth (0-1)...")
        self.text_box.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.text_box.setVisible(False)

        self.text_boxs = QLineEdit()
        self.text_boxs.setPlaceholderText("Confidence Interval (7-100)")
        self.text_boxs.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.text_boxs.setVisible(False)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.start_button.setVisible(False)
        self.start_button.clicked.connect(self.start_process)

        spacer_item = QSpacerItem(int(screen_width * 0.01), int(screen_height * 0.03), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.result_box_widget = QWidget()
        result_box_layout = QVBoxLayout(self.result_box_widget)
        self.result_box = QLabel("Result")
        self.result_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_box.setStyleSheet(
            "background-color: black; padding: 10px 18px; border: none; border-radius: 5px; font-size: 16px; color: white;"
        )
        self.result_box.setVisible(False)
        result_box_layout.addWidget(self.result_box)
        result_box_layout.setContentsMargins(0, 0, 0, 0)
        result_box_layout.setSpacing(0)

        self.error_label_proc = QLabel()
        self.error_label_proc.setStyleSheet("color: red")

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_files)
        self.download_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.download_button.setVisible(False)

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(
            "background-color: #f44336; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.back_button.clicked.connect(self.switch_to_file_selection)

        select_algorithm.currentTextChanged.connect(self.show_hide_widgets)

        select_layout.addWidget(select_algorithm)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.text_box)
        select_layout.addWidget(self.text_boxs)
        select_layout.addWidget(self.error_label_proc)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.start_button)
        select_layout.addItem(spacer_item)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.result_box_widget)
        select_layout.addItem(spacer_item)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.download_button)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.back_button)

        layout.addWidget(select_frame)

        frames_layout = QVBoxLayout()
        self.frame1 = QWidget()
        self.frame1.setStyleSheet("background-color: #fff; border: 2px solid #333; border-radius: 10px;")
        self.frame1.setFixedSize(int(screen_width * 0.45), int(screen_height * 0.47))

        self.frame2 = QWidget()
        self.frame2.setStyleSheet("background-color: #fff; border: 2px solid #333; border-radius: 10px;")
        self.frame2.setFixedSize(int(screen_width * 0.45), int(screen_height * 0.47))

        frames_layout.setContentsMargins(
            int(screen_width * 0.061), int(screen_height * 0.01), int(screen_width * 0.036), int(screen_height * 0.01)
        )
        frames_layout.addWidget(self.frame1)
        frames_layout.addWidget(self.frame2)

        layout.addLayout(frames_layout)

        right_layout = QVBoxLayout()
        self.data_frame_view = QTableView()
        self.data_frame_view.setVisible(False)
        self.data_frame_view.setMinimumWidth(int(screen_width * 0.250))
        right_layout.addWidget(self.data_frame_view)

        layout.addLayout(right_layout)

        right_margin = QWidget()
        layout.addWidget(right_margin)
        layout.setStretchFactor(right_margin, 1)

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.frame1.setLayout(self.layout1)
        self.frame2.setLayout(self.layout2)

    def select_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv)")
            if file_path:
                self.selected_file_label.setText(file_path)
                self.file_path = file_path
                self.process_button.setEnabled(True)
                self.clear_error()
                self.logger.info(f"Selected file: {file_path}")
        except Exception as e:
            self.show_error(f"Error selecting file: {str(e)}")
            self.logger.error(f"Error selecting file: {str(e)}")

    def switch_to_processing(self):
        if self.file_path and self.file_path.endswith(".csv"):
            self.stacked_widget.setCurrentWidget(self.processing_widget)
            self.clear_error()
            self.logger.info(f"Switching to processing view with file: {self.file_path}")
        else:
            self.show_error("Error: Only CSV files (*.csv) can be processed.")
            self.logger.warning("Invalid file format selected")

    def switch_to_file_selection(self):
        self.stacked_widget.setCurrentWidget(self.file_selection_widget)
        self.clear_displayed_images()
        self.result_box.setVisible(False)
        self.text_box.clear()
        self.text_boxs.clear()
        self.download_button.setVisible(False)
        self.data_frame_view.setVisible(False)
        self.logger.info("Switched back to file selection view")

    def show_hide_widgets(self, text):
        self.select_text = text
        self.download_button.setVisible(False)
        if text == "KDE":
            self.text_box.setVisible(True)
            self.text_boxs.setVisible(False)
            self.start_button.setVisible(True)
            self.result_box.setVisible(False)
            self.clear_error()
        elif text == "MCP":
            self.start_button.setVisible(True)
            self.text_box.setVisible(False)
            self.text_boxs.setVisible(True)
        else:
            self.text_box.setVisible(False)
            self.start_button.setVisible(False)
            self.result_box.setVisible(False)
            self.text_boxs.setVisible(False)
            self.clear_error()

    def start_process(self):
        self.logger.info(f"Starting process with file: {self.file_path}")
        if not self.file_path:
            self.error_label_proc.setText("Error: No file selected")
            self.logger.warning("No file selected")
            return

        if self.select_text == "KDE":
            float_kde = self.text_box.text().strip()
            self.logger.info(f"KDE bandwidth input: {float_kde}")
            if not float_kde:
                self.error_label_proc.setText("Error: Enter a bandwidth value (0-1)")
                self.logger.warning("Empty bandwidth")
                return
            try:
                float_value_kde = float(float_kde)
                if not (0 <= float_value_kde <= 1):
                    raise ValueError("Value must be between 0 and 1")
                self.clear_error()
            except ValueError as e:
                self.error_label_proc.setText(f"Error: {str(e)}")
                self.logger.error(f"KDE value error: {str(e)}")
                return
            try:
                self.logger.info(f"Calling kde with file: {self.file_path}, bandwidth: {float_value_kde}")
                day_kde, night_kde = kde(self.file_path, float_value_kde)
                self.logger.info(f"KDE returned: {day_kde}, {night_kde}")
                self.img_day, self.img_night = day_kde, night_kde
                self.load_image_into_frame_day(day_kde)
                self.load_image_into_frame_night(night_kde)
            except Exception as e:
                self.error_label_proc.setText(f"Error: {str(e)}")
                self.logger.error(f"KDE runtime error: {str(e)}")
                return

        elif self.select_text == "MCP":
            float_value_str = self.text_boxs.text().strip()
            self.logger.info(f"MCP confidence input: {float_value_str}")
            if not float_value_str:
                self.error_label_proc.setText("Error: Enter a confidence value (7-100)")
                self.logger.warning("Empty confidence")
                return
            try:
                float_value = float(float_value_str)
                if not (7 <= float_value <= 100):
                    raise ValueError("Value must be between 7 and 100")
                self.clear_error()
            except ValueError as e:
                self.error_label_proc.setText(f"Error: {str(e)}")
                self.logger.error(f"MCP value error: {str(e)}")
                return
            try:
                self.logger.info(f"Calling MCP with file: {self.file_path}, confidence: {float_value}")
                day_mcp, night_mcp, day_area, night_area, total_area = MCP(self.file_path, 0.5, float_value)
                self.logger.info(f"MCP returned: {day_mcp}, {night_mcp}, {day_area}, {night_area}, {total_area}")
                self.img_day, self.img_night = day_mcp, night_mcp
                self.load_image_into_frame_day(day_mcp)
                self.load_image_into_frame_night(night_mcp)
                self.update_result_box(day_area, night_area, total_area)
                self.result_box.setVisible(True)
                self.update_data_frame_view()
            except Exception as e:
                self.error_label_proc.setText(f"Error: {str(e)}")
                self.logger.error(f"MCP runtime error: {str(e)}")
                return
        else:
            self.error_label_proc.setText("Error: No algorithm selected.")
            self.logger.warning("No algorithm selected")
            return
        self.download_button.setVisible(True)
        self.logger.info("Process completed")

    def update_result_box(self, day_area, night_area, total_area):
        result_text = f"Day Area: {day_area} km²\nNight Area: {night_area} km²\nTotal Area: {total_area} km²"
        self.result_box.setText(result_text)

    def clear_error(self):
        self.error_label.clear()
        self.error_label_proc.clear()

    def clear_displayed_images(self):
        self.label1.clear()
        self.label2.clear()

    def load_image_into_frame_day(self, image_buffer):
        pixmap = self.convert_buffer_to_pixmap(image_buffer)
        scaled_width = int(self.frame1.width() * 0.6)
        pixmap = pixmap.scaledToWidth(scaled_width, Qt.TransformationMode.SmoothTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout1.addWidget(self.label1)

    def load_image_into_frame_night(self, image_buffer):
        pixmap = self.convert_buffer_to_pixmap(image_buffer)
        scaled_width = int(self.frame2.width() * 0.6)
        pixmap = pixmap.scaledToWidth(scaled_width, Qt.TransformationMode.SmoothTransformation)
        self.label2.setPixmap(pixmap)
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout2.addWidget(self.label2)

    def convert_buffer_to_pixmap(self, image_buffer):
        if hasattr(image_buffer, 'getvalue'):
            image_data = image_buffer.getvalue()
        else:
            image_data = image_buffer
        img = QImage.fromData(image_data)
        return QPixmap.fromImage(img)

    def save_mcp(self, day_mcp, night_mcp):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            if hasattr(day_mcp, 'getvalue'):
                day_pixmap = self.convert_buffer_to_pixmap(day_mcp)
                night_pixmap = self.convert_buffer_to_pixmap(night_mcp)
            else:
                day_pixmap = QPixmap.fromImage(QImage.fromData(day_mcp))
                night_pixmap = QPixmap.fromImage(QImage.fromData(night_mcp))
            day_pixmap.save(f"{directory}/day_mcp.tiff")
            night_pixmap.save(f"{directory}/night_mcp.tiff")
            data = dist(self.file_path)
            df = pd.DataFrame(data)
            df.to_excel(f"{directory}/output.xlsx", index=False)
            self.logger.info(f"Saved MCP files to {directory}")
        else:
            self.error_label_proc.setText("No directory selected for saving files.")
            self.logger.warning("No directory selected for saving MCP files")

    def save_kde(self, day_kde, night_kde):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            if hasattr(day_kde, 'getvalue'):
                day_pixmap = self.convert_buffer_to_pixmap(day_kde)
                night_pixmap = self.convert_buffer_to_pixmap(night_kde)
            else:
                day_pixmap = QPixmap.fromImage(QImage.fromData(day_kde))
                night_pixmap = QPixmap.fromImage(QImage.fromData(night_kde))
            day_pixmap.save(f"{directory}/day_kde.tiff")
            night_pixmap.save(f"{directory}/night_kde.tiff")
            self.logger.info(f"Saved KDE files to {directory}")
        else:
            self.error_label_proc.setText("No directory selected for saving files.")
            self.logger.warning("No directory selected for saving KDE files")

    def download_files(self):
        if self.select_text == "MCP":
            if self.img_day and self.img_night:
                self.save_mcp(self.img_day, self.img_night)
            else:
                self.error_label_proc.setText("Error: Image buffers are not properly initialized.")
                self.logger.error("Image buffers not initialized for MCP download")
        elif self.select_text == "KDE":
            if self.img_day and self.img_night:
                self.save_kde(self.img_day, self.img_night)
            else:
                self.error_label_proc.setText("Error: Image buffers are not properly initialized.")
                self.logger.error("Image buffers not initialized for KDE download")

    def update_data_frame_view(self):
        data = dist(self.file_path)
        df = pd.DataFrame(data)
        model = PandasModel(df)
        self.data_frame_view.setModel(model)
        self.data_frame_view.setVisible(True)
        total_width = self.data_frame_view.width()
        column_width = total_width // df.shape[1]
        for column in range(df.shape[1]):
            self.data_frame_view.setColumnWidth(column, column_width)
        self.data_frame_view.resizeColumnsToContents()
        self.data_frame_view.resizeRowsToContents()

    def show_error(self, message):
        self.error_label.setText(message)