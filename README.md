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

**Total ≈ AU$283** plus shipping, assuming you already have a bench power supply and a 3D printer.

| Item | What it's for | Where | Price |
|---|---|---|---:|
| **Jaycar CW2196** — 8" woofer, 8 Ω, Fs 28.1 Hz, Re 6.0 Ω, 90 W | **The actuator.** A speaker is a voice coil with the piston and gas seal already built in | [Jaycar CW2196](https://www.jaycar.com.au/woofer-speaker-driver-8-inch/p/CW2196) | $44.95 |
| **MPXV7002DP breakout** — ±2 kPa (±15 mmHg) differential, barbed ports | Measures chamber pressure against room air — the one number the whole rig exists to produce | [AliExpress](https://www.aliexpress.com/item/1005007057842984.html) | $20.19 |
| **Raspberry Pi Pico 2** (headers soldered) | Runs everything: generates the drive waveform, reads the pressure, streams CSV over USB | [AliExpress](https://www.aliexpress.com/item/1005008058623788.html) · [Core Electronics](https://core-electronics.com.au/) | $5.94–17 |
| **ADS1115** — 16-bit I²C ADC *(optional)* | Not needed — the Pico has ADCs. Worth $2 as a fallback if the built-in one proves noisy next to the motor driver | [AliExpress](https://www.aliexpress.com/item/1005012498259780.html) | $1.99 |
| **IBT-2 / BTS7960** — H-bridge motor driver | Drives the coil in both directions at frequencies an audio amp can't reach | [AliExpress](https://www.aliexpress.com/item/1005009194435701.html) | $17.29 |
| **Holman 100mm × 3m PVC DWV pipe** | The chamber. 85 mL per cm, so 800 mm ≈ 6.7 L | [Bunnings](https://www.bunnings.com.au/holman-100mm-x-3m-pvc-dwv-pipe_p4770345) | $33.65 |
| **Holman 100mm PVC DWV push-on cap** × 2 | Seals the far end; one gets drilled for the sensor port | [Bunnings](https://www.bunnings.com.au/search/products?q=Holman+100mm+PVC+DWV+Push+On+Cap) | $7.80 |
| **Deks 100mm PVC-to-PVC rubber joiner** × 2 | **Every joint in the rig, reversibly.** A rubber sleeve with two hose clamps — joins the adaptor to the pipe, and pipe sections to each other. Undo two clamps to change the chamber volume | [Bunnings](https://www.bunnings.com.au/deks-100mm-pvc-to-pvc-rubber-joiner_p4730112) | $21.00 |
| **Protek 250ml Type N PVC cement** | Glues pipe joints — solvent-welded joints don't leak | [Bunnings](https://www.bunnings.com.au/search/products?q=Protek+Type+N+PVC+Cement+Non+Pressure) | $8.42 |
| **Protek 125ml priming fluid** | Preps the PVC so the cement actually bonds | [Bunnings](https://www.bunnings.com.au/search/products?q=Protek+Red+Priming+Fluid) | $6.68 |
| **Neutral-cure silicone sealant** | Seals the sensor port and anything not solvent-welded | [Bunnings](https://www.bunnings.com.au/search/products?q=neutral+cure+silicone+sealant) | $12 |
| **Two-part epoxy** | Brushed over the printed adaptor — FDM prints leak through layer lines even when they look solid | [Bunnings](https://www.bunnings.com.au/search/products?q=two+part+epoxy+resin) | $20 |
| **PETG or PLA filament** (~300 g) | The adaptor, from `cad/adaptor.stl` | you have this | — |
| **Barbed fitting + silicone tube** | Connects the chamber to the pressure sensor | [Bunnings](https://www.bunnings.com.au/search/products?q=barbed+hose+fitting) | $10 |
| **M4 bolts + closed-cell foam gasket** | Bolts the driver to the printed adaptor, gasket makes it airtight | [Bunnings](https://www.bunnings.com.au/search/products?q=M4+bolts) | $15 |
| **60 mL syringe** | Injects a known volume for the leak test and to calibrate the sensor | [Bunnings](https://www.bunnings.com.au/search/products?q=60ml+syringe) | $5 |
| **2200 µF 35 V electrolytic capacitor** | Sits across the motor driver's supply. **Don't skip it** — see below | [Jaycar](https://www.jaycar.com.au/search?text=2200uF%2035V%20electrolytic) | $3 |
| **2 × 10 kΩ resistors** | Voltage divider so the 5 V sensor output can't damage the 3.3 V ADC | [Jaycar](https://www.jaycar.com.au/search?text=10k%20ohm%20resistor) | $1 |
| **Figure-8 speaker cable**, 16–18 AWG, a few metres | Driver to motor driver. It carries 3–5 A, so not jumper wire | [Jaycar](https://www.jaycar.com.au/search?text=figure%208%20speaker%20cable) | $8 |
| **Spade connectors** to suit the driver terminals | Onto the speaker tabs, unless you'd rather solder | [Jaycar](https://www.jaycar.com.au/search?text=spade%20connectors) | $5 |
| **Female-female jumper leads** | Pico GPIO to the driver's logic pins and the sensor | [Jaycar](https://www.jaycar.com.au/search?text=jumper%20leads%20female) | $8 |
| **Micro-USB cable** (data, not charge-only) | Powers and programs the Pico. Easy to assume you have one — most people only have USB-C now | [Jaycar](https://www.jaycar.com.au/search?text=micro%20usb%20cable) | $8 |
| **Small breadboard** | The divider and sensor. **Logic side only** — see the warning in Wire it | [Jaycar](https://www.jaycar.com.au/search?text=breadboard) | $8 |
| **2 × pipe saddle clips**, or a G-clamp | Holds the rig down. 29 N oscillating at 1 Hz will walk a 1 m pipe across the bench | [Bunnings](https://www.bunnings.com.au/search/products?q=100mm+pipe+saddle+clip) | $12 |

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

2. **Print the adaptor** — `cad/adaptor-spigot.stl`. 245 mm flange, 182 mm driver cutout, tapering
   to a 110 mm spigot that a rubber joiner clamps onto. 100 mm long. Print flange-down: the taper is
   38° from vertical, so no support needed.

   245 mm fits flat on a 256 bed, diagonally on a 220. It's chunky — ~460 cm³ solid, so a couple of
   hundred grams and several hours. Drop `FLANGE_THICKNESS` to 6 mm in `cad/adaptor.py` if you want
   it lighter.

   **No bolt holes.** Jaycar give the 212 mm bolt circle but not how many holes the driver has, so
   the front face has a shallow scribed groove at that diameter. Sit the driver on it, mark through
   its own flange, drill to match.

3. **Join everything with the rubber joiners — nothing here is glued.** The joiner is a rubber
   sleeve with two hose clamps: slide it over the adaptor's spigot and the pipe, tighten both, done.
   Undo the clamps and the whole rig comes apart.

   That matters more than convenience: the test plan works by *changing the chamber volume*, so
   pipe joints you can undo in thirty seconds are the difference between a rig you can sweep and one
   you'd have to cut up.

4. **Check the print is gas-tight before assembling.** FDM prints can leak through the layer lines.
   Blank off the spigot, pressurise, and see. PETG with 5+ perimeters is often fine as-is — only
   coat it if it actually leaks, and see the note below on sealing options.

5. **Bolt the driver on**, cone facing into the tube, basket out in free air. Foam gasket under the
   flange, bolts through your drilled holes. Also reversible.

   That orientation isn't cosmetic. Mounted this way the funnel only has to clear the shallow dish
   of the cone. Turned round, it would have to swallow the entire 92 mm-deep basket, and the funnel
   would need to be far bigger.

7. **Leak test before you go further.** Push some air in with a syringe and watch the pressure. It
   should hold for at least ten seconds. If it drops fast, find the leak now — a leaky tube looks
   exactly like a weak actuator, and you'll waste a weekend chasing the wrong thing.

8. **Measure the real chamber volume** — don't calculate it. The adaptor alone adds **1.36 L**, and
   the dish of the cone adds a few hundred mL more. So 800 mm of pipe is not 6.7 L, it's closer to
   8 L. That's a 20% error if you go by pipe length, which is more than enough to make your
   predictions disagree with reality for no visible reason.

   Inject a known volume **slowly** with the syringe (slowly matters — it keeps the air isothermal)
   and read the settled pressure. Then:

   ```
   V = 760 × injected_volume / ΔP        [litres, mmHg]
   ```

   60 mL giving 8.9 mmHg means 5.1 L. Use that measured figure everywhere instead of the pipe
   length, and your predicted pressures will actually match what you see.

---

## Keeping it all reversible

Nothing in this build is glued shut. That's deliberate — you'll be changing the chamber volume
repeatedly, and a rig you can't take apart is a rig you can only measure once.

| Joint | How it seals | To undo |
|---|---|---|
| Adaptor → pipe | Deks rubber joiner, two hose clamps | Loosen two clamps |
| Pipe → pipe section | Second rubber joiner | Loosen two clamps |
| Driver → adaptor | Foam gasket + bolts | Unbolt |
| End cap → pipe | Push-on cap, friction fit | Pull |
| Sensor port | Barb through the cap | Silicone here is fine — it's small, and silicone peels off cleanly anyway |

If the push-on cap weeps, wrap the pipe end in a couple of turns of self-amalgamating silicone tape
before pushing it on. Still reversible.

**A note on the epoxy.** It was never a glue — it's a brushed-on coating to seal the *porosity* of
the print, and it doesn't bond the adaptor to anything. You may not need it at all: at 0.19 psi, a
PETG print with 5+ perimeters is often gas-tight on its own. Test first. If it does weep, in
increasing order of permanence:

1. Reprint with more perimeters and a hotter nozzle — better layer bonding, no coating at all
2. Acrylic spray sealer — thin, cheap, reversible enough
3. Brushed epoxy or XTC-3D — the durable option, and still only a surface coat

**If you'd rather have no external hardware**, the alternative is `cad/adaptor-socket.stl`: a socket
that slips over the pipe with an O-ring or silicone seal. It's more compact and adds 0.33 L less
dead volume, but you'd need a ~110 mm O-ring, and it's fiddlier to separate. The rubber joiner is
the better trade for a rig you'll be reconfiguring.

---

## Wire it

**Driver → IBT-2 → Pico**

| IBT-2 pin | Goes to |
|---|---|
| `B+` / `B−` | Bench supply at 12 V, **with the 2200 µF cap across these pins** |
| `M+` / `M−` | Speaker terminals (8 Ω nominal, 6 Ω DC) |
| `VCC` | Pico **3V3** (pin 36) — this is what makes 3.3 V logic register properly |
| `GND` | Pico GND **and** supply ground |
| `R_EN`, `L_EN` | Both to Pico 3V3 |
| `RPWM` | GP16 |
| `LPWM` | GP17 |

GP16 and GP17 are channels A and B of the same PWM slice, so they share one 20 kHz carrier with
independent duty — exactly what's wanted. PWM one and hold the other low to push the cone; swap them
to pull. **Never drive both high** — that shorts the supply through the bridge.

> **Keep the motor circuit off the breadboard.** Supply, driver and speaker carry 3–5 A; breadboards
> and jumper wire are good for about 1 A before they heat up and the contacts degrade. Use the
> IBT-2's screw terminals and proper cable for anything in that loop. Only the logic pins — `RPWM`,
> `LPWM`, `R_EN`, `L_EN`, `VCC`, `GND` — should ever see a jumper lead.

> **Use the motor driver, not an audio amplifier.** Audio amps deliberately block anything below
> ~20 Hz. You're running at about 1 Hz, so an audio amp would throw away almost everything and make
> the rig look like a total failure.

**Pressure sensor → Pico**

- Sensor: **VBUS** (pin 40, 5 V when the Pico is USB-powered) and GND.
- Sensor output → **2:1 divider** (two 10 kΩ resistors) → **GP26** (ADC0).

The divider isn't optional. The sensor runs on 5 V and swings 0.5–4.5 V; the Pico's ADC tops out at
3.3 V. Halving gives 0.25–2.25 V, which fits with headroom even if the sensor rails.

Resolution works out to about **0.012 mmHg per step**, and you can oversample on top of that. Nowhere
near a limitation.

Two things that will cost you an evening if you get them wrong:

- **The sensor has two ports. Only one goes to the chamber**; the other must stay open to room air.
  That's what makes the reading differential. Which port you pick sets the sign — if suction reads
  positive, swap the tubes or flip the sign in software.
- **Star-ground at the IBT-2.** The Pico is powered from your laptop's USB, and its ground now
  connects to a circuit switching several amps. Run the motor ground straight back to the driver
  rather than daisy-chaining it through the breadboard, or you'll see the switching noise in your
  pressure trace and possibly drop the USB connection.

**Optional: ADS1115 instead of the built-in ADC.** The Pico's ADC is a 12-bit SAR whose reference is
the 3.3 V rail — the same rail sitting next to a motor driver switching several amps at 20 kHz. If
the pressure trace looks noisier than the rig should be, swapping to the ADS1115 (16-bit, own
reference, programmable gain) tells you immediately whether the noise is real or an artefact of
measurement. Wire it 3V3 / GND / SDA→GP0 / SCL→GP1, with the same divider into A0.

Start with the built-in ADC — fewer parts, faster to get going. Keep the ADS1115 in the drawer.

---

## First power-up

Do this in order. Each step isolates one thing, so when something misbehaves you know what it was.

1. **Set the supply before anything is connected.** 12 V, current limit 4 A. Verify with a meter —
   don't trust the front panel.

2. **Test the driver with the speaker on the bench, out of the chamber.** Run a slow sine at low
   amplitude and watch the cone. You're checking that the driver works, the direction reverses, and
   nothing rubs. If it fails here it's electrical, and you don't want to be wondering whether it's a
   leak.

3. **Listen at the extremes.** Wind the amplitude up until you hear the coil bottom out — a dull
   click at the excursion limit. Note the drive level where that starts and stay below it. That
   figure is also your first real estimate of Xmax, which no datasheet gave you.

4. **Now bolt it to the chamber** and repeat at low amplitude. Pressure should appear immediately.

5. **Leak test before you interpret anything.**

## Run it

Generate a sine wave on the PWM pins, log the pressure, plot it.

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

Firmware is MicroPython on the Pico: hardware PWM for the carrier, a timer to step the waveform,
`machine.ADC` for the sensor, and `print()` of CSV over USB serial. Capture on your laptop and plot
there. Timing is deterministic, so the 50 ms step measurement and later ECG gating will both hold up
— which a Linux host would not have.

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
