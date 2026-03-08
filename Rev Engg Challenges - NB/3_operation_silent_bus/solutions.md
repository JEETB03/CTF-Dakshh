\# Challenge 3 — CAN Firmware Extraction



\## Solution Guide (For Organisers)



\### Challenge Overview



This challenge simulates an \*\*automotive ECU firmware flashing session over a CAN bus\*\*.



Players are provided with:



\* `can\_dump.log`

\* `README.md`



The goal is to analyze the CAN traffic, reconstruct the firmware being transferred, and recover the hidden flag.



The CAN traffic contains \*\*UDS (Unified Diagnostic Services)\*\* messages using \*\*ISO-TP segmentation\*\*.



---



\# 1. Inspect the CAN Dump



Players should begin by opening the log.



```bash

cat can\_dump.log

```



Example entries:



```

35899.960945 0x7b9 b'102a62f110444e38'

35899.960945 0x7b1 b'3008020000000000'

35899.960945 0x7b9 b'214120414441535f'

35899.97093125 0x7b9 b'2250524b20414e4c'

```



Structure:



```

timestamp   CAN\_ID   payload

```



Example:



```

35899.960945   0x7b9   b'102a62f110444e38'

```



| Field     | Meaning         |

| --------- | --------------- |

| timestamp | capture time    |

| CAN\_ID    | arbitration ID  |

| payload   | 8-byte CAN data |



---



\# 2. Identify the Protocol



Observing the first byte of the payload reveals values like:



```

10

21

22

23

30

```



These correspond to \*\*ISO-TP frame types\*\*.



ISO-TP (ISO 15765-2) allows transmitting messages larger than 8 bytes by splitting them across multiple CAN frames.



---



\# 3. Understand ISO-TP Frames



The \*\*first nibble\*\* determines the frame type.



| First Nibble | Frame Type        |

| ------------ | ----------------- |

| 0            | Single Frame      |

| 1            | First Frame       |

| 2            | Consecutive Frame |

| 3            | Flow Control      |



Example frame:



```

102a62f110444e38

```



Breakdown:



```

10 2a

```



Meaning:



\* `1` → First Frame

\* `0x2A` → Total payload length (42 bytes)



The remaining bytes contain the beginning of the payload.



---



\# 4. Reassemble ISO-TP Messages



Example sequence:



```

102a62f110444e38

214120414441535f

2250524b20414e4c

2320312e30302031

242e303120393939

2531302d4c303030

2630aaaaaaaaaaaa

```



Frame meanings:



| Frame | Meaning              |

| ----- | -------------------- |

| 10    | First frame          |

| 21    | Consecutive frame #1 |

| 22    | Consecutive frame #2 |

| 23    | Consecutive frame #3 |



The \*\*PCI bytes\*\* must be removed before concatenation.



Reconstructed payload:



```

62f110444e384120414441535f50524b20414e4c20312e303020312e30312039393931302d4c30303030

```



---



\# 5. Identify UDS Messages



UDS (Unified Diagnostic Services) is a common automotive diagnostic protocol.



The \*\*first byte of the payload is the Service ID (SID).\*\*



| SID  | Meaning                  |

| ---- | ------------------------ |

| 0x10 | DiagnosticSessionControl |

| 0x27 | SecurityAccess           |

| 0x31 | RoutineControl           |

| 0x34 | RequestDownload          |

| 0x36 | TransferData             |

| 0x37 | RequestTransferExit      |



Example:



```

36

```



This indicates a \*\*TransferData\*\* message.



---



\# 6. Detect the Firmware Flashing Sequence



The log contains a typical firmware programming sequence:



```

10 02          DiagnosticSessionControl (programming session)

27              SecurityAccess

31 FF00         Erase memory routine

34              RequestDownload

36              TransferData

36              TransferData

36              TransferData

...

37              RequestTransferExit

31 FF01         Check programming

11              ECU reset

```



The \*\*actual firmware bytes are transferred inside the `TransferData` messages.\*\*



---



\# 7. Extract Firmware Data



The structure of a TransferData message:



```

36 <block\_counter> <firmware\_bytes>

```



Example:



```

36 01 a1b2c3d4e5f6...

```



| Byte | Meaning       |

| ---- | ------------- |

| 36   | Service ID    |

| 01   | Block counter |

| rest | firmware data |



To reconstruct the firmware:



1\. Find all payloads beginning with `0x36`

2\. Remove the first two bytes

3\. Append the remaining bytes to a binary file



---



\# 8. Write an Extraction Script



Minimal extraction script:



```python

import re



firmware = bytearray()



with open("can\_dump.log") as f:

&nbsp;   for line in f:



&nbsp;       m = re.search(r"b'(\[0-9a-f]+)'", line)



&nbsp;       if not m:

&nbsp;           continue



&nbsp;       data = bytes.fromhex(m.group(1))



&nbsp;       if data\[0] == 0x36:

&nbsp;           firmware.extend(data\[2:])



with open("firmware.bin","wb") as f:

&nbsp;   f.write(firmware)

```



Run:



```bash

python extract.py

```



Output:



```

firmware.bin

```



---



\# 9. Analyze the Firmware



Check the file size:



```bash

ls -lh firmware.bin

```



Search for strings:



```bash

strings firmware.bin

```



Or:



```bash

strings firmware.bin | grep flag

```



---



\# 10. Recover the Flag



The firmware contains the flag embedded as a plaintext string.



Example output:



```

flag{uds\_firmware\_extracted\_from\_can\_bus}

```



---



\# Intended Skills Tested



\* CAN bus log analysis

\* ISO-TP protocol understanding

\* UDS firmware flashing workflow

\* Binary reconstruction

\* Firmware analysis



---



\# Common Mistakes Players May Make



| Mistake                       | Reason                                 |

| ----------------------------- | -------------------------------------- |

| Ignoring ISO-TP segmentation  | Multi-frame messages appear fragmented |

| Parsing Flow Control frames   | They do not contain useful data        |

| Extracting wrong UDS messages | Only `0x36` frames contain firmware    |

| Forgetting block counter byte | Causes corrupted firmware              |



---



\# Difficulty



\*\*Medium\*\*



Requires:



\* Basic automotive protocol knowledge

\* Python scripting

\* Binary analysis



---

