from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor
from qfluentwidgets import FluentTranslator, SplitTitleBar

import sys
from PySide6.QtCore import Qt, QSize, QUrl, QLocale
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame

from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF


class LoginWindow(AcrylicWindow):

    def __init__(self):
        super().__init__()

        # change theme color
        setThemeColor('#28afe9')

        # change title bar
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('PyQt-Fluent-Widget')
        self.windowEffect.setMicaEffect(self.winId())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.installTranslator(FluentTranslator(QLocale()))
    w = LoginWindow()
    w.show()
    app.exec()


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # unique object name
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Widget('Home Interface', self)
        self.musicInterface = Widget('Music Interface', self)
        self.videoInterface = Widget('Video Interface', self)
        self.settingInterface = Widget('Setting Interface', self)
        self.albumInterface = Widget('Album Interface', self)
        self.albumInterface1 = Widget('Album Interface 1', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')
        self.addSubInterface(self.musicInterface, FIF.MUSIC, 'Music library')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')

        self.navigationInterface.addSeparator()

        self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums',
                             NavigationItemPosition.SCROLL)
        self.addSubInterface(self.albumInterface1,
                             FIF.ALBUM,
                             'Album 1',
                             parent=self.albumInterface)

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings',
                             NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
