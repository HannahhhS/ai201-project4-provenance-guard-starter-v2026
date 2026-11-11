# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->


1. **Receive submission:** The service receives a `POST /submit` request containing the writer's text and `creator_id`.
2. **Validate input:** The service checks that the required fields are present and that the submitted text is usable.
3. **Run semantic detection:** The text is passed to `detector.py`, which uses a pretrained local model to analyze the text and produce a detection score.
4. **Analyze writing style:** The text is passed to `stylometry.py`, which measures writing characteristics such as sentence-length variation, word variety, and punctuation density.
5. **Combine signals:** The outputs from the semantic detector and stylometry analysis are passed to `scoring.py`, where `combine_signals` combines the two signals into an overall confidence score and guess.
6. **Assign a label and record the result:** The score is mapped to one of three plain-English labels: high-confidence AI, high-confidence human, or unsure. The service generates a `content_id` and records the decision in the audit log.
7. **Return the result and handle appeals:** The service returns the `content_id`, guess, confidence score, and label to the writer. If the writer disagrees, they can submit a `POST /appeal` request with the `content_id` and their reasoning. The service records the appeal and changes the item's status to `under_review` without automatically running detection again.  

### False Positive Trace

A false positive occurs when a human writer submits their own original work, but the system incorrectly classifies it as AI-generated.

1. **Submission:** A writer submits original work through `POST /submit`.
2. **Model signal:** The semantic detector identifies language patterns that resemble AI-generated text and produces a higher AI score.
3. **Style signal:** The stylometry analysis also detects consistent sentence lengths and predictable vocabulary, which contribute to an AI-like style score.
4. **Combined score:** The scoring system combines both signals and produces a score that falls into the high-confidence AI range.
5. **Incorrect label:** The writer receives a high-confidence AI label even though they wrote the text themselves.
6. **Appeal:** The writer submits `POST /appeal` with the content ID and an explanation that the work is original.
7. **Under review:** The service records the appeal and changes the item's status to `under_review`. The original detection result is preserved, and the system does not automatically run detection again.

### Endpoint Shapes

**POST /submit**

Accepts a JSON request containing:
- `text`: The content submitted by the writer.
- `creator_id`: The ID of the writer submitting the content.

Returns a JSON response containing:
- `content_id`: A unique identifier for the submission.
- `guess`: The system's prediction: `ai`, `human`, or `unsure`.
- `confidence`: The combined score, from 0.0 (confidently human) to 1.0 (confidently AI).
- `label`: A plain-English explanation of the result.
- `model_score`: The model signal's score (0–1, higher = more likely AI).
- `style_score`: The style signal's score (0–1, higher = more likely AI).

**POST /appeal**

Accepts a JSON request containing:
- `content_id`: The ID of the submission being appealed.
- `reasoning`: The writer's explanation for why they disagree with the result.

Returns a JSON response containing:
- `content_id`: The ID of the appealed submission.
- `status`: The updated status (`under_review`).
- `message`: Confirmation that the appeal was recorded.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**

How predictable the text is to a small language model (GPT-2), measured as perplexity. `detector.py::model_signal` turns perplexity into a 0–1 score: text the model finds easy to predict scores close to 1 (more likely AI), and text that surprises it scores close to 0 (more likely human).

**Why that might differ between human and AI writing:**

AI-generated writing can contain patterns that differ from natural human writing, such as predictable phrasing or consistent language patterns. The model attempts to recognize these differences based on patterns it learned during training.

**What it can't see:**

It cannot know who actually wrote the text or whether AI was used. It may incorrectly classify human writing that happens to resemble AI-generated writing, or AI-generated writing that has been heavily edited. Predictability isn't authorship: plain, formal, or step-by-step human writing is also very predictable. A paragraph from my own lab report scored 0.7080 on this signal, close to my clearly AI sample (0.7544).

### Signal two — the style signal

**What it measures:**

The style signal analyzes measurable writing characteristics, including sentence-length variation, word variety (unique words compared to total words), and punctuation density.

**Why that might differ between human and AI writing:**

Human writing often has natural variation in sentence length, vocabulary, and punctuation. AI-generated writing may have more consistent or predictable patterns, although this is not always the case.

**What it can't see:**

It cannot determine who wrote the text or understand its meaning and context. Human writers can have consistent writing styles, and AI-generated text can be edited to include more natural variation. These characteristics alone cannot reliably establish authorship.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

The combined score is an equal-weight average of the two signals. Both signals point the same way (higher = more likely AI), so the average does too. When the signals disagree, the score lands between them, which usually puts it in the unsure band. Neither signal can push a submission to a confident label on its own; a high-confidence label needs both signals to lean the same way.

**The numbers:**

- `combined = 0.5 × model_score + 0.5 × style_score` (weights in `config.py`)
- Style signal (`stylometry.py::style_signal`): an equal average of three measures, each scaled to 0–1 and flipped so higher means more AI:
  - sentence-length spread (std dev ÷ mean), capped at 1.2: low spread → more AI
  - type-token ratio (unique ÷ total words): low variety → more AI
  - punctuation density (`, ; : — ( )` per word), capped at 0.15: less punctuation → more AI
