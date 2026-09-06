# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

No code yet. No build, test, or run commands exist — do not invent them; update this file once the
first firmware lands.

**Current focus is `README.md`: MVP 1, a bench rig answering one question — can a voice coil generate
useful +/- pressure in a sealed chamber?** Thigh seal, ECG gating, physiological endpoints, and
human use are all explicitly deferred. Read `README.md` before proposing work.

MVP budget is < AU$500, so the AU$1,190 VCAR voice coil is out of scope for now — the plan shrinks
the *chamber* instead, since required stroke volume scales linearly with chamber volume.

## What this project is

"Leg sucker" — a medical device concept: a **sealed rigid chamber enclosing an entire leg**, in which
a bellows/piston generates **alternating negative and positive ambient pressure**, **gated to the ECG
R-wave**. Intended for severe peripheral vascular disease and ulcerated limbs, where conventional
compression is contraindicated because it touches the tissue.

The distinguishing claim versus prior art is the combination of: full-leg sealed chamber (not cuffs),
active generation of *both* negative and positive pressure, ECG-gated timing, and non-contact
operation. Closest prior art is EECP (Enhanced External Counterpulsation), which uses ECG-triggered
pneumatic *cuffs* — same physiological intent, different mechanism.

## Established design numbers

Do not re-derive these; they are settled.

| Parameter | Value |
|---|---|
| Chamber | ~75-80 cm long x 30 cm dia -> **~53 L** gross |
| Effective air volume | ~40-45 L (leg displaces ~8-12 L) |
| Target pressure swing | **-10 to +10 mmHg** initially (-5/+5 conservative start) |
| Bellows stroke for +/-10 mmHg | **~0.5-0.7 L**; design for 1 L adjustable |
| Transition time target | **~50 ms** negative-to-positive within one cardiac cycle |
| Implied flow rate | ~10 L/s |
| Pneumatic power at that duty | only ~13 W — the load is *accelerating the piston*, not pumping |
| Force on a 200 mm diaphragm at 1.33 kPa | ~42 N static; size actuator to **100-300 N peak** |
| Tubing | >=30-40 mm ID to keep resistance low |

**Corrected small-signal relation** (the table above came from an AI-generated working that had two
errors; treat the relation below as authoritative):

```
dV_pp = V * dP_pp / (n * 760)        [mmHg, litres]
```

1. **Polytropic, not isothermal.** `n` runs 1.0 (isothermal, slow) to 1.4 (adiabatic, fast). At a
   50 ms transient the gas is closer to adiabatic, so up to 40% *more* pressure per unit stroke than
   the isothermal figure suggests. `n(f)` is a measured output of MVP 1, not an assumption.
2. **Amplitude vs peak-to-peak was conflated.** The "0.5-0.7 L" bellows figure is the stroke to go
   from 0 to -10 mmHg. A true +/-10 mmHg *swing* at 53 L needs ~1.0-1.4 L peak-to-peak.

Force is never the constraint: +/-10 mmHg is +/-1.33 kPa = +/-0.19 psi, so a 210 mm piston sees only
~29 N. The difficulty is entirely **gas-tightness and swept volume**. Do not over-engineer the
pressure vessel.

## Physiological rationale

- Negative external pressure during **systole** raises arterial transmural pressure
  (`P_transmural = P_internal - P_external`) -> increased arterial inflow.
- Positive external pressure during **diastole** reduces capillary filtration and venous pooling
  -> opposes oedema.
- Excessive positive pressure impairs arterial inflow — hence the modest initial targets.

The controller must expose, as tunable parameters: R-wave delay to suction onset, suction duration,
return-to-positive timing, positive pressure duration, bellows stroke volume, max pressure limits,
and waveform shape.

## Actuator research (completed, 2026-08)

Conventional pumps are the wrong architecture for a 50 ms transient — this needs a device that
*physically changes volume* fast. Ranked: voice-coil linear actuator > large BLDC + scotch yoke >
linear servo > pneumatic cylinder > diaphragm pump (wrong tool).

AliExpress survey results, for reference:

- **VCAR series** (listing `1005008598907114`) — flat price ~AU$1,190 across *all 22 variants*, so
  buy the largest. `VCAR0294-0498-00A` = 294 N peak / 49.8 mm stroke / Kf 24.5 N/A. Best fit.
- **60VC002** (listing `1005007792648215`, SHANGLINMOTOR) — 49 N / 16 mm / 24 V, ~AU$244. Marginal:
  back-EMF at 0.5 m/s is ~18.5 V against a 24 V rating, so it is voltage-limited for this duty.
- **Listing trap:** most "60VC002 ... 5KG 16mm" listings at AU$50-130 are grab-bags of 18 unlabelled
  variants; the cheap ones are 0.1-0.4 kgf / 4-5 mm motors. Only buy listings with *named* variants.
- Cheap prototype alternative: a long-excursion 12" subwoofer driver is mechanically the same thing
  (Sd ~500 cm^2, +/-15 mm Xmax -> 1.5 L peak-to-peak) for AU$100-200, but Xmax specs are unreliable.

