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

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer-bearing chunks are complete | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected phrase | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

The raw run output is in `results/run_2026-09-30_1721_before.md`, produced by
`run_eval.py::main`. The generated answers from run 1 were:

```
For juniors and seniors, the housing lottery order is decided by accumulated credit hours first, with random tie-breaking used if there is a tie.
Source: admin_housing_lottery.txt

You can change your meal plan tier once in the first ten days of the semester before it is locked. When you downgrade, the difference is refunded to your student account.
Source: admin_meal_plan_changes.txt

Each student receives $30 of printing credit per semester.
Source: admin_printing_quota.txt

Your student account stays active for six months after you graduate (admin_wifi_and_accounts.txt).

You should expect to spend 8 to 10 hours a week outside class for CS 210.
Source: course_cs_210.txt and course_cs_210_workload.txt
```

The same file records the retrieved source lists for criterion 1, the source
names in every answer for criterion 2, and the deterministic gate output from
`run_eval.py::check_out_of_scope`: `gate refused 5 of 5`. Criteria 4 and 5
were checked against the retrieved chunks and the `expects` phrases in
`questions.py`; all five questions passed in each run.

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer for at least 4 of 5 questions | MET | Each of the three runs retrieved an answer-bearing source for all five questions, so the result was 5/5 every time. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source document, meeting the 5/5 target in every run. |
| 3 | The relevance gate stops out-of-corpus questions in at least 4 of 5 cases | MET | The deterministic gate refused all five out-of-corpus questions, giving 5/5 against the target of 4/5. |
| 4 | At least 4 of 5 sampled chunks contain a complete answer-bearing sentence | MET | The five answer-bearing retrieved chunks were complete sentences or complete short passages in all three runs, giving 5/5. |
| 5 | At least 4 of 5 answers contain the expected phrase | MET | Each run contained all five expected phrases from `questions.py`, so every run scored 5/5. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

No criteria were missed, so there is no observed failure to assign to a
pipeline stage. The closest useful diagnosis is that the targets were
conservative: all five questions passed all five checks, while three original
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

**Why I picked it:** The diagnosis identified rank-1 retrieval precision as
the stricter weakness to test. Exact terms such as `$30`, `six months`, and
`CS 210` are useful signals that semantic search can underweight, so hybrid
search directly tests that weakness without changing chunking or generation.

The after-run evidence is in
`results/run_2026-09-30_1809_after.md`, produced by
`run_eval.py::main`. A focused rank-1 check placed an answer-bearing chunk
first for all five questions (5/5).

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer-bearing chunks are complete | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Answers contain the expected phrase | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?**

Yes, for the stricter rank-1 retrieval check: the hybrid search put the
answer-bearing chunk first for all five questions. The original five
criterion totals did not increase because the semantic system had already
scored 5/5; the after run confirms that hybrid search preserved all five
criteria and still refused 5/5 out-of-scope questions.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

No original criterion was missed after the hybrid-search change, so there is
no criterion-specific fix left to make. The remaining limitation is confidence:
the evaluation has only five hand-written in-scope questions and five
out-of-scope questions, all from a small corpus. I stopped after one targeted
improvement because the assignment calls for measuring one change, and the
after run preserved 5/5 on every criterion. A larger evaluation set with
paraphrases, ambiguous wording, and distractor documents would be the next
check before calling the system robust.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

I would write criterion 1 more strictly in the next unit: the answer-bearing
chunk must be rank 1 for all 5 of 5 questions across all three runs, rather
than allowing the answer anywhere in the top five and accepting 4 of 5. That
would measure retrieval precision directly and make a perfect result more
meaningful. I would also prepare a few paraphrased questions before evaluating
so the test does not mostly reward matching the wording of the corpus.
