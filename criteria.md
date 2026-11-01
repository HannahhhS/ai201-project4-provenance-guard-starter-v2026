# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Of 10 pieces of original writing I wrote myself, no more than 1 should receive a high-confidence AI label in each of the three evaluation trials.

**Why this target:**

A false positive can unfairly accuse someone of using AI when they wrote the work themselves. I want to keep false positives low because the consequences of incorrectly accusing a writer are more serious than missing some AI-generated content.I allow one false positive because completely eliminating false positives may not be realistic for an automated detection system. 2 false positives costs alot as false positives are dangerous accusations. 

---

## 2.

The average confidence score of 5 clearly AI-generated samples should be at least 0.30 higher than the average of 5 clearly human-written samples in each of the three evaluation trials. Confidence runs from 0.0 (confidently human) to 1.0 (confidently AI). "Clearly AI-generated" means chatbot output with no edits. "Clearly human-written" means pieces I wrote myself with no AI help.

**Why this target:**

The system should distinguish between clearly different types of writing rather than assigning nearly identical scores to everything. I chose 0.30 because it matches the width of my unsure band (0.35–0.65). With a smaller gap, both group averages could land on "unsure" and the criterion would pass without the system confidently labelling either group.

---

## 3.

All three labels (high-confidence human, unsure, and high-confidence AI) must be reachable: in each of the three evaluation trials, at least one test submission must receive each label. Test submissions must be full paragraphs of at least 50 words.

**Why this target:**

The system should not force every submission into a human or AI classification. The unsure label is important because the signals may not always provide enough evidence for a confident decision.Testing all three labels ensures that each one can actually be used, and the 50-word minimum gives the system enough text to analyze meaningful writing patterns.

---

## 4.

In each of the three evaluation trials, all 3 valid appeals must be recorded in the audit log with status `under_review`, while preserving the original decision. A valid appeal has a content ID that exists in the audit log and non-empty reasoning.

**Why this target:**

Writers should have a reliable way to challenge an incorrect result. Recording every appeal ensures their concerns are not lost and disputed submissions can be reviewed.

---

## 5.

In each of the three evaluation trials, missing, empty, whitespace-only, or non-string text, as well as text longer than 10,000 characters, must be rejected with an HTTP 400 response. Rejected submissions must not receive a content ID or be recorded as successful decisions.

**Why this target:**

The service should handle invalid input predictably instead of trying to analyze incomplete submissions. This prevents invalid submissions from being treated as legitimate decisions.I chose 10,000 characters because it allows room for a substantial writing submission while preventing excessively large inputs from requiring unnecessary processing.


<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
