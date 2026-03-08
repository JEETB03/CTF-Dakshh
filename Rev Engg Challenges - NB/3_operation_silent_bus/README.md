# Challenge 3 — OPERATION: SILENT BUS

**Category:** Reverse Engineering / Automotive Systems  
**Difficulty:** Level 3  
**Points:** 800  

---

## Mission Briefing

**Directorate of Technical Intelligence**  
**Internal Transmission — Authorized Personnel Only**

An intercepted telemetry archive from a classified automotive test facility has been forwarded to our division for analysis.

The capture contains **raw Controller Area Network (CAN) traffic** recorded during what appears to be a **firmware programming session for a vehicle Electronic Control Unit (ECU)**.

Initial signals analysis indicates that the session follows a **standard automotive diagnostic workflow**, likely used during factory-level flashing or maintenance procedures.

However, analysts discovered irregularities within the transmission sequence.

Specifically:

- The diagnostic session appears **longer than expected**
- The firmware transfer sequence contains **non-standard payload characteristics**
- A pattern embedded within the update traffic suggests **deliberate data concealment**

Our working hypothesis is that someone used a legitimate ECU update procedure to **smuggle information inside the firmware being transmitted over the CAN bus**.

Your assignment is to recover that hidden message.

---

## Intelligence Package

The following artifact has been cleared for analysis:

```
can_dump.log
```

This file contains the **captured CAN bus frames** from the diagnostic session.

No additional context or tooling is provided.

Everything required to complete the mission exists within this dataset.

---

## Operational Objectives

You must:

1. Examine the CAN traffic
2. Identify the communication protocol used during the diagnostic session
3. Reconstruct the data transferred during the firmware programming process
4. Extract the concealed message hidden within the transferred data

Successful extraction will reveal the **flag**.

---

## Flag Format

```
DAKSHH{...}
```

---

## Technical Context

Modern vehicles rely on multiple Electronic Control Units communicating over the **Controller Area Network (CAN)**.

To update ECU firmware, manufacturers typically use **diagnostic protocols layered over CAN**, enabling engineers to:

- Initiate programming sessions  
- Unlock security access  
- Erase ECU memory  
- Transfer firmware blocks  
- Finalize installation  

Because CAN frames are limited in size, **large data transfers are segmented across multiple frames** using specialized transport protocols.

Understanding this communication pattern will be essential for reconstructing the transmitted data.

---

## Analyst Notes

During preliminary inspection of the capture, investigators observed:

- Structured multi-frame message patterns  
- Repeating block transmissions  
- Indicators of a firmware download routine  

These patterns strongly suggest the presence of a **structured firmware transfer sequence** embedded in the CAN traffic.

Hidden somewhere inside that transfer lies the information we need.

---

## Your Role

You are part of the **Advanced Systems Analysis Unit**.

Treat the capture as if it were collected during a real-world interception operation.

No assumptions.  
No shortcuts.

Break down the communication, reconstruct the transferred data, and uncover what was hidden inside.

---

**The signal is buried in the noise.**

Find it.
