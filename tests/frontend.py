import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
from img_ploter import kde
from minimum_convex_polygon import MCP

class MyWidget(QWidget):
    def __init__(self, tab_window):
        super().__init__()
        self.tab_window = tab_window
        self.initUI()

    def initUI(self):
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
        self.process_button.clicked.connect(self.process_file)
        self.process_button.setEnabled(False)
        self.process_button.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px"
        )
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

        # Create widgets to contain labels and buttons
        file_label_widget = QWidget()
        file_label_layout = QHBoxLayout(file_label_widget)
        file_label_layout.addWidget(file_label)
        file_label_layout.addWidget(self.selected_file_label)
        file_label_layout.addWidget(select_button)
        file_label_layout.setSpacing(10)
        file_label_layout.setAlignment(Qt.AlignCenter)

        process_button_widget = QWidget()
        process_button_layout = QHBoxLayout(process_button_widget)
        process_button_layout.addWidget(self.process_button)
        process_button_layout.setAlignment(Qt.AlignCenter)

        error_label_widget = QWidget()
        error_label_layout = QHBoxLayout(error_label_widget)
        error_label_layout.addWidget(self.error_label)
        error_label_layout.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        vbox.addWidget(file_label_widget)
        vbox.addWidget(process_button_widget)
        vbox.addWidget(error_label_widget)
        vbox.addStretch(1)
        vbox.setContentsMargins(20, 20, 20, 20)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file_label.setText(file_path)
            self.process_button.setEnabled(True)
            self.clear_error()

    def process_file(self):
        if self.selected_file_label.text().endswith(".csv"):
            self.tab_window.file_path = self.selected_file_label.text()
            self.tab_window.showMaximized()
            self.clear_error()
        else:
            self.show_error("Error: Only CSV files (*.csv) can be processed.")

    def show_error(self, message):
        self.error_label.setText(message)

    def clear_error(self):
        self.error_label.clear()

