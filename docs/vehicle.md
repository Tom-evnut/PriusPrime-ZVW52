# Vehicle: Toyota Prius Prime / Prius PHV (ZVW52), 2017-2022

Second-generation Toyota plug-in Prius. Sold as **Prius Prime** (North America) and **Prius PHV / Prius Plug-in Hybrid** (Japan, Europe). Built on the TNGA-C platform alongside the 4th-gen Prius (ZVW50/51).

## Plug-in Prius generations (to avoid mix-ups)

| Generation | Years | Code | Pack (series cells) | Nominal | Capacity | OBC |
|---|---|---|---|---|---|---|
| Gen 1 Prius Plug-in / PHV | 2012-16 | ZVW35 | 56S | ~207 V | 4.4 kWh, 21.5 Ah | ? |
| **Gen 2 Prius Prime / PHV** | **2017-22** | **ZVW52** | **95S (5 stacks x 19)** | **351.5 V** | **8.8 kWh, 25 Ah** | **3.3 kW** |
| Gen 3 Prius Prime / PHEV | 2023+ | MXWH61 | 72S | ~266 V | 13.6 kWh, 51 Ah | 3.5 kW |
| (RAV4 Prime / NX450h+, for comparison) | 2021+ | AXAP54 | 96S | 355.2 V | 18.1 kWh, 51 Ah | 3.3 / 6.6 kW |

Cell count is confirmed in the field: OBDb's cell-voltage request (`747 / 22 182E`) returns 95 cells on a 2020 Prime and 72 on 2023/2025 cars.

## HV battery

- Li-ion, 3.7 V nominal cells, 95 in series, 25 Ah, air cooled, under the rear cargo floor.
- Battery heater fitted (OBDb exposes battery heater temperatures).
- Sources: [Argonne D3 2017 Prius Prime](https://www.anl.gov/taps/d3-2017-toyota-prius-prime), [TFLcar](https://tflcar.com/2016/10/embargo-the-2017-toyota-prius-prime-is-a-plug-in-hybrid-with-impressive-numbers-video/), [PriusChat - pack configuration](https://www.priuschat.com/goto/post?id=2708082).

## Charging system

- J1772 inlet, **3.3 kW** onboard charger ("battery charger assembly"). About 5.5 h from 120 V, about 2 h on Level 2.
- **Plug-in charge control ECU** controls the charger, handles the EVSE pilot/proximity, drives the charge indicator, and talks to the hybrid vehicle control ECU (power management ECU) over CAN.
- Toyota's terminal lists (earlier PHV generation) show the plug-in charge control ECU with several CAN pairs (CA1/CA4/CA5) **plus a separate CAN pair on the charger connector**. That private ECU-to-charger link is the main thing to capture for standalone charger use. Not yet confirmed for ZVW52. See [mytoyo - Plug-in Charge Control System](https://www.mytoyo.com/plug_in_charge_control_system_for_phev_model_-2489.html) and [Automotive Tech Info](https://automotivetechinfo.com/2023/02/on-the-juice-a-toyota-prius-performance-enhancement-to-beat-the-competition/).
- A separate **charge contactor** exists. OBDb exposes its solenoid current from `7B0 / 21 A3` (`PRIUSPRIME_SCC_SOLENOID_CURRENT`).
- JDM/EU cars have an optional **solar roof** charging system.
- Part numbers: TODO. G9060-47130 is the portable **EVSE cable**, not the OBC.

## ECUs of interest

| ECU | Role | Known diag address |
|---|---|---|
| Hybrid vehicle control ECU (power management) | THS master, talks to battery ECU, MG ECU, plug-in ECU | `7D2 -> 7DA` (per OBDb) |
| Battery ECU | Pack voltage/current/cells/temps, SOC | `747 -> 74F` (per OBDb) |
| Plug-in charge control ECU | Charger master, EVSE comms | unknown |
| Battery charger assembly (OBC) | 3.3 kW AC-DC | unknown |
| MG ECU (in inverter w/ converter) | Motor/generator control, DC-DC | unknown (DC-DC values are read via `7D2`) |
| Central gateway (CGW) | Forwards selected frames to the camera/ADAS bus | - |

## Security / SecOC

opendbc puts the 2017-22 Prius/Prime on the normal Toyota platform config, not `ToyotaSecOCPlatformConfig` (which is used for RAV4 Prime 2021+ and later cars). So message authentication should not get in the way of sniffing or injecting on this car.
