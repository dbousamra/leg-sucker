# Leg Sucker — MVP 1

## What this is

Some people have arteries in their legs so narrowed that not enough blood gets in. The tissue
starves, ulcers open up and won't heal, and in bad cases the leg is amputated. The usual treatment —
squeezing the limb with compression stockings or cuffs — can't be used, because squeezing a leg
that's already short of arterial blood makes the inflow worse, and the skin is often too fragile to
touch at all.

The idea is to move blood **without touching the leg**: seal the limb in a rigid chamber and cycle
the air pressure around it in time with the heartbeat. Suck as the heart beats, so the arteries meet
less resistance from outside. Push gently between beats, to help fluid drain back out. A bellows
around the leg, breathing with the pulse.

That's unproven and a long way off. **This document is the first question underneath it: can a voice
coil generate useful pressure in a sealed chamber?** A speaker on a sealed PVC tube, and a gauge to
see what comes out.

No leg, no seal, no ECG, no human.

---

## Parts

| Item | What it does |
|---|---|
| [8" woofer, Jaycar CW2196](https://www.jaycar.com.au/woofer-speaker-driver-8-inch/p/CW2196) | **The actuator.** A speaker is a voice coil that already has a piston (the cone) and a flexible gas seal (the surround) built in |
| [100 mm PVC DWV pipe, 3 m](https://www.bunnings.com.au/holman-100mm-x-3m-pvc-dwv-pipe_p4770345) | The chamber. 85 mL of air per cm of length |
| [100 mm push-on cap](https://www.bunnings.com.au/search/products?q=Holman+100mm+PVC+DWV+Push+On+Cap) × 2 | Seals the far end. One gets drilled for the sensor port |
| [Deks 100 mm rubber joiner](https://www.bunnings.com.au/deks-100mm-pvc-to-pvc-rubber-joiner_p4730112) × 2 | Joins adaptor to pipe, and pipe to pipe — with hose clamps, so you can pull it apart to change the chamber volume |
| `cad/adaptor-spigot.stl` | Printed funnel taking the 220 mm driver down to the 110 mm pipe |
| [4 mm brass bulkhead barb](https://www.aliexpress.com/item/33041152234.html) | Passes through the end cap so the sensor can see chamber pressure. Nut clamps it, silicone seals it |
| [Clear silicone tube, OD5 × ID3 mm](https://www.aliexpress.com/item/1005008350652653.html) | Barb to sensor. Clear, so you can see if condensation collects |
| [MPXV7002DP sensor](https://www.aliexpress.com/item/1005007057842984.html) | Measures chamber pressure against room air. ±15 mmHg. **The one number this whole rig exists to produce** |
| [Raspberry Pi Pico 2](https://www.aliexpress.com/item/1005008058623788.html) | Generates the drive waveform, reads the sensor, streams CSV over USB |
| [IBT-2 / BTS7960 motor driver](https://www.aliexpress.com/item/1005009194435701.html) | Pushes current through the coil in both directions, at frequencies an audio amp can't reach |
| [2200 µF 35 V capacitor](https://www.aliexpress.com/item/1005011811368397.html) | Sits across the driver's supply and soaks up the energy the cone pushes back |
| [Resistor kit](https://www.aliexpress.com/item/1005011772534173.html) — you need 2 × 10 kΩ | Halves the sensor's 5 V output so it can't destroy the Pico's 3.3 V input |
| [830-point breadboard](https://www.aliexpress.com/item/1005003647931024.html) | Holds the divider and the sensor |
| [Dupont jumpers, 120 pc](https://www.aliexpress.com/item/1005002349042216.html) | Pico to driver logic pins and to the sensor |
| [18 AWG silicone cable, 3 m](https://www.aliexpress.com/item/1005009192506490.html) | Driver to speaker. Carries 3–5 A, so not jumper wire |
| [Spade connectors](https://www.jaycar.com.au/search?text=spade%20connectors) | Onto the speaker tabs |
| [Neutral-cure silicone](https://www.bunnings.com.au/search/products?q=neutral+cure+silicone+sealant) | Seats the barb and anything not solvent-welded |
| [PVC cement + priming fluid](https://www.bunnings.com.au/search/products?q=Protek+Type+N+PVC+Cement+Non+Pressure) | The PVC-to-PVC joints. Does **not** bond to PLA or PETG |
| [Two-part epoxy](https://www.bunnings.com.au/search/products?q=two+part+epoxy+resin) | Sealing the printed adaptor if it leaks through the layer lines |
| [M4 bolts + foam gasket](https://www.bunnings.com.au/search/products?q=M4+bolts) | Mounts the driver airtight to the adaptor |
| [Pipe saddle clips](https://www.bunnings.com.au/search/products?q=100mm+pipe+saddle+clip) × 2 | Holds the rig down. 29 N oscillating at 1 Hz will walk a 1 m pipe off the bench |
| [60 mL syringe](https://www.bunnings.com.au/search/products?q=60ml+syringe) | Injects a known volume for the leak test and to measure the chamber |

Plus a bench supply, a 3D printer, and a micro-USB cable.

---

## Build

**1. Print the adaptor** — `cad/adaptor-spigot.stl`. 245 mm flange, 182 mm driver cutout, tapering
to a 110 mm spigot. Print flange-down; the taper is 38° from vertical so it needs no support.

The front face has a scribed groove at the 212 mm bolt circle but **no bolt holes** — Jaycar don't
publish how many the driver has. Sit the driver on the groove, mark through its own flange, drill.

**2. Cut 800 mm of pipe.** Cap one end.

**3. Drill the end cap** for the bulkhead barb. Nut on the inside, silicone on the seat.

**4. Check the print holds air.** Blank off the spigot and pressurise. PETG with 5+ perimeters is
often fine; only brush it with epoxy if it actually weeps.

**5. Bolt the driver on** — cone facing *into* the tube, basket out in free air, foam gasket under
the flange.

That orientation matters. Mounted this way the funnel only clears the shallow dish of the cone.
Turned round, it would have to swallow the whole 92 mm-deep basket.

**6. Clamp the adaptor to the pipe** with a rubber joiner. Tighten both hose clamps. Nothing here is
glued — solvent cement dissolves PVC and does nothing to PETG, and you'll be pulling this apart
repeatedly to change volume.

**7. Bolt the rig down** with the saddle clips.

**8. Leak test.** Push air in with the syringe and watch the pressure. It should hold for at least
ten seconds. Find leaks now — a leaky tube looks exactly like a weak actuator.

**9. Measure the real chamber volume.** Don't calculate it: the adaptor alone adds 1.36 L, so 800 mm
of pipe is nearer 8 L than 6.7 L. Inject a known volume **slowly** and read the settled pressure:

```
V = 760 × injected_volume / ΔP        [litres, mmHg]
```

60 mL giving 8.9 mmHg means 5.1 L. Use that number everywhere afterwards.

---

## Wire

**Driver → IBT-2 → Pico**

| IBT-2 | Goes to |
|---|---|
| `B+` / `B−` | Bench supply, **with the 2200 µF capacitor across these pins** (stripe to `B−`) |
| `M+` / `M−` | Speaker terminals, 18 AWG cable |
| `VCC` | Pico `3V3` (pin 36) |
| `GND` | Pico `GND` **and** supply ground |
| `R_EN`, `L_EN` | Both to Pico `3V3` |
| `RPWM` | `GP16` |
| `LPWM` | `GP17` |

PWM one and hold the other low to push the cone; swap to pull. **Never drive both high** — that
shorts the supply through the bridge.

**Sensor → Pico**

- Sensor power: `VBUS` (pin 40) and `GND`
- Sensor output → **2:1 divider**, two 10 kΩ resistors → `GP26`
- **Only one sensor port goes to the chamber.** The other stays open to room air — that's what makes
  it differential

**Four things that will cost you an evening**

- **Motor driver, not an audio amp.** Audio amps block everything below ~20 Hz. You're running at
  1 Hz, so one would throw away almost everything and make the rig look dead.
- **The divider isn't optional.** The sensor swings to 4.5 V; the Pico's ADC stops at 3.3 V.
- **Keep the motor circuit off the breadboard.** It carries 3–5 A; breadboards manage about 1 A
  before the contacts cook. Screw terminals and proper cable for that loop.
- **Star-ground at the IBT-2.** Run motor ground straight back to the driver, not daisy-chained
  through the breadboard, or the switching noise lands in your pressure trace.

---

## Run

Set the supply to **12 V with a 4 A current limit** before anything is connected. Verify with a
meter.

**1. Test the driver with the speaker on the bench, out of the chamber.** Slow sine, low amplitude,
watch the cone. If it fails here it's electrical — you don't want to be wondering whether it's a
leak.

**2. Wind the amplitude up until you hear the coil bottom out** — a dull click. Stay below that
level, and note it. **That's your first real measurement of Xmax**, which no datasheet gave you, and
every predicted pressure below scales off it.

**3. Bolt it to the chamber** and repeat at low amplitude. Pressure should appear immediately.

**4. Start with a long chamber and work down.** At 15 L you need only 1.5–2 A. At 6.7 L you need
3–5 A, near your supply's ceiling — and if the result disappoints you won't know whether it's
current limiting, a leak, or the driver.

Then measure:

- **Slow sine, ~1 Hz** — how many mmHg? That's the headline number
- **Sweep 0.5 to 20 Hz** — find where it falls off
- **Fast step** — flip negative to positive as fast as you can. 50 ms is the target, the useful
  window in a heartbeat
- **Add pipe** — pressure should drop in proportion. That's the scaling law that predicts a
  leg-sized chamber

**Don't hold a steady offset for long.** Below resonance the coil behaves like a plain resistor and
pulls current while doing nothing, so it heats. Short bursts only.

---

## What to expect

The driver sweeps about **176 mL** per cycle (220 cm² cone, ±4 mm).

| Chamber | Expected swing |
|---:|---|
| 2 L | ±33 to ±47 mmHg |
| 5 L | ±13 to ±19 mmHg |
| 6.7 L | ±10 to ±14 mmHg |
| 10 L | ±6.7 to ±9.4 mmHg |
| 15 L | ±4.5 to ±6.2 mmHg |
| 45 L (real leg chamber) | ±1.5 to ±2.1 mmHg |

Each range spans slow compression (heat escapes) to fast (it doesn't). Which end you land on is one
of the things this rig measures.

**Success** is a clean, repeatable swing of a few mmHg that behaves as expected when you change
amplitude and tube length.

**The 45 L row is the real finding.** Not a failure — the scaling law being honest. A leg chamber
needs roughly 1 litre of swept volume, about 6× this driver. Proving the physics at 5 L is what
justifies spending real money on that actuator.

---

## Later

Thigh seal · ECG gating · measuring anything physiological · anything involving a person.
