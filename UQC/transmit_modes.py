#!/usr/bin/env python3
"""HackRF Multi-Mode IQ Generator
Generates int8 IQ samples on stdout for piping to hackrf_transfer.
Usage: python3 transmit_modes.py MODE MESSAGE WPM TONE_HZ F_DEV CALLSIGN
"""
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                                                                             │
# │  .------..------..------..------..------..------..------.         .------..------. │
# │  |W.--. ||E.--. ||L.--. ||C.--. ||O.--. ||M.--. ||E.--. | .-.     |T.--. ||O.--. | │
# │  | :/\: || (\/) || :/\: || :/\: || :/\: || (\/) || (\/) |((3))    | :/\: || :/\: | │
# │  | :\/: || :\/: || (__) || :\/: || :\/: || :\/: || :\/: | '-.-.   | (__) || :\/: | │
# │  | '--23|| '--'5|| '--12|| '--'3|| '--15|| '--13|| '--'5|  ((22)) | '--20|| '--15| │
# │  `------'`------'`------'`------'`------'`------'`------'    '-'  `------'`------' │
# │  .------..------..------..------..------.         .------..------..------..------..------. │
# │  |C.--. ||Y.--. ||B.--. ||E.--. ||R.--. | .-.     |V.--. ||I.--. ||N.--. ||E.--. ||S.--. | │
# │  | :/\: || (\/) || :(): || (\/) || :(): |((3))    | :(): || (\/) || :(): || (\/) || :/\: | │
# │  | :\/: || :\/: || ()() || :\/: || ()() | '-.-.   | ()() || :\/: || ()() || :\/: || :\/: | │
# │  | '--'3|| '--25|| '--'2|| '--'5|| '--18|  ((22)) | '--22|| '--'9|| '--14|| '--'5|| '--19| │
# │  `------'`------'`------'`------'`------'    '-'  `------'`------'`------'`------'`------' │
# │                                                                             │
# │  QR Code — https://cybervines.com                                           │
# │                                                                             │
# │  ██████████████  ██      ████        ██████████████                          │
# │  ██          ██  ██  ██  ██  ██  ██  ██          ██                          │
# │  ██  ██████  ██  ██  ████████████    ██  ██████  ██                          │
# │  ██  ██████  ██    ████    ████  ██  ██  ██████  ██                          │
# │  ██  ██████  ██  ██████████████  ██  ██  ██████  ██                          │
# │  ██          ██    ██      ████  ██  ██          ██                          │
# │  ██████████████  ██  ██  ██  ██  ██  ██████████████                          │
# │                          ██████████                                          │
# │  ██    ████████████      ██  ██  ████    ██  ██████                          │
# │    ████████    ██  ██  ██    ████  ██  ██████████                            │
# │  ██  ██      ████    ████████████████  ██  ██    ██                          │
# │          ████  ██    ██  ██  ██  ██  ██    ████████                          │
# │  ██    ██    ████      ██        ██  ████        ██                          │
# │  ████    ██      ██      ██  ██████      ██    ██                            │
# │  ████████    ████  ████      ██████  ██  ██████████                          │
# │  ██  ██████    ██████    ██    ██      ██  ████  ██                          │
# │  ██    ██  ████        ██████  ████████████  ████                            │
# │                  ████  ██  ██  ████      ██  ████                            │
# │  ██████████████  ██████  ████    ██  ██  ██      ██                          │
# │  ██          ██  ██    ██  ██  ████      ██                                  │
# │  ██  ██████  ██  ██    ██  ██  ████████████    ████                          │
# │  ██  ██████  ██  ██████  ██████    ████        ████                          │
# │  ██  ██████  ██        ██  ██  ██  ██    ██████████                          │
# │  ██          ██      ████████  ██    ██████  ██████                          │
# │  ██████████████  ██  ████████    ██  ██    ██    ██                          │
# │                                                                             │
# │  Copyright 12011 HE - 12026 HE Cyber Vines, LLC                            │
# │  All rights reserved.                                                       │
# │                                                                             │
# │  -----------------------------------------------------------------          │
# │  Warning: This system is restricted to private use                          │
# │  authorized users for business purposes only. Unauthorized access           │
# │  or use is a violation of company policy and the law. This system           │
# │  may be monitored for administrative and security reasons. By               │
# │  proceeding, you acknowledge that (1) you have read and understand          │
# │  this notice and (2) you consent to the system monitoring.                  │
# │                                                                             │
# │  This Website is intended only for use by 'Authorized Personnel'            │
# │  and may contain legally privileged and/or confidential information.        │
# │  This Website, including any files and attachments, is covered by           │
# │  the Electronic Communications Privacy Act, 18 U.S.C. 2510-2522            │
# │  and should not be disclosed to third parties. If you are not the           │
# │  intended recipient, you are hereby notified that any dissemination,        │
# │  distribution, use for any reason, or copying is strictly prohibited.       │
# │  For support, please immediately notify Cyber Vines, LLC                    │
# │  at webadmin@cybervines.com or phone +1 214 295 8481                        │
# │                                                                             │
# │  Although Cyber Vines, LLC has attempted to ensure the accuracy of          │
# │  the technical support information it is possible that it may contain       │
# │  technical inaccuracies, typographical, or other errors.                    │
# │  Cyber Vines, LLC assumes no liability for any errors in this               │
# │  information, and for damages, whether direct, indirect, incidental,        │
# │  and consequential or otherwise, that may result from such error,           │
# │  including, but not limited to loss of data or profits.                     │
# │                                                                             │
# │  Our website follows the safe harbor provisions of 17 U.S.C. §512,         │
# │  otherwise known as Digital Millennium Copyright Act ("DMCA").              │
# │  To file a copyright infringement notification with us, you will            │
# │  need to send a written communication that includes substantially           │
# │  the following:                                                             │
# │                                                                             │
# │  A physical or electronic signature of a person authorized to act           │
# │  on behalf of the owner of an exclusive right that is allegedly             │
# │  infringed.                                                                 │
# │                                                                             │
# │  Identification of the copyrighted work claimed to have been                │
# │  infringed, or, if multiple copyrighted works at a single online            │
# │  site are covered by a single notification, a representative list           │
# │  of such works at that site.                                                │
# │                                                                             │
# │  Identification of the material that is claimed to be infringing            │
# │  or to be the subject of infringing activity and that is to be              │
# │  removed or access to which is to be disabled, and information              │
# │  reasonably sufficient to permit the service provider to locate             │
# │  the material. Providing URLs in the body of an email is the best           │
# │  way to help us locate content quickly.                                     │
# │                                                                             │
# │  Information reasonably sufficient to permit the service provider           │
# │  to contact the complaining party, such as an address, telephone            │
# │  number, and, if available, an electronic mail address at which             │
# │  the complaining party may be contacted.                                    │
# │                                                                             │
# │  A statement that the complaining party has a good faith belief             │
# │  that use of the material in the manner complained of is not                │
# │  authorized by the copyright owner, its agent, or the law.                  │
# │                                                                             │
# │  A statement that the information in the notification is accurate,          │
# │  and under penalty of perjury, that the complaining party is                │
# │  authorized to act on behalf of the owner of an exclusive right             │
# │  that is allegedly infringed (Note that under Section 512(f) any            │
# │  person who knowingly and materially misrepresents that material            │
# │  or activity is infringing may be subject to liability for damages.         │
# │                                                                             │
# │  All basic services start at $89 per hour...                                │
# │  -----------------------------------------------------------------          │
# │                                                                             │
# └─────────────────────────────────────────────────────────────────────────────┘
#
import numpy as np, sys, math

SR = 8_000_000
CHUNK_SAMPLES = 500_000  # Flush to stdout every ~0.25s of samples

# ── Helpers ───────────────────────────────────────────────────────────────────
def emit(i_f, q_f):
    iq = np.empty(len(i_f) * 2, dtype=np.int8)
    iq[0::2] = np.clip(np.round(i_f), -127, 127).astype(np.int8)
    iq[1::2] = np.clip(np.round(q_f), -127, 127).astype(np.int8)
    sys.stdout.buffer.write(iq.tobytes())
    sys.stdout.buffer.flush()

class StreamBuffer:
    """Accumulates IQ segments and auto-flushes to prevent memory buildup."""
    def __init__(self):
        self.i_buf = []
        self.q_buf = []
        self.count = 0

    def add(self, i_f, q_f):
        self.i_buf.append(i_f)
        self.q_buf.append(q_f)
        self.count += len(i_f)
        if self.count >= CHUNK_SAMPLES:
            self.flush()

    def flush(self):
        if self.count > 0:
            emit(np.concatenate(self.i_buf), np.concatenate(self.q_buf))
            self.i_buf = []
            self.q_buf = []
            self.count = 0

def text_to_bits(text):
    bits = []
    for ch in text:
        b = ord(ch) & 0xFF
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits

def rrc_taps(alpha, sps, n_sym=11):
    n = n_sym * sps + 1
    t = np.linspace(-n_sym / 2, n_sym / 2, n)
    with np.errstate(divide='ignore', invalid='ignore'):
        num = np.sin(np.pi * t * (1 - alpha)) + 4 * alpha * t * np.cos(np.pi * t * (1 + alpha))
        den = np.pi * t * (1 - (4 * alpha * t) ** 2)
        h = np.where(np.abs(den) > 1e-8, num / den, 0.0)
    # Fix t=0
    h[np.abs(t) < 1e-8] = 1 + alpha * (4 / np.pi - 1)
    # Fix t=±1/(2*alpha)
    edge = np.abs(np.abs(t) - 1 / (2 * alpha)) < 1e-8
    h[edge] = (alpha / np.sqrt(2)) * (
        (1 + 2 / np.pi) * np.sin(np.pi / (4 * alpha)) +
        (1 - 2 / np.pi) * np.cos(np.pi / (4 * alpha)))
    return h / np.sqrt(np.sum(h ** 2))

