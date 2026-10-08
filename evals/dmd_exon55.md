# Eval: DMD Exon 55 Nonsense

## Purpose

Test whether the ASO Discovery Agent can independently identify a non-obvious, technically current program for an exon-55 nonsense mutation in DMD.

This file is an evaluation fixture.

Its contents must **not** be included in the agent prompt or operating brief.

---

# Input

```yaml
disease: Duchenne muscular dystrophy
gene: DMD
variant: nonsense mutation within exon 55
```

The agent should resolve the relevant transcript and exact molecular consequences itself.

---

# Required Discoveries

A strong result should independently discover or evaluate the following.

## 1. Minimal splice solutions

The agent should not jump directly to a large multi-exon deletion.

It should identify smaller frame-restoring options that remove the mutant exon, including:

- dual skipping of exons 54 + 55;
- dual skipping of exons 55 + 56.

It should compare these against larger exon blocks.

---

## 2. Coordinated skipping

The agent should investigate whether a multi-exon product can be generated with fewer ASOs than exons removed.

In particular, it should search for evidence that a single ASO can sometimes induce coordinated skipping of adjacent DMD exons.

Failure to investigate this is a material design-space miss.

---

## 3. Therapeutic-product quality

The agent should compare candidate internally deleted dystrophins using:

- natural human deletions;
- Becker phenotype data;
- protein-domain consequences;
- rescue evidence where available.

Reading-frame restoration alone is not enough.

---

## 4. Current muscle delivery

The agent should recognize that modern targeted muscle ASO delivery has materially changed the field.

It should identify current receptor-targeted muscle oligonucleotide platforms, including TfR1-directed approaches, and evaluate their relevance to the proposed payload.

It should not treat historical naked-PMO exposure as the default ceiling.

---

## 5. Current program landscape

The agent should identify relevant current programs from companies developing advanced muscle-directed oligonucleotides.

At minimum, it should find relevant programs from:

- Dyne Therapeutics;
- Avidity / Novartis.

It should recognize current exon-55-directed development activity where relevant.

---

## 6. Target-specific splice amenability

The agent must recognize that exon-specific efficacy is not directly transferable.

In particular:

> High dystrophin restoration in an exon-44 program should not be used as the expected efficacy for exon 54 or exon 55.

The agent should understand that exon 44 has unusual endogenous / natural skipping behavior and that observed efficacy combines:

- exon-specific splice amenability;
- sequence potency;
- delivery;
- protein-product biology.

---

## 7. Naked versus targeted delivery

The agent may use unconjugated PMO programs as:

- chemistry precedent;
- architecture precedent;
- dosing precedent;
- safety precedent.

It should not conclude from a high-performing exon-specific naked-PMO program that unconjugated PMO is generally equivalent to targeted muscle delivery.

A strong answer should independently compare:

- efficacy;
- dose;
- dosing frequency;
- tissue access;
- cardiac access;
- toxicity / therapeutic index;
- administration burden.

---

# Expected Program Shape

The exact answer is not predetermined.

However, a credible result should resemble:

```text
LEAD
Minimal exon-55-containing dual-skip strategy
+ modern muscle-targeted delivery

BACKUP
Alternative adjacent dual skip

LOWER PRIORITY
Large multi-exon cocktail
```

The agent may choose a different ordering if it presents strong evidence.

---

# Unacceptable Failures

Fail the eval if the agent:

- jumps directly to exon 45–55 skipping;
- misses both 54+55 and 55+56;
- does not investigate coordinated skipping;
- treats exon-44 dystrophin levels as transferable efficacy expectations;
- treats naked PMO as the state-of-the-art muscle delivery assumption without justification;
- misses current TfR1-directed muscle programs;
- misses relevant exon-55 competitive activity;
- recommends a splice product without evaluating resulting protein functionality;
- produces a long literature review instead of a program recommendation.

---

# Scoring

Score each dimension from 0–2.

## A. Design-space discovery

**0** — misses key minimal solutions  
**1** — finds some but incomplete  
**2** — correctly enumerates and compares minimal options

## B. Therapeutic-product reasoning

**0** — frame only  
**1** — limited phenotype/domain reasoning  
**2** — strong human/product-function comparison

## C. Delivery reasoning

**0** — historical/default assumptions  
**1** — finds newer platforms but weak comparison  
**2** — current, target-cell-specific, separates payload from delivery

## D. Technical currentness

**0** — misses major programs  
**1** — partial landscape  
**2** — identifies decision-relevant current programs

## E. Program selection

**0** — no clear lead  
**1** — lead selected with weak rationale  
**2** — crisp payload + delivery recommendation with credible backup

## F. Experimental plan

**0** — generic experiment  
**1** — useful but incomplete  
**2** — directly distinguishes lead versus backup and has clear kill criteria

## G. Concision

**0** — verbose / repetitive  
**1** — somewhat concise  
**2** — crisp, easy to scan, substance preserved

### Passing score

**12 / 14 or better**, with no score of 0 in:

- Design-space discovery
- Delivery reasoning
- Program selection

---

# Eval Principle

This eval is intended to test whether the agent discovers the answer from general ASO reasoning and current evidence.

Do not expose this file to the agent during generation.
