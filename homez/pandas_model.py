import pandas as pd
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QBrush, QColor

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df = df
    def rowCount(self, parent=None):
        return self._df.shape[0]
    def columnCount(self, parent=None):
        return self._df.shape[1]
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._df.iloc[index.row(), index.column()])
        elif role == Qt.ItemDataRole.ForegroundRole:
            return QBrush(QColor("white"))
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QBrush(QColor("#333"))
        return None
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._df.columns[section])
            return str(self._df.index[section])
        elif role == Qt.ItemDataRole.ForegroundRole:
            return QBrush(QColor("white"))
        elif role == Qt.ItemDataRole.BackgroundRole:
            return QBrush(QColor("#444"))
        return None