# ASO Discovery Agent

## 1. Purpose

Build an ASO drug-discovery agent for rare and ultra-rare genetic diseases.

The agent's job is not to answer:

> Could an ASO theoretically treat this disease?

It must answer:

> Given the exact molecular lesion, what is the best ASO therapeutic program that could plausibly be built today?

The output should resemble the work of an experienced oligonucleotide discovery team: specific, technically current, and experimentally actionable.

---

# 2. Core Principle

Separate three jobs:

```text
DESIGN-SPACE ENUMERATION
What ASO interventions are physically / genetically possible?

        ↓

STATE-OF-THE-ART SEARCH
What chemistry, delivery and development precedents exist today?

        ↓

SCIENTIFIC JUDGMENT
Which program should we actually build and how should we test it?
```

Do not rely on the LLM to perform deterministic operations from memory.

Use tools for things that can be calculated or retrieved.

Use the LLM for scientific interpretation and program design.

---

# 3. Inputs

Minimum input:

```yaml
disease:
gene:
variant:
```

When available:

```yaml
transcript:
genomic_coordinates:
patient_sequence:
affected_tissues:
affected_cell_types:
```

The agent should resolve missing transcript and variant information from authoritative sources before designing an ASO strategy.

---

# 4. Step 1 — Define the RNA Problem

Determine what the mutation does to RNA or protein.

Examples:

- premature termination codon;
- exon-disrupting deletion;
- splice-site mutation;
- cryptic splice activation;
- poison exon;
- toxic RNA;
- gain-of-function transcript;
- transcript overexpression;
- allele-specific toxic transcript.

Then define what an ASO would need to accomplish:

```text
skip exon
include exon
skip multiple exons
block cryptic splice site
induce transcript degradation
stabilize transcript
suppress mutant allele
alter polyadenylation
other splice redirection
```

Do not select a specific ASO design until the desired RNA product is clear.

---

# 5. Step 2 — Enumerate the ASO Design Space

This step should be deterministic wherever possible.

For splice-modulating strategies, explicitly enumerate all plausible transcript products.

For each candidate manipulation calculate:

```yaml
splice_solution:
  exons_removed_or_included:
  resulting_junction:
  reading_frame:
  mutation_removed:
  predicted_protein_change:
  oligo_count:
```

For DMD-like genes this means computationally enumerating:

- single-exon skips;
- adjacent dual-exon skips;
- larger contiguous skips;
- any known coordinated-skipping behavior.

Never jump directly to a historically popular exon block if a smaller solution exists.

Rank solutions initially by:

1. correct molecular product;
2. minimal perturbation;
3. minimal number of oligos;
4. likely functional protein product;
5. existing biological precedent.

The LLM interprets the enumeration. It does not perform exon-frame arithmetic from memory.

---

# 6. Step 3 — Search for Biological Precedent

For each promising ASO design, search specifically for:

- naturally occurring equivalent transcript or deletion;
- human genotype–phenotype evidence;
- spontaneous exon skipping;
- published ASOs targeting the same exon;
- coordinated skipping induced by a single ASO;
- patient-cell rescue;
- animal-model rescue;
- clinical programs against the same exon or nearby exons.

The important question is:

> Has biology already shown that this RNA product can work?

Prefer human natural experiments and direct rescue evidence over generic pathway evidence.

---

# 7. Step 4 — Search the Current ASO Technology Landscape

This search is mandatory.

The agent must determine what is technically achievable **today**, not what was historically achievable with naked oligonucleotides.

For the relevant tissue and cell type search:

```text
ASO chemistry
delivery technology
targeting receptor / ligand
cargo
clinical maturity
human pharmacodynamic data
relevant companies
active programs
failed programs
```

Examples of delivery categories:

- unconjugated ASO / PMO;
- GalNAc;
- peptide conjugates;
- antibody-oligonucleotide conjugates;
- Fab-oligonucleotide conjugates;
- receptor-targeted conjugates;
- other tissue-targeting ligands.

For each delivery platform ask:

1. Does it reach the required tissue?
2. Does it reach the required cell type?
3. Does it produce functional intracellular ASO activity?
4. Is there human pharmacodynamic evidence?
5. Has it delivered the same or similar oligo chemistry?
6. Is heart/CNS/other secondary tissue exposure relevant?
7. Is the technology realistically accessible through partnership or licensing?

Historical failure of naked ASO delivery must not be used to dismiss a strategy if newer targeted delivery has materially changed exposure.

---

# 8. Step 5 — Search Existing Programs

Search companies, trials, publications, patents where practical, and conference disclosures for programs involving:

- the same exon;
- adjacent exons;
- the same target gene;
- the same tissue;
- the same delivery receptor;
- the same ASO mechanism.

This search must be current.

The agent should explicitly identify:

```yaml
competitive_precedent:
  organization:
  program:
  target:
  payload:
  delivery:
  stage:
  key_result:
  relevance:
```

