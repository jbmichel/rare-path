# Eval: CDKL5 Loss-of-Function (Mutation-Agnostic)

## Purpose

Test whether the ASO Discovery Agent can handle a **dosage** disease rather than a splice-correction disease.

The DMD exon-55 eval tests design-space breadth within a mechanism the agent already knows is available. This eval tests something harder: whether the agent can recognize that its default ASO mechanism may have **no target in this gene**, enumerate the alternative upregulation mechanisms, and gate the program on an existence experiment instead of asserting a lead.

The failure mode under test is **mechanism anchoring**: reaching for splice-switching because that is what ASOs do, and then reasoning forward from a target that has not been shown to exist.

This file is an evaluation fixture.

Its contents must **not** be included in the agent prompt or operating brief.

---

# Input

```yaml
disease: CDKL5 deficiency disorder
gene: CDKL5
variant: loss-of-function, no specific variant given
```

The agent should resolve the transcript, the X-linked inheritance consequences, and the molecular nature of the deficit itself.

Note that the input deliberately withholds a specific variant. A correct response must either commit to a mutation-agnostic strategy or explicitly stratify by genotype class. Silently assuming one variant class is a failure.

---

# Required Discoveries

A strong result should independently discover or evaluate the following.

## 1. Correct problem framing

The agent must establish that the deficit is **too little functional protein per neuron**, not one correctable splicing error.

It follows that the therapeutic product must be ordinary full-length CDKL5 protein from an intact gene copy.

The agent should reach the consequence that matters for design:

> Reading-frame restoration is contraindicated here, not merely suboptimal.

Truncated CDKL5 proteins are themselves found in severely and moderately affected patients, so an exon-skipping or frame-restoring strategy would deliver a disease protein rather than a drug. An agent that proposes frame restoration without confronting this has failed the core product-quality test.

The agent should also find the natural human dose-response evidence on both sides:

- heterozygous girls whose X-inactivation favours the healthy allele are mild or unaffected, which establishes that a modest per-neuron rise in normal protein is clinically meaningful;
- CDKL5 duplication carriers show autism and developmental delay, which establishes an **upper** bound.

A credible program targets a bounded rise and says so. Maximizing expression is a failure.

---

## 2. Design-space enumeration across upregulation mechanisms

This is the central test.

The agent should not jump directly to poison-exon suppression (TANGO-style) and stop there.

It should enumerate and compare, at minimum:

- suppression of a non-productive / NMD-coupled splicing event;
- **regulatory-RNA / enhancer-directed transcriptional upregulation**;
- 5'UTR, leader-usage or TSS redirection to raise protein output per transcript;
- XIST-directed reactivation of the silenced wild-type allele in heterozygous females;
- variant-specific splice correction for the donor +5 subgroup.

Missing the regulatory-RNA mechanism entirely is a material design-space miss, equivalent in severity to missing coordinated skipping in the DMD eval.

The agent should recognize that these mechanisms differ in a decision-relevant way:

> Poison-exon suppression redistributes an existing pre-mRNA flux. Transcriptional upregulation increases the flux. Only the first requires a specific pre-existing splicing event to exist.

---

## 3. Existence risk, actively tested

The agent must not assume a usable non-productive CDKL5 splicing event exists.

It should actively search for one, find that none has been validated, and quantify why the known events are insufficient rather than asserting it:

- CDKL5 is absent from the 2025 transcriptome-wide brain poison-exon survey;
- the one quantified alternative CDKL5 exon is in-frame and productive at roughly 10% of brain transcripts;
- exon-11 cryptic-donor forms sit under 5%.

The agent should reach the arithmetic consequence: complete suppression of a 5% event recovers almost nothing, so the mechanism needs a target with a large enough waste fraction to clear a 1.5-fold goal.

A strong answer gates the program on an existence experiment. An answer that nominates a lead ASO against an unidentified element is a failure regardless of how well the rest is argued.

The agent should also identify the **iatrogenic risk** in the obvious tiling region: a single change at the intron-16 donor +5 position removes roughly 80% of correct splicing, so an ASO walk there can induce the exon-16-skipped degraded transcript. Proposing a blind tile across that intron without flagging this is a failure.

---

## 4. Non-transferable efficacy — the SCN1A trap

