# DMD nonsense mutation within exon 55

**Verdict: TEST FIRST**

## Recommendation

**LEAD — Remove DMD exons 54 and 55 together with a morpholino oligonucleotide, so patients make a shortened but membrane-anchoring Becker-type dystrophin.**

- This patient's Duchenne muscular dystrophy comes from a stop codon inside exon 55, so no full-length dystrophin is made at all.
- Skipping exon 55 alone cannot work, because the exon is 190 bases long and removing it shifts the downstream reading frame.
- Removing exons 54 and 55 together joins exon 53 to exon 56 in frame and deletes only 115 amino acids.
- That product keeps the actin-binding, cysteine-rich and C-terminal domains that anchor dystrophin at the muscle membrane.
- Published work shows one oligonucleotide against exon 54 can pull exon 55 out with it, so a single drug may suffice.

## Why this design

- Exons 54 and 55 are the smallest in-frame block containing the mutation, so the protein is perturbed as little as possible.
- Human pre-messenger RNA treats exons 54 and 55 as a coupled pair, which means the double removal may need only one oligonucleotide.
- The new junction rebuilds one normal-length rod segment rather than a stub, the configuration associated with milder Becker disease.

## Delivery

- Separate payload from delivery: validate the sequence first as an unconjugated morpholino, which is cheap and free of licensing constraints.
- Unconjugated morpholino is sufficient for every RNA and protein readout we need at the discovery stage.
- For the clinical asset, conjugate the winning sequence to an antibody or antibody fragment against transferrin receptor 1.
- That class is the only one with dystrophin confirmed in human muscle biopsies plus cardiac restoration in animals, and monthly dosing.
- The main limitation is access, because both leading conjugate platforms sit inside companies advancing their own exon-skipping drugs.
- The follow-on test is intravenous dosing in humanised mice then monkeys, measuring dystrophin separately in limb muscle, diaphragm and heart.

## Backup

- **Two-oligonucleotide cocktail removing exons 55 and 56 instead, giving an in-frame exon 54 to 57 junction**
  - This deletes 121 amino acids, almost the same as the lead, and a validated exon-56 oligonucleotide already exists.
  - It becomes preferable only if exon 54 proves hard to skip, because no coupling is reported for this pair, so two independent skips are always needed.
  - It also removes an entire rod segment without replacing its length, which is a weaker structural bet than the lead.
- **Three-to-four oligonucleotide cocktail removing exons 52 through 55, deleting 225 amino acids**
  - A purpose-built mouse carrying this exact deletion makes normal amounts of correctly localised dystrophin with normal muscle and heart function when young.
  - It becomes preferable if neither two-exon product can be driven efficiently, accepting more manufacturing complexity and a late exercise-induced functional decline in that mouse.

## Critical risk

- The dominant risk is that an exon-54 oligonucleotide mostly removes exon 54 alone, which joins exon 53 to exon 55 out of frame.
- That outcome swaps one decayed transcript for another, so we would gain nothing and might lower residual transcript further.
- The single source for exon 54 and 55 coupling is qualitative, so the ratio must be measured again for every candidate sequence.
- No person with a deletion of exons 54 and 55 has been described, so protein function is inferred from reading frame and domain content, not observed.

## First experiment

- **Model**
  - Muscle cells from a patient carrying an exon-55 nonsense mutation, because coupling behaviour must be read on the actual mutant locus.
  - A second independent patient line plus normal human muscle cells, to show the coupling is not donor-specific.
  - Delivery is deliberately artificial at this stage, by nucleofection or high free-oligonucleotide concentrations, since the question is payload behaviour.
- **Constructs**
  - About twenty morpholinos tiled across exon 54, concentrated on its acceptor site and the first half of the exon.
  - A parallel exon-55 walk, and the best exon-54 plus best exon-55 pair tested together as a two-oligonucleotide cocktail.
  - Controls are a scrambled morpholino, untreated cells, and a known exon-51 morpholino as a positive control for skipping.
- **Primary readout**
  - Sequencing across exons 50 to 60 that counts every splice product as a fraction of total DMD transcript.
  - Dystrophin protein by western blot and mass spectrometry against a quantified normal muscle standard, because transcript alone is not predictive.
  - Immunofluorescence showing the shortened dystrophin reaches the muscle membrane and recruits its partner proteins.
- **Success criterion**
  - The in-frame exon 53 to 56 product is the dominant skipped species and reaches at least a fifth of total DMD transcript.
  - Dystrophin rises dose-dependently, agrees between western blot and mass spectrometry, and localises correctly at the membrane.
  - No new cryptic or neighbouring-exon junction exceeds two percent of reads.
- **Kill criterion**
  - Kill the one-oligonucleotide idea if every exon-54 oligonucleotide makes more out-of-frame exon-54-only product than in-frame product.
  - Kill the exon 54 and 55 product if the two-oligonucleotide cocktail also fails, or if correct transcript is made but no dystrophin is measurable.
  - Nothing advances on a reverse-transcription PCR band alone.

## Key precedents

- Oligonucleotides aimed at exon 54 of human dystrophin gave two products: transcripts missing exon 54 alone, and transcripts missing exons 54 and 55 together. That second product matters because it is the only way one oligonucleotide can produce an in-frame transcript in this patient.
- An independent paper restates that directing an oligonucleotide to exon 54 removed both exons 54 and 55, so the observation is not a single reading of one figure.
- PGN-EDO51 produced 4.26 percent skipped transcript but only 0.59 percent dystrophin and was discontinued, so this program must be judged on protein, never on skipped transcript.
- Brogidirsen, one morpholino product containing two linked targeting sequences, has five-year clinical data, showing a multi-sequence drug is developable and approvable.
- Dyne's DYNE-255, an exon-55-directed morpholino on a transferrin-receptor conjugate, is already at the stage of enabling studies, so the exon-55 arm is a licensing question rather than a discovery one.
