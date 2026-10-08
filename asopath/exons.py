"""Deterministic design-space enumeration for exon-skipping ASOs (AGENT.md section 5).

Everything here is computed from Ensembl sequence, never from model memory: exon boundaries,
reading-frame phase, spliced-junction translation, premature stops and deleted protein length.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from functools import lru_cache

HOSTS = ["https://rest.ensembl.org", "https://grch37.rest.ensembl.org"]
CACHE = __import__("pathlib").Path(".cache/ensembl")
CODONS = dict(zip(
    (a + b + c for a in "TCAG" for b in "TCAG" for c in "TCAG"),
    "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"))


def _get(path: str, text: bool = False):
    """Ensembl REST with on-disk cache; falls back to the GRCh37 mirror (same transcript CDS) when the main host is down."""
    cache = CACHE / (hashlib.md5(path.encode()).hexdigest() + (".txt" if text else ".json"))
    if cache.exists():
        raw = cache.read_text()
        return raw if text else json.loads(raw)
    last = None
    for attempt in range(3):
        for host in HOSTS:
            try:
                req = urllib.request.Request(host + path, headers={"Accept": "text/plain" if text else "application/json", "User-Agent": "asopath/0.1"})
                raw = urllib.request.urlopen(req, timeout=90).read().decode()
                CACHE.mkdir(parents=True, exist_ok=True)
                cache.write_text(raw)
                return raw if text else json.loads(raw)
            except Exception as e:
                last = e
        time.sleep(2 * (attempt + 1))
    raise last


def translate(cds: str) -> str:
    return "".join(CODONS.get(cds[i:i + 3], "X") for i in range(0, len(cds) - len(cds) % 3, 3))


@lru_cache(maxsize=8)
def load_transcript(gene: str, transcript: str | None = None) -> dict:
    """Canonical (or given) transcript: per-exon CDS segments in transcript order."""
    if not transcript:
        transcript = _get(f"/lookup/symbol/homo_sapiens/{gene}?expand=0")["canonical_transcript"].split(".")[0]
    t = _get(f"/lookup/id/{transcript}?expand=1")
    tr = t["Translation"]
    cdna = _get(f"/sequence/id/{transcript}?type=cdna", text=True).strip().upper()
    minus = t["strand"] == -1
    exons = sorted(t["Exon"], key=lambda e: e["start"], reverse=minus)   # transcript order
    # CDS start/end positions in transcript coordinates
    cds_genomic_start = tr["end"] if minus else tr["start"]
    cds_genomic_end = tr["start"] if minus else tr["end"]
    pos, cds_t0, cds_t1, spans = 0, None, None, []
    for e in exons:
        ln = e["end"] - e["start"] + 1
        lo, hi = (e["end"], e["start"]) if minus else (e["start"], e["end"])   # transcript-order ends
        if cds_t0 is None and min(e["start"], e["end"]) <= cds_genomic_start <= max(e["start"], e["end"]):
            cds_t0 = pos + abs(cds_genomic_start - lo)
        if min(e["start"], e["end"]) <= cds_genomic_end <= max(e["start"], e["end"]):
            cds_t1 = pos + abs(cds_genomic_end - lo)
        spans.append((pos, pos + ln, e))
        pos += ln
    assert pos == len(cdna), f"exon lengths {pos} != cDNA {len(cdna)}"
    cds = cdna[cds_t0:cds_t1 + 1]
    protein = translate(cds)
    assert protein.endswith("*") or len(protein) >= tr["length"], "CDS translation mismatch"
    segs = []
    for i, (a, b, e) in enumerate(spans, 1):
        lo, hi = max(a, cds_t0), min(b, cds_t1 + 1)
        segs.append({"exon": i, "id": e["id"], "exon_len": b - a,
                     "cds_start": lo - cds_t0 if hi > lo else None, "cds_len": max(0, hi - lo),
                     "genomic": f"chrX:{e['start']}-{e['end']}" if e["seq_region_name"] == "X" else f"{e['seq_region_name']}:{e['start']}-{e['end']}"})
    return {"gene": gene, "transcript": transcript, "name": t["display_name"], "cds": cds,
            "protein_len": len(protein.rstrip("*")), "exons": segs}


def _skip(tx: dict, a: int, b: int) -> dict:
    cds, segs = tx["cds"], tx["exons"]
    cut = [s for s in segs[a - 1:b] if s["cds_len"]]
    removed = sum(s["cds_len"] for s in cut)
    first, last = cut[0], cut[-1]
    new = cds[:first["cds_start"]] + cds[last["cds_start"] + last["cds_len"]:]
    prot = translate(new)
    stop = prot.find("*")
    in_frame = removed % 3 == 0
    return {
        "skip": f"{a}" if a == b else f"{a}-{b}",
        "exons": list(range(a, b + 1)),
        "n_exons": b - a + 1,
        "bp_removed": removed,
        "in_frame": in_frame,
        "frame_shift": removed % 3,
        "new_stop_at_aa": stop + 1 if 0 <= stop < len(prot) - 1 else None,
        "premature_stop": 0 <= stop < len(prot) - 1,
        "protein_len": len(prot.rstrip("*")),
        "aa_deleted": (tx["protein_len"] - len(prot.rstrip("*"))) if in_frame else None,
        "deleted_aa_range": f"{first['cds_start'] // 3 + 1}-{(last['cds_start'] + last['cds_len']) // 3}",
        "oligos_min_max": f"1 (if coordinated skipping exists) to {b - a + 1}",
        "junction": f"{cds[max(0, first['cds_start'] - 12):first['cds_start']]}|{cds[last['cds_start'] + last['cds_len']:last['cds_start'] + last['cds_len'] + 12]}",
    }


def enumerate_skips(gene: str, target_exon: int, max_span: int = 12, transcript: str | None = None) -> dict:
    """All contiguous skips of exons containing `target_exon` (so the mutation is removed),
    with frame, junction stop and deleted-protein consequences. Sorted by AGENT.md section 5 ranking."""
    tx = load_transcript(gene, transcript)
    segs = tx["exons"]
    n = len(segs)
    te = segs[target_exon - 1]
    out = []
    for width in range(1, max_span + 1):
        for a in range(max(1, target_exon - width + 1), target_exon + 1):
            b = a + width - 1
            if b > n or a < 1:
                continue
            if not any(s["cds_len"] for s in segs[a - 1:b]):
                continue
            out.append(_skip(tx, a, b))
    viable = [o for o in out if o["in_frame"] and not o["premature_stop"]]
    viable.sort(key=lambda o: (o["n_exons"], o["aa_deleted"]))
    return {
        "gene": gene, "transcript": tx["transcript"], "transcript_name": tx["name"],
        "protein_aa": tx["protein_len"], "target_exon": target_exon,
        "target_exon_len": te["exon_len"], "target_exon_cds_len": te["cds_len"],
        "target_exon_frame_mod3": te["cds_len"] % 3,
        "target_alone_in_frame": te["cds_len"] % 3 == 0,
        "exon_lengths": {s["exon"]: s["cds_len"] for s in segs[max(0, target_exon - 8):target_exon + 7]},
        "viable_in_frame_skips": viable,
        "rejected_skips": [{"skip": o["skip"], "why": "out of frame" if not o["in_frame"] else f"premature stop at aa {o['new_stop_at_aa']}"}
                           for o in out if not (o["in_frame"] and not o["premature_stop"])],
        "note": "Contiguous blocks only; coordinated-skipping behaviour (one ASO, several exons) is NOT computed here - it is a literature question.",
    }


if __name__ == "__main__":
    import sys
    r = enumerate_skips(sys.argv[1], int(sys.argv[2]))
    print(json.dumps({k: v for k, v in r.items() if k != "rejected_skips"}, indent=1)[:5000])