- The caps are heuristic choices from a handful of test samples, not established thresholds.
- Known limitation: type-token ratio falls as text gets longer, so longer submissions score more AI-like on the style signal regardless of who wrote them. A one-sentence submission also gets zero spread, which reads as AI-like.

Results on the four Milestone 4 inputs:

| Input | model_score | style_score | combined |
|---|---|---|---|
| Clearly AI | 0.7544 | 0.506 | 0.6302 |
| Clearly human | 0.4445 | 0.2293 | 0.3369 |
| Formal human (my lab report) | 0.5504 | 0.6574 | 0.6039 |
| Lightly edited AI | 0.3489 | 0.4081 | 0.3785 |

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

My formal human sample (a paragraph from a lab report I wrote) split the two signals. The style signal scored it 0.6574, leaning AI, because the paragraph is long (190 words, which lowers word variety), its sentences are fairly even in length, and it uses little punctuation. The model signal scored it 0.5504, close to the middle. The average was 0.6039, in the unsure band, so the style signal alone couldn't label my own writing as AI. It was a narrow result, though. A second paragraph from the same report scored 0.6834 combined (model 0.7080, style 0.6588), where both signals leaned AI, and it would be labelled high-confidence AI: a false positive on my own writing.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | Your sample was probably written by a human. |
| unsure | 0.35 – 0.65 | Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you. |
| high-confidence AI | 0.65 – 1.00 | This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The first sentence admits that the system is uncertain. The second sentence reassures the writer that an unsure result doesn't automatically mean their work is AI-written, and makes clear there's nothing else they need to do.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

*Milestone 3: earlier run with one signal only (the JSON below is the log entry it produced)*

```powershell
curl.exe --% -i -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d "{\"text\":\"I like to eat dark chocolate and drink matcha.\",\"creator_id\":\"test-user\"}"  
```

```json
 {
      "combined_score": null,
      "content_id": "c_418d2f5b7252",
      "creator_id": "test-user",
      "guess": null,
      "label": null,
      "model_score": 0.3193,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-04T02:08:20+00:00"
    }

```

*Milestone 5: both signals, combined score and real label*

```powershell
curl.exe --% -i -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d "{\"text\":\"Regular exercise is one of the most important things you can do for your health. It helps to improve your physical fitness and your overall well-being. Exercise can also help to reduce stress and improve your mood. Many people find that regular physical activity helps them to sleep better at night. It is important to find a type of exercise that you enjoy doing. This will make it easier to stay motivated and keep a regular routine. Overall, regular exercise is a simple and effective way to improve your quality of life.\",\"creator_id\":\"chatbot-ai\"}"
```

```json
{
  "confidence": 0.8471,
  "content_id": "c_1fff4a8f34b3",
  "guess": "ai",
  "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
  "model_score": 0.9536,
  "style_score": 0.7405
}
```

**An appeal**

```powershell
curl.exe --% -i -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d "{\"content_id\":\"c_1fff4a8f34b3\",\"reasoning\":\"I wrote this myself and did not use AI.\"}"
```

