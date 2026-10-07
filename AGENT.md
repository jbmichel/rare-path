# Rare Disease Therapeutic Development System

## 1. Purpose

Build a multi-agent scientific decision system for rare and ultra-rare diseases.

The primary users are patient foundations, families, researchers, and biotech practitioners trying to decide how best to spend time and money advancing therapeutics.

The central question is:

> Given what is known about this disease, what therapeutic approaches are most plausible, what are the main reasons they might fail, and what should be done next to determine whether they are worth pursuing?

The system should behave like a small therapeutic-development team, not like a literature-review engine.

Its job is to turn disease biology into decisions.

---

# 2. Scope

Version 1 focuses on:

- disease mechanism;
- molecular and cellular pathology;
- therapeutic intervention opportunities;
- small molecules;
- oligonucleotides;
- RNA therapeutics;
- proteins and biologics;
- repurposing;
- delivery;
- disease models and assays;
- therapeutic de-risking.

Commercial analysis is secondary.

The following are explicitly out of scope for Version 1:

- gene addition / gene replacement;
- genome editing;
- epigenome editing;
- cell therapy.

The system may note these when obviously relevant, but should not analyze them deeply.

---

# 3. Core Principle

> Prefer the smallest internal representation that preserves the therapeutic decision.

Do not rebuild biomedical knowledge infrastructure.

Use resources such as OMIM, Orphanet, MONDO, HPO, Monarch, Open Targets, ClinVar, Reactome, UniProt, ChEMBL, PubMed, ClinicalTrials.gov, MATRIX / Every Cure, and disease-specific resources as sources.

Spend reasoning effort where the system can add differentiated value:

> translating molecular and cellular pathology into plausible therapeutic approaches.

---

# 4. Central Reasoning Chain

```text
What is going wrong?
        ↓
What biology appears causal?
        ↓
What biological change might help?
        ↓
Where could we intervene?
        ↓
Which therapeutic approaches could produce that change?
        ↓
Are there existing agents that already do it?
        ↓
Can the intervention reach the relevant cells?
        ↓
Can we test the idea credibly?
        ↓
What should we do next?
```

---

# 5. Architecture

```text
                      DISEASE
                         │
                         ▼
                  MECHANISM AGENT
                         │
              "What is going wrong?"
                         │
                         ▼
              THERAPEUTIC STRATEGIST
                         │
              "What could we change?"
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     Small           Oligonucleotide    Protein /
    Molecule             + RNA          Biologic
 + Repurposing
        │                │                │
        └────────────────┼────────────────┘
                         ▼
             EXPERIMENTAL STRATEGIST
                         │
              "What should we test?"
                         │
                         ▼
              REVIEWER / SYNTHESIZER
                         │
                         ▼
                      DOSSIER
```

Keep the architecture simple.

Do not create additional agents unless a distinct reasoning task repeatedly justifies one.

---

# 6. Mechanism Agent

## Mission

Build the minimum disease model required for therapeutic reasoning.

Answer:

- What initiates the disease?
- What molecular consequence follows?
- Which cells are most relevant?
- What pathological processes appear disease-driving?
- What is established versus uncertain?

Use existing structured resources wherever possible. Use literature mainly for mechanistic questions not adequately captured elsewhere.

## Output

```yaml
disease_mechanism:
  causal_defect:
  molecular_consequence:
  key_cell_types: []
  key_pathology: []
  evidence_strength:
  major_unknowns: []
```

Do not attempt to create a complete disease ontology.

---

# 7. Therapeutic Strategist

## Mission

Translate the disease mechanism into a small number of biologically meaningful therapeutic hypotheses.

Ask:

> Given what is going wrong, what biological change could plausibly improve disease?

Start from pathology, not from available drugs.

Consider:

- reducing something excessive or toxic;
- increasing something deficient;
- restoring a lost function;
- correcting abnormal RNA processing;
- stabilizing dysfunctional protein;
- reducing toxic substrate;
- increasing clearance;
- blocking a damaging downstream process;
- activating a compensatory pathway;
- exploiting a paralog or bypass.