def psk_modulate(syms, baud, alpha=0.35):
    sps = max(int(SR / baud), 1)
    if sps > 200:
        # Low baud rate: work at reduced internal rate, then interpolate in chunks
        internal_sps = 20
        n_sym = min(11, max(3, len(syms) // 4))
        h = rrc_taps(alpha, internal_sps, n_sym)
        up = np.zeros(len(syms) * internal_sps, dtype=complex)
        up[::internal_sps] = syms
        filtered = np.convolve(up, h, mode='same')
        # Compute peak from the small internal-rate signal
        peak = max(np.max(np.abs(np.real(filtered))),
                   np.max(np.abs(np.imag(filtered)))) + 1e-10
        total_len = len(syms) * sps
        x_old = np.linspace(0, 1, len(filtered))
        # Chunked interpolation and emission
        denom = max(total_len - 1, 1)
        for start in range(0, total_len, CHUNK_SAMPLES):
            end = min(start + CHUNK_SAMPLES, total_len)
            x_new = np.linspace(start / denom, (end - 1) / denom, end - start)
            I = np.interp(x_new, x_old, np.real(filtered)) / peak * 120
            Q = np.interp(x_new, x_old, np.imag(filtered)) / peak * 120
            emit(I, Q)
    else:
        n_sym = min(11, max(3, len(syms) // 4))
        h = rrc_taps(alpha, sps, n_sym)
        up = np.zeros(len(syms) * sps, dtype=complex)
        up[::sps] = syms
        filtered = np.convolve(up, h, mode='same')
        peak = np.max(np.abs(filtered)) + 1e-10
        s = filtered / peak * 120
        for start in range(0, len(s), CHUNK_SAMPLES):
            end = min(start + CHUNK_SAMPLES, len(s))
            emit(np.real(s[start:end]), np.imag(s[start:end]))

def fsk_segment(n_samples, freq_hz, phase):
    dph = 2 * np.pi * freq_hz / SR
    phi = phase + dph * np.arange(n_samples)
    end_phase = float(phi[-1] + dph) if n_samples > 0 else phase
    return 127 * np.cos(phi), 127 * np.sin(phi), end_phase

# ══════════════════════════════════════════════════════════════════════════════
# CW / MORSE CODE
# ══════════════════════════════════════════════════════════════════════════════
MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....',
    'I':'..','J':'.---','K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.',
    'Q':'--.-','R':'.-.','S':'...','T':'-','U':'..-','V':'...-','W':'.--','X':'-..-',
    'Y':'-.--','Z':'--..','0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.','.':'.-.-.-',',':'--..--',
    '?':'..--..','!':'-.-.--','/':'-..-.','-':'-....-','(':'-.--.',')':'-.--.-',
}

def gen_cw(text, wpm=15, tone_hz=572, fdev=5000, mode='FM'):
    dot = int(1.2 / wpm * SR)
    buf = StreamBuffer()
    state = 0.0

    if mode == 'FM':
        def seg_on(n, st):
            t = np.arange(n) / SR
            dp = 2 * np.pi * fdev * np.cos(2 * np.pi * tone_hz * t) / SR
            phi = st + np.cumsum(dp)
            return 127 * np.cos(phi), 127 * np.sin(phi), float(phi[-1])
        def seg_off(n, st):
            return np.full(n, 127 * np.cos(st)), np.full(n, 127 * np.sin(st)), st
    else:
        A_C, A_M = 63, 63
        def seg_on(n, st):
            t = np.arange(st, st + n) / SR
            return A_C + A_M * np.cos(2 * np.pi * tone_hz * t), np.zeros(n), st + n
        def seg_off(n, st):
            return np.full(n, float(A_C)), np.zeros(n), st + n

    words = text.upper().split()
    for wi, word in enumerate(words):
        for ci, ch in enumerate(word):
            code = MORSE.get(ch, '')
            for ei, sym in enumerate(code):
                n = dot if sym == '.' else 3 * dot
                i, q, state = seg_on(n, state)
                buf.add(i, q)
                if ei < len(code) - 1:
                    i, q, state = seg_off(dot, state)
                    buf.add(i, q)
            if ci < len(word) - 1:
                i, q, state = seg_off(3 * dot, state)
                buf.add(i, q)
        if wi < len(words) - 1:
            i, q, state = seg_off(7 * dot, state)
            buf.add(i, q)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# PSK MODES (BPSK / QPSK / 8PSK)
# ══════════════════════════════════════════════════════════════════════════════
def gen_bpsk(text, baud):
    bits = [0] * 32 + text_to_bits(text) + [0] * 32
    syms, prev = [], 1 + 0j
    for b in bits:
        s = prev if b == 0 else -prev
        syms.append(s); prev = s
    psk_modulate(np.array(syms), baud)

def gen_qpsk(text, baud):
    bits = [0] * 32 + text_to_bits(text) + [0] * 32
    bits += [0] * ((-len(bits)) % 2)
    PHASES = [1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j]
    syms, idx = [], 0
    for i in range(0, len(bits), 2):
        d = (bits[i] << 1) | bits[i + 1]
        idx = (idx + d) % 4
        syms.append(PHASES[idx])
    psk_modulate(np.array(syms), baud)

def gen_8psk(text, baud):
    bits = [0] * 24 + text_to_bits(text) + [0] * 24
    bits += [0] * ((-len(bits)) % 3)
    PT = np.array([0, 1, 3, 2, 6, 7, 5, 4]) * (np.pi / 4)
    phase, syms = 0.0, []
    for i in range(0, len(bits), 3):
        s = (bits[i] << 2) | (bits[i + 1] << 1) | bits[i + 2]
        phase = (phase + PT[s]) % (2 * np.pi)
        syms.append(np.exp(1j * phase))
    psk_modulate(np.array(syms), baud)

# ══════════════════════════════════════════════════════════════════════════════
# RTTY (ITA2 Baudot)
# ══════════════════════════════════════════════════════════════════════════════
ITA2_LTRS = {
    'A': 3, 'B': 25, 'C': 14, 'D': 9, 'E': 1, 'F': 13, 'G': 26, 'H': 20,
    'I': 6, 'J': 11, 'K': 15, 'L': 18, 'M': 28, 'N': 12, 'O': 24, 'P': 22,
    'Q': 23, 'R': 10, 'S': 5, 'T': 16, 'U': 7, 'V': 30, 'W': 19, 'X': 29,
    'Y': 21, 'Z': 17, '\r': 8, '\n': 2, ' ': 4,
}
ITA2_FIGS = {
    '3': 1, '-': 3, "'": 5, '8': 6, '7': 7, '4': 10, ',': 12, '!': 13,
    ':': 14, '(': 15, '5': 16, '"': 17, ')': 18, '2': 19, '#': 20, '6': 21,
    '0': 22, '1': 23, '9': 24, '?': 25, '&': 26, '.': 28, '/': 29, ';': 30,
    '\r': 8, '\n': 2, ' ': 4,
}
LTRS_SHIFT = 31
FIGS_SHIFT = 27

def gen_rtty(text, baud=45.45, shift_hz=170.0):
    sps = int(SR / baud)
    baudot_bits = []

    def send_code(code):
        baudot_bits.append(0)  # start (space)
        for i in range(5):
            baudot_bits.append((code >> i) & 1)
        baudot_bits.extend([1, 1])  # 1.5 stop bits (approximated as 2)

    # Preamble: 20 mark bits
    baudot_bits.extend([1] * 20)
    send_code(LTRS_SHIFT)
    shift = 'LTRS'

    for ch in text.upper():
        if ch in ITA2_LTRS:
            if shift != 'LTRS':
                send_code(LTRS_SHIFT); shift = 'LTRS'
            send_code(ITA2_LTRS[ch])
        elif ch in ITA2_FIGS:
            if shift != 'FIGS':
                send_code(FIGS_SHIFT); shift = 'FIGS'
            send_code(ITA2_FIGS[ch])

    send_code(LTRS_SHIFT)

    buf = StreamBuffer()
    phase = 0.0
    for bit in baudot_bits:
        freq = shift_hz / 2 if bit == 1 else -shift_hz / 2
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# AFSK (Bell 202 style)
# ══════════════════════════════════════════════════════════════════════════════
def gen_afsk(text, mark_hz=1200, space_hz=2200, baud=1200):
    data = text.encode('ascii')
    bits = []
    for b in data:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    # NRZI: 1=no change, 0=toggle
    nrzi, last = [], 0
    for b in bits:
        last = last if b == 1 else 1 - last
        nrzi.append(last)

    sps = int(SR / baud)
    buf = StreamBuffer()
    phase = 0.0
    for bit in nrzi:
        freq = mark_hz if bit == 1 else space_hz
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)
    buf.flush()

def gen_fsk441(text):
    """FSK441: meteor scatter, 441 baud, 4 tones."""
    bits = text_to_bits(text)
    bits += [0] * ((-len(bits)) % 2)
    baud = 441
    sps = int(SR / baud)
    tones = [882, 1323, 1764, 2205]  # 4 tone frequencies
    buf = StreamBuffer()
    phase = 0.0
    for i in range(0, len(bits), 2):
        sym = (bits[i] << 1) | bits[i + 1]
        ii, qq, phase = fsk_segment(sps, tones[sym], phase)
        buf.add(ii, qq)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# MFSK (Multi-Frequency Shift Keying) — varicode + FEC + interleaving
# ══════════════════════════════════════════════════════════════════════════════

# Varicode table (PSK31/MFSK standard, G3PLX)
# Variable-length codes; no code contains '00', so '00' is the inter-char separator
VARICODE = [
    "1010101011", "1011011011", "1011101101", "1101110111",  # NUL SOH STX ETX
    "1011101011", "1101011111", "1011101111", "1011111101",  # EOT ENQ ACK BEL
    "1011111111", "11101111",   "11101",      "1101101111",  # BS  HT  LF  VT
    "1011011101", "11111",      "1101110101", "1110101011",  # FF  CR  SO  SI
    "1011110111", "1011110101", "1110101101", "1110101111",  # DLE DC1 DC2 DC3
    "1101011011", "1101101011", "1101101101", "1101010111",  # DC4 NAK SYN ETB
    "1101111011", "1101111101", "1110110111", "1101010101",  # CAN EM  SUB ESC
    "1101011101", "1110111011", "1011111011", "1101111111",  # FS  GS  RS  US
    "1",          "111111111",  "101011111",  "111110101",   # SP  !   "   #
    "111011011",  "1011010101", "1010111011", "101111111",   # $   %   &   '
    "11111011",   "11110111",   "101101111",  "111011111",   # (   )   *   +
    "1110101",    "110101",     "1010111",    "110101111",   # ,   -   .   /
    "10110111",   "10111101",   "11101101",   "11111111",    # 0   1   2   3
    "101110111",  "101011011",  "101101011",  "110101101",   # 4   5   6   7
    "110101011",  "110110111",  "11110101",   "110111101",   # 8   9   :   ;
    "111101101",  "1010101",    "111010111",  "1010101111",  # <   =   >   ?
    "1010111101", "1111101",    "11101011",   "10101101",    # @   A   B   C
    "10110101",   "1110111",    "11011011",   "11111101",    # D   E   F   G
    "101010101",  "1111111",    "111111101",  "101111101",   # H   I   J   K
    "11010111",   "10111011",   "11011101",   "10101011",    # L   M   N   O
    "11010101",   "111011101",  "10101111",   "1101111",     # P   Q   R   S
    "1101101",    "101010111",  "110110101",  "101011101",   # T   U   V   W
    "101110101",  "101111011",  "1010101101", "111110111",   # X   Y   Z   [
    "111101111",  "111111011",  "1010111111", "101101101",   # \   ]   ^   _
    "1011011111", "1011",       "1011111",    "101111",      # `   a   b   c
    "101101",     "11",         "111101",     "1011011",     # d   e   f   g
    "101011",     "1101",       "111101011",  "10111111",    # h   i   j   k
    "11011",      "111011",     "1111",       "111",         # l   m   n   o
    "111111",     "110111111",  "10101",      "10111",       # p   q   r   s
    "101",        "110111",     "1111011",    "1101011",     # t   u   v   w
    "11011111",   "1011101",    "111010101",  "1010110111",  # x   y   z   {
    "110111011",  "1010110101", "1011010111", "1110110101",  # |   }   ~   DEL
]

def varicode_encode(text):
    """Encode text as varicode bit stream with '00' inter-character separators."""
    bits = []
    for ch in text:
        code = VARICODE[ord(ch) & 0x7F]
        for b in code:
            bits.append(int(b))
        bits.extend([0, 0])
    return bits

# ── Reverse lookup tables for decoders ────────────────────────────────────────
MORSE_REV = {v: k for k, v in MORSE.items()}

ITA2_LTRS_REV = {v: k for k, v in ITA2_LTRS.items()}
ITA2_FIGS_REV = {v: k for k, v in ITA2_FIGS.items()}

VARICODE_REV = {}
for _i, _code in enumerate(VARICODE):
    if _i < 128:
        VARICODE_REV[_code] = chr(_i)

def conv_encode_k7(bits):
    """Rate-1/2 convolutional encoder, K=7, polynomials G1=171o G2=133o."""
    poly = [0x79, 0x5B]
    k = 7
    mask = (1 << k) - 1
    reg = 0
    out = []
    for b in bits:
        reg = ((reg << 1) | b) & mask
        for p in poly:
            out.append(bin(reg & p).count('1') % 2)
    for _ in range(k - 1):
        reg = (reg << 1) & mask
        for p in poly:
            out.append(bin(reg & p).count('1') % 2)
    return out

def block_interleave(bits, cols):
    """Block interleaver: write by rows, read by columns."""
    rows = (len(bits) + cols - 1) // cols
    padded = bits + [0] * (rows * cols - len(bits))
    out = []
    for c in range(cols):
        for r in range(rows):
            out.append(padded[r * cols + c])
    return out

def gen_mfsk(text, n_tones=16, baud=15.625):
    """MFSK with varicode encoding, convolutional FEC, interleaving, Gray coding."""
    bits_per_sym = int(np.log2(n_tones))
    tone_spacing = baud
    base_offset = -n_tones / 2 * tone_spacing
    sps = int(SR / baud)

    # Encode: text → varicode → convolutional FEC → interleave
    vc_bits = varicode_encode(text)
    fec_bits = conv_encode_k7(vc_bits)
    il_bits = block_interleave(fec_bits, n_tones)
    il_bits += [0] * ((-len(il_bits)) % bits_per_sym)

    buf = StreamBuffer()
    phase = 0.0

    # Sync preamble: alternating low/high tones
    for k in range(16):
        freq = base_offset + (0 if k % 2 == 0 else (n_tones - 1)) * tone_spacing
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)

    # Data symbols with Gray-coded tone mapping
    for k in range(0, len(il_bits), bits_per_sym):
        sym = 0
        for j in range(bits_per_sym):
            sym = (sym << 1) | il_bits[k + j]
        sym ^= (sym >> 1)  # Binary → Gray code
        freq = base_offset + sym * tone_spacing
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# OLIVIA — Walsh-Hadamard coded MFSK with LFSR scrambling
# ══════════════════════════════════════════════════════════════════════════════
def gen_olivia(text, n_tones=8, bandwidth=500):
    """Olivia MFSK: each symbol spread over n_tones periods with LFSR scrambling."""
    baud = bandwidth / n_tones
    tone_spacing = baud
    base_offset = -bandwidth / 2
    sps = int(SR / baud)
    bits_per_sym = int(np.log2(n_tones))

    # Convert text to symbol values (0 to n_tones-1)
    bits = text_to_bits(text)
    bits += [0] * ((-len(bits)) % bits_per_sym)
    symbols = []
    for k in range(0, len(bits), bits_per_sym):
        sym = 0
        for j in range(bits_per_sym):
            sym = (sym << 1) | bits[k + j]
        symbols.append(sym)

    # LFSR scrambling sequence (x^9 + x^4 + 1, primitive, period 511)
    lfsr_reg = 0x1FF
    total_sym_periods = len(symbols) * n_tones
    scramble = []
    for _ in range(total_sym_periods):
        scramble.append(lfsr_reg % n_tones)
        bit = ((lfsr_reg >> 8) ^ (lfsr_reg >> 3)) & 1
        lfsr_reg = ((lfsr_reg << 1) | bit) & 0x1FF

    buf = StreamBuffer()
    phase = 0.0
    scr_idx = 0

    for c in symbols:
        # Each symbol value c is transmitted over n_tones consecutive periods
        # tone[k] = (c + scramble[k]) mod n_tones
        # Receiver unscrambles and uses majority voting / Walsh-Hadamard decode
        for k in range(n_tones):
            tone = (c + scramble[scr_idx]) % n_tones
            scr_idx += 1
            freq = base_offset + tone * tone_spacing
            i, q, phase = fsk_segment(sps, freq, phase)
            buf.add(i, q)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# THOR (IFK+ — Incremental Frequency Keying)
# ══════════════════════════════════════════════════════════════════════════════
def gen_thor(text, n_tones=64, baud=100.0):
    """THOR mode: varicode + convolutional FEC + interleaving + IFK+ modulation.
    IFK+ transmits the tone *difference* from the previous tone.
    Differences 0 and 1 are reserved for sync; data symbols offset by +2.
    THOR 100: 64 tones, 100 baud, 100 Hz spacing, ~6400 Hz bandwidth.
    """
    tone_spacing = baud
    bandwidth = n_tones * tone_spacing
    base_offset = -bandwidth / 2
    sps = int(SR / baud)
    data_tones = n_tones - 2  # 2 reserved for sync (differences 0 and 1)
    bits_per_sym = int(np.log2(data_tones))  # 5 bits for 62 data tones

    # Encode: text → varicode → convolutional FEC → interleave
    vc_bits = varicode_encode(text)
    fec_bits = conv_encode_k7(vc_bits)
    il_bits = block_interleave(fec_bits, n_tones)
    il_bits += [0] * ((-len(il_bits)) % bits_per_sym)

    # Map bits to data symbols (0 .. 2^bits_per_sym - 1)
    symbols = []
    for k in range(0, len(il_bits), bits_per_sym):
        sym = 0
        for j in range(bits_per_sym):
            sym = (sym << 1) | il_bits[k + j]
        symbols.append(sym)

    buf = StreamBuffer()
    phase = 0.0
    prev_tone = 0

    # Sync preamble: alternating differences 0 and 1
    for k in range(16):
        diff = k % 2
        prev_tone = (prev_tone + diff) % n_tones
        freq = base_offset + prev_tone * tone_spacing
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)

    # Data: IFK+ encoding — difference = symbol + 2
    for sym in symbols:
        diff = sym + 2
        prev_tone = (prev_tone + diff) % n_tones
        freq = base_offset + prev_tone * tone_spacing
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)
    buf.flush()

# ══════════════════════════════════════════════════════════════════════════════
# WEAK SIGNAL MODES (correct modulation, simplified encoding)
# ══════════════════════════════════════════════════════════════════════════════
def gen_gfsk_tones(text, n_tones, baud, tone_spacing, bt=2.0):
    """Generic GFSK multi-tone modulation used by FT8/FT4/WSPR/JT65."""
    bits = text_to_bits(text)
    bits_per_sym = max(1, int(np.log2(n_tones)))
    bits += [0] * ((-len(bits)) % bits_per_sym)
    sps = int(SR / baud)

    tones = []
    for k in range(0, len(bits), bits_per_sym):
        sym = 0
        for j in range(bits_per_sym):
            sym = (sym << 1) | bits[k + j]
        tones.append(sym % n_tones)

    base = -n_tones / 2 * tone_spacing
    freq_seq = np.array([base + t * tone_spacing for t in tones])

    # For low baud rates, work at reduced internal rate then upsample in chunks
    if sps > 200:
        internal_sps = 40
        freq_up = np.repeat(freq_seq, internal_sps).astype(float)
        n_gauss = max(3, int(4 * internal_sps))
        t_g = np.arange(n_gauss) / internal_sps - 2
        h = np.exp(-2 * (np.pi * bt * t_g) ** 2 / np.log(2))
        h /= h.sum()
        freq_smooth_low = np.convolve(freq_up, h, mode='same')

        total_len = len(tones) * sps
        x_old = np.linspace(0, 1, len(freq_smooth_low))
        phase = 0.0
        denom = max(total_len - 1, 1)
        for start in range(0, total_len, CHUNK_SAMPLES):
            end = min(start + CHUNK_SAMPLES, total_len)
            x_new = np.linspace(start / denom, (end - 1) / denom, end - start)
            freq_chunk = np.interp(x_new, x_old, freq_smooth_low)
            dphi = 2 * np.pi * freq_chunk / SR
            phi = phase + np.cumsum(dphi)
            phase = float(phi[-1])
            emit(127 * np.cos(phi), 127 * np.sin(phi))
    else:
        freq_up = np.repeat(freq_seq, sps).astype(float)
        n_gauss = max(3, int(4 * sps))
        t_g = np.arange(n_gauss) / sps - 2
        h = np.exp(-2 * (np.pi * bt * t_g) ** 2 / np.log(2))
        h /= h.sum()
        freq_smooth = np.convolve(freq_up, h, mode='same')

        phase = 0.0
        for start in range(0, len(freq_smooth), CHUNK_SAMPLES):
            end = min(start + CHUNK_SAMPLES, len(freq_smooth))
            dphi = 2 * np.pi * freq_smooth[start:end] / SR
            phi = phase + np.cumsum(dphi)
            phase = float(phi[-1])
            emit(127 * np.cos(phi), 127 * np.sin(phi))

def gen_ft8(text):
    gen_gfsk_tones(text, n_tones=8, baud=6.25, tone_spacing=6.25)

def gen_ft4(text):
    gen_gfsk_tones(text, n_tones=4, baud=12.5, tone_spacing=12.5)

def gen_wspr(text):
    gen_gfsk_tones(text[:6], n_tones=4, baud=1.4648, tone_spacing=1.4648, bt=1.0)

def gen_jt65(text):
    gen_gfsk_tones(text, n_tones=65, baud=2.6923, tone_spacing=2.6923, bt=1.0)

# ══════════════════════════════════════════════════════════════════════════════
# ANALOG MODES (AM / FM / SSB — text encoded as Morse audio)
# ══════════════════════════════════════════════════════════════════════════════
def gen_am(text, tone_hz=572, wpm=15):
    gen_cw(text, wpm=wpm, tone_hz=tone_hz, mode='AM')

def gen_nbfm(text, tone_hz=572, fdev=5000, wpm=15):
    gen_cw(text, wpm=wpm, tone_hz=tone_hz, fdev=fdev, mode='FM')

def gen_wbfm(text, tone_hz=572, wpm=15):
    gen_cw(text, wpm=wpm, tone_hz=tone_hz, fdev=75000, mode='FM')