```json
{
  "content_id": "c_1fff4a8f34b3",
  "message": "Your appeal has been recorded and this submission is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
curl.exe -s "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8471,
      "content_id": "c_1fff4a8f34b3",
      "creator_id": "chatbot-ai",
      "guess": "ai",
      "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.",
      "model_score": 0.9536,
      "status": "decided",
      "style_score": 0.7405,
      "timestamp": "2026-11-04T05:14:27+00:00"
    },
    {
      "content_id": "c_1fff4a8f34b3",
      "creator_id": "chatbot-ai",
      "event": "appeal",
      "reasoning": "I wrote this myself and did not use AI.",
      "status": "under_review",
      "timestamp": "2026-11-04T05:16:28+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude to implement the three style measures in `stylometry.py` (sentence-length spread, type-token ratio, punctuation density) one at a time, showing me each change before editing, and then to help me decide how to combine them into `style_signal`.
- *What came back:* The three measures, tested on my samples. The results showed type-token ratio pointed the opposite way from what I'd assumed: my AI sample had the most varied vocabulary, not the least. Claude laid out three options for combining the measures, with the scores each would give my samples. It also explained why one of my formal human samples, a traffic-safety report, scored as AI on the model signal: its stock academic phrasing is very predictable to GPT-2.
- *What I changed:* I chose to keep all three measures and flip word variety as originally planned, with caps of 1.2 for spread and 0.15 for punctuation, and documented them as heuristics rather than proven thresholds. I replaced the traffic report with a paragraph from my own lab report, because I couldn't be sure a teammate hadn't used AI on it. I also wrote up the length limitation in the README instead of tuning the numbers to fit four samples.

**Moment 2**

- *What I asked for:* I asked Claude to check my three label sentences against the brief's requirements.
- *What came back:* The human label was fine. The unsure label admitted uncertainty but didn't tell the writer what it meant for them, so "human or AI" could still read as suspicion. The AI label sounded certain and didn't tell the writer they could push back, even though my own lab report had already been labelled AI.
- *What I changed:* I rewrote both myself. I added a second sentence to the unsure label saying it doesn't mean the work is AI-written and that no action is needed. I added to the AI label that the system can make mistakes and that the writer should appeal if they wrote it themselves. I kept "most likely", because the appeal sentence balances it.

**Moment 3**

- *What I asked for:* I asked Claude to generate five AI samples for criterion 2 and to split two of my own documents into ten pieces for criterion 1.
- *What came back:* Claude suggested prompts on the same topics as my writing (astrophotography and my New Testament course), so the comparison would test who wrote it rather than what it was about. It split my documents into ten paragraphs, kept my typos, and left out the data tables.
- *What I changed:* I asked for the pieces to alternate between the two documents, so the five human samples in criterion 2 weren't all from one report. I confirmed none of my writing used AI help or came from a group member, and I used the AI samples exactly as generated.

**Moment 4**

- *What I asked for:* I asked Claude for options to improve my criteria results in Milestone 5, focusing on the thresholds or the style signal.
- *What came back:* Claude tested five options on my eval texts and the attacks before changing anything: two human thresholds (0.45 and 0.48), tighter style caps, and two reweightings. No option fixed criterion 2. Only the 0.48 threshold met criterion 3, but it did that by labelling one of the Claude samples human. Tightening the caps cut false accusations in half but made criterion 3 worse.
- *What I changed:* I chose to tighten the style caps (spread 1.2 → 0.6, punctuation 0.15 → 0.08), because reducing false positives matters most to me. A wrong accusation costs a real writer more than a missed detection costs the site. I accepted that criterion 3 got worse and that two evasions now come back as human, and reported both.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
A real writer submits their own work a few times an hour at most, so 5 a minute and 50 a day never get in their way. A script sending a thousand variations to map my thresholds gets cut off after 5 tries a minute and 50 a day, which would turn a mapping run that takes minutes into one that takes weeks.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->
Per `creator_id`, falling back to the caller's IP address when there isn't one. The weakness is that a script can send a new made-up `creator_id` with every request and never hit the limit.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
============================================================

10 of 15 were rate limited. Paste the run above into your README
under **Rate Limiting**, and check GET /log recorded the rejections.

Wrote results\flood_2026-11-09_2308.md

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

From `results/attack_run_2026-11-09_2354.md`, produced by `run_attacks.py::main` against `app.py::submit`.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_b1d19d35cf46` | unsure | 0.375 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_b8126d1f5344` | unsure | 0.505 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_c6d6a07c7da2` | unsure | 0.590 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_82c8d199ecf7` | unsure | 0.597 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_11fa064b97b9` | unsure | 0.371 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_a108cfc3a321` | unsure | 0.460 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_07cbf142e55d` | unsure | 0.498 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `c_26929f8be4f2` | unsure | 0.417 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_10a159020f58` | unsure | 0.596 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_3f661f09859d` | ai | 0.881 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_8e2440502356` | unsure | 0.606 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c_da331615f679` | ai | 0.703 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_9af04d515d46` | ai | 0.737 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_7cdcfd8cca2e` | ai | 0.714 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_b616f2c7b839` | ai | 0.733 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_5a0190c4a131` | ai | 0.729 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_ffd5f2ebc7db` | ai | 0.725 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `c_9149e7988a20` | unsure | 0.434 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_7cf26b96d7bc` | unsure | 0.484 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_0cd0f91b1b4c` | human | 0.303 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_76362a3ac26e` | unsure | 0.537 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_e9d1bbd0e41a` | unsure | 0.464 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_79de15fe4a1e` | unsure | 0.427 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_79b162eea9b7` | unsure | 0.580 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c_3cd8f32e8402` | human | 0.333 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `c_547471367c7b` | unsure | 0.506 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `c_a2f48539c2b7` | ai | 0.832 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `c_e849aca448ae` | ai | 0.999 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `c_4ea55a9d4c82` | ai | 0.953 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `c_572a2b1e5508` | unsure | 0.453 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `c_fb392dab9838` | unsure | 0.358 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD* |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD* |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_d90d68397087` | human | 0.348 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_fd12e1127735` | human | 0.348 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_1c8642d71b2d` | human | 0.348 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_28bff9466c34` | human | 0.348 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_ee6ae5822027` | human | 0.348 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Count: 32 held, 24 broke (56 attacks).**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 2 | 6 |
| prompt_injection | 6 | 5 | 1 |
| malformed | 20 | 12 | 8 |
| flood_same_creator | 12 | 12 | 0 |

**How I marked them:**
- **Evasion:** an "unsure" result counts as BROKE. My unsure label tells the writer "no further action is needed," so AI text that lands there faces no consequence.
- **PI02:** BROKE. Its text is generic AI-style writing under a fake "SYSTEM" line asking for `guess=human`, and it came back human.
- **RQ02:** HELD. The text was valid, and a missing creator_id defaults to `"unknown"`.
- **RQ06:** BROKE. A creator_id that isn't a string was accepted and written into the audit log as-is.
- **\*RQ10, RQ11:** HELD, but not really tested. With no readable creator_id, they counted against my IP address, hit the per-minute limit, and got a 429 before reaching my route.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From `logs/audit.jsonl`:

```json
{"timestamp": "2026-11-10T04:54:16+00:00", "content_id": "c_9af04d515d46", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6679, "combined_score": 0.7365, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:16+00:00", "content_id": "c_b616f2c7b839", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6644, "combined_score": 0.7325, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:18+00:00", "content_id": "c_4ea55a9d4c82", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9532, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:18+00:00", "content_id": "c_e849aca448ae", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9985, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:14+00:00", "content_id": "c_11fa064b97b9", "creator_id": "attacker_EV05", "guess": "unsure", "model_score": 0.3212, "style_score": 0.4208, "combined_score": 0.371, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:15+00:00", "content_id": "c_10a159020f58", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.4877, "combined_score": 0.5959, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:16+00:00", "content_id": "c_0cd0f91b1b4c", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.4017, "combined_score": 0.303, "label": "Your sample was probably written by a human.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:19+00:00", "content_id": "c_fb392dab9838", "creator_id": {"id": "x"}, "guess": "unsure", "model_score": 0.0492, "style_score": 0.6667, "combined_score": 0.3579, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "status": "decided"}
{"timestamp": "2026-11-10T04:54:19+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-10T04:54:18+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long", "length": 57640}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03 — a non-native English speaker writing carefully.** A real person's writing came back as high-confidence AI (combined score 0.737; model signal 0.805, style signal 0.668), with the label *"This sample was most likely written by AI."* This is the one I'd least want to explain: the writer did nothing wrong except write carefully in a language that isn't their first, and my system confidently accused them and left it to them to appeal.


