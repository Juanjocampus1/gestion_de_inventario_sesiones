from PyQt5.QtWidgets import QListWidget

class SalesHistoryManager:
    def __init__(self, parent):
        self.parent = parent

    def create_sales_history_list(self):
        return QListWidget()

    def add_sale(self, sales_history, sale):
        sales_history.addItem(sale)