import os
import json
import urllib.request
from datetime import date, datetime


def fmt_datetime(dt):
    if type(dt) == date:
        dt = datetime(dt.year, dt.month, dt.day)
    return dt.isoformat()


def apaga_arquivo(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)
        return True
    return False


class ClienteApi:
    endpoint = '/api/cliente/'

    def __init__(self, domain):
        self.__domain = domain

    def _build_url(self, id=None):
        url = self.__domain + self.endpoint

        if id is not None:
            url += str(id)
        return url

    def fetch(self, id=None):
        raw = self._get(id)
        if raw is None:
            return raw
        return json.loads(raw.decode())

    def _get(self, id=None):
        url = self._build_url(id)
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise e


class Cliente:
    def __init__(self, id=None, nome=None):
        self.id = id
        self.nome = nome

    @classmethod
    def use(kls, api=None):
        if api:
            kls.api = api

    @classmethod
    def por_id(kls, id):
        data = kls.api.fetch(id)
        if data is None:
            return None
        return kls(**data)


# api = ClienteApi('http://cctdcapllx0415.df.caixa:8033')
# api = ClienteApi('http://localhost:8000')
# Cliente.use(api=api)
# Cliente.todos()
# Cliente.por_id(1)
