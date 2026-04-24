"""
WtfDig importer: parses a wtfdig.info URL and uses Claude to generate
structured mechanic drill data ready for database import.

The wtfdig.info pages are fully JS-rendered so we can only scrape a small
amount of raw text.  Claude fills the gaps using its FFXIV domain knowledge
and the strategy name from the URL hash (e.g. #toxic → Toxic Friends strat).
"""

import json
import os
import re

import requests

# ---------------------------------------------------------------------------
# Fight + tier metadata used to seed the Claude prompt
# ---------------------------------------------------------------------------

FIGHT_KNOWLEDGE: dict[str, dict] = {
    "m1s":  {"name": "AAC Light-heavyweight M1 (Savage)", "short_name": "M1S",  "boss": "Black Cat",          "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.0"},
    "m2s":  {"name": "AAC Light-heavyweight M2 (Savage)", "short_name": "M2S",  "boss": "Honey B. Lovely",    "difficulty": "SAVAGE",   "arena_shape": "CIRCLE", "patch": "7.0"},
    "m3s":  {"name": "AAC Light-heavyweight M3 (Savage)", "short_name": "M3S",  "boss": "Brute Bomber",       "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.0"},
    "m4s":  {"name": "AAC Light-heavyweight M4 (Savage)", "short_name": "M4S",  "boss": "Wicked Thunder",     "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.0"},
    "m5s":  {"name": "AAC Cruiserweight M1 (Savage)",     "short_name": "M5S",  "boss": "Dancing Green",      "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.2"},
    "m6s":  {"name": "AAC Cruiserweight M2 (Savage)",     "short_name": "M6S",  "boss": "Sugar Riot",         "difficulty": "SAVAGE",   "arena_shape": "CIRCLE", "patch": "7.2"},
    "m7s":  {"name": "AAC Cruiserweight M3 (Savage)",     "short_name": "M7S",  "boss": "Brute Abomination",  "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.2"},
    "m8s":  {"name": "AAC Cruiserweight M4 (Savage)",     "short_name": "M8S",  "boss": "Howling Blade",      "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.2"},
    "m9s":  {"name": "AAC Heavyweight M1 (Savage)",       "short_name": "M9S",  "boss": "Vamp Fatale",        "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.4"},
    "m10s": {"name": "AAC Heavyweight M2 (Savage)",       "short_name": "M10S", "boss": "Honey B. Fierce",    "difficulty": "SAVAGE",   "arena_shape": "CIRCLE", "patch": "7.4"},
    "m11s": {"name": "AAC Heavyweight M3 (Savage)",       "short_name": "M11S", "boss": "Brute Distortion",   "difficulty": "SAVAGE",   "arena_shape": "SQUARE", "patch": "7.4"},
    "m12s": {"name": "AAC Heavyweight M4 (Savage)",       "short_name": "M12S", "boss": "Howling Blade Prime", "difficulty": "SAVAGE",  "arena_shape": "SQUARE", "patch": "7.4"},
    "fru":  {"name": "Futures Rewritten (Ultimate)",      "short_name": "FRU",  "boss": "Eden's Promise",     "difficulty": "ULTIMATE", "arena_shape": "SQUARE", "patch": "7.1"},
    "top":  {"name": "The Omega Protocol (Ultimate)",     "short_name": "TOP",  "boss": "Omega",              "difficulty": "ULTIMATE", "arena_shape": "SQUARE", "patch": "6.3"},
    "dsr":  {"name": "Dragonsong's Reprise (Ultimate)",   "short_name": "DSR",  "boss": "King Thordan",       "difficulty": "ULTIMATE", "arena_shape": "CIRCLE", "patch": "6.1"},
    "ucob": {"name": "The Unending Coil of Bahamut (Ultimate)", "short_name": "UCoB", "boss": "Bahamut Prime", "difficulty": "ULTIMATE", "arena_shape": "CIRCLE", "patch": "4.1"},
    "uwu":  {"name": "The Weapon's Refrain (Ultimate)",   "short_name": "UWU",  "boss": "The Ultima Weapon",  "difficulty": "ULTIMATE", "arena_shape": "CIRCLE", "patch": "4.3"},
}

