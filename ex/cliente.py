import os
from datetime import date, datetime


def fmt_datetime(dt):
    if type(dt) == date:
        dt = datetime(dt.year, dt.month, dt.day)
    return dt.isoformat()


def apaga_arquivo(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)
