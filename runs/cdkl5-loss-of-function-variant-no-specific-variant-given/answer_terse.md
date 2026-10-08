# CDKL5 loss-of-function variant (no specific variant given)

**Verdict: TEST FIRST**

## Recommendation

**LEAD — CDKL5-UP: mutation-agnostic 2'-MOE PS steric-block ASO raising full-length hCDKL5_1 from the non-mutant allele by suppressing a non-productive CDKL5 splicing event (exon-20 3'-terminal isoform, or intron-16 "exon 16x"), intrathecal bolus, funded only through a payload-existence gate.**

Product and route are the best available: unmodified canonical 960-aa CDKL5 from a healthy allele, one mutation-agnostic oligo, plain intrathecal 2'-MOE already dosed in children. The payload is not: no validated CDKL5 non-productive or NMD-coupled event was retrieved. Fund a six-month existence-and-magnitude experiment, not a program.

## Why this design

- Only option delivering canonical brain protein from the patient's own allele: zero domain cost, covers males and females, single oligo.
- Redosable CSF oligo differentiates on safety where AAV-CDKL5 cannot be titrated or withdrawn.
- Chemistry, pediatric intrathecal schedule and FDA acceptance of ASO upregulation with non-seizure endpoints are all precedented.

## Delivery

Naked 2'-MOE PS 18-20mer, lumbar intrathecal bolus: two loading doses then q4 months, the zorevunersen schedule run in ages 2 to under 18. Accept the exposure gradient rather than engineering around it: NHP deep-brain accumulation is >10-fold below cortex and cord, and nusinersen autopsy shows a caudal-to-rostral gradient with little brainstem or deep cortical drug. Hippocampus, deep cerebellum and deep-structure GABAergic interneurons must therefore be measured in NHP, not assumed. Retina is unreachable intrathecally — drop it unless a visual endpoint becomes pivotal, then as a separate intravitreal arm.

## Backup

- **Variant-specific splice-correcting ASO for CDKL5 +5 donor alleles (c.2376+5G>A exon 16; c.99+5G>A exon 3).** Holds the only quantitative CDKL5 rescue data and an open, unclaimed n-Lorem individualised intrathecal route, but serves a small named subgroup and the demonstrated modality was U1 snRNA, not an oligo.
- **Xist-targeting ASO, with or without a DNA-methylation inhibitor, to reactivate wild-type CDKL5 on the inactive X.** Natural proof of concept is exact — favourably skewed females are mild or unaffected, and dual-AAV dCas9-TET1 work converges — but Xi reactivation is genome-wide non-selective, CDKL5-specific evidence was unretrievable, and hemizygous males are excluded.

## Critical risk

The binding risk is payload existence, not delivery. CDKL5 is absent from a 2025 transcriptome-wide brain poison-exon atlas, and the only "exon 16x" claim is a patent with no sequences or expression data. The one quantified alternative exon (16b/17) is in-frame and productive at ~10% of brain transcripts and exon-11 cryptic-donor isoforms are <5%, so even complete suppression caps recoverable productive mRNA far below SCN1A. Exon 16's donor loses ~80% of correct splicing to a single +5 change, so intron-16 walking can itself create the exon-16-skipped NMD species. Stoke's MECP2 TANGO program, the only ASO-upregulation attempt in an X-linked NDD, was discontinued without published potency.

## First experiment

- **Model:** CDD patient iPSC neurons in cortical excitatory and GABAergic fates: at least two heterozygous female lines, one hemizygous male, isogenic controls. Gymnotic dosing at three concentrations, each arm with and without SMG1 inhibition.
- **Constructs:** ~40 fully 2'-MOE PS 18-20mers at 5-nt steps across the intron-16 candidate exon and the exon-20 3'-terminal region including its polyA signal. Plus one two-arm linked oligo (brogidirsen architecture) and chemistry-matched controls.
- **Primary readout:** Targeted long-read sequencing of full-length transcripts for absolute productive hCDKL5_1 fraction and the whole isoform distribution, paired with CDKL5 protein by capillary immunoassay and pEB2-Ser222. ddPCR is confirmatory only.
- **Success:** At least 1.5-fold CDKL5 protein with concordant pEB2-Ser222 rise in heterozygous female neurons at 5 micromolar or below, plus a matching long-read gain in productive hCDKL5_1. No new isoform above 5% of transcripts and no rise in the exon-16-skipped NMD species.
- **Kill:** Stop the mutation-agnostic track if NMD-inhibition long reads show no NMD-coupled CDKL5 isoform at 10% or more of baseline transcripts, or if the best oligo gives under 1.3-fold protein. Budget then moves to the +5 backup.
- **Then, delivery:** Single intrathecal bolus of the winning human-cross-reactive sequence in NHP, measuring productive isoform share and CDKL5 protein separately in cortex, hippocampus, cerebellum, brainstem and cord at 4 and 12 weeks, with CSF protein and histopathology.

## Key precedents

- CDKL5 absent from 12,014 putative brain poison exons — the mutation-agnostic payload has no validated handle, so gate rather than launch.
- Engineered U1 restored >70% CDKL5 protein, kinase activity and dendritic morphology for +5 donor variants but failed at +1 — defines and bounds the backup.
- Zorevunersen: two 70 mg intrathecal loads then 45 mg q4mo, Phase 3 fully enrolled, CSF protein elevation main finding — dosing and safety template only.
- NHP deep-brain ASO accumulation >10-fold below cortex/cord plus nusinersen caudal-to-rostral autopsy gradient — hippocampal and brainstem coverage must be measured.
- Neurogene NGN-401 high-dose cohort halted for HLH-like SAE in Rett; UX055 IND delayed on dosing — a redosable CSF ASO has a real differentiation claim.
