# main.py (fragmento) database inicialization
from utils.db import create_connection
from ui.app import App

if __name__ == "__main__":
    App(create_connection).mainloop()