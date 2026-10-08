# CDKL5 loss-of-function variant (no specific variant given)

**Verdict: TEST FIRST**

## Recommendation

**LEAD — A mutation-agnostic antisense oligonucleotide that raises full-length CDKL5 protein from the patient's healthy allele, funded only through a six-month test that the required splicing event exists.**

- CDKL5 deficiency disorder is a severe childhood epilepsy and developmental disorder caused by loss-of-function variants that leave too little CDKL5 kinase per neuron.
- The product is ordinary full-length CDKL5 protein, made from the patient's own non-mutant allele. The coding sequence is never altered, so a single drug serves all patients regardless of which variant they carry.
- The mechanism is a steric-block oligonucleotide that suppresses a non-productive CDKL5 splicing event, shifting pre-mRNA processing toward the canonical protein-coding transcript.
- Fund a six-month existence test in human neurons, not a program, because no such non-productive CDKL5 splicing event has been validated.

## Why this design

- Raising the normal protein from a healthy allele costs no protein domains and works in both affected girls and hemizygous boys, so a single sequence covers the whole population.
- Women with favourable X-inactivation are mild or unaffected, which means a modest increase of roughly 1.5 to 2-fold should be clinically meaningful.
- Gene therapy competitors cannot be re-dosed or titrated, and one high-dose trial in Rett syndrome caused a hyperinflammatory serious adverse event, so a re-dosable spinal-fluid drug differentiates on safety.

## Delivery

- Use an unconjugated 2'-O-methoxyethyl phosphorothioate 18-20mer given as a lumbar intrathecal bolus, the only route buildable today.
- Follow the pediatric schedule already run for zorevunersen in Dravet syndrome, two loading doses then maintenance every four months, which the field and regulators accept in children.
- Accept the exposure gradient rather than engineering around it. Deep-brain oligonucleotide levels in monkeys are more than ten-fold below cortex and cord, so exposure in hippocampus, deep cerebellum and deep interneurons must be measured rather than assumed.
- Transferrin-receptor antibody-oligonucleotide conjugates are the generation-two answer for deep brain. But no one has yet shown a conjugated steric-block oligonucleotide raising a brain protein, so the lead must not be built on them.

## Backup

- **Variant-specific splice correction for CDKL5 donor-site +5 variants**
  - Engineered U1 small nuclear RNA restored more than 70 percent of CDKL5 protein and kinase activity for these variants, the only quantitative CDKL5 rescue data available.
  - This becomes the lead if the mutation-agnostic test fails, accepting that it serves a small named subgroup and that the modality shown was U1, not an oligonucleotide.
- **Reactivating the healthy CDKL5 allele on the inactive X with an Xist-targeting oligonucleotide**
  - Its proof of concept is human: girls whose X-inactivation favours the healthy allele are mild or unaffected, and a related approach raised MECP2 strongly from the inactive X.
  - It becomes preferable if selective reactivation can be shown, but today it is genome-wide rather than gene-selective and it excludes boys entirely.

## Critical risk

- The decisive risk is whether the payload exists at all, not whether we can deliver it.
- CDKL5 does not appear among the 12,014 candidate brain poison exons catalogued in a 2025 survey. The only claimed non-productive CDKL5 exon sits in a patent that provides no sequences and no expression data.
- The CDKL5 alternative exons that are quantified are either productive or used by under 10 percent of brain transcripts, so even complete suppression may not add enough protein.

## First experiment

- **Model**
  - Patient-derived induced pluripotent stem cell neurons, both cortical excitatory and inhibitory, including female and hemizygous male lines, because the splicing event must exist in human neurons to be druggable.
- **Constructs**
  - About 40 oligonucleotides walking the candidate non-productive regions in five-nucleotide steps, plus a two-arm linked oligonucleotide and chemistry-matched controls.
- **Primary readout**
  - Long-read sequencing of full-length CDKL5 transcripts to measure the productive fraction, paired with CDKL5 protein and its kinase-activity marker.
- **Success criterion**
  - At least a 1.5-fold rise in CDKL5 protein with matching kinase-activity and productive-transcript gains, and no new aberrant isoform above 5 percent.
- **Kill criterion**
  - Stop if no degradation-coupled CDKL5 isoform reaches 10 percent of baseline transcripts, or if the best oligonucleotide gives under 1.3-fold protein.

## Key precedents

- A 2025 survey of 12,014 candidate brain poison exons did not include CDKL5, which is why this program is gated rather than launched.
- Engineered U1 restored over 70 percent of CDKL5 protein for donor +5 variants but failed for +1 variants, which both defines and limits the variant-specific backup.
- Zorevunersen gives two intrathecal loading doses then maintenance every four months in children, setting our dosing and safety template but not our potency expectation.
- Monkey and human autopsy data show intrathecal oligonucleotides reach deep brain poorly, so hippocampus and brainstem coverage must be measured in monkeys before committing.
- A high-dose gene therapy cohort in Rett syndrome was halted for a hyperinflammatory serious adverse event, supporting a re-dosable spinal-fluid oligonucleotide instead.
