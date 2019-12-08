# -*- coding: utf-8 -*-
"""
Created on 18/05/2019 12:03
Project    Ozone
@author:   Dmitry
    Compare ozone data
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.environ["PROJ_LIB"] = "C:/Users/admin/Anaconda3/Library/share"  # epsg file should be
from mpl_toolkits.basemap import Basemap

import a_saveplot


# === main class
class Processing():

    # --- init
    def __init__(self, inp_dir, plt_dir):
        # --- path
        self.inp_dir = inp_dir
        self.plt_dir = plt_dir

        # --- 2d map for Japan
        self.map_lims = [36, 38, 140, 144, 1, 1]

    # --- data processing
    def proccess(self, yr):

        # --- pd settings
        pd.set_option('expand_frame_repr', False)

        # --- files to read
        file_d = self.inp_dir + 'TD' + yr + '0600.txt'
        file_m = self.inp_dir + 'TM' + yr + '0000.txt'
        print('File to read:', file_m, file_d)

        # --- read
        df_d = pd.read_csv(file_d, encoding='cp932')
        df_m = pd.read_csv(file_m, encoding='cp932')
        #df_m = pd.read_csv(file_m, encoding='utf-8')

        # --- subset
        df_d1 = df_d[['測定局コード', '昼間の１時間値の最高値(ppm)', '昼間の日最高１時間値の年平均値(ppm)']]
        df_d1.set_index('測定局コード', inplace=True)

        df_m1 = df_m[['国環研局番', '同左_ローマ字', '都道府県名', '市区町村名', '緯度_度', '緯度_分', '緯度_秒', '経度_度', '経度_分', '経度_秒']]
        df_m1.rename({'国環研局番': '測定局コード'}, axis='columns', inplace=True)
        df_m1.set_index('測定局コード', inplace=True)

        # --- joint df
        df_a = pd.concat([df_m1, df_d1], axis=1)
        #df_a.dropna(inplace=True)

        # --- check data
        print('Working datasets' + ' for ' + yr)
        print(df_d1.head())
        print(df_m1.head())
        print(df_a.head())

        # --- lat/lons
        # var1d = df_a['OX_測定高度(m)'].values
        # lats = df_a['緯度_度'].values + df_a['緯度_分'].values / 60 + df_a['緯度_秒'].values / 3600
        # lons = df_a['経度_度'].values + df_a['経度_分'].values / 60 + df_a['経度_秒'].values / 3600
        # sites = df_a['同左_ローマ字'].values
        # sites = df_a['市区町村名'].values

        # --- data to plot
        n_var = ['昼間の１時間値の最高値(ppm)', '昼間の日最高１時間値の年平均値(ppm)']
        n_drp = ['昼間の日最高１時間値の年平均値(ppm)', '昼間の１時間値の最高値(ppm)']
        n_ttl = ['Maximum O$_3$, ppm', 'Average O$_3$, ppm']
        n_fll = ['Maximum_O3', 'Average_O3']

        # --- loop
        for l in range(0, len(n_var)):
            df_plt = df_a.copy()
            df_plt.drop(n_drp[l], axis=1, inplace=True)
            df_plt.dropna(inplace=True)

            # --- data to plot
            var1d = df_plt[n_var[l]].values
            lats = df_plt['緯度_度'].values + df_plt['緯度_分'].values / 60 + df_plt['緯度_秒'].values / 3600
            lons = df_plt['経度_度'].values + df_plt['経度_分'].values / 60 + df_plt['経度_秒'].values / 3600
            # sites = df_plt['同左_ローマ字'].values
            # sites = df_plt['市区町村名'].values
            sites = df_plt['都道府県名'].values

            # --- plot map if var1d not empty
            if var1d != []:
                plot_name = self.plt_dir + n_fll[l] + '_' + yr
                title = n_ttl[l]
                self.plot_map(var1d, lats, lons, sites, plot_name, title, yr)

    # === plot map
    def plot_map(self, var1d, lats, lons, sites, plot_name, title, yr):

        from matplotlib.font_manager import FontProperties

        fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc', size=5)

        # --- Build Map ---
        fig = plt.figure()
        plt.rc('font', family='serif')
        my_cmap = plt.get_cmap('rainbow')
        font_size = 10

        # --- limits
        map_lims = self.map_lims

        # --- map labels ---
        mp = Basemap(projection='gall', llcrnrlat=map_lims[0], urcrnrlat=map_lims[1],
                     llcrnrlon=map_lims[2], urcrnrlon=map_lims[3], resolution='l')
        mp.drawcoastlines(color='grey')
        mp.drawcountries(color='grey')
        mp.drawparallels(np.arange(-90, 91, map_lims[4]), labels=[True, False, True, False],
                         fontsize=font_size, color='grey')
        mp.drawmeridians(np.arange(2, 362, map_lims[5]), labels=[False, True, False, True],
                         fontsize=font_size, color='grey')

        x, y = mp(lons, lats)
        mp.scatter(x, y, c=var1d, s=10, cmap=my_cmap)

        # --- selected sites
        o_site = ''
        for j in range(0, len(sites), 1):
            n_lat = lats[j]
            n_lon = lons[j]
            n_site = sites[j]

            # --- plot only unploted sites
            # if n_site != o_site:
            if n_site[:1] != o_site[:1]:
                x, y = mp(n_lon, n_lat)
                plt.text(x, y, n_site, color='k', weight='bold', fontsize=font_size - 6, fontproperties=fp)
            o_site = sites[j]


        # --- title
        plt.title(title + ' for ' + yr)

        # --- legend
        # plt.legend(loc="lower left", ncol=4, prop={'size': font_size - 4}, fancybox=True, shadow=True)
        plt.colorbar()

        # --- save to plot
        a_saveplot.save_plot(plot_name, ext="png", close=True, verbose=False)
        plt.show()