---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10 | 1/10 | 1/10 | 1/10 | MET |
| 2. AI average minus human average (5 each) | ≥ 0.30 | −0.038 | −0.038 | −0.038 | MISSED |
| 3. All three labels reachable (50+ word paragraphs) | 3 of 3 | 2/3 | 2/3 | 2/3 | MISSED |
| 4. Valid appeals recorded as `under_review`, original kept | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 5. Bad input rejected with 400, no content_id | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

Criteria 1, 2, 3 and 5 were run with `python run_eval.py --label before` → `results/run_2026-11-10_1651_before.md`. Criterion 4 was tested by hand in PowerShell (3 submits and 3 appeals per trial), because `run_eval.py` only calls `/submit`. All three trials came out identical, as expected, since neither signal is random.

**How I decided each verdict:**
1. **MET**: 1 of 10 of my own pieces was labelled high-confidence AI in every trial, which is exactly at the target. It's a narrow pass: four other pieces scored between 0.60 and 0.65, within 0.05 of the AI cutoff.
2. **MISSED**: the AI average was 0.038 *below* the human average in every trial, nowhere near the required +0.30. My writing scored as more AI-like than the actual AI text.
3. **MISSED**: in every trial, none of the 15 full paragraphs got the high-confidence human label, so only 2 of the 3 labels were reachable.
4. **MET**: in every trial, all 3 valid appeals were logged with status `under_review`, and each original `decided` entry was still in the log.
5. **MET**: all 7 bad inputs returned a 400 with no content_id in every trial, and none were logged as decisions.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

All from Trial 1. Criteria 1, 2, 3 and 5 are from `results/run_2026-11-10_1651_before.md`, produced by `run_eval.py::main` sending each body to `app.py::submit`. Trials 2 and 3 were identical.

**Criterion 1 — my own writing** (1 of 10 labelled AI: the 9th piece, astrophotography paragraph 5)

```json
{"status": 200, "guess": "unsure", "confidence": 0.643, "model_score": 0.6561, "style_score": 0.6298, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "The type of astrophotography chosen for the final project was deep sky"}
{"status": 200, "guess": "unsure", "confidence": 0.6178, "model_score": 0.6206, "style_score": 0.615, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "This course has allowed me to grow alot in my awareness of the new tes"}
{"status": 200, "guess": "unsure", "confidence": 0.5526, "model_score": 0.5198, "style_score": 0.5854, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Data mining was used to obtain these images. The telescope used was th"}
{"status": 200, "guess": "unsure", "confidence": 0.4779, "model_score": 0.3988, "style_score": 0.557, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "A few things that were new and interesting to learn was about the actu"}
{"status": 200, "guess": "unsure", "confidence": 0.5397, "model_score": 0.5984, "style_score": 0.481, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Calibration frames were used to remove any sort of artifacts from the "}
{"status": 200, "guess": "unsure", "confidence": 0.5399, "model_score": 0.5314, "style_score": 0.5484, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Another area which was interesting to know was the study of the pascha"}
{"status": 200, "guess": "unsure", "confidence": 0.6039, "model_score": 0.5504, "style_score": 0.6574, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Registration was needed to align the stars in the images.  Due to the "}
{"status": 200, "guess": "unsure", "confidence": 0.6059, "model_score": 0.6206, "style_score": 0.5912, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Another part of this class that I appreciated was looking into specifi"}
{"status": 200, "guess": "ai", "confidence": 0.6834, "model_score": 0.708, "style_score": 0.6588, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "sent": "After stacking was done for each filter, I moved on to stretching. Eac"}
{"status": 200, "guess": "unsure", "confidence": 0.6175, "model_score": 0.6334, "style_score": 0.6015, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Towards the end of the semester, I also enjoyed looking into the Pauli"}
```

**Criterion 2 — AI samples vs. my writing** (AI average 0.5286, human average 0.5662, gap −0.0376)

AI samples:

