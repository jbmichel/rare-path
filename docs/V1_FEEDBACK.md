# V1 feedback

Reviewer comments on V1, from a run against DMD exon 55 nonsense (verbatim):

> I ran this against a few indications. Here are the results for DMD exon 55 nonsense.
> The biggest problem is that this is much too shallow from a drug discovery standpoint: it's very obvious, and it's not finding a good path. It should have figured out that Dyne/Avidity have cracked antibody-aso muscle-directed delivery, and should have figured out that a dual-exon skip 54/55 or 55/56 might work.
> The secondary problem is that this is way too verbose, and not crisp.
>
> We need more work, and I am not certain whether our LLM path here is the right one, or if we need to change tack.
>
> In order to dive into this, let's zero in on just 1 modality (ASOs), and refine this until we get it right.

## Takeaways

1. **Depth**: output is obvious, not a discovery-grade path. It missed (a) antibody-oligonucleotide conjugate delivery to muscle (Dyne, Avidity) and (b) multi-exon skipping (54/55 or 55/56) for a nonsense exon 55 variant.
2. **Concision**: dossiers are verbose; they need to be crisp.
3. **Approach**: unclear whether the generalist multi-agent LLM pipeline is the right path. Next step is to narrow to one modality (ASOs) and iterate until it is right.

## Known V1 issues found during the runs

- Dossier-level "MECHANISM UNCERTAIN" banners even when the mechanism stage was OK.
- PURSUE verdicts coexisting with MECHANISM UNCERTAIN flags (DMD readthrough).
- Unverified "no existing agent" claims (e.g. mTOR in TSC).
- Long table cells in the Markdown dossier.
