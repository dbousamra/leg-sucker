# Leg Sucker — MVP 1

## What we're ultimately trying to build

Some people have arteries in their legs so narrowed that not enough blood gets in. The tissue starves,
ulcers open up and won't heal, and in bad cases the leg is eventually amputated.

The usual way to help a poorly circulating leg is to squeeze it — compression stockings, inflatable
cuffs — which pushes blood back toward the heart. But you can't do that to these legs. Squeezing a
limb that's already short of arterial blood makes the inflow worse, and the skin is often too fragile
and ulcerated to touch at all.

So the idea is to move blood **without touching the leg**. Seal the whole limb inside a rigid chamber
and change the air pressure around it, timed to the heartbeat:

- **Suck (lower the pressure) as the heart beats** — the leg's arteries meet less resistance from
  outside, so blood should flow in more easily.
- **Push (raise it slightly) between beats** — helping blood and fluid drain back out, which should
  reduce swelling.

Think of it as a bellows around the leg, breathing in time with the pulse. Nothing ever contacts the
skin, which is the whole point — it should work on limbs that no compression device could safely go
near.

Whether that actually helps a patient is a long way off and completely unproven. This document is
about the first question underneath it all.

## Goal of this MVP

**Put a voice coil on a sealed PVC tube and see how much pressure it can make.**

No leg, no seal, no ECG, no human. Just: does this move pressure, and how much?

---

## On the actuator

Bare voice coil motors (the cylindrical AliExpress ones) have no piston and no seal — you'd have to
design and print both, plus a guide to stop the coil rubbing.

Guided voice coil actuators with a housing, shaft and internal bearings do exist — Moticont GVCM,
H2W NCM — but **none of them are sealed either**. They give you a shaft, not a pump. They're also
quote-only industrial parts, well outside this budget. Voice-coil-driven sealed pumps show up in
patents, not catalogues.

**A loudspeaker driver is the off-the-shelf version of exactly that assembly:** voice coil motor,
rigid piston (the cone), flexible gas seal at the rim (the surround), and a centring spring that
provides the linear guidance (the spider). For AU$40.

This is also how it's done in respiratory medicine — forced oscillation technique and impulse
oscillometry use a loudspeaker as a calibrated pressure source. Same job, smaller volume.

---

## Bill of materials

**Total ≈ AU$227** plus shipping, assuming you already have the Pi 4, a bench power supply, and the
3D printer.

