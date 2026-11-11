# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 22:55
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_297427c4b488` | human | 0.319 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_e1b34cd4d501` | unsure | 0.424 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_745c570fa858` | unsure | 0.491 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_b31f782dbe87` | unsure | 0.539 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_e5312b6a7e29` | human | 0.239 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_ae07c73c9521` | unsure | 0.427 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_1371150d20d8` | unsure | 0.498 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_d036d5a8e556` | unsure | 0.377 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_3390143fbe29` | unsure | 0.487 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_cf38892d2cb4` | ai | 0.827 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_10d63d169a64` | unsure | 0.523 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_231cea17b408` | ai | 0.657 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_7dc6f20d9b1f` | ai | 0.691 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_80acfa87d01a` | unsure | 0.649 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_2cbc3431e14d` | ai | 0.666 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_0975084029cb` | unsure | 0.641 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_92fb53492ef3` | unsure | 0.627 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_5b97fcd1d869` | unsure | 0.374 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_f4611950d625` | unsure | 0.409 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_422d131daf32` | human | 0.184 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_b7e08461b92f` | unsure | 0.437 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_4d025f1f01fc` | human | 0.333 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_2db61267213b` | unsure | 0.361 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_379c7469a958` | unsure | 0.501 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c_1548970cd887` | human | 0.333 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_af3a45959169` | unsure | 0.506 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_3a427603d9f1` | ai | 0.832 |  |
| MF06 | malformed | text is emoji only | 200 | `c_f56727e80b02` | ai | 0.999 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_c2e21beca98a` | ai | 0.953 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_b0509d82a712` | unsure | 0.453 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_98fda0071149` | unsure | 0.358 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_2b3eb76001b6` | human | 0.348 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_529a55b3b22d` | human | 0.348 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_fb193bd94717` | human | 0.348 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_c231c757e162` | human | 0.348 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_9a5313a5e83f` | human | 0.348 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_297427c4b488",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3185,
  "model_score": 0.1635,
  "style_score": 0.4734,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_e1b34cd4d501",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4244,
  "model_score": 0.5943,
  "style_score": 0.2546,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_745c570fa858",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4914,
  "model_score": 0.6662,
  "style_score": 0.3166,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_b31f782dbe87",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5393,
  "model_score": 0.6114,
  "style_score": 0.4673,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_e5312b6a7e29",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2389,
  "model_score": 0.3212,
  "style_score": 0.1565,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_ae07c73c9521",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4267,
  "model_score": 0.5727,
  "style_score": 0.2808,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_1371150d20d8",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4976,
  "model_score": 0.5862,
  "style_score": 0.4089,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_d036d5a8e556",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3773,
  "model_score": 0.2452,
  "style_score": 0.5095,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_3390143fbe29",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4873,
  "model_score": 0.7042,
  "style_score": 0.2703,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_cf38892d2cb4",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8267,
  "model_score": 0.9792,
  "style_score": 0.6743,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_10d63d169a64",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5231,
  "model_score": 0.6175,
  "style_score": 0.4287,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_231cea17b408",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6567,
  "model_score": 0.7387,
  "style_score": 0.5748,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_7dc6f20d9b1f",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6909,
  "model_score": 0.8051,
  "style_score": 0.5767,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_80acfa87d01a",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6492,
  "model_score": 0.8329,
  "style_score": 0.4654,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_2cbc3431e14d",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6662,
  "model_score": 0.8005,
  "style_score": 0.5319,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_0975084029cb",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6415,
  "model_score": 0.8814,
  "style_score": 0.4017,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_92fb53492ef3",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6273,
  "model_score": 0.8816,
  "style_score": 0.3729,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_5b97fcd1d869",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3742,
  "model_score": 0.3223,
  "style_score": 0.4261,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_f4611950d625",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4091,
  "model_score": 0.4625,
  "style_score": 0.3556,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_422d131daf32",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1837,
  "model_score": 0.2044,
  "style_score": 0.163,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_b7e08461b92f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4367,
  "model_score": 0.5943,
  "style_score": 0.2791,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_4d025f1f01fc",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.3325,
  "model_score": 0.4998,
  "style_score": 0.1652,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_2db61267213b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3614,
  "model_score": 0.6401,
  "style_score": 0.0826,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_379c7469a958",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5006,
  "model_score": 0.5583,
  "style_score": 0.4428,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_1548970cd887",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.3333,
  "model_score": 0.0,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_af3a45959169",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5056,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_3a427603d9f1",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321,
  "model_score": 0.9976,
  "style_score": 0.6667,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_f56727e80b02",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9985,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_c2e21beca98a",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_b0509d82a712",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.4531,
  "model_score": 0.2395,
  "style_score": 0.6667,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_98fda0071149",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.3579,
  "model_score": 0.0492,
  "style_score": 0.6667,
  "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_2b3eb76001b6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3477,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_529a55b3b22d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3477,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_fb193bd94717",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3477,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_c231c757e162",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3477,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_9a5313a5e83f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3477,
  "model_score": 0.0287,
  "style_score": 0.6667,
  "label": "Your sample was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