Consider both:

- proximal interventions close to the causal defect;
- downstream interventions when they are therapeutically meaningful.

Prioritize causal biology and evidence of rescue over mere association.

Human genetics, genotype–phenotype relationships, natural experiments, and rescue experiments are especially valuable.

## Output

```yaml
candidate_approaches:
  - name:
    biological_hypothesis:
    target_or_process:
    desired_perturbation:
    plausible_modalities: []
    evidence_for: []
    evidence_against: []
    key_biological_uncertainty:
```

Generate a few serious hypotheses, not an exhaustive list.

Different modalities implementing the same biological hypothesis should remain conceptually linked rather than being treated as unrelated ideas.

---

# 8. Therapeutic Approach

The main decision object in the system is the `TherapeuticApproach`.

```yaml
therapeutic_approach:
  name:

  biological_hypothesis:
  target_or_process:
  desired_perturbation:

  modality:
  strategy:

  existing_agents: []

  disease_relevant_cells: []

  delivery_feasibility:
    target_tissue:
    target_cell:
    expected_access:
    major_constraint:

  supporting_evidence: []
  contradictory_evidence: []

  biggest_unknown:
  biggest_failure_mode:

  best_next_experiment:

  verdict:
    # pursue
    # investigate
    # low_priority
    # reject
```

Add fields only when they repeatedly improve therapeutic decisions.

---

# 9. Small Molecule Agent

## Mission

Determine whether pharmacology can execute a proposed biological perturbation.

Consider:

- inhibition;
- activation;
- agonism / antagonism;
- stabilization;
- pharmacological chaperoning;
- degradation where relevant;
- substrate reduction;
- metabolic manipulation;
- pathway modulation.

Search existing agents before assuming new chemistry is required:

```text
approved drug
→ clinical-stage compound
→ preclinical / tool compound
→ novel chemistry required
```

Repurposing is a first-class strategy.

Use external resources such as MATRIX / Every Cure, ChEMBL, Open Targets, PubChem, clinical-trial databases, and regulatory sources rather than rebuilding repurposing algorithms.

The key question is not whether a drug is associated with the disease.

It is:

> Does this agent produce the required biological perturbation at an exposure relevant to the disease?

---

# 10. Oligonucleotide Agent

## Mission

Determine whether transcript-level intervention can execute the desired biological change.

Consider:

- RNase-H knockdown;
- splice correction;
- exon skipping;
- transcript modulation;
- allele-selective suppression.

Evaluate mechanism and delivery together.

Ask:

- Is the relevant transcript expressed in the disease-driving cells?
- What direction of transcript change is required?
- Can the relevant tissue and cell type be reached?
- Is the required intracellular compartment accessible?
- Is repeat dosing plausible?
- Is there relevant delivery precedent?

Emerging approaches such as antibody-oligonucleotide and peptide-oligonucleotide conjugates should be considered where relevant.

---

# 11. RNA Therapeutics Agent

## Mission

Evaluate RNA approaches outside the core oligonucleotide strategies.

Relevant approaches may include:

- siRNA;
- RNA interference;
- mRNA-based protein replacement;
- other sufficiently mature RNA modalities.

Evaluate:

- biological fit;
- target cell;
- intracellular site of action;
- delivery;
- durability;
- repeat dosing;
- precedent.

Delivery is part of the therapeutic strategy, not a downstream afterthought.

---

# 12. Protein / Biologic Agent

## Mission

Determine whether a protein or biologic can execute the desired therapeutic perturbation.

Consider:

- enzyme replacement;
- recombinant protein replacement;
- antibodies;
- agonist or antagonist antibodies;
- ligand traps;
- soluble receptors;
- replacement of circulating factors;
- targeted protein therapeutics.

Search for existing agents before assuming a new biologic must be created.

Evaluate:

- site of action;
- tissue penetration;
- target-cell access;
- extracellular versus intracellular biology;
- receptor-mediated uptake when relevant;
- CNS access where relevant;
- repeat dosing;
- immunogenicity.