def gen_ssb(text, sideband='USB', tone_hz=572, wpm=15):
    dot = int(1.2 / wpm * SR)
    audio = []
    for ch in text.upper():
        code = MORSE.get(ch, '')
        if ch == ' ':
            audio.append(np.zeros(4 * dot))
            continue
        for ei, sym in enumerate(code):
            n = dot if sym == '.' else 3 * dot
            t = np.arange(n) / SR
            audio.append(np.sin(2 * np.pi * tone_hz * t))
            if ei < len(code) - 1:
                audio.append(np.zeros(dot))
        audio.append(np.zeros(3 * dot))

    if not audio:
        return
    sig = np.concatenate(audio)

    # Hilbert transform for analytic signal
    from numpy.fft import fft, ifft
    n = len(sig)
    S = fft(sig)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = h[n // 2] = 1
        h[1:n // 2] = 2
    else:
        h[0] = 1
        h[1:(n + 1) // 2] = 2
    analytic = ifft(S * h)

    I = np.real(analytic) * 100
    Q = np.imag(analytic) * 100
    if sideband == 'LSB':
        Q = -Q
    for start in range(0, len(I), CHUNK_SAMPLES):
        end = min(start + CHUNK_SAMPLES, len(I))
        emit(I[start:end], Q[start:end])

# ══════════════════════════════════════════════════════════════════════════════
# AX.25 / APRS
# ══════════════════════════════════════════════════════════════════════════════
def ax25_fcs(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0x8408 if crc & 1 else crc >> 1
    return crc ^ 0xFFFF

def ax25_addr(callsign, ssid=0, last=False):
    cs = callsign.upper().ljust(6)[:6]
    addr = bytearray()
    for ch in cs:
        addr.append(ord(ch) << 1)
    ctrl = (ssid & 0xF) << 1
    if last:
        ctrl |= 1
    addr.append(0x60 | ctrl)
    return bytes(addr)

def gen_ax25(text, src='N0CALL', dst='APRS'):
    src_parts = (src.split('-') + ['0'])[:2]
    dst_parts = (dst.split('-') + ['0'])[:2]
    dst_addr = ax25_addr(dst_parts[0], int(dst_parts[1]), False)
    src_addr = ax25_addr(src_parts[0], int(src_parts[1]), True)
    frame_data = dst_addr + src_addr + bytes([0x03, 0xF0]) + text.encode('ascii')
    fcs = ax25_fcs(frame_data)
    frame = frame_data + bytes([fcs & 0xFF, (fcs >> 8) & 0xFF])

    # Bit-stuff: insert 0 after 5 consecutive 1s
    raw_bits = []
    for byte in frame:
        for i in range(8):
            raw_bits.append((byte >> i) & 1)
    stuffed, ones = [], 0
    for b in raw_bits:
        stuffed.append(b)
        if b == 1:
            ones += 1
            if ones == 5:
                stuffed.append(0); ones = 0
        else:
            ones = 0

    flag = [0, 1, 1, 1, 1, 1, 1, 0]
    all_bits = flag * 8 + stuffed + flag * 4

    # NRZI + AFSK1200
    nrzi, last = [], 1
    for b in all_bits:
        last = last if b == 1 else 1 - last
        nrzi.append(last)

    sps = int(SR / 1200)
    buf = StreamBuffer()
    phase = 0.0
    for bit in nrzi:
        freq = 1200 if bit == 1 else 2200
        i, q, phase = fsk_segment(sps, freq, phase)
        buf.add(i, q)
    buf.flush()

def gen_aprs(text, src='N0CALL'):
    aprs_info = '>' + text
    gen_ax25(aprs_info, src=src, dst='APRS')

# ══════════════════════════════════════════════════════════════════════════════
# WAV AUDIO MODULATION (record / TTS → transmit)
# ══════════════════════════════════════════════════════════════════════════════
def load_wav(path):
    """Load WAV file, return mono float32 audio (-1..1) and sample rate."""
    import wave
    with wave.open(path, 'rb') as wf:
        nch = wf.getnchannels()
        sw = wf.getsampwidth()
        rate = wf.getframerate()
        raw = wf.readframes(wf.getnframes())
    if sw == 2:
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    elif sw == 1:
        audio = np.frombuffer(raw, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
    elif sw == 4:
        audio = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
    else:
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if nch > 1:
        audio = audio[::nch]
    return audio, rate

def gen_wav_fm(wav_path, fdev=5000):
    """FM modulate audio from WAV file."""
    audio, rate = load_wav(wav_path)
    peak = np.max(np.abs(audio)) + 1e-10
    audio = audio / peak
    n_out = int(len(audio) * SR / rate)
    x_old = np.linspace(0, 1, len(audio))
    denom = max(n_out - 1, 1)
    phase = 0.0
    for start in range(0, n_out, CHUNK_SAMPLES):
        end = min(start + CHUNK_SAMPLES, n_out)
        x_new = np.linspace(start / denom, (end - 1) / denom, end - start)
        chunk = np.interp(x_new, x_old, audio)
        dphi = 2 * np.pi * fdev * chunk / SR
        phi = phase + np.cumsum(dphi)
        phase = float(phi[-1])
        emit(127 * np.cos(phi), 127 * np.sin(phi))

def gen_wav_am(wav_path):
    """AM modulate audio from WAV file."""
    audio, rate = load_wav(wav_path)
    peak = np.max(np.abs(audio)) + 1e-10
    audio = audio / peak
    n_out = int(len(audio) * SR / rate)
    x_old = np.linspace(0, 1, len(audio))
    denom = max(n_out - 1, 1)
    for start in range(0, n_out, CHUNK_SAMPLES):
        end = min(start + CHUNK_SAMPLES, n_out)
        x_new = np.linspace(start / denom, (end - 1) / denom, end - start)
        chunk = np.interp(x_new, x_old, audio)
        envelope = 1.0 + 0.8 * chunk
        emit(np.clip(envelope * 80, -127, 127), np.zeros(end - start))

def gen_wav_ssb(wav_path, sideband='USB'):
    """SSB modulate audio from WAV file."""
    audio, rate = load_wav(wav_path)
    peak = np.max(np.abs(audio)) + 1e-10
    audio = audio / peak
    # Hilbert transform at original sample rate (memory-efficient)
    from numpy.fft import fft, ifft
    n = len(audio)
    S = fft(audio)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = h[n // 2] = 1
        h[1:n // 2] = 2
    else:
        h[0] = 1
        h[1:(n + 1) // 2] = 2
    analytic = ifft(S * h)
    I_orig = np.real(analytic).astype(np.float32)
    Q_orig = np.imag(analytic).astype(np.float32)
    if sideband == 'LSB':
        Q_orig = -Q_orig
    # Upsample and emit in chunks
    n_out = int(n * SR / rate)
    x_old = np.linspace(0, 1, n)
    denom = max(n_out - 1, 1)
    for start in range(0, n_out, CHUNK_SAMPLES):
        end = min(start + CHUNK_SAMPLES, n_out)
        x_new = np.linspace(start / denom, (end - 1) / denom, end - start)
        I = np.interp(x_new, x_old, I_orig) * 100
        Q = np.interp(x_new, x_old, Q_orig) * 100
        emit(I, Q)

# ══════════════════════════════════════════════════════════════════════════════
# DEMODULATION (IQ → WAV for speech recognition)
# ══════════════════════════════════════════════════════════════════════════════
def demod_to_wav(iq_path, wav_path, mode='NBFM', audio_rate=16000):
    """Demodulate raw int8 IQ file to 16-bit mono WAV (chunked to limit memory)."""
    import wave, os

    file_size = os.path.getsize(iq_path)
    total_iq_samples = file_size // 2  # each IQ pair = 2 bytes
    dec = max(1, SR // audio_rate)

    # Process in chunks of ~2M IQ samples (~4 MB RAM per chunk)
    IQ_CHUNK = 2_000_000
    audio_chunks = []
    peak = 0.0
    prev_sample = None  # carry-over for FM discriminator

    with open(iq_path, 'rb') as f:
        while True:
            raw = np.frombuffer(f.read(IQ_CHUNK * 2), dtype=np.int8)
            if len(raw) < 2:
                break
            # Ensure even number of bytes
            if len(raw) % 2 != 0:
                raw = raw[:-1]
            I = raw[0::2].astype(np.float32)
            Q = raw[1::2].astype(np.float32)

            if mode in ('NBFM', 'WBFM'):
                signal = I + 1j * Q
                if prev_sample is not None:
                    signal = np.concatenate(([prev_sample], signal))
                prev_sample = signal[-1]
                product = signal[1:] * np.conj(signal[:-1])
                audio_raw = np.arctan2(np.imag(product), np.real(product))
            elif mode == 'AM':
                audio_raw = np.sqrt(I**2 + Q**2)
                audio_raw -= np.mean(audio_raw)
            else:
                # SSB
                bfo = 1500.0
                offset = 0 if prev_sample is None else int(np.real(prev_sample))
                t = np.arange(offset, offset + len(I), dtype=np.float64) / SR
                cos_t = np.cos(2 * np.pi * bfo * t).astype(np.float32)
                sin_t = np.sin(2 * np.pi * bfo * t).astype(np.float32)
                if mode == 'USB':
                    audio_raw = I * cos_t - Q * sin_t
                else:
                    audio_raw = I * cos_t + Q * sin_t
                # Store sample offset for continuity
                prev_sample = np.float32(offset + len(I))

            # Decimate this chunk
            n = (len(audio_raw) // dec) * dec
            if n > 0:
                chunk_audio = audio_raw[:n].reshape(-1, dec).mean(axis=1)
                chunk_peak = np.max(np.abs(chunk_audio))
                if chunk_peak > peak:
                    peak = chunk_peak
                audio_chunks.append(chunk_audio)

    if not audio_chunks:
        # Write a silent WAV if no audio
        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(audio_rate)
            wf.writeframes(b'')
        return

    # Normalize and write
    peak = peak + 1e-10
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(audio_rate)
        for chunk in audio_chunks:
            audio_int16 = np.clip(chunk / peak * 32767, -32768, 32767).astype(np.int16)
            wf.writeframes(audio_int16.tobytes())

# ══════════════════════════════════════════════════════════════════════════════
# SIGNAL DECODERS (WAV audio → text)
# ══════════════════════════════════════════════════════════════════════════════

def decode_cw(audio, rate):
    """Decode CW/Morse from demodulated audio."""
    # Bandpass filter around expected tone (400-1200 Hz)
    from numpy.fft import rfft, irfft
    n = len(audio)
    if n < rate // 10:
        return "[CW: signal too short]"
    freqs = np.fft.rfftfreq(n, 1.0 / rate)
    spectrum = rfft(audio)
    # Find peak tone frequency
    mag = np.abs(spectrum)
    tone_mask = (freqs >= 300) & (freqs <= 1500)
    if not np.any(tone_mask):
        return "[CW: no tone detected]"
    tone_idx = np.argmax(mag * tone_mask)
    tone_freq = freqs[tone_idx]
    # Bandpass around detected tone (+/- 100 Hz)
    bp_mask = (freqs >= tone_freq - 100) & (freqs <= tone_freq + 100)
    filtered_spec = spectrum * bp_mask
    filtered = np.real(irfft(filtered_spec, n))
    # Envelope detection: rectify + lowpass
    envelope = np.abs(filtered)
    # Lowpass the envelope (moving average, ~50 Hz cutoff)
    win = max(1, int(rate / 50))
    kernel = np.ones(win) / win
    envelope = np.convolve(envelope, kernel, mode='same')
    # Normalize
    env_max = np.max(envelope)
    if env_max < 1e-6:
        return "[CW: no signal detected]"
    envelope = envelope / env_max
    # Threshold to binary
    threshold = 0.35
    binary = (envelope > threshold).astype(int)
    # Find runs of on/off
    changes = np.diff(binary)
    on_starts = np.where(changes == 1)[0] + 1
    off_starts = np.where(changes == -1)[0] + 1
    if len(on_starts) == 0 or len(off_starts) == 0:
        return "[CW: no keying detected]"
    # Align: first on before first off
    if off_starts[0] < on_starts[0]:
        off_starts = off_starts[1:]
    min_len = min(len(on_starts), len(off_starts))
    if min_len == 0:
        return "[CW: insufficient keying]"
    on_starts = on_starts[:min_len]
    off_starts = off_starts[:min_len]
    on_durations = off_starts - on_starts
    # Adaptive timing: find the dot duration
    valid_durations = on_durations[on_durations > rate / 500]  # min 2ms
    if len(valid_durations) == 0:
        return "[CW: no valid elements]"
    # Cluster into short (dot) and long (dash) using median split
    median_dur = np.median(valid_durations)
    short_mask = valid_durations < median_dur * 1.5
    if np.any(short_mask):
        dot_dur = np.median(valid_durations[short_mask])
    else:
        dot_dur = median_dur / 3
    dot_dur = max(dot_dur, rate / 500)
    # Classify elements
    elements = []
    gaps = []
    for i in range(min_len):
        dur = on_durations[i]
        if dur < dot_dur * 2:
            elements.append('.')
        else:
            elements.append('-')
        # Gap after this element (before next on)
        if i < min_len - 1:
            gap = on_starts[i + 1] - off_starts[i]
            gaps.append(gap)
    # Decode using gaps to separate characters and words
    char_gap = dot_dur * 2.5
    word_gap = dot_dur * 5
    result = []
    current_code = elements[0] if elements else ''
    for i in range(len(gaps)):
        if gaps[i] > word_gap:
            # Word gap
            ch = MORSE_REV.get(current_code, '?')
            result.append(ch)
            result.append(' ')
            current_code = elements[i + 1] if i + 1 < len(elements) else ''
        elif gaps[i] > char_gap:
            # Character gap
            ch = MORSE_REV.get(current_code, '?')
            result.append(ch)
            current_code = elements[i + 1] if i + 1 < len(elements) else ''
        else:
            # Element gap (within character)
            current_code += elements[i + 1] if i + 1 < len(elements) else ''
    # Final character
    if current_code:
        ch = MORSE_REV.get(current_code, '?')
        result.append(ch)
    return ''.join(result)


def decode_rtty(audio, rate, baud=45.45, shift=170):
    """Decode RTTY (ITA2/Baudot) from demodulated audio."""
    from numpy.fft import rfft
    n = len(audio)
    if n < rate // 2:
        return "[RTTY: signal too short]"
    # Detect mark/space center frequencies
    freqs = np.fft.rfftfreq(n, 1.0 / rate)
    mag = np.abs(rfft(audio))
    # Find two strongest peaks separated by ~shift Hz
    tone_mask = (freqs >= 500) & (freqs <= 3000)
    mag_masked = mag * tone_mask
    peak1_idx = np.argmax(mag_masked)
    peak1_freq = freqs[peak1_idx]
    # Look for second peak near shift Hz away
    shift_mask = (np.abs(freqs - peak1_freq - shift) < shift * 0.3) | \
                 (np.abs(freqs - peak1_freq + shift) < shift * 0.3)
    if not np.any(shift_mask & tone_mask):
        # Fall back to standard RTTY tones
        mark_freq = 2125.0
        space_freq = 2295.0
    else:
        mag_shift = mag * shift_mask * tone_mask
        peak2_idx = np.argmax(mag_shift)
        peak2_freq = freqs[peak2_idx]
        # Mark is the lower frequency
        mark_freq = min(peak1_freq, peak2_freq)
        space_freq = max(peak1_freq, peak2_freq)
    # Bandpass filters for mark and space
    sps = int(rate / baud)
    # Correlation detector: multiply by mark/space tones, then integrate per bit
    t = np.arange(n, dtype=np.float64) / rate
    mark_ref = np.cos(2 * np.pi * mark_freq * t)
    space_ref = np.cos(2 * np.pi * space_freq * t)
    mark_energy = audio * mark_ref
    space_energy = audio * space_ref
    # Integrate over each bit period
    win = max(1, sps)
    kernel = np.ones(win) / win
    mark_smooth = np.convolve(mark_energy, kernel, mode='same')
    space_smooth = np.convolve(space_energy, kernel, mode='same')
    # Binary decision: mark=1 (high), space=0 (low)
    bit_signal = (np.abs(mark_smooth) > np.abs(space_smooth)).astype(int)
    # Sample at bit centers
    n_bits = n // sps
    bits = []
    for i in range(n_bits):
        center = i * sps + sps // 2
        if center < len(bit_signal):
            bits.append(bit_signal[center])
    # Skip preamble (find first start bit = 0 after mark idle = 1s)
    # Find first 0 after at least 5 consecutive 1s
    start_idx = 0
    ones_count = 0
    for i, b in enumerate(bits):
        if b == 1:
            ones_count += 1
        else:
            if ones_count >= 5:
                start_idx = i
                break
            ones_count = 0
    # Decode Baudot frames: start(0) + 5 data bits + stop(1)(1)
    result = []
    shift_state = 'LTRS'
    i = start_idx
    while i + 7 <= len(bits):
        if bits[i] != 0:
            i += 1
            continue
        # Start bit found
        data = 0
        for j in range(5):
            data |= bits[i + 1 + j] << j
        stop = bits[i + 6]
        if stop != 1:
            i += 1
            continue
        i += 7  # advance past frame (approximating 1.5 stop bits as 2)
        # Decode
        if data == LTRS_SHIFT:
            shift_state = 'LTRS'
            continue
        if data == FIGS_SHIFT:
            shift_state = 'FIGS'
            continue
        if shift_state == 'LTRS':
            ch = ITA2_LTRS_REV.get(data, '')
        else:
            ch = ITA2_FIGS_REV.get(data, '')
        if ch:
            result.append(ch)
    return ''.join(result)


def decode_bpsk(audio, rate, baud=31.25):
    """Decode BPSK (PSK31/63/125) from demodulated audio."""
    n = len(audio)
    if n < rate // 2:
        return "[BPSK: signal too short]"
    sps = int(rate / baud)
    # Find carrier frequency via spectral peak
    from numpy.fft import rfft
    freqs = np.fft.rfftfreq(n, 1.0 / rate)
    mag = np.abs(rfft(audio))
    tone_mask = (freqs >= 200) & (freqs <= 3000)
    carrier_idx = np.argmax(mag * tone_mask)
    carrier_freq = freqs[carrier_idx]
    if carrier_freq < 200:
        return "[BPSK: no carrier detected]"
    # Mix down to baseband
    t = np.arange(n, dtype=np.float64) / rate
    baseband_i = audio * np.cos(2 * np.pi * carrier_freq * t) * 2
    baseband_q = audio * -np.sin(2 * np.pi * carrier_freq * t) * 2
    # Lowpass filter (moving average at ~2x baud rate)
    win = max(1, int(rate / (baud * 2)))
    kernel = np.ones(win) / win
    bb_i = np.convolve(baseband_i, kernel, mode='same')
    bb_q = np.convolve(baseband_q, kernel, mode='same')
    # Compute phase
    phase = np.arctan2(bb_q, bb_i)
    # Sample at symbol centers
    n_syms = n // sps
    sym_phases = []
    for i in range(n_syms):
        center = i * sps + sps // 2
        if center < len(phase):
            sym_phases.append(phase[center])
    if len(sym_phases) < 2:
        return "[BPSK: too few symbols]"
    # Differential decode: phase change > pi/2 = 1, else 0
    bits = []
    for i in range(1, len(sym_phases)):
        dp = sym_phases[i] - sym_phases[i - 1]
        # Normalize to -pi..pi
        dp = (dp + np.pi) % (2 * np.pi) - np.pi
        bits.append(1 if abs(dp) > np.pi / 2 else 0)
    # Varicode decode: split on '00' separator
    result = []
    bitstr = ''.join(str(b) for b in bits)
    codes = bitstr.split('00')
    for code in codes:
        if code and code != '0':
            # Remove leading/trailing zeros that aren't part of varicode
            code = code.strip('0')
            if not code:
                continue
            ch = VARICODE_REV.get(code, '')
            if ch and ord(ch) >= 32:
                result.append(ch)
    decoded = ''.join(result)
    # Filter out garbage: keep only printable runs
    cleaned = ''.join(c for c in decoded if c.isprintable())
    return cleaned if cleaned else "[BPSK: no decodable text]"


def decode_afsk1200(audio, rate):
    """Decode Bell 202 AFSK1200 / AX.25 / APRS from demodulated audio."""
    n = len(audio)
    if n < rate // 4:
        return "[AFSK1200: signal too short]"
    baud = 1200
    mark_freq = 1200.0
    space_freq = 2200.0
    sps = int(rate / baud)
    # Correlation detector for mark/space
    t = np.arange(n, dtype=np.float64) / rate
    # Use short correlation windows (one bit period)
    win = sps
    mark_i = np.cos(2 * np.pi * mark_freq * t) * audio
    mark_q = np.sin(2 * np.pi * mark_freq * t) * audio
    space_i = np.cos(2 * np.pi * space_freq * t) * audio
    space_q = np.sin(2 * np.pi * space_freq * t) * audio
    kernel = np.ones(win) / win
    mark_mag = np.sqrt(np.convolve(mark_i, kernel, 'same') ** 2 +
                       np.convolve(mark_q, kernel, 'same') ** 2)
    space_mag = np.sqrt(np.convolve(space_i, kernel, 'same') ** 2 +
                        np.convolve(space_q, kernel, 'same') ** 2)
    # Binary: mark=1, space=0
    bit_signal = (mark_mag > space_mag).astype(int)
    # Sample at bit centers
    n_bits = n // sps
    bits = []
    for i in range(n_bits):
        center = i * sps + sps // 2
        if center < len(bit_signal):
            bits.append(bit_signal[center])
    # NRZI decode: no transition = 1, transition = 0
    nrzi_bits = []
    for i in range(1, len(bits)):
        nrzi_bits.append(1 if bits[i] == bits[i - 1] else 0)
    # Find AX.25 flags (0x7E = 01111110)
    flag = [0, 1, 1, 1, 1, 1, 1, 0]
    frames = []
    bitstr = nrzi_bits
    i = 0
    while i <= len(bitstr) - 8:
        if bitstr[i:i + 8] == flag:
            # Found flag, look for next flag
            j = i + 8
            while j <= len(bitstr) - 8:
                if bitstr[j:j + 8] == flag:
                    frame_bits = bitstr[i + 8:j]
                    if len(frame_bits) >= 48:  # minimum frame size
                        frames.append(frame_bits)
                    i = j
                    break
                j += 1
            else:
                break
        i += 1
    if not frames:
        return "[AFSK1200: no AX.25 frames detected]"
    results = []
    for frame_bits in frames:
        # Remove bit-stuffing: delete 0 after five consecutive 1s
        destuffed = []
        ones = 0
        skip = False
        for b in frame_bits:
            if skip:
                skip = False
                ones = 0
                continue
            destuffed.append(b)
            if b == 1:
                ones += 1
                if ones == 5:
                    skip = True  # next bit is stuffed 0
            else:
                ones = 0
        # Convert to bytes (LSB first, AX.25 convention)
        n_bytes = len(destuffed) // 8
        if n_bytes < 16:
            continue
        frame_bytes = bytearray()
        for k in range(n_bytes):
            byte = 0
            for j in range(8):
                byte |= destuffed[k * 8 + j] << j
            frame_bytes.append(byte)
        # Verify FCS (last 2 bytes)
        if len(frame_bytes) < 18:
            continue
        data = frame_bytes[:-2]
        fcs_recv = frame_bytes[-2] | (frame_bytes[-1] << 8)
        fcs_calc = ax25_fcs(data)
        fcs_ok = (fcs_recv == fcs_calc)
        # Parse addresses
        try:
            dst_call = ''.join(chr(b >> 1) for b in data[0:6]).strip()
            dst_ssid = (data[6] >> 1) & 0xF
            src_call = ''.join(chr(b >> 1) for b in data[7:13]).strip()
            src_ssid = (data[13] >> 1) & 0xF
            # Info field starts after control (1 byte) and PID (1 byte)
            info_start = 14
            # Skip digipeater addresses
            if not (data[13] & 1):  # more address bytes follow
                idx = 14
                while idx + 6 < len(data):
                    if data[idx + 6] & 1:
                        info_start = idx + 7
                        break
                    idx += 7
            if info_start + 2 <= len(data):
                info = data[info_start + 2:].decode('ascii', errors='replace')
            else:
                info = data[info_start:].decode('ascii', errors='replace')
            fcs_str = "OK" if fcs_ok else "BAD"
            src_str = f"{src_call}-{src_ssid}" if src_ssid else src_call
            dst_str = f"{dst_call}-{dst_ssid}" if dst_ssid else dst_call
            results.append(f"[{src_str}>{dst_str} FCS:{fcs_str}] {info}")
        except Exception:
            results.append(f"[AX.25 frame, {len(frame_bytes)} bytes, FCS:{'OK' if fcs_ok else 'BAD'}]")
    return '\n'.join(results) if results else "[AFSK1200: frames found but unparseable]"


def decode_mfsk(audio, rate, n_tones=16, baud=15.625):
    """Decode MFSK from demodulated audio (FFT tone detection + de-interleave + Viterbi)."""
    n = len(audio)
    if n < rate // 2:
        return "[MFSK: signal too short]"
    bits_per_sym = int(np.log2(n_tones))
    sps = int(rate / baud)
    tone_spacing = baud
    base_offset = -n_tones / 2 * tone_spacing
    n_syms = n // sps
    if n_syms < 20:
        return "[MFSK: too few symbols]"
    # FFT-based tone detection per symbol period
    symbols = []
    for i in range(n_syms):
        start = i * sps
        end = start + sps
        if end > n:
            break
        segment = audio[start:end]
        # FFT of this symbol
        fft_n = max(sps, 256)
        spec = np.abs(np.fft.rfft(segment, n=fft_n))
        fft_freqs = np.fft.rfftfreq(fft_n, 1.0 / rate)
        # Find which tone bin has the most energy
        best_tone = 0
        best_energy = 0
        for t in range(n_tones):
            tone_freq = abs(base_offset + t * tone_spacing)
            # Find nearest FFT bin
            bin_idx = np.argmin(np.abs(fft_freqs - tone_freq))
            # Sum energy around the bin
            lo = max(0, bin_idx - 1)
            hi = min(len(spec), bin_idx + 2)
            energy = np.sum(spec[lo:hi])
            if energy > best_energy:
                best_energy = energy
                best_tone = t
        # Gray decode: Gray → binary
        gray = best_tone
        binary = gray
        mask = gray >> 1
        while mask:
            binary ^= mask
            mask >>= 1
        symbols.append(binary)
    # Skip sync preamble (alternating low/high tones)
    data_start = 0
    for i in range(min(32, len(symbols) - 1)):
        if i >= 16:
            data_start = i
            break
        # Sync is alternating 0 and n_tones-1
        expected = 0 if i % 2 == 0 else n_tones - 1
        if symbols[i] != expected:
            data_start = i
            break
    data_symbols = symbols[data_start:]
    # Extract bits from symbols
    il_bits = []
    for sym in data_symbols:
        for j in range(bits_per_sym - 1, -1, -1):
            il_bits.append((sym >> j) & 1)
    # De-interleave (reverse block interleave: was written by rows, read by columns)
    cols = n_tones
    rows = (len(il_bits) + cols - 1) // cols
    padded = il_bits + [0] * (rows * cols - len(il_bits))
    deinterleaved = [0] * len(padded)
    idx = 0
    for c in range(cols):
        for r in range(rows):
            if idx < len(padded):
                deinterleaved[r * cols + c] = padded[idx]
                idx += 1
    # Viterbi decode (K=7, rate 1/2, polynomials G1=0x79 G2=0x5B)
    decoded_bits = _viterbi_decode_k7(deinterleaved)
    # Varicode decode
    bitstr = ''.join(str(b) for b in decoded_bits)
    codes = bitstr.split('00')
    result = []
    for code in codes:
        if code:
            ch = VARICODE_REV.get(code, '')
            if ch and ord(ch) >= 32:
                result.append(ch)
    decoded = ''.join(result)
    cleaned = ''.join(c for c in decoded if c.isprintable())
    return cleaned if cleaned else "[MFSK: no decodable text]"


def _viterbi_decode_k7(received_bits):
    """Viterbi decoder for rate-1/2 K=7 convolutional code (G1=0x79, G2=0x5B)."""
    poly = [0x79, 0x5B]
    k = 7
    n_states = 1 << (k - 1)
    mask = n_states - 1
    # Precompute output for each state and input bit
    outputs = {}
    for state in range(n_states):
        for inp in (0, 1):
            reg = ((state << 1) | inp) & ((1 << k) - 1)
            out = []
            for p in poly:
                out.append(bin(reg & p).count('1') % 2)
            outputs[(state, inp)] = out
    # Process pairs of received bits
    n_pairs = len(received_bits) // 2
    if n_pairs == 0:
        return []
    # Path metrics: [state] -> (metric, path)
    # Use arrays for efficiency
    INF = float('inf')
    path_metric = [INF] * n_states
    path_metric[0] = 0
    paths = [[] for _ in range(n_states)]
    for i in range(n_pairs):
        r0 = received_bits[2 * i]
        r1 = received_bits[2 * i + 1]
        new_metric = [INF] * n_states
        new_paths = [None] * n_states
        for state in range(n_states):
            if path_metric[state] == INF:
                continue
            for inp in (0, 1):
                next_state = ((state << 1) | inp) & mask
                expected = outputs[(state, inp)]
                dist = (r0 ^ expected[0]) + (r1 ^ expected[1])
                m = path_metric[state] + dist
                if m < new_metric[next_state]:
                    new_metric[next_state] = m
                    new_paths[next_state] = (state, inp)
        # Prune: keep only states within reasonable metric of best
        best = min(new_metric)
        if best == INF:
            break
        # Limit states to prevent memory explosion
        threshold = best + 12
        for s in range(n_states):
            if new_metric[s] > threshold:
                new_metric[s] = INF
                new_paths[s] = None
        path_metric = new_metric
        for s in range(n_states):
            if new_paths[s] is not None:
                prev_state, inp = new_paths[s]
                paths[s] = paths[prev_state] + [inp]
            elif path_metric[s] < INF:
                pass  # keep old path
            else:
                paths[s] = []
    # Find best final state
    best_state = min(range(n_states), key=lambda s: path_metric[s])
    return paths[best_state] if path_metric[best_state] < INF else []


def decode_olivia(audio, rate, n_tones=8, bw=500):
    """Decode Olivia from demodulated audio."""
    n = len(audio)
    if n < rate:
        return "[Olivia: signal too short]"
    baud = bw / n_tones
    tone_spacing = baud
    base_offset = -bw / 2
    sps = int(rate / baud)
    n_periods = n // sps
    if n_periods < n_tones * 2:
        return "[Olivia: too few symbol periods]"
    # FFT tone detection per period
    tone_sequence = []
    for i in range(n_periods):
        start = i * sps
        end = start + sps
        if end > n:
            break
        segment = audio[start:end]
        fft_n = max(sps, 256)
        spec = np.abs(np.fft.rfft(segment, n=fft_n))
        fft_freqs = np.fft.rfftfreq(fft_n, 1.0 / rate)
        best_tone = 0
        best_energy = 0
        for t in range(n_tones):
            tone_freq = abs(base_offset + t * tone_spacing)
            bin_idx = np.argmin(np.abs(fft_freqs - tone_freq))
            lo = max(0, bin_idx - 1)
            hi = min(len(spec), bin_idx + 2)
            energy = np.sum(spec[lo:hi])
            if energy > best_energy:
                best_energy = energy
                best_tone = t
        tone_sequence.append(best_tone)
    # LFSR descramble (x^9 + x^4 + 1)
    lfsr_reg = 0x1FF
    scramble = []
    for _ in range(len(tone_sequence)):
        scramble.append(lfsr_reg % n_tones)
        bit = ((lfsr_reg >> 8) ^ (lfsr_reg >> 3)) & 1
        lfsr_reg = ((lfsr_reg << 1) | bit) & 0x1FF
    descrambled = [(tone_sequence[i] - scramble[i]) % n_tones for i in range(len(tone_sequence))]
    # Group into blocks of n_tones periods per symbol
    # Majority voting across n_tones repetitions
    n_symbols = len(descrambled) // n_tones
    symbols = []
    for i in range(n_symbols):
        block = descrambled[i * n_tones:(i + 1) * n_tones]
        # Majority vote
        counts = [0] * n_tones
        for v in block:
            if 0 <= v < n_tones:
                counts[v] += 1
        symbols.append(np.argmax(counts))
    # Symbols to bits to ASCII
    bits_per_sym = int(np.log2(n_tones))
    bits = []
    for sym in symbols:
        for j in range(bits_per_sym - 1, -1, -1):
            bits.append((sym >> j) & 1)
    # Group into bytes
    result = []
    for i in range(0, len(bits) - 7, 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        if 32 <= byte < 127:
            result.append(chr(byte))
    decoded = ''.join(result)
    return decoded if decoded else "[Olivia: no decodable text]"


def decode_ft8(audio, rate):
    """Decode FT8 tone sequence (simplified — outputs tone values)."""
    n = len(audio)
    if n < rate:
        return "[FT8: signal too short]"
    baud = 6.25
    n_tones = 8
    tone_spacing = 6.25
    sps = int(rate / baud)
    n_syms = n // sps
    if n_syms < 10:
        return "[FT8: too few symbols]"
    # FFT per symbol to detect tone (0-7)
    tones = []
    for i in range(n_syms):
        start = i * sps
        end = start + sps
        if end > n:
            break
        segment = audio[start:end]
        fft_n = max(sps, 4096)
        spec = np.abs(np.fft.rfft(segment, n=fft_n))
        fft_freqs = np.fft.rfftfreq(fft_n, 1.0 / rate)
        best_tone = 0
        best_energy = 0
        for t in range(n_tones):
            tone_freq = t * tone_spacing
            bin_idx = np.argmin(np.abs(fft_freqs - tone_freq))
            lo = max(0, bin_idx - 2)
            hi = min(len(spec), bin_idx + 3)
            energy = np.sum(spec[lo:hi])
            if energy > best_energy:
                best_energy = energy
                best_tone = t
        tones.append(best_tone)
    # Output raw tone sequence
    tone_str = ' '.join(str(t) for t in tones)
    return f"[FT8 tones ({len(tones)} symbols): {tone_str}]"


def analyze_signal(audio, rate):
    """Auto-detect signal type from demodulated audio. Returns mode string."""
    from numpy.fft import rfft
    n = len(audio)
    if n < rate // 4:
        return "UNKNOWN"
    # Full-signal spectral analysis
    fft_n = min(n, 65536)
    spec = np.abs(rfft(audio[:fft_n]))
    freqs = np.fft.rfftfreq(fft_n, 1.0 / rate)
    # Normalize spectrum
    spec_max = np.max(spec)
    if spec_max < 1e-10:
        return "UNKNOWN"
    spec_norm = spec / spec_max
    # Find peaks (above -20 dB = 0.1 of max)
    peak_threshold = 0.1
    peaks = []
    in_peak = False
    peak_start = 0
    for i in range(1, len(spec_norm) - 1):
        if spec_norm[i] > peak_threshold and not in_peak:
            in_peak = True
            peak_start = i
        elif spec_norm[i] <= peak_threshold and in_peak:
            in_peak = False
            peak_idx = peak_start + np.argmax(spec_norm[peak_start:i])
            peaks.append((freqs[peak_idx], spec_norm[peak_idx]))
    n_peaks = len(peaks)
    peak_freqs = [p[0] for p in peaks]
    # Bandwidth measurement (-20 dB)
    above = np.where(spec_norm > peak_threshold)[0]
    if len(above) > 0:
        bw = freqs[above[-1]] - freqs[above[0]]
    else:
        bw = 0
    # Envelope analysis for baud rate estimation
    envelope = np.abs(audio)
    win = max(1, int(rate / 200))
    kernel = np.ones(win) / win
    env_smooth = np.convolve(envelope, kernel, mode='same')
    # Autocorrelation of envelope for baud rate
    env_centered = env_smooth - np.mean(env_smooth)
    max_lag = min(len(env_centered), int(rate / 5))  # down to 5 baud
    if max_lag > 100:
        acf = np.correlate(env_centered[:max_lag * 2], env_centered[:max_lag * 2], 'full')
        acf = acf[len(acf) // 2:]
        # Find first peak after initial decay
        min_lag = int(rate / 2000)  # up to 2000 baud
        if min_lag < len(acf) - 1:
            acf_search = acf[min_lag:]
            if len(acf_search) > 10:
                # Find first significant peak
                acf_norm = acf_search / (acf[0] + 1e-10)
                peak_candidates = []
                for i in range(1, len(acf_norm) - 1):
                    if acf_norm[i] > acf_norm[i - 1] and acf_norm[i] > acf_norm[i + 1] and acf_norm[i] > 0.2:
                        peak_candidates.append((i + min_lag, acf_norm[i]))
                if peak_candidates:
                    best_lag = peak_candidates[0][0]
                    est_baud = rate / best_lag
                else:
                    est_baud = 0
            else:
                est_baud = 0
        else:
            est_baud = 0
    else:
        est_baud = 0
    # On/off keying detection (for CW)
    env_max = np.max(env_smooth)
    if env_max > 1e-10:
        env_binary = (env_smooth / env_max > 0.35).astype(int)
        on_fraction = np.mean(env_binary)
        transitions = np.sum(np.abs(np.diff(env_binary)))
    else:
        on_fraction = 0
        transitions = 0
    # Decision tree
    # CW: single strong tone + on/off keying pattern
    if n_peaks <= 2 and transitions > 10 and 0.1 < on_fraction < 0.9:
        return "CW"
    # AFSK1200: two tones near 1200/2200 Hz
    if n_peaks >= 2:
        for f1 in peak_freqs:
            for f2 in peak_freqs:
                if abs(f1 - 1200) < 200 and abs(f2 - 2200) < 200:
                    return "AFSK1200"
    # RTTY: two tones ~170 Hz apart
    if n_peaks == 2 and len(peak_freqs) >= 2:
        tone_sep = abs(peak_freqs[1] - peak_freqs[0])
        if 100 < tone_sep < 250:
            return "RTTY"
    # FT8: 8+ tones, ~6.25 baud
    if n_peaks >= 4 and 3 < est_baud < 12:
        return "FT8"
    # BPSK31: narrow single carrier, ~31 baud
    if n_peaks <= 2 and bw < 100 and 20 < est_baud < 50:
        return "BPSK31"
    # MFSK: many tones
    if n_peaks >= 8 and bw > 200:
        if n_peaks >= 32:
            return "MFSK64"
        elif n_peaks >= 16:
            return "MFSK32"
        else:
            return "MFSK16"
    # Olivia: 8 tones within 500 Hz BW
    if 4 <= n_peaks <= 12 and bw < 600:
        return "OLIVIA8"
    # Report what we found
    return f"UNKNOWN (peaks={n_peaks}, bw={bw:.0f}Hz, baud~{est_baud:.1f})"


def decode_dispatch(decode_type, audio, rate):
    """Dispatch to the appropriate decoder."""
    decode_map = {
        'CW': decode_cw,
        'RTTY': lambda a, r: decode_rtty(a, r, 45.45, 170),
        'BPSK31': lambda a, r: decode_bpsk(a, r, 31.25),
        'BPSK63': lambda a, r: decode_bpsk(a, r, 62.5),
        'BPSK125': lambda a, r: decode_bpsk(a, r, 125.0),
        'AFSK1200': decode_afsk1200,
        'MFSK16': lambda a, r: decode_mfsk(a, r, 16, 15.625),
        'MFSK32': lambda a, r: decode_mfsk(a, r, 32, 31.25),
        'MFSK64': lambda a, r: decode_mfsk(a, r, 64, 62.5),
        'OLIVIA8': lambda a, r: decode_olivia(a, r, 8, 500),
        'OLIVIA16': lambda a, r: decode_olivia(a, r, 16, 500),
        'OLIVIA32': lambda a, r: decode_olivia(a, r, 32, 1000),
        'FT8': decode_ft8,
    }
    if decode_type in decode_map:
        return decode_map[decode_type](audio, rate)
    # If auto-detect returned UNKNOWN with details, report it
    if decode_type.startswith('UNKNOWN'):
        return f"[Auto-detect: {decode_type}]"
    return f"[Unknown decode mode: {decode_type}]"


# ══════════════════════════════════════════════════════════════════════════════
# JITTER FREQUENCY DATA ANALYSIS
# Peaks → 1, Valleys → 0 → Binary → Ciphers, Gematria, Math Anomalies
# ══════════════════════════════════════════════════════════════════════════════

# ── Gematria Tables ───────────────────────────────────────────────────────────

# Simple Gematria: A=1, B=2, ... Z=26
SIMPLE_GEMATRIA = {chr(65 + i): i + 1 for i in range(26)}
SIMPLE_GEMATRIA_REV = {v: k for k, v in SIMPLE_GEMATRIA.items()}

# English Gematria: A=6, B=12, C=18 ... Z=156 (multiples of 6)
ENGLISH_GEMATRIA = {chr(65 + i): (i + 1) * 6 for i in range(26)}
ENGLISH_GEMATRIA_REV = {v: k for k, v in ENGLISH_GEMATRIA.items()}

# Hebrew Gematria (Mispar Hechrachi / Absolute Value)
HEBREW_GEMATRIA = {
    'Aleph': 1, 'Bet': 2, 'Gimel': 3, 'Dalet': 4, 'He': 5,
    'Vav': 6, 'Zayin': 7, 'Chet': 8, 'Tet': 9, 'Yod': 10,
    'Kaf': 20, 'Lamed': 30, 'Mem': 40, 'Nun': 50, 'Samekh': 60,
    'Ayin': 70, 'Pe': 80, 'Tsadi': 90, 'Qof': 100, 'Resh': 200,
    'Shin': 300, 'Tav': 400,
}
# Hebrew letters (Unicode)
HEBREW_LETTERS = {
    1: '\u05D0', 2: '\u05D1', 3: '\u05D2', 4: '\u05D3', 5: '\u05D4',
    6: '\u05D5', 7: '\u05D6', 8: '\u05D7', 9: '\u05D8', 10: '\u05D9',
    20: '\u05DB', 30: '\u05DC', 40: '\u05DE', 50: '\u05E0', 60: '\u05E1',
    70: '\u05E2', 80: '\u05E4', 90: '\u05E6', 100: '\u05E7', 200: '\u05E8',
    300: '\u05E9', 400: '\u05EA',
}
# Hebrew to Latin transliteration for readability
HEBREW_TRANSLIT = {
    1: 'A', 2: 'B', 3: 'G', 4: 'D', 5: 'H', 6: 'V', 7: 'Z',
    8: 'Ch', 9: 'T', 10: 'Y', 20: 'K', 30: 'L', 40: 'M', 50: 'N',
    60: 'S', 70: 'Ay', 80: 'P', 90: 'Ts', 100: 'Q', 200: 'R',
    300: 'Sh', 400: 'Th',
}
HEBREW_VALUES = sorted(HEBREW_LETTERS.keys(), reverse=True)

# Abjad Numerals (Islamic / Arabic letter-number system — Mashriqi order)
ABJAD_NUMERALS = {
    'Alif': 1, 'Ba': 2, 'Jim': 3, 'Dal': 4, 'Ha': 5, 'Waw': 6,
    'Zayn': 7, 'Hha': 8, 'Ta': 9, 'Ya': 10, 'Kaf': 20, 'Lam': 30,
    'Mim': 40, 'Nun': 50, 'Sin': 60, 'Ayn': 70, 'Fa': 80, 'Sad': 90,
    'Qaf': 100, 'Ra': 200, 'Shin': 300, 'Ta2': 400, 'Tha': 500,
    'Kha': 600, 'Dhal': 700, 'Dad': 800, 'Zha': 900, 'Ghayn': 1000,
}
ABJAD_LETTERS = {
    1: '\u0627', 2: '\u0628', 3: '\u062C', 4: '\u062F', 5: '\u0647',
    6: '\u0648', 7: '\u0632', 8: '\u062D', 9: '\u0637', 10: '\u064A',
    20: '\u0643', 30: '\u0644', 40: '\u0645', 50: '\u0646', 60: '\u0633',
    70: '\u0639', 80: '\u0641', 90: '\u0635', 100: '\u0642', 200: '\u0631',
    300: '\u0634', 400: '\u062A', 500: '\u062B', 600: '\u062E', 700: '\u0630',
    800: '\u0636', 900: '\u0638', 1000: '\u063A',
}
ABJAD_TRANSLIT = {
    1: 'A', 2: 'B', 3: 'J', 4: 'D', 5: 'H', 6: 'W', 7: 'Z',
    8: 'Hh', 9: 'T', 10: 'Y', 20: 'K', 30: 'L', 40: 'M', 50: 'N',
    60: 'S', 70: 'Ay', 80: 'F', 90: 'Sd', 100: 'Q', 200: 'R',
    300: 'Sh', 400: 'T2', 500: 'Th', 600: 'Kh', 700: 'Dh', 800: 'Dd',
    900: 'Zh', 1000: 'Gh',
}
ABJAD_VALUES = sorted(ABJAD_LETTERS.keys(), reverse=True)

# Greek Isopsephy (Greek letter-number values)
GREEK_ISOPSEPHY = {
    1: '\u0391', 2: '\u0392', 3: '\u0393', 4: '\u0394', 5: '\u0395',
    6: '\u03DC', 7: '\u0396', 8: '\u0397', 9: '\u0398', 10: '\u0399',
    20: '\u039A', 30: '\u039B', 40: '\u039C', 50: '\u039D', 60: '\u039E',
    70: '\u039F', 80: '\u03A0', 90: '\u03D8', 100: '\u03A1', 200: '\u03A3',
    300: '\u03A4', 400: '\u03A5', 500: '\u03A6', 600: '\u03A7', 700: '\u03A8',
    800: '\u03A9', 900: '\u03E0',
}
GREEK_TRANSLIT = {
    1: 'A', 2: 'B', 3: 'G', 4: 'D', 5: 'E', 6: 'St', 7: 'Z',
    8: 'Et', 9: 'Th', 10: 'I', 20: 'K', 30: 'L', 40: 'M', 50: 'N',
    60: 'X', 70: 'O', 80: 'P', 90: 'Q', 100: 'R', 200: 'S',
    300: 'T', 400: 'U', 500: 'Ph', 600: 'Ch', 700: 'Ps', 800: 'Om',
    900: 'Sa',
}
GREEK_VALUES = sorted(GREEK_ISOPSEPHY.keys(), reverse=True)

# Mathematical constants for anomaly detection
PI_DIGITS = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
PHI_DIGITS = "16180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911375"
E_DIGITS = "27182818284590452353602874713526624977572470936999595749669676277240766303535475945713821785251664274"
SQRT2_DIGITS = "14142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727"
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
             987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
          59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
          127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181,
          191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]

# Bacon's cipher (A=aaaaa=00000, B=aaaab=00001, ... Z=11001)
BACON_REV = {}
for _i in range(26):
    _code = format(_i, '05b')
    BACON_REV[_code] = chr(65 + _i)


def _extract_peaks_valleys(audio, rate):
    """Extract binary stream from audio: peaks → 1, valleys → 0.
    Returns the raw binary list and metadata about the extraction."""
    n = len(audio)
    # Smooth to remove noise — adaptive window based on sample rate
    win = max(1, int(rate / 500))
    kernel = np.ones(win) / win
    smoothed = np.convolve(audio, kernel, mode='same')
    # Find local maxima and minima
    binary = []
    timestamps = []
    amplitudes = []
    # Use zero-crossing of the derivative to find peaks/valleys
    deriv = np.diff(smoothed)
    for i in range(1, len(deriv)):
        if deriv[i - 1] > 0 and deriv[i] <= 0:
            # Peak (local maximum)
            binary.append(1)
            timestamps.append(i / rate)
            amplitudes.append(float(smoothed[i]))
        elif deriv[i - 1] < 0 and deriv[i] >= 0:
            # Valley (local minimum)
            binary.append(0)
            timestamps.append(i / rate)
            amplitudes.append(float(smoothed[i]))
    # Also compute jitter intervals (time between consecutive peaks/valleys)
    intervals = []
    for i in range(1, len(timestamps)):
        intervals.append(timestamps[i] - timestamps[i - 1])
    return binary, timestamps, amplitudes, intervals


def _binary_to_groups(binary, group_size):
    """Split binary list into groups of group_size, return list of integer values."""
    groups = []
    for i in range(0, len(binary) - group_size + 1, group_size):
        val = 0
        for j in range(group_size):
            val = (val << 1) | binary[i + j]
        groups.append(val)
    return groups


def _num_to_hebrew(n):
    """Convert number to Hebrew letter(s) using additive decomposition."""
    if n <= 0 or n > 999:
        return str(n)
    letters = []
    translit = []
    remaining = n
    for v in HEBREW_VALUES:
        while remaining >= v:
            letters.append(HEBREW_LETTERS[v])
            translit.append(HEBREW_TRANSLIT[v])
            remaining -= v
    return ''.join(letters) + '(' + ''.join(translit) + ')' if letters else str(n)


def _num_to_abjad(n):
    """Convert number to Arabic/Abjad letter(s) using additive decomposition."""
    if n <= 0 or n > 1999:
        return str(n)
    letters = []
    translit = []
    remaining = n
    for v in ABJAD_VALUES:
        while remaining >= v:
            letters.append(ABJAD_LETTERS[v])
            translit.append(ABJAD_TRANSLIT[v])
            remaining -= v
    return ''.join(letters) + '(' + ''.join(translit) + ')' if letters else str(n)


def _num_to_greek(n):
    """Convert number to Greek letter(s) using additive decomposition."""
    if n <= 0 or n > 999:
        return str(n)
    letters = []
    translit = []
    remaining = n
    for v in GREEK_VALUES:
        while remaining >= v:
            letters.append(GREEK_ISOPSEPHY[v])
            translit.append(GREEK_TRANSLIT[v])
            remaining -= v
    return ''.join(letters) + '(' + ''.join(translit) + ')' if letters else str(n)


def _is_prime(n):
    """Check if n is prime."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def _digital_root(n):
    """Compute digital root (repeated digit sum until single digit)."""
    n = abs(n)
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def _check_math_constants(digit_string):
    """Check if a digit string appears in Pi, Phi, e, or sqrt(2). Returns matches."""
    matches = []
    if len(digit_string) >= 3:
        if digit_string in PI_DIGITS:
            pos = PI_DIGITS.index(digit_string)
            matches.append(f"Pi (position {pos})")
        if digit_string in PHI_DIGITS:
            pos = PHI_DIGITS.index(digit_string)
            matches.append(f"Phi/Golden Ratio (position {pos})")
        if digit_string in E_DIGITS:
            pos = E_DIGITS.index(digit_string)
            matches.append(f"Euler's e (position {pos})")
        if digit_string in SQRT2_DIGITS:
            pos = SQRT2_DIGITS.index(digit_string)
            matches.append(f"sqrt(2) (position {pos})")
    return matches


# Common English words for detection (2-letter minimum, frequency-ranked)
_COMMON_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'in', 'that', 'have', 'it', 'for',
    'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but',
    'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an',
    'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so',
    'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
    'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could',
    'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only',
    'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use',
    'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new',
    'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us',
    'is', 'are', 'was', 'were', 'been', 'being', 'am', 'has', 'had',
    'did', 'does', 'got', 'let', 'may', 'might', 'must', 'shall',
    'should', 'need', 'here', 'where', 'why', 'yes', 'no', 'god',
    'love', 'life', 'death', 'world', 'man', 'light', 'dark', 'water',
    'fire', 'earth', 'air', 'spirit', 'soul', 'mind', 'body', 'heart',
    'word', 'name', 'truth', 'peace', 'war', 'king', 'lord', 'help',
    'call', 'send', 'hear', 'speak', 'tell', 'ask', 'answer', 'open',
    'close', 'begin', 'end', 'start', 'stop', 'live', 'die', 'born',
    'free', 'hope', 'faith', 'grace', 'mercy', 'power', 'glory',
    'heaven', 'angel', 'demon', 'human', 'divine', 'sacred', 'holy',
    'sin', 'save', 'pray', 'bless', 'curse', 'heal', 'break', 'build',
    'rise', 'fall', 'sun', 'moon', 'star', 'tree', 'seed', 'root',
    'path', 'door', 'key', 'sign', 'code', 'message', 'signal',
    'frequency', 'wave', 'sound', 'voice', 'song', 'music', 'number',
    'zero', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'hundred', 'thousand', 'alpha', 'omega', 'genesis', 'exodus',
    'test', 'data', 'error', 'warn', 'info', 'debug', 'hello', 'hi',
    'ok', 'sos', 'cq', 'de', 'qth', 'qsl', 'roger', 'copy', 'over',
    'mayday', 'radio', 'transmit', 'receive', 'antenna', 'morse',
}


def _detect_words_in_binary(bitstring):
    """Scan the entire binary string at every bit offset and multiple bit widths
    to find readable words and sentences. Returns list of report lines."""
    findings = []
    n = len(bitstring)
    if n < 5:
        return findings

    # Also prepare inverted and bit-reversed variants
    inv_bitstring = ''.join('1' if b == '0' else '0' for b in bitstring)
    variants = [
        ('Normal', bitstring),
        ('Inverted', inv_bitstring),
    ]

    all_hits = []  # (score, description_lines)

    for var_name, bs in variants:
        for bit_width in [8, 7, 6, 5]:
            # Slide through every starting bit offset
            for offset in range(bit_width):
                # Decode entire stream from this offset
                chars = []
                positions = []
                for i in range(offset, len(bs) - bit_width + 1, bit_width):
                    val = int(bs[i:i + bit_width], 2)
                    if bit_width == 8 or bit_width == 7:
                        if 32 <= val < 127:
                            chars.append(chr(val))
                        else:
                            chars.append('\x00')  # non-printable marker
                    elif bit_width == 6:
                        # 6-bit: map 0-25=A-Z, 26-51=a-z, 52-61=0-9, 62=space, 63=.
                        if val < 26:
                            chars.append(chr(65 + val))
                        elif val < 52:
                            chars.append(chr(97 + val - 26))
                        elif val < 62:
                            chars.append(chr(48 + val - 52))
                        elif val == 62:
                            chars.append(' ')
                        else:
                            chars.append('.')
                    elif bit_width == 5:
                        # 5-bit: Bacon's cipher A-Z (0-25), rest as symbols
                        if val < 26:
                            chars.append(chr(65 + val))
                        else:
                            chars.append('\x00')
                    positions.append(i)

                if not chars:
                    continue

                text = ''.join(chars)

                # Also try LSB-first (bit-reversed within each group)
                chars_rev = []
                for i in range(offset, len(bs) - bit_width + 1, bit_width):
                    chunk = bs[i:i + bit_width][::-1]
                    val = int(chunk, 2)
                    if bit_width == 8 or bit_width == 7:
                        if 32 <= val < 127:
                            chars_rev.append(chr(val))
                        else:
                            chars_rev.append('\x00')
                    elif bit_width == 5:
                        if val < 26:
                            chars_rev.append(chr(65 + val))
                        else:
                            chars_rev.append('\x00')
                    else:
                        chars_rev.append(chr(val) if 32 <= val < 127 else '\x00')

                text_rev = ''.join(chars_rev)

                for endian_label, candidate in [('MSB', text), ('LSB', text_rev)]:
                    # Find runs of printable characters (min 2)
                    _scan_for_words(candidate, all_hits, var_name,
                                    bit_width, offset, endian_label, positions, bs)

    # Sort hits by score (best first), deduplicate by text content
    all_hits.sort(key=lambda x: -x[0])
    seen_texts = set()
    rank = 0
    for score, hit_lines in all_hits:
        # Extract the found text for dedup
        text_key = hit_lines[0] if hit_lines else ''
        if text_key in seen_texts:
            continue
        seen_texts.add(text_key)
        rank += 1
        if rank > 30:  # cap output
            findings.append(f"\n  ... ({len(all_hits) - 30} more hits omitted)")
            break
        for line in hit_lines:
            findings.append(line)

    if not all_hits:
        # Even with no word matches, show the longest printable runs
        findings.append(f"\n  No dictionary words found. Longest printable runs:")
        for var_name, bs in variants:
            for bw in [8, 7]:
                for off in range(bw):
                    chars = []
                    for i in range(off, len(bs) - bw + 1, bw):
                        val = int(bs[i:i + bw], 2)
                        if 32 <= val < 127:
                            chars.append(chr(val))
                        else:
                            chars.append('\x00')
                    text = ''.join(chars)
                    # Find longest printable run
                    best_run = ''
                    current_run = ''
                    for c in text:
                        if c != '\x00':
                            current_run += c
                        else:
                            if len(current_run) > len(best_run):
                                best_run = current_run
                            current_run = ''
                    if len(current_run) > len(best_run):
                        best_run = current_run
                    if len(best_run) >= 3:
                        findings.append(
                            f"    {var_name} {bw}-bit off={off}: "
                            f"\"{best_run[:60]}\" ({len(best_run)} chars)")

    return findings


def _scan_for_words(text, all_hits, var_name, bit_width, offset,
                    endian_label, positions, source_bits):
    """Scan decoded text for dictionary words and long printable runs.
    source_bits is the full bitstring this decode came from."""
    text_lower = text.lower()
    n = len(text)

    # 1. Find all dictionary word matches at every position
    word_matches = []  # (pos, word, whole_word)
    for pos in range(n):
        for word in _COMMON_WORDS:
            wlen = len(word)
            if pos + wlen <= n and text_lower[pos:pos + wlen] == word:
                before_ok = (pos == 0 or not text_lower[pos - 1].isalpha()
                             or text_lower[pos - 1] == '\x00')
                after_ok = (pos + wlen >= n or not text_lower[pos + wlen].isalpha()
                            or text_lower[pos + wlen] == '\x00')
                if before_ok and after_ok:
                    word_matches.append((pos, word, True))
                else:
                    word_matches.append((pos, word, False))

    # 2. Find long printable runs (potential sentences)
    printable_runs = []
    current_run_start = -1
    current_run = ''
    for i, c in enumerate(text):
        if c != '\x00' and c.isprintable():
            if current_run_start < 0:
                current_run_start = i
            current_run += c
        else:
            if len(current_run) >= 3:
                printable_runs.append((current_run_start, current_run))
            current_run = ''
            current_run_start = -1
    if len(current_run) >= 3:
        printable_runs.append((current_run_start, current_run))

    # 3. Score and report
    whole_words = [(p, w) for p, w, whole in word_matches if whole]
    embedded_words = [(p, w) for p, w, whole in word_matches if not whole and len(w) >= 3]

    score = (len(whole_words) * 10
             + sum(len(w) for _, w in whole_words)
             + len(embedded_words) * 3
             + sum(len(r) for _, r in printable_runs if len(r) >= 4) // 2)

    if score < 5:
        return

    hit_lines = []
    header = (f"\n  [{var_name} | {bit_width}-bit {endian_label} | "
              f"offset={offset} | score={score}]")
    hit_lines.append(header)

    # Show printable runs with raw binary for each
    for run_start, run_text in printable_runs[:5]:
        display_run = run_text[:80]
        if run_start < len(positions):
            from_bit = positions[run_start]
            run_chars = min(len(run_text), 80)
            to_bit = from_bit + run_chars * bit_width
            hit_lines.append(f"    Text : \"{display_run}\"")
            hit_lines.append(f"    Range: bit {from_bit} → {to_bit} "
                             f"({run_chars} chars x {bit_width}-bit)")
            # Show raw binary grouped per character (cap at 40 chars worth)
            show_chars = min(run_chars, 40)
            raw_parts = []
            for ci in range(show_chars):
                char_idx = run_start + ci
                if char_idx < len(positions):
                    bp = positions[char_idx]
                    raw_parts.append(source_bits[bp:bp + bit_width])
            raw_line = ' '.join(raw_parts)
            hit_lines.append(f"    Raw  : {raw_line}")
        else:
            hit_lines.append(f"    Text : \"{display_run}\"")

    if whole_words:
        word_list = []
        for p, w in whole_words[:12]:
            # Show the raw bits for each detected word
            if p < len(positions):
                bp = positions[p]
                word_bits = source_bits[bp:bp + len(w) * bit_width]
                spaced_bits = ' '.join(word_bits[i:i+bit_width]
                                       for i in range(0, len(word_bits), bit_width))
                word_list.append(f'"{w}" @char {p} (bit {bp}): {spaced_bits}')
            else:
                word_list.append(f'"{w}" @char {p}')
        hit_lines.append(f"    ── Words found ──")
        for wl in word_list:
            hit_lines.append(f"    {wl}")

    if embedded_words:
        emb_list = []
        for p, w in embedded_words[:8]:
            if p < len(positions):
                bp = positions[p]
                emb_list.append(f'"{w}" @char {p} (bit {bp})')
            else:
                emb_list.append(f'"{w}" @char {p}')
        hit_lines.append(f"    ── Embedded in larger text ──")
        for el in emb_list:
            hit_lines.append(f"    {el}")

    all_hits.append((score, hit_lines))


def jitter_analyze(audio, rate):
    """Full jitter frequency analysis: peaks/valleys → binary → all decoders."""
    lines = []
    lines.append("=" * 72)
    lines.append("  JITTER FREQUENCY DATA ANALYSIS")
    lines.append("  Peaks = 1 | Valleys = 0 | Water Flow Binary Extraction")
    lines.append("=" * 72)

    # ── Step 1: Extract binary from peaks/valleys ─────────────────────────
    binary, timestamps, amplitudes, intervals = _extract_peaks_valleys(audio, rate)
    n_bits = len(binary)

    if n_bits < 8:
        lines.append(f"\n[Insufficient data: only {n_bits} peaks/valleys detected]")
        return '\n'.join(lines)

    bitstring = ''.join(str(b) for b in binary)
    ones = binary.count(1)
    zeros = binary.count(0)

    lines.append(f"\n{'─' * 72}")
    lines.append("  EXTRACTION SUMMARY")
    lines.append(f"{'─' * 72}")
    lines.append(f"  Total peaks+valleys : {n_bits}")
    lines.append(f"  Peaks (1s)          : {ones} ({100*ones/n_bits:.1f}%)")
    lines.append(f"  Valleys (0s)        : {zeros} ({100*zeros/n_bits:.1f}%)")
    lines.append(f"  Ratio (1s/0s)       : {ones/(zeros+1e-10):.6f}")
    if intervals:
        lines.append(f"  Mean interval       : {np.mean(intervals)*1000:.3f} ms")
        lines.append(f"  Std dev interval    : {np.std(intervals)*1000:.3f} ms")
        lines.append(f"  Min/Max interval    : {np.min(intervals)*1000:.3f} / {np.max(intervals)*1000:.3f} ms")
    # ── Raw Binary Sequence (full) ──────────────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  RAW BINARY SEQUENCE (complete)")
    lines.append(f"{'─' * 72}")
    # Print in rows of 64 bits with offset labels
    for row_start in range(0, n_bits, 64):
        row_end = min(row_start + 64, n_bits)
        row = bitstring[row_start:row_end]
        # Add spacing every 8 bits for readability
        spaced = ' '.join(row[i:i+8] for i in range(0, len(row), 8))
        lines.append(f"  [{row_start:>6d}] {spaced}")

    # ── Word & Sentence Detection ────────────────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  WORD & SENTENCE DETECTION")
    lines.append("  (scanning every bit offset, all bit widths, normal + inverted)")
    lines.append(f"{'─' * 72}")

    word_findings = _detect_words_in_binary(bitstring)
    if word_findings:
        for finding in word_findings:
            lines.append(finding)
    else:
        lines.append("  (no recognizable words detected)")

    # ── Step 2: ASCII Decodings ───────────────────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  CIPHER DECODINGS")
    lines.append(f"{'─' * 72}")

    # 2a. Direct 8-bit ASCII
    ascii_8 = _binary_to_groups(binary, 8)
    ascii_text = ''.join(chr(v) if 32 <= v < 127 else '.' for v in ascii_8)
    lines.append(f"\n  [8-bit ASCII]")
    lines.append(f"  Values  : {ascii_8[:32]}{'...' if len(ascii_8) > 32 else ''}")
    lines.append(f"  Text    : {ascii_text[:64]}{'...' if len(ascii_text) > 64 else ''}")

    # 2b. 7-bit ASCII
    ascii_7 = _binary_to_groups(binary, 7)
    ascii7_text = ''.join(chr(v) if 32 <= v < 127 else '.' for v in ascii_7)
    lines.append(f"\n  [7-bit ASCII]")
    lines.append(f"  Values  : {ascii_7[:32]}{'...' if len(ascii_7) > 32 else ''}")
    lines.append(f"  Text    : {ascii7_text[:64]}{'...' if len(ascii7_text) > 64 else ''}")

    # 2c. 5-bit (Baudot/Bacon range)
    groups_5 = _binary_to_groups(binary, 5)
    lines.append(f"\n  [5-bit groups]")
    lines.append(f"  Values  : {groups_5[:40]}{'...' if len(groups_5) > 40 else ''}")

    # 2d. Bacon's Cipher (5-bit → letter)
    bacon_text = ''.join(BACON_REV.get(bitstring[i:i+5], '?')
                         for i in range(0, len(bitstring) - 4, 5))
    lines.append(f"\n  [Bacon's Cipher (5-bit binary → letter)]")
    lines.append(f"  Text    : {bacon_text[:64]}{'...' if len(bacon_text) > 64 else ''}")

    # 2e. Caesar cipher on 8-bit ASCII (all 26 rotations, show promising ones)
    lines.append(f"\n  [Caesar Cipher (shifts on 8-bit ASCII values)]")
    best_caesar = []
    for shift in range(1, 26):
        shifted = ''.join(chr(((v - 65 + shift) % 26) + 65)
                          if 65 <= v <= 90
                          else chr(((v - 97 + shift) % 26) + 97)
                          if 97 <= v <= 122
                          else chr(v) if 32 <= v < 127 else '.'
                          for v in ascii_8)
        printable = sum(1 for c in shifted if c.isalpha() or c == ' ')
        ratio = printable / max(len(shifted), 1)
        if ratio > 0.4 or shift <= 3:
            best_caesar.append((shift, shifted, ratio))
    for shift, text, ratio in best_caesar[:6]:
        marker = " <<<" if ratio > 0.6 else ""
        lines.append(f"  ROT-{shift:02d}  : {text[:48]}{marker}")

    # 2f. Atbash cipher (A↔Z, B↔Y, ...)
    atbash = ''.join(chr(155 - v) if 65 <= v <= 90
                     else chr(219 - v) if 97 <= v <= 122
                     else chr(v) if 32 <= v < 127 else '.'
                     for v in ascii_8)
    lines.append(f"\n  [Atbash Cipher (letter reversal)]")
    lines.append(f"  Text    : {atbash[:64]}")

    # 2g. XOR with common single-byte keys
    lines.append(f"\n  [XOR Single-Byte Keys (showing most printable)]")
    xor_results = []
    for key in range(1, 256):
        xored = ''.join(chr(v ^ key) if 32 <= (v ^ key) < 127 else '.' for v in ascii_8)
        printable = sum(1 for c in xored if c.isalnum() or c == ' ')
        ratio = printable / max(len(xored), 1)
        if ratio > 0.5:
            xor_results.append((key, xored, ratio))
    xor_results.sort(key=lambda x: -x[2])
    for key, text, ratio in xor_results[:5]:
        lines.append(f"  XOR 0x{key:02X} : {text[:48]} (printable: {ratio*100:.0f}%)")
    if not xor_results:
        lines.append(f"  (no XOR key produced >50% printable output)")

    # 2h. Bit reversal (LSB first instead of MSB)
    reversed_bits = list(binary)
    reversed_groups = []
    for i in range(0, len(reversed_bits) - 7, 8):
        chunk = reversed_bits[i:i+8]
        chunk.reverse()
        val = 0
        for b in chunk:
            val = (val << 1) | b
        reversed_groups.append(val)
    rev_text = ''.join(chr(v) if 32 <= v < 127 else '.' for v in reversed_groups)
    lines.append(f"\n  [Bit-Reversed 8-bit ASCII (LSB first)]")
    lines.append(f"  Text    : {rev_text[:64]}")

    # 2i. Inverted binary (0→1, 1→0)
    inv_binary = [1 - b for b in binary]
    inv_ascii = _binary_to_groups(inv_binary, 8)
    inv_text = ''.join(chr(v) if 32 <= v < 127 else '.' for v in inv_ascii)
    lines.append(f"\n  [Inverted Binary (NOT gate, 0<->1)]")
    lines.append(f"  Text    : {inv_text[:64]}")

    # 2j. Morse interpretation (runs of 1s: short=dot, long=dash)
    lines.append(f"\n  [Morse-style Run-Length Interpretation]")
    runs = []
    current = binary[0]
    count = 1
    for i in range(1, len(binary)):
        if binary[i] == current:
            count += 1
        else:
            runs.append((current, count))
            current = binary[i]
            count = 1
    runs.append((current, count))
    # Only 1-runs are signal; classify by median length
    one_runs = [r[1] for r in runs if r[0] == 1]
    if one_runs:
        med = np.median(one_runs)
        morse_code = ''
        morse_chars = []
        current_char = ''
        for val, cnt in runs:
            if val == 1:
                current_char += '.' if cnt < med * 1.5 else '-'
            else:
                if cnt > med * 4:  # word gap
                    if current_char:
                        morse_chars.append(MORSE_REV.get(current_char, '?'))
                        current_char = ''
                    morse_chars.append(' ')
                elif cnt > med * 1.5:  # char gap
                    if current_char:
                        morse_chars.append(MORSE_REV.get(current_char, '?'))
                        current_char = ''
        if current_char:
            morse_chars.append(MORSE_REV.get(current_char, '?'))
        morse_text = ''.join(morse_chars)
        lines.append(f"  Text    : {morse_text[:64]}")
    else:
        lines.append(f"  (no 1-runs detected)")

    # ── Step 3: Gematria Analysis ─────────────────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  GEMATRIA & SACRED NUMBER SYSTEMS")
    lines.append(f"{'─' * 72}")

    # Use 8-bit values as the primary number source
    values = ascii_8[:64]  # first 64 values for readability

    # 3a. Simple Gematria (1-26 range)
    lines.append(f"\n  [Simple Gematria (A=1 B=2 ... Z=26)]")
    simple_mapped = []
    for v in values:
        reduced = (v % 26) + 1 if v > 0 else 1
        letter = SIMPLE_GEMATRIA_REV.get(reduced, '?')
        simple_mapped.append(letter)
    simple_text = ''.join(simple_mapped)
    simple_sum = sum((v % 26) + 1 for v in values if v > 0)
    lines.append(f"  Text    : {simple_text[:64]}")
    lines.append(f"  Sum     : {simple_sum}")
    lines.append(f"  Digital root : {_digital_root(simple_sum)}")

    # 3b. English Gematria (multiples of 6)
    lines.append(f"\n  [English Gematria (A=6 B=12 ... Z=156)]")
    eng_mapped = []
    for v in values:
        nearest = min(ENGLISH_GEMATRIA.values(), key=lambda x: abs(x - v))
        eng_mapped.append(ENGLISH_GEMATRIA_REV[nearest])
    eng_text = ''.join(eng_mapped)
    eng_sum = sum(min(ENGLISH_GEMATRIA.values(), key=lambda x: abs(x - v)) for v in values)
    lines.append(f"  Text    : {eng_text[:64]}")
    lines.append(f"  Sum     : {eng_sum}")
    lines.append(f"  Digital root : {_digital_root(eng_sum)}")

    # 3c. Hebrew Gematria
    lines.append(f"\n  [Hebrew Gematria (Mispar Hechrachi)]")
    hebrew_mapped = []
    hebrew_sum = 0
    for v in values[:32]:
        capped = max(1, min(v, 400))
        hebrew_mapped.append(_num_to_hebrew(capped))
        hebrew_sum += capped
    lines.append(f"  Letters : {' '.join(hebrew_mapped[:16])}")
    if len(hebrew_mapped) > 16:
        lines.append(f"            {' '.join(hebrew_mapped[16:32])}")
    lines.append(f"  Sum     : {hebrew_sum}")
    lines.append(f"  Digital root : {_digital_root(hebrew_sum)}")
    # Notable Hebrew gematria values
    notable_hebrew = {
        26: 'YHVH (Tetragrammaton)', 86: 'Elohim', 345: 'El Shaddai/Moses',
        72: 'Chesed', 18: 'Chai (Life)', 36: 'Double Chai',
        137: 'Kabbalah', 358: 'Mashiach', 541: 'Israel',
        314: 'Shaddai/Metatron', 777: 'Perfection',
        13: 'Ahavah (Love)/Echad (One)', 40: 'Mem (Water/Trial)',
        50: 'Nun (Fish/Renewal)', 70: 'Ayin (Eye/Insight)',
    }
    for nv, meaning in notable_hebrew.items():
        if hebrew_sum == nv or simple_sum == nv:
            lines.append(f"  >>> MATCH: {nv} = {meaning}")
    # Check individual values
    notable_in_values = []
    for v in values:
        if v in notable_hebrew:
            notable_in_values.append(f"{v}={notable_hebrew[v]}")
    if notable_in_values:
        lines.append(f"  Values matching : {', '.join(notable_in_values[:8])}")

    # 3d. Abjad Numerals (Islamic)
    lines.append(f"\n  [Abjad Numerals (Islamic Tradition)]")
    abjad_mapped = []
    abjad_sum = 0
    for v in values[:32]:
        capped = max(1, min(v, 1000))
        abjad_mapped.append(_num_to_abjad(capped))
        abjad_sum += capped
    lines.append(f"  Letters : {' '.join(abjad_mapped[:16])}")
    if len(abjad_mapped) > 16:
        lines.append(f"            {' '.join(abjad_mapped[16:32])}")
    lines.append(f"  Sum     : {abjad_sum}")
    lines.append(f"  Digital root : {_digital_root(abjad_sum)}")
    # Notable Islamic numbers
    notable_islamic = {
        786: 'Bismillah (In the name of God)',
        66: 'Allah', 92: 'Muhammad', 110: 'Ali',
        19: 'Quran mathematical structure (Rashad)',
        114: 'Number of Surahs', 99: 'Names of Allah (Asma ul Husna)',
        7: 'Heavens / Fatiha verses', 40: 'Days of trial/purification',
        313: 'Badr warriors / Imam Mahdi companions',
        12: 'Twelve Imams', 5: 'Pillars of Islam / Ahl al-Bayt',
        14: 'Fourteen Infallibles (Shia)', 72: 'Martyrs of Karbala',
        30: 'Juz (sections of Quran)',
    }
    for nv, meaning in notable_islamic.items():
        if abjad_sum == nv:
            lines.append(f"  >>> MATCH: {nv} = {meaning}")
    abjad_notable_in = []
    for v in values:
        if v in notable_islamic:
            abjad_notable_in.append(f"{v}={notable_islamic[v]}")
    if abjad_notable_in:
        lines.append(f"  Values matching : {', '.join(abjad_notable_in[:8])}")

    # 3e. Greek Isopsephy
    lines.append(f"\n  [Greek Isopsephy]")
    greek_mapped = []
    greek_sum = 0
    for v in values[:32]:
        capped = max(1, min(v, 900))
        greek_mapped.append(_num_to_greek(capped))
        greek_sum += capped
    lines.append(f"  Letters : {' '.join(greek_mapped[:16])}")
    lines.append(f"  Sum     : {greek_sum}")
    lines.append(f"  Digital root : {_digital_root(greek_sum)}")

    # 3f. Sanskrit/Vedic Katapayadi system (consonant → digit mapping)
    lines.append(f"\n  [Katapayadi (Vedic/Sanskrit numeral encoding)]")
    # Map values 0-9 directly as Katapayadi digits
    kata_digits = [v % 10 for v in values]
    kata_str = ''.join(str(d) for d in kata_digits[:64])
    lines.append(f"  Digit sequence : {kata_str}")
    # Read as number (Katapayadi reads right-to-left)
    kata_rev = kata_str[:16][::-1]
    lines.append(f"  R-to-L (first 16) : {kata_rev}")

    # ── Step 4: Mathematical Anomaly Detection ────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  MATHEMATICAL ANOMALY DETECTION")
    lines.append(f"{'─' * 72}")

    anomalies_found = 0

    # 4a. Check binary string against mathematical constants
    lines.append(f"\n  [Digit String vs Mathematical Constants]")
    # Convert binary groups to digit strings
    digit_str_8 = ''.join(str(v) for v in ascii_8[:32])
    digit_str_5 = ''.join(str(v) for v in groups_5[:32])
    for label, dstr in [("8-bit values", digit_str_8), ("5-bit values", digit_str_5)]:
        # Search for matching substrings of length 4+
        for window in range(min(8, len(dstr)), 3, -1):
            for start in range(len(dstr) - window + 1):
                substr = dstr[start:start + window]
                matches = _check_math_constants(substr)
                if matches:
                    lines.append(f"  {label}[{start}:{start+window}] = '{substr}' found in: {', '.join(matches)}")
                    anomalies_found += 1
                    break  # one match per window size is enough
            if anomalies_found > 0:
                break

    # 4b. Check ratios between consecutive values for Golden Ratio
    lines.append(f"\n  [Ratio Analysis (Golden Ratio = 1.6180339...)]")
    golden_hits = []
    for i in range(1, min(len(values), 32)):
        if values[i - 1] > 0:
            ratio = values[i] / values[i - 1]
            if abs(ratio - 1.6180339887) < 0.05:
                golden_hits.append((i - 1, i, ratio))
                anomalies_found += 1
            elif abs(ratio - 0.6180339887) < 0.05:
                golden_hits.append((i - 1, i, ratio))
                anomalies_found += 1
    if golden_hits:
        for a, b, r in golden_hits[:5]:
            lines.append(f"  values[{a}]/values[{b-1}] = {values[b]}/{values[a]} = {r:.6f} ~ Phi!")
    else:
        lines.append(f"  (no consecutive pairs approximate Phi)")

    # 4c. Check for Pi-related values
    lines.append(f"\n  [Pi Proximity Detection (3.14159...)]")
    pi_hits = []
    for i, v in enumerate(values[:32]):
        # Check if value relates to Pi
        if v == 314 or v == 31 or v == 227:  # 227/72 ≈ Pi
            pi_hits.append((i, v, "direct Pi digits"))
            anomalies_found += 1
        # Check ratios
        if i > 0 and values[i - 1] > 0:
            r = v / values[i - 1]
            if abs(r - 3.14159) < 0.05:
                pi_hits.append((i, v, f"{v}/{values[i-1]} = {r:.5f} ~ Pi"))
                anomalies_found += 1
    if pi_hits:
        for idx, val, desc in pi_hits[:5]:
            lines.append(f"  values[{idx}] = {val}: {desc}")
    else:
        lines.append(f"  (no direct Pi relationships found)")

    # 4d. Fibonacci sequence detection
    lines.append(f"\n  [Fibonacci Sequence Detection]")
    fib_set = set(FIBONACCI)
    fib_in_values = [(i, v) for i, v in enumerate(values[:32]) if v in fib_set]
    if fib_in_values:
        lines.append(f"  Fibonacci numbers found: {', '.join(f'[{i}]={v}' for i,v in fib_in_values)}")
        anomalies_found += len(fib_in_values)
    # Check for Fibonacci-like sequences (each = sum of prior two)
    fib_runs = []
    for i in range(2, min(len(values), 32)):
        if values[i] == values[i-1] + values[i-2] and values[i] > 0:
            fib_runs.append(i)
    if fib_runs:
        lines.append(f"  Fibonacci-like sums at indices: {fib_runs}")
        anomalies_found += 1
    if not fib_in_values and not fib_runs:
        lines.append(f"  (no Fibonacci patterns detected)")

    # 4e. Prime number analysis
    lines.append(f"\n  [Prime Number Analysis]")
    prime_set = set(PRIMES)
    prime_values = [(i, v) for i, v in enumerate(values[:32]) if v in prime_set or _is_prime(v)]
    prime_count = len(prime_values)
    prime_ratio = prime_count / max(len(values[:32]), 1)
    lines.append(f"  Primes in values: {prime_count}/{min(len(values), 32)} ({prime_ratio*100:.1f}%)")
    if prime_ratio > 0.5:
        lines.append(f"  >>> ANOMALY: Unusually high prime density!")
        anomalies_found += 1
    if prime_values:
        lines.append(f"  Prime values: {', '.join(f'[{i}]={v}' for i,v in prime_values[:10])}")

    # 4f. Digital root analysis (numerology/sacred numbers)
    lines.append(f"\n  [Digital Root / Numerological Analysis]")
    roots = [_digital_root(v) for v in values[:32]]
    root_counts = {r: roots.count(r) for r in range(1, 10)}
    lines.append(f"  Root distribution: {root_counts}")
    dominant = max(root_counts, key=root_counts.get)
    dom_pct = root_counts[dominant] / max(len(roots), 1) * 100
    lines.append(f"  Dominant root: {dominant} ({dom_pct:.1f}%)")
    if dom_pct > 30:
        root_meanings = {
            1: 'Unity/Source/God', 2: 'Duality/Balance',
            3: 'Trinity/Creation/Divine', 4: 'Foundation/Earth',
            5: 'Change/Humanity/Pentagram', 6: 'Harmony/Star of David',
            7: 'Perfection/Spiritual completion', 8: 'Infinity/Resurrection',
            9: 'Completion/Wisdom/Enlightenment',
        }
        lines.append(f"  >>> NOTABLE: Root {dominant} = {root_meanings.get(dominant, 'unknown')}")
        anomalies_found += 1

    # 4g. Entropy analysis
    lines.append(f"\n  [Shannon Entropy Analysis]")
    if values:
        value_set = set(values)
        probs = [values.count(v) / len(values) for v in value_set]
        entropy = -sum(p * np.log2(p) for p in probs if p > 0)
        max_entropy = np.log2(max(len(value_set), 1))
        lines.append(f"  Entropy: {entropy:.4f} bits (max possible: {max_entropy:.4f})")
        lines.append(f"  Normalized entropy: {entropy/max(max_entropy,1e-10):.4f}")
        if entropy / max(max_entropy, 1e-10) < 0.5:
            lines.append(f"  >>> ANOMALY: Low entropy — structured/non-random data!")
            anomalies_found += 1
        elif entropy / max(max_entropy, 1e-10) > 0.95:
            lines.append(f"  >>> High entropy — appears random/encrypted")

    # 4h. Jitter interval analysis for sacred geometry
    if intervals and len(intervals) > 2:
        lines.append(f"\n  [Jitter Interval Ratios — Sacred Geometry Check]")
        int_array = np.array(intervals)
        # Check if interval ratios form musical/sacred proportions
        sacred_ratios = {
            'Octave (2:1)': 2.0, 'Fifth (3:2)': 1.5,
            'Fourth (4:3)': 1.333, 'Major Third (5:4)': 1.25,
            'Phi (Golden)': 1.6180339887, 'Pi/2': 1.5707963,
            'sqrt(2)': 1.41421356, 'sqrt(3)': 1.7320508,
        }
        for i in range(1, min(len(int_array), 32)):
            if int_array[i - 1] > 1e-10:
                r = int_array[i] / int_array[i - 1]
                for name, target in sacred_ratios.items():
                    if abs(r - target) < 0.02 or (target > 0 and abs(r - 1/target) < 0.02):
                        lines.append(f"  Intervals [{i-1}→{i}]: ratio {r:.6f} ~ {name}")
                        anomalies_found += 1
                        break

    # 4i. Binary palindrome check
    lines.append(f"\n  [Structural Patterns]")
    # Check segments for palindromes
    palindromes = []
    for width in [8, 16, 32]:
        for start in range(0, min(len(bitstring), 128) - width + 1, width):
            segment = bitstring[start:start + width]
            if segment == segment[::-1] and '1' in segment:
                palindromes.append((start, width, segment))
    if palindromes:
        lines.append(f"  Binary palindromes found:")
        for start, width, seg in palindromes[:5]:
            lines.append(f"    Bits [{start}:{start+width}] = {seg}")
        anomalies_found += len(palindromes)
    else:
        lines.append(f"  (no binary palindromes in first 128 bits)")

    # Check for repeating patterns
    for period in [4, 8, 12, 16]:
        if len(bitstring) >= period * 3:
            pattern = bitstring[:period]
            repeats = 0
            for i in range(period, len(bitstring) - period + 1, period):
                if bitstring[i:i + period] == pattern:
                    repeats += 1
                else:
                    break
            if repeats >= 2:
                lines.append(f"  Repeating {period}-bit pattern: {pattern} (repeats {repeats+1}x)")
                anomalies_found += 1

    # ── Step 5: Cross-System Concordance ──────────────────────────────────
    lines.append(f"\n{'─' * 72}")
    lines.append("  CROSS-SYSTEM CONCORDANCE")
    lines.append(f"{'─' * 72}")
    total_sum = sum(values[:32])
    lines.append(f"\n  Total sum of first 32 values: {total_sum}")
    lines.append(f"  Digital root: {_digital_root(total_sum)}")
    lines.append(f"  Mod 22 (Hebrew letters): {total_sum % 22} → {_num_to_hebrew(max(1, total_sum % 22 + 1))}")
    lines.append(f"  Mod 28 (Abjad letters): {total_sum % 28} → {_num_to_abjad(max(1, total_sum % 28 + 1))}")
    lines.append(f"  Mod 26 (Latin): {total_sum % 26} → {chr(65 + total_sum % 26)}")
    lines.append(f"  Is prime: {'Yes' if _is_prime(total_sum) else 'No'}")
    lines.append(f"  Is Fibonacci: {'Yes' if total_sum in fib_set else 'No'}")
    const_matches = _check_math_constants(str(total_sum))
    if const_matches:
        lines.append(f"  Found in: {', '.join(const_matches)}")
        anomalies_found += 1

    # Summary
    lines.append(f"\n{'─' * 72}")
    lines.append(f"  ANOMALIES DETECTED: {anomalies_found}")
    if anomalies_found == 0:
        lines.append(f"  Signal appears statistically normal.")
    elif anomalies_found <= 3:
        lines.append(f"  Minor anomalies — could be noise or coincidence.")
    elif anomalies_found <= 8:
        lines.append(f"  Moderate anomalies — warrants further investigation.")
    else:
        lines.append(f"  Significant anomalies — structured patterns detected!")
    lines.append(f"{'─' * 72}")

    return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# ANOMALY & EVENT LOG REPOSITORY
# Persistent JSON-based storage for all anomalies, events, and analysis results
# ══════════════════════════════════════════════════════════════════════════════

import json, os, time, uuid
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hackrf_logs')

# Severity levels (ascending)
SEV_INFO = 'INFO'
SEV_NOTABLE = 'NOTABLE'
SEV_ANOMALY = 'ANOMALY'
SEV_CRITICAL = 'CRITICAL'

# Categories
CAT_SYSTEM = 'SYSTEM'         # capture, demod, session start/stop
CAT_SIGNAL = 'SIGNAL'         # signal detection, mode identification
CAT_CIPHER = 'CIPHER'         # Caesar, Atbash, XOR, Bacon, ASCII, Morse
CAT_GEMATRIA = 'GEMATRIA'     # Hebrew, English, Simple, Abjad, Greek, Katapayadi
CAT_MATH = 'MATH'             # Pi, Phi, Fibonacci, primes, entropy, sacred geometry
CAT_WORD = 'WORD'             # word/sentence detection
CAT_PATTERN = 'PATTERN'       # repeating patterns, palindromes, structural


def _ensure_log_dir():
    """Create log directory if it doesn't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)


def _log_path(filename):
    """Return full path for a log file."""
    return os.path.join(LOG_DIR, filename)


def log_event(category, subcategory, severity, summary, detail='',
              frequency_mhz=None, demod_mode=None, decode_mode=None,
              duration_sec=None, raw_binary='', values=None,
              session_id=None):
    """Append a single event to the log repository."""
    _ensure_log_dir()
    entry = {
        'id': str(uuid.uuid4())[:8],
        'timestamp': datetime.now().isoformat(timespec='seconds'),
        'epoch': time.time(),
        'session_id': session_id or '',
        'category': category,
        'subcategory': subcategory,
        'severity': severity,
        'summary': summary,
        'detail': detail,
        'frequency_mhz': frequency_mhz,
        'demod_mode': demod_mode,
        'decode_mode': decode_mode,
        'duration_sec': duration_sec,
        'raw_binary': raw_binary[:2048] if raw_binary else '',
        'values': values or {},
    }
    with open(_log_path('events.jsonl'), 'a') as f:
        f.write(json.dumps(entry, default=str) + '\n')
    # Also write to anomalies file if severity warrants it
    if severity in (SEV_ANOMALY, SEV_CRITICAL, SEV_NOTABLE):
        with open(_log_path('anomalies.jsonl'), 'a') as f:
            f.write(json.dumps(entry, default=str) + '\n')
    return entry['id']


def log_session_start(frequency_mhz=None, demod_mode=None, mode_label=None):
    """Log a new session start, return session ID."""
    sid = str(uuid.uuid4())[:12]
    log_event(CAT_SYSTEM, 'session_start', SEV_INFO,
              f'Session started: {mode_label or "unknown"}',
              frequency_mhz=frequency_mhz, demod_mode=demod_mode,
              session_id=sid)
    return sid


def log_jitter_results(jitter_output, frequency_mhz=None, demod_mode=None,
                       duration_sec=None, session_id=None, bitstring=''):
    """Parse jitter analysis output and create categorized log entries."""
    lines = jitter_output.split('\n')
    events_logged = 0

    # Common kwargs
    kw = dict(frequency_mhz=frequency_mhz, demod_mode=demod_mode,
              duration_sec=duration_sec, session_id=session_id)

    # Extract key sections by scanning for markers
    current_section = ''
    section_lines = []

    for line in lines:
        stripped = line.strip()

        # Track sections
        if 'EXTRACTION SUMMARY' in stripped:
            current_section = 'extraction'
        elif 'WORD & SENTENCE DETECTION' in stripped:
            current_section = 'words'
        elif 'CIPHER DECODINGS' in stripped:
            current_section = 'cipher'
        elif 'GEMATRIA' in stripped and 'SACRED' in stripped:
            current_section = 'gematria'
        elif 'MATHEMATICAL ANOMALY' in stripped:
            current_section = 'math'
        elif 'CROSS-SYSTEM CONCORDANCE' in stripped:
            current_section = 'concordance'
        elif 'STRUCTURAL' in stripped or 'Structural' in stripped:
            current_section = 'pattern'

        # Log anomaly/notable markers
        if '>>> ANOMALY' in stripped or '>>> MATCH' in stripped or '>>> NOTABLE' in stripped:
            sev = SEV_ANOMALY if 'ANOMALY' in stripped else SEV_NOTABLE
            # Determine category from section
            if current_section == 'math':
                cat = CAT_MATH
            elif current_section == 'gematria':
                cat = CAT_GEMATRIA
            elif current_section == 'cipher':
                cat = CAT_CIPHER
            elif current_section == 'words':
                cat = CAT_WORD
            elif current_section == 'pattern':
                cat = CAT_PATTERN
            else:
                cat = CAT_SIGNAL
            subcat = current_section
            log_event(cat, subcat, sev, stripped.replace('>>>', '').strip(),
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log word detections with scores
        if 'score=' in stripped and current_section == 'words':
            log_event(CAT_WORD, 'detection', SEV_NOTABLE, stripped,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log whole word finds
        if 'Whole words:' in stripped:
            log_event(CAT_WORD, 'whole_word', SEV_ANOMALY, stripped,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log sacred geometry hits
        if 'ratio' in stripped and ('Phi' in stripped or 'Octave' in stripped
                                     or 'Fifth' in stripped or 'sqrt' in stripped):
            log_event(CAT_MATH, 'sacred_geometry', SEV_NOTABLE, stripped, **kw)
            events_logged += 1

        # Log Fibonacci finds
        if 'Fibonacci' in stripped and ('found' in stripped or 'sums' in stripped):
            log_event(CAT_MATH, 'fibonacci', SEV_NOTABLE, stripped, **kw)
            events_logged += 1

        # Log Pi/Phi constant matches
        if ('Pi (' in stripped or 'Phi/' in stripped or 'Euler' in stripped
                or 'sqrt(2)' in stripped) and 'position' in stripped:
            log_event(CAT_MATH, 'constant_match', SEV_ANOMALY, stripped,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log repeating patterns
        if 'Repeating' in stripped and 'pattern' in stripped:
            log_event(CAT_PATTERN, 'repeating', SEV_NOTABLE, stripped,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log palindromes
        if 'palindrome' in stripped.lower() and 'found' in stripped.lower():
            log_event(CAT_PATTERN, 'palindrome', SEV_NOTABLE, stripped,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1

        # Log Caesar/XOR hits with high printable ratio
        if '<<<' in stripped and current_section == 'cipher':
            log_event(CAT_CIPHER, 'caesar_hit', SEV_NOTABLE, stripped, **kw)
            events_logged += 1
        if 'XOR' in stripped and 'printable:' in stripped:
            log_event(CAT_CIPHER, 'xor_hit', SEV_NOTABLE, stripped, **kw)
            events_logged += 1

    # Log extraction summary
    for line in lines:
        if 'Total peaks+valleys' in line:
            log_event(CAT_SYSTEM, 'extraction', SEV_INFO, line.strip(),
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1
            break

    # Log the anomaly count summary
    for line in lines:
        if 'ANOMALIES DETECTED:' in line:
            count_str = line.strip()
            try:
                count = int(count_str.split(':')[1].strip())
                sev = SEV_CRITICAL if count > 8 else SEV_ANOMALY if count > 3 else SEV_INFO
            except (ValueError, IndexError):
                sev = SEV_INFO
            log_event(CAT_SYSTEM, 'anomaly_summary', sev, count_str,
                      raw_binary=bitstring[:512], **kw)
            events_logged += 1
            break

    return events_logged


def log_query(category=None, severity=None, search=None, limit=50,
              since=None, session_id=None):
    """Query the event log. Returns formatted report lines."""
    _ensure_log_dir()
    logfile = _log_path('anomalies.jsonl') if severity in (SEV_ANOMALY, SEV_CRITICAL) \
        else _log_path('events.jsonl')
    if not os.path.exists(logfile):
        return ["  (no log entries found)"]

    entries = []
    with open(logfile, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            # Apply filters
            if category and entry.get('category') != category:
                continue
            if severity and entry.get('severity') != severity:
                continue
            if session_id and entry.get('session_id') != session_id:
                continue
            if since and entry.get('epoch', 0) < since:
                continue
            if search and search.lower() not in json.dumps(entry).lower():
                continue
            entries.append(entry)

    if not entries:
        return ["  (no matching entries)"]

    # Most recent first
    entries.sort(key=lambda e: e.get('epoch', 0), reverse=True)
    entries = entries[:limit]

    lines = []
    for e in entries:
        ts = e.get('timestamp', '?')
        sev = e.get('severity', '?')
        cat = e.get('category', '?')
        sub = e.get('subcategory', '')
        summary = e.get('summary', '')
        freq = e.get('frequency_mhz')
        eid = e.get('id', '?')

        sev_icon = {'INFO': '.', 'NOTABLE': '*', 'ANOMALY': '!', 'CRITICAL': '!!'}
        icon = sev_icon.get(sev, '?')

        freq_str = f" @{freq}MHz" if freq else ''
        lines.append(f"  [{icon}] {ts} [{cat}/{sub}]{freq_str}")
        lines.append(f"      {summary}")

        detail = e.get('detail', '')
        if detail:
            for dl in detail.split('\n')[:2]:
                lines.append(f"      {dl}")

        raw = e.get('raw_binary', '')
        if raw:
            lines.append(f"      Binary: {raw[:80]}{'...' if len(raw) > 80 else ''}")
        lines.append('')

    return lines


def log_stats():
    """Generate statistics report across all logged events."""
    _ensure_log_dir()
    logfile = _log_path('events.jsonl')
    if not os.path.exists(logfile):
        return ["  (no log data)"]

    entries = []
    with open(logfile, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not entries:
        return ["  (no log entries)"]

    lines = []
    lines.append(f"  Total events logged: {len(entries)}")

    # By severity
    sev_counts = {}
    for e in entries:
        s = e.get('severity', 'UNKNOWN')
        sev_counts[s] = sev_counts.get(s, 0) + 1
    lines.append(f"\n  By Severity:")
    for s in [SEV_CRITICAL, SEV_ANOMALY, SEV_NOTABLE, SEV_INFO]:
        if s in sev_counts:
            lines.append(f"    {s:10s}: {sev_counts[s]}")

    # By category
    cat_counts = {}
    for e in entries:
        c = e.get('category', 'UNKNOWN')
        cat_counts[c] = cat_counts.get(c, 0) + 1
    lines.append(f"\n  By Category:")
    for c in sorted(cat_counts.keys()):
        lines.append(f"    {c:12s}: {cat_counts[c]}")

    # By subcategory
    sub_counts = {}
    for e in entries:
        s = e.get('subcategory', '')
        if s:
            sub_counts[s] = sub_counts.get(s, 0) + 1
    lines.append(f"\n  By Subcategory:")
    for s in sorted(sub_counts, key=lambda x: -sub_counts[x])[:15]:
        lines.append(f"    {s:20s}: {sub_counts[s]}")

    # Frequency distribution
    freq_counts = {}
    for e in entries:
        f = e.get('frequency_mhz')
        if f:
            freq_counts[f] = freq_counts.get(f, 0) + 1
    if freq_counts:
        lines.append(f"\n  By Frequency:")
        for f in sorted(freq_counts.keys()):
            lines.append(f"    {f} MHz: {freq_counts[f]} events")

    # Session count
    sessions = set(e.get('session_id', '') for e in entries if e.get('session_id'))
    lines.append(f"\n  Total sessions: {len(sessions)}")

    # Time span
    epochs = [e.get('epoch', 0) for e in entries if e.get('epoch')]
    if epochs:
        first = datetime.fromtimestamp(min(epochs)).strftime('%Y-%m-%d %H:%M:%S')
        last = datetime.fromtimestamp(max(epochs)).strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"  Time span: {first} → {last}")

    # Top anomalies (most repeated summaries)
    anomaly_entries = [e for e in entries if e.get('severity') in (SEV_ANOMALY, SEV_CRITICAL)]
    if anomaly_entries:
        summary_counts = {}
        for e in anomaly_entries:
            s = e.get('summary', '')[:80]
            summary_counts[s] = summary_counts.get(s, 0) + 1
        lines.append(f"\n  Top Recurring Anomalies:")
        for s in sorted(summary_counts, key=lambda x: -summary_counts[x])[:10]:
            lines.append(f"    [{summary_counts[s]}x] {s}")

    return lines


def log_export(format='text'):
    """Export the full log repository."""
    _ensure_log_dir()
    logfile = _log_path('events.jsonl')
    if not os.path.exists(logfile):
        return "(no log data to export)"

    entries = []
    with open(logfile, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if format == 'json':
        return json.dumps(entries, indent=2, default=str)
    elif format == 'csv':
        header = 'timestamp,severity,category,subcategory,frequency_mhz,summary,raw_binary\n'
        rows = []
        for e in entries:
            row = ','.join([
                str(e.get('timestamp', '')),
                str(e.get('severity', '')),
                str(e.get('category', '')),
                str(e.get('subcategory', '')),
                str(e.get('frequency_mhz', '')),
                '"' + str(e.get('summary', '')).replace('"', '""') + '"',
                str(e.get('raw_binary', ''))[:64],
            ])
            rows.append(row)
        return header + '\n'.join(rows)
    else:
        # Plain text report
        lines = []
        lines.append("=" * 72)
        lines.append("  HACKRF ANOMALY & EVENT LOG — FULL EXPORT")
        lines.append(f"  Generated: {datetime.now().isoformat(timespec='seconds')}")
        lines.append(f"  Total entries: {len(entries)}")
        lines.append("=" * 72)

        # Group by session
        sessions = {}
        no_session = []
        for e in entries:
            sid = e.get('session_id', '')
            if sid:
                sessions.setdefault(sid, []).append(e)
            else:
                no_session.append(e)

        for sid in sorted(sessions.keys(),
                          key=lambda s: min(e.get('epoch', 0) for e in sessions[s])):
            sess_entries = sessions[sid]
            sess_entries.sort(key=lambda e: e.get('epoch', 0))
            first_ts = sess_entries[0].get('timestamp', '?')
            freq = next((e.get('frequency_mhz') for e in sess_entries
                        if e.get('frequency_mhz')), '?')
            lines.append(f"\n{'─' * 72}")
            lines.append(f"  Session: {sid} | Started: {first_ts} | Freq: {freq} MHz")
            lines.append(f"{'─' * 72}")
            for e in sess_entries:
                sev = e.get('severity', '?')
                cat = e.get('category', '?')
                sub = e.get('subcategory', '')
                ts = e.get('timestamp', '?')
                summary = e.get('summary', '')
                lines.append(f"  [{sev:8s}] {ts} [{cat}/{sub}] {summary}")
                raw = e.get('raw_binary', '')
                if raw:
                    lines.append(f"             Binary: {raw[:80]}")

        if no_session:
            lines.append(f"\n{'─' * 72}")
            lines.append(f"  Unsessioned Events ({len(no_session)})")
            lines.append(f"{'─' * 72}")
            for e in no_session:
                lines.append(f"  [{e.get('severity','?'):8s}] {e.get('timestamp','?')} "
                             f"[{e.get('category','?')}] {e.get('summary','')}")

        lines.append(f"\n{'═' * 72}")
        return '\n'.join(lines)


def log_clear(archive=True):
    """Clear the log repository. If archive=True, rename to timestamped backup."""
    _ensure_log_dir()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    for fname in ['events.jsonl', 'anomalies.jsonl']:
        fpath = _log_path(fname)
        if os.path.exists(fpath):
            if archive:
                backup = _log_path(f'{fname}.{ts}.bak')
                os.rename(fpath, backup)
            else:
                os.remove(fpath)
    return f"Logs {'archived' if archive else 'cleared'} at {ts}"


# ══════════════════════════════════════════════════════════════════════════════
# DISPATCH
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    mode = sys.argv[1]

    # Handle demod modes separately (different arg format: MODE IQ_PATH WAV_PATH)
    if mode.startswith('DEMOD_'):
        iq_path = sys.argv[2] if len(sys.argv) > 2 else ''
        wav_path = sys.argv[3] if len(sys.argv) > 3 else '/tmp/demod.wav'
        demod_type = mode.replace('DEMOD_', '')
        demod_to_wav(iq_path, wav_path, demod_type)
        sys.exit(0)

    # Handle jitter frequency analysis (arg format: JITTER_ANALYZE WAV_PATH [FREQ] [DEMOD] [DUR] [SESSION_ID])
    if mode == 'JITTER_ANALYZE':
        wav_path = sys.argv[2] if len(sys.argv) > 2 else ''
        freq_mhz = float(sys.argv[3]) if len(sys.argv) > 3 else None
        demod = sys.argv[4] if len(sys.argv) > 4 else None
        dur = float(sys.argv[5]) if len(sys.argv) > 5 else None
        sid = sys.argv[6] if len(sys.argv) > 6 else None
        audio, audio_rate = load_wav(wav_path)
        result = jitter_analyze(audio, audio_rate)
        print(result)
        # Extract bitstring for logging
        binary, _, _, _ = _extract_peaks_valleys(audio, audio_rate)
        bitstring = ''.join(str(b) for b in binary)
        n_logged = log_jitter_results(result, frequency_mhz=freq_mhz,
                                       demod_mode=demod, duration_sec=dur,
                                       session_id=sid, bitstring=bitstring)
        print(f"\n  [{n_logged} events logged to repository]", file=sys.stderr)
        sys.exit(0)

    # Handle log repository commands (LOGSTORE_*)
    if mode.startswith('LOGSTORE_'):
        subcmd = mode.replace('LOGSTORE_', '')
        if subcmd == 'QUERY':
            cat = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '_' else None
            sev = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '_' else None
            search = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '_' else None
            limit = int(sys.argv[5]) if len(sys.argv) > 5 else 50
            result = log_query(category=cat, severity=sev, search=search, limit=limit)
            print('\n'.join(result))
        elif subcmd == 'STATS':
            result = log_stats()
            print('\n'.join(result))
        elif subcmd == 'EXPORT':
            fmt = sys.argv[2] if len(sys.argv) > 2 else 'text'
            output_path = sys.argv[3] if len(sys.argv) > 3 else ''
            result = log_export(format=fmt)
            if output_path:
                with open(output_path, 'w') as f:
                    f.write(result)
                print(f"Exported to {output_path}")
            else:
                print(result)
        elif subcmd == 'CLEAR':
            archive = sys.argv[2] != 'no_archive' if len(sys.argv) > 2 else True
            result = log_clear(archive=archive)
            print(result)
        elif subcmd == 'SESSION_START':
            freq = float(sys.argv[2]) if len(sys.argv) > 2 else None
            demod = sys.argv[3] if len(sys.argv) > 3 else None
            label = sys.argv[4] if len(sys.argv) > 4 else None
            sid = log_session_start(freq, demod, label)
            print(sid)
        elif subcmd == 'LOG_EVENT':
            # LOGSTORE_LOG_EVENT cat subcat sev summary [detail] [freq] [session_id]
            cat = sys.argv[2] if len(sys.argv) > 2 else CAT_SYSTEM
            subcat = sys.argv[3] if len(sys.argv) > 3 else ''
            sev = sys.argv[4] if len(sys.argv) > 4 else SEV_INFO
            summary = sys.argv[5] if len(sys.argv) > 5 else ''
            detail = sys.argv[6] if len(sys.argv) > 6 else ''
            freq = float(sys.argv[7]) if len(sys.argv) > 7 and sys.argv[7] != '_' else None
            sid = sys.argv[8] if len(sys.argv) > 8 else None
            eid = log_event(cat, subcat, sev, summary, detail=detail,
                            frequency_mhz=freq, session_id=sid)
            print(eid)
        else:
            print(f"Unknown LOGSTORE command: {subcmd}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # Handle decode modes (different arg format: MODE WAV_PATH)
    if mode.startswith('DECODE_'):
        wav_path = sys.argv[2] if len(sys.argv) > 2 else ''
        audio, audio_rate = load_wav(wav_path)
        decode_type = mode.replace('DECODE_', '')
        if decode_type == 'AUTO':
            detected = analyze_signal(audio, audio_rate)
            print(f"[DETECTED: {detected}]", file=sys.stderr)
            decode_type = detected
        result = decode_dispatch(decode_type, audio, audio_rate)
        print(result)
        sys.exit(0)

    msg  = sys.argv[2] if len(sys.argv) > 2 else ''
    wpm  = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    tone = float(sys.argv[4]) if len(sys.argv) > 4 else 572
    fdev = float(sys.argv[5]) if len(sys.argv) > 5 else 5000
    call = sys.argv[6] if len(sys.argv) > 6 else 'N0CALL'

    dispatch = {
        'CW_AM':     lambda: gen_cw(msg, wpm, tone, fdev, 'AM'),
        'CW_FM':     lambda: gen_cw(msg, wpm, tone, fdev, 'FM'),
        'BPSK31':    lambda: gen_bpsk(msg, 31.25),
        'BPSK63':    lambda: gen_bpsk(msg, 62.5),
        'BPSK125':   lambda: gen_bpsk(msg, 125.0),
        'QPSK31':    lambda: gen_qpsk(msg, 31.25),
        'QPSK63':    lambda: gen_qpsk(msg, 62.5),
        '8PSK125':   lambda: gen_8psk(msg, 125.0),
        '8PSK250':   lambda: gen_8psk(msg, 250.0),
        '8PSK500':   lambda: gen_8psk(msg, 500.0),
        '8PSK1200F': lambda: gen_8psk(msg, 1200.0),
        'RTTY45':    lambda: gen_rtty(msg, 45.45, 170.0),
        'RTTY50':    lambda: gen_rtty(msg, 50.0, 170.0),
        'FSK441':    lambda: gen_fsk441(msg),
        'AFSK1200':  lambda: gen_afsk(msg, 1200, 2200, 1200),
        'AFSK2400':  lambda: gen_afsk(msg, 1200, 2400, 2400),
        'MFSK16':    lambda: gen_mfsk(msg, 16, 15.625),
        'MFSK32':    lambda: gen_mfsk(msg, 32, 31.25),
        'MFSK64':    lambda: gen_mfsk(msg, 64, 62.5),
        'OLIVIA8':   lambda: gen_olivia(msg, 8, 500),
        'OLIVIA16':  lambda: gen_olivia(msg, 16, 500),
        'OLIVIA32':  lambda: gen_olivia(msg, 32, 1000),
        'THOR100':   lambda: gen_thor(msg, 64, 100.0),
        'FT8':       lambda: gen_ft8(msg),
        'FT4':       lambda: gen_ft4(msg),
        'WSPR':      lambda: gen_wspr(msg),
        'JT65':      lambda: gen_jt65(msg),
        'AM':        lambda: gen_am(msg, tone, wpm),
        'NBFM':      lambda: gen_nbfm(msg, tone, fdev, wpm),
        'WBFM':      lambda: gen_wbfm(msg, tone, wpm),
        'USB':       lambda: gen_ssb(msg, 'USB', tone, wpm),
        'LSB':       lambda: gen_ssb(msg, 'LSB', tone, wpm),
        'AX25':      lambda: gen_ax25(msg, src=call),
        'APRS':      lambda: gen_aprs(msg, src=call),
        'WAV_NBFM':  lambda: gen_wav_fm(msg, 5000),
        'WAV_WBFM':  lambda: gen_wav_fm(msg, 75000),
        'WAV_AM':    lambda: gen_wav_am(msg),
        'WAV_USB':   lambda: gen_wav_ssb(msg, 'USB'),
        'WAV_LSB':   lambda: gen_wav_ssb(msg, 'LSB'),
    }

    if mode in dispatch:
        dispatch[mode]()
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
