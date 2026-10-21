# PriusPrime-ZVW52

Collecting everything known about the CAN buses of the **2nd-gen Toyota plug-in Prius (Prius Prime / Prius PHV, ZVW52, 2017-22, 95S 351.5 V 8.8 kWh pack)**, with the goal of reverse engineering the **3.3 kW onboard charger** for use in EV conversion projects.

No public DBC exists for this car's hybrid or charging buses. The plan is to start from what openpilot/comma and OBDb have already mapped, then capture the internal buses directly.

## Layout

| Path | Contents |
|---|---|
| [`docs/vehicle.md`](docs/vehicle.md) | Specs, generations (Gen 1/2/3 pack and charger differences), charging system, ECUs |
| [`docs/can-findings.md`](docs/can-findings.md) | What's on the comma-visible bus, DBC coverage, **Prime-specific candidate IDs** |
| [`docs/diagnostic-pids.md`](docs/diagnostic-pids.md) | Polled UDS PIDs (95 cell voltages, SOC, pack V/I, DC-DC, charge contactor...), generated from OBDb |
| [`docs/sources.md`](docs/sources.md) | Links to every DBC, dataset, forum thread and related project found |
| [`DBC/ZVW52_HV.dbc`](DBC/ZVW52_HV.dbc) | Working DBC for the internal HV / plug-in / charger buses (empty, nodes only) |
| [`third_party/opendbc/`](third_party/opendbc) | opendbc reference DBCs for the camera-harness bus (MIT) |
| [`data/`](data) | commaCarSegments index, per-segment VIN/variant, CAN ID inventory, 2019 PHV fingerprint |
| [`Logs/`](Logs) | Own captures (see naming convention in `Logs/README.md`) |
| [`tools/`](tools) | `comma_segments.py` (index / download / inventory / export to SavvyCAN), `obdb_pids.py` |

## Quick start

```bash
pip install zstandard pycapnp
```

```bash
python tools/comma_segments.py download --platform TOYOTA_PRIUS --count 40 --one-per-device
```

```bash
python tools/comma_segments.py inventory
```

```bash
python tools/comma_segments.py export Logs/comma/<dongle>/<route>/<seg>/rlog.zst --bus 0
```

## Status / to do

- [x] Gather existing DBCs, datasets, PIDs and forum work
- [x] Separate Prime from regular Prius segments in commaCarSegments (by VIN on CAN 0x580-0x582)
- [x] First list of Prime-only broadcast IDs on the camera bus (0x338, 0x3CE, 0x48C-0x48F, ...)
- [ ] Capture at the camera connector while plugged in, to see if the Prime candidates change during charging
- [ ] Service manual / EWD: plug-in charge control ECU and OBC connector pinouts, which CAN pairs go where
- [ ] OBC part number(s), source a used OBC + plug-in charge control ECU
- [ ] Capture ECU <-> OBC CAN during a full charge session, while polling OBDb PIDs for reference values
- [ ] Bench test: replay plug-in ECU frames to run the OBC standalone

## Log

21/10/26 : Repo created. Collected opendbc DBCs, OBDb PIDs, commaCarSegments index (12,410 Prius-family segments). Sampled 40 segments (21 Prime by VIN) and found a group of Prime-specific IDs on the gateway bus. 0x3CE carries live per-car data.
