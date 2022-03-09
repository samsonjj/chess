import sys

index64 = [
    0,  1, 48,  2, 57, 49, 28,  3,
   61, 58, 50, 42, 38, 29, 17,  4,
   62, 55, 59, 36, 53, 51, 43, 22,
   45, 39, 33, 30, 24, 18, 12,  5,
   63, 47, 56, 27, 60, 41, 37, 16,
   54, 35, 52, 21, 44, 32, 23, 11,
   46, 26, 40, 15, 34, 20, 31, 10,
   25, 14, 19,  9, 13,  8,  7,  6
];

from gmpy import scan1

def bitScanForward(bb):
    return scan1(bb)
   # debruijn64 = 0x03f79d71b4cb0a89
   # assert bb != 0
   # return index64[((bb & -bb) * debruijn64) >> 58]


print(bitScanForward(int(sys.argv[1])))
