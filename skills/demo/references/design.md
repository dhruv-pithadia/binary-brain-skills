# Warm paper explainer recipe

Use this direction when the user wants the linked style or supplies no other brand. Keep the content, claims and cartoon character original.

- Portrait master: 1080×1920, 30fps. Draft: 540×960 with every layout dimension scaled consistently, not smaller text in the same canvas.
- Palette: warm paper #EBE7E1, ink #1E1C1A, red #D7372C, grey #8A857E, cards #FBFAF8. Verify contrast for small text; the palette is not an accessibility guarantee.
- Cards: an ink outline, moderate rounded corners and a restrained halftone offset instead of a soft glow. Search the existing registry for the treatment before implementing it. Fine static grain is optional and must not inflate render cost.
- Type: a condensed display face for short titles, a readable sans for captions, a restrained italic serif for a key word, and mono for small labels. The reference families are Anton, Instrument Sans, Instrument Serif and JetBrains Mono; use local licensed files or available alternatives and disclose substitutions. Avoid network font loads during rendering.
- Captions: top-left by default, a few spoken words per line, with one meaningful emphasis. Reserve platform-safe areas and measure actual text bounds. Avoid pale text on cream if it fails readability. Normal block flow preserves spaces; use a measured caption layout rather than relying on whitespace between flex items.
- Presenter: original flat-color SVG, chest-up in a bottom corner, around one-third of the frame where possible. The reference's large lower-right presenter may obscure content; fit it around the lesson instead of copying coordinates blindly. Separate facial and hand groups allow gestures without image generation or a 3D rig.
- Motion: cards may pop over about 0.3s, rise about 0.4s, or exit over about 0.2s. Stamp or underline emphasis belongs to a spoken idea. A short stagger can introduce a small set; avoid every scene using every effect.
- Structure: problem and promised payoff, a sequence of points and concrete demonstrations, then a closing payoff. A title need not be repeated as a paragraph. Match demos to the explanation rather than dropping generic terminals into every topic.
- Rig timing: seeded blinks around every 2.4–4.2 seconds, a roughly 0.14s blink, subtle head motion, and brief pointing/open-palm gestures for important transitions. Keep amplitude animation and gestures deterministic at any seek time. Do not overlap so many movements that the lesson becomes hard to read.
- Sound: restrained matching SFX, a quiet optional music bed and clearly dominant narration. A deliberate quiet moment is valid. Do not imply fixed fader values produce a target LUFS.

Keep static states readable and minimize decoration. Large numerals, badges and counters require truthful values and a real explanation. Staging a new scene needs a clear reason; seven points in thirty seconds may be too dense, so shorten the script rather than race the voice.
