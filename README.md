# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This system answers questions about the `campus_life` corpus, which contains
short posts about university procedures, housing, dining, printing, accounts,
and courses. It retrieves relevant document chunks and uses them to generate a
brief answer that names the source file. A relevance gate refuses questions
whose best retrieved chunk is not close enough, so questions outside campus
life are answered with an honest lack-of-information message.

## Chunking Strategy

**Chunk size:**
Up to 400 characters, using paragraph boundaries
**Overlap:**
0 characters

The campus_life corpus has short posts, and its paragraphs range from 10 to 373
characters. I kept each document title with its first paragraph, then used each
remaining paragraph as its own chunk. The resulting title-plus-first-paragraph
chunks are at most 397 characters, so a 400-character ceiling fits the corpus
without cutting a sentence. I used no overlap because each paragraph is already
a complete, small thought and overlapping them would duplicate most of the
document.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer
window — through the end of week six — but a drop after week two shows as a W on
your transcript. Nothing anywhere on the registrar's site says this plainly,
and students find out from each other.
```

**Chunk 2** — source: `course_cs_340_exams.txt#1` — produced by: `chunker.py::split_documents`

```
Start the term project in week three, not week eight; everyone learns this the
hard way.
```

**Chunk 3** — source: `course_phys_130_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for PHYS 130 Mechanics

People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time,
not optimistic time.
```

**Chunk 4** — source: `dining_verrill_street_grill_followup.txt#1` — produced by: `chunker.py::split_documents`

```
Also worth saying: one register, so the queue is a single line no matter how
busy. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt#1` — produced by: `chunker.py::split_documents`

```
The good: cheapest housing tier by about $900 a year, and the singles are real
singles.
```

## Sample Answer

**Question:** How is the housing lottery order decided for juniors and seniors?

**Answer:** For juniors and seniors, the housing lottery order is decided by accumulated credit hours first, with random tie-breaks used only in the event of a tie (`admin_housing_lottery.txt`).

```
Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt,
advising_registration.txt, housing_aldridge_hall.txt, housing_morrow_house.txt
```

**My relevance cutoff:** 0.6

The five in-scope questions had best distances from 0.1839 to 0.3719. The five
out-of-scope questions had best distances from 0.7873 to 0.9228. I kept the
starter cutoff of 0.6 because it falls in the gap between the two groups: all
five in-scope questions pass and all five out-of-scope questions are refused.
I kept `top-k=5` because the relevant chunk was first for all five questions,
while returning several nearby chunks lets the answer include context when a
question needs it.

| Question | In corpus? | Best distance |
|---|---|---|
| How is the housing lottery order decided for juniors and seniors? | Yes | 0.2138 |
| How long do I have to change my meal plan tier, and what happens when I downgrade? | Yes | 0.1839 |
| How much printing credit does each student receive per semester? | Yes | 0.3719 |
| How long does my student account stay active after graduation? | Yes | 0.3540 |
| How many hours per week should I expect to spend outside class for CS 210? | Yes | 0.2281 |
| What is the capital of Mongolia? | No | 0.7873 |
| How do I change the oil in a diesel engine? | No | 0.9228 |
| Who won the 1994 World Cup? | No | 0.8474 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8243 |
| How do I write a for loop in Rust? | No | 0.8768 |

## How I Used AI

**1.** I asked an AI tool to pressure-test my acceptance criteria by explaining
how each one could be checked from its wording alone. It pointed out that
"useful thought" was subjective, so I changed the chunk criterion to require a
complete answer-bearing sentence and a measurable result for at least 4 of 5
sampled chunks.

**2.** I asked an AI tool to help me choose a chunking strategy after I read the
short `campus_life` documents and measured their paragraph lengths. It suggested
paragraph-aware chunks, but I chose the final details myself: attach each title
to its first paragraph, use no overlap, and keep the observed maximum under a
400-character target. I implemented and checked the function against the
generated chunks before documenting five samples.

**3.** In unit 2, I used an AI tool to inspect the retrieval path and compare
the before and after evidence. It suggested hybrid BM25 plus semantic ranking
because my stricter diagnosis focused on exact terms and rank-1 precision. I
kept the implementation decision myself, caught and fixed an initial score-
alignment bug with a focused retrieval check, and then ran the full evaluation.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

Submission evidence: the completed criterion tables below summarize the saved
[before transcript](results/run_2026-09-30_1721_before.md) and
[after transcript](results/run_2026-09-30_1809_after.md), each with three actual
uncached generation runs per question. The blank question-level score cells
in those raw reports mean no automatic scorer was installed; the answers
below them are present and were assessed for the criterion tables here.

