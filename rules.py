"""The rule engine: a small, explicit knowledge base applied AFTER the LLM's
claim-by-claim verdicts. This is the deliberately symbolic half of the
system — fixed, human-written rules rather than another model call, so its
behaviour is fully predictable and explainable. It never invents new
claims; it only adjusts or annotates verdicts the LLM already produced.

Two kinds of rule run here:
  1. Source-trust rules — a hand-maintained tier list of domains.
  2. A numeric-verification rule — checks whether a figure in the claim
     actually appears, verbatim, in the source text that supposedly backs it.

Cross-source contradiction checking is NOT done here, on purpose: spotting
that two sources disagree needs real language understanding (different
wording for the same fact), which a fixed rule table can't do reliably.
That check lives in critic.py as a separate LLM call instead — see
check_conflicts(). Keeping the two kinds of checking apart, instead of
blending them, makes it obvious in the code (and in a report) which parts
of Verily are classical/symbolic and which are model-based.
"""

import re

# ---------------------------------------------------------------- knowledge base

# Deliberately small and conservative: only domains we're confident about go
# in here. Anything not listed is "unclassified" rather than guessed at —
# an unfamiliar .com site is not assumed untrustworthy, just unrated.
HIGH_TRUST_SUFFIXES = (".gov", ".edu", ".int", ".mil")

# Government, academic and research domains in country-code form, e.g.
# isro.gov.in, iitb.ac.in, nic.in sites, gov.uk, ox.ac.uk, edu.au.
# Without this, only US-style .gov/.edu sites counted as high trust.
COUNTRY_HIGH_TRUST = re.compile(r"(^|\.)(gov|edu|ac|nic|res|mil)\.[a-z]{2}$")

HIGH_TRUST_DOMAINS = {
    # international
    "who.int", "nature.com", "sciencedirect.com", "ncbi.nlm.nih.gov",
    "un.org", "nasa.gov", "cdc.gov", "nih.gov", "unesco.org",
    # India (bodies not covered by the .gov.in / .ac.in pattern)
    "rbi.org.in", "icmr.org.in", "sebi.gov.in", "isro.gov.in",
}
MEDIUM_TRUST_DOMAINS = {
    # international
    "bbc.com", "reuters.com", "apnews.com", "npr.org", "theguardian.com",
    "nytimes.com", "washingtonpost.com", "wsj.com", "economist.com",
    "time.com", "nationalgeographic.com", "scientificamerican.com",
    "smithsonianmag.com", "britannica.com", "wikipedia.org",
    # India
    "thehindu.com", "indianexpress.com", "hindustantimes.com",
    "livemint.com", "business-standard.com", "ndtv.com",
    "indiatoday.in", "timesofindia.indiatimes.com", "downtoearth.org.in",
}
LOW_TRUST_DOMAINS = {
    "medium.com", "blogspot.com", "wordpress.com", "tumblr.com",
    "answers.com", "ehow.com",
}


def _matches(domain, listed):
    """True if domain is a listed site or a subdomain of one
    (e.g. en.wikipedia.org matches wikipedia.org)."""
    return any(domain == d or domain.endswith("." + d) for d in listed)


def trust_tier(domain):
    """Classify one source domain: "high" | "medium" | "low" | "unclassified"."""
    domain = domain.lower()
    if (domain.endswith(HIGH_TRUST_SUFFIXES) or COUNTRY_HIGH_TRUST.search(domain)
            or _matches(domain, HIGH_TRUST_DOMAINS)):
        return "high"
    if _matches(domain, MEDIUM_TRUST_DOMAINS):
        return "medium"
    if _matches(domain, LOW_TRUST_DOMAINS):
        return "low"
    return "unclassified"


_TIER_RANK = {"high": 3, "medium": 2, "unclassified": 1, "low": 0}


def best_tier(tiers):
    """The most trustworthy tier among a claim's cited sources."""
    return max(tiers, key=lambda t: _TIER_RANK[t]) if tiers else "unclassified"


# ---------------------------------------------------------------- rules

# Digits with optional internal separators ("2,400", "3.5") and an optional
# "%". A trailing full stop or comma is NOT part of the number, so "1969."
# at the end of a sentence still matches "1969" in the source.
_NUMBER = re.compile(r"\d+(?:[.,]\d+)*%?")


def _numbers_in(text):
    # "2,400" and "2400" are the same number, so commas are dropped
    return {n.replace(",", "") for n in _NUMBER.findall(text)}


def apply_rules(claims, sources):
    """Run the knowledge-base rules over the LLM's claims and annotate them.

    Adds to each claim: "trust" (best tier among its cited sources),
    "cross_verified" (2+ sources agree, vs. just 1), and "rule_notes" (a
    trace of which rule changed anything — shown in the UI so the check is
    auditable, not a black box). May downgrade "supported" to "partial";
    never upgrades a verdict and never invents a correction the LLM didn't
    already consider — a rule-flagged claim keeps its original wording and
    is just marked less certain.
    """
    by_id = {s["id"]: s for s in sources}
    out = []
    for c in claims:
        c = dict(c)
        cited = [by_id[n] for n in c["sources"] if n in by_id]
        tiers = [trust_tier(s["domain"]) for s in cited]
        c["trust"] = best_tier(tiers)
        c["cross_verified"] = len(cited) >= 2
        notes = []

        if c["verdict"] == "supported" and cited and all(t == "low" for t in tiers):
            c["verdict"] = "partial"
            c["correction"] = c["correction"] or c["claim"]
            notes.append("Every cited source is in a lower-trust category "
                        "(rule: low-trust-only \u2192 partial).")

        if c["verdict"] == "supported":
            claim_nums = _numbers_in(c["claim"])
            if claim_nums and cited:
                source_nums = set()
                for s in cited:
                    source_nums |= _numbers_in(s["text"])
                missing = claim_nums - source_nums
                if missing:
                    c["verdict"] = "partial"
                    c["correction"] = c["correction"] or c["claim"]
                    shown = ", ".join(sorted(missing))
                    notes.append(f"Figure {shown} doesn't appear verbatim in the "
                                f"cited source(s) (rule: numeric verification).")

        c["rule_notes"] = notes
        out.append(c)
    return out


# ---------------------------------------------------------------- scoring

_WEIGHT = {"supported": 1.0, "partial": 0.5, "unsupported": 0.0}


def confidence_score(claims):
    """A single 0-100 score summarising how well the draft held up.

    Cross-verified (2+ source) supported claims count fully; single-source
    supported claims count slightly less, since only one source backed
    them — a direct, explainable application of the "more sources agreeing
    is stronger evidence" idea, not a model judgement.
    """
    if not claims:
        return None
    total = 0.0
    for c in claims:
        w = _WEIGHT.get(c["verdict"], 0.0)
        if c["verdict"] == "supported" and not c.get("cross_verified"):
            w = 0.85
        total += w
    return round(100 * total / len(claims))