PATCH_TO_TIER: dict[str, dict] = {
    "7.0": {"slug": "aac-lhw", "name": "AAC Light-heavyweight", "expansion": "Dawntrail", "patch": "7.0", "order": 1},
    "7.1": {"slug": "fru",     "name": "Futures Rewritten",     "expansion": "Dawntrail", "patch": "7.1", "order": 2},
    "7.2": {"slug": "aac-cw",  "name": "AAC Cruiserweight",     "expansion": "Dawntrail", "patch": "7.2", "order": 4},
    "7.4": {"slug": "aac-hw",  "name": "AAC Heavyweight",       "expansion": "Dawntrail", "patch": "7.4", "order": 3},
    "6.3": {"slug": "top",     "name": "The Omega Protocol",    "expansion": "Endwalker", "patch": "6.3", "order": 9},
    "6.1": {"slug": "dsr",     "name": "Dragonsong's Reprise",  "expansion": "Endwalker", "patch": "6.1", "order": 8},
    "4.1": {"slug": "ucob",    "name": "Unending Coil",         "expansion": "Stormblood", "patch": "4.1", "order": 10},
    "4.3": {"slug": "uwu",     "name": "Weapon's Refrain",      "expansion": "Stormblood", "patch": "4.3", "order": 11},
}


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_wtfdig_url(url: str) -> dict:
    """
    Extract fight slug, patch, and strat from a wtfdig.info URL.

    Examples:
      https://wtfdig.info/74/m9s#toxic   → {fight_slug: "m9s", patch: "7.4", strat: "toxic"}
      https://wtfdig.info/74/m9s         → {fight_slug: "m9s", patch: "7.4", strat: ""}
    """
    pattern = r'wtfdig\.info/(\d+)/(\w+)(?:#(\S+))?'
    m = re.search(pattern, url)
    if not m:
        raise ValueError(
            f"Not a recognised wtfdig.info URL: {url!r}. "
            "Expected format: https://wtfdig.info/<patch>/<fight>[#strat]"
        )
    raw_patch = m.group(1)    # "74"
    fight_slug = m.group(2).lower()  # "m9s"
    strat = m.group(3) or ""  # "toxic" or ""

    # Convert "74" → "7.4"
    if len(raw_patch) == 2:
        patch = f"{raw_patch[0]}.{raw_patch[1:]}"
    else:
        patch = raw_patch

    return {"patch": patch, "fight_slug": fight_slug, "strat": strat, "url": url}


# ---------------------------------------------------------------------------
# Page scraping (best-effort — page is JS-rendered)
# ---------------------------------------------------------------------------

def fetch_page_text(url: str) -> str:
    """
    Fetch whatever text the server returns for a wtfdig.info URL.
    Because the page is fully client-side rendered, most mechanic data
    won't appear here — but we send it to Claude anyway so it can pick up
    any static text that does make it through (e.g. strategy names).
    """
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        resp.raise_for_status()
        html = resp.text
        # Strip scripts, styles, and HTML tags to leave readable text
        html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
        html = re.sub(r'<style[^>]*>.*?</style>',   ' ', html, flags=re.DOTALL)
        html = re.sub(r'<[^>]+>',                   ' ', html)
        text = re.sub(r'\s+', ' ', html).strip()
        return text[:10000]
    except Exception as exc:
        return f"(Page fetch failed: {exc})"


# ---------------------------------------------------------------------------
# Claude-powered data generation
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are an expert FFXIV raid strategy assistant with encyclopaedic knowledge of
every released raid mechanic and its standard Party Finder (PF) strategies.

Your task is to produce a structured JSON dataset for a mechanic drill trainer.

━━━ COORDINATE SYSTEM ━━━
All positions are normalised 0.0–1.0:
  x: 0 = left wall, 1 = right wall
  y: 0 = north wall, 1 = south wall
  centre = (0.5, 0.5)

8-clock cardinals/intercardinals (approximate):
  N  = (0.50, 0.10)   NE = (0.82, 0.18)
  E  = (0.90, 0.50)   SE = (0.82, 0.82)
  S  = (0.50, 0.90)   SW = (0.18, 0.82)
  W  = (0.10, 0.50)   NW = (0.18, 0.18)

━━━ ROLES & SPOTS ━━━
TANK spot 1 = MT  |  TANK spot 2 = OT
HEALER spot 1 = H1  |  HEALER spot 2 = H2
MELEE spot 1 = M1  |  MELEE spot 2 = M2
RANGED spot 1 = R1  |  RANGED spot 2 = R2

Standard 8-clock: MT=N, H1=NE, M1=E, R1=SE, OT=S, H2=SW, M2=W, R2=NW
Light Party 1 (LP1): MT + H1 + M1 + R1
Light Party 2 (LP2): OT + H2 + M2 + R2

━━━ AoE SHAPES ━━━
circle: {shape, cx, cy, r, color, label}
rect:   {shape, x, y, w, h, color, label}
cone:   {shape, cx, cy, angle, spread, color, label}  (angle 0=N, 90=E, CW)

━━━ OUTPUT FORMAT ━━━
Return ONLY valid JSON — no markdown fences, no commentary.

