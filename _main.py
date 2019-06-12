# -*- coding: utf-8 -*-
"""
Created on 18/05/2019 12:03
Project    Ozone
@author:   Dmitry
    Compare ozone data
"""

import a_esttime
import code1

# === main
if __name__ == '__main__':
    # --- path
    path = '../'
    #path = 'D:/Dropbox/1_Work/Students/Shitsu/'
    inp_dir = path + 'inp_data/'
    out_dir = path + 'out_data/'
    mid_dir = path + 'mid_dir/'
    plt_dir = path + 'plots/'

    # --- time start
    led = a_esttime.a_esttime(0)

    # --- read
    obj = code1.Processing(inp_dir, plt_dir)

    # --- start and end years
    years = [1973, 1975]
    for yr in range(years[0], years[1]):
        obj.proccess(str(yr))



    # --- time end
    led = a_esttime.a_esttime(led)
