#!/usr/bin/env python3
"""
GSC-Driven Topic Selector
Picks the best blog topic based on Google Search Console demand data.

Usage:
  from gsc_topic_selector import pick_topic_gsc_driven, load_gsc_cache

  topic = pick_topic_gsc_driven(persona, used_topics)
  # Returns: "best rental income tracker Canada" (or highest-scoring available topic)
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple

_SCRIPT_DIR = Path(__file__).parent
_LOCAL_CACHE_DIR = _SCRIPT_DIR / "data" / "gsc_cache"
_SIBLING_CACHE_DIR = _SCRIPT_DIR.parent / "rental-management-app" / "data" / "gsc_cache"

# Prefer local data/gsc_cache/; fall back to sibling rental-management-app
CACHE_DIR = _LOCAL_CACHE_DIR if _LOCAL_CACHE_DIR.exists() else _SIBLING_CACHE_DIR
GSC_CACHE_FILE = CACHE_DIR / "gsc_queries_90d.json"

STOP_WORDS = frozenset({
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'among', 'throughout',
    'despite', 'towards', 'upon', 'within', 'without', 'can', 'canada',
    'cra', 'line', 'vs', 'versus', '2026', '2025', '2024',
})


def load_gsc_cache() -> dict:
    """Load GSC cache from disk. Returns empty structure if missing."""
    if not GSC_CACHE_FILE.exists():
        return {"queries": []}
    with open(GSC_CACHE_FILE) as f:
        return json.load(f)


def _normalize(text: str) -> set:
    """Lowercase, strip punctuation, remove stop words, return keyword set."""
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    return {w for w in text.split() if w not in STOP_WORDS and len(w) > 2}


def _score_topic(topic: str, gsc_queries: list) -> Tuple[float, List[str], int, float]:
    """Score a topic against GSC queries. Returns (score, matched_queries, total_impressions, avg_position)."""
    topic_kw = _normalize(topic)
    if not topic_kw:
        return 0.0, [], 0, 100.0

    matched, total_imp, pos_sum, pos_count = [], 0, 0.0, 0

    for q in gsc_queries:
        keys = q.get("keys", [""])
        query = keys[0] if isinstance(keys, list) else keys
        imp = q.get("impressions", 0)
        pos = q.get("position", 100)
        overlap = topic_kw & _normalize(query)

        if overlap:
            weight = imp * (1.0 / max(pos, 1))
            matched.append(query)
            total_imp += imp
            pos_sum += pos
            pos_count += 1

    if not matched:
        return 0.0, [], 0, 100.0

    score = sum(
        q.get("impressions", 0) * (1.0 / max(q.get("position", 1), 1))
        for q in gsc_queries
        if any(w in q.get("keys", [""])[0].lower() for w in topic_kw)
    )
    return score, matched, total_imp, pos_sum / pos_count


def _find_gaps(gsc_queries: list, persona_topics: list) -> list:
    """Find high-impression GSC queries not covered by existing persona topics."""
    persona_kw = set()
    for t in persona_topics:
        persona_kw |= _normalize(t)

    gaps = []
    for q in gsc_queries:
        keys = q.get("keys", [""])
        query = keys[0] if isinstance(keys, list) else keys
        imp = q.get("impressions", 0)
        pos = q.get("position", 100)
        lower = query.lower()

        if (imp >= 10 and 5 <= pos <= 30
                and "rentalops" not in lower and "rental ops" not in lower):
            query_kw = _normalize(query) - STOP_WORDS
            if len(persona_kw & query_kw) <= 2:
                gaps.append({
                    "topic": query,
                    "score": imp * (1.0 / pos),
                    "impressions": imp,
                    "position": pos,
                })

    gaps.sort(key=lambda x: x["score"], reverse=True)
    return gaps[:5]


def pick_topic_gsc_driven(
    persona: dict,
    used_topics: list,
    fallback_fn=None,
) -> Optional[str]:
    """Pick the best topic for a persona using GSC demand data.

    Args:
        persona: dict with "name" and "topics" keys
        used_topics: list of already-used topic strings
        fallback_fn: optional callable(persona, used_topics) -> str for fallback

    Returns:
        Best topic string, or result of fallback_fn, or None.
    """
    cache = load_gsc_cache()
    queries = cache.get("queries", [])

    if not queries:
        if fallback_fn:
            return fallback_fn(persona, used_topics)
        return None

    scored = []
    for topic in persona.get("topics", []):
        if topic in used_topics:
            continue
        score, matched, imp, pos = _score_topic(topic, queries)
        scored.append({
            "topic": topic, "score": score, "impressions": imp,
            "position": pos, "matched": matched, "is_gap": False,
        })

    gaps = _find_gaps(queries, persona.get("topics", []))
    for g in gaps:
        scored.append({
            "topic": g["topic"], "score": g["score"],
            "impressions": g["impressions"], "position": g["position"],
            "matched": [], "is_gap": True,
        })

    if not scored:
        if fallback_fn:
            return fallback_fn(persona, used_topics)
        return None

    scored.sort(key=lambda x: x["score"], reverse=True)
    best = scored[0]

    if best["is_gap"]:
        print(f"🎯 GSC Gap: {best['topic']} (impr: {best['impressions']}, pos: {best['position']:.1f})")
    else:
        print(f"🎯 GSC Scored: {best['topic']} (score: {best['score']:.1f}, impr: {best['impressions']}, pos: {best['position']:.1f})")
        if best["matched"]:
            print(f"   Matches: {', '.join(best['matched'][:3])}")

    return best["topic"]


# ─── CLI entry point ─────────────────────────────
if __name__ == "__main__":
    # Demo: score a sample persona
    sample_persona = {
        "name": "First-Time Landlord",
        "topics": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "landlord tenant board Ontario how it works",
            "how to set rent price Canadian rental property",
            "security deposit rules Ontario landlords",
        ],
    }
    result = pick_topic_gsc_driven(sample_persona, used_topics=[], fallback_fn=lambda p, u: p["topics"][0])
    print(f"\nSelected: {result}")
