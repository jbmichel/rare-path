# Eval result: 13/16 — FAIL

| Dimension | Score | Evidence |
|---|---|---|
| A_framing_product | 2 | "too little functional protein per neuron, not one correctable splicing error"; "restored a reading frame would therefore deliver a disease protein"; skewed-XCI girls as lower bound; "stays well below the level in people carrying CDKL5 duplications"; 1.5–2 fold target. |
| B_design_space | 1 | Main answer offers only three mechanisms (non-productive splicing, +5 variant correction, XIST). Regulatory-RNA/enhancer and 5'UTR/TSS appear only as a single appendix WATCH row; no flux-increase vs flux-redistribution distinction, no cross-mechanism comparison at decision level. |
| C_existence_risk | 2 | "The payload may not exist"; CDKL5 absent from 2025 12,014-PE atlas; ~10% in-frame productive and <5% exon-11 quantified as insufficient; NMD-inhibited long-read gate with 10% kill criterion; intron-16 +5 "80% of correct splicing" hazard plus counter-screen. |
| D_transferability | 2 | "It sets our dosing schedule and safety expectations, but says nothing about how well our payload will work"; appendix: "SCN1A has a validated, highly included NMD exon... The SCN1A productive-mRNA headroom simply does not exist here." |
| E_currentness | 1 | Competitive landscape strong (NGN-401 halt, stalled AAV, split-dCas9 CDKL5 reactivation). But CAMP4 captured only as "CMP-002 (SYNGAP1, first-in-human cleared 2026)" — no ~1.5-fold NHP brain rise, no mouse rescue, no Phase 1 platform safety, no GSK, no honest-cost comparison. |
| F_delivery | 2 | ">ten-fold lower than in cortex and spinal cord"; nusinersen autopsy brainstem gap; names "hippocampus, deep cerebellar layers and interneurons in deep structures"; "must be measured in primates before lead nomination." |
| G_experiment | 2 | Het female + hemizygous male + isogenic iPSC, cortical and interneuron fates, SMG1-inhibitor arm, no transfection reagent, targeted long-read absolute productive fraction, pEB2-S222 kinase surrogate, no exon-16-skipped increase, quantitative kill criterion. |
| H_concision_evidence | 1 | 1286 words, scannable. Good flagging (data-free patent, DMD exon-16 false conflation, unretrievable preprint). But the load-bearing duplication ceiling is marked "(search snippet, full text not verified)" yet asserted as fact; absence is never distinguished from pipeline-filter exclusion. |

## Unacceptable failures
- [ok] proposes reading-frame restoration or exon skipping as the therapeutic strategy — Explicitly contraindicates frame restoration; P7/P8 truncation comparators rejected as disease proteins.
- [ok] proposes poison-exon suppression as the only mechanism considered — XIST reactivation and +5 variant correction carried as named backups.
- [ok] misses regulatory-RNA / enhancer-directed upregulation entirely — Present as appendix WATCH row with CAMP4 SYNGAP1 regRNA ASO cited; absent from main answer, so credit is thin.
- [ok] nominates a lead ASO against a non-productive element without establishing that one exists — Borderline: labels a LEAD and tiles 40 ASOs at a patent-asserted element, but verdict is TEST FIRST and funding is gated on the existence gate.
- [ok] transfers SCN1A / zorevunersen efficacy figures to CDKL5 — Figures explicitly quarantined as dosing/safety precedent; availability named as the non-transferring term.
- [ok] proposes tiling across intron 16 without flagging the +5 donor hazard — Flagged in main answer and enforced as a counter-screen.
- [ok] aims to maximize CDKL5 expression, or omits the duplication-carrier ceiling — Bounded 1.5–2 fold with duplication-carrier ceiling stated.
- [TRIGGERED] claims mutation-agnosticism without addressing mutant-allele upregulation — Repeatedly claims "from the patient's healthy gene copy / non-mutant allele" — biologically false for a splice-switching ASO. No NMD vs stable-truncated stratification anywhere.
- [ok] treats intrathecal delivery as solved and omits the deep-brain gradient — Gradient quantified; under-dosed compartments named; NHP measurement required.
- [ok] claims the competitive space is unoccupied, or misses the AAV safety context — NGN-401 hyperinflammatory SAE, stalled UX055, split-dCas9 epigenome editing all captured.
- [ok] asserts an unverified count or absence as a load-bearing fact — 12,014 count cited to full-text preprint; duplication ceiling asserted in main answer while appendix marks it unverified — looseness, scored in H.
- [ok] claims a sequence model resolves the existence question — No reliance on SpliceAI; existence resolved by NMD-inhibited long-read experiment.
- [ok] produces a long literature review instead of a program recommendation — Clear verdict, lead, backups, gate, kill criteria.

## Required discoveries missed
- Allele non-selectivity (section 6): never confronts that splice-switching raises output from the mutant allele too; misdescribes the product as coming from the 'non-mutant allele' and offers no NMD-vs-stable-truncated stratification
- CAMP4 RAP magnitude evidence (section 5): ~1.5-fold SYNGAP1 protein rise in NHP brain on biweekly intrathecal dosing, mouse ICV rescue, urea-cycle Phase 1 safety, GLP tox/GSK collaboration; SYNGAP1 not identified as the structurally equivalent clinical analogue
- Honest costs of the regRNA mechanism (enhancer-mapping burden, contested eRNA function, multi-gene enhancers vs a narrow dose ceiling, incumbent claim position)
- The decision-relevant distinction that poison-exon suppression redistributes existing pre-mRNA flux while transcriptional upregulation increases it
- Section 10 nuance: 'absent from a candidate list' may reflect conservation/expression filters rather than non-existence
- Parallel handle test across mechanisms in one gate — the first experiment tests two splicing handles only, not regRNA or 5'UTR/TSS handles

Strong on the hard parts: dosage framing, product quality, existence-risk discipline, SCN1A decomposition, delivery depth and a genuinely well-specified gate experiment. Fails on breadth and currentness: regulatory-RNA upregulation survives only as an appendix watch item, CAMP4's SYNGAP1 NHP magnitude evidence is absent, and the program is marketed as mutation-agnostic while asserting the product comes from the 'non-mutant allele' — biologically false and an unaddressed overclaim. 13/16; below the 14 threshold.
