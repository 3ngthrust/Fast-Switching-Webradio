#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: 3ngthrust
"""
import gpiozero
import time

def bitstring(n):
    s = bin(n)[2:]
    return '0'*(8-len(s)) + s

class MCP3002(gpiozero.MCP3002):
    def _read(self):
        reply_bytes = self._spi.transfer([[192, 224][self.channel], 0]) # self._spi.transfer ^= xfer2 
        reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
        reply = reply_bitstring[5:15]
        return int(reply, 2)

if __name__ == "__main__":     
    adc_0 = MCP3002(channel=0) 
    adc_1 = MCP3002(channel=1) 
    
    while True:
        print(int(adc_0.value * 100))
        print(int(adc_1.value * 100))
        time.sleep(0.5)