**Criteria revisions:** None. The original targets in `criteria.md` remain
unchanged. The proposed rank-1 target below is a future tightening, not a
replacement used to grade these runs. No second-improvement stretch is claimed.

**Evidence audit, October 6, 2026:**
`tools/audit_unit2.py::main` checked the saved answers and repeated retrieval
against the current index with the real MiniLM model on CPU. This audit makes
no generation calls and is not a new set of three generation runs. Its full
text output is in [unit2_evidence_audit.txt](results/unit2_evidence_audit.txt).
The historical reports saved source filenames but not chunk bodies, so the
chunk excerpts below are explicitly supplementary current-index evidence.


## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer-bearing chunks are complete | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected phrase | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The raw run output is in `results/run_2026-09-30_1721_before.md`, produced by
`run_eval.py::main`. The answers were generated by `generate.py::answer_from_chunks`, called by
`run_eval.py::run_once`. The generated answers from run 1 were:

```
For juniors and seniors, the housing lottery order is decided by accumulated credit hours first, with random tie-breaking used if there is a tie.

Source: admin_housing_lottery.txt

You can change your meal plan tier once in the first ten days of the semester before it is locked. When you downgrade, the difference is refunded to your student account.

Source: admin_meal_plan_changes.txt

Each student receives $30 of printing credit per semester.

Source: `admin_printing_quota.txt`

Your student account stays active for six months after you graduate (admin_wifi_and_accounts.txt).

You should expect to spend 8 to 10 hours a week outside class for CS 210.

Source: `course_cs_210.txt` and `course_cs_210_workload.txt`
```

The same file records the retrieved source lists for criterion 1, the source
names in every answer for criterion 2, and the deterministic gate output from
`run_eval.py::check_out_of_scope`: `gate refused 5 of 5`. Criteria 4 and 5
were checked against the retrieved chunks and the `expects` phrases in
`questions.py`; all five questions passed in each run.

### Text evidence for all five criteria

**Criteria 1 and 4 — retrieved answer-bearing chunks.** The current-index
retrieval audit printed the five hybrid rank-1 chunks below; each contains
the answer and ends with a complete sentence. Semantic rank-1 chunks also
passed this manual inspection (including `course_cs_210.txt#1`, printed in
the audit). Source presence in the historical logs supports the original
retrieval assessment, but does not by itself prove which chunk was returned.
These fresh excerpts make the chunk check inspectable without pretending
chunk bodies were preserved in the September logs.

Produced by `store.py::search`, chunks from `chunker.py::split_documents`,
printed by `tools/audit_unit2.py::main`:

```
rank-one admin_housing_lottery.txt#0, produced by chunker.py::split_documents:
On the housing lottery

The housing lottery is not random in the way most people assume. Rising sophomores get a number drawn at random, but juniors and seniors are ordered by accumulated credit hours first, and only tie-break randomly. That means a senior who took summer courses reliably beats a senior who didn't. Numbers come out the second week of March and selection runs over four evenings.

rank-one admin_meal_plan_changes.txt#0, produced by chunker.py::split_documents:
On the meal plan changes

You can change your meal plan tier once, in the first ten days of the semester. After that it's locked. Downgrading refunds the difference to your student account; upgrading bills you immediately.

rank-one admin_printing_quota.txt#0, produced by chunker.py::split_documents:
On the printing quota

Every student gets $30 of printing per semester, which is roughly 600 black-and-white pages. It does not roll over. Colour costs eight times as much per page, which people discover after printing one poster.

rank-one admin_wifi_and_accounts.txt#0, produced by chunker.py::split_documents:
On the wifi and accounts

Your student account gives you campus wifi, printing, and a cloud drive with unlimited storage that most people never discover. The account stays active for six months after you graduate, and the cloud drive is purged at that point without a second warning.

rank-one course_cs_210_workload.txt#0, produced by chunker.py::split_documents:
Workload for CS 210 Data Structures

People keep asking so: 8 to 10 hours a week outside class. That's real time, not optimistic time.
```

**Criteria 2 and 5 — source names and expected phrases.** The five saved
Run 1 answers above expose both directly. Checking all three saved runs
produced the following audit output:

```
Saved before report: run_2026-09-30_1721_before.md
Run 1: C2 source named 5/5; C5 expected phrase 5/5
Run 2: C2 source named 5/5; C5 expected phrase 5/5
Run 3: C2 source named 5/5; C5 expected phrase 5/5
C3: saved deterministic gate refused 5/5 (same value in each run column)

Saved after report: run_2026-09-30_1809_after.md
Run 1: C2 source named 5/5; C5 expected phrase 5/5
Run 2: C2 source named 5/5; C5 expected phrase 5/5
Run 3: C2 source named 5/5; C5 expected phrase 5/5
C3: saved deterministic gate refused 5/5 (same value in each run column)

```

