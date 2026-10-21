#!/usr/bin/env python3
"""
Pull Prius / Prius Prime CAN logs out of comma's public commaCarSegments dataset
and summarise them.

  index      list every segment for the Prius platforms -> data/comma_segments_index.csv
  download   fetch N rlog.zst files                     -> Logs/comma/<dongle>/<route>/<seg>/rlog.zst
  inventory  decode downloaded rlogs: VIN per segment, and every CAN ID seen per bus
             with rate / DLC / whether a reference DBC already names it
  export     convert one rlog to a SavvyCAN (GVRET) CSV, optionally filtered by bus / ID

Dependencies:  pip install zstandard pycapnp
The openpilot cereal schema is fetched once into tools/.cache/cereal.

Dataset: https://huggingface.co/datasets/commaai/commaCarSegments (MIT)
"""
import argparse
import csv
import io
import json
import os
import random
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HF = "https://huggingface.co/datasets/commaai/commaCarSegments"
OP_RAW = "https://raw.githubusercontent.com/commaai/openpilot/master/openpilot/cereal/"
DBC_RAW = "https://raw.githubusercontent.com/commaai/opendbc/master/opendbc/car/"
# (local path, source url) -- log.capnp imports "/car.capnp" and "/include/c++.capnp" from the import root
CEREAL_FILES = [
  ("log.capnp", OP_RAW + "log.capnp"),
  ("custom.capnp", OP_RAW + "custom.capnp"),
  ("deprecated.capnp", OP_RAW + "deprecated.capnp"),
  ("car.capnp", DBC_RAW + "car.capnp"),
  ("include/c++.capnp", OP_RAW + "include/c++.capnp"),
]
CACHE = REPO / "tools" / ".cache"

# Gen 2 plug-in (ZVW52, 2017-22) lives under these opendbc platforms, mixed in with the regular Prius
PLATFORMS = ["TOYOTA_PRIUS", "TOYOTA PRIUS 2017", "TOYOTA_PRIUS_TSS2", "TOYOTA PRIUS TSS2 2021"]

# VIN chars 4-8 (WMI excluded). Prime = "KARFP", regular Prius = "KARFU"/"KBRFU"/"KDRFU" etc.
PRIME_VDS = ("KARFP",)

DBCS = [
  REPO / "DBC" / "ZVW52_HV.dbc",
  REPO / "third_party" / "opendbc" / "toyota_nodsu_pt_generated.dbc",
  REPO / "third_party" / "opendbc" / "toyota_2017_ref_pt.dbc",
  REPO / "third_party" / "opendbc" / "toyota_adas.dbc",
]


def fetch(url):
  req = urllib.request.Request(url, headers={"User-Agent": "PriusPrime-ZVW52"})
  with urllib.request.urlopen(req, timeout=120) as r:
    return r.read()


def load_database():
  db = json.loads(fetch(f"{HF}/resolve/main/database.json"))
  # entries look like "<dongle>/<route>/<seg>/s" -- drop the selector
  return {p: [s[:-2] if s.endswith("/s") else s for s in db[p]] for p in PLATFORMS if p in db}


def cmd_index(args):
  db = load_database()
  out = REPO / "data" / "comma_segments_index.csv"
  with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["platform", "dongle_id", "route", "segment"])
    for p, segs in db.items():
      for s in segs:
        dongle, route, seg = s.split("/")
        w.writerow([p, dongle, route, seg])
  for p, segs in db.items():
    print(f"{p:28s} {len(segs):6d} segments  {len({s.split('/')[0] for s in segs}):4d} devices")
  print(f"wrote {out.relative_to(REPO)}")


def cmd_download(args):
  db = load_database()
  segs = db.get(args.platform, [])
  if not segs:
    sys.exit(f"no segments for {args.platform}; choose from {list(db)}")
  rng = random.Random(args.seed)
  if args.one_per_device:
    by_dev = defaultdict(list)
    for s in segs:
      by_dev[s.split("/")[0]].append(s)
    segs = [rng.choice(v) for v in by_dev.values()]
  rng.shuffle(segs)
  for s in segs[:args.count]:
    dst = REPO / "Logs" / "comma" / s / "rlog.zst"
    if dst.exists():
      continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    print("downloading", s)
    try:
      dst.write_bytes(fetch(f"{HF}/resolve/main/segments/{s}/rlog.zst"))
    except Exception as e:  # some segments in the manifest are not uploaded yet
      print("  failed:", e)


def load_schema():
  import capnp
  capnp.remove_import_hook()
  d = CACHE / "cereal"
  for f, url in CEREAL_FILES:
    p = d / f
    if not p.exists():
      p.parent.mkdir(parents=True, exist_ok=True)
      p.write_bytes(fetch(url))
  return capnp.load(str(d / "log.capnp"), imports=[str(d)])


def read_events(log, path):
  import zstandard
  raw = zstandard.ZstdDecompressor().stream_reader(open(path, "rb")).read()
  return log.Event.read_multiple_bytes(raw, traversal_limit_in_words=2**64 - 1, nesting_limit=64)


def dbc_names():
  # plain BO_ scan: cantools rejects toyota_2017_ref_pt.dbc (non-standard 30-bit ids for gateway pseudo-frames)
  names = {}
  for p in DBCS:
    if not p.exists():
      continue
    for m in re.finditer(r"^BO_ (\d+) (\w+)", p.read_text(encoding="utf-8", errors="replace"), re.M):
      names.setdefault(int(m.group(1)), f"{m.group(2)} ({p.stem})")
  return names


