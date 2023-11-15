# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_analysis_engine.py
# @Project : AmazingQuant
# ------------------------------

from AmazingQuant.analysis_center.event_backtesting_analysis import *


def run_backtesting_analysis_engine(strategy, cal_all=True):
    event_backtesting = EventBacktestingAnalysis()
    event_backtesting.event_data_dict["strategy_data"] = strategy
    EventBacktestingAnalysis.save_backtesting_record_to_csv(event_backtesting)
    EventBacktestingAnalysis.show_backtesting_indicator(event_backtesting, cal_all=cal_all)


if __name__ == "__main__":
    run_backtesting_analysis_engine("qweqweqwe")
