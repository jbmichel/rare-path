"""Retrieval tools served to research agents (in addition to built-in WebSearch / WebFetch)."""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "asopath/0.1"


def _get(url: str, accept: str = "application/json") -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept}), timeout=45).read()


def pubmed_search(query: str, max_results: int = 8) -> dict:
    n = min(int(max_results), 15)
    ids = json.loads(_get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "term": query, "retmax": n, "retmode": "json", "sort": "relevance"})))["esearchresult"]["idlist"]
    if not ids:
        return {"count": 0, "articles": []}
    xml = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}), "application/xml")
    out = []
    for a in ET.fromstring(xml).findall(".//PubmedArticle"):
        t = a.find(".//ArticleTitle")
        out.append({"pmid": a.findtext(".//PMID"), "title": "".join(t.itertext()) if t is not None else "",
                    "year": a.findtext(".//PubDate/Year") or (a.findtext(".//PubDate/MedlineDate") or "")[:4],
                    "abstract": " ".join("".join(x.itertext()) for x in a.findall(".//AbstractText"))[:1200]})
    return {"count": len(out), "articles": out}


def europepmc_search(query: str, max_results: int = 8) -> dict:
    """Europe PMC: also covers preprints (bioRxiv/medRxiv) and recent literature."""
    d = json.loads(_get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(
        {"query": query, "format": "json", "pageSize": min(int(max_results), 15), "resultType": "core", "sort": "RELEVANCE"})))
    return {"count": d.get("hitCount"), "results": [
        {"id": r.get("pmid") or r.get("id"), "source": r.get("source"), "title": r.get("title"), "year": r.get("pubYear"),
         "abstract": (r.get("abstractText") or "")[:1200]} for r in d.get("resultList", {}).get("result", [])]}


def clinicaltrials_search(condition: str, intervention: str | None = None, max_results: int = 10) -> dict:
    p = {"query.cond": condition, "pageSize": min(int(max_results), 20), "format": "json"}
    if intervention:
        p["query.intr"] = intervention
    d = json.loads(_get("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(p)))
    out = []
    for s in d.get("studies", []):
        pr = s.get("protocolSection", {})
        i, st = pr.get("identificationModule", {}), pr.get("statusModule", {})
        out.append({"nct": i.get("nctId"), "title": i.get("briefTitle"), "sponsor": pr.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name"),
                    "status": st.get("overallStatus"), "phases": pr.get("designModule", {}).get("phases"),
                    "interventions": [x.get("name") for x in pr.get("armsInterventionsModule", {}).get("interventions", [])][:4],
                    "updated": st.get("lastUpdatePostDateStruct", {}).get("date")})
    return {"studies": out}


def _s(desc, props, req):
    return {"description": desc, "input_schema": {"type": "object", "properties": props, "required": req}}


REGISTRY = {
    "pubmed_search": (_s("Search PubMed; returns titles, years and abstracts.",
                         {"query": {"type": "string"}, "max_results": {"type": "integer"}}, ["query"]), pubmed_search),
    "europepmc_search": (_s("Search Europe PMC (includes preprints and very recent papers).",
                            {"query": {"type": "string"}, "max_results": {"type": "integer"}}, ["query"]), europepmc_search),
    "clinicaltrials_search": (_s("Search ClinicalTrials.gov by condition and optional intervention; returns sponsor, status, phase.",
                                 {"condition": {"type": "string"}, "intervention": {"type": "string"}, "max_results": {"type": "integer"}},
                                 ["condition"]), clinicaltrials_search),
}


def run_tool(name: str, args: dict) -> tuple[str, bool]:
    try:
        return json.dumps(REGISTRY[name][1](**args))[:12000], False
    except Exception as e:  # tools never raise
        return f"tool error: {type(e).__name__}: {e}", True
