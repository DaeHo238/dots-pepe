---
name: dots-pepe
description: 기준 픽셀아트 Pepe(파란 티셔츠, 연보라 배경, 손 없음)의 얼굴 모양·자세·구도는 그대로 두고 옷, 손(든 물건 또는 손동작), 배경, 표정만 바꾼 이미지를 만든다. "페페 옷 바꿔줘", "페페가 OO 들고 있게", "배경을 OO로", "OO 페페 그려줘", "울고 있는 페페", "활짝 웃는 페페", "페페 리믹스" 같은 요청이면 반드시 이 스킬을 사용한다. 사용자가 네 가지 중 하나만 말해도, 혹은 "해적 페페"처럼 컨셉만 말해도 사용한다.
---

# dots-pepe

기준 이미지: `assets/pepe_base.png` (512x512 픽셀아트).
파란 티셔츠를 입은 Pepe 상반신, 연보라 단색 배경, **손은 보이지 않는다**(양팔이 아래로 내려가 화면 밖).
이 이미지의 **얼굴 모양·몸·구도·화풍**은 고정하고, **옷 / 손 / 배경 / 표정** 네 칸만 바꾼다.

## 왜 기준 이미지를 꼭 첨부하나

텍스트 프롬프트만으로는 매번 다른 Pepe가 나온다. 얼굴과 구도를 지키는 가장 확실한 방법은 이미지 생성 도구에 `assets/pepe_base.png`를 **참조 이미지(편집 모드)**로 넣고, 프롬프트로는 "바꿀 것"과 "지킬 것"을 분명히 나눠 말하는 것이다.

## 작업 순서

1. 사용자 요청에서 네 칸을 뽑는다: `OUTFIT`, `HAND`, `BACKGROUND`, `EXPRESSION`.
   - `EXPRESSION`은 "표정 문구" 표에서 고른다 (씨익 / 활짝 / 실망 / 눈물만 / 오열 / 분노 / 소리침). 말하지 않으면 기본(느끼한 미소)이다.
   - `HAND`는 셋 중 하나다:
     - **없음**: 손 얘기가 없으면 손을 그리지 않는다 (기본값).
     - **든 물건**: 칼, 국자, 마이크, 잔…
     - **손동작**: 엄지 척, 브이, 손 흔들기, 가리키기…
   - 말하지 않은 칸은 기본값을 유지한다. 임의로 바꾸지 않는다.
   - "해적 페페"처럼 컨셉만 오면 옷과 배경은 컨셉에 맞게 채운다. 손은 컨셉에 꼭 어울리는 물건이 있을 때만 넣고, 넣었다면 사용자에게 한 줄로 알린다.
2. 아래 템플릿의 `{HAND_LINE}`을 `HAND` 종류에 맞는 문구로 채운다 ("손 문구" 참고). `{FACE_LINE}`과 `{FACE_END}`는 `EXPRESSION`에 맞는 문구로 채운다 ("표정 문구" 참고).
3. 템플릿을 채워 최종 프롬프트를 만든다. 프롬프트는 영어로 쓴다(이미지 모델이 영어를 더 정확히 따른다).
4. 이미지를 생성한다. Claude에는 이미지 생성 도구가 없으므로 **Codex CLI(GPT 이미지 생성)**를 호출한다.
   1. 완성한 영어 프롬프트를 현재 폴더의 `<이름>_prompt.txt`에 저장한다. `<이름>`은 컨셉을 영어 소문자로 쓴다 (예: `pepe_pirate`).
   2. 번들 스크립트를 실행한다. 생성에 1~3분 걸리므로 Bash timeout을 600000으로 준다.
      ```bash
      bash <이 스킬 폴더>/scripts/generate.sh <이름>_prompt.txt <이름>
      ```
      스크립트는 `assets/pepe_base.png`를 참조 이미지로 첨부해 `codex exec`를 호출하고, `<이름>.png`(원본 크기)와 `<이름>_512.png`(512x512)를 만든다.
   3. `<이름>_512.png`를 열어 기준 이미지와 비교한다. 표정 외에 얼굴 모양이 바뀌었거나 캐릭터가 확대·이동했으면 `KEEP` 문단을 더 강하게 고쳐 `<이름>_v2`로 한 번 더 생성한다. 가장 흔한 실패는 캐릭터 확대(특히 모자·헬멧이 있을 때)이므로 Framing 줄의 수치는 빼지 않는다.
   4. 실행이 막히면(권한 거부, codex 미설치, 로그인 만료) 우회하지 말고, 프롬프트를 주며 사용자가 Codex 앱에서 기준 이미지를 첨부해 직접 생성하도록 안내한다.
   - 기본은 바로 생성한다. 사용자가 "프롬프트만" 달라고 하면 4단계를 건너뛴다. 생성할 때 기준 이미지와 프롬프트가 OpenAI로 전송된다.

