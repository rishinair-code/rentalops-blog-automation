#!/usr/bin/env python3
"""
GSC Cache Refresh for rentalops-blog-automation
Pulls 90 days of Google Search Console query/page data into data/gsc_cache/

Usage:
  python3 refresh_gsc_cache.py --force

Auth:
  - Local dev: looks for service account JSON at <repo>/gen-lang-client-0434933989-9a10aec11373.json
  - GitHub Actions: reads GSC_SERVICE_ACCOUNT_KEY (JSON string) from env, writes temp file
"""

import os
import json
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SITE_URL = "sc-domain:rentalops.ca"
DAYS_BACK = 90

CACHE_DIR = Path(__file__).parent / "data" / "gsc_cache"
CACHE_FILE = CACHE_DIR / "gsc_queries_90d.json"
META_FILE = CACHE_DIR / "cache_meta.json"

# Local dev fallback — service account JSON in repo root
_LOCAL_SA_FILE = Path(__file__).parent / "gen-lang-client-0434933989-9a10aec11373.json"


def _get_service_account_file() -> str:
    """Return path to service account JSON, writing from env if needed."""
    # CI: GSC_SERVICE_ACCOUNT_KEY is JSON string
    sa_key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY")
    if sa_key:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(json.loads(sa_key), tmp)
        tmp.close()
        return tmp.name

    # Local dev: service account file in repo root
    if _LOCAL_SA_FILE.exists():
        return str(_LOCAL_SA_FILE)

    raise FileNotFoundError(
        "No service account found. Set GSC_SERVICE_ACCOUNT_KEY env var (CI) "
        f"or place JSON at {_LOCAL_SA_FILE} (local)."
    )


def get_gsc_service():
    creds = service_account.Credentials.from_service_account_file(
        _get_service_account_file(),
        scopes=['https://www.googleapis.com/auth/webmasters.readonly'],
    )
    return build('searchconsole', 'v1', credentials=creds)


def fetch_gsc_queries(service, start_date: str, end_date: str, row_limit: int = 1000) -> list:
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query'],
        'rowLimit': row_limit,
        'orderBy': [{'field': 'impressions', 'descending': True}],
    }
    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    return response.get('rows', [])


def fetch_gsc_pages(service, start_date: str, end_date: str, row_limit: int = 100) -> list:
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page'],
        'rowLimit': row_limit,
        'orderBy': [{'field': 'clicks', 'descending': True}],
    }
    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    return response.get('rows', [])


def main():
    print("=" * 60)
    print("🔄 GSC Cache Refresh (blog-automation)")
    print("=" * 60)

    force = '--force' in sys.argv
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Skip if fresh (< 24h) unless --force
    if not force and META_FILE.exists():
        with open(META_FILE) as f:
            meta = json.load(f)
        age = datetime.now() - datetime.fromisoformat(meta["last_refresh"])
        if age < timedelta(hours=24):
            print("⏭️  Cache fresh (< 24h). Skipping. Use --force to override.")
            return 0

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=DAYS_BACK)

    print(f"📡 Fetching GSC data for {SITE_URL}")
    print(f"   Range: {start_date} → {end_date}")

    try:
        service = get_gsc_service()
        print("✅ GSC authenticated")

        queries = fetch_gsc_queries(service, str(start_date), str(end_date), row_limit=1000)
        print(f"   Queries: {len(queries)}")
        pages = fetch_gsc_pages(service, str(start_date), str(end_date), row_limit=100)
        print(f"   Pages: {len(pages)}")

        total_clicks = sum(r.get('clicks', 0) for r in queries)
        total_impr = sum(r.get('impressions', 0) for r in queries)
        avg_ctr = sum(r.get('ctr', 0) for r in queries) / len(queries) if queries else 0
        avg_pos = sum(r.get('position', 0) for r in queries) / len(queries) if queries else 0

        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump({
                "fetched_at": datetime.now().isoformat(),
                "date_range": {"start": str(start_date), "end": str(end_date)},
                "site_url": SITE_URL,
                "queries": queries,
                "pages": pages,
                "summary": {
                    "total_queries": len(queries),
                    "total_clicks": total_clicks,
                    "total_impressions": total_impr,
                    "avg_ctr": avg_ctr,
                    "avg_position": avg_pos,
                },
            }, f, indent=2)

        with open(META_FILE, 'w') as f:
            json.dump({"last_refresh": datetime.now().isoformat(), "version": 1}, f, indent=2)

        print(f"✅ Saved: {len(queries)} queries, {len(pages)} pages")
        print(f"   Clicks: {total_clicks} | Impr: {total_impr} | CTR: {avg_ctr:.2%} | Avg pos: {avg_pos:.1f}")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