**Criterion 3 — gate output.** The before report records these distances and
decisions from `run_eval.py::check_out_of_scope`, using `gate.py::check`:

```
What is the capital of Mongolia? | 0.787 | refused
How do I change the oil in a diesel engine? | 0.923 | refused
Who won the 1994 World Cup? | 0.847 | refused
What is the recommended dosage of ibuprofen for a headache? | 0.824 | refused
How do I write a for loop in Rust? | 0.877 | refused
Refused 5 of 5.
```

The gate is deterministic; its single measured total is repeated in the
three run columns as the starter instructs. The generation criteria use
three separate saved answers per question, not duplicated answers.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer for at least 4 of 5 questions | MET | Each of the three runs retrieved an answer-bearing source for all five questions, so the result was 5/5 every time. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source document, meeting the 5/5 target in every run. |
| 3 | The relevance gate stops out-of-corpus questions in at least 4 of 5 cases | MET | The deterministic gate refused all five out-of-corpus questions, giving 5/5 against the target of 4/5. |
| 4 | At least 4 of 5 sampled chunks contain a complete answer-bearing sentence | MET | The recorded assessment was 5/5 in each run. Fresh inspection of five chunks confirms 5/5 complete answer-bearing passages; historical chunk bodies were not saved, so that part is supported by reconstruction. |
| 5 | At least 4 of 5 answers contain the expected phrase | MET | Each run contained all five expected phrases from `questions.py`, so every run scored 5/5. |

## Diagnoses

No criteria were missed, so there is no observed failure to assign to a
pipeline stage. The closest useful diagnosis is that the targets were
conservative: all five questions passed all five checks, while four original
targets allowed 4/5 and criterion 1 counted any answer-bearing chunk in the
top five. The evaluation therefore did not expose a loading, chunking,
embedding, retrieval, or generation failure.

The pattern is a strong but small result rather than evidence that every stage
is robust. The corpus questions are specific and the relevant documents are
short, so this test set may be easier than a larger or noisier set would be.
The criterion I would tighten is criterion 1: require the top-ranked result
(rank 1, not merely any of the top five) to contain the answer for all 5 of 5
questions across all three runs. That keeps the measurement objective while
testing retrieval precision more strictly.

## The Improvement

**What I changed:** I added BM25 keyword reranking in `store.py::search`,
combining normalized keyword scores with the existing semantic scores. The
semantic distance is still preserved for the relevance gate.

**Why I picked it:** The diagnosis identified a lenient retrieval target, so
this was an exploratory change at the **retrieval** stage. BM25 rewards exact
query-token matches such as `CS 210`, `printing`, and `meal plan`; combining
that signal with semantic similarity might promote the answer-bearing chunk.
This is a proposed mechanism, not an observed baseline failure. The facts
`$30` and `six months` are answer terms, not tokens in their questions, so
keyword matching cannot directly reward those facts for these queries.

The after-run evidence is in
`results/run_2026-09-30_1809_after.md`, produced by
`run_eval.py::main`. A focused rank-1 check placed an answer-bearing chunk
first for all five questions (5/5).

### Run Log — After

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer-bearing chunks are complete | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected phrase | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

**No measurable improvement on this test set.** Every original criterion
remained 5/5 in Run 1, Run 2, and Run 3 before and after: a change of 0/5.
The supplementary rank-1 audit also scored semantic search 5/5 and hybrid
search 5/5, a change of 0/5. Both saved gate evaluations refused 5/5 unrelated
questions. The change preserved measured performance but did not establish
a benefit. A perfect hybrid score alone does not show improvement over an
already-perfect baseline.

## What's Still Broken

No original criterion was missed after the hybrid-search change, so there is
no criterion-specific fix left to make. The remaining limitation is confidence:
the evaluation has only five hand-written in-scope questions and five
out-of-scope questions, all from a small corpus. I stopped after one targeted
improvement because the assignment calls for measuring one change, and the
after run preserved 5/5 on every criterion. A larger evaluation set with
paraphrases, ambiguous wording, and distractor documents would be the next
check before calling the system robust.

## What I'd Do Differently

I would write criterion 1 more strictly in the next unit: the answer-bearing
chunk must be rank 1 for all 5 of 5 questions across all three runs, rather
than allowing the answer anywhere in the top five and accepting 4 of 5. That
would measure retrieval precision directly and make a perfect result more
meaningful. I would also prepare a few paraphrased questions before evaluating
so the test does not mostly reward matching the wording of the corpus.