None of these ship with position feedback — an encoder/LVDT and a closed loop are ours to add. The
VCAR coil is also unsupported (no bearing), so the diaphragm or a flexure must provide radial
constraint.

## Existence proof: SensorMedics 3100A (read from the manual, 2026-09)

Full operator's manual text is extracted to `reference/sensormedics-3100a-manual.txt`, which is
**gitignored** — it is a third-party copyrighted manual, kept locally rather than redistributed. If
it is missing, re-fetch from
<https://documents.cdn.ifixit.com/MNibDr4xbBxuZJrE.pdf> and run `pdftotext -layout`. Everything
relied on below is already summarised here, so the file is a convenience, not a dependency.

**The architecture is already a shipping clinical device**, and the manual describes it as
*"very similar to a permanent magnet speaker"* — a linear motor whose coil is *"suspended by
'spiders' within the permanent magnet"*, with no physical contact, driving a diaphragm-sealed
piston. That is a loudspeaker with a sealed piston instead of a cone. **The MVP's speaker is not an
approximation of this device; it is the same machine.**

Verified specifications:

| Parameter | Value |
|---|---|
| Frequency | 3-15 Hz |
| % inspiratory time | 30-50% of cycle |
| delta-P at 100% power | > 90 cmH2O **peak-to-peak** (~66 mmHg p-p, i.e. +/-33 mmHg) at the wye |
| Max piston stroke | ~365 mL, **stop-to-stop, i.e. peak-to-peak** |
| Piston transit time | *"only a matter of milliseconds"* — no figure published |
| Drive waveform | Square wave; piston slams between mechanical stops, not sinusoidal |
| Position feedback | Infrared sensor tracking piston head |
| Cooling | **60 LPM forced air** over the coil; thermal cutout at **190 degC** coil temperature |
| Life | >4000 hours |

**Measured performance** (read off Appendix B graphs, PDF pages 88 and 90 of the manual):

Distal/proximal delta-P ratio — how much of the machine's pressure actually reaches the patient
(Fig B.3, C = 1.02 mL/cmH2O, 50% I-time):

| ET tube | at 3 Hz | at 15 Hz |
|---|---|---|
| 3.5 mm | 0.60 | 0.16 |
| 3.0 mm | 0.44 | 0.10 |
| 2.5 mm | 0.26 | 0.065 |

Distal tidal volume at maximum power (Fig B.1, 3.0 mm ETT, C = 1.02 mL/cmH2O):

| I-time | at 3 Hz | at 15 Hz |
|---|---|---|
| 50% | ~48 mL | ~11 mL |
| 33% | ~41 mL | ~10 mL |

**So 365 mL of piston travel delivers only 10-48 mL of tidal volume.** The rest is absorbed by
circuit compliance and ET tube resistance. Bias flow (separate from the oscillation) is 0-40 LPM
continuous.

**Transit time, bounded.** No rise time is published. But the manual states amplitude is attenuated
at high frequency by *"slew rate limiting (the transit time of the piston is greater than the cycle
time required by the Frequency adjustment)"*. At 15 Hz / 30% I-time the inspiratory phase is ~20 ms,
so full-stroke transit must be **roughly 20-45 ms** — if it were ~5 ms, slew limiting would never
appear in the 3-15 Hz band. A 20 mmHg swing is only ~30% of full amplitude, so scales to
**~5-20 ms** in its own patient circuit.

**Critical caveat: that number does not transfer.** Response time is a property of actuator *plus
load*. The 3100A drives a few hundred mL of compliant circuit plus a neonatal lung. A rigid 45 L
chamber is a completely different load.

**The 3100A oscillator is too small for the leg chamber.** 365 mL p-p into 45 L gives only:

- 6.2 mmHg p-p isothermal (n=1.0)
- 8.6 mmHg p-p adiabatic (n=1.4)

i.e. **+/-3.1 to +/-4.3 mmHg — about 2.5-3x short of the +/-10 mmHg target.** Full-scale needs
roughly 1 L of swept volume, not 365 mL. Harvesting a decommissioned unit would not solve the
problem even ignoring cost.

**Corroborates the thermal warning.** A purpose-built clinical oscillator at this duty needs 60 LPM
of forced air cooling and a 190 degC cutout. Any sustained-duty rig here will need active cooling
too.

It is *not* prior art for the leg chamber concept — it oscillates a small compliant lung through an
ET tube, not a rigid volume around a limb.

## Sourcing conclusion: no off-the-shelf sealed voice coil (verified 2026-09)

Checked Moticont, H2W, Geeplus, and the Chinese AliExpress suppliers. The finding is consistent:

- **Guided voice coil actuators do exist** — housing, shaft, integrated linear bearings. Moticont
  GVCM series (to ~284 N continuous); H2W NCM series.
- **None of them are sealed.** No catalogue model from any of these makers includes a piston,
  diaphragm, or gas seal. They give you a shaft, not a pump.
