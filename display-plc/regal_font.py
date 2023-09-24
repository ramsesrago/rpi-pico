font = bytearray([
    7, # Height - MAXIMUM OF 16 PIXELS!
       # values above 8 will assign two bytes per column to font data
    6, # Max Width - Number of columns per char

#   105 entry lookup table for each character width
#      !  "  #  $  %  &  '  (  )  *  +  ,  -  .  /
    1, 1, 3, 5, 5, 5, 6, 1, 2, 2, 3, 3, 1, 3, 2, 3,
#   0  1  2  3  4  5  6  7  8  9  :  ;  <  =  >  ?
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 3, 3, 3, 4,
#   @  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
    6, 5, 5, 5, 5, 5, 4, 5, 4, 3, 4, 4, 4, 5, 5, 5,
#   P  Q  R  S  T  U  V  W  X  Y  Z  [  \  ]  ^  _
    5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 2, 3, 2, 3, 3,
#   `  a  b  c  d  e  f  g  h  i  j  k  l  m  n  o
    2, 5, 5, 5, 5, 4, 4, 5, 4, 3, 4, 4, 4, 5, 5, 5,
#   p  q  r  s  t  u  v  w  x  y  z  {  |  }  ~
    5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 3, 1, 3, 3, 1,

#   Extra
#   Æ  Þ  ß  æ  þ  £  ¥  ©  °
    5, 5, 4, 5, 5, 4, 4, 4, 3,

#   Character Data
#   Must be blocks of max-width * math.ceil(height / 8)
#   Each byte (or pair of bytes) represents a vertical column of pixels
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, #
    0x2e, 0x00, 0x00, 0x00, 0x00, 0x00, # !
    0x06, 0x00, 0x06, 0x00, 0x00, 0x00, # "
    0x14, 0x3e, 0x14, 0x3e, 0x14, 0x00, # #
    0x04, 0x2a, 0x3e, 0x2a, 0x10, 0x00, # $
    0x22, 0x10, 0x08, 0x04, 0x22, 0x00, # %
    0x14, 0x2a, 0x2a, 0x2c, 0x10, 0x28, # &
    0x06, 0x00, 0x00, 0x00, 0x00, 0x00, # '
    0x1c, 0x22, 0x00, 0x00, 0x00, 0x00, # (
    0x22, 0x1c, 0x00, 0x00, 0x00, 0x00, # )
    0x14, 0x08, 0x14, 0x00, 0x00, 0x00, # *
    0x08, 0x1c, 0x08, 0x00, 0x00, 0x00, # +
    0x60, 0x00, 0x00, 0x00, 0x00, 0x00, # ,
    0x08, 0x08, 0x08, 0x00, 0x00, 0x00, # -
    0x60, 0x60, 0x00, 0x00, 0x00, 0x00, # .
    0x30, 0x0c, 0x02, 0x00, 0x00, 0x00, # /

    #0x1e, 0x31, 0x29, 0x25, 0x1e, 0x00, # 0
    0x3e, 0x51, 0x49, 0x45, 0x3e, 0x00, # 0
    #0x02, 0x3e, 0x00, 0x00, 0x00, 0x00, # 1
    0x00, 0x42, 0x7f, 0x40, 0x00, 0x00, # 1
    #0x62, 0x51, 0x49, 0x45, 0x42, 0x00, # 2
    0x72, 0x49, 0x49, 0x49, 0x46, 0x00, # 2
    0x21, 0x41, 0x49, 0x4d, 0x33, 0x00, # 3
    #0x08, 0x0c, 0x0a, 0x7f, 0x08, 0x00, # 4
    0x18, 0x14, 0x12, 0x7f, 0x10, 0x00, # 4
    0x27, 0x45, 0x45, 0x45, 0x39, 0x00, # 5
    0x3c, 0x4a, 0x49, 0x49, 0x31, 0x00, # 6
    0x41, 0x21, 0x11, 0x09, 0x07, 0x00, # 7
    0x36, 0x49, 0x49, 0x49, 0x36, 0x00, # 8
    0x46, 0x49, 0x49, 0x29, 0x1e, 0x00, # 9
    0x24, 0x00, 0x00, 0x00, 0x00, 0x00, # :
    0x64, 0x00, 0x00, 0x00, 0x00, 0x00, # ;
    0x08, 0x14, 0x22, 0x00, 0x00, 0x00, # <
    0x14, 0x14, 0x14, 0x00, 0x00, 0x00, # =
    0x22, 0x14, 0x08, 0x00, 0x00, 0x00, # >
    0x02, 0x2a, 0x0a, 0x04, 0x00, 0x00, # ?

#   Uppercase
    0x3c, 0x02, 0x1a, 0x2a, 0x22, 0x1e, # @
    0x7c, 0x12, 0x11, 0x12, 0x7c, 0x00, # A
    0x3c, 0x2a, 0x2a, 0x2e, 0x10, 0x00, # B
    0x3e, 0x41, 0x41, 0x41, 0x22, 0x00, # C
    0x3c, 0x22, 0x22, 0x22, 0x1c, 0x00, # D
    0x7f, 0x49, 0x49, 0x49, 0x41, 0x00, # E
    0x3c, 0x12, 0x12, 0x12, 0x00, 0x00, # F
    0x3c, 0x22, 0x22, 0x2a, 0x1a, 0x00, # G
    0x3e, 0x08, 0x08, 0x3e, 0x00, 0x00, # H
    0x22, 0x3e, 0x22, 0x00, 0x00, 0x00, # I
    0x30, 0x22, 0x22, 0x1e, 0x00, 0x00, # J
    0x3e, 0x08, 0x0c, 0x32, 0x00, 0x00, # K
    0x3e, 0x20, 0x20, 0x20, 0x00, 0x00, # L
    0x3c, 0x02, 0x3c, 0x02, 0x3c, 0x00, # M
    0x3c, 0x02, 0x02, 0x02, 0x3e, 0x00, # N
    0x1c, 0x22, 0x22, 0x22, 0x1e, 0x00, # O

    0x3c, 0x12, 0x12, 0x12, 0x0e, 0x00, # P
    0x1c, 0x22, 0x22, 0x62, 0x1e, 0x00, # Q
    0x3c, 0x12, 0x12, 0x32, 0x0e, 0x00, # R
    0x24, 0x2a, 0x2a, 0x12, 0x00, 0x00, # S
    0x03, 0x01, 0x7f, 0x01, 0x03, 0x00, # T
    0x1e, 0x20, 0x20, 0x20, 0x1e, 0x00, # U
    0x0e, 0x10, 0x20, 0x10, 0x0e, 0x00, # V
    0x3e, 0x20, 0x1e, 0x20, 0x1e, 0x00, # W
    0x36, 0x08, 0x08, 0x36, 0x00, 0x00, # X
    0x26, 0x28, 0x28, 0x1e, 0x00, 0x00, # Y
    0x32, 0x2a, 0x2a, 0x26, 0x00, 0x00, # Z
    0x3e, 0x22, 0x00, 0x00, 0x00, 0x00, # [
    0x02, 0x0c, 0x30, 0x00, 0x00, 0x00, # "\"
    0x22, 0x3e, 0x00, 0x00, 0x00, 0x00, # ]
    0x04, 0x02, 0x04, 0x00, 0x00, 0x00, # ^
    0x20, 0x20, 0x20, 0x00, 0x00, 0x00, # _

#   Lowercase
    0x02, 0x04, 0x00, 0x00, 0x00, 0x00, # `
    0x3c, 0x12, 0x12, 0x12, 0x3e, 0x00, # a
    0x3c, 0x2a, 0x2a, 0x2e, 0x10, 0x00, # b
    0x38, 0x44, 0x44, 0x44, 0x28, 0x00, # c
    0x3c, 0x22, 0x22, 0x22, 0x1c, 0x00, # d
    0x3c, 0x2a, 0x2a, 0x2a, 0x00, 0x00, # e
    0x3c, 0x12, 0x12, 0x12, 0x00, 0x00, # f
    0x3c, 0x22, 0x22, 0x2a, 0x1a, 0x00, # g
    0x3e, 0x08, 0x08, 0x3e, 0x00, 0x00, # h
    0x22, 0x3e, 0x22, 0x00, 0x00, 0x00, # i
    0x30, 0x22, 0x22, 0x1e, 0x00, 0x00, # j
    0x3e, 0x08, 0x0c, 0x32, 0x00, 0x00, # k
    0x3e, 0x20, 0x20, 0x20, 0x00, 0x00, # l
    0x3c, 0x02, 0x3c, 0x02, 0x3e, 0x00, # m
    0x3c, 0x02, 0x02, 0x02, 0x3e, 0x00, # n
    0x1c, 0x22, 0x22, 0x22, 0x1e, 0x00, # o

    0x3c, 0x12, 0x12, 0x12, 0x0e, 0x00, # p
    0x1c, 0x22, 0x22, 0x62, 0x1e, 0x00, # q
    0x3c, 0x12, 0x12, 0x32, 0x0e, 0x00, # r
    0x48, 0x54, 0x54, 0x54, 0x24, 0x00, # s
    0x04, 0x04, 0x3f, 0x44, 0x24, 0x00, # t
    0x1e, 0x20, 0x20, 0x20, 0x1e, 0x00, # u
    0x0e, 0x10, 0x20, 0x10, 0x0e, 0x00, # v
    0x3e, 0x20, 0x1e, 0x20, 0x1e, 0x00, # w
    0x36, 0x08, 0x08, 0x36, 0x00, 0x00, # x
    0x26, 0x28, 0x28, 0x1e, 0x00, 0x00, # y
    0x32, 0x2a, 0x2a, 0x26, 0x00, 0x00, # z
    0x08, 0x3e, 0x22, 0x00, 0x00, 0x00, # {
    0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, # |
    0x22, 0x3e, 0x08, 0x00, 0x00, 0x00, # }
    0x04, 0x02, 0x02, 0x00, 0x00, 0x00, # ~
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,

#   Extra
    0x3c, 0x12, 0x3c, 0x2a, 0x2a, 0x00, # Æ
    0x3f, 0x12, 0x12, 0x12, 0x0e, 0x00, # Þ
    0x3e, 0x0a, 0x2a, 0x34, 0x00, 0x00, # ß
    0x3c, 0x12, 0x3c, 0x2a, 0x2a, 0x00, # æ
    0x3f, 0x12, 0x12, 0x12, 0x0e, 0x00, # þ
    0x08, 0x3c, 0x2a, 0x2a, 0x00, 0x00, # £
    0x26, 0x28, 0x28, 0x1e, 0x00, 0x00, # ¥s
    0x1c, 0x22, 0x22, 0x22, 0x00, 0x00, # ©
    0x02, 0x05, 0x02, 0x00, 0x00, 0x00, # °

#   Accents + Offsets
#   All chars are shifted 8px down into a 32 pixel canvas for combining with accents.
#   Accent shift values (the first two numbers in each line below) move the accent down to meet them.
#   These are the shift values for lower and UPPER case letters respectively.
    6,6,   0x00, 0x00, 0x01, 0x02, 0x00, 0x00, # Grave
    6,6,   0x00, 0x00, 0x02, 0x01, 0x00, 0x00, # Acute
    6,6,   0x00, 0x02, 0x01, 0x02, 0x00, 0x00, # Circumflex
    6,6,   0x00, 0x01, 0x02, 0x01, 0x02, 0x00, # Tilde
    6,6,   0x00, 0x01, 0x00, 0x01, 0x00, 0x00, # Diaresis
    6,6,   0x00, 0x02, 0x05, 0x02, 0x00, 0x00, # Ring Above
    6,6,   0x00, 0x40, 0x20, 0x10, 0x00, 0x00, # Stroke
    10,10, 0x00, 0x00, 0x28, 0x10, 0x00, 0x00  # Cedilla
])
