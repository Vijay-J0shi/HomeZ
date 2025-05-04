# I made this to be the main window for my app
# It lets you pick a csv and run MCP or KDE stuff
# Shows pics and data in a table

import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QComboBox, QLineEdit, QFrame, QTableView,
    QSpacerItem, QSizePolicy, QStackedWidget
)
from PyQt6.QtGui import QPixmap, QImage, QGuiApplication
from PyQt6.QtCore import Qt
from pandas_model import PandasModel
from logging_setup import start_log

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from home_range.kde_img_ploter import kde, dist
from home_range.minimum_convex_polygon import MCP

class Win(QWidget):
    day_img = None
    night_img = None
    conf = 95

    def __init__(self):
        super().__init__()
        self.log = start_log()
        self.setWindowTitle("Range App")
        self.file = None
        self.build_ui()
        
    def build_ui(self):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
        layout = QVBoxLayout(self)
        img_path = os.path.join(os.path.dirname(__file__), "src", "images", "HomeZ_bg1.jpg")
        bg = QPixmap(img_path)
        self.bg_lab = QLabel(self)
        self.bg_lab.setPixmap(bg)
        self.bg_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bg_lab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        scr = QGuiApplication.primaryScreen().geometry()
        self.bg_lab.resize(scr.size())
        self.setGeometry(scr)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.file_win = QWidget()
        self.setup_file_ui()
        self.stack.addWidget(self.file_win)

        self.proc_win = QWidget()
        self.setup_proc_ui()
        self.stack.addWidget(self.proc_win)

        self.showMaximized()

    def setup_file_ui(self):
        lab = QLabel("File:")
        lab.setStyleSheet("font-weight: bold; font-size: 14px; color: #fff")
        
        self.file_lab = QLabel("None")
        self.file_lab.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.7); color: #333; padding: 5px; border-radius: 5px"
        )

        btn = QPushButton("Pick")
        btn.clicked.connect(self.pick_file)
        btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px"
        )

        self.run_btn = QPushButton("Go")
        self.run_btn.clicked.connect(self.go_proc)
        self.run_btn.setEnabled(False)
        self.run_btn.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px"
        )

        self.err = QLabel()
        self.err.setStyleSheet("color: red")

        row1 = QWidget()
        lay1 = QHBoxLayout(row1)
        lay1.addWidget(lab)
        lay1.addWidget(self.file_lab)
        lay1.addWidget(btn)
        lay1.setSpacing(10)
        lay1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row2 = QWidget()
        lay2 = QHBoxLayout(row2)
        lay2.addWidget(self.run_btn)
        lay2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        row3 = QWidget()
        lay3 = QHBoxLayout(row3)
        lay3.addWidget(self.err)
        lay3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        box = QVBoxLayout(self.file_win)
        box.addStretch(1)
        box.addWidget(row1)
        box.addWidget(row2)
        box.addWidget(row3)
        box.addStretch(1)
        box.setContentsMargins(20, 20, 20, 20)

    def setup_proc_ui(self):
        self.proc_win.setStyleSheet("background-color: grey;")
        scr = QGuiApplication.primaryScreen().geometry()
        w = scr.width()
        h = scr.height()

        lay = QHBoxLayout(self.proc_win)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        panel = QFrame()
        panel.setStyleSheet("background-color: black;")
        panel.setFixedWidth(int(w * 0.2))
        panel_lay = QVBoxLayout(panel)
        panel_lay.setContentsMargins(int(w * 0.02), 0, int(w * 0.02), 0)
        panel_lay.setSpacing(10)
        panel_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        spc = QSpacerItem(int(w * 0.1), int(h * 0.20), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        panel_lay.addItem(spc)

        algo = QComboBox()
        algo.addItem("Pick algo")
        algo.addItems(["MCP", "KDE"])
        algo.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")

        self.bw = QLineEdit()
        self.bw.setPlaceholderText("Bandwidth (0-1)")
        self.bw.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.bw.setVisible(False)

        self.cf = QLineEdit()
        self.cf.setPlaceholderText("Conf (7-100)")
        self.cf.setStyleSheet("background-color: white; color: black; min-height: 40px; font-size: 16px;")
        self.cf.setVisible(False)

        self.start = QPushButton("Start")
        self.start.setStyleSheet(
            "background-color: #008CBA; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.start.setVisible(False)
        self.start.clicked.connect(self.do_proc)

        gap = QSpacerItem(int(w * 0.01), int(h * 0.03), QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.res_box = QWidget()
        res_lay = QVBoxLayout(self.res_box)
        self.res = QLabel("Result")
        self.res.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.res.setStyleSheet(
            "background-color: black; padding: 10px 18px; border: none; border-radius: 5px; font-size: 16px; color: white;"
        )
        self.res.setVisible(False)
        res_lay.addWidget(self.res)
        res_lay.setContentsMargins(0, 0, 0, 0)
        res_lay.setSpacing(0)

        self.err2 = QLabel()
        self.err2.setStyleSheet("color: red")

        self.save = QPushButton("Save")
        self.save.clicked.connect(self.save_files)
        self.save.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.save.setVisible(False)

        self.back = QPushButton("Back")
        self.back.setStyleSheet(
            "background-color: #f44336; color: white; font-weight: bold; padding: 10px 24px; border: none; border-radius: 5px; min-height: 30px; font-size: 16px;"
        )
        self.back.clicked.connect(self.go_file)

        algo.currentTextChanged.connect(self.show_hide)

        panel_lay.addWidget(algo)
        panel_lay.addItem(gap)
        panel_lay.addWidget(self.bw)
        panel_lay.addWidget(self.cf)
        panel_lay.addWidget(self.err2)
        panel_lay.addItem(gap)
        panel_lay.addWidget(self.start)
        panel_lay.addItem(gap)
        panel_lay.addWidget(self.res_box)
        panel_lay.addItem(gap)
        panel_lay.addWidget(self.save)
        panel_lay.addItem(gap)
        panel_lay.addWidget(self.back)

        lay.addWidget(panel)

        imgs = QVBoxLayout()
        self.day = QWidget()
        self.day.setStyleSheet("background-color: #fff; border: 2px solid #333; border-radius: 10px;")
        self.day.setFixedSize(int(w * 0.45), int(h * 0.47))

        self.night = QWidget()
        self.night.setStyleSheet("background-color: #fff; border: 2px solid #333; border-radius: 10px;")
        self.night.setFixedSize(int(w * 0.45), int(h * 0.47))

        imgs.setContentsMargins(int(w * 0.061), int(h * 0.01), int(w * 0.036), int(h * 0.01))
        imgs.addWidget(self.day)
        imgs.addWidget(self.night)
        lay.addLayout(imgs)

        tbl = QVBoxLayout()
        self.tbl = QTableView()
        self.tbl.setVisible(False)
        self.tbl.setMinimumWidth(int(w * 0.250))
        tbl.addWidget(self.tbl)
        lay.addLayout(tbl)

        filler = QWidget()
        lay.addWidget(filler)
        lay.setStretchFactor(filler, 1)

        self.day_lab = QLabel()
        self.night_lab = QLabel()
        self.day_lay = QVBoxLayout()
        self.night_lay = QVBoxLayout()
        self.day.setLayout(self.day_lay)
        self.night.setLayout(self.night_lay)

    def pick_file(self):
        try:
            f, _ = QFileDialog.getOpenFileName(self, "Pick File", "", "CSV Files (*.csv)")
            if f:
                self.file_lab.setText(f)
                self.file = f
                self.run_btn.setEnabled(True)
                self.clr_err()
                self.log.info(f"Got file: {f}")
        except Exception as e:
            self.show_err(f"File error: {str(e)}")
            self.log.error(f"File pick error: {str(e)}")

    def go_proc(self):
        if self.file and self.file.endswith(".csv"):
            self.stack.setCurrentWidget(self.proc_win)
            self.clr_err()
            self.log.info(f"Going to proc with: {self.file}")
        else:
            self.show_err("Need a CSV file")
            self.log.warning("Bad file type")

    def go_file(self):
        self.stack.setCurrentWidget(self.file_win)
        self.clr_imgs()
        self.res.setVisible(False)
        self.bw.clear()
        self.cf.clear()
        self.save.setVisible(False)
        self.tbl.setVisible(False)
        self.log.info("Back to file pick")

    def show_hide(self, txt):
        self.algo = txt
        self.save.setVisible(False)
        if txt == "KDE":
            self.bw.setVisible(True)
            self.cf.setVisible(False)
            self.start.setVisible(True)
            self.res.setVisible(False)
            self.clr_err()
        elif txt == "MCP":
            self.bw.setVisible(False)
            self.cf.setVisible(True)
            self.start.setVisible(True)
            self.res.setVisible(False)
        else:
            self.bw.setVisible(False)
            self.cf.setVisible(False)
            self.start.setVisible(False)
            self.res.setVisible(False)
            self.clr_err()

    def do_proc(self):
        self.log.info(f"Starting proc on: {self.file}")
        if not self.file:
            self.err2.setText("No file picked")
            self.log.warning("No file")
            return

        if self.algo == "KDE":
            val = self.bw.text().strip()
            self.log.info(f"KDE val: {val}")
            if not val:
                self.err2.setText("Need bandwidth (0-1)")
                self.log.warning("No bandwidth")
                return
            try:
                num = float(val)
                if not 0 <= num <= 1:
                    raise ValueError("Must be 0-1")
                self.clr_err()
            except ValueError as e:
                self.err2.setText(f"Error: {str(e)}")
                self.log.error(f"KDE err: {str(e)}")
                return
            try:
                self.log.info(f"Run KDE: {self.file}, {num}")
                d, n = kde(self.file, num)
                self.day_img, self.night_img = d, n
                self.load_day(d)
                self.load_night(n)
                self.log.info("KDE done")
            except Exception as e:
                self.err2.setText(f"Error: {str(e)}")
                self.log.error(f"KDE crash: {str(e)}")
                return

        elif self.algo == "MCP":
            val = self.cf.text().strip()
            self.log.info(f"MCP val: {val}")
            if not val:
                self.err2.setText("Need conf (7-100)")
                self.log.warning("No conf")
                return
            try:
                num = float(val)
                if not 7 <= num <= 100:
                    raise ValueError("Must be 7-100")
                self.clr_err()
            except ValueError as e:
                self.err2.setText(f"Error: {str(e)}")
                self.log.error(f"MCP err: {str(e)}")
                return
            try:
                self.log.info(f"Run MCP: {self.file}, {num}")
                d, n, da, na, ta = MCP(self.file, 0.5, num)
                self.day_img, self.night_img = d, n
                self.load_day(d)
                self.load_night(n)
                self.show_res(da, na, ta)
                self.res.setVisible(True)
                self.show_tbl()
                self.log.info("MCP done")
            except Exception as e:
                self.err2.setText(f"Error: {str(e)}")
                self.log.error(f"MCP crash: {str(e)}")
                return
        else:
            self.err2.setText("Pick an algo")
            self.log.warning("No algo")
            return

        self.save.setVisible(True)

    def show_res(self, da, na, ta):
        txt = f"Day: {da} km²\nNight: {na} km²\nTotal: {ta} km²"
        self.res.setText(txt)

    def clr_err(self):
        self.err.clear()
        self.err2.clear()

    def clr_imgs(self):
        self.day_lab.clear()
        self.night_lab.clear()

    def load_day(self, img):
        pix = self.to_pix(img)
        w = int(self.day.width() * 0.6)
        pix = pix.scaledToWidth(w, Qt.TransformationMode.SmoothTransformation)
        self.day_lab.setPixmap(pix)
        self.day_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.day_lay.addWidget(self.day_lab)

    def load_night(self, img):
        pix = self.to_pix(img)
        w = int(self.night.width() * 0.6)
        pix = pix.scaledToWidth(w, Qt.TransformationMode.SmoothTransformation)
        self.night_lab.setPixmap(pix)
        self.night_lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.night_lay.addWidget(self.night_lab)

    def to_pix(self, buf):
        if hasattr(buf, 'getvalue'):
            data = buf.getvalue()
        else:
            data = buf
        img = QImage.fromData(data)
        return QPixmap.fromImage(img)

    def save_mcp(self, d, n):
        dir = QFileDialog.getExistingDirectory(self, "Pick Folder")
        if dir:
            if hasattr(d, 'getvalue'):
                dp = self.to_pix(d)
                np = self.to_pix(n)
            else:
                dp = QPixmap.fromImage(QImage.fromData(d))
                np = QPixmap.fromImage(QImage.fromData(n))
            dp.save(f"{dir}/day_mcp.tiff")
            np.save(f"{dir}/night_mcp.tiff")
            data = dist(self.file)
            df = pd.DataFrame(data)
            df.to_excel(f"{dir}/output.xlsx", index=False)
            self.log.info(f"Saved MCP to {dir}")
        else:
            self.err2.setText("No folder picked")
            self.log.warning("No folder")

    def save_kde(self, d, n):
        dir = QFileDialog.getExistingDirectory(self, "Pick Folder")
        if dir:
            if hasattr(d, 'getvalue'):
                dp = self.to_pix(d)
                np = self.to_pix(n)
            else:
                dp = QPixmap.fromImage(QImage.fromData(d))
                np = QPixmap.fromImage(QImage.fromData(n))
            dp.save(f"{dir}/day_kde.tiff")
            np.save(f"{dir}/night_kde.tiff")
            self.log.info(f"Saved KDE to {dir}")
        else:
            self.err2.setText("No folder picked")
            self.log.warning("No folder")

    def save_files(self):
        if self.algo == "MCP":
            if self.day_img and self.night_img:
                self.save_mcp(self.day_img, self.night_img)
            else:
                self.err2.setText("Images not ready")
                self.log.error("MCP imgs missing")
        elif self.algo == "KDE":
            if self.day_img and self.night_img:
                self.save_kde(self.day_img, self.night_img)
            else:
                self.err2.setText("Images not ready")
                self.log.error("KDE imgs missing")

    def show_tbl(self):
        data = dist(self.file)
        df = pd.DataFrame(data)
        model = PandasModel(df)
        self.tbl.setModel(model)
        self.tbl.setVisible(True)
        w = self.tbl.width()
        cw = w // df.shape[1]
        for c in range(df.shape[1]):
            self.tbl.setColumnWidth(c, cw)
        self.tbl.resizeColumnsToContents()
        self.tbl.resizeRowsToContents()

    def show_err(self, msg):
        self.err.setText(msg)