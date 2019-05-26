import random as rd
import pandas as pd
from requests import Session
from resources.constants import *


class UzParser():

    def __init__(self, mongo_client=None, use_socks=True):
        self.mongo_client = mongo_client
        self.s = Session()
        self.s.headers['User-Agent'] = USER_AGENT
        self.use_socks = use_socks and len(SOCKS)
        if self.use_socks:
            self.s.proxies = self.get_rd_socks()
        self.stations_df = pd.read_csv('./resources/stations.csv').set_index('_id')

    @staticmethod
    def get_rd_socks():
        if len(SOCKS):
            return {'https': f'socks5://{rd.choice(SOCKS)}'}

    def st_name_to_id(self, name, lang='en'):
        return self.stations_df[f'name_{lang}'].reset_index().set_index(f'name_{lang}')['_id'][name]

    def refactor_tuple(self, date, from_st, to_st):
        if not isinstance(date, str):
            date = date.strftime(DATE_FORMAT)
        if not isinstance(from_st, int):
            from_st = self.st_name_to_id(from_st)
        if not isinstance(to_st, int):
            to_st = self.st_name_to_id(to_st)
        return date, from_st, to_st

    def search_by_date(self, date, from_st, to_st, num_try=5):
        date, from_st, to_st = self.refactor_tuple(date, from_st, to_st)
        data = {
            'from': from_st,
            'to': to_st,
            'date': date,
        #     'time': '00:00',
        #     'get_tpl': 1
        }
        i = 0
        while True:
            try:
                r = self.s.post(TRAIN_SEARCH_EN_URL, data=data, timeout=3).json()['data']['list']
                df = pd.DataFrame(r)
                if not df.empty:
                    df = df.set_index('num')
                return df
            except Exception as e:
                self.s.proxies = self.get_rd_socks()
                i += 1
                if i > num_try:
                    if 'SOCKSHTTPSConnectionPool' in str(e):
                        continue
                    print(f'[search_by_date] error {i + 1} - {e}')
                    raise e

    def get_route(self, date, from_st, to_st, train_num, num_try=5):
        date, from_st, to_st = self.refactor_tuple(date, from_st, to_st)
        data = {
            'routes[0][from]': from_st,
            'routes[0][to]': to_st,
            'routes[0][date]': date,
            'routes[0][train]': train_num,
        }
        i = 0
        while True:
            try:
                r = self.s.post(ROUTE_EN_URL, data=data, timeout=3).json()['data']['routes'][0]['list']
                df = pd.DataFrame(r)
                if not df.empty:
                    df = df.set_index('code')
                return df
            except Exception as e:
                self.s.proxies = self.get_rd_socks()
                i += 1
                if i > num_try:
                    if 'SOCKSHTTPSConnectionPool' in str(e):
                        continue
                    print(f'[get_route] error {i} - {e}')
                    raise e

    def get_train_wagons_types(self, date, from_st, to_st, train_num, wagon_type_id=None, num_try=5):
        date, from_st, to_st = self.refactor_tuple(date, from_st, to_st)
        data = {
            'from': from_st,
            'to': to_st,
            'date': date,
            'train': train_num
        }
        if wagon_type_id:
            data['wagon_type_id'] = wagon_type_id
        i = 0
        while True:
            try:
                r = self.s.post(TRAIN_WAGONS_EN_URL, data=data, timeout=3).json()['data']
                if wagon_type_id:
                    return r
                r = r['types']
                df = pd.DataFrame(r)
                if not df.empty:
                    df = df.set_index('type_id')
                return df
            except Exception as e:
                self.s.proxies = self.get_rd_socks()
                i += 1
                if i > num_try:
                    if 'SOCKSHTTPSConnectionPool' in str(e):
                        continue
                    print(f'[get_train_wagons_types] error {i} - {e}')
                    raise e

    def get_wagons_by_type(self, date, from_st, to_st, train_num, wagon_type_id, num_try=5):
        date, from_st, to_st = self.refactor_tuple(date, from_st, to_st)
        data = {
            'from': from_st,
            'to': to_st,
            'date': date,
            'train': train_num,
            'wagon_type_id': wagon_type_id
        }
        i = 0
        while True:
            try:
                r = self.s.post(WAGONS_EN_URL, data=data, timeout=3).json()['data']['wagons']
                df = pd.DataFrame(r)
                if not df.empty:
                    df = df.set_index('num')
                return df
            except Exception as e:
                self.s.proxies = self.get_rd_socks()
                i += 1
                if i > num_try:
                    if 'SOCKSHTTPSConnectionPool' in str(e):
                        continue
                    if 'string indices must be integers' in str(e).lower():
                        return pd.DataFrame()
                    print(f'[get_wagons_by_type] error {i} - {e}')
                    raise e

    def get_wagon_seats(self, date, from_st, to_st, train_num, wagon_type_id, wagon_num, wagon_class=None, save=True, num_try=5):
        date, from_st, to_st = self.refactor_tuple(date, from_st, to_st)
        if len(wagon_type_id) > 1:
            wagon_type, wagon_class = wagon_type_id
        else:
            wagon_type = wagon_type_id
        data = {
            'from': from_st,
            'to': to_st,
            'date': date,
            'train': train_num,
            'wagon_type': wagon_type,
            'wagon_num': wagon_num
        }
        if wagon_class:
            data['wagon_class'] = wagon_class
        i = 0
        while True:
            try:
                r = self.s.post(TRAIN_WAGON_EN_URL, data=data, timeout=3).json()['data']
                if save:
                    r['date'] = pd.datetime.strptime(date, DATE_FORMAT)
                    r['from'] = from_st
                    r['to'] = to_st
                    r['train'] = train_num
                    r['wagon_type'] = wagon_type_id
                    r['wagon_num'] = wagon_num
                    r['parsed_time'] = pd.datetime.now()
                    if self.mongo_client:
                        self.mongo_client['uz']['presence'].insert_one(r)
                    return r
                df = pd.DataFrame(r)
                return df
            except Exception as e:
                self.s.proxies = self.get_rd_socks()
                i += 1
                if i > num_try:
                    if 'SOCKSHTTPSConnectionPool' in str(e):
                        continue
                    if "'str' object does not support item assignment" in str(e):
                        return {} if save else pd.DataFrame()
                    print(f'[get_wagon_seats] error {i} - {e}')
                    raise e

    def search_wagon_seats_by_date(self, date, from_st, to_st, save=True, num_try=5):
        main_dict = {}
        df = self.search_by_date(date, from_st=from_st, to_st=to_st, num_try=num_try)
        if not df.empty:
            try:
                train_nums = df[df['types'].map(len) > 0].index.tolist()
                for train_num in train_nums:
                    wagon_types = self.get_train_wagons_types(date, from_st=from_st, to_st=to_st,
                                                              train_num=train_num, num_try=num_try).index.tolist()
                    types_dict = {}
                    for wagon_type_id in wagon_types:
                        wagon_nums = self.get_wagons_by_type(date, from_st=from_st, to_st=to_st, train_num=train_num,
                                                             wagon_type_id=wagon_type_id, num_try=num_try).index.tolist()
                        wagon_dict = {}
                        for wagon_num in wagon_nums:
                            r = self.get_wagon_seats(date, from_st=from_st, to_st=to_st, train_num=train_num,
                                                     wagon_type_id=wagon_type_id, wagon_num=wagon_num, save=save, num_try=num_try)
                            places = r.get('places', {'no_keys': []})
                            places = places[list(places.keys())[0]]
                            if places:
                                wagon_dict[wagon_num] = places
                        if wagon_dict:
                            types_dict[wagon_type_id] = wagon_dict
                    if types_dict:
                        main_dict[train_num] = types_dict
            except Exception as e:
                print(date.strptime('%Y-%m-%d %H:%M:%S'), from_st, to_st, train_num, wagon_type_id, wagon_num)
        return main_dict
