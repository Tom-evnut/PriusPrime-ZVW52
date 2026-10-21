# Onboard charger (OBC)

Toyota calls it the **"Charger Assy, Electric Vehicle"** (later revisions: "Charger Sub-Assy, Electric Vehicle"), Toyota parts group **G9090B**. US dealer catalogues also list it as "Battery Charger, Control Module". 3.3 kW, AC only. It has a separate **charger cooling blower** and duct.

## Part numbers

### Service part numbers (G9099-xxxxx)

| Part number | Market | Years (catalogue fitment) | Name | Source |
|---|---|---|---|---|
| G9099-47040 | US Prime | 2017-2019 | Charger Assy, Electric Vehicle | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47040.html) |
| G9099-47050 | US Prime | 2017-2019 | Charger Assy, Electric Vehicle. One dealer site labels it "without Smart Charge". | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47050.html), [Sparks Parts](https://www.sparksparts.com/oem-parts/toyota-2017-2018-toyota-prius-prime-control-module-g909947050) |
| G9099-47041 | US Prime | 2018-2020 | Charger Sub-Assembly, El | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47041.html) |
| G9099-47051 | US Prime | 2018-2020 | Charger Sub-Assembly, El | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47051.html), [Sparks Parts](https://www.sparksparts.com/oem-parts/toyota-2019-toyota-prius-prime-control-module-g909947051) |
| G9099-47090 | US Prime | 2019-2021 | Charger Sub-Assembly, El | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47090.html) |
| G9099-47091 | US Prime | 2020-2022 | Charger Sub-Assembly, El ("without Smart Charge") | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47091.html) |
| G9099-47092 | US Prime | 2021-2022 | Charger Sub-Assy, El ("without Smart Charge") | [toyotapartsdeal](https://www.toyotapartsdeal.com/oem/toyota~charger~assy~electric~g9099-47092.html), [Sparks Parts](https://www.sparksparts.com/oem-parts/toyota-2022-toyota-prius-prime-control-module-g909947092) |
| G9099-47020 | JDM PHV (ZVW52-AHXHB) | 2016/09-2018/12 | CHARGER ASSY, ELECTRIC VEHICLE | [jp-carparts fig 8442](https://jp-carparts.com/toyota/partlist.php?maker=toyota&type=224130&cartype=3&fig=8442) |
| G9099-47021 | JDM PHV (ZVW52-AHXHB) | 2018/12-2019/04 | CHARGER ASSY, ELECTRIC VEHICLE | same |
| G9099-47030 | JDM PHV | ? | EV charger assembly. Amayama lists 47020, 47030 and 47040 for ZVW52; variant notes not checked because the site is behind a bot check. | [Amayama](https://www.amayama.com/en/catalogs/toyota/prius-phv/4-hatchback-right-zvw52-2017-3348/electrics-4/ev-charger-dc-dc-converter-366) |

"-4704x" and "-4705x" are parallel variants and "-4709x" is the later revision. I don't know what separates the 4704x and 4705x families. "Smart Charge" may be the connected-services / charge-schedule option. Check against the VIN with a dealer.

### Other numbers seen on used units

- **Label numbers on the unit** (eBay): G9090-47030, G9090-47031, G9090-47053. These appear to be the number printed on the case rather than the service number. Example: [eBay "DC Converter Inverter Charger G909047030"](https://www.ebay.com/itm/127810200959).
- **Hollander interchange: 660-10018.** Use this on salvage-yard search sites (e.g. car-part.com) to find used units.

### Related parts (JDM fig 8442, 2016/09-2019/04)

| Part number | Name |
|---|---|
| 821H5-47030 | WIRE, HV BATTERY CHARGER (charger HV/LV harness) |
| G9081-47040 / G9081-47050 | CABLE, AC CHARGER INLET (G9081-47040 also sold for US Prime) |
| G9082-47010 | CABLE, DC CHARGER INLET (JDM CHAdeMO-equipped cars) |
| G926V-47010 | BLOWER, CHARGER COOLING |
| G926Q-47010 | DUCT, EV CHARGER |
| G3840-47040 | RELAY ASSY, ELECTRIC VEHICLE |
| G90F0-47090 | LOCK ASSY, CABLE EV CHARGER (inlet lock actuator) |
| G90H0-47010 | INDICATOR ASSY, EV CHARGER LID |
| 89100-47010 | COMPUTER ASSY, NETWORK GATEWAY (FOR DC POWER SUPPLY) |
| 89981-47xxx | COMPUTER, HYBRID VEHICLE CONTROL (fig 8433, several variants, split by "AC charging only" vs DC-capable) |

## Where the charge control logic lives

- On the **2023+ Prime (XW60)**, the repair manual shows a separate **plug-in charge control ECU assembly** and an **electric vehicle charger assembly** that contains its own "charge control ECU" plus the "voltage inverter assembly". The plug-in ECU's connector R62 has E1 ground, PISW (proximity), CPLT (control pilot) and four CAN lines on pins 11-14. Its DTC list includes *U01BB87 Lost communication with battery charger control module "B"* and *P1CE996 Charger cooling fan revolution sensor*. Source: [mytoyo (XW60 manual)](https://www.mytoyo.com/plug_in_charge_control_system_for_phev_model_-2489.html). **This is the wrong generation**, but it shows the likely architecture: the OBC is its own CAN node.
- On the **ZVW52**, the JDM parts catalogue lists **no separate plug-in charge control ECU**, only the hybrid vehicle control computers (fig 8433) and the charger assembly. The US catalogue's alternate name for the charger is "Battery Charger, Control Module". So on this generation the pilot/proximity handling and charge control are probably inside the charger assembly, the hybrid ECU, or split between them. **Unconfirmed.**

## Connector pinout

**No public pinout found** (searched PriusChat, openinverter, eBay listings, parts catalogues, leaked-manual sites, 2026-10-21). In 2018 a PriusChat member reported that TIS showed no EWD for the Prime. The repair manual's *Terminals of ECU* tables are the place to look.

To get it:
1. **Toyota TIS** ([techinfo.toyota.com](https://techinfo.toyota.com)) sells short-term subscriptions. Look in the 2017-2022 Prius Prime repair manual for *Hybrid / Battery Control > Plug-in Charge Control System > Terminals of ECU*, *Electric Vehicle Charger Assembly > Removal*, and the EWD *Plug-in charge control* / *Power source* system circuits and connector list.
2. **Haynes online**, Toyota Prius / Prius Prime (ZVW50/52/55) 2015-2022: [uk.haynes.com](https://uk.haynes.com/products/toyota-prius-prime-zvw50-zvw52-zvw55-from-2015-to-2022). Paid. Wiring coverage "where available".
3. **Bench**: get a used unit (Hollander 660-10018) with as much harness (821H5-47030) as possible. Then ring out the LV connector: 12 V/ground by diode-checking to the case, CAN pairs by about 60 Ω differential to each other with the internal termination, IGCT/wake lines by powering up with 12 V and watching for traffic.

### Expected signals on the charger LV connector (to confirm)

Based on the XW60 terminal list and the Gen 1 PHV charger description ([Automotive Tech Info](https://automotivetechinfo.com/2023/02/on-the-juice-a-toyota-prius-performance-enhancement-to-beat-the-competition/)), expect some of these:

- +B (12 V permanent), IG / wake, GND
- CAN H/L, possibly two pairs (vehicle side + private link)
- CPLT (control pilot) and PISW / PP (proximity), if the charger does the EVSE handling itself
- Cooling blower drive and speed sense (DTC P1CE996 on XW60)
- Charge port lock motor and lock position, charge indicator LED (could instead sit on another ECU)
- On the Gen 1 PHV, the charger had an ILMT (current-limit) signal and an AC input voltage sense

## J1772 inlet

The vehicle inlet is standard SAE J1772 (L1, N, PE, CP, PP), so its pinout follows the standard.
