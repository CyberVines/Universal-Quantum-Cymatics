#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Radio Tx
# Author: Justin Ried
# Description: Radio TX
# Generated: Sun May 22 05:33:31 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class Radio_TX(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Radio Tx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.freq = freq = 462650000
        self.variable_static_text_0 = variable_static_text_0 = (3e8/freq)/4
        self.rf_gain = rf_gain = 10
        self.if_gain = if_gain = 25
        self.aud_gain = aud_gain = 2

        ##################################################
        # Blocks
        ##################################################
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label="RF Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=300,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_rf_gain_sizer, 3, 1, 1, 1)
        _if_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._if_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	label="IF Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._if_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_if_gain_sizer,
        	value=self.if_gain,
        	callback=self.set_if_gain,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_if_gain_sizer, 4, 1, 1, 1)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label="Transmit Frequency",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=462640000,
        	maximum=462670000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 1, 1, 1, 1)
        self._variable_static_text_0_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.variable_static_text_0,
        	callback=self.set_variable_static_text_0,
        	label="Antenna Lenth (meters)",
        	converter=forms.float_converter(),
        )
        self.Add(self._variable_static_text_0_static_text)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=2,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=12,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(int(48e3))
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	5, 48000, 22000, 10000, firdes.WIN_HAMMING, 6.76))
        self.audio_source_0 = audio.source(48000, "", True)
        _aud_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._aud_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_aud_gain_sizer,
        	value=self.aud_gain,
        	callback=self.set_aud_gain,
        	label="Audio Input Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._aud_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_aud_gain_sizer,
        	value=self.aud_gain,
        	callback=self.set_aud_gain,
        	minimum=1,
        	maximum=5,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_aud_gain_sizer, 6, 1, 1, 1)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=int(48e3),
        	quad_rate=int(480e3),
        	tau=75e-6,
        	max_dev=75e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.audio_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_tx_0, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.osmosdr_sink_0, 0))    

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_variable_static_text_0((3e8/self.freq)/4)
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self._if_gain_slider.set_value(self.if_gain)
        self._if_gain_text_box.set_value(self.if_gain)
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_aud_gain(self):
        return self.aud_gain

    def set_aud_gain(self, aud_gain):
        self.aud_gain = aud_gain
        self._aud_gain_slider.set_value(self.aud_gain)
        self._aud_gain_text_box.set_value(self.aud_gain)


def main(top_block_cls=Radio_TX, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
