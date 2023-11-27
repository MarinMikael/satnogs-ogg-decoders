#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Satnogs OGG BPSK to AX25
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
import math
import satnogs


class ogg_bpsk_decoder(gr.top_block):

    def __init__(self, baudrate=1200, decoded_file="/home/mikael/satnogs_kafasat/decoded/", excess_bw=0.5, max_cfo=2000.0, ogg_file='/home/mikael/satnogs/records/satnogs_6159130_2022-07-02T07-43-45.ogg'):
        gr.top_block.__init__(self, "Satnogs OGG BPSK to AX25")

        ##################################################
        # Parameters
        ##################################################
        self.baudrate = baudrate
        self.decoded_file = decoded_file
        self.excess_bw = excess_bw
        self.max_cfo = max_cfo
        self.ogg_file = ogg_file

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.audio_samp_rate = audio_samp_rate = 48000
        self.nfilts = nfilts = 32
        self.decimation = decimation = satnogs.find_decimation(baudrate, 2, audio_samp_rate,sps)
        self.variable_ax25_decoder_0 = variable_ax25_decoder_0 = satnogs.ax25_decoder_make('ASCL', 0, True, True, True, 1024, False)
        self.samp_rate = samp_rate = (baudrate*decimation)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), excess_bw, 11*sps*nfilts)
        self.if_freq = if_freq = 12000
        self.bpsk_constellation = bpsk_constellation = digital.constellation_bpsk().base()

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_ogg_source_0 = satnogs.ogg_source(ogg_file, 1, False)
        self.satnogs_json_converter_0 = satnogs.json_converter()
        self.satnogs_frame_file_sink_0_1_0 = satnogs.frame_file_sink(decoded_file, 0)
        self.satnogs_frame_decoder_0_0 = satnogs.frame_decoder(variable_ax25_decoder_0, 1 * 1)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            (baudrate*decimation)/audio_samp_rate,
            taps=None,
            flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            decimation // sps,
            firdes.low_pass(
                1,
                baudrate*decimation,
                baudrate/2 + excess_bw *baudrate/2 + abs(max_cfo),
                baudrate / 10.0,
                firdes.WIN_HAMMING,
                6.76))
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(sps, 2.0 * math.pi/100.0, rrc_taps, nfilts, nfilts/2, 1.5, 1)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(0.1, 2, False)
        self.digital_constellation_receiver_cb_0 = digital.constellation_receiver_cb(bpsk_constellation, 2.0 * math.pi/100.0, -0.25, 0.25)
        self.blocks_rotator_cc_0_0 = blocks.rotator_cc(-2.0 * math.pi * (if_freq / audio_samp_rate))
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_agc2_xx_0_0_0 = analog.agc2_cc(1e-3, 1e-3, 0.5, 1.0)
        self.analog_agc2_xx_0_0_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satnogs_frame_decoder_0_0, 'out'), (self.satnogs_json_converter_0, 'in'))
        self.msg_connect((self.satnogs_json_converter_0, 'out'), (self.satnogs_frame_file_sink_0_1_0, 'frame'))
        self.connect((self.analog_agc2_xx_0_0_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_rotator_cc_0_0, 0))
        self.connect((self.blocks_rotator_cc_0_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 0), (self.satnogs_frame_decoder_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_receiver_cb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_agc2_xx_0_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.satnogs_ogg_source_0, 0), (self.blocks_float_to_complex_0, 0))


    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.set_decimation(satnogs.find_decimation(self.baudrate, 2, self.audio_samp_rate,self.sps))
        self.set_samp_rate((self.baudrate*self.decimation))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.baudrate*self.decimation, self.baudrate/2 + self.excess_bw *self.baudrate/2 + abs(self.max_cfo), self.baudrate / 10.0, firdes.WIN_HAMMING, 6.76))
        self.pfb_arb_resampler_xxx_0.set_rate((self.baudrate*self.decimation)/self.audio_samp_rate)

    def get_decoded_file(self):
        return self.decoded_file

    def set_decoded_file(self, decoded_file):
        self.decoded_file = decoded_file

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.baudrate*self.decimation, self.baudrate/2 + self.excess_bw *self.baudrate/2 + abs(self.max_cfo), self.baudrate / 10.0, firdes.WIN_HAMMING, 6.76))

    def get_max_cfo(self):
        return self.max_cfo

    def set_max_cfo(self, max_cfo):
        self.max_cfo = max_cfo
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.baudrate*self.decimation, self.baudrate/2 + self.excess_bw *self.baudrate/2 + abs(self.max_cfo), self.baudrate / 10.0, firdes.WIN_HAMMING, 6.76))

    def get_ogg_file(self):
        return self.ogg_file

    def set_ogg_file(self, ogg_file):
        self.ogg_file = ogg_file

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_decimation(satnogs.find_decimation(self.baudrate, 2, self.audio_samp_rate,self.sps))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.set_decimation(satnogs.find_decimation(self.baudrate, 2, self.audio_samp_rate,self.sps))
        self.blocks_rotator_cc_0_0.set_phase_inc(-2.0 * math.pi * (self.if_freq / self.audio_samp_rate))
        self.pfb_arb_resampler_xxx_0.set_rate((self.baudrate*self.decimation)/self.audio_samp_rate)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.excess_bw, 11*self.sps*self.nfilts))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_samp_rate((self.baudrate*self.decimation))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.baudrate*self.decimation, self.baudrate/2 + self.excess_bw *self.baudrate/2 + abs(self.max_cfo), self.baudrate / 10.0, firdes.WIN_HAMMING, 6.76))
        self.pfb_arb_resampler_xxx_0.set_rate((self.baudrate*self.decimation)/self.audio_samp_rate)

    def get_variable_ax25_decoder_0(self):
        return self.variable_ax25_decoder_0

    def set_variable_ax25_decoder_0(self, variable_ax25_decoder_0):
        self.variable_ax25_decoder_0 = variable_ax25_decoder_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*1)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps(self.rrc_taps)

    def get_if_freq(self):
        return self.if_freq

    def set_if_freq(self, if_freq):
        self.if_freq = if_freq
        self.blocks_rotator_cc_0_0.set_phase_inc(-2.0 * math.pi * (self.if_freq / self.audio_samp_rate))

    def get_bpsk_constellation(self):
        return self.bpsk_constellation

    def set_bpsk_constellation(self, bpsk_constellation):
        self.bpsk_constellation = bpsk_constellation




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--baudrate", dest="baudrate", type=eng_float, default="1.2k",
        help="Set baudrate [default=%(default)r]")
    parser.add_argument(
        "--decoded-file", dest="decoded_file", type=str, default="/home/mikael/satnogs_kafasat/decoded/",
        help="Set decoded_file [default=%(default)r]")
    parser.add_argument(
        "--excess-bw", dest="excess_bw", type=eng_float, default="500.0m",
        help="Set excess_bw [default=%(default)r]")
    parser.add_argument(
        "--max-cfo", dest="max_cfo", type=eng_float, default="2.0k",
        help="Set max_cfo [default=%(default)r]")
    parser.add_argument(
        "--ogg-file", dest="ogg_file", type=str, default='/home/mikael/satnogs/records/satnogs_6159130_2022-07-02T07-43-45.ogg',
        help="Set ogg_file [default=%(default)r]")
    return parser


def main(top_block_cls=ogg_bpsk_decoder, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(baudrate=options.baudrate, decoded_file=options.decoded_file, excess_bw=options.excess_bw, max_cfo=options.max_cfo, ogg_file=options.ogg_file)

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
