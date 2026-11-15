---
name: dots-pepe
description: Makes a remixed pixel-art Pepe image from a fixed base image (Pepe in a blue t-shirt, pale lavender background, no hands). Keeps the face shape, pose and framing exactly the same and changes only the outfit, hand (held item or gesture), background and facial expression. Always use this skill for requests like "change Pepe's clothes", "Pepe holding X", "put Pepe on a Y background", "draw a X Pepe", "crying Pepe", "grinning Pepe", "Pepe remix", or Korean requests such as "페페 옷 바꿔줘", "OO 페페 그려줘", "울고 있는 페페", "페페 리믹스". Use it even when the user names only one of the four slots, or only a concept such as "pirate Pepe".
---

# dots-pepe

Base image: `assets/pepe_base.png` (512x512 pixel art).
It shows Pepe from the chest up in a blue t-shirt on a flat pale lavender background. **No hands are visible** (both arms hang down and are cropped by the bottom edge).
The **face shape, body, framing and art style** of this image are fixed. Only four slots change: **outfit / hand / background / expression**.

## Why the base image must always be attached

Text prompts alone produce a different Pepe every time. The most reliable way to keep the face and framing is to pass `assets/pepe_base.png` to the image generator as a **reference image (edit mode)** and to split the prompt clearly into "keep this" and "change this".

## Workflow

1. Extract four slots from the user's request: `OUTFIT`, `HAND`, `BACKGROUND`, `EXPRESSION`.
   - `EXPRESSION` is picked from the "Expression texts" section (smirk / grin / disappointed / tears / sob / angry / scream). If not mentioned, use the default (smug smile).
   - `HAND` is one of three:
     - **None**: if hands are not mentioned, draw no hands (default).
     - **Held item**: a knife, ladle, microphone, glass...
     - **Gesture**: thumbs-up, peace sign, waving, pointing...
   - Slots the user did not mention keep their default. Never change them on your own.
   - If only a concept arrives ("pirate Pepe"), fill outfit and background to fit the concept. Add a hand only when there is an item that clearly belongs to the concept, and if you add one, tell the user in one line.
2. In the template below, fill `{HAND_LINE}` with the text for the chosen `HAND` type (see "Hand texts"). Fill `{FACE_LINE}` and `{FACE_END}` with the text for the chosen `EXPRESSION` (see "Expression texts").
3. Fill the template to build the final prompt. Write the prompt in English (image models follow English more accurately).
4. Generate the image. Claude has no image generation tool, so call the **Codex CLI (GPT image generation)**.
   1. Save the finished English prompt to `<name>_prompt.txt` in the current folder. `<name>` is the concept in lowercase English (e.g. `pepe_pirate`).
   2. Run the bundled script. Generation takes 1-3 minutes, so give the Bash call a timeout of 600000.
      ```bash
      bash <this skill folder>/scripts/generate.sh <name>_prompt.txt <name>
      ```
      The script attaches `assets/pepe_base.png` as the reference image, calls `codex exec`, and produces `<name>.png` (original size) and `<name>_512.png` (512x512).
   3. When the script finishes, `scripts/check_framing.py` runs automatically and prints PASS / WARN / SKIP. It measures head movement and enlargement from the position and width of the lips, and is skipped silently if PIL is missing. On WARN, consider regenerating. Even on PASS, compare by eye as described below. SKIP means the mouth is covered, so check by eye only. For images with a changed expression the mouth shape differs, so measure with `python3 scripts/check_framing.py <file> --expr` to widen the allowed range.
   4. Open `<name>_512.png` and compare it with the base image. If anything other than the expression changed in the face shape, or the character was enlarged or moved, strengthen the `KEEP` paragraph and generate once more as `<name>_v2`. The most common failure is the character being enlarged (especially with a hat or helmet), so never remove the numbers in the Framing line.
   5. If execution is blocked (permission denied, codex not installed, login expired), do not work around it. Give the user the prompt and tell them to attach the base image in the Codex app and generate it themselves.
   - By default, generate right away. If the user asks for "prompt only", skip step 4. Generating sends the base image and the prompt to OpenAI.

## Defaults (slots the user did not mention)

