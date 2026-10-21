# opendbc reference DBCs

Copied from [commaai/opendbc](https://github.com/commaai/opendbc) at commit `c3955753ae7258412814e2cdca3ee8af979e4679` (2026-10-21), MIT licence (see `LICENSE` in this folder).

| File | What |
|---|---|
| `toyota_nodsu_pt_generated.dbc` | Ready-to-use DBC for the camera-harness bus on the 2017-22 Prius / Prime. Built from the four `_*.dbc` + `toyota_nodsu_pt.dbc` sources below with the same concatenation as opendbc's `generator.py`. |
| `_toyota_2017.dbc`, `_toyota_adas_standard.dbc`, `_community.dbc`, `toyota_nodsu_pt.dbc` | Generator sources |
| `toyota_adas.dbc` | Radar bus |
| `toyota_2017_ref_pt.dbc` | Toyota-internal names for gateway-forwarded frames. Some IDs are non-standard 30-bit pseudo IDs, which cantools rejects. |

Don't edit these. New decodes go in `../../DBC/`.