def vin_from_can(parts):
  # VIN_PART_1 (0x580): bytes 0-2 = VIN 1-3, VIN_PART_2 (0x581): 8 bytes, VIN_PART_3 (0x582): 6 bytes
  if not all(k in parts for k in (0x580, 0x581, 0x582)):
    return ""
  b = parts[0x580][:3] + parts[0x581][:8] + parts[0x582][:6]
  try:
    return b.decode("ascii")
  except UnicodeDecodeError:
    return ""


def cmd_inventory(args):
  log = load_schema()
  names = dbc_names()
  rlogs = sorted((REPO / "Logs" / "comma").rglob("rlog.zst"))
  if not rlogs:
    sys.exit("no rlogs under Logs/comma -- run download first")

  stats = defaultdict(lambda: {"n": 0, "dlc": set(), "segs": set(), "prime_segs": set()})
  seg_rows = []
  for path in rlogs:
    seg = "/".join(path.relative_to(REPO / "Logs" / "comma").parts[:3])
    vin_parts, t0, t1, vin_param = {}, None, None, ""
    seen = defaultdict(lambda: {"n": 0, "dlc": set()})
    try:
      for ev in read_events(log, path):
        w = ev.which()
        if w == "can":
          t = ev.logMonoTime
          t0 = t if t0 is None else t0
          t1 = t
          for c in ev.can:
            if c.src >= 128:  # panda echoes of sent messages
              continue
            s = seen[(c.src, c.address)]
            s["n"] += 1
            s["dlc"].add(len(c.dat))
            if c.src == 0 and c.address in (0x580, 0x581, 0x582):
              vin_parts[c.address] = bytes(c.dat)
        elif w == "carParams" and not vin_param:
          vin_param = ev.carParams.carVin
    except Exception as e:
      print(f"{seg}: read error {e}", file=sys.stderr)
      continue
    vin = vin_param if vin_param and vin_param != "0" * 17 else vin_from_can(vin_parts)
    # comma blanks VINs for some users ("00000000000XXXXXX"); treat those as unknown
    prime = vin[3:8] in PRIME_VDS if len(vin) == 17 and vin[:3].isalpha() else None
    dur = (t1 - t0) / 1e9 if t0 and t1 else 0
    seg_rows.append([seg, vin, {True: "prime", False: "prius", None: "unknown"}[prime], f"{dur:.1f}", len(seen)])
    for k, v in seen.items():
      st = stats[k]
      st["n"] += v["n"]
      st["dlc"] |= v["dlc"]
      st.setdefault("dur", 0.0)
      st["dur"] += dur
      st["segs"].add(seg)
      if prime:
        st["prime_segs"].add(seg)
    print(f"{seg}  vin={vin or '?':17s}  {seg_rows[-1][2]:7s}  ids={len(seen)}")

  out_dir = REPO / "data"
  with open(out_dir / "comma_segment_vins.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["segment", "vin", "variant", "duration_s", "can_ids"])
    w.writerows(seg_rows)

  n_prime = sum(r[2] == "prime" for r in seg_rows)
  with open(out_dir / "can_id_inventory.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bus", "id_hex", "id_dec", "hz", "dlc", "segments", "prime_segments", "dbc_name"])
    for (bus, addr), st in sorted(stats.items()):
      hz = st["n"] / st["dur"] if st["dur"] else 0
      w.writerow([bus, f"0x{addr:03X}", addr, f"{hz:.2f}", "/".join(map(str, sorted(st["dlc"]))),
                  len(st["segs"]), len(st["prime_segs"]), names.get(addr, "")])
  print(f"\n{len(seg_rows)} segments ({n_prime} Prime), {len(stats)} bus/ID pairs")
  print("wrote data/comma_segment_vins.csv and data/can_id_inventory.csv")


def cmd_export(args):
  log = load_schema()
  src = Path(args.rlog)
  ids = {int(x, 16) for x in args.ids.split(",")} if args.ids else None
  out = Path(args.out) if args.out else src.with_name("savvycan.csv")
  n, t0 = 0, None
  with open(out, "w", newline="") as f:
    f.write("Time Stamp,ID,Extended,Dir,Bus,LEN,D1,D2,D3,D4,D5,D6,D7,D8\n")
    for ev in read_events(log, src):
      if ev.which() != "can":
        continue
      t0 = ev.logMonoTime if t0 is None else t0
      ts = (ev.logMonoTime - t0) // 1000
      for c in ev.can:
        if c.src >= 128 or (args.bus is not None and c.src != args.bus) or (ids and c.address not in ids):
          continue
        d = bytes(c.dat)
        f.write(f"{ts},{c.address:08X},{'true' if c.address > 0x7FF else 'false'},Rx,{c.src},{len(d)},"
                + ",".join(f"{b:02X}" for b in d) + "," * (8 - len(d)) + "\n")
        n += 1
  print(f"wrote {n} frames to {out}")


def main():
  ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  sub = ap.add_subparsers(dest="cmd", required=True)
  sub.add_parser("index")
  d = sub.add_parser("download")
  d.add_argument("--platform", default="TOYOTA_PRIUS")
  d.add_argument("--count", type=int, default=20)
  d.add_argument("--one-per-device", action="store_true", help="spread the sample across different cars")
  d.add_argument("--seed", type=int, default=0)
  sub.add_parser("inventory")
  e = sub.add_parser("export")
  e.add_argument("rlog")
  e.add_argument("--bus", type=int)
  e.add_argument("--ids", help="comma separated hex ids, e.g. 338,48C")
  e.add_argument("--out")
  args = ap.parse_args()
  {"index": cmd_index, "download": cmd_download, "inventory": cmd_inventory, "export": cmd_export}[args.cmd](args)


if __name__ == "__main__":
  main()