---

# 13. Delivery

Delivery is mandatory reasoning but does not require a separate top-level agent.

Every modality agent must answer:

```yaml
delivery_feasibility:
  target_tissue:
  target_cell:
  expected_access:
  major_constraint:
```

Evaluate delivery at the cell-type level when it matters.

A therapy that reaches an organ but not the disease-driving cell population may not be viable.

Novel delivery technologies should be considered when mechanistically relevant, but their maturity and evidence should be stated clearly.

---

# 14. Experimental Strategist

## Mission

For each therapeutic approach, answer:

> What is the simplest credible experiment that would materially change whether we pursue this approach?

Consider:

- disease models;
- assays;
- therapeutic rescue;
- pharmacology;
- delivery;
- biomarkers;
- translational relevance.

Prefer experiments that can invalidate weak approaches early.

---

## Model Fitness

Rare diseases frequently lack good disease models.

For every important therapeutic hypothesis, assess whether an available model is fit to answer the relevant question.

```yaml
model_fitness:
  best_available_model:
  captures_relevant_mechanism:
  captures_relevant_cell_type:
  measurable_phenotype:
  important_limitations:
  fitness:
    # adequate
    # partial
    # inadequate
    # unknown
```

Do not ask whether a model reproduces the entire disease.

Ask whether it can answer the specific therapeutic question.

A simple cellular model may be sufficient for one decision while an animal model is necessary for another.

If existing models are inadequate, identify the simplest new model needed to unblock the decision.

Lack of an adequate disease model should be surfaced as a major development gap when appropriate.

---

## Experimental Output

```yaml
experimental_plan:
  critical_question:
  proposed_experiment:
  model:
  primary_readout:
  supportive_result:
  negative_result:
  decision_enabled:
```

Every experiment should enable a decision.

---

# 15. Reviewer / Synthesizer

## Mission

Compare therapeutic approaches and produce the final development dossier.

Act as both skeptical reviewer and therapeutic program lead.

For each approach ask:

- Why could this work?
- What evidence supports it?
- What evidence argues against it?
- What is the dominant failure mode?
- Can the relevant cells be reached?
- Can the hypothesis be tested in a credible model?
- Is there an existing agent that could accelerate validation?
- Does the proposed next experiment genuinely reduce uncertainty?

Use four verdicts:

```text
PURSUE
INVESTIGATE
LOW PRIORITY
REJECT
```

Avoid artificial numerical rankings.

Explain comparative judgments directly.

---

# 16. Evidence Rules

Every important scientific conclusion should be traceable to evidence.

Distinguish:

```text
EVIDENCE
Directly supported by a source.

INFERENCE
Derived from available evidence.

HYPOTHESIS
Requires experimental validation.
```

When useful, characterize evidence as:

```text
Supportive
Contradictory
Inconclusive
Not studied
```

Do not treat absence of literature as evidence against a hypothesis.

This is especially important in ultra-rare diseases.

Actively look for evidence that contradicts important therapeutic hypotheses.

---

# 17. Research Priorities

Spend less effort on:

- generic disease description;
- exhaustive phenotype catalogs;
- reconstructing ontologies;
- exhaustive literature histories.

Spend more effort on:

- causal molecular and cellular pathology;
- rescue evidence;
- reversibility;
- compensatory biology;
- therapeutic leverage points;
- target pharmacology;
- existing drugs and biologics;
- cell-specific delivery;
- disease-model fitness;
- experiments that could invalidate or support a program.

A useful rule is:

> Stop retrieving when additional information is unlikely to change the therapeutic decision.

---

# 18. Orchestration

Use a simple pipeline:

```text
1. Identify the disease.

2. Build the disease mechanism.

3. Generate therapeutic hypotheses.

4. Send each hypothesis only to relevant modality agents.

5. Search for repurposing opportunities where appropriate.

6. Merge approaches that represent the same underlying biology.

7. Determine delivery feasibility.

8. Determine whether an adequate model exists.

9. Define the best next experiment.

10. Review and prioritize approaches.

11. Produce the dossier.
```

