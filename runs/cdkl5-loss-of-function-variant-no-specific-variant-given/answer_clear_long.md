# CDKL5 loss-of-function variant (no specific variant given)

**Verdict: TEST FIRST**

## Recommendation

**LEAD — We propose a mutation-agnostic antisense oligonucleotide that raises normal CDKL5 protein from the patient's healthy gene copy by blocking a wasteful splicing event, but we fund only a six-month experiment to test whether such an event exists in human neurons.**

- CDKL5 deficiency disorder is a severe infantile-onset epilepsy and developmental disorder caused by loss-of-function mutations in the X-linked gene CDKL5. The defect is therefore too little functional protein per neuron, not one correctable splicing error.
- The product we want is more of the ordinary 960-amino-acid brain CDKL5 protein made from the patient's non-mutant allele, which works whatever mutation the patient carries and covers both girls and hemizygous boys.
- The molecule would be a single fully 2'-O-methoxyethyl phosphorothioate 18-to-20-mer steric blocker, given as an intrathecal bolus, that masks a non-productive splicing element so processing is redirected toward the canonical coding transcript.
- We target only a 1.5-to-2-fold protein rise, which stays well below the level in people carrying CDKL5 duplications, who show autism and developmental delay.

## Why this design

- Truncated CDKL5 proteins are themselves found in severely and moderately affected patients. An oligonucleotide that restored a reading frame would therefore deliver a disease protein rather than a drug, so only the untouched canonical protein is an acceptable product.
- Girls whose X-inactivation happens to favour the healthy allele are mild or unaffected, which is direct human evidence that a modest rise in normal CDKL5 per neuron is clinically meaningful.
- Both AAV gene-replacement programs in this disease have stalled or been dose-limited, so a redosable and titratable cerebrospinal-fluid oligonucleotide has a genuine safety and dosing advantage rather than just a modality preference.

## Delivery

- Use an unconjugated 2'-MOE phosphorothioate oligonucleotide given by lumbar puncture, two loading doses then maintenance every four months, because that is the only route buildable today for a CDKL5 upregulator.
- The best precedent is zorevunersen, a splice-modulating oligonucleotide given intrathecally to children aged 2 to under 18 as two 70 mg loading doses then 45 mg every four months. It sets our dosing schedule and safety expectations, but says nothing about how well our payload will work.
- The main limitation is depth of brain exposure. In monkeys, oligonucleotide levels in deep brain are more than ten-fold lower than in cortex and spinal cord, and human autopsy after nusinersen shows a gradient from spinal cord upward with little drug in the brainstem.
- This means hippocampus, deep cerebellar layers and interneurons in deep structures are the under-dosed compartments for a disorder that needs broad neuronal coverage, so they must be measured rather than assumed.
- The follow-on delivery test is a single intrathecal dose of the winning sequence in non-human primates. We measure the productive CDKL5 transcript share and CDKL5 protein separately in cortex, hippocampus, cerebellum, brainstem and spinal cord at 4 and 12 weeks.

## Backup

- **Variant-specific splice-correcting oligonucleotide for CDKL5 donor-site variants at the +5 position, such as c.2376+5G>A in exon 16 and c.99+5G>A in exon 3**
  - In these variants a weakened splice donor causes the exon to be skipped and the transcript destroyed. Engineered U1 small nuclear RNA restored more than 70 percent of CDKL5 protein in patient cells, along with kinase activity and normal dendrite shape.
  - This becomes the preferred track if the mutation-agnostic screen fails, because it carries the only quantitative CDKL5 rescue data available. Its limits are that it serves a small named-variant subgroup and that the rescue was shown with U1 RNA rather than an oligonucleotide.
