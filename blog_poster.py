import os
import json
import requests
import random
import re
import time
from datetime import datetime

# GSC-driven topic selection (falls back gracefully when cache/API unavailable)
try:
    from gsc_topic_selector import pick_topic_gsc_driven, load_gsc_cache
except ImportError:
    pick_topic_gsc_driven = None
    load_gsc_cache = lambda: {"queries": []}

# API Keys from GitHub Secrets
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
DEVTO_API_KEY = os.environ.get('DEVTO_API_KEY')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')

# ─────────────────────────────────────────────
# PERSONAS & HIGH-INTENT CRA TOPICS
# ─────────────────────────────────────────────
PERSONAS = [
    {
        "name": "First-Time Landlord",
        "description": "Someone who recently became a landlord and is overwhelmed by taxes, compliance, and paperwork. Has 1-2 properties.",
        "topics": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "CRA Line 8960: Repairs vs Capital Expenses for Canadian Landlords",
            "Ontario landlord tenant board rules 2026",
            "how to screen tenants legally Canada",
            "security deposit rules Ontario landlords",
            "first time landlord mistakes Canada",
            "how to set rent price Canadian rental property",
            "landlord tenant board Ontario how it works",
            "how to write lease agreement Ontario",
            "CRA audit rental income what triggers it Canada",
            "is rental income taxable in Canada",
            "landlord tax deductions Canada complete guide",
            "what can landlords claim CRA landlord tax deductions checklist",
        ],
    },
    {
        "name": "Portfolio Builder",
        "description": "A small landlord with 2-5 properties looking to manage efficiently and minimize tax burden without an accountant for every question.",
        "topics": [
            "tracking rental income expenses multiple properties Canada",
            "Can Landlords Deduct Mortgage Interest in Canada Line 8710",
            "capital cost allowance rental property Canada explained",
            "GST HST Canadian landlords what you need to know",
            "how to incorporate rental properties Canada",
            "automating rent collection multiple properties Canada",
            "refinancing rental properties Canada tax implications",
            "holding company rental properties Canada benefits",
            "landlord multiple provinces Canada rules",
            "property manager vs self managing Canada tax comparison",
            "year end tax checklist Canadian landlords multiple properties",
            "rental property depreciation Canada CCA guide",
            "capital gains rental property Canada landlord guide",
        ],
    },
    {
        "name": "Accidental Landlord",
        "description": "Someone renting out a property by necessity — inherited home, relocated for work, couldn't sell. 1 property, very uncertain about rules.",
        "topics": [
            "tax rules renting out principal residence Canada",
            "reporting rental income part year landlord Canada",
            "renting out basement suite Canada rules",
            "CRA Line 9220: Deducting Utilities for a Basement Suite",
            "capital gains selling rental property Canada",
            "failing to report rental income CRA consequences",
            "short term vs long term rental tax rules Canada",
            "Airbnb tax rules Canadian landlords 2026",
            "converting rental property back to personal use Canada",
            "insurance requirements renting home Canada",
            "CRA principal residence exemption rental income Canada",
            "what happens CRA audit rental property Canada",
            "rental income affect tax bracket Canada",
        ],
    },
    {
        "name": "Part-Time Property Manager",
        "description": "Someone managing 2-5 properties for family or as side income alongside a full-time job. Wants simple systems not complexity.",
        "topics": [
            "rental income tax bracket Canada 2026",
            "home office deduction landlord Canada",
            "record keeping requirements Canadian landlords CRA",
            "splitting rental income spouse Canada tax",
            "How to Calculate Motor Vehicle Expenses for Landlords Line 9281",
            "rental property accounting software vs spreadsheets Canada",
            "property management software Canada landlords",
            "tax season preparation part time landlord Canada",
            "professional fees deduction landlord Canada legal accounting",
            "passive income rental income CRA rules Canada",
            "landlord accounting software Canada review",
            "best rental income tracker Canada",
        ],
    },
]