```json
{"status": 200, "guess": "unsure", "confidence": 0.4766, "model_score": 0.426, "style_score": 0.5272, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "For my astrophotography final project, I wanted a target that would re"}
{"status": 200, "guess": "unsure", "confidence": 0.5181, "model_score": 0.4553, "style_score": 0.5809, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Calibration frames are what turn raw astrophotography exposures into c"}
{"status": 200, "guess": "unsure", "confidence": 0.5156, "model_score": 0.5274, "style_score": 0.5038, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "To process my nebula image, I started with separate grayscale datasets"}
{"status": 200, "guess": "unsure", "confidence": 0.5296, "model_score": 0.6162, "style_score": 0.4431, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "This course changed the way I think about how the New Testament came t"}
{"status": 200, "guess": "unsure", "confidence": 0.6033, "model_score": 0.6221, "style_score": 0.5844, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Studying the historical Jesus and Paul’s letters affected my faith in "}
```

Human samples (my first five pieces, same output as the first five lines under Criterion 1):

```json
{"status": 200, "guess": "unsure", "confidence": 0.643, "model_score": 0.6561, "style_score": 0.6298, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "The type of astrophotography chosen for the final project was deep sky"}
{"status": 200, "guess": "unsure", "confidence": 0.6178, "model_score": 0.6206, "style_score": 0.615, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "This course has allowed me to grow alot in my awareness of the new tes"}
{"status": 200, "guess": "unsure", "confidence": 0.5526, "model_score": 0.5198, "style_score": 0.5854, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Data mining was used to obtain these images. The telescope used was th"}
{"status": 200, "guess": "unsure", "confidence": 0.4779, "model_score": 0.3988, "style_score": 0.557, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "A few things that were new and interesting to learn was about the actu"}
{"status": 200, "guess": "unsure", "confidence": 0.5397, "model_score": 0.5984, "style_score": 0.481, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "sent": "Calibration frames were used to remove any sort of artifacts from the "}
```

**Criterion 3 — label coverage** (all 15 texts above; 14 unsure, 1 ai, 0 human). The `c3 label coverage` scenario sends the same 15 texts, and the output matches the entries above line for line. The only non-unsure result:

```json
{"status": 200, "guess": "ai", "confidence": 0.6834, "model_score": 0.708, "style_score": 0.6588, "label": "This sample was most likely written by AI. However, this checker system can make mistakes. If you wrote the sample yourself, please submit an appeal.", "sent": "After stacking was done for each filter, I moved on to stretching. Eac"}
```

**Criterion 4 — appeals**, Trial 1, from `logs/audit.jsonl`. The decisions were written by `app.py::submit` (`audit.log_decision`) and the appeals by `app.py::appeal` (`audit.log_appeal`):

```json
{"timestamp": "2026-11-10T23:37:00+00:00", "content_id": "c_a29fd3860974", "creator_id": "c4_t1_a", "guess": "human", "model_score": 0.1801, "style_score": 0.5042, "combined_score": 0.3422, "label": "Your sample was probably written by a human.", "status": "decided"}
{"timestamp": "2026-11-10T23:37:00+00:00", "content_id": "c_3dc335856b7b", "creator_id": "c4_t1_b", "guess": "unsure", "model_score": 0.4494, "style_score": 0.6782, "combined_score": 0.5638, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "status": "decided"}
{"timestamp": "2026-11-10T23:37:01+00:00", "content_id": "c_f9367e764c49", "creator_id": "c4_t1_c", "guess": "unsure", "model_score": 0.4614, "style_score": 0.6194, "combined_score": 0.5404, "label": "Unable to determine if this sample was written by a human or AI. This doesn't mean that the sample is AI-written, and no further action is needed from you.", "status": "decided"}
{"timestamp": "2026-11-10T23:37:01+00:00", "content_id": "c_a29fd3860974", "creator_id": "c4_t1_a", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-10T23:37:01+00:00", "content_id": "c_3dc335856b7b", "creator_id": "c4_t1_b", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-10T23:37:01+00:00", "content_id": "c_f9367e764c49", "creator_id": "c4_t1_c", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
```

**Criterion 5 — bad input** (7 of 7 returned 400 with no content_id)