- **Oligonucleotide against Xist to reactivate the silenced wild-type CDKL5 allele on the inactive X chromosome in heterozygous girls**
  - The natural proof of concept is exact: girls whose inactive X carries the mutant allele are mild or unaffected. A related approach, an Xist oligonucleotide combined with a DNA-methylation inhibitor, strongly raised MECP2 from the inactive X in cultured cells.
  - This becomes preferable only if selectivity improves, because reactivating the inactive X is genome-wide rather than CDKL5-specific, and it cannot help hemizygous boys at all.

## Critical risk

- The payload may not exist: no validated non-productive CDKL5 splicing event has been published, and CDKL5 is absent from a 2025 transcriptome-wide survey of 12,014 candidate brain poison exons.
- The known alternative CDKL5 splicing events are too small to help. The one quantified alternative exon is in-frame and productive at roughly 10 percent of brain transcripts, and the exon-11 cryptic-donor forms are under 5 percent, so even complete suppression recovers little extra protein.
- Walking an oligonucleotide along intron 16 could make things worse. A single change at the +5 position of that donor removes about 80 percent of correct splicing, so our own drug could induce the exon-16-skipped transcript, which is degraded.

## First experiment

- **Model**
  - Patient-derived induced pluripotent stem cell neurons differentiated to cortical excitatory and GABAergic interneuron fates, including at least two heterozygous female lines, one hemizygous male line and isogenic controls.
  - Oligonucleotides added to the medium without any transfection reagent, each arm run with and without a SMG1 inhibitor to block nonsense-mediated decay and reveal transcripts that are normally degraded before they can be seen.
- **Constructs**
  - About 40 fully 2'-MOE phosphorothioate 18-to-20-mers tiled at 5-nucleotide steps across the candidate element in intron 16 and across the exon-20 3'-terminal region including its polyadenylation signal.
  - One two-armed single oligonucleotide joining the best splice-site blocker to the best enhancer blocker, plus scrambled and non-CDKL5 chemistry-matched controls.
- **Primary readout**
  - Targeted long-read sequencing of full-length CDKL5 transcripts, giving the absolute fraction that is the productive canonical isoform and the full distribution of every alternative form.
  - CDKL5 protein by capillary immunoassay together with phosphorylation of EB2 at serine 222 as a kinase-activity surrogate, so we confirm the protein is functional and not just present.
- **Success criterion**
  - In heterozygous female neurons, at 5 micromolar or below, at least a 1.5-fold rise in CDKL5 protein with a matching rise in EB2 serine-222 phosphorylation. Long-read sequencing must show a concordant increase in the productive isoform share.
  - No new or off-target CDKL5 isoform above 5 percent of transcripts, and specifically no increase in the exon-16-skipped degraded species relative to vehicle.
- **Kill criterion**
  - If long-read sequencing with nonsense-mediated decay inhibited shows no degradation-coupled CDKL5 isoform used at 10 percent or more of baseline transcripts, there is no handle to act on and the mutation-agnostic track stops.
  - If the best oligonucleotide raises CDKL5 protein less than 1.3-fold, move the budget to the variant-specific +5 donor-site backup.

## Key precedents

- A 2025 survey of 12,014 candidate brain poison exons did not include CDKL5, which is why this program is gated on an existence experiment rather than launched.
- Engineered U1 small nuclear RNA restored more than 70 percent of CDKL5 protein and its kinase activity for donor +5 variants but failed entirely for +1 variants, which both defines and bounds the variant-specific backup.
- Zorevunersen is given as two 70 mg intrathecal loading doses then 45 mg every four months in children, with elevated cerebrospinal-fluid protein the main finding, which gives us a ready-made pediatric dosing and safety template.
- Oligonucleotide levels in monkey deep brain are more than ten-fold below cortex and spinal cord, and human autopsy after nusinersen shows little drug in the brainstem. Hippocampal and brainstem coverage must therefore be measured in primates before lead nomination.
- The high-dose cohort of the NGN-401 AAV trial in Rett syndrome was halted for a hyperinflammatory serious adverse event. That is why a redosable cerebrospinal-fluid oligonucleotide has a real differentiation claim against gene replacement in this population.