## 기본값 (말하지 않은 칸)

- OUTFIT: a plain bright blue crew-neck t-shirt
- HAND: 없음
- BACKGROUND: a plain flat pale lavender-gray background (#D4DAF2)
- EXPRESSION: 기본 (느끼한 미소)

## 프롬프트 템플릿

```
Edit the attached reference image. Keep the same pixel art Pepe the Frog character.

KEEP EXACTLY THE SAME:
- Pixel art style: crisp square pixels, about 128x128 pixel grid, dark 1-pixel outlines, flat limited palette, no anti-aliasing, no blur, no gradients except dithering.
- Face: {FACE_LINE}
- Framing: square 1:1, do NOT zoom in or move the character. The top of the head is at 17% from the top edge, the right edge of the head is at 87% of the image width, the left edge of the head is at about 38% of the width, and the bottom of the chin is at about 60% from the top.
- Body: upper body only, shoulders start right under the chin and fill the bottom of the image, torso turned slightly toward the right, cropped at the bottom edge.
- Any hat or helmet sits firmly ON the head, not above it: its lower edge overlaps and hides the top part of the head, with no gap and no background visible between the hat and the head. Hats and helmets are drawn OVERSIZED: noticeably big, extending past both sides of the head and rising high into the background. The face, eyes and lips keep exactly the same size and position no matter how big the hat or helmet is.

HAND:
{HAND_LINE}

CHANGE ONLY:
- Outfit: {OUTFIT}
- Background: {BACKGROUND}

Do not add text, watermarks, extra characters, or extra hands. {FACE_END}
```

기본 표정이면 `{FACE_LINE}`과 `{FACE_END}`는 아래 기본 문구를 쓴다.

## 표정 문구 (`{FACE_LINE}`, `{FACE_END}`)

표정을 바꿔도 머리 모양·크기·기울기·위치, 눈 크기, 입술 색과 외곽선 화풍은 그대로다. 바뀌는 건 눈꺼풀·눈동자·입 모양·눈물뿐이다.

**기본 (느끼한 미소):**

`{FACE_LINE}`:
```
same green Pepe head, slightly tilted, three-quarter view, heavy half-closed smug eyelids, big black pupils with small white highlights, wide orange-brown lips (#C8783A tone) with a dark outline in a smug closed-mouth smile. Same face shape and expression, pixel for pixel as much as possible.
```
`{FACE_END}`:
```
Do not change the face shape or expression.
```

아래 일곱 가지는 `{FACE_LINE}`을 이 문구로 바꾸고, `{FACE_END}`는 모두 똑같이 `Do not change the head shape, size, position or tilt. Only the facial expression described above changes.`로 쓴다.

**씨익 (입꼬리만 살짝 올라간 웃음):** 사용자 확정 버전. 입꼬리 외에는 기본 얼굴과 똑같이 둔다. 눈을 옆으로 흘기거나 눈썹을 올리거나 입을 넓히면 너무 느끼해지니 넣지 않는다.
```
exactly the same face as the reference image, pixel for pixel: same green Pepe head shape, size, position and slight tilt, same heavy half-closed eyelids, same eye direction and big black pupils with small white highlights, same eyebrows, same wide orange-brown lips (#C8783A tone) with the same dark outline and same lip shape. The ONLY change: the two outer corners of the closed mouth are lifted up by just one or two pixels, a very subtle hint of a smile. Do not widen the mouth, do not add cheek creases, do not raise any eyebrow, do not change the eyes.
```

**활짝 (환하게 웃음):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: a big, bright, wide-open happy grin. The mouth is wide open in a big smile showing a dark mouth interior and a small pink tongue, the eyes open wide and bright with raised cheeks, no heavy sleepy eyelids.
```

**실망 (시무룩):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: disappointed and let down. Mouth closed with the lip corners turned downward into a flat frown, the eyelids drooping heavily, the inner ends of the brows slanted up sadly, the pupils looking down and to the side. No tears.
```

**눈물만 (소리 없이 눈물 흘림):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: silently crying. Mouth closed with the lips pressed together and the corners trembling slightly downward, the eyes glassy and watery with sad drooping eyelids, and two thin light-blue pixel tear streams running down from the eyes along the cheeks. No open mouth, no sobbing.
```

**오열 (엉엉 욺):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: sobbing uncontrollably. The mouth is wide open in a loud wail showing a dark mouth interior, the eyes squeezed tightly shut with scrunched brows, and thick light-blue pixel tear streams pouring down both cheeks with a few tear drops flying off the face.
```

**분노 (화남):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same big black pupils with small white highlights, same wide orange-brown lips (#C8783A tone) with a dark outline. EXPRESSION: furious anger. Thick dark brows slanted sharply downward toward the center of the face, the eyelids narrowed into a hard glare with the pupils staring forward, a few small red anger vein marks on the forehead, and the mouth closed with the lips pressed tight and the corners pulled sharply downward into a hard scowl.
```

**소리침 (분노해서 고함):**
```
same green Pepe head shape, size, position and slight tilt, three-quarter view, same orange-brown lip color (#C8783A tone) with a dark outline. EXPRESSION: screaming at the top of his lungs in rage. The mouth is stretched wide open in a loud roar showing a dark mouth interior, the eyes wide and bulging with tiny pupils, thick dark brows slanted sharply downward, red anger vein marks on the forehead, and a few small spit droplets and short motion lines near the mouth.
```

표정 주의:
- 눈물과 입 모양이 큰 표정(활짝, 오열)은 머리가 커지거나 이동하기 쉽다. 생성 후 Framing 수치(머리 위 17%, 오른쪽 87%, 턱 60%)가 지켜졌는지 꼭 비교한다.
- 가면이 얼굴 전체를 덮으면 표정이 보이지 않는다. 그럴 땐 표정 칸을 무시하고 사용자에게 한 줄로 알린다.
- 표정 강도는 사용자가 말한 만큼만 쓴다. 눈 흘기기, 눈썹 올리기, 입 넓히기 같은 요소를 임의로 더하면 페페가 너무 느끼해진다. "더 세게/약하게" 요청이 오면 바꿀 부분만 고치고 나머지 얼굴은 기본 그대로 둔다 (씨익 문구가 그 예).

## 손 문구 (`{HAND_LINE}`)

**없음 (기본):**
```
- No hands are visible. Both arms hang down at the sides and are cropped off by the bottom edge. Nothing is held.
```

**든 물건:** 손은 화면 왼쪽 아래 한 곳에만 그린다. 물건 모양이 달라도 이 위치는 같다.
```
- Add exactly one hand: his right hand (viewer's left side) raised in a loose fist in front of the chest at the lower-left of the frame (the fist sits around 8-35% of the width and 55-85% of the height), holding {ITEM} up beside his face, {GRIP}. The other arm stays down out of frame.
```
`{GRIP}` 고르는 법:
- 손잡이 있는 물건(칼, 마이크, 횃불, 깃발): `gripped by the handle with the top pointing up-left`
- 원통형(망원경, 병): `gripped around its middle with the top end pointing up-left`
- 납작한 물건(스마트폰, 카드, 책): `held between the fingers facing the viewer`
- 잔 종류: `held by the stem`
- 큰 물건은 원래 잔 크기 정도로 줄여 화면 왼쪽 가장자리 안에 들어오게 한다. 두 손 물건(기타, 큰 깃발)은 한 손으로 쥘 수 있게 줄이거나 목 부분을 쥐게 한다.

**손동작:**
```
- Add exactly one hand: his right hand (viewer's left side) raised in front of the chest at the lower-left of the frame (around 8-35% of the width and 55-85% of the height). Gesture: {GESTURE}. Nothing is held. The other arm stays down out of frame.
```
`{GESTURE}` 예시:
- 엄지 척: `an empty fist giving a thumbs-up, thumb pointing straight up`
- 브이: `a peace sign with the index and middle fingers raised in a V, palm facing the viewer`
- 손 흔들기: `an open hand with the palm facing the viewer and fingers spread, waving hello`
- 가리키기: `a fist with the index finger pointing up-left`
- 경례: 손이 이마로 가야 해서 손 위치 고정과 충돌한다. 요청이 오면 그 사실을 한 줄로 알리고, 같은 위치에서 엄지 척 같은 다른 동작을 제안한다.


### 가면일 때 (얼굴 전체를 덮는 가면)

`{FACE_LINE}`의 끝 문장(`Same face shape and expression, ...`)을 이것으로 바꾼다 (표정 칸은 무시):
```
EXCEPTION: he now wears a full mask that covers the whole face (see Outfit). That is intended: the eyes and lips are hidden. Keep the same head size, position and tilt. Green Pepe skin must clearly show between the mask's straps, around the mask edges and at the sides of the head, so the character is unmistakably the same green frog.
```
`{FACE_END}`는 `Do not change the head size or position.`으로 바꾼다.

옷 문구의 가면 부분은 이렇게 쓴다:
```
On his face he wears {MASK}, covering the entire face from the forehead to the chin, fastened with two or three leather straps wrapped around the green head, with green skin visible between the straps.
```
가면을 쓰면 손은 기본값(없음)으로 둔다. 손에 다른 물건을 들게 하는 건 괜찮다.

## 출력 형식

사용자에게 이 순서로 준다:

1. **바뀌는 것** 한 줄씩: 옷 / 손(없음, 물건 또는 동작) / 배경 / 표정 (기본값이면 "기본 유지")
2. 프롬프트 중 바뀐 부분 (코드 블록 하나)과 전체 프롬프트 파일 링크
3. 생성했다면: `<이름>_512.png` 파일 링크와, 기준 이미지와 같은 점·다른 점을 한두 줄씩.
   생성하지 않았다면: "기준 이미지 `pepe_base.png`를 꼭 같이 첨부하세요." 한 줄 안내.

## 예시

**입력:** 페페를 우주비행사로 만들고 손에는 별 모양 막대사탕, 배경은 우주

**바뀌는 것**
- 옷: 흰 우주복 (헬멧 없음)
- 손: 별 모양 막대사탕
- 배경: 행성과 별이 있는 우주
- 표정: 기본 유지

```
HAND:
- Add exactly one hand: his right hand (viewer's left side) raised in a loose fist in front of the chest at the lower-left of the frame (the fist sits around 8-35% of the width and 55-85% of the height), holding a star-shaped yellow lollipop up beside his face, gripped by the stick with the star pointing up-left. The other arm stays down out of frame.

CHANGE ONLY:
- Outfit: a white astronaut spacesuit with an orange collar ring and small mission patches, no helmet so the face stays visible
- Background: dark outer space with a ringed purple planet, small pixel stars and a distant galaxy
```

## 주의

- 모자와 헬멧은 기본으로 **크게** 그린다 (사용자 취향). 옷 문구의 모자 앞에 `an OVERSIZED ... cap/hat, noticeably big, with a very wide, tall crown that extends well past both sides of the head` 같은 말을 붙인다. 사용자가 작은 모자를 원하면 템플릿의 `Hats are drawn OVERSIZED` 문장을 빼고 `the hat stays small`로 바꾼다.
- 모자는 `sitting on top of the head`라고 쓰면 머리 위로 붕 뜬다. `worn snugly on the head, its brim resting on the forehead just above the eyelids without covering the eyes`처럼 머리에 얹힌다고 쓴다.
- 헬멧은 `an OVERSIZED ... helmet, noticeably big and chunky, a wide rounded shell that extends well past both sides of the head and rises high above it`처럼 크게 쓰고, 바이저는 올리고 산소마스크는 빼서 얼굴이 다 보이게 한다. 얼굴이 같이 커지지 않도록 `the whole face, eyes and lips stay fully visible at the same size`를 꼭 붙인다.
- **가면은 얼굴 전체에 씌운다** (사용자 결정). 얼굴이 가려져도 괜찮다. 대신 가면을 고정하는 끈 사이와 가면 가장자리로 초록 피부가 보이게 해서 페페임을 드러낸다. 아래 "가면일 때" 문구를 쓴다.
- 헬멧과 선글라스는 가면이 아니다. 헬멧은 바이저를 올리고, 선글라스는 이마에 올려 얼굴이 보이게 한다.
- 실존 영화·게임·만화 캐릭터(히어로 등)는 상징적인 마스크·의상·로고를 그대로 넣지 않는다. 개인용이라고 해도 같다. 그런 요청이 오면 그 사실을 한 줄로 알리고, 분위기만 살린 새 디자인으로 그린다. 원작 색 배합·문양·로고를 그대로 쓰면 이미지 안전 필터(`moderation_blocked`)에 막히기도 한다. 막히면 우회하지 말고 원작 요소를 뺀 오리지널 디자인으로 한 번 다시 만든다.
- 실제 국가 군복처럼 국기가 필요한 게 아니면 `no national flags or country insignia`를 옷 문구에 넣는다. 안 넣으면 엉뚱한 국기 패치가 생기곤 한다.
- 글자가 들어갈 만한 소품(모자 리본, 명찰)은 글자가 깨져 나오므로 `no letters or readable text`를 덧붙인다.
- 에너지 음료 캔처럼 상표가 있는 소품은 "no logo"라고만 써도 실제 로고 모양(예: M자, 발톱 무늬)이 그려질 수 있다. 무늬를 아예 빼고 `a completely plain, solid matte black cylinder ... no pattern, no stripes, no logo, no emblem, no letters`처럼 표면 전체가 민무늬라고 쓴다.
