# -*- coding: utf-8 -*-
"""
Created on 05/04/2019 15:15
@author:   Dmitry
    Estimate running time
"""

import os
import datetime


def a_esttime(led):

    # Start of simulation
    if led == 0:
        # Clear
        os.system('cls' if os.name == 'nt' else 'clear')

        # Begin time stamp
        led = datetime.datetime.now()
        print('\nStart time       : ', led)
        print()

        return led

    # End of simulation
    else:
        print('\nEnd time        : ', datetime.datetime.now())
        print('Running time    : ', datetime.datetime.now() - led)
        print('Main done')