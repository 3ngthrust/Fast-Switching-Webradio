#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 3ngthrust
"""
import os
import gpiozero
import functools
import time
from MCP3002 import MCP3002

def split_into_equal_sublists(a_list, number_of_parts):
    """ Splits a list into a list of sublists

    Arguments
    ----------
    a_list : list object
        List wich will be split into Sublists
    number_of_parts : int
        Number of sublists which should be created
    
    Returns
    -------
    seperated_lists : list of lists
        List of Sublists of the given list which are as equal sized as possible
    """
    start = 0
    seperated_lists = []
    for i in range(number_of_parts):
        end = round((len(a_list) / number_of_parts) * (i + 1))
        seperated_lists.append(list(range(start,end)))
        start = end
    return seperated_lists
        
def update_station_faktory(num_of_stations, adc):
    """ Creates a function to update the station of the player

    Arguments
    ----------
    num_of_stations : int
        Number of different stations selectable on the player
    adc : gpiozero MCO3xxx object
        Analog to Digital Converter wich reads the raw slider position
    
    Returns
    -------
    update_station : function
        Function wich will take the current station number and update the 
        station on the player if necessary
    """
    # Create sublists of equal sized percentage ranges for each station
    percentage_sublists = split_into_equal_sublists(list(range(0,101)), num_of_stations)
    
    def update_station(current_station, current_volume):
        slider_value = int(adc.value * 100)
        
        for i, l in enumerate(percentage_sublists):
            if slider_value in l:
                new_station_number = percentage_sublists.index(l)
                break
            if i == (len(percentage_sublists) - 1):
                raise Exception("slider_value {} is not between 0 and 100".format(slider_value))
        
        # First element in mpc is 1 not 0
        new_station_number += 1
                
        if current_station == new_station_number:
            return current_station

        else:
            os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(current_station) + ' volume 0')
            os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(new_station_number) + ' volume ' + str(current_volume))
            return new_station_number
            
    return update_station
                    
def update_volume(adc, current_station, current_volume):
    """ Updates the volume of the player

    Arguments
    ----------
    adc : gpiozero MCO3xxx object
        Analog to Digital Converter wich reads the raw volume knob position
    """
    new_volume = 100 - int(adc.value * 100)
    
    if current_volume == new_volume:
        return current_volume

    else:
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(current_station) + ' volume ' + str(new_volume))
        return new_volume    

def toggle_mute_factory(led_0):
    mute_list = []    # Small Hack: Empty List = False
    
    def toggle_mute():
        if not mute_list:
            mute_list.append(1)
            led_0.toggle()
            
        else:
            mute_list.pop()
            led_0.toggle()
            
    def mute():
        return bool(mute_list)

    return toggle_mute, mute
    
def reload_factory(led_1, num_of_stations):
    def reload():
        led_1.toggle()
        
        for i in range(1, num_of_stations + 1):
            os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(i) + ' play ' + str(i))
            
        led_1.toggle()
    return reload
        
if __name__ == "__main__":
    
    #time.sleep(30)  # Wait for wifi connction to be established on startup
    
    num_of_stations = 10
    
    # Start mpd server
    for i in range(1, num_of_stations + 1):
        os.system('mpd /home/pi/.config/mpd/mpd_' + str(i) + '.conf')
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(i) + ' clear')
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(i) + ' load webradio_stations')       
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(i) + ' volume 0')
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(i) + ' play ' + str(i))
        
    print('All mpd servers started')
    
    # Setup frontend
    adc_0 = MCP3002(channel=0)
    adc_1 = MCP3002(channel=1)
    led_0 = gpiozero.LED(23)
    led_1 = gpiozero.LED(22)
    button_0 = gpiozero.Button(17)
    button_1 = gpiozero.Button(18)
    
    # Init
    current_station = 0
    current_volume = 0
    
    # Create Functions
    update_station = update_station_faktory(num_of_stations, adc_0)
    update_volume = functools.partial(update_volume, adc_1)
    toggle_mute, mute = toggle_mute_factory(led_0)
    reload = reload_factory(led_1, num_of_stations)
    
    # Assign functions
    button_0.when_pressed = toggle_mute
    button_1.when_pressed = reload
    
    try:
        while True:
            if mute():
                os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(current_station) + ' volume 0')
                current_volume = 0
                while mute():
                    time.sleep(0.05)

            current_station = update_station(current_station, current_volume)
            current_volume = update_volume(current_station, current_volume)
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        os.system('mpc --host=/home/pi/.config/mpd/socket_' + str(current_station) + ' volume 0')
        
