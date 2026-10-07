"""Research tools backed by public structured resources (AGENT.md section 3).

We do not rebuild biomedical knowledge infrastructure; each tool is a thin,
size-bounded wrapper over an existing API. Tools never raise: errors are
returned as text so the agent can reason about missing data (and report
uncertainty) instead of crashing the pipeline.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Callable

MAX_RESULT_CHARS = 12_000
TIMEOUT = 30
UA = "rarepath/0.1 (therapeutic-development research tool)"


def _get(url: str, *, data: bytes | None = None, headers: dict | None = None) -> bytes:
    h = {"User-Agent": UA, "Accept": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def _json(url: str, **kw) -> dict:
    return json.loads(_get(url, **kw))


def _q(**params) -> str:
    return urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})


# --- individual tools -------------------------------------------------------

def monarch_search_disease(query: str) -> dict:
    d = _json("https://api-v3.monarchinitiative.org/v3/api/search?" +
              _q(q=query, category="biolink:Disease", limit=6))
    return {"results": [
        {"id": i.get("id"), "name": i.get("name"), "synonyms": (i.get("has_synonym") or [])[:5],
         "description": (i.get("description") or "")[:400]}
        for i in d.get("items", [])]}


def monarch_disease_genes(disease_id: str) -> dict:
    d = _json(f"https://api-v3.monarchinitiative.org/v3/api/association?" +
              _q(object=disease_id, category="biolink:CausalGeneToDiseaseAssociation", limit=15))
    return {"causal_genes": [
        {"gene": i.get("subject_label"), "id": i.get("subject"), "predicate": i.get("predicate"),
         "evidence_count": i.get("evidence_count")} for i in d.get("items", [])]}


def pubmed_search(query: str, max_results: int = 8) -> dict:
    max_results = min(int(max_results), 15)
    ids = _json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" +
                _q(db="pubmed", term=query, retmax=max_results, retmode="json", sort="relevance"))
    idlist = ids["esearchresult"]["idlist"]
    if not idlist:
        return {"count": 0, "articles": [], "note": "No results. Absence of literature is not evidence against a hypothesis."}
    xml = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" +
               _q(db="pubmed", id=",".join(idlist), retmode="xml"), headers={"Accept": "application/xml"})
    out = []
    for art in ET.fromstring(xml).findall(".//PubmedArticle"):
        abstract = " ".join("".join(t.itertext()) for t in art.findall(".//AbstractText"))
        out.append({
            "pmid": art.findtext(".//PMID"),
            "title": "".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else "",
            "year": art.findtext(".//PubDate/Year") or (art.findtext(".//PubDate/MedlineDate") or "")[:4],
            "journal": art.findtext(".//Journal/Title"),
            "abstract": abstract[:1100],
        })
    return {"count": len(out), "articles": out}


def clinicaltrials_search(condition: str, intervention: str | None = None, max_results: int = 10) -> dict:
    d = _json("https://clinicaltrials.gov/api/v2/studies?" + _q(
        **{"query.cond": condition, "query.intr": intervention,
           "pageSize": min(int(max_results), 20), "format": "json"}))
    out = []
    for s in d.get("studies", []):
        p = s.get("protocolSection", {})
        idm, st, dm = p.get("identificationModule", {}), p.get("statusModule", {}), p.get("designModule", {})
        out.append({
            "nct": idm.get("nctId"), "title": idm.get("briefTitle"),
            "status": st.get("overallStatus"), "phases": dm.get("phases"),
            "why_stopped": st.get("whyStopped"),
            "interventions": [i.get("name") for i in p.get("armsInterventionsModule", {}).get("interventions", [])][:5],
        })
    return {"studies": out}


def opentargets_search(query: str) -> dict:
    gql = """query($q:String!){search(queryString:$q,entityNames:["disease","target","drug"],page:{index:0,size:6}){
      hits{id entity name description}}}"""
    d = _json("https://api.platform.opentargets.org/api/v4/graphql",
              data=json.dumps({"query": gql, "variables": {"q": query}}).encode(),
              headers={"Content-Type": "application/json"})
    return {"hits": [{**h, "description": (h.get("description") or "")[:250]}
                     for h in d["data"]["search"]["hits"]]}


def opentargets_disease_targets(disease_id: str, size: int = 15) -> dict:
    """disease_id is an EFO/MONDO/Orphanet id as returned by opentargets_search, e.g. MONDO_0010679."""
    gql = """query($id:String!,$n:Int!){disease(efoId:$id){name
      associatedTargets(page:{index:0,size:$n}){count rows{score target{id approvedSymbol approvedName}}}}}"""
    d = _json("https://api.platform.opentargets.org/api/v4/graphql",
              data=json.dumps({"query": gql, "variables": {"id": disease_id.replace(":", "_"), "n": min(int(size), 25)}}).encode(),
              headers={"Content-Type": "application/json"})
    dis = (d.get("data") or {}).get("disease")
    if not dis:
        return {"error": f"disease {disease_id} not found"}
    return {"disease": dis["name"], "total_targets": dis["associatedTargets"]["count"],
            "targets": [{"symbol": r["target"]["approvedSymbol"], "ensembl": r["target"]["id"],
                         "name": r["target"]["approvedName"], "score": round(r["score"], 3)}
                        for r in dis["associatedTargets"]["rows"]]}


def chembl_target_drugs(gene_symbol: str) -> dict:
    """Known mechanisms/drugs acting on a human target. Answers: does an existing agent already do this?"""
    t = _json("https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + _q(q=gene_symbol, limit=10))
    tgt = next((x for x in t.get("targets", [])
                if x.get("organism") == "Homo sapiens" and x.get("target_type") == "SINGLE PROTEIN"), None)
    if not tgt:
        return {"note": f"No single-protein human ChEMBL target found for {gene_symbol}"}
    tid = tgt["target_chembl_id"]
    m = _json("https://www.ebi.ac.uk/chembl/api/data/mechanism.json?" + _q(target_chembl_id=tid, limit=30))
    mechs = m.get("mechanisms", [])
    ids = sorted({x["molecule_chembl_id"] for x in mechs if x.get("molecule_chembl_id")})
    names: dict[str, dict] = {}
    if ids:
        mol = _json("https://www.ebi.ac.uk/chembl/api/data/molecule.json?" +
                    _q(molecule_chembl_id__in=",".join(ids), limit=50))
        names = {x["molecule_chembl_id"]: x for x in mol.get("molecules", [])}
    return {"target": tid, "target_name": tgt.get("pref_name"), "mechanisms": [
        {"molecule": names.get(x["molecule_chembl_id"], {}).get("pref_name") or x["molecule_chembl_id"],
         "max_phase": names.get(x["molecule_chembl_id"], {}).get("max_phase"),
         "action": x.get("action_type"), "mechanism": x.get("mechanism_of_action")} for x in mechs],
        "note": "Empty mechanisms means no curated drug mechanism in ChEMBL, not that no tool compound exists."}


def uniprot_protein(gene_symbol: str) -> dict:
    d = _json("https://rest.uniprot.org/uniprotkb/search?" + _q(
        query=f"gene_exact:{gene_symbol} AND organism_id:9606 AND reviewed:true",
        fields="accession,gene_names,protein_name,length,cc_function,cc_subcellular_location,cc_tissue_specificity,cc_disease",
        format="json", size=1))
    r = (d.get("results") or [None])[0]
    if not r:
        return {"note": f"No reviewed human UniProt entry for {gene_symbol}"}
    comments = {}
    for c in r.get("comments", []):
        txt = " ".join(t.get("value", "") for t in c.get("texts", []))
        if c["commentType"] == "SUBCELLULAR LOCATION":
            txt = "; ".join(l["location"]["value"] for l in c.get("subcellularLocations", []))
        comments.setdefault(c["commentType"], []).append(txt[:700])
    return {"accession": r["primaryAccession"], "length": r.get("sequence", {}).get("length"),
            "protein": r.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value"),
            "comments": comments}


# --- registry ---------------------------------------------------------------

def _tool(name: str, description: str, props: dict, required: list[str]) -> dict:
    return {"name": name, "description": description,
            "input_schema": {"type": "object", "properties": props, "required": required, "additionalProperties": False}}


S = {"type": "string"}
REGISTRY: dict[str, tuple[dict, Callable[..., dict]]] = {
    "monarch_search_disease": (_tool("monarch_search_disease",
        "Resolve a disease name to MONDO identifiers (Monarch). Use first to identify the disease.",
        {"query": S}, ["query"]), monarch_search_disease),
    "monarch_disease_genes": (_tool("monarch_disease_genes",
        "Causal genes for a MONDO disease id (Monarch).", {"disease_id": S}, ["disease_id"]), monarch_disease_genes),
    "pubmed_search": (_tool("pubmed_search",
        "Search PubMed; returns titles and abstract excerpts. Use for mechanistic questions, rescue experiments, "
        "disease models, and to look for contradicting evidence. Supports PubMed query syntax.",
        {"query": S, "max_results": {"type": "integer"}}, ["query"]), pubmed_search),
    "clinicaltrials_search": (_tool("clinicaltrials_search",
        "Search ClinicalTrials.gov by condition and optional intervention (status, phase, why_stopped).",
        {"condition": S, "intervention": S, "max_results": {"type": "integer"}}, ["condition"]), clinicaltrials_search),
    "opentargets_search": (_tool("opentargets_search",
        "Search Open Targets for disease/target/drug ids.", {"query": S}, ["query"]), opentargets_search),
    "opentargets_disease_targets": (_tool("opentargets_disease_targets",
        "Top associated targets for a disease id (e.g. MONDO_0010679) from Open Targets. Association is not causality.",
        {"disease_id": S, "size": {"type": "integer"}}, ["disease_id"]), opentargets_disease_targets),
    "chembl_target_drugs": (_tool("chembl_target_drugs",
        "Curated drugs/clinical compounds and mechanisms for a human gene symbol (ChEMBL). Use to find existing agents.",
        {"gene_symbol": S}, ["gene_symbol"]), chembl_target_drugs),
    "uniprot_protein": (_tool("uniprot_protein",
        "Protein function, subcellular location, tissue specificity for a human gene symbol (UniProt). "
        "Use to judge extracellular vs intracellular biology and delivery.", {"gene_symbol": S}, ["gene_symbol"]), uniprot_protein),
}


def schemas(names: list[str]) -> list[dict]:
    return [REGISTRY[n][0] for n in names]


def run_tool(name: str, args: dict) -> tuple[str, bool]:
    """Returns (text, is_error). Never raises."""
    if name not in REGISTRY:
        return f"Unknown tool {name}", True
    try:
        text = json.dumps(REGISTRY[name][1](**args), ensure_ascii=False)
    except (urllib.error.URLError, TimeoutError, ET.ParseError, KeyError, TypeError, ValueError) as e:
        return f"Tool error ({type(e).__name__}): {e}. Treat this source as unavailable; do not infer absence.", True
    if len(text) > MAX_RESULT_CHARS:
        text = text[:MAX_RESULT_CHARS] + "...[truncated]"
    return text, False
