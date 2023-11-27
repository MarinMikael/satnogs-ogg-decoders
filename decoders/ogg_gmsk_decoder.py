#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ogg_gmsk_decoder
# Author: Manolis Surligas (surligas@gmail.com)
# Description: Generic FSK/MSK decoder supporting AX.25 and AX.100 framing schemes
# GNU Radio version: 3.8.2.0

from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
import math
import satnogs


class ogg_gmsk_decoder(gr.top_block):

    def __init__(self, baudrate=1200, decoded_file="/home/mikael/satnogs_kafasat/decoded/", framing="ax25", ogg_file='/home/mikael/satnogs_kafasat/satnogs_ogg/satnogs_8523554_2023-11-16T04-34-53.ogg'):
        gr.top_block.__init__(self, "ogg_gmsk_decoder")

        ##################################################
        # Parameters
        ##################################################
        self.baudrate = baudrate
        self.decoded_file = decoded_file
        self.framing = framing
        self.ogg_file = ogg_file

        ##################################################
        # Variables
        ##################################################
        self.variable_ax25_decoder_0 = variable_ax25_decoder_0 = satnogs.ax25_decoder_make('GND', 0, True, True, True, 1024, False)
        self.variable_ax100_mode6_decoder_0 = variable_ax100_mode6_decoder_0 = satnogs.ax100_decoder_mode6_make(satnogs.crc.CRC32_C, satnogs.whitening_make_ccsds(True), True)
        self.variable_ax100_mode5_decoder_0 = variable_ax100_mode5_decoder_0 = satnogs.ax100_decoder_mode5_make([], 0, [0x93, 0x0B, 0x51, 0xDE], 3, satnogs.crc.CRC32_C,  satnogs.whitening.make_ccsds(True), True)
        self.available_framings = available_framings = {'ax25':variable_ax25_decoder_0, 'ax100_mode5':variable_ax100_mode5_decoder_0,  'ax100_mode6':variable_ax100_mode6_decoder_0}
        self.audio_samp_rate = audio_samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_ogg_source_0 = satnogs.ogg_source(ogg_file, 1, False)
        self.satnogs_json_converter_0 = satnogs.json_converter()
        self.satnogs_frame_file_sink_0_1_0 = satnogs.frame_file_sink(decoded_file, 0)
        self.satnogs_frame_decoder_0_0 = satnogs.frame_decoder(available_framings[framing], 1 * 1)
        self.pfb_arb_resampler_xxx_1_0 = pfb.arb_resampler_fff(
            (baudrate*2)/(audio_samp_rate),
            taps=None,
            flt_size=32)
        self.pfb_arb_resampler_xxx_1_0.declare_sample_delay(0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(2, 2 * math.pi / 100, 0.5, 0.5/8.0, 0.01)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satnogs_frame_decoder_0_0, 'out'), (self.satnogs_json_converter_0, 'in'))
        self.msg_connect((self.satnogs_json_converter_0, 'out'), (self.satnogs_frame_file_sink_0_1_0, 'frame'))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satnogs_frame_decoder_0_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_1_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.satnogs_ogg_source_0, 0), (self.pfb_arb_resampler_xxx_1_0, 0))


    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.pfb_arb_resampler_xxx_1_0.set_rate((self.baudrate*2)/(self.audio_samp_rate))

    def get_decoded_file(self):
        return self.decoded_file

    def set_decoded_file(self, decoded_file):
        self.decoded_file = decoded_file

    def get_framing(self):
        return self.framing

    def set_framing(self, framing):
        self.framing = framing

    def get_ogg_file(self):
        return self.ogg_file

    def set_ogg_file(self, ogg_file):
        self.ogg_file = ogg_file

    def get_variable_ax25_decoder_0(self):
        return self.variable_ax25_decoder_0

    def set_variable_ax25_decoder_0(self, variable_ax25_decoder_0):
        self.variable_ax25_decoder_0 = variable_ax25_decoder_0
        self.set_available_framings({'ax25':self.variable_ax25_decoder_0, 'ax100_mode5':self.variable_ax100_mode5_decoder_0,  'ax100_mode6':self.variable_ax100_mode6_decoder_0})

    def get_variable_ax100_mode6_decoder_0(self):
        return self.variable_ax100_mode6_decoder_0

    def set_variable_ax100_mode6_decoder_0(self, variable_ax100_mode6_decoder_0):
        self.variable_ax100_mode6_decoder_0 = variable_ax100_mode6_decoder_0
        self.set_available_framings({'ax25':self.variable_ax25_decoder_0, 'ax100_mode5':self.variable_ax100_mode5_decoder_0,  'ax100_mode6':self.variable_ax100_mode6_decoder_0})

    def get_variable_ax100_mode5_decoder_0(self):
        return self.variable_ax100_mode5_decoder_0

    def set_variable_ax100_mode5_decoder_0(self, variable_ax100_mode5_decoder_0):
        self.variable_ax100_mode5_decoder_0 = variable_ax100_mode5_decoder_0
        self.set_available_framings({'ax25':self.variable_ax25_decoder_0, 'ax100_mode5':self.variable_ax100_mode5_decoder_0,  'ax100_mode6':self.variable_ax100_mode6_decoder_0})

    def get_available_framings(self):
        return self.available_framings

    def set_available_framings(self, available_framings):
        self.available_framings = available_framings

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.pfb_arb_resampler_xxx_1_0.set_rate((self.baudrate*2)/(self.audio_samp_rate))




def argument_parser():
    description = 'Generic FSK/MSK decoder supporting AX.25 and AX.100 framing schemes'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--baudrate", dest="baudrate", type=eng_float, default="1.2k",
        help="Set baudrate [default=%(default)r]")
    parser.add_argument(
        "--decoded-file", dest="decoded_file", type=str, default="/home/mikael/satnogs_kafasat/decoded/",
        help="Set decoded_file [default=%(default)r]")
    parser.add_argument(
        "--framing", dest="framing", type=str, default="ax25",
        help="Set the framing scheme to use [ax25, ax100_mode5, ax100_mode6] [default=%(default)r]")
    parser.add_argument(
        "--ogg-file", dest="ogg_file", type=str, default='/home/mikael/satnogs_kafasat/satnogs_ogg/satnogs_8523554_2023-11-16T04-34-53.ogg',
        help="Set ogg_file [default=%(default)r]")
    return parser


def main(top_block_cls=ogg_gmsk_decoder, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(baudrate=options.baudrate, decoded_file=options.decoded_file, framing=options.framing, ogg_file=options.ogg_file)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