{
  "fight": {
    "slug": "m9s",
    "name": "AAC Heavyweight M1 (Savage)",
    "short_name": "M9S",
    "boss_name": "Vamp Fatale",
    "difficulty": "SAVAGE",
    "arena_shape": "SQUARE",
    "order": 1
  },
  "tier": {
    "slug": "aac-hw",
    "name": "AAC Heavyweight",
    "expansion": "Dawntrail",
    "patch": "7.4",
    "order": 3
  },
  "mechanics": [
    {
      "slug": "mechanic-slug",
      "name": "Mechanic Name",
      "phase_name": "Phase 1",
      "description": "What this mechanic does.",
      "difficulty_rating": 3,
      "tags": ["spread", "stack"],
      "order": 1,
      "steps": [
        {
          "order": 1,
          "title": "Step title shown to the player",
          "narration": "Short coaching cue.",
          "timer_seconds": 5,
          "action_type": "POSITION",
          "default_tolerance": 0.12,
          "arena_state": {
            "boss_position": {"x": 0.5, "y": 0.5},
            "boss_facing": "north",
            "aoes": [],
            "markers": [],
            "tethers": [],
            "debuffs": []
          },
          "choices": [],
          "explanation": "Why this is correct.",
          "role_variants": [
            {"role": "TANK",   "spot": 1, "correct_position": {"x": 0.50, "y": 0.10}},
            {"role": "TANK",   "spot": 2, "correct_position": {"x": 0.50, "y": 0.90}},
            {"role": "HEALER", "spot": 1, "correct_position": {"x": 0.82, "y": 0.18}},
            {"role": "HEALER", "spot": 2, "correct_position": {"x": 0.18, "y": 0.82}},
            {"role": "MELEE",  "spot": 1, "correct_position": {"x": 0.90, "y": 0.50}},
            {"role": "MELEE",  "spot": 2, "correct_position": {"x": 0.10, "y": 0.50}},
            {"role": "RANGED", "spot": 1, "correct_position": {"x": 0.82, "y": 0.82}},
            {"role": "RANGED", "spot": 2, "correct_position": {"x": 0.18, "y": 0.18}}
          ]
        }
      ]
    }
  ]
}

For CHOICE steps:
  action_type = "CHOICE"
  choices = [{"id": "...", "label": "..."}, ...]
  In role_variants use "correct_choice": "choice_id" instead of correct_position.

Rules:
- Every step must have exactly 8 role_variants (TANK×2, HEALER×2, MELEE×2, RANGED×2).
- Use realistic, accurate positions for the named strategy.
- Use default_tolerance: 0.08 (very precise), 0.12 (standard), 0.18 (loose), 0.25 (half-arena).
- Cover all major mechanics of the fight, grouped into phases.
- Output ONLY the JSON object. No extra text.\
"""


def generate_preview(
    url: str,
    fight_slug: str,
    strat: str,
    scraped_text: str,
) -> dict:
    """
    Call the Claude API to generate a structured fight preview.

    Raises:
        ImportError if the anthropic package is not installed.
        EnvironmentError if ANTHROPIC_API_KEY is not set.
        json.JSONDecodeError if Claude returns invalid JSON.
        anthropic.APIError on API failures.
    """
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise ImportError(
            "The 'anthropic' package is required for the wtfdig importer. "
            "Run: pip install anthropic"
        ) from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Export it before starting the Django server."
        )

    fight_info = FIGHT_KNOWLEDGE.get(fight_slug, {})
    strat_label = f" using the '{strat}' strategy" if strat else " using PF-standard strategy"
    tier_info = PATCH_TO_TIER.get(fight_info.get("patch", ""), {})

    user_message = f"""\
Generate the complete mechanic drill dataset for:
  Fight:    {fight_info.get('name', fight_slug.upper())}
  Boss:     {fight_info.get('boss', 'Unknown')}
  Strategy: {strat_label}
  Source:   {url}

Fight metadata:
  difficulty  = {fight_info.get('difficulty', 'SAVAGE')}
  arena_shape = {fight_info.get('arena_shape', 'SQUARE')}
  patch       = {fight_info.get('patch', '?')}
  tier        = {tier_info.get('name', 'Unknown')}

Raw text scraped from the page (JS-rendered; may be incomplete):
---
{scraped_text[:8000]}
---

Generate ALL mechanics for this fight with full step breakdowns and
role-specific positions.  Use the strategy named above for positioning.
Include every distinct player decision point as a separate step.
Output only the JSON.\
"""

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw = response.content[0].text.strip()
    # Strip accidental markdown fences
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$',          '', raw)

    return json.loads(raw)