- OUTFIT: a plain bright blue crew-neck t-shirt
- HAND: none
- BACKGROUND: a plain flat pale lavender-gray background (#D4DAF2)
- EXPRESSION: default (smug smile)

## Prompt template

```
Edit the attached reference image. Keep the same pixel art Pepe the Frog character.

KEEP EXACTLY THE SAME:
- Pixel art style: crisp square pixels, about 128x128 pixel grid, dark 1-pixel outlines, flat limited palette, no anti-aliasing, no blur, no gradients except dithering.
- Face: {FACE_LINE}
- Framing: square 1:1, do NOT zoom in or move the character. The top of the head is at 17% from the top edge, the right edge of the head is at 87% of the image width, the left edge of the head is at about 38% of the width, and the bottom of the chin is at about 60% from the top.
- Body: upper body only, shoulders start right under the chin and fill the bottom of the image, torso turned slightly toward the right, cropped at the bottom edge.
- Any hat or helmet sits firmly ON the head, not above it: its lower edge overlaps and hides the top part of the head, with no gap and no background visible between the hat and the head. Hats and helmets are drawn at a fixed medium-large size: about 60% of the image width wide (the brim or shell reaching roughly from 20% to 80% of the width) and about 15% of the image height tall, extending a clear distance past both sides of the head. The face, eyes and lips keep exactly the same size and position no matter what hat or helmet is worn.

HAND:
{HAND_LINE}

CHANGE ONLY:
- Outfit: {OUTFIT}
- Background: {BACKGROUND}

Do not add text, watermarks, extra characters, or extra hands. {FACE_END}
```

For the default expression, use the default texts below for `{FACE_LINE}` and `{FACE_END}`.

## Expression texts (`{FACE_LINE}`, `{FACE_END}`)

Changing the expression never changes the head shape, size, tilt, position, eye size, lip color or outline style. Only the eyelids, pupils, mouth shape and tears change.

**Default (smug smile):**

`{FACE_LINE}`:
```
same green Pepe head, slightly tilted, three-quarter view, heavy half-closed smug eyelids, big black pupils with small white highlights, wide orange-brown lips (#C8783A tone) with a dark outline in a smug closed-mouth smile. Same face shape and expression, pixel for pixel as much as possible.
```
`{FACE_END}`:
```
Do not change the face shape or expression.
```

For the seven expressions below, replace `{FACE_LINE}` with the given text and use the same `{FACE_END}` for all of them: `Do not change the head shape, size, position or tilt. Only the facial expression described above changes.`

**Smirk (only the mouth corners lifted slightly):** user-approved version. Everything except the mouth corners stays identical to the default face. Glancing sideways, raising an eyebrow or widening the mouth makes Pepe far too smug, so do not add them.
```
exactly the same face as the reference image, pixel for pixel: same green Pepe head shape, size, position and slight tilt, same heavy half-closed eyelids, same eye direction and big black pupils with small white highlights, same eyebrows, same wide orange-brown lips (#C8783A tone) with the same dark outline and same lip shape. The ONLY change: the two outer corners of the closed mouth are lifted up by just one or two pixels, a very subtle hint of a smile. Do not widen the mouth, do not add cheek creases, do not raise any eyebrow, do not change the eyes.
```

**Grin (big bright smile):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: a big, bright, wide-open happy grin. The mouth is wide open in a big smile showing a dark mouth interior and a small pink tongue, the eyes open wide and bright with raised cheeks, no heavy sleepy eyelids.
```

**Disappointed (let down):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: disappointed and let down. Mouth closed with the lip corners turned downward into a flat frown, the eyelids drooping heavily, the inner ends of the brows slanted up sadly, the pupils looking down and to the side. No tears.
```

**Tears (silently crying):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: silently crying. Mouth closed with the lips pressed together and the corners trembling slightly downward, the eyes glassy and watery with sad drooping eyelids, and two thin light-blue pixel tear streams running down from the eyes along the cheeks. No open mouth, no sobbing.
```

**Sob (wailing):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: sobbing uncontrollably. The mouth is wide open in a loud wail showing a dark mouth interior, the eyes squeezed tightly shut with scrunched brows, and thick light-blue pixel tear streams pouring down both cheeks with a few tear drops flying off the face.
```

**Angry:**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: furious anger. Thick dark brows slanted sharply downward toward the center of the face, the eyelids narrowed into a hard glare with the pupils staring forward, a few small red anger vein marks on the forehead, and the mouth closed with the lips pressed tight and the corners pulled sharply downward into a hard scowl.
```

**Scream (roaring in rage):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: screaming at the top of his lungs in rage. The mouth is stretched wide open in a loud roar showing a dark mouth interior, the eyes wide and bulging with tiny pupils, thick dark brows slanted sharply downward, red anger vein marks on the forehead, and a few small spit droplets and short motion lines near the mouth.
```

**Expression set (several expressions at once):** when the user says "all expressions", "an expression set" or "in several expressions", use `generate_set.py`. First build the default-expression prompt (`<name>_prompt.txt`). The script then keeps outfit, hand and background unchanged, swaps only the `- Face:` line, generates 7 images in parallel and checks the framing of each. The expression texts live in `scripts/expressions.json` (the same content as above). If you change a text, change it in both places.
```bash
python3 <this skill folder>/scripts/generate_set.py <name>_prompt.txt <name> [smirk grin disappointed tears sob angry scream]
```
Omit the expression keys for all 7, or list only some to make just those. Results are `<name>_<key>_512.png`. Seven parallel images use a lot of Codex quota, so use this only when the user wants several expressions.

Expression notes:
- Expressions with big tears or a big open mouth (grin, sob) tend to make the head larger or move it. After generating, always check that the Framing numbers (head top 17%, right edge 87%, chin 60%) still hold.
- A full-face mask hides the expression. In that case ignore the expression slot and tell the user in one line.
- Use only as much expression intensity as the user asked for. Adding glances, raised brows or a wider mouth on your own makes Pepe far too smug. When a request says "stronger" or "weaker", change only the needed part and keep the rest of the face at default (the smirk text is the example).

## Hand texts (`{HAND_LINE}`)

**None (default):**
```
- No hands are visible. Both arms hang down at the sides and are cropped off by the bottom edge. Nothing is held.
```

**Held item:** the hand is drawn in one place only, the lower left of the frame. The position is the same whatever the item's shape.
```
- Add exactly one hand: his right hand (viewer's left side) raised in a loose fist in front of the chest at the lower-left of the frame (the fist sits around 8-35% of the width and 55-85% of the height), holding {ITEM} up beside his face, {GRIP}. The other arm stays down out of frame.
```
How to choose `{GRIP}`:
- Items with a handle (knife, microphone, torch, flag): `gripped by the handle with the top pointing up-left`
- Cylinders (telescope, bottle): `gripped around its middle with the top end pointing up-left`
- Flat items (smartphone, card, book): `held between the fingers facing the viewer`
- Glasses: `held by the stem`
- Shrink large items to about the size of a glass so they fit inside the left edge of the frame. Make two-handed items (guitar, large flag) small enough for one hand, or have him grip the neck.

**Gesture:**
```
- Add exactly one hand: his right hand (viewer's left side) raised in front of the chest at the lower-left of the frame (around 8-35% of the width and 55-85% of the height). Gesture: {GESTURE}. Nothing is held. The other arm stays down out of frame.
```
`{GESTURE}` examples:
- Thumbs-up: `an empty fist giving a thumbs-up, thumb pointing straight up`
- Peace sign: `a peace sign with the index and middle fingers raised in a V, palm facing the viewer`
- Waving: `an open hand with the palm facing the viewer and fingers spread, waving hello`
- Pointing: `a fist with the index finger pointing up-left`
- Salute: the hand has to reach the forehead, which conflicts with the fixed hand position. If requested, say so in one line and suggest another gesture such as a thumbs-up at the same position.


### When a full-face mask is worn

Replace the last sentence of `{FACE_LINE}` (`Same face shape and expression, ...`) with this (ignore the expression slot):
```
EXCEPTION: he now wears a full mask that covers the whole face (see Outfit). That is intended: the eyes and lips are hidden. Keep the same head size, position and tilt. Green Pepe skin must clearly show between the mask's straps, around the mask edges and at the sides of the head, so the character is unmistakably the same green frog.
```
Change `{FACE_END}` to `Do not change the head size or position.`

Write the mask part of the outfit like this:
```
On his face he wears {MASK}, covering the entire face from the forehead to the chin, fastened with two or three leather straps wrapped around the green head, with green skin visible between the straps.
```
With a mask, keep the hand at the default (none). Having him hold some other item is fine.

## Output format

Give the user the following, in this order:

1. **What changes**, one line each: outfit / hand (none, item or gesture) / background / expression ("unchanged" for defaults)
2. The changed part of the prompt (one code block) and a link to the full prompt file
3. If generated: a link to `<name>_512.png` and one or two lines each on what is the same as and different from the base image.
   If not generated: one line saying "Be sure to attach the base image `pepe_base.png`."

## Example

**Input:** Make Pepe an astronaut holding a star-shaped lollipop, with space as the background

**What changes**
- Outfit: white astronaut spacesuit (no helmet)
- Hand: star-shaped lollipop
- Background: space with a planet and stars
- Expression: unchanged

```
HAND:
- Add exactly one hand: his right hand (viewer's left side) raised in a loose fist in front of the chest at the lower-left of the frame (the fist sits around 8-35% of the width and 55-85% of the height), holding a star-shaped yellow lollipop up beside his face, gripped by the stick with the star pointing up-left. The other arm stays down out of frame.

CHANGE ONLY:
- Outfit: a white astronaut spacesuit with an orange collar ring and small mission patches, no helmet so the face stays visible
- Background: dark outer space with a ringed purple planet, small pixel stars and a distant galaxy
```

## Uniform example: South Korean Army (from a reference photo, user-approved)

A case where only clothing details were copied from a reference photo. For the same request (an army soldier), use the `Outfit` text below as is (user-approved). Do not change details the photo did not show (such as the rank design). This version uses a coarse, chunky camouflage pattern and has all round buttons removed. Change the background as requested (e.g. a base gate at sunset).

```
- Outfit: a South Korean army enlisted soldier's combat uniform. On the head, a plain dark black-olive wool beret: a flat round soft cap with a matte felt-like surface, tilted slightly, with a thin black leather band around the bottom edge resting on the forehead just above the eyelids without covering the eyes. The whole face, eyes and lips stay fully visible at the same size. On the front-left of the beret (the viewer's right side of the beret front) sits a large, clearly drawn, detailed badge, about 11% of the image width wide and 10% of the image height tall, shaped like a tall arch (flat bottom, rounded top) with a dark forest-green felt backing and a thin teal outline. On the badge: two golden-yellow laurel leaf branches curving up the left and right sides like a wreath, a round gold-rimmed circle in the center containing a white ring around a red-and-blue yin-yang swirl, two tiny white flower dots at the top between the leaf tips, and a small white ribbon bow at the bottom where the branches meet. The badge must be crisp and recognizable even at this small size, drawn with bold shapes and few colors (green, gold, white, red, blue). On the body, a long-sleeved digital pixel camouflage field shirt with a coarse, rough camouflage pattern: large chunky square-pixel blocks (each block about twice as big as a normal pixel-camo block), jagged and irregular clumps of muted green, olive, tan-beige and dark brown with uneven, ragged edges and a few scattered single blocks, clearly rougher and blockier than a fine digital pattern, with a folded-down pointed collar, plain shoulder epaulettes with no buttons, a smooth flat front placket with a hidden closure, and two chest pockets with plain pointed flaps. There are NO round buttons anywhere on the shirt: no buttons on the front placket, none on the pocket flaps, none on the shoulder epaulettes; those areas are plain flat camouflage fabric. A short plain olive-green name tape with a thin dark border sits above the chest pocket on the viewer's left side of the frame, and a longer wide olive-green tape with a thin dark border sits above the chest pocket on the viewer's right side, above the pocket flap. The short tape on the left stays completely blank. The long tape has bold black pixel lettering in one line that reads exactly: 대한민국 육군 ROKA (Korean Hangul letters followed by the Latin letters R-O-K-A), large and evenly spaced, drawn in simple blocky pixel letters so every character is readable. On the pocket flap of the chest pocket on the viewer's right side of the frame (the soldier's left chest), placed at the LEFT end of that flap and not centered, directly below the 2nd and 3rd Hangul letters of the lettering on the long tape above it (the letters 한 and 민 of 대한민국), a small rank patch: a small rectangle of dark olive fabric with exactly two thin black horizontal bars stacked one above the other, nothing else on it, no chevrons. On the upper sleeve on the viewer's left side of the frame, a small rectangular patch showing a national flag design: a white field with a red and blue circle in the center and four black bar symbols in the corners. No other letters or readable text anywhere else in the image.
```

- Lessons from this case: describing a small emblem (the badge) only as "recognizable" makes it blurry. List its **size relative to the image (%)**, the shape of its backing and each component (branches, circle, flowers, ribbon) one by one, and tell the model to simplify with `bold shapes and few colors`.
- Left and right are easy to confuse. "Pepe's left" is the right side of the image, while "left as the viewer sees it" is the left side of the image. If it is unclear which the user means, do not decide on your own; ask once. In the prompt, write both frames, such as `the viewer's right side (the soldier's left)`, and add a visible anchor point such as "below a specific letter, at the left end of the pocket".
- Short text renders sharply. The long name tape "대한민국 육군 ROKA" came out readable with `reads exactly` and `simple blocky pixel letters`. The position of text (e.g. directly below a specific letter) may not be matched exactly.
- When the user says to remove something, as in "remove the buttons", list every place it must be absent, like `NO round buttons anywhere ... plain flat fabric`.
- Use a national flag only as a single sleeve patch, and only when the real uniform needs it. Keep `no national flags` for all other outfits.

## Notes

- The default size of hats and helmets is fixed at **about 60% of the image width and about 15% of the image height** (user-approved: based on the final navy cap). The template already states the size as numbers, so do not use words like `OVERSIZED` in the outfit text; describe only the shape of the hat. If the user wants a smaller or bigger hat, replace the 60%/15% in the template with new ratio numbers (e.g. "25% bigger" means 75% wide and 19% tall).
- Writing `sitting on top of the head` makes a hat float above the head. Write that it rests on the head, like `worn snugly on the head, its brim resting on the forehead just above the eyelids without covering the eyes`.
- Describe a helmet only by shape, like `a chunky helmet with a wide rounded shell`, and leave the size to the template numbers. Raise the visor and leave out any oxygen mask so the whole face shows. Always add `the whole face, eyes and lips stay fully visible at the same size` so the face does not grow with it.
- **A mask covers the whole face** (user decision). It is fine for the face to be hidden. Instead, let green skin show between the straps and at the mask edges so Pepe is still recognizable. Use the "When a full-face mask is worn" text.
- A helmet and sunglasses are not masks. Raise the helmet's visor, and push sunglasses up onto the forehead so the face stays visible.
- Do not draw the iconic mask, costume or logo of an existing film, game or comic character (heroes etc.) as is, even for personal use. If such a request arrives, say so in one line and draw a new design that only keeps the mood. Using the original color scheme, patterns or logo as is can also be blocked by the image safety filter (`moderation_blocked`). If blocked, do not work around it; redo it once as an original design without the original elements.
- Unless the outfit really needs a flag (such as a real national military uniform), put `no national flags or country insignia` in the outfit text. Without it, stray flag patches tend to appear.
- For props that could carry writing (hat ribbons, name tags), letters come out garbled, so add `no letters or readable text`.
- For clothing whose exact shape matters, such as real military uniforms and other uniforms, text searches alone cannot confirm the details (cap band and anchor, rank insignia, batons, etc.). Ask the user for reference photos and copy into the prompt only the clothing details visible in the photo (hat shape, positions of pockets, name tags and rank, sleeve length). Do not mention the person in the photo or draw their face. Do not assert unverified details; tell the user they were "not confirmed".
- Wording like "smaller" or "a bit bigger" barely moves hat size. State the current hat width and height as percentages of the image and instruct with numbers, such as "25% bigger". It is still not exact, so measure the result. The bigger the hat, the more the head tends to grow or shift with it, so compare against the Framing numbers.
- For branded props such as energy drink cans, writing only "no logo" can still produce a real logo shape (e.g. an M, claw marks). Remove all decoration and say the whole surface is plain, like `a completely plain, solid matte black cylinder ... no pattern, no stripes, no logo, no emblem, no letters`.