This is the direct analogue of the exon-44 lesson in the DMD eval.

The agent will encounter zorevunersen. It must separate what that program does and does not license.

Acceptable use of the precedent:

- intrathecal pediatric dosing schedule (loading then maintenance);
- CSF safety expectations and monitoring;
- chemistry and architecture precedent;
- regulatory path shape.

Unacceptable use:

> Treating SCN1A upregulation efficacy as the expected efficacy for CDKL5.

The agent should understand that TANGO worked on SCN1A because SCN1A has a well-characterized, highly utilized poison exon. The observed clinical effect is a product of poison-exon availability, sequence potency, delivery and target biology. Only the last two transfer. Availability is exactly the term that is unestablished in CDKL5, and it is the term that dominates.

An agent that quotes SCN1A protein-rise figures as a CDKL5 expectation fails this dimension outright.

---

## 5. Current upregulation platform landscape

The agent should recognize that ASO-mediated gene upregulation is no longer splice-modulation-only, and should identify current regulatory-RNA-directed programs.

At minimum it should find CAMP4's RAP platform and evaluate its relevance, including the closest clinical analogue:

- SYNGAP1-related disorder — autosomal haploinsufficiency, infantile-onset epilepsy with severe developmental impairment, no approved therapy. Structurally the same therapeutic problem as CDD.
- roughly **1.5-fold SYNGAP1 protein increase in non-human primate brain** across multiple disease-relevant regions on biweekly intrathecal dosing, with dose-linear exposure;
- single ICV dose restoring protein to near-normal range in haploinsufficient mice, two doses rescuing motor and spatial learning deficits;
- platform-level clinical safety from the urea cycle program (Phase 1 SAD, 48 subjects, no MTD, all TEAEs Grade 1–2);
- GLP toxicology initiated for the SYNGAP1 candidate, trial start guided, and a GSK collaboration.

The agent should recognize the significance of the NHP number: it is approximately the target rise, by a different mechanism, in primate brain, by the intended route. This is the strongest available external evidence that the *magnitude* goal is achievable, and it is mechanism-independent.

The agent should also surface the honest costs of this mechanism rather than only its appeal:

- regRNA targets cannot be found from sequence, so it converts a design problem into an enhancer-mapping and screening problem;
- eRNA function is contested and no approved drug works this way;
- enhancers may regulate more than one gene, which interacts badly with a narrow dose ceiling;
- the incumbent has a proprietary catalog, a pharma partner and a claim position in CNS haploinsufficiency — the stated focus area that CDD sits inside.

Finding the platform but treating it as unambiguously superior is incomplete. Finding it and comparing it honestly is the target behavior.

---

## 6. Allele non-selectivity

The agent should recognize that **every** mechanism in section 2 except XIST reactivation and variant-specific correction raises output from both alleles.

It should connect this to its own product argument from section 1: if truncated CDKL5 protein is pathogenic, then boosting transcription of a mutant allele that produces stable truncated protein is not neutral.

The agent should reach the consequence that mutation-agnosticism is **cleaner in claim than in biology**, and that the honest position is stratification by whether the patient's mutant transcript is NMD-degraded or produces stable protein.

An agent that markets its approach as mutation-agnostic without confronting this has overclaimed.

---

## 7. CNS delivery depth, measured not assumed

The agent should identify the real ceiling on intrathecal oligonucleotide programs for a disorder needing broad neuronal coverage:

- oligonucleotide levels in monkey deep brain run more than ten-fold below cortex and spinal cord;
- human autopsy after nusinersen shows a gradient from spinal cord upward with little drug in the brainstem.

It should name the under-dosed compartments that matter for this disease — hippocampus, deep cerebellar layers, interneurons in deep structures — and require that coverage be measured in primates rather than assumed before lead nomination.

It should not treat CSF delivery as a solved problem because an approved CSF drug exists.

---

## 8. Competitive landscape beyond oligonucleotides

The agent should establish that the "raise CDKL5 from the intact or silenced allele" thesis is occupied, and should use that landscape to support its modality choice rather than ignoring it.

At minimum:

- AAV gene-replacement programs in this disease have stalled or been dose-limited;
- the high-dose cohort of the NGN-401 AAV trial in Rett syndrome was halted for a hyperinflammatory serious adverse event;
- CRISPR-based epigenome editing — split dCas9 with simultaneous transcriptional activation and promoter demethylation, delivered by AAV9 — has restored Cdkl5 protein and rescued motor and cognitive deficits in heterozygous E6del mice, and normalized network activity in patient organoids.

The agent should draw the differentiation argument correctly: a redosable, titratable CSF oligonucleotide has a genuine safety and dose-control advantage over AAV in this population, which is a real claim rather than a modality preference. It should not claim the space is empty.

---

## 9. Computational reasoning, if proposed

If the agent proposes in silico prediction to resolve the existence question, it must reason correctly about tool fit.

It should distinguish:

- **variant-effect predictors** (SpliceAI, SpliceAI2 in its primary mode) — require a ref/alt pair and answer "how much does this change perturb splicing";
- **usage / isoform quantification** — answers "what fraction of reference transcripts take this path", which is the quantity the kill criterion is written in.

It should identify the blind spot that matters:

> Models trained on annotation and short-read RNA-seq systematically under-represent NMD-degraded isoforms, because NMD destroys them before sequencing. The class of event being hunted is depleted from the training signal.

The correct consequence is asymmetric reading: a positive prediction is informative, a negative prediction is weak evidence, and computation cannot substitute for the NMD-inhibited long-read readout.

A strong answer should also propose mining before predicting — NMD-perturbation RNA-seq (UPF1/SMG1 knockdown), long-read brain transcriptomes, junction-level resources, curated NMD-target databases — and conservation-first candidate finding, since poison exons are unusually conserved for intronic sequence.

Claiming that SpliceAI or SpliceAI2 alone answers the existence question is a failure of this dimension.

---

## 10. Citation hygiene on load-bearing numbers

The agent's kill criterion rests on a published absence. It should verify such a claim against the primary source rather than the abstract or a secondary summary.

It should also recognize what an absence does and does not mean:

> "Absent from a candidate list" may mean no poison exon exists, or may mean the discovery pipeline's conservation and expression filters excluded it. These have different implications for whether to fund the experiment.

An agent that states a specific count or an absence it did not check, or that treats an absence as proof of non-existence, loses this dimension.

---

# Expected Program Shape

The exact answer is not predetermined.

A credible result should resemble:

```text
VERDICT
TEST FIRST — no mechanism nominated as lead until a handle is shown to exist

PARALLEL HANDLE TEST (single model system, one gate)
  non-productive splicing event
  regRNA / enhancer-directed upregulation
  5'UTR / TSS / leader-usage redirection

PRE-VALIDATED FALLBACK
  variant-specific +5 donor-site correction
  (carries the only quantitative CDKL5 rescue data; serves a small named subgroup)

CONTINGENT ON SELECTIVITY
  XIST-directed reactivation
  (genome-wide rather than CDKL5-specific; cannot help hemizygous males)
```

The agent may order these differently or commit to a single handle, but only with evidence that the handle exists.

A confident single-mechanism LEAD with no existence evidence scores worse than a well-argued TEST FIRST.

---

# First-Experiment Requirements

A strong answer's first experiment should include:

- patient-derived iPSC neurons across both relevant genotype contexts (heterozygous female and hemizygous male) with isogenic controls;
- differentiation to more than one relevant neuronal fate, including interneurons;
- an **NMD-inhibited arm**, since the target class is otherwise invisible;
- long-read or otherwise isoform-resolving readout giving absolute productive-isoform fraction, not just relative junction ratios;
- a **functional** protein readout, not abundance alone — kinase-activity surrogate alongside protein level;
- gymnotic delivery (no transfection reagent), so the result predicts free uptake;
- an explicit specificity criterion — no new off-target isoform above threshold, and specifically no increase in the degraded exon-16-skipped species;
- a quantitative kill criterion tied to the arithmetic in section 3.

An experiment that measures protein without measuring isoform structure, or isoform structure without measuring function, is incomplete.

---

# Unacceptable Failures

Fail the eval if the agent:

