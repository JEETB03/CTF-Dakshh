# The Last Beacon - Writeup

## Challenge Description
Players are given an audio file `signal.wav` and a text file `transmission_note.txt`. The note plainly hints at "Short beep = dot, Long beep = dash", pointing directly to Morse code logic.

## Solution Steps
1. Listen to `signal.wav` and observe the distinct short and long beeps.
2. Use an audio visualization tool (like Audacity Spectrogram) or an online automatic Morse code audio decoder to translate the beeps. Another option is manually writing down dots and dashes and looking up a Morse alphabet chart.
3. The decoded audio spells out: `FLAG SATELLITE SIGNAL RESTORED`
4. Convert this to the standard flag format, which is lowercase words separated by underscores, as told by the transmission note.

## Flag
`flag{satellite_signal_restored}`
