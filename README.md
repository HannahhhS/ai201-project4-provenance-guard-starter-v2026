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
- `guess`: The system's prediction (AI or human).
- `confidence`: The confidence score associated with the prediction.
- `label`: A plain-English explanation of the result.

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

The model analyzes the text and estimates whether its language patterns are more characteristic of AI-generated or human-written text.

**Why that might differ between human and AI writing:**

AI-generated writing can contain patterns that differ from natural human writing, such as predictable phrasing or consistent language patterns. The model attempts to recognize these differences based on patterns it learned during training.

**What it can't see:**

It cannot know who actually wrote the text or whether AI was used. It may incorrectly classify human writing that happens to resemble AI-generated writing, or AI-generated writing that has been heavily edited.

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

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