# ─────────────────────────────────────────────
# PILLAR POSTS 
# ─────────────────────────────────────────────
PILLAR_POSTS = [
    {
        "id": "cra-tax-pillar",
        "cluster": "CRA Tax & Reporting",
        "topic": "rental income tax Canada complete guide small landlords 2026",
        "title_hint": "Rental Income Tax in Canada: Complete Guide for Small Landlords (2026)",
        "description": "The definitive guide covering everything a 1-3 property Canadian landlord needs to know about rental income tax, T776, CRA compliance, and deductions.",
        "target_word_count": 3500,
        "cluster_posts": [
            "rental property tax deductions Canada 2026",
            "how to fill out T776 form Canada step by step",
            "CRA Line 8960: Repairs vs Capital Expenses for Canadian Landlords",
            "Can Landlords Deduct Mortgage Interest in Canada Line 8710",
            "CRA Line 9220: Deducting Utilities for a Basement Suite",
            "How to Calculate Motor Vehicle Expenses for Landlords Line 9281",
            "what can landlords claim CRA landlord tax deductions checklist",
        ],
        "internal_links": [
            {
                "slug": "failing-to-report-rental-income-to-cra-a-costly-mistake-for-canadian-landlords",
                "title": "Failing to Report Rental Income to CRA: A Costly Mistake for Canadian Landlords",
            },
            {
                "slug": "year-end-tax-checklist-for-canadian-landlords-a-comprehensive-guide",
                "title": "Year-End Tax Checklist for Canadian Landlords: A Comprehensive Guide",
            },
            {
                "slug": "reporting-rental-income-in-canada-a-guide-for-part-year-landlords",
                "title": "Reporting Rental Income in Canada: A Guide for Part-Year Landlords",
            },
        ],
    },
    {
        "id": "ontario-landlord-pillar",
        "cluster": "Ontario Landlord Rules",
        "topic": "Ontario landlord guide 2026 rules rights responsibilities small landlords",
        "title_hint": "Ontario Landlord Guide 2026: Rules, Rights and Responsibilities",
        "description": "Everything a small Ontario landlord needs to know about the LTB, lease agreements, tenant screening, security deposits, and eviction rules.",
        "target_word_count": 3500,
        "cluster_posts": [
            "Ontario landlord tenant board rules 2026",
            "how to write lease agreement Ontario",
            "security deposit rules Ontario landlords",
            "how to screen tenants legally Canada",
            "landlord tenant board Ontario how it works",
            "converting rental property back to personal use Canada",
            "reporting rental income part year landlord Canada",
        ],
        "internal_links": [
            {
                "slug": "converting-rental-property-to-personal-use-in-canada-a-step-by-step-guide",
                "title": "Converting Rental Property to Personal Use in Canada: A Step-by-Step Guide",
            },
        ],
    },
]

# ─────────────────────────────────────────────────────────────
# CORE API CALL HANDLERS (FIXES GEMINI 404 AND FALLBACKS)
# ─────────────────────────────────────────────────────────────

def call_gemini_api(prompt_text):
    """
    Handles robust text generation with official pathing fallbacks to prevent 404s.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: Missing Gemini API configuration inside running environment.")

    # Fix: Route directly through standard v1 instead of the broken v1beta endpoint for 2.0-flash
    url = f"https://googleapis.com{api_key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Fallback Strategy: If 2.0 still returns a 404 for your account tier, jump to stable 1.5-flash path
        if response.status_code == 404:
            print("Model 2.0-flash returned 404. Dropping back to stable v1beta/gemini-1.5-flash route...")
            fallback_url = f"https://googleapis.com{api_key}"
            response = requests.post(fallback_url, json=payload, headers=headers)
            
        response.raise_for_status()
        
        # Parse the content return object safely
        response_data = response.json()
        return response_data['candidates']['content']['parts']['text']

    except Exception as e:
        print(f"❌ Gemini API call failed: {e}")
        raise e