- proposes reading-frame restoration or exon skipping as the therapeutic strategy;
- proposes poison-exon suppression as the only mechanism considered;
- misses regulatory-RNA / enhancer-directed upregulation entirely;
- nominates a lead ASO against a non-productive element without establishing that one exists;
- transfers SCN1A / zorevunersen efficacy figures to CDKL5;
- proposes tiling across intron 16 without flagging the +5 donor hazard;
- aims to maximize CDKL5 expression, or omits the duplication-carrier ceiling;
- claims mutation-agnosticism without addressing mutant-allele upregulation;
- treats intrathecal delivery as solved and omits the deep-brain gradient;
- claims the competitive space is unoccupied, or misses the AAV safety context;
- asserts an unverified count or absence as a load-bearing fact;
- claims a sequence model resolves the existence question;
- produces a long literature review instead of a program recommendation.

---

# Scoring

Score each dimension from 0–2.

## A. Problem framing and product quality

**0** — treats this as a splice-correction problem, or proposes frame restoration
**1** — correct framing, weak product-quality reasoning
**2** — dosage framing, canonical-protein-only product, both human dose bounds established

## B. Design-space discovery

**0** — single mechanism considered
**1** — two or three mechanisms, incomplete comparison
**2** — enumerates the full upregulation space and compares on existence risk, discovery burden and selectivity

## C. Existence-risk discipline

**0** — assumes a target exists
**1** — notes uncertainty but proceeds as if resolved
**2** — actively tests, quantifies why known events are insufficient, gates the program

## D. Transferability reasoning

**0** — imports SCN1A efficacy as a CDKL5 expectation
**1** — hedges without decomposing why it does not transfer
**2** — separates dosing/safety/chemistry precedent from efficacy, and names poison-exon availability as the non-transferring term

## E. Technical currentness

**0** — misses regulatory-RNA platforms and current competitive activity
**1** — partial landscape
**2** — identifies decision-relevant current programs including the closest clinical analogue, with honest costs

## F. Delivery reasoning

**0** — assumes CSF delivery is solved
**1** — notes the gradient without naming consequences
**2** — identifies under-dosed compartments for this disease and requires primate measurement before lead nomination

## G. Experimental plan

**0** — generic experiment
**1** — useful but missing the NMD arm or the functional readout
**2** — distinguishes handles in one gate, NMD-inhibited, isoform-resolving, functional, with specificity and kill criteria

## H. Concision and evidence hygiene

**0** — verbose, or asserts unverified load-bearing facts
**1** — somewhat concise, minor sourcing looseness
**2** — crisp and scannable, load-bearing claims verified, absences read correctly

### Passing score

**14 / 16 or better**, with no score of 0 in:

- Design-space discovery
- Existence-risk discipline
- Transferability reasoning

---

# Grader Reference Notes

Figures the agent should land near, for checking its work. Verify against primary sources before using these to mark down a response — several are preprint-stage and version-dependent.

| Claim | Value | Note |
|---|---|---|
| Target protein rise | 1.5–2 fold | bounded above by duplication phenotype |
| CDKL5 in brain poison-exon survey | absent | survey count differs between preprint versions; verify |
| Quantified alternative CDKL5 exon | ~10% of brain transcripts | in-frame, productive — not a handle |
| Exon-11 cryptic-donor forms | <5% | too small to matter |
| Intron 16 donor +5 single change | ~80% loss of correct splicing | iatrogenic hazard |
| U1 snRNA rescue, +5 donor variants | >70% CDKL5 protein restored | kinase activity and dendrite morphology also rescued; fails for +1 variants |
| CAMP4 SYNGAP1 NHP protein rise | ~1.5-fold | biweekly intrathecal, multiple brain regions |
| Monkey deep brain vs cortex ASO levels | >10-fold lower | plus brainstem gap in human nusinersen autopsy |
| Zorevunersen pediatric dosing | 2 × 70 mg load, then 45 mg q4mo | intrathecal, ages 2 to <18 |

---

# Eval Principle

This eval tests whether the agent reasons from the **disease mechanism** to the mechanism of action, rather than from its available modality to a target.

The DMD eval rewards finding the smallest sufficient splice solution. This eval rewards something closer to the opposite: recognizing when the familiar solution has no footing in this gene, saying so, and designing the experiment that would settle it.

A response that is confident and wrong about mechanism should score below a response that is uncertain and correct about what is unknown.

Do not expose this file to the agent during generation.
