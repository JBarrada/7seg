a_, b_, c_, d_, e_, f_, g_, dp = range(8)

h20_h2f = [
    [],  # 0x20 space
    [],  # 0x21 exclam
    [],  # 0x22 double quote
    [],  # 0x23 pound sign
    [],  # 0x24 dollar
    [],  # 0x25 percent
    [],  # 0x26 ampersand
    [],  # 0x27 single quote
    [],  # 0x28 o parenth
    [],  # 0x29 c parenth
    [],  # 0x2a asterisk
    [],  # 0x2b plus
    [],  # 0x2c comma
    [],  # 0x2d hyphen
    [],  # 0x2e period
    [],  # 0x2f slash
]

h30_h39 = [
    [a_, b_, c_, d_, e_, f_],       # 0x30 0
    [b_, c_],                       # 0x31 1
    [a_, b_, d_, e_, g_],           # 0x32 2
    [a_, b_, c_, d_, g_],           # 0x33 3
    [b_, c_, f_, g_],               # 0x34 4
    [a_, c_, d_, f_, g_],           # 0x35 5
    [a_, c_, d_, e_, f_, g_],       # 0x36 6
    [a_, b_, c_],                   # 0x37 7
    [a_, b_, c_, d_, e_, f_, g_],   # 0x38 8
    [a_, b_, c_, f_, g_],           # 0x39 9
]

h3a_h40 = [
    [],  # 0x3a colon
    [],  # 0x3b semicolon
    [],  # 0x3c less than
    [],  # 0x3d equals
    [],  # 0x3e greater than
    [],  # 0x3f question mark
    [],  # 0x40 at symbol
]

h5b_h60 = [
    [],  # 0x5b o bracket
    [],  # 0x5c backslash
    [],  # 0x5d c bracket
    [],  # 0x5e caret
    [],  # 0x5f underscore
    [],  # 0x60 grave
]

hb0_hb9 = [
    [a_, b_, f_, g_],  # 0xb0 degree
    [],  # 0xb1 plus-minus
    [],  # 0xb2 super 2
    [],  # 0xb3 super 3
    [],  # 0xb4 acute accent
    [],  # 0xb5 micro
    [],  # 0xb6 pilcrow
    [],  # 0xb7 middle dot
    [],  # 0xb8 spacing cedilla
    [],  # 0xb9 super 1
]

alphabet = [
    [a_, b_, c_, e_, f_, g_],       # A
    [a_, b_, c_, d_, e_, f_, g_],   # B
    [a_, d_, e_, f_],               # C
    [a_, b_, c_, d_, e_, f_],       # D
    [a_, d_, e_, f_, g_],           # E
    [a_, e_, f_, g_],               # F
    [a_, b_, c_, d_, f_, g_],       # G
    [b_, c_, e_, f_, g_],           # H
    [b_, c_],                       # I
    [b_, c_, d_, e_],               # J
    [b_, c_, e_, f_, g_],           # K
    [d_, e_, f_],                   # L
    [a_, c_, e_],                   # M
    [c_, e_, g_],                   # N
    [a_, b_, c_, d_, e_, f_],       # O
    [a_, b_, e_, f_, g_],           # P
    [a_, b_, c_, f_, g_],           # Q
    [e_, g_],                       # R
    [a_, c_, d_, f_, g_],           # S
    [d_, e_, f_, g_],               # T
    [b_, c_, d_, e_, f_],           # U
    [c_, d_, e_],                   # V
    [b_, d_, f_],                   # W
    [b_, c_, e_, f_, g_],           # X
    [b_, c_, d_, f_, g_],           # Y
    [a_, b_, d_, e_, g_],           # Z
]


def char_segs(char):
    char = ord(char)

    if 0x00 <= char < 0x20:
        return []
    if 0x20 <= char < 0x30:
        return h20_h2f[char-0x20]
    if 0x30 <= char < 0x3a:
        return h30_h39[char-0x30]
    if 0x3a <= char < 0x41:
        return h3a_h40[char-0x3a]
    if 0x41 <= char < 0x5b:
        return alphabet[char-0x41]
    if 0x5b <= char < 0x61:
        return h5b_h60[char-0x5b]
    if 0x61 <= char < 0x7b:
        return alphabet[char-0x61]
    if 0x7b <= char < 0xb0:
        return []
    if 0xb0 <= char < 0xba:
        return hb0_hb9[char-0xb0]
    if 0xba <= char <= 0xff:
        return []
