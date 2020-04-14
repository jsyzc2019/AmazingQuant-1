# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2020/4/14
# @Author  : gao
# @File    : update_sws_index.py
# @Project : AmazingQuant
# ------------------------------
import pandas as pd

from AmazingQuant.constant import DatabaseName, LocalDataFolderName
from AmazingQuant.config.local_data_path import LocalDataPath
from AmazingQuant.data_center.database_field.field_a_sws_index import ASwsIndex
from AmazingQuant.data_center.update_local_data.save_data import save_data_to_hdf5
from AmazingQuant.data_center.mongo_connection_me import MongoConnect


class UpdateASwsIndex(object):
    def __init__(self):
        self.a_sws_index_df = pd.DataFrame.empty

    def update_a_sws_index(self):
        database = DatabaseName.STOCK_BASE_DATA.value
        with MongoConnect(database):
            a_sws_index = ASwsIndex.objects().as_pymongo()
            field_list = ['sw_index_code', 'time_tag',
                          'pre_close', 'open', 'high', 'low', 'close', 'volume', 'amount',
                          'index_pe', 'index_pb',
                          'index_free_float_market_capitalisation', 'index_total_market_capitalisation']
            self.a_sws_index_df = pd.DataFrame(a_sws_index).reindex(columns=field_list)
            folder_name = LocalDataFolderName.SWS_INDEX.value
            path = LocalDataPath.path + folder_name + '/'
            data_name = folder_name
            save_data_to_hdf5(path, data_name, self.a_sws_index_df)


if __name__ == '__main__':
    kline_object = UpdateASwsIndex()
    kline_object.update_a_sws_index()