Avoid uncontrolled agent loops.

When evidence is insufficient, return uncertainty rather than researching indefinitely.

---

# 19. Final Dossier

The final dossier should have six sections.

## 1. Disease Mechanism

What is going wrong biologically?

Focus on molecular and cellular pathology relevant to therapeutic decisions.

State major uncertainties.

---

## 2. Therapeutic Leverage Points

What biological changes might improve disease?

Keep this to the most credible opportunities.

---

## 3. Therapeutic Approaches

For each serious approach summarize:

| Approach | Why it could work | Modality | Existing agent? | Delivery | Main risk |
|---|---|---|---|---|---|

Do not include weak ideas merely for completeness.

---

## 4. What Is Already Known

Summarize prior work that materially affects the therapeutic decision:

- relevant therapeutic experiments;
- rescue experiments;
- existing agents;
- failed approaches;
- useful disease models;
- relevant therapeutic precedents.

Do not produce an exhaustive literature review.

---

## 5. Critical Gaps

Identify the few uncertainties blocking therapeutic progress.

These may include:

- uncertain mechanism;
- unknown reversibility;
- unknown rescue threshold;
- delivery;
- lack of a fit-for-purpose disease model;
- uncertain pharmacology;
- lack of an interpretable assay.

---

## 6. What Should Be Done Next

Recommend a short sequence of concrete actions.

For each action state:

- what question it answers;
- what experiment or activity is required;
- what result would support the approach;
- what result would weaken or kill it.

Also state what should **not** be funded yet when downstream work would be premature.

---

# 20. Desired Output Style

The system should reason like this:

```text
WHAT WE THINK IS HAPPENING

Loss of enzyme X causes accumulation of metabolite Y in neurons.
Human genetics and patient biochemistry strongly support this.

WHAT WE COULD CHANGE

Reducing production of Y may compensate for loss of X.

THERAPEUTIC APPROACH

Drug A inhibits enzyme Z, which controls production of Y.

WHY IT COULD WORK

The mechanism is consistent with the disease biology and Drug A
already produces the required pharmacology in humans.

WHY IT COULD FAIL

It is unclear whether sufficient drug reaches the affected neurons.

MODEL

Patient-derived neurons capture the relevant metabolic defect and
provide a reasonable first system for testing biochemical rescue.

WHAT TO DO NEXT

Test Drug A at clinically realistic exposures in patient-derived
neurons.

DECISION

If metabolite Y falls and the disease phenotype improves at plausible
exposure, advance the approach.

If rescue requires unrealistic exposure, deprioritize Drug A while
retaining substrate reduction as a valid therapeutic hypothesis.
```

---

# 21. Failure Behavior

The system must be comfortable returning:

```text
MECHANISM UNCERTAIN

INSUFFICIENT EVIDENCE

NO ADEQUATE MODEL

NO PLAUSIBLE DELIVERY PATH

NO EXISTING AGENT IDENTIFIED

THERAPEUTIC HYPOTHESIS NOT TESTABLE YET
```

These are useful conclusions.

Do not force every disease into a complete therapeutic plan.

---

# 22. Non-Goals

Version 1 should not attempt to:

- build a comprehensive disease ontology;
- reproduce Monarch, Open Targets, or similar resources;
- recreate drug-repurposing algorithms;
- generate exhaustive target lists;
- evaluate every possible modality;
- deeply evaluate gene therapy, editing, or cell therapy;
- generate novel molecules;
- autonomously design clinical trials;
- replace experimental validation;
- provide medical advice.

---

# 23. Success Criterion

The system succeeds if a scientifically sophisticated disease community can read the output and answer:

> What are the few therapeutic ideas worth serious attention?

> Why might they work?

> What is most likely to kill them?

> Do we have a credible way to test them?

> What should we spend money on next?

The product is not a universal biomedical knowledge system.

Its differentiated job is:

> **Translate known molecular and cellular pathology into a small number of credible therapeutic approaches, identify why each might fail, and determine the fastest useful experiment for deciding what to pursue.**
