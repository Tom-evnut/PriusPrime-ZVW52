# CAN findings

## Where the comma logs come from

The comma harness taps the **windscreen camera connector**. Per the inventory below, the rlog buses for this platform are:

| rlog bus | What it is | Main DBC |
|---|---|---|
| 0 | Car side of the camera connector: frames the **central gateway forwards** (driving, body, some engine/hybrid summaries) | `toyota_nodsu_pt_generated` |
| 1 | Radar bus | `toyota_adas` |
| 2 | Camera side (LKA/HUD frames from the camera) | `toyota_nodsu_pt_generated` |

The internal hybrid buses (battery ECU, MG ECU, plug-in charge ECU, OBC) are **not** visible here, so they need to be captured directly.

## Inventory of 40 sampled segments (2026-10-21)

`tools/comma_segments.py download --platform TOYOTA_PRIUS --count 40 --one-per-device`, then `inventory`.
VINs decoded from CAN `VIN_PART_1..3` (0x580-0x582): **21 Prime** (`JTDKARFP...`), 14 regular Prius, 5 with blanked VINs.
Full table: [`data/can_id_inventory.csv`](../data/can_id_inventory.csv), per-segment VINs: [`data/comma_segment_vins.csv`](../data/comma_segment_vins.csv).

### How much does each DBC explain? (IDs present in >= 20 of 40 segments)

| Bus | Common IDs | Named in `toyota_nodsu_pt_generated` | Named only in `toyota_2017_ref_pt` | Unnamed |
|---|---|---|---|---|
| 0 | 90 | 40 | 23 | 27 |
| 1 | 71 | 10 (+29 in `toyota_adas`) | 6 | 26 |

**Is `toyota_2017_ref_pt.dbc` useful?** Yes, as a naming map, but not for the charger. On bus 0 it names 23 more IDs than the openpilot DBC. Because it uses Toyota's internal message names, it shows which ECU family each frame comes from (`ENG` engine/hybrid, `ECT` transmission, `VSC` brakes, `AVN` head unit, `MET` meter, `CGW` gateway). Its only hybrid-relevant signal on this bus is `ENG1F03.HVFLAG` (0x3F9). Nothing in it relates to charging.

Bus-0 IDs named only by the ref DBC: 0x232 VSC1S14, 0x366 DS11D71, 0x384/0x386/0x389/0x3A5/0x3E6-0x3E9/0x434/0x435 AVN1Sxx, 0x391 AFS1S01, 0x396 CSR1S01, 0x3B1 ABG1S01, 0x3BB ENG1S92, 0x3F9 ENG1F03, 0x423 STR1S02, 0x45A CGW1N02, 0x4CB ACC1N01, 0x4CC CSR1N01, 0x4D5 BSR1N01, 0x4FF FRD1N01.

Bus-0 IDs unnamed anywhere: 0x128 (61 Hz), 0x292, 0x2C9, 0x2E7 (31 Hz), 0x32A (21 Hz), 0x32E, 0x33D, 0x33E, 0x35F, 0x3B6, 0x3B9, 0x3CB, 0x3CE, 0x3CF, 0x3E1, 0x421, 0x42F, 0x43A, 0x43C, 0x43D, 0x43E, 0x46C, 0x497, 0x615, 0x624, 0x63B, 0x6F1.

### Prime-specific candidates (bus 0)

IDs that appear far more often on Prime segments than on others. The ~0.11 "other" share is probably Primes with blanked VINs.

| ID | Rate | On Prime segs | On other segs | Ref DBC name | Notes |
|---|---|---|---|---|---|
| 0x338 | 10 Hz | 81% | 11% | - | `00 00` while driving (2 or 8 bytes) |
| 0x3CE | 1 Hz | 100% | 11% | - | **Live data**: 127 distinct payloads across 21 cars. Byte 0 flags (0x40/0x80/0x04), byte 2 0xC0/0x00, bytes 4-5 a 16-bit value that varies between cars (e.g. 0x01B7, 0x0145, 0x00AF, 0x007C). Strong lead (EV range? charge schedule?) |
| 0x434 | 1 Hz | 100% | 16% | AVN1S20 | `41 40 00 00 01 80 00 00` / `5F 40 ...` |
| 0x391 | 1 Hz | 100% | 32% | AFS1S01 | constant `00 00 00 01 00 00 00 00` |
| 0x48C | 2 Hz | 81% | 11% | - | all zero while driving |
| 0x48D | 2 Hz | 81% | 11% | - | all zero while driving |
| 0x48E | 2 Hz | 81% | 11% | - | constant `.. .. 03 F0` |
| 0x48F | 2 Hz | 81% | 11% | - | all zero while driving |

The 0x48C-0x48F block is a set of four messages that are static while driving, which would fit a charge timer/schedule or a charging status that only changes when plugged in. This is unconfirmed. The next step is to capture these IDs at the camera connector while the car is plugged in.

## Earlier fingerprint

[HylkeJellema/prius-PHV-fingerprint](https://github.com/HylkeJellema/prius-PHV-fingerprint) (2019, EU Prius PHV): 94 IDs, all also in openpilot's Prius fingerprints. Copy in [`data/fingerprints/prius_phv_2019_eu.txt`](../data/fingerprints/prius_phv_2019_eu.txt). It contains three of the Prime candidates above (0x391 = 913, 0x3CE = 974, 0x434 = 1076) but not 0x338 or 0x48C-0x48F, which may be US-Prime-only or appear later than the fingerprint window. All 94 IDs are also in openpilot's Prius fingerprint list, probably merged in from this one.

## Older-generation hybrid CAN work (may not transfer)

- Gen 2 Prius 0x348 / 0x3C8 engine/EV requests - [PriusChat](https://priuschat.com/threads/decoding-can-messages-0x348-0x3c8-as-described-by-peef.110042/)
- Gen 3 passive messages (SOC, wheel speeds, throttle) - [PriusChat](https://priuschat.com/threads/passive-can-messages.116038/)
- Battery ECU SOC broadcast about every 100 ms, HV ECU uses last message received - [EAA-PHEV wiki](https://www.eaa-phev.org/wiki/Prius_PHEV_TechInfo)
- ETH Zurich semester project on Prius CAN - [PDF](https://attachments.priuschat.com/attachment-files/2017/04/122809_Communication_with_a_Toyota_Prius.pdf)
