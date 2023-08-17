# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2023/6/15
# @Author  : gao
# @File    : tgw_api.py 
# @Project : AmazingQuant 
# ------------------------------
import tgw

from AmazingQuant.utils.data_transfer import date_to_datetime


class TgwApiData(object):
    def __init__(self, end_date):
        self.end_date = end_date
        self.calendar = []
        self.code_sh_list, self.code_sz_list = [], []
        self.stock_list = []
        self.code_list_hist = []

    def get_calendar(self, data_type='datetime'):
        index_kline = tgw.ReqKline()
        index_kline.cq_flag = 0
        index_kline.auto_complete = 1
        index_kline.cyc_type = tgw.MDDatatype.kDayKline
        index_kline.begin_date = 19900101
        index_kline.end_date = self.end_date
        index_kline.begin_time = 930
        index_kline.end_time = 1700

        index_kline.security_code = '000001'
        index_kline.market_type = tgw.MarketType.kSSE

        index_kline_df, _ = tgw.QueryKline(index_kline)

        self.calendar = list(index_kline_df['kline_time'].sort_values(ascending=True))
        if data_type == 'datetime':
            self.calendar = [date_to_datetime(str(i)) for i in self.calendar]
        return self.calendar

    def get_code_list(self, add_market=False, all_code=False):
        for market in [tgw.MarketType.kSZSE, tgw.MarketType.kSSE]:
            item = tgw.SubCodeTableItem()
            item.market = market
            item.security_code = ""
            code_table_df, error = tgw.QuerySecuritiesInfo(item)
            # print('code_table_df', code_table_df)
            code_table_df = code_table_df[code_table_df['security_type'].isin(['02001', '02003', '02004', '02999'])]
            code_list = list(code_table_df['security_code'])
            if market == tgw.MarketType.kSZSE:
                self.code_sz_list = code_list
                if add_market:
                    self.code_sz_list = [i + '.SZ' for i in self.code_sz_list]
            elif market == tgw.MarketType.kSSE:
                self.code_sh_list = code_list
                if add_market:
                    self.code_sh_list = [i + '.SH' for i in self.code_sh_list]

        if all_code:
            self.stock_list = self.code_sh_list + self.code_sz_list
            return self.stock_list
        else:
            return self.code_sh_list, self.code_sz_list

    def get_code_list_hist(self):
        task_id = tgw.GetTaskID()
        tgw.SetThirdInfoParam(task_id, "function_id", "A010010006")
        tgw.SetThirdInfoParam(task_id, "start_date", "19000101")
        tgw.SetThirdInfoParam(task_id, "end_date", "20991231")
        df, error = tgw.QueryThirdInfo(task_id)
        self.code_list_hist = list(df['MARKET_CODE'])
        return self.code_list_hist