class TabWindow(QWidget):
    img_day = None
    img_night = None
    conf_val = 95

    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.initUI()

    def initUI(self):
        self.select_text = ""
        self.file_path = None
        self.setStyleSheet("background-color: grey;")

        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        select_frame = QFrame()
        select_frame.setStyleSheet("background-color: black;")
        select_frame.setFixedWidth(int(screen_width * 0.2))

        select_layout = QVBoxLayout(select_frame)
        select_layout.setContentsMargins(int(screen_width * 0.02), 0, int(screen_width * 0.02), 0)
        select_layout.setSpacing(10)
        select_layout.setAlignment(Qt.AlignTop)

        margin_spacer = QSpacerItem(int(screen_width * 0.1), int(screen_height * 0.20), QSizePolicy.Minimum, QSizePolicy.Fixed)
        select_layout.addItem(margin_spacer)

        select_algorithm = QComboBox()
        select_algorithm.addItem("Choose your algorithm")
        select_algorithm.addItems(["MCP", "KDE"])
        select_algorithm.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")

        self.text_box = QLineEdit()
        self.text_box.setPlaceholderText("Enter something...")
        self.text_box.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.text_box.setVisible(False)

        self.start_button = QPushButton("Start")
        self.start_button.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.start_button.setVisible(False)
        self.start_button.clicked.connect(self.start_process)

        spacer_item = QSpacerItem(int(screen_width * 0.01), int(screen_height * 0.03), QSizePolicy.Minimum, QSizePolicy.Fixed)

        # Wrap result_box in a QWidget
        self.result_box_widget = QWidget()
        result_box_layout = QVBoxLayout(self.result_box_widget)
        self.result_box = QLabel("Result")
        self.result_box.setAlignment(Qt.AlignCenter)
        self.result_box.setStyleSheet(
            "background-color: black; padding: 10px 18px; border: none; border-radius: 5px; font-size: 16px; color: white;"
        )
        self.result_box.setVisible(False)
        result_box_layout.addWidget(self.result_box)
        result_box_layout.setContentsMargins(0, 0, 0, 0)
        result_box_layout.setSpacing(0)

        self.text_boxs = QLineEdit()
        self.text_boxs.setPlaceholderText("Confidence Interval (7-100)")
        self.text_boxs.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.text_boxs.setVisible(False)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")

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
        self.back_button.setVisible(True)
        self.back_button.clicked.connect(self.go_back)

        select_algorithm.currentTextChanged.connect(self.show_hide_widgets)

        select_layout.addWidget(select_algorithm)
        select_layout.addItem(spacer_item)
        select_layout.addWidget(self.text_box)
        select_layout.addWidget(self.text_boxs)
        select_layout.addWidget(self.error_label)
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

        self.setLayout(layout)
        self.setGeometry(100, 100, screen_geometry.width() - 200, screen_geometry.height() - 200)

        # Ensure labels are set correctly
        self.label1 = QLabel()
        self.label2 = QLabel()
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.frame1.setLayout(self.layout1)
        self.frame2.setLayout(self.layout2)

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
        if self.file_path:
            if self.select_text == "KDE":
                float_kde = self.text_box.text()
                try:
                    float_value_kde = float(float_kde)
                    if not (0 <= float_value_kde <= 1):
                        raise ValueError("Value must be between 0 and 1")
                    else:
                        self.clear_error()
                except ValueError as e:
                    self.error_label.setText(f"Error: {str(e)}")
                    self.result_box.setVisible(False)
                    self.download_button.setVisible(False)
                    self.clear_displayed_images()
                    return
                try:
                    day_kde, night_kde = kde(self.file_path, float_value_kde)
                    self.img_day, self.img_night = day_kde, night_kde
                    self.load_image_into_frame_day(day_kde)
                    self.load_image_into_frame_night(night_kde)
                except ValueError:
                    self.error_label.setText("Error: Invalid float value")
                    return
            elif self.select_text == "MCP":
                float_value_str = self.text_boxs.text()
                try:
                    float_value = float(float_value_str)
                    if not (7 <= float_value <= 100):
                        raise ValueError("Value must be between 7 and 100")
                    else:
                        self.clear_error()
                except ValueError as e:
                    self.error_label.setText(f"Error: {str(e)}")
                    self.result_box.setVisible(False)
                    self.download_button.setVisible(False)
                    self.clear_displayed_images()
                    return
                day_mcp, night_mcp, day_area, night_area, total_area = MCP(self.file_path, 0.5, float_value)
                self.load_image_into_frame_day(day_mcp)
                self.load_image_into_frame_night(night_mcp)
                self.img_day, self.img_night = day_mcp, night_mcp
                self.update_result_box(day_area, night_area, total_area)
                self.result_box.setVisible(True)
                self.update_data_frame_view()
            else:
                self.error_label.setText("Error: No algorithm selected.")
                return
            self.download_button.setVisible(True)

    def update_result_box(self, day_area, night_area, total_area):
        result_text = f"Day Area: {day_area} km²\nNight Area: {night_area} km²\nTotal Area: {total_area} km²"
        self.result_box.setText(result_text)

    def clear_error(self):
        self.error_label.clear()

    def clear_displayed_images(self):
        self.label1.clear()
        self.label2.clear()

    def load_image_into_frame_day(self, image_buffer):
        pixmap = self.convert_buffer_to_pixmap(image_buffer)
        scaled_width = int(self.frame1.width() * 0.6)
        pixmap = pixmap.scaledToWidth(scaled_width, Qt.SmoothTransformation)
        self.label1.setPixmap(pixmap)
        self.label1.setAlignment(Qt.AlignCenter)
        self.layout1.addWidget(self.label1)

    def load_image_into_frame_night(self, image_buffer):
        pixmap = self.convert_buffer_to_pixmap(image_buffer)
        scaled_width = int(self.frame2.width() * 0.6)
        pixmap = pixmap.scaledToWidth(scaled_width, Qt.SmoothTransformation)
        self.label2.setPixmap(pixmap)
        self.label2.setAlignment(Qt.AlignCenter)
        self.layout2.addWidget(self.label2)

    def convert_buffer_to_pixmap(self, image_buffer):
        image_buffer.seek(0)
        img = QImage.fromData(image_buffer.read())
        pixmap = QPixmap.fromImage(img)
        return pixmap

    def save_mcp(self, day_mcp, night_mcp):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.img_day = self.convert_buffer_to_pixmap(day_mcp)
            self.img_night = self.convert_buffer_to_pixmap(night_mcp)
            self.img_day.save(f"{directory}/day_mcp.tiff")
            self.img_night.save(f"{directory}/night_mcp.tiff")
            from img_ploter import dist
            data = dist(self.file_path)
            df = pd.DataFrame(data)
            df.to_excel(f"{directory}/output.xlsx", index=False)
        else:
            self.error_label.setText("No directory selected for saving files.")

    def save_kde(self, day_kde, night_kde):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.kde_day = self.convert_buffer_to_pixmap(day_kde)
            self.kde_night = self.convert_buffer_to_pixmap(night_kde)
            self.kde_day.save(f"{directory}/day_kde.tiff")
            self.kde_night.save(f"{directory}/night_kde.tiff")
        else:
            self.error_label.setText("No directory selected for saving files.")

    def download_files(self):
        if self.select_text == "MCP":
            if self.img_day and self.img_night:
                self.save_mcp(self.img_day, self.img_night)
            else:
                self.error_label.setText("Error: Image buffers are not properly initialized.")
        elif self.select_text == "KDE":
            if self.img_day and self.img_night:
                self.save_kde(self.img_day, self.img_night)
            else:
                self.error_label.setText("Error: Image buffers are not properly initialized.")

    def go_back(self):
        self.hide()
        self.main_widget.show()
        self.clear_displayed_images()
        self.result_box.setVisible(False)
        self.text_box.clear()
        self.text_boxs.clear()
        self.download_button.setVisible(False)

    def closeEvent(self, event):
        self.hide()
        self.main_widget.show()
        event.ignore()

    def update_data_frame_view(self):
        from img_ploter import dist

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

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._df.columns[section]
            if orientation == Qt.Vertical:
                return self._df.index[section]
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("File Selector")

    pixmap = QPixmap("nature.jpg")
    background_label = QLabel(main_window)
    background_label.setPixmap(pixmap)
    background_label.setAlignment(Qt.AlignCenter)
    background_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    screen_geometry = app.primaryScreen().geometry()
    background_label.resize(screen_geometry.size())
    main_window.setGeometry(screen_geometry)

    overlay_frame = QFrame(main_window)
    overlay_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2)")
    overlay_frame.setContentsMargins(0, 0, 0, 0)
    overlay_frame.setFixedSize(800, 600)

    tab_window = TabWindow(None)
    main_widget = MyWidget(tab_window)
    tab_window.main_widget = main_widget

    vbox = QVBoxLayout(main_window)
    vbox.addWidget(main_widget)
    main_window.setLayout(vbox)

    def center_overlay():
        overlay_frame.move(
            (main_window.width() - overlay_frame.width()) // 2,
            (main_window.height() - overlay_frame.height()) // 2,
        )

    main_window.resizeEvent = lambda event: center_overlay()

    main_window.showMaximized()
    center_overlay()
    sys.exit(app.exec())
