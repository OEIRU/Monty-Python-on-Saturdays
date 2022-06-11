import logging
import requests
import json
import pandas as pd
import csv
import os
from datetime import datetime


MAX_CHARS_IN_LOG = 200

class GetTablListError(Exception):
    pass

class JsonSeriazible:
    def for_json(self):
        #print(dir(self))
        return [i for i in dir(self)]

class Api(JsonSeriazible):
    def __init__(self, base_url: str, list_url: str, table_url:str, api_key: str):
        self._base_url = base_url
        self._list_url = list_url
        self._table_url = table_url
        self._api_key = api_key

    def get_list(self) -> list:
        table_list = []
        url = self._base_url+self._list_url
        try:
            res = requests.get(url, headers={'Http-Api-Key': self._api_key})
            data = json.loads(res.text)
            table_list = [i['TABLE_NAME'] for i in data if i['IS_PUBLIC'] == 1]
        except requests.exceptions.InvalidSchema:
            logging.error(f"Некорректный URL: {url}")
        except json.decoder.JSONDecodeError:
            logging.error(f"Что-то пошло не так c json: {res.text[:MAX_CHARS_IN_LOG]}")
            raise GetTablListError(url)
        except Exception as e:
            logging.error(f"Что-то пошло не так: {type(e)}")
        return table_list

    def make_request(self, name):
        data = None
        try:
            url = self._base_url+self._table_url.format(name)
            res = requests.get(url, headers={'Http-Api-Key': self._api_key})
            data = json.loads(res.text)
        except requests.exceptions.InvalidSchema:
            logging.error(f"Некорректный URL: {url}")
        except json.decoder.JSONDecodeError:
            logging.error(f"Что-то пошло не так c json: таблица {self._name} json - {res.text[:MAX_CHARS_IN_LOG]}")
        return data

    @classmethod
    def some_class_method(cls, self):
        print(cls, self)


class Table:
    def __init__(self,  name, api: Api):
        self._name = name
        self._api = api
        self.data = self.get_data()

    def __str__(self):
        return f"{self._name} - [{self.data[0]}, ...]" if self.data else f"{self._name}"

    def get_data(self):
        data = None
        try:
            data = self._api.make_request(self._name)
            self.error_status = 0
        except Exception as e:
            logging.error(f"Что-то пошло не так ({type(e)}): таблица {self._name}")
            self.error_status = 1
        return data

    def write_data(self, path=None):
        if not path:
            path = self._name+'.txt'
        if self.error_status:
            logging.error(f"Данные не получены: таблица {self._name}")
            return
        with open(path, 'w') as f:
            for i in self.data:
                f.write(str(i))


class TableWriter:
    def __init__(self, path: str):
        self.path = path
        self.tables = []

    def add_table(self, table: Table):
        self.tables.append(table)


class XlsxWriter(TableWriter):
    def write_tables(self):
        # создать excelwriter
        with pd.ExcelWriter(self.path) as writer:
            for t in self.tables:
                df = pd.DataFrame(t.data)
                #записать датафрейм в excelwriter
                df.to_excel(writer, sheet_name=t._name)


class CsvWriter(TableWriter):
    def write_tables(self):
        # использовать csv-writer
        pass


if __name__ == '__main__':
    url = 'https://api.ciu.nstu.ru/v1.0/desc/simple'
    tbl_url = 'https://api.ciu.nstu.ru/v1.0/data/simple/{0}'
    api = Api('https://api.ciu.nstu.ru/v1.0/',
              'desc/simple',
              'data/simple/{0}',
              'sdfget456DFHGWEv34gf')
    tbls = api.get_list()
    wrt = XlsxWriter('all_tables.xlsx')
    for i in tbls:
        t = Table(i, api)
        wrt.add_table(t)
    wrt.write_tables()






