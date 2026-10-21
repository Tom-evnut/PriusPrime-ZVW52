# Sources and existing work

## DBCs / CAN definitions

- [commaai/opendbc](https://github.com/commaai/opendbc) (MIT). The 2017-20 Prime is the `TOYOTA_PRIUS` platform and the 2021-22 is `TOYOTA_PRIUS_TSS2`. Both use `toyota_nodsu_pt_generated` (+ `toyota_adas` radar). Copies are in [`third_party/opendbc`](../third_party/opendbc).
  - `toyota_nodsu_pt_generated.dbc`: driving, ADAS and body. Hybrid content is limited to `GAS_PEDAL_HYBRID` 0x245, `GEAR_PACKET_HYBRID` 0x127, `ENGINE_RPM` 0x1C4.
  - `toyota_2017_ref_pt.dbc`: Toyota-internal message names for gateway-forwarded frames. See [can-findings.md](can-findings.md) for how useful it is.
  - `toyota_prius_2010_pt.dbc`: Gen 3 Prius, not included.
- No public DBC for the ZVW52 hybrid / HV / charger buses was found (GitHub, PriusChat, openinverter) as of 2026-10-21.

## Logs

- [commaCarSegments](https://huggingface.co/datasets/commaai/commaCarSegments) (MIT): 1-minute rlogs from openpilot users. `TOYOTA_PRIUS` 8,310 segments / 244 devices, `TOYOTA_PRIUS_TSS2` 3,939 / 103, plus a few under legacy names. Index: [`data/comma_segments_index.csv`](../data/comma_segments_index.csv). Roughly half the sampled `TOYOTA_PRIUS` cars are Primes.
- Public openpilot test routes (viewable in cabana): `d2525c22173da58b/2021-04-25--16-47-04` (TOYOTA_PRIUS), `0a0de17a1e6a2d15/2020-09-21--21-24-41` (TOYOTA_PRIUS_TSS2).
- [4TU dataset - Toyota Prius architecture reverse engineering](https://data.4tu.nl/export/cff/datasets/4df14b88-a779-4b3b-a2d8-176be4e75cb1) (CC BY-NC 4.0). Prius generation not confirmed.

## Diagnostics

- [OBDb/Toyota-Prius-Prime](https://github.com/OBDb/Toyota-Prius-Prime) (CC BY-SA 4.0): UDS PIDs with test responses from 2017/2020-2026 cars. Rendered for ZVW52 in [diagnostic-pids.md](diagnostic-pids.md).
- [PriusChat - Gen IV Prius Prime custom PIDs for Torque](https://priuschat.com/goto/post?id=2496485)
- [Hybrid Assistant trip report from a 2017 Prime](https://attachments.priuschat.com/attachment-files/2018/01/138055_Hybrid_Assistant_Report_.pdf)

## Charger / plug-in system

- [mytoyo - Plug-in Charge Control System (PHEV)](https://www.mytoyo.com/plug_in_charge_control_system_for_phev_model_-2489.html): ECU terminals including CAN pairs and a charger-connector CAN pair.
- [Automotive Tech Info - Prius plug-in charging](https://automotivetechinfo.com/2023/02/on-the-juice-a-toyota-prius-performance-enhancement-to-beat-the-competition/): plug-in charge control ECU role, ILMT / input voltage signals (Gen 1 PHV).
- [PriusChat - 3.3 kW to 6.6 kW upgrade](https://priuschat.com/threads/can-3-3kw-charger-be-upgraded-to-6-6kw-on-prius-prime-or-rav4-prime.219516/)
- [PriusChat - Prime EVSE G9060-47130](https://priuschat.com/goto/post?id=2659975)
- [go-parts - 2023+ Prime charge port TSB T-SB-0054-24](https://www.go-parts.com/garage/drive-motor-battery-pack-charging-port-connector-toyota-prius-prime-2023-2025) (Gen 3, plug-in ECU not sleeping)

## Parts catalogues

- [jp-carparts - ZVW52-AHXHB fig 8442 DC/DC converter & charger](https://jp-carparts.com/toyota/partlist.php?maker=toyota&type=224130&cartype=3&fig=8442) (JDM, includes fig 8433 HEV control computer)
- [Amayama - ZVW52 EV charger & DC/DC converter](https://www.amayama.com/en/catalogs/toyota/prius-phv/4-hatchback-right-zvw52-2017-3348/electrics-4/ev-charger-dc-dc-converter-366) (bot check)
- [toyotapartsdeal - G9099-47050](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47050.html) and sibling pages for -47040/-47041/-47051/-47090/-47091/-47092
- [mytoyo - 2023+ (XW60) plug-in charge control system](https://www.mytoyo.com/plug_in_charge_control_system_for_phev_model_-2489.html): wrong generation, but has terminal tables and DTC list
- [Toyota TIS](https://techinfo.toyota.com) (paid, short-term subscriptions) and [Haynes online ZVW50/52/55](https://uk.haynes.com/products/toyota-prius-prime-zvw50-zvw52-zvw55-from-2015-to-2022)

## Related projects

- [nelsonblaha/prius-bridge](https://github.com/nelsonblaha/prius-bridge): comma 3X + Toyota cloud to Home Assistant on a 2022 Prime. Gets charge status from the cloud, not CAN.
- [HylkeJellema/prius-PHV-fingerprint](https://github.com/HylkeJellema/prius-PHV-fingerprint): 2019 EU PHV CAN fingerprint.
- [hmnvdk/ZVW52-680A-HMI](https://github.com/hmnvdk/ZVW52-680A-HMI): placeholder, no content yet.
- [optskug/docs](https://github.com/optskug/docs): Toyota SecOC history (later platforms).
- openinverter forum: Prius Gen 2/3 inverter work, nothing on the Gen 4 / Prime transaxle or the Prime OBC yet.

## Vehicle specs

- [Argonne D3 - 2017 Prius Prime](https://www.anl.gov/taps/d3-2017-toyota-prius-prime)
- [TFLcar - 2017 Prius Prime](https://tflcar.com/2016/10/embargo-the-2017-toyota-prius-prime-is-a-plug-in-hybrid-with-impressive-numbers-video/)
- [PriusChat - Prime traction battery configuration](https://www.priuschat.com/goto/post?id=2708082)
- [Enel X - Prius Prime charging](https://evcharging.enelx.com/toyota-charging-stations/prius-prime)
