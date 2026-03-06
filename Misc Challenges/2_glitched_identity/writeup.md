# Glitched Identity - Writeup

## Challenge Description
Players are given a `glitched_qr.png` file and a `note.txt`. The note plainly reminds players about "error correction" which implies that the QR code doesn't need to be perfectly pristine to be scanned.

## Solution Steps
1. The provided QR code is missing some data blocks (randomly replaced by black and white rectangles). 
2. However, QR codes use robust Reed-Solomon error correction. This particular QR code was generated with high error correction levels.
3. Because key areas (the three large position markers in the corners) remain intact, the player simply needs to scan the QR code using any physical smartphone camera or an online QR code reader (such as ZXing).
4. The reader's built-in error correction algorithms will mathematically restore the missing segments, easily extracting the hidden flag from the image.

## Flag
`flag{qr_codes_never_lie}`