Existing programs may:

- validate the concept;
- provide a delivery solution;
- suggest a partnership path;
- make a new program redundant;
- reveal a failure mode.

---

# 9. Step 6 — Select the Lead ASO Concept

Compare candidate strategies on a small number of decision variables:

```text
Does it create the right RNA/protein?

How many oligos are required?

How much precedent exists for the resulting product?

Can current delivery technology reach the required cells?

Is there an existing delivery platform or partner?

Can the concept be tested cleanly?

What is the dominant failure mode?
```

Do not use artificial numerical scores.

Select:

```text
LEAD
BACKUP
WATCH / FUTURE
REJECT
```

A two-exon solution should normally outrank an eleven-exon solution if both produce credible proteins, unless evidence strongly favors the larger product.

A single-ASO strategy that induces coordinated multi-exon skipping should be explicitly investigated before proposing a multi-ASO cocktail.

---

# 10. Step 7 — Design the First Experiment

The first experiment should answer the major uncertainty in the ASO concept, not reproduce established disease biology.

For splice-modulating ASOs this will often mean:

```text
patient-relevant cells
+
tiled ASO screen
+
delivery-independent transfection initially
+
quantitative transcript-product analysis
+
protein confirmation
```

Measure all relevant splice products, not only the desired PCR band.

For example:

```yaml
experiment:
  question:
  ASOs_tested:
  model:
  primary_readout:
  undesired_products:
  protein_readout:
  success_condition:
  kill_condition:
```

Separate:

### Payload validation

Can the ASO create the desired RNA product when intracellular exposure is not limiting?

from:

### Delivery validation

Can a clinically relevant delivery system achieve sufficient intracellular exposure?

Do not confound these in the first experiment unless necessary.

---

# 11. Output

The final output should be short.

## Lead concept

One paragraph.

## Why it wins

Maximum 3 bullets.

## Delivery strategy

Current best delivery solution and supporting human/clinical precedent.

## Backup

One or two credible alternatives.

## Critical unknown

The single largest uncertainty.

## Next experiment

Specific and decision-changing.

## Relevant programs / partners

Only programs that materially affect the development decision.

## Verdict

```text
BUILD
TEST FIRST
WAIT FOR PLATFORM
DO NOT PURSUE
```

Detailed evidence may appear beneath the main answer but should not interrupt the decision narrative.

---

# 12. DMD Exon 55 Nonsense — Acceptance Test

The ASO agent is not ready unless it independently reaches the following findings.

### Design space

It must discover that an exon-55 nonsense mutation should not automatically lead to an exon 45–55 multi-skip program.

It must enumerate smaller frame-restoring possibilities including:

```text
exons 54 + 55
exons 55 + 56
```

and compare them with larger skips.

Published DMD exon-skipping analyses explicitly identify dual-exon strategies around exon 55, so failure to find them is a discovery failure.

### Coordinated skipping

It must investigate whether either dual skip can be achieved with fewer ASOs than the number of exons being skipped.

In particular it should find and evaluate published evidence that targeting exon 54 can induce coordinated skipping involving exons 54 and 55.

### Delivery

It must recognize that naked PMO is no longer an adequate representation of the state of the art in muscle ASO delivery.

It must identify modern receptor-targeted muscle delivery, including TfR1-directed antibody/Fab-oligonucleotide approaches, and determine their relevance to the proposed payload.

### Current competitive landscape

It must identify major current muscle-targeted oligonucleotide programs and, as of 2026, discover that:

- Avidity has clinically tested TfR1-targeted PMO delivery in DMD;
- Dyne has clinically advanced a TfR1-targeted Fab-PMO platform;
- Dyne is developing an exon-55 program.

### Program conclusion

A credible answer should therefore evaluate something close to:

```text
LEAD:
minimal exon-55-containing dual skip
using modern targeted muscle delivery

VERSUS:

BACKUP:
alternative adjacent dual skip

VERSUS:

LOWER PRIORITY:
large 45–55 multi-exon cocktail
```

The exact ranking may vary with evidence.

Failing to surface the smaller skip geometries or modern muscle-delivery platforms is unacceptable.

---

# 13. Failure Modes

The agent has failed if it:

- produces only obvious textbook ASO strategies;
- relies on historical delivery limitations without searching current technology;
- proposes a large multi-ASO cocktail before enumerating smaller solutions;
- performs exon-frame reasoning purely from LLM memory;
- fails to search current company pipelines;
- equates "no approved product" with "no viable delivery solution";
- produces extensive disease background instead of a drug-discovery recommendation;
- gives many ideas without selecting a lead;
- proposes experiments that do not change the program decision.

---

# 14. Success Criterion

The agent succeeds when an experienced ASO scientist can read its output and say:

> This found the non-obvious design options I would have considered, understands what current oligonucleotide technology can actually do, and gives me a sensible first experiment.

The objective is not completeness.

The objective is to find the best buildable ASO program.