| Item | What it's for | Where | Price |
|---|---|---|---:|
| **Jaycar CW2196** — 8" woofer, 8 Ω, Fs 28.1 Hz, Re 6.0 Ω, 90 W | **The actuator.** A speaker is a voice coil with the piston and gas seal already built in | [Jaycar CW2196](https://www.jaycar.com.au/woofer-speaker-driver-8-inch/p/CW2196) | $44.95 |
| **MPXV7002DP breakout** — ±2 kPa (±15 mmHg) differential, barbed ports | Measures chamber pressure against room air — the one number the whole rig exists to produce | [AliExpress](https://www.aliexpress.com/item/1005007057842984.html) | $20.19 |
| **ADS1115** — 16-bit I²C ADC | The Pi 4 has no analogue input; this converts the sensor's voltage for it | [AliExpress](https://www.aliexpress.com/item/1005012498259780.html) | $4.49 |
| **IBT-2 / BTS7960** — H-bridge motor driver | Drives the coil in both directions at frequencies an audio amp can't reach | [AliExpress](https://www.aliexpress.com/item/1005009194435701.html) | $17.29 |
| **Holman 100mm × 3m PVC DWV pipe** | The chamber. 85 mL per cm, so 800 mm ≈ 6.7 L | [Bunnings](https://www.bunnings.com.au/holman-100mm-x-3m-pvc-dwv-pipe_p4770345) | $33.65 |
| **Holman 100mm PVC DWV push-on cap** × 2 | Seals the far end; one gets drilled for the sensor port | [Bunnings](https://www.bunnings.com.au/search/products?q=Holman+100mm+PVC+DWV+Push+On+Cap) | $7.80 |
| **Holman 100mm DWV repair coupling** *(optional)* | Joins sections so you can vary chamber volume. Skip it if you'd rather change volume by putting sealed bottles inside | [Bunnings](https://www.bunnings.com.au/search/products?q=Holman+100mm+DWV+PVC+Repair+Coupling) | $17.94 |
| **Protek 250ml Type N PVC cement** | Glues pipe joints — solvent-welded joints don't leak | [Bunnings](https://www.bunnings.com.au/search/products?q=Protek+Type+N+PVC+Cement+Non+Pressure) | $8.42 |
| **Protek 125ml priming fluid** | Preps the PVC so the cement actually bonds | [Bunnings](https://www.bunnings.com.au/search/products?q=Protek+Red+Priming+Fluid) | $6.68 |
| **Neutral-cure silicone sealant** | Seals the sensor port and anything not solvent-welded | [Bunnings](https://www.bunnings.com.au/search/products?q=neutral+cure+silicone+sealant) | $12 |
| **Two-part epoxy** | Brushed over the printed adaptor — FDM prints leak through layer lines even when they look solid | [Bunnings](https://www.bunnings.com.au/search/products?q=two+part+epoxy+resin) | $20 |
| **Barbed fitting + silicone tube** | Connects the chamber to the pressure sensor | [Bunnings](https://www.bunnings.com.au/search/products?q=barbed+hose+fitting) | $10 |
| **M4 bolts + closed-cell foam gasket** | Bolts the driver to the printed adaptor, gasket makes it airtight | [Bunnings](https://www.bunnings.com.au/search/products?q=M4+bolts) | $15 |
| **60 mL syringe** | Injects a known volume for the leak test and to calibrate the sensor | [Bunnings](https://www.bunnings.com.au/search/products?q=60ml+syringe) | $5 |
| **2200 µF 35 V electrolytic capacitor** | Sits across the motor driver's supply. **Don't skip it** — see below | [Jaycar](https://www.jaycar.com.au/search?text=2200uF%2035V%20electrolytic) | $3 |
| **2 × 10 kΩ resistors** | Voltage divider so the 5 V sensor output can't damage the 3.3 V ADC | [Jaycar](https://www.jaycar.com.au/search?text=10k%20ohm%20resistor) | $1 |

Notes on a few of these:

- **The driver.** Jaycar publish the full Thiele-Small parameters (Fs 28.1 Hz, Qts 0.33, Vas 42 L,
  Re 6.0 Ω), which is why this one over the alternatives — you can predict its behaviour instead of
  guessing. They don't publish excursion, so this doc assumes ~220 cm² of cone and ±4 mm of travel,
  typical for an 8". Every number in the expected-pressure table scales linearly with those, so your
  first bench measurement effectively calibrates the whole rig.
- **Its recommended box is 42 L and you're using 7–15 L.** That's fine: at 6.7 L it becomes a
  Qtc 0.89 / Fc 76 Hz sealed alignment, which is an ordinary small sealed build. The paper cone will
  cope. But it does mean the air spring ends up roughly 6× stiffer than the driver's own suspension,
  and that stiffness is where the current demand below comes from.
- **3 m of pipe** is far more than the 800 mm you start with, deliberately: the spare lets you extend
  the chamber and watch the pressure fall off, which is the measurement that justifies scaling up.

### Power supply

**A 0–30 V / 0–5 A bench supply is ideal** — better than a fixed 12 V brick, for two reasons:

- **Adjustable voltage** lets you start at 5 V and wind up gradually. Much safer than going straight
  to full drive on the first run.
- **The current limit is a hardware safety net for the voice coil.** Set it to **4 A** — that's
  inside both the driver's 90 W rating and your supply's 5 A ceiling, so the coil physically cannot
  be cooked no matter what the software does.

The driver is 8 Ω nominal but **6 Ω DC**, so at 12 V it draws about 2 A and at 24 V about 4 A.

**Current is the binding constraint here, not the driver.** Reaching ±10 mmHg in a 6.7 L chamber
needs somewhere around **3–5 A at 18–29 V** — right at the top of what your supply can give. That
estimate is rough, since excursion isn't published.

> **So build long, then shorten.** Start with a bigger chamber — 15 L or so, where you'd only need
> 1.5–2 A — and confirm the whole rig works end to end. Then cut the pipe down toward 6.7 L and watch
> the pressure climb. Much better than starting at full pressure and having to work out whether a
> disappointing result is current limiting, a leak, or the driver itself.
>
> If you can't reach ±10 mmHg at 4 A, don't push the current — use a longer chamber and accept a
> smaller swing. The scaling law is what you're measuring; the absolute number matters less.

> **You must add a bulk capacitor.** Solder a **2200 µF, 35 V** electrolytic directly across `B+` and
> `B−` at the motor driver — stripe to `B−`. It's not optional, for two reasons:
>
> 1. The driver draws current in 20 kHz pulses. A bench supply's regulation loop is far too slow to
>    follow that, and the long leads make it worse. Without local capacitance the supply rail sags
>    and rings.
> 2. **A bench supply can source current but cannot sink it.** Every time the cone decelerates or
>    reverses, energy flows back into the supply. With nowhere to go it pushes the rail voltage up,
>    which can trip the supply's over-voltage protection or damage the driver. The capacitor absorbs
>    it.

One behaviour to know: if you hit the current limit the supply drops into constant-current mode and
the voltage sags. That protects the coil, but it also distorts your waveform. If the pressure trace
suddenly looks clipped or misshapen, check whether the supply has gone into CC before you go hunting
for a mechanical cause.

---

## What to expect

An 8" driver has a cone area of roughly 220 cm² and moves about ±4 mm, so it sweeps around
**176 mL** per cycle. Put that into different tube lengths and you should see:

| Tube volume | DN100 pipe length | Expected swing |
|---:|---:|---|
| 2 L | 235 mm | ±33 to ±47 mmHg |
| **5 L** | **590 mm** | **±13 to ±19 mmHg** |
| 6.7 L | 790 mm | ±10 to ±14 mmHg |
| 10 L | 1180 mm | ±6.7 to ±9.4 mmHg |
| 15 L | 1770 mm | ±4.5 to ±6.2 mmHg |
| 45 L (real leg chamber) | — | ±1.5 to ±2.1 mmHg |

The range on each row is because air heats slightly as it's compressed. Squeeze it slowly and the
heat escapes (lower figure); squeeze it fast and it doesn't (upper figure). Which end you land on is
one of the things this rig measures.

Two things fall out of that table:

- **At 5 L you'll overshoot ±10 mmHg and probably saturate the ±15 mmHg sensor.** That's a good
  problem — it means the concept works. Add pipe until it fits on the scale.
- **At 45 L this driver gives you almost nothing.** That's not a failure, it's the scaling law doing
  what it does: you'd need roughly 1 litre of swept volume for ±10 mmHg in a leg-sized chamber, about
  6× this driver. Proving the physics at 5 L is what justifies spending real money on that actuator.

## Build it

Start at **~800 mm of pipe (6.7 L)**, which should land near ±10 mmHg and keep you on-scale.

**The driver is about twice the diameter of the pipe**, so they can't just be joined — you print an
adaptor between them:

| | |
|---|---|
| Driver overall diameter | **220 mm** (and 92 mm deep) |
| Driver cutout | **182 mm** |
| Driver bolt circle | 212 mm |
| DN100 pipe | 110 mm outside, **~104 mm inside** |

1. **Cut ~800 mm of pipe.** Cap one end. Drill the cap for the barb fitting and seal it with
   silicone — that's where the pressure sensor connects.

2. **Print the adaptor plate** for the other end. Keep it **flat, not a cone**: a disc roughly
   245 mm across and 10 mm thick, with the 182 mm driver cutout and bolt pattern on the front, and a
   short spigot on the back that solvent-welds into the pipe socket. The bore just steps abruptly
   from 182 mm down to 104 mm inside the plate.

   A cone would look neater but adds well over a litre of dead volume. At 1 Hz the abrupt step
   costs you nothing — the air has all the time in the world to get through.

   245 mm may not fit your print bed. Print it in halves and bond them if so.

3. **Epoxy the printed part.** 3D prints leak through the layer lines even when they look solid.
   Brush it and test it on its own before assembling.

4. **Bolt the driver on**, cone facing into the tube, back open to the room. Foam gasket under the
   flange.

5. **Leak test before you go further.** Push some air in with a syringe and watch the pressure. It
   should hold for at least ten seconds. If it drops fast, find the leak now — a leaky tube looks
   exactly like a weak actuator, and you'll waste a weekend chasing the wrong thing.

6. **Measure the real chamber volume** — don't calculate it. The adaptor cavity and the dish of the
   cone itself add somewhere around half a litre on top of the pipe, which is ~10% of your total and
   too much to hand-wave.

   Inject a known volume **slowly** with the syringe (slowly matters — it keeps the air isothermal)
   and read the settled pressure. Then:

   ```
   V = 760 × injected_volume / ΔP        [litres, mmHg]
   ```

   60 mL giving 8.9 mmHg means 5.1 L. Use that measured figure everywhere instead of the pipe
   length, and your predicted pressures will actually match what you see.

---

## Wire it

**Driver → IBT-2 → Pi**

| IBT-2 pin | Goes to |
|---|---|
| `B+` / `B−` | Bench supply at 12 V, **with the 2200 µF cap across these pins** |
| `M+` / `M−` | Speaker terminals (8 Ω nominal, 6 Ω DC) |
| `VCC` | Pi **3.3 V** — this is what makes 3.3 V logic register properly |
| `GND` | Pi GND **and** supply ground |
| `R_EN`, `L_EN` | Both to Pi 3.3 V |
| `RPWM` | GPIO12 |
| `LPWM` | GPIO13 |

GPIO12 and 13 are the Pi's hardware PWM pins. PWM one and hold the other low to push the cone; swap
them to pull. **Never drive both high** — that shorts the supply through the bridge.

> **Use the motor driver, not an audio amplifier.** Audio amps deliberately block anything below
> ~20 Hz. You're running at about 1 Hz, so an audio amp would throw away almost everything and make
> the rig look like a total failure.

**Pressure sensor → ADS1115 → Pi**

- Sensor: 5 V and GND from the Pi.
- Sensor output → **2:1 divider** (two 10 kΩ resistors) → ADS1115 channel A0.
  The sensor swings 0.5–4.5 V, which would damage a 3.3 V-powered ADC. Halving gives 0.25–2.25 V.
- ADS1115: 3.3 V, GND, SDA → GPIO2, SCL → GPIO3.

Even after halving, resolution is around 0.001 mmHg per step. Nowhere near a limitation.

---

## Run it

Use `pigpio` for hardware-timed PWM. Generate a sine wave, log the pressure, plot it.

Then try:

- **Slow sine, ~1 Hz.** How many mmHg? That's the headline number.
- **Wind the amplitude up** until it stops improving.
- **Sweep frequency**, 0.5 to 20 Hz, and find where it falls off.
- **Fast step** — flip negative to positive as fast as you can. 50 ms is the target, since that's the
  useful window in a heartbeat.
- **Add pipe.** Glue on the coupling and another section. Pressure should drop in proportion. That's
  the scaling law that lets you predict a leg-sized chamber.

Two practical notes:

- **If the sensor pins at ±15 mmHg**, good problem — add more pipe.
- **Don't hold a steady offset for long.** At these speeds the coil behaves like a plain resistor and
  pulls current while doing nothing, so it heats up. Short bursts are fine.

**One Pi 4 caveat:** Linux isn't real-time. The PWM carrier is hardware so that's rock solid, but
waveform updates come from Python and may jitter a millisecond or two. Irrelevant now. If you later
want tight ECG-gated timing, that part moves to a microcontroller.

---

## Success looks like

A clean, repeatable pressure swing of a few mmHg, behaving the way you'd expect when you change
amplitude and tube length.

If that works, the question becomes how it scales up — and you'll have real numbers instead of
estimates.

---

## Where this goes next

The architecture is already proven in a clinical device. The **SensorMedics 3100A** high-frequency
oscillatory ventilator drives a **365 cc diaphragmatically sealed piston** with an electrical coil at
3–15 Hz, producing over 90 cmH₂O (~66 mmHg) of swing — voice coil, sealed piston, both positive and
negative pressure. It's been in neonatal ICUs for decades. Its 365 cc displacement is close to the
~400 mL peak-to-peak needed for ±10 mmHg in a 15 L chamber.

So phase 2, once this rig gives you real numbers, is a bigger actuator on a bought diaphragm:

- **Actuator:** H2W `NCM08-25-100-2LB` — 19.1 mm stroke, 45 N continuous / 134 N peak, integrated
  ball bushing bearing. Price on application; these are quote-only industrial parts.
- **Diaphragm:** don't fabricate one. A **speaker passive radiator** is a rigid piston plus a rubber
  rolling seal plus a bolt-on frame, with no motor — AU$12–62 in 8" to 15". Bolt the actuator shaft
  to the centre. A 200 mm diaphragm at 19.1 mm stroke sweeps about 600 mL, which is right in range.

---

## Later (not now)

Thigh seal · ECG gating · measuring anything physiological · anything involving a person.
