# Logs

Own captures go here. Use SavvyCAN GVRET CSV, or candump `.log`.

Name files `YYYY-MM-DD_<where>_<what>.csv` and describe each one below:

- **where**: the tap point, e.g. `obd`, `camera`, `plg-ecu-CA4`, `obc-connector`, `batt-ecu`
- **what**: what the car was doing, e.g. `plugin-l1-full-charge`, `ready-ev-drive`, `obc-12v-only`

| File | Car (year/market) | Tap point | Bus speed | Conditions | Notes |
|---|---|---|---|---|---|
| | | | | | |

`comma/` holds rlogs downloaded with `tools/comma_segments.py download`. It is git-ignored because the files can be re-fetched. Convert one to SavvyCAN with:

```bash
python tools/comma_segments.py export Logs/comma/<dongle>/<route>/<seg>/rlog.zst --bus 0
```