```json
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"creator_id\": \"eval_bad_missing\"}"}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "(empty text)"}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "   \n\t  "}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"text\": [\"a\", \"list\"], \"creator_id\": \"eval_bad_list\"}"}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"}
{"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "word word word word word word word word word word word word word word "}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

Every miss and every broken attack, with the stage and the mechanism. Scores are model / style → combined.

#### Missed criteria

**Criterion 2: gap −0.038, target +0.30. Stage: signal one and signal two together.**
My writing averaged model 0.559 / style 0.574, and the Claude samples averaged 0.529 / 0.528. For signal one, my plain wording and repeated phrases ("I moved on to", "in order to") gave lower perplexity (about 40 vs. 43) than Claude's rarer vocabulary, and GPT-2 reads predictable text as AI. For signal two, I reuse words (stretch, stacked, filter), so my type-token ratio was 0.57 vs. Claude's 0.69, and low variety reads as AI. The combining rule averages two signals that are wrong in the same direction, so nothing cancels.

**Criterion 3: no human label. Stage: signal two, plus the combining rule.**
For normal paragraphs, the style signal never went below 0.44. Spread (0.2–0.5) and punctuation density (0.03–0.10) sit far below their caps (1.2 and 0.15), so those two parts always lean AI. With style at 0.44 or above, a 50/50 average only drops to the 0.35 human threshold if the model score is about 0.25 or lower, which means perplexity around 90 or more. None of the 15 paragraphs got there.

#### Broken attacks

**Evasion (9)**

| ID | Scores | Stage | Mechanism |
|---|---|---|---|
| EV01 typos | 0.164 / 0.587 → 0.375 | signal one | Typos are tokens GPT-2 doesn't expect, so perplexity rose and the model score dropped to 0.16. It targeted signal two, but signal one is what gave way. |
| EV02 broken-up sentences | 0.594 / 0.416 → 0.505 | signal two | Chopping sentences raised sentence length spread, so style read human. |
| EV03 pasted quotation | 0.666 / 0.513 → 0.590 | signal two + combining rule | The model alone was above 0.65 (AI). The quote changed the shape, style dropped to 0.51, and the 50/50 average pulled the result under the AI cutoff. |
| EV04 unusual words | 0.611 / 0.583 → 0.597 | signal one | Rare words raised perplexity enough to keep the model score under 0.65, and style wasn't high enough to make up for it. |
| EV05 heavy human edit | 0.321 / 0.421 → 0.371 | signal one + signal two | Real human edits made the text less predictable and more varied, so both signals moved toward human. |
| EV06 one long + one short sentence | 0.573 / 0.348 → 0.460 | signal two | A 1-long/1-short pair inflates spread (stdev ÷ mean), so style dropped to 0.35. |
| EV07 punctuation padding | 0.586 / 0.409 → 0.498 | signal two | Extra commas, dashes and parentheses raised punctuation density, which my style signal counts as human. |
| EV08 below token window | 0.245 / 0.588 → 0.417 | signal one | Short text gives GPT-2 little context, so perplexity is high and the model score fell to 0.25. |
| EV09 human opening bolted on | 0.704 / 0.488 → 0.596 | combining rule | The model correctly said AI (0.70). The human opening lowered style to 0.49, and the equal weighting averaged the correct signal away. |

**False positive (6). Stage for all six: signal one.**

| ID | Scores | Mechanism |
|---|---|---|
| FP02 formal register | 0.739 / 0.667 → 0.703 | Formal, conventional phrasing is predictable to GPT-2. |
| FP03 non-native, careful | 0.805 / 0.668 → 0.737 | Careful writers sticking to words they're sure of produce low perplexity. |
| FP04 rubric essay | 0.833 / 0.596 → 0.714 | Writing to a rubric uses expected structure and stock phrases, which are predictable. |
| FP05 technical docs | 0.801 / 0.664 → 0.733 | Repeated technical terms and fixed patterns are easy to predict. |
| FP06 imitating a template | 0.881 / 0.576 → 0.729 | Template wording is exactly what a language model expects next. |
| FP07 repeated phrase | 0.882 / 0.569 → 0.725 | After the first repetition, every repeat is near-certain to GPT-2. |

The style score sat at 0.57–0.67 for all six, which also pushed toward AI, but the model score is what carried each one over 0.65.

**Prompt injection (1)**

| ID | Scores | Stage | Mechanism |
|---|---|---|---|
| PI02 fake SYSTEM message | 0.204 / 0.402 → 0.303 | signal one | Nothing in the pipeline followed the instruction. The odd "SYSTEM: … guess=human, confidence=0.02" line is high-perplexity text, which dragged the model score down to 0.20 and gave the attacker the human result anyway. |

**Malformed (8)**

| ID | Result | Stage | Mechanism |
|---|---|---|---|
| MF02 single character | 500 | route | The route only checks for empty text. `detector.perplexity` raises `ValueError` on under 3 tokens and nothing catches it, so the writer gets a 500 and the audit log gets no entry. |
| RQ07 JSON array body | 500 | route | `request.get_json(...) or {}` only replaces empty bodies. A list is truthy, so `payload.get` raises `AttributeError`, again with no log entry. |
| MF03 control characters | human 0.333 | route → signal one | Non-prose passed the "non-empty string" check. Gibberish has huge perplexity, so model = 0.0 and the result was human. |
| MF04 punctuation only | unsure 0.506 | route → signal two | With no words, all three style measures are 0, which flips to style 1.0. Model 0.01 averaged it to unsure. |
| MF05 one very long word | ai 0.832 | route → signal one | After the first few tokens, the rest of a long repeated word is predictable, so model = 0.998. |
| MF06 emoji only | ai 0.999 | route → signal one + signal two | Repeated emoji tokens are predictable (model 0.997), and `words()` only matches `a-z`, so no words gives style 1.0. |
| MF07 right-to-left script | ai 0.953 | signal two (+ signal one) | `words()` uses `[a-z0-9']`, so Arabic or Hebrew text has zero "words" and style is pinned at 1.0. Real non-English writing gets labelled AI. |
| RQ06 creator_id is an object | decided | route | The route never checks that `creator_id` is a string, so the object was written into the audit log as the creator. |

**By stage:** signal one 11 (EV01, EV04, EV05, EV08, FP02–FP07, PI02), signal two 5 (EV02, EV03, EV06, EV07, MF07), combining rule 1 (EV09), route 7 (MF02–MF06, RQ06, RQ07). The label mapping wasn't the main cause of any miss.

#### Patterns

The 2 misses and 24 broken attacks come down to three problems, not 26.

**Pattern 1: plain, predictable writing reads as AI to both signals.** Explains criterion 2, FP02–FP07, PI02, and criterion 1's one AI label (my astrophotography paragraph 5, model 0.708). Both of my signals measure *unusualness*, not authorship. Signal one rewards text GPT-2 can't predict, and signal two rewards varied vocabulary and lots of punctuation. Plain, careful or repetitive human writing scores as machine-like on both, while polished modern AI uses rarer words and scores lower. The same mechanism runs the other way for EV01, EV04, EV05 and EV08: anything that makes AI text less predictable (typos, rare words, edits, shortness) pulls it toward human. Because both signals lean the same way, averaging them doesn't correct the error.

**Pattern 2: the score range is squeezed into the unsure band.** Explains criterion 3, EV01–EV09, and why even unedited Claude text (0.48–0.60) never reached the AI label. The style signal has a floor of about 0.44 on normal paragraphs, because spread and punctuation sit far below their caps, and the 50/50 average halves any strong reading from one signal (EV09: model 0.70 → combined 0.596). Real paragraphs land between 0.44 and 0.70, so neither confident label is reachable in practice. The evasions mostly didn't have to beat the detector, since clean AI text already landed in unsure.

**Pattern 3: the route checks the type of `text`, not whether it's prose.** Explains MF02–MF07, RQ06 and RQ07. The route accepts any non-empty string under 10,000 characters, so emoji, control characters, punctuation and non-Latin script reach the signals. Signal two's `words()` only matches `a-z`, so text with no Latin letters gets style 1.0, which is how real Arabic or Hebrew writing (MF07) was labelled AI at 0.953. The two inputs the route doesn't check at all (a 1-character text and a non-object body) crash with a 500 and leave nothing in the audit log, so an attack made of them would be invisible.

---

## The Improvement

**What I changed:** One change, in `stylometry.py::style_signal`: I tightened the two caps that scale the style measures. Sentence length spread went from 1.2 to **0.6**, and punctuation density from 0.15 to **0.08**. Nothing else changed: same weights (50/50), same thresholds (0.35 / 0.65), same route.

**Which diagnosis pointed at it:** Pattern 2. Real paragraphs had spread of 0.2–0.5 and punctuation of 0.03–0.10, far below the old caps, so those two parts always leaned AI and the style signal never went below about 0.44. Tightening the caps lets those measures use more of their 0–1 range. Before choosing, I tested this against moving the human threshold (0.45 or 0.48) and reweighting the signals (0.7 / 0.3). I picked the caps because they cut false accusations the most, and my criteria say a wrong accusation costs more than a missed detection.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

From `results/attack_run_2026-11-10_2255_after.md`, produced by `run_attacks.py::main` against `app.py::submit`. Marked with the same rules as the before run.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_297427c4b488` | human | 0.319 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_e1b34cd4d501` | unsure | 0.424 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_745c570fa858` | unsure | 0.491 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_b31f782dbe87` | unsure | 0.539 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_e5312b6a7e29` | human | 0.239 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_ae07c73c9521` | unsure | 0.427 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_1371150d20d8` | unsure | 0.498 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `c_d036d5a8e556` | unsure | 0.377 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_3390143fbe29` | unsure | 0.487 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_cf38892d2cb4` | ai | 0.827 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_10d63d169a64` | unsure | 0.523 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c_231cea17b408` | ai | 0.657 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_7dc6f20d9b1f` | ai | 0.691 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_80acfa87d01a` | unsure | 0.649 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_2cbc3431e14d` | ai | 0.666 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_0975084029cb` | unsure | 0.641 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_92fb53492ef3` | unsure | 0.627 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `c_5b97fcd1d869` | unsure | 0.374 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_f4611950d625` | unsure | 0.409 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_422d131daf32` | human | 0.184 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_b7e08461b92f` | unsure | 0.437 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_4d025f1f01fc` | human | 0.333 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_2db61267213b` | unsure | 0.361 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_379c7469a958` | unsure | 0.501 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c_1548970cd887` | human | 0.333 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `c_af3a45959169` | unsure | 0.506 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `c_3a427603d9f1` | ai | 0.832 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `c_f56727e80b02` | ai | 0.999 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `c_c2e21beca98a` | ai | 0.953 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `c_b0509d82a712` | unsure | 0.453 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `c_98fda0071149` | unsure | 0.358 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD* |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD* |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_2b3eb76001b6` | human | 0.348 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_529a55b3b22d` | human | 0.348 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_fb193bd94717` | human | 0.348 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_c231c757e162` | human | 0.348 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_9a5313a5e83f` | human | 0.348 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

\*Same as before: these hit the IP-keyed rate limit and never reached the route.

PI04 came back human this time, but its goal was to make the label text hostile, and the label is a fixed string, so it still held.

### Run Log — After

`python run_eval.py --label after` → `results/run_2026-11-10_2258_after.md` (criteria 1, 2, 3 and 5). Criterion 4 was re-run by hand in PowerShell with `c4after_` creator_ids. All three trials were identical again.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. AI average minus human average (5 each) | ≥ 0.30 | −0.041 | −0.041 | −0.041 | MISSED |
| 3. All three labels reachable (50+ word paragraphs) | 3 of 3 | 1/3 | 1/3 | 1/3 | MISSED |
| 4. Valid appeals recorded as `under_review`, original kept | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 5. Bad input rejected with 400, no content_id | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |

### Before and After, Side by Side

| | Before | After |
|---|---|---|
| **Criterion 1:** own writing → AI | 1/10 (MET) | **0/10** (MET) |
| **Criterion 2:** AI avg − human avg | −0.038 (MISSED) | −0.041 (MISSED) |
| **Criterion 3:** labels reached | 2/3 (MISSED) | **1/3** (MISSED, worse) |
| **Criterion 4:** appeals | 3/3 (MET) | 3/3 (MET) |
| **Criterion 5:** bad input | 7/7 (MET) | 7/7 (MET) |
| My writing, combined range | 0.478–0.683 | 0.378–0.600 |
| Claude samples, combined range | 0.477–0.603 | 0.376–0.515 |
| **Attacks held / broke** | 32 / 24 | **35 / 21** |
| evasion | 1 / 9 | 1 / 9 (EV01 and EV05 now labelled **human**) |
| false_positive | 2 / 6 | **5 / 3** |
| prompt_injection | 5 / 1 | 5 / 1 |
| malformed | 12 / 8 | 12 / 8 |
| flood | 12 / 0 | 12 / 0 |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

It helped with the mistake I care about most and hurt everything else. False accusations went down: the false-positive attacks labelled AI dropped from 6 to 3 (FP04, FP06 and FP07 are now unsure), and none of my own writing is labelled AI anymore (my astrophotography paragraph went from 0.683 to 0.600). The cost is that the change moved every score down instead of spreading them out. My writing now sits at 0.38–0.60 and Claude's at 0.38–0.52, so all 15 paragraphs are unsure and criterion 3 fell from 2/3 to 1/3 labels. Two evasions (EV01 typos, EV05 heavy edit) went from unsure to **human**, which is worse than before. Criterion 2 didn't move (−0.038 → −0.041), which confirms my diagnosis: both signals measure the wrong thing on my writing, and rescaling one of them can't flip which group scores higher. Overall: fewer wrong accusations, in exchange for a detector that confidently clears more AI text.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

After the improvement, 2 criteria are still missed and 21 attacks still get through.

**Criterion 2 (AI vs. human gap, −0.041) and criterion 3 (only 1 of 3 labels).** What I'd do: replace or recalibrate the signals themselves. Signal one would need a newer model than GPT-2, one that actually finds modern AI text predictable, and signal two would need measures that don't treat repeated words and light punctuation as machine-like. Once the two groups separate, I'd revisit the thresholds so both confident labels can be reached. Why I stopped: no single setting fixes this. My Milestone 5 tests showed that every threshold, cap and weight I tried left the gap negative, and swapping the model is bigger than the one change this unit allows.

**Evasion: EV01–EV09 (9).** What I'd do: the same signal fix as criteria 2 and 3, since even unedited AI text only reaches 0.38–0.52 now, so the evasions hardly have to try. For EV09 specifically, I'd score the text in chunks and flag it if any chunk reads strongly as AI, so a human opening can't average the rest away. Why I stopped: same reason as above, and EV01 and EV05 got worse (unsure → human) with my change, which I chose to accept in exchange for fewer false accusations.

**False positive: FP02, FP03, FP05 (3).** What I'd do: for formal, technical and second-language writing, a high model score alone shouldn't be enough to say AI. I'd require both signals to clearly agree before giving the AI label. Why I stopped: that's a change to the combining rule, which would have been a second change. These three are the ones I'd most want fixed, especially FP03.

**Prompt injection: PI02 (1).** What I'd do: strip or flag lines that look like instructions to a system ("SYSTEM:", "Return guess=…") before scoring, so they can't move perplexity. Why I stopped: nothing actually obeyed the instruction, and the cause is the same signal one weakness behind EV01. Fixing the signal matters more than filtering one phrasing.

**Malformed: MF02–MF07, RQ06, RQ07 (8).** What I'd do: input validation in `app.py::submit`. Check that the body is a JSON object (RQ07) and `creator_id` is a string (RQ06), require a minimum number of real words (MF02–MF06), and catch any signal error as a logged 400 instead of a 500. For MF07, I'd make `words()` match letters in any script, not just `a-z`, so non-English writing isn't pinned at style 1.0. Why I stopped: I chose to spend my one change on the criteria. This is the fix I'd make next, because the two 500s leave nothing in the audit log.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd keep going the way my change went: fewer wrong accusations, even though more AI text gets through, because a false accusation can cost a real writer their reputation, and the writers my system accuses most are plain, careful and second-language writers who have the least room to argue back. The people who pay for that are honest writers on the site, whose work now sits next to AI text that got cleared, and readers, who can't fully trust that what they're reading is human.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