- **All are quote-only**, no published pricing, no online purchase. Industrial pricing, out of scope
  for a home project budget.
- Voice-coil-driven sealed pumps appear only in **patents** (WO2015148833A1 "Voice coil activated
  pump"; US6138458, voice coil + rolling diaphragm + sealed air chamber) — custom OEM designs.

**Therefore a loudspeaker driver is the off-the-shelf version of the assembly**: voice coil motor +
rigid piston (cone) + flexible gas seal (surround) + centring/linear guide (spider). Same
architecture as the 3100A and the patents, mass-produced for ~AU$40. This is the correct engineering
choice for MVP 1, not a compromise. Precedent: forced oscillation technique / impulse oscillometry
have used loudspeakers as calibrated pressure sources in respiratory medicine since the 1950s.

**Phase-2 actuator candidate** — H2W `NCM08-25-100-2LB`: 19.1 mm stroke, 45 N continuous / 134 N
peak, 62.2 mm dia x 111 mm, 460 g moving mass, 10.4 ohm, 5.1 mH, Kf 30.9 N/A, integrated
recirculating ball bushing. Paired with a ~200 mm rolling diaphragm that is ~600 mL swept volume.
Force budget checks out: ~42 N pressure + ~29 N inertia = ~71 N against 134 N peak. Price on
application.

## Diaphragms are a buyable commodity — do not fabricate (verified 2026-09)

Ranked, cheapest and easiest first:

1. **Speaker passive radiator** — the best answer. A complete assembly: rigid cone/plate + rubber
   rolling surround + steel frame with bolt holes, and *no motor*. Bolt an actuator shaft to the
   centre and it is exactly the "piston + rolling seal + flange" needed. Sold in 5/6.5/8/10/12/15".
   - 5/6.5/8" — AU$12.09, [item 1005009240138696](https://www.aliexpress.com/item/1005009240138696.html)
   - ZIZI 8" — AU$14.29, [item 1005008908826504](https://www.aliexpress.com/item/1005008908826504.html)
   - MW Audio 8/10/12/15", steel basket — AU$61.99, [item 1005012375218450](https://www.aliexpress.com/item/1005012375218450.html)

   Two caveats: most passive radiators have a surround but **no spider**, so they do not self-centre
   axially — fine when the driving actuator has its own bearing (the H2W does), not fine with a bare
   VCM. And some have flimsy plastic cones; at ~42 N distributed load pick a stiff flat-plate or
   steel-basket type, or bond a printed stiffener to the back.

2. **Speaker surround ring on its own** + a printed piston disc — dirt cheap and lets you pick the
   piston diameter exactly. 4-12" sizes, AU$3.72-4.25 for a pair:
   [item 1005009719454580](https://www.aliexpress.com/item/1005009719454580.html),
   [item 1005008524449095](https://www.aliexpress.com/item/1005008524449095.html)

3. **Bellofram rolling diaphragm** — the proper industrial part. Standard bores from 0.25" to over
   8", published stroke/bore design tables. US supplier (Marsh Bellofram), quote-only with likely
   minimum orders. Correct but overkill for a bench rig.

4. **Fabricate from latex sheet** — only if nothing above fits the geometry.

AliExpress has no Bellofram-style rolling diaphragms in useful sizes; searching returns carburettor
diaphragms and pump repair kits.

## Who the user is, and how to pitch things

**The user is a software developer.** They have a 3D printer and are very proficient at CAD. They are
**not** an electronics engineer and **not** a mechanical engineer, and have said so explicitly.

Pitch accordingly:

- **Software and firmware:** talk to them as a peer. No hand-holding on architecture, language
  choice, data structures, debugging, or tooling.
- **CAD and 3D printing:** peer level. Describe *what* a part must do and the constraints it must
  meet; don't walk them through modelling it.
- **Electronics:** explain from first principles. Spell out every term on first use — H-bridge, PWM,
  back-EMF, DC-coupled, current limiting. Say *why* a component is needed, not just which one to buy.
  Give exact part numbers and wiring, since "any suitable driver" is not actionable for them.
- **Mechanical / physics / pneumatics:** same. Define the symbols (`Sd`, `Xmax`, `Fs`, `Re`, `BL`,
  polytropic index `n`). Show the arithmetic rather than asserting a result.
- **Physiology and medicine:** unknown competence — do not assume either way. An earlier version of
  this file claimed the user was medically trained; that was an unverified inference from an email
  domain and pasted AI-generated text, and should not be relied on. Ask if it matters.

Avoid jargon-as-shorthand generally. If a term genuinely earns its place, define it inline the first
time and keep using it — don't substitute vaguer words, and don't over-simplify the engineering
itself. The goal is accessible language around rigorous content, not softer content.

## Project context

This is a **home project**, not a commercial or regulated programme. No patent has been filed and the
user has explicitly deprioritised that; don't gate work on IP concerns unless they raise it.
