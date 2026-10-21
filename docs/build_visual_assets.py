"""
Visual Asset Builder for Datheon Python Programming Internship Suite
Generates production-grade light-theme SVGs and renders crisp PNGs via headless Chrome.
"""
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(r"d:\intership\python\mw")
IMAGES_DIR = BASE_DIR / "assets" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def render_svg_to_png(svg_path: Path, png_path: Path, width: int, height: int):
    """Renders an SVG file to PNG using Chrome headless via an HTML wrapper."""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #FAF9F6;
  }}
  svg {{
    width: {width}px;
    height: {height}px;
    display: block;
  }}
</style>
</head>
<body>
{svg_path.read_text(encoding='utf-8')}
</body>
</html>
"""
    temp_html = svg_path.with_suffix(".temp.html")
    temp_html.write_text(html_content, encoding="utf-8")
    
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={png_path.resolve()}",
        f"file:///{temp_html.resolve().as_posix()}"
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        print(f"Rendered: {png_path.name} ({width}x{height}) - Exists: {png_path.exists()}")
    finally:
        if temp_html.exists():
            temp_html.unlink()

# ==============================================================================
# 1. LINKEDIN SHOWCASE BANNER (1200 x 675 - 16:9)
# ==============================================================================
linkedin_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675">
  <defs>
    <linearGradient id="liBgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <linearGradient id="liMeshBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="liMeshPurple" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A855F7" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#7C3AED" stop-opacity="0.0"/>
    </linearGradient>
    <linearGradient id="topAccent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3B82F6"/>
      <stop offset="35%" stop-color="#8B5CF6"/>
      <stop offset="70%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>
    <filter id="liShadow" x="-10%" y="-10%" width="125%" height="130%">
      <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#0F172A" flood-opacity="0.06"/>
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.03"/>
    </filter>
  </defs>

  <!-- Background Base -->
  <rect width="1200" height="675" rx="20" fill="url(#liBgGrad)"/>
  <rect width="1200" height="675" rx="20" fill="none" stroke="#E2E8F0" stroke-width="2"/>
  <path d="M 0 20 Q 0 0 20 0 L 1180 0 Q 1200 0 1200 20 L 1200 6 L 0 6 Z" fill="url(#topAccent)"/>

  <!-- Ambient Light Orbs -->
  <circle cx="120" cy="120" r="160" fill="url(#liMeshBlue)"/>
  <circle cx="1080" cy="140" r="170" fill="url(#liMeshPurple)"/>

  <!-- Header Section -->
  <g transform="translate(60, 36)">
    <!-- Pill Badges -->
    <g transform="translate(0, 0)">
      <rect width="210" height="28" rx="14" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.5"/>
      <circle cx="14" cy="14" r="5" fill="#4F46E5"/>
      <text x="26" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="11" font-weight="800" fill="#4338CA" letter-spacing="0.5">DATHEON INTERNSHIP</text>
    </g>
    <g transform="translate(222, 0)">
      <rect width="160" height="28" rx="14" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5"/>
      <circle cx="14" cy="14" r="5" fill="#10B981"/>
      <text x="26" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="11" font-weight="800" fill="#047857" letter-spacing="0.5">PYTHON 3.10+</text>
    </g>
    <g transform="translate(394, 0)">
      <rect width="195" height="28" rx="14" fill="#FEF3C7" stroke="#FDE68A" stroke-width="1.5"/>
      <circle cx="14" cy="14" r="5" fill="#D97706"/>
      <text x="26" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="11" font-weight="800" fill="#B45309" letter-spacing="0.5">100% UNIT TEST PASS</text>
    </g>

    <!-- Main Title -->
    <text x="0" y="66" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="30" font-weight="900" fill="#0F172A" letter-spacing="-0.5">
      Python Engineering Internship — 4-Project Capstone Suite
    </text>
    <text x="0" y="93" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, sans-serif" font-size="14.5" font-weight="400" fill="#64748B">
      Engineered by <tspan font-weight="700" fill="#1E293B">Maheswari</tspan> • Decoupled Clean Architecture • 58 Automated Unit Tests • Pure Python Standard Library
    </text>
  </g>

  <!-- 4 Bento Cards (2x2 Grid) -->
  <g transform="translate(60, 155)">

    <!-- CARD 01: HANGMAN -->
    <g transform="translate(0, 0)" filter="url(#liShadow)">
      <rect width="525" height="205" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect width="6" height="205" rx="3" fill="#0284C7"/>
      
      <g transform="translate(22, 18)">
        <rect width="72" height="24" rx="6" fill="#E0F2FE"/>
        <text x="10" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="800" fill="#0369A1">TASK 01</text>
        <text x="84" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="17" font-weight="800" fill="#0F172A">Hangman Console Engine</text>
        
        <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12.5" font-weight="400" fill="#475569">
          Deterministic word guessing state machine with isolated ASCII gallows.
        </text>

        <!-- Feature chips -->
        <g transform="translate(0, 58)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#0369A1">✓ 6-Mistake Ceiling</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#0369A1">✓ Repeat Input Immunity</text>
        </g>
        <g transform="translate(0, 90)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#0369A1">✓ 8,076 English Words</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F0FDF4" stroke="#BBF7D0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#15803D">✓ 18 Unit Tests (100%)</text>
        </g>

        <!-- Code Pill -->
        <g transform="translate(0, 126)">
          <rect width="480" height="26" rx="6" fill="#F1F5F9"/>
          <text x="12" y="17" font-family="'JetBrains Mono', monospace" font-size="11" fill="#334155">$ python task1_hangman/hangman.py --word PYTHON</text>
        </g>
      </g>
    </g>

    <!-- CARD 02: PORTFOLIO TRACKER -->
    <g transform="translate(555, 0)" filter="url(#liShadow)">
      <rect width="525" height="205" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect width="6" height="205" rx="3" fill="#059669"/>
      
      <g transform="translate(22, 18)">
        <rect width="72" height="24" rx="6" fill="#DCFCE7"/>
        <text x="10" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="800" fill="#15803D">TASK 02</text>
        <text x="84" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="17" font-weight="800" fill="#0F172A">Stock Portfolio Tracker</text>
        
        <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12.5" font-weight="400" fill="#475569">
          Valuation analytics engine with S&amp;P 500 validation &amp; RFC 4180 CSV export.
        </text>

        <!-- Feature chips -->
        <g transform="translate(0, 58)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#047857">✓ Real-time/Offline Feeds</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#047857">✓ 503 S&amp;P Constituents</text>
        </g>
        <g transform="translate(0, 90)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#047857">✓ P&amp;L Metric Calculations</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F0FDF4" stroke="#BBF7D0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#15803D">✓ 14 Unit Tests (100%)</text>
        </g>

        <!-- Code Pill -->
        <g transform="translate(0, 126)">
          <rect width="480" height="26" rx="6" fill="#F1F5F9"/>
          <text x="12" y="17" font-family="'JetBrains Mono', monospace" font-size="11" fill="#334155">$ python task2_portfolio/portfolio.py --demo</text>
        </g>
      </g>
    </g>

    <!-- CARD 03: FILE ORGANIZER -->
    <g transform="translate(0, 222)" filter="url(#liShadow)">
      <rect width="525" height="205" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect width="6" height="205" rx="3" fill="#D97706"/>
      
      <g transform="translate(22, 18)">
        <rect width="72" height="24" rx="6" fill="#FEF3C7"/>
        <text x="10" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="800" fill="#B45309">TASK 03</text>
        <text x="84" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="17" font-weight="800" fill="#0F172A">Automated File Organizer</text>
        
        <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12.5" font-weight="400" fill="#475569">
          Safe filesystem categorizer across 8 taxonomy categories with audit trails.
        </text>

        <!-- Feature chips -->
        <g transform="translate(0, 58)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#B45309">✓ Root &amp; System32 Guard</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#B45309">✓ Dry-Run Zero Disk State</text>
        </g>
        <g transform="translate(0, 90)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#B45309">✓ Collision Renaming</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F0FDF4" stroke="#BBF7D0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#15803D">✓ 12 Unit Tests (100%)</text>
        </g>

        <!-- Code Pill -->
        <g transform="translate(0, 126)">
          <rect width="480" height="26" rx="6" fill="#F1F5F9"/>
          <text x="12" y="17" font-family="'JetBrains Mono', monospace" font-size="11" fill="#334155">$ python task3_file_organizer/organizer.py --dry-run</text>
        </g>
      </g>
    </g>

    <!-- CARD 04: FAQ CHATBOT -->
    <g transform="translate(555, 222)" filter="url(#liShadow)">
      <rect width="525" height="205" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
      <rect width="6" height="205" rx="3" fill="#7C3AED"/>
      
      <g transform="translate(22, 18)">
        <rect width="72" height="24" rx="6" fill="#F3E8FF"/>
        <text x="10" y="16" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="800" fill="#6B21A8">TASK 04</text>
        <text x="84" y="18" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="17" font-weight="800" fill="#0F172A">Rule-Based FAQ Assistant</text>
        
        <text x="0" y="44" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12.5" font-weight="400" fill="#475569">
          Deterministic token NLP engine answering queries without hallucinations.
        </text>

        <!-- Feature chips -->
        <g transform="translate(0, 58)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#6B21A8">✓ Token Scoring (0.40)</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#6B21A8">✓ JSON Schema Adapter</text>
        </g>
        <g transform="translate(0, 90)">
          <rect width="180" height="24" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
          <text x="10" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="600" fill="#6B21A8">✓ Truthful Fallback</text>

          <rect x="190" width="185" height="24" rx="6" fill="#F0FDF4" stroke="#BBF7D0"/>
          <text x="200" y="16" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#15803D">✓ 14 Unit Tests (100%)</text>
        </g>

        <!-- Code Pill -->
        <g transform="translate(0, 126)">
          <rect width="480" height="26" rx="6" fill="#F1F5F9"/>
          <text x="12" y="17" font-family="'JetBrains Mono', monospace" font-size="11" fill="#334155">$ python task4_chatbot/chatbot.py --query "Stipend"</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Bottom Metric Bar -->
  <g transform="translate(60, 600)">
    <rect width="1080" height="52" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#liShadow)"/>
    
    <g transform="translate(24, 16)">
      <circle cx="8" cy="10" r="5" fill="#10B981"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="800" fill="#0F172A">58 / 58 UNIT TESTS PASSING</text>
    </g>

    <g transform="translate(300, 16)">
      <circle cx="8" cy="10" r="5" fill="#3B82F6"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#334155">ZERO EXTERNAL DEPENDENCIES</text>
    </g>

    <g transform="translate(615, 16)">
      <circle cx="8" cy="10" r="5" fill="#8B5CF6"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#334155">CLIENT-SIDE WEB DASHBOARD</text>
    </g>

    <g transform="translate(900, 16)">
      <circle cx="8" cy="10" r="5" fill="#F59E0B"/>
      <text x="20" y="14" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="700" fill="#334155">MIT OPEN SOURCE</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 2. TASK 01 HANGMAN CARD (1000 x 440)
# ==============================================================================
task1_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440">
  <defs>
    <linearGradient id="t1Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F0F9FF"/>
    </linearGradient>
    <filter id="t1Shadow" x="-5%" y="-5%" width="115%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0284C7" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1000" height="440" rx="18" fill="url(#t1Bg)"/>
  <rect width="1000" height="440" rx="18" fill="none" stroke="#BAE6FD" stroke-width="2"/>
  <rect x="0" y="0" width="1000" height="6" fill="#0284C7"/>

  <!-- Left: Visual Mockup Container -->
  <g transform="translate(40, 36)" filter="url(#t1Shadow)">
    <rect width="400" height="368" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect width="400" height="36" rx="14" fill="#F8FAFC"/>
    <circle cx="24" cy="18" r="5" fill="#EF4444"/>
    <circle cx="42" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="60" cy="18" r="5" fill="#10B981"/>
    <text x="80" y="22" font-family="'JetBrains Mono', monospace" font-size="11.5" fill="#64748B">hangman_engine.py</text>

    <!-- Gallows ASCII Art Visual -->
    <g transform="translate(40, 60)">
      <g stroke="#334155" stroke-width="3" stroke-linecap="round">
        <line x1="20" y1="180" x2="110" y2="180"/>
        <line x1="60" y1="180" x2="60" y2="30"/>
        <line x1="60" y1="30" x2="130" y2="30"/>
        <line x1="130" y1="30" x2="130" y2="55"/>
        <!-- Figure -->
        <circle cx="130" cy="70" r="15" fill="none" stroke="#0284C7" stroke-width="2.5"/>
        <line x1="130" y1="85" x2="130" y2="125" stroke="#0284C7" stroke-width="2.5"/>
        <line x1="130" y1="95" x2="105" y2="115" stroke="#0284C7" stroke-width="2.5"/>
        <line x1="130" y1="95" x2="155" y2="115" stroke="#0284C7" stroke-width="2.5"/>
        <line x1="130" y1="125" x2="110" y2="155" stroke="#0284C7" stroke-width="2.5"/>
        <line x1="130" y1="125" x2="150" y2="155" stroke="#0284C7" stroke-width="2.5"/>
      </g>
    </g>

    <!-- Word Guess Tiles -->
    <g transform="translate(220, 90)">
      <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#64748B">MYSTERY WORD:</text>
      <g transform="translate(0, 14)">
        <g transform="translate(0,0)"><rect width="22" height="30" rx="4" fill="#E0F2FE" stroke="#0284C7"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#0369A1">P</text></g>
        <g transform="translate(26,0)"><rect width="22" height="30" rx="4" fill="#E0F2FE" stroke="#0284C7"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#0369A1">Y</text></g>
        <g transform="translate(52,0)"><rect width="22" height="30" rx="4" fill="#E0F2FE" stroke="#0284C7"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#0369A1">T</text></g>
        <g transform="translate(78,0)"><rect width="22" height="30" rx="4" fill="#E0F2FE" stroke="#0284C7"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#0369A1">H</text></g>
        <g transform="translate(104,0)"><rect width="22" height="30" rx="4" fill="#F1F5F9" stroke="#CBD5E1"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#64748B">_</text></g>
        <g transform="translate(130,0)"><rect width="22" height="30" rx="4" fill="#E0F2FE" stroke="#0284C7"/><text x="6" y="21" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="800" fill="#0369A1">N</text></g>
      </g>

      <text x="0" y="75" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#64748B">MISTAKES REMAINING:</text>
      <g transform="translate(0, 85)">
        <circle cx="10" cy="8" r="7" fill="#0284C7"/>
        <circle cx="28" cy="8" r="7" fill="#0284C7"/>
        <circle cx="46" cy="8" r="7" fill="#0284C7"/>
        <circle cx="64" cy="8" r="7" fill="#0284C7"/>
        <circle cx="82" cy="8" r="7" fill="#E2E8F0" stroke="#94A3B8"/>
        <circle cx="100" cy="8" r="7" fill="#E2E8F0" stroke="#94A3B8"/>
        <text x="115" y="12" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#0284C7">4 / 6</text>
      </g>
    </g>

    <!-- Terminal Output Strip -->
    <g transform="translate(20, 290)">
      <rect width="360" height="60" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="22" font-family="'JetBrains Mono', monospace" font-size="11" fill="#10B981">&gt; Guess letter: O</text>
      <text x="12" y="42" font-family="'JetBrains Mono', monospace" font-size="11" fill="#0284C7">&gt; Splendid! 'O' is in the word! (Status: VICTORY)</text>
    </g>
  </g>

  <!-- Right: Architecture & Features -->
  <g transform="translate(470, 36)">
    <g>
      <rect width="90" height="26" rx="6" fill="#E0F2FE"/>
      <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#0369A1">MODULE 01</text>
      <text x="102" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" font-weight="900" fill="#0F172A">Hangman Console Game</text>
    </g>

    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" fill="#475569">
      An isolated finite-state engine providing interactive word-guessing gameplay with deterministic input sanitization and zero-penalty deduplication.
    </text>

    <!-- Spec List -->
    <g transform="translate(0, 95)" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13">
      <g transform="translate(0, 0)">
        <rect width="24" height="24" rx="12" fill="#E0F2FE"/>
        <text x="7" y="16" font-weight="800" fill="#0284C7">1</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Finite-State Lifecycle:</text>
        <text x="195" y="16" fill="#64748B">Active, Victory, Defeat with 7 ASCII stages</text>
      </g>

      <g transform="translate(0, 40)">
        <rect width="24" height="24" rx="12" fill="#E0F2FE"/>
        <text x="7" y="16" font-weight="800" fill="#0284C7">2</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Input Validation Sanitizer:</text>
        <text x="215" y="16" fill="#64748B">Strips whitespace, rejects punctuation/digits</text>
      </g>

      <g transform="translate(0, 80)">
        <rect width="24" height="24" rx="12" fill="#E0F2FE"/>
        <text x="7" y="16" font-weight="800" fill="#0284C7">3</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Word Corpus Integration:</text>
        <text x="215" y="16" fill="#64748B">8,076 verified words with offline fallback</text>
      </g>

      <g transform="translate(0, 120)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#15803D">✓</text>
        <text x="36" y="16" font-weight="700" fill="#15803D">18 Automated Unit Tests:</text>
        <text x="215" y="16" fill="#166534">100% Passing in 0.089s (unittest)</text>
      </g>
    </g>

    <!-- Terminal Command Snippet -->
    <g transform="translate(0, 275)">
      <rect width="490" height="85" rx="10" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.5"/>
      <rect width="490" height="26" rx="10" fill="#F0F9FF"/>
      <text x="14" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#0284C7">TERMINAL LAUNCH COMMAND</text>
      <text x="14" y="48" font-family="'JetBrains Mono', monospace" font-size="12" fill="#0F172A">$ python task1_hangman/hangman.py</text>
      <text x="14" y="70" font-family="'JetBrains Mono', monospace" font-size="11" fill="#64748B"># Or deterministic mode: python task1_hangman/hangman.py --word PYTHON</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 3. TASK 02 PORTFOLIO CARD (1000 x 440)
# ==============================================================================
task2_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440">
  <defs>
    <linearGradient id="t2Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F0FDF4"/>
    </linearGradient>
    <filter id="t2Shadow" x="-5%" y="-5%" width="115%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#059669" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1000" height="440" rx="18" fill="url(#t2Bg)"/>
  <rect width="1000" height="440" rx="18" fill="none" stroke="#BBF7D0" stroke-width="2"/>
  <rect x="0" y="0" width="1000" height="6" fill="#059669"/>

  <!-- Left: Financial Valuation Mockup -->
  <g transform="translate(40, 36)" filter="url(#t2Shadow)">
    <rect width="400" height="368" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect width="400" height="36" rx="14" fill="#F8FAFC"/>
    <circle cx="24" cy="18" r="5" fill="#EF4444"/>
    <circle cx="42" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="60" cy="18" r="5" fill="#10B981"/>
    <text x="80" y="22" font-family="'JetBrains Mono', monospace" font-size="11.5" fill="#64748B">portfolio_tracker.py --demo</text>

    <!-- Metrics Summary Card -->
    <g transform="translate(20, 50)">
      <rect width="360" height="70" rx="10" fill="#F0FDF4" stroke="#86EFAC"/>
      <text x="16" y="24" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#15803D">PORTFOLIO VALUATION</text>
      <text x="16" y="52" font-family="'JetBrains Mono', monospace" font-size="22" font-weight="800" fill="#065F46">$11,480.00</text>
      <rect x="230" y="16" width="115" height="36" rx="8" fill="#DCFCE7"/>
      <text x="242" y="38" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="800" fill="#15803D">+14.80% ▲</text>
    </g>

    <!-- Ticker Table Mockup -->
    <g transform="translate(20, 135)" font-family="'JetBrains Mono', monospace" font-size="11">
      <rect width="360" height="24" rx="4" fill="#F1F5F9"/>
      <text x="10" y="16" font-weight="700" fill="#475569">TICKER   QTY   BUY PRICE   MARKET    P&amp;L</text>

      <g transform="translate(0, 32)">
        <text x="10" y="0" font-weight="700" fill="#0F172A">AAPL     15    $175.00     $190.50   +$232.50</text>
        <text x="10" y="24" font-weight="700" fill="#0F172A">MSFT     10    $380.00     $420.00   +$400.00</text>
        <text x="10" y="48" font-weight="700" fill="#0F172A">GOOGL    12    $140.00     $165.00   +$300.00</text>
        <text x="10" y="72" font-weight="700" fill="#0F172A">NVDA      8    $450.00     $520.00   +$560.00</text>
      </g>
    </g>

    <!-- CSV Export Strip -->
    <g transform="translate(20, 275)">
      <rect width="360" height="75" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="22" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#059669">EXPORT: RFC 4180 COMPLIANT CSV</text>
      <text x="12" y="42" font-family="'JetBrains Mono', monospace" font-size="10" fill="#64748B">Ticker,Company,Shares,CostBasis,CurrentValue,GainLoss</text>
      <text x="12" y="60" font-family="'JetBrains Mono', monospace" font-size="10" fill="#15803D">✓ Saved: portfolio_summary_20261021.csv</text>
    </g>
  </g>

  <!-- Right: Architecture & Features -->
  <g transform="translate(470, 36)">
    <g>
      <rect width="90" height="26" rx="6" fill="#DCFCE7"/>
      <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#15803D">MODULE 02</text>
      <text x="102" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" font-weight="900" fill="#0F172A">Stock Portfolio Tracker</text>
    </g>

    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" fill="#475569">
      A financial valuation analytics tool calculating capital invested, current market worth, and percentage yield with strict constituent validation.
    </text>

    <!-- Spec List -->
    <g transform="translate(0, 95)" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13">
      <g transform="translate(0, 0)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#059669">1</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Provider-Independent Pricing:</text>
        <text x="240" y="16" fill="#64748B">Live quotes, offline cache, or manual input</text>
      </g>

      <g transform="translate(0, 40)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#059669">2</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">S&amp;P 500 Constituent Validation:</text>
        <text x="250" y="16" fill="#64748B">Validates against 503 verified companies</text>
      </g>

      <g transform="translate(0, 80)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#059669">3</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Educational Legal Disclaimer:</text>
        <text x="240" y="16" fill="#64748B">RFC-compliant audit disclaimers in exports</text>
      </g>

      <g transform="translate(0, 120)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#15803D">✓</text>
        <text x="36" y="16" font-weight="700" fill="#15803D">14 Automated Unit Tests:</text>
        <text x="215" y="16" fill="#166534">100% Passing in 0.058s (unittest)</text>
      </g>
    </g>

    <!-- Terminal Command Snippet -->
    <g transform="translate(0, 275)">
      <rect width="490" height="85" rx="10" fill="#FFFFFF" stroke="#BBF7D0" stroke-width="1.5"/>
      <rect width="490" height="26" rx="10" fill="#F0FDF4"/>
      <text x="14" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#059669">TERMINAL LAUNCH COMMAND</text>
      <text x="14" y="48" font-family="'JetBrains Mono', monospace" font-size="12" fill="#0F172A">$ python task2_portfolio/portfolio.py --demo</text>
      <text x="14" y="70" font-family="'JetBrains Mono', monospace" font-size="11" fill="#64748B"># Or interactive portfolio builder: python task2_portfolio/portfolio.py</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 4. TASK 03 ORGANIZER CARD (1000 x 440)
# ==============================================================================
task3_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440">
  <defs>
    <linearGradient id="t3Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#FFFBEB"/>
    </linearGradient>
    <filter id="t3Shadow" x="-5%" y="-5%" width="115%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#D97706" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1000" height="440" rx="18" fill="url(#t3Bg)"/>
  <rect width="1000" height="440" rx="18" fill="none" stroke="#FDE68A" stroke-width="2"/>
  <rect x="0" y="0" width="1000" height="6" fill="#D97706"/>

  <!-- Left: Taxonomy & Safety Mockup -->
  <g transform="translate(40, 36)" filter="url(#t3Shadow)">
    <rect width="400" height="368" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect width="400" height="36" rx="14" fill="#F8FAFC"/>
    <circle cx="24" cy="18" r="5" fill="#EF4444"/>
    <circle cx="42" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="60" cy="18" r="5" fill="#10B981"/>
    <text x="80" y="22" font-family="'JetBrains Mono', monospace" font-size="11.5" fill="#64748B">organizer.py --dry-run</text>

    <!-- Safety Shield Banner -->
    <g transform="translate(20, 50)">
      <rect width="360" height="52" rx="8" fill="#FEF2F2" stroke="#FECACA"/>
      <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#DC2626">🛡️ STRICT SAFETY GUARDRAIL ACTIVE</text>
      <text x="14" y="40" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" fill="#7F1D1D">Refuses: C:\, System32, /bin, &amp; Project Source Roots</text>
    </g>

    <!-- 8 Taxonomy Categories Grid -->
    <g transform="translate(20, 115)">
      <text x="0" y="0" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#64748B">8 SEMANTIC TAXONOMY FOLDERS:</text>
      
      <g transform="translate(0, 14)" font-family="'JetBrains Mono', monospace" font-size="10.5">
        <g transform="translate(0,0)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Documents (.pdf,.docx)</text></g>
        <g transform="translate(185,0)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Images (.png,.jpg,.svg)</text></g>
        <g transform="translate(0,30)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Audio (.mp3,.wav,.flac)</text></g>
        <g transform="translate(185,30)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Video (.mp4,.mkv,.mov)</text></g>
        <g transform="translate(0,60)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Archives (.zip,.tar.gz)</text></g>
        <g transform="translate(185,60)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Code (.py,.js,.html,.c)</text></g>
        <g transform="translate(0,90)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Executables (.exe,.msi)</text></g>
        <g transform="translate(185,90)"><rect width="175" height="24" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/><text x="8" y="16" fill="#0F172A">📁 Data (.csv,.json,.sql)</text></g>
      </g>
    </g>

    <!-- Simulation Output Strip -->
    <g transform="translate(20, 265)">
      <rect width="360" height="85" rx="8" fill="#FFFBEB" stroke="#FDE68A"/>
      <text x="12" y="22" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#B45309">[DRY-RUN PREVIEW] ZERO FILES MOVED</text>
      <text x="12" y="42" font-family="'JetBrains Mono', monospace" font-size="10" fill="#78350F">Planned: budget.xlsx -&gt; Documents/budget.xlsx</text>
      <text x="12" y="58" font-family="'JetBrains Mono', monospace" font-size="10" fill="#78350F">Planned: photo.png   -&gt; Images/photo.png</text>
      <text x="12" y="74" font-family="'JetBrains Mono', monospace" font-size="10" fill="#B45309">Audit: logs/organizer_audit.log ready</text>
    </g>
  </g>

  <!-- Right: Architecture & Features -->
  <g transform="translate(470, 36)">
    <g>
      <rect width="90" height="26" rx="6" fill="#FEF3C7"/>
      <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#B45309">MODULE 03</text>
      <text x="102" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" font-weight="900" fill="#0F172A">Automated File Organizer</text>
    </g>

    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" fill="#475569">
      A safety-first filesystem automation utility classifying disorganized directories into 8 semantic taxonomy categories with immutable audit logging.
    </text>

    <!-- Spec List -->
    <g transform="translate(0, 95)" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13">
      <g transform="translate(0, 0)">
        <rect width="24" height="24" rx="12" fill="#FEF3C7"/>
        <text x="7" y="16" font-weight="800" fill="#D97706">1</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Dry-Run Simulation Guard:</text>
        <text x="215" y="16" fill="#64748B">Previews operations without modifying disk state</text>
      </g>

      <g transform="translate(0, 40)">
        <rect width="24" height="24" rx="12" fill="#FEF3C7"/>
        <text x="7" y="16" font-weight="800" fill="#D97706">2</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Collision Resolution Policy:</text>
        <text x="215" y="16" fill="#64748B">Timestamp renaming prevents accidental overwrites</text>
      </g>

      <g transform="translate(0, 80)">
        <rect width="24" height="24" rx="12" fill="#FEF3C7"/>
        <text x="7" y="16" font-weight="800" fill="#D97706">3</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Anti-Recursive Idempotency:</text>
        <text x="215" y="16" fill="#64748B">Re-running ignores already-organized folders</text>
      </g>

      <g transform="translate(0, 120)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#15803D">✓</text>
        <text x="36" y="16" font-weight="700" fill="#15803D">12 Automated Unit Tests:</text>
        <text x="215" y="16" fill="#166534">100% Passing in 0.057s (unittest)</text>
      </g>
    </g>

    <!-- Terminal Command Snippet -->
    <g transform="translate(0, 275)">
      <rect width="490" height="85" rx="10" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5"/>
      <rect width="490" height="26" rx="10" fill="#FFFBEB"/>
      <text x="14" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#B45309">TERMINAL LAUNCH COMMAND</text>
      <text x="14" y="48" font-family="'JetBrains Mono', monospace" font-size="12" fill="#0F172A">$ python task3_file_organizer/organizer.py --dry-run</text>
      <text x="14" y="70" font-family="'JetBrains Mono', monospace" font-size="11" fill="#64748B"># Live run: python task3_file_organizer/organizer.py --target "C:\\Downloads"</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 5. TASK 04 FAQ CHATBOT CARD (1000 x 440)
# ==============================================================================
task4_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440">
  <defs>
    <linearGradient id="t4Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#FAF5FF"/>
    </linearGradient>
    <filter id="t4Shadow" x="-5%" y="-5%" width="115%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#7C3AED" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1000" height="440" rx="18" fill="url(#t4Bg)"/>
  <rect width="1000" height="440" rx="18" fill="none" stroke="#E9D5FF" stroke-width="2"/>
  <rect x="0" y="0" width="1000" height="6" fill="#7C3AED"/>

  <!-- Left: Conversational Chat Mockup -->
  <g transform="translate(40, 36)" filter="url(#t4Shadow)">
    <rect width="400" height="368" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect width="400" height="36" rx="14" fill="#F8FAFC"/>
    <circle cx="24" cy="18" r="5" fill="#EF4444"/>
    <circle cx="42" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="60" cy="18" r="5" fill="#10B981"/>
    <text x="80" y="22" font-family="'JetBrains Mono', monospace" font-size="11.5" fill="#64748B">chatbot.py --query</text>

    <!-- Chat Dialogue Bubbles -->
    <g transform="translate(20, 52)">
      <!-- Student Query -->
      <g transform="translate(80, 0)">
        <rect width="280" height="40" rx="12" fill="#7C3AED"/>
        <text x="14" y="25" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="600" fill="#FFFFFF">How many hours per week are required?</text>
      </g>

      <!-- Assistant Response -->
      <g transform="translate(0, 54)">
        <rect width="320" height="64" rx="12" fill="#F3E8FF" stroke="#D8B4FE"/>
        <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#6B21A8">🤖 DATHEON ASSISTANT (Match: 0.85 &gt; 0.40):</text>
        <text x="14" y="44" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11.5" fill="#3B0764">"Interns are expected to dedicate 10 to 15</text>
        <text x="14" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11.5" fill="#3B0764">hours weekly for module milestones."</text>
      </g>

      <!-- Student Query 2 (Fallback demonstration) -->
      <g transform="translate(100, 130)">
        <rect width="260" height="40" rx="12" fill="#7C3AED"/>
        <text x="14" y="25" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="600" fill="#FFFFFF">Can you fly me to Mars for training?</text>
      </g>

      <!-- Assistant Fallback Response -->
      <g transform="translate(0, 184)">
        <rect width="320" height="64" rx="12" fill="#FEF2F2" stroke="#FECACA"/>
        <text x="14" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#DC2626">🛡️ ZERO-HALLUCINATION FALLBACK (Score: 0.00):</text>
        <text x="14" y="44" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" fill="#7F1D1D">"I am specifically trained on Datheon FAQ topics.</text>
        <text x="14" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" fill="#7F1D1D">Could you please rephrase your internship inquiry?"</text>
      </g>
    </g>

    <!-- Schema Indicator Strip -->
    <g transform="translate(20, 310)">
      <rect width="360" height="40" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
      <text x="12" y="24" font-family="'JetBrains Mono', monospace" font-size="10.5" fill="#6B21A8">Schema: data/sample_faq.json (Normalized Token Bag)</text>
    </g>
  </g>

  <!-- Right: Architecture & Features -->
  <g transform="translate(470, 36)">
    <g>
      <rect width="90" height="26" rx="6" fill="#F3E8FF"/>
      <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#6B21A8">MODULE 04</text>
      <text x="102" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" font-weight="900" fill="#0F172A">Rule-Based FAQ Assistant</text>
    </g>

    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" fill="#475569">
      A deterministic conversational assistant grounded entirely in verified JSON knowledge bases, utilizing token scoring without hallucination.
    </text>

    <!-- Spec List -->
    <g transform="translate(0, 95)" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13">
      <g transform="translate(0, 0)">
        <rect width="24" height="24" rx="12" fill="#F3E8FF"/>
        <text x="7" y="16" font-weight="800" fill="#7C3AED">1</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Token Scoring Engine:</text>
        <text x="195" y="16" fill="#64748B">Normalized token overlap with 0.40 score threshold</text>
      </g>

      <g transform="translate(0, 40)">
        <rect width="24" height="24" rx="12" fill="#F3E8FF"/>
        <text x="7" y="16" font-weight="800" fill="#7C3AED">2</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Flexible Schema Adapter:</text>
        <text x="215" y="16" fill="#64748B">Loads canonical FAQ arrays and dictionary trees</text>
      </g>

      <g transform="translate(0, 80)">
        <rect width="24" height="24" rx="12" fill="#F3E8FF"/>
        <text x="7" y="16" font-weight="800" fill="#7C3AED">3</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Truthful Non-Fabrication:</text>
        <text x="215" y="16" fill="#64748B">Rejects low-confidence queries cleanly</text>
      </g>

      <g transform="translate(0, 120)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#15803D">✓</text>
        <text x="36" y="16" font-weight="700" fill="#15803D">14 Automated Unit Tests:</text>
        <text x="215" y="16" fill="#166534">100% Passing in 0.031s (unittest)</text>
      </g>
    </g>

    <!-- Terminal Command Snippet -->
    <g transform="translate(0, 275)">
      <rect width="490" height="85" rx="10" fill="#FFFFFF" stroke="#E9D5FF" stroke-width="1.5"/>
      <rect width="490" height="26" rx="10" fill="#FAF5FF"/>
      <text x="14" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#7C3AED">TERMINAL LAUNCH COMMAND</text>
      <text x="14" y="48" font-family="'JetBrains Mono', monospace" font-size="12" fill="#0F172A">$ python task4_chatbot/chatbot.py</text>
      <text x="14" y="70" font-family="'JetBrains Mono', monospace" font-size="11" fill="#64748B"># Or single query: python task4_chatbot/chatbot.py --query "Stipend info"</text>
    </g>
  </g>
</svg>
"""

# ==============================================================================
# 6. DASHBOARD LIGHT PREVIEW (1000 x 440)
# ==============================================================================
dashboard_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 440" width="1000" height="440">
  <defs>
    <linearGradient id="dashBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <filter id="dashShadow" x="-5%" y="-5%" width="115%" height="120%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.08"/>
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0F172A" flood-opacity="0.04"/>
    </filter>
  </defs>

  <rect width="1000" height="440" rx="18" fill="url(#dashBg)"/>
  <rect width="1000" height="440" rx="18" fill="none" stroke="#E2E8F0" stroke-width="2"/>
  <rect x="0" y="0" width="1000" height="6" fill="#3B82F6"/>

  <!-- Left: Browser Frame Mockup of index.html -->
  <g transform="translate(40, 36)" filter="url(#dashShadow)">
    <rect width="400" height="368" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5"/>
    <rect width="400" height="36" rx="14" fill="#F8FAFC"/>
    <circle cx="24" cy="18" r="5" fill="#EF4444"/>
    <circle cx="42" cy="18" r="5" fill="#F59E0B"/>
    <circle cx="60" cy="18" r="5" fill="#10B981"/>
    <!-- URL Bar -->
    <rect x="80" y="8" width="280" height="20" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
    <text x="92" y="22" font-family="'JetBrains Mono', monospace" font-size="10.5" fill="#1D4ED8">https://maheswari9080.github.io/...</text>

    <!-- Webpage Content Simulation -->
    <g transform="translate(20, 52)">
      <!-- Top banner strip -->
      <rect width="360" height="55" rx="8" fill="#F0F9FF" stroke="#BAE6FD"/>
      <text x="14" y="24" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="800" fill="#0369A1">Datheon Python Internship Portal</text>
      <text x="14" y="42" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="10.5" fill="#64748B">Client-side static developer documentation &amp; command hub</text>

      <!-- 4 App mini tiles -->
      <g transform="translate(0, 68)">
        <rect width="175" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#0284C7">01. Hangman Game</text>
        <text x="10" y="40" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#64748B">18 tests • CLI engine</text>
        <text x="10" y="55" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="600" fill="#10B981">● Live View</text>

        <rect x="185" width="175" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="195" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#059669">02. Portfolio Tracker</text>
        <text x="195" y="40" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#64748B">14 tests • S&amp;P 500</text>
        <text x="195" y="55" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="600" fill="#10B981">● Live View</text>
      </g>

      <g transform="translate(0, 142)">
        <rect width="175" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="10" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#D97706">03. File Organizer</text>
        <text x="10" y="40" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#64748B">12 tests • Dry-run safe</text>
        <text x="10" y="55" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="600" fill="#10B981">● Live View</text>

        <rect x="185" width="175" height="65" rx="8" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="195" y="22" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="700" fill="#7C3AED">04. FAQ Chatbot</text>
        <text x="195" y="40" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#64748B">14 tests • NLP token bag</text>
        <text x="195" y="55" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="9.5" font-weight="600" fill="#10B981">● Live View</text>
      </g>

      <!-- Bottom Status Pill -->
      <g transform="translate(0, 220)">
        <rect width="360" height="30" rx="6" fill="#F1F5F9"/>
        <text x="12" y="19" font-family="'JetBrains Mono', monospace" font-size="10.5" fill="#475569">Pure Client-Side • Zero Server Dependency</text>
      </g>
    </g>
  </g>

  <!-- Right: Architecture & Features -->
  <g transform="translate(470, 36)">
    <g>
      <rect width="90" height="26" rx="6" fill="#DBEAFE"/>
      <text x="12" y="17" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#1D4ED8">PORTAL</text>
      <text x="102" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="22" font-weight="900" fill="#0F172A">Universal Web Dashboard</text>
    </g>

    <text x="0" y="58" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" fill="#475569">
      A zero-server, client-side web portal (index.html) providing interactive terminal helpers, documentation navigation, and test metrics.
    </text>

    <!-- Spec List -->
    <g transform="translate(0, 95)" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13">
      <g transform="translate(0, 0)">
        <rect width="24" height="24" rx="12" fill="#DBEAFE"/>
        <text x="7" y="16" font-weight="800" fill="#2563EB">1</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">Zero Server Requirement:</text>
        <text x="215" y="16" fill="#64748B">Runs directly via file:/// or GitHub Pages</text>
      </g>

      <g transform="translate(0, 40)">
        <rect width="24" height="24" rx="12" fill="#DBEAFE"/>
        <text x="7" y="16" font-weight="800" fill="#2563EB">2</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">One-Click Clipboard Helpers:</text>
        <text x="235" y="16" fill="#64748B">Instantly copy execution &amp; test commands</text>
      </g>

      <g transform="translate(0, 80)">
        <rect width="24" height="24" rx="12" fill="#DBEAFE"/>
        <text x="7" y="16" font-weight="800" fill="#2563EB">3</text>
        <text x="36" y="16" font-weight="700" fill="#0F172A">WCAG AA Light Theme Tokens:</text>
        <text x="245" y="16" fill="#64748B">Accessible contrast, typography, &amp; clean layout</text>
      </g>

      <g transform="translate(0, 120)">
        <rect width="24" height="24" rx="12" fill="#DCFCE7"/>
        <text x="7" y="16" font-weight="800" fill="#15803D">✓</text>
        <text x="36" y="16" font-weight="700" fill="#15803D">Live GitHub Pages Deployment:</text>
        <text x="255" y="16" fill="#166534">maheswari9080.github.io</text>
      </g>
    </g>

    <!-- Terminal Command Snippet -->
    <g transform="translate(0, 275)">
      <rect width="490" height="85" rx="10" fill="#FFFFFF" stroke="#BFDBFE" stroke-width="1.5"/>
      <rect width="490" height="26" rx="10" fill="#EFF6FF"/>
      <text x="14" y="18" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#1D4ED8">BROWSER LAUNCH</text>
      <text x="14" y="48" font-family="'JetBrains Mono', monospace" font-size="12" fill="#0F172A">Start-Process "index.html"  # PowerShell</text>
      <text x="14" y="70" font-family="'JetBrains Mono', monospace" font-size="11" fill="#64748B"># Or open in Google Chrome / Microsoft Edge / Safari</text>
    </g>
  </g>
</svg>
"""

def main():
    assets = [
        ("linkedin_showcase", linkedin_svg, 1200, 675),
        ("task1_hangman_card", task1_svg, 1000, 440),
        ("task2_portfolio_card", task2_svg, 1000, 440),
        ("task3_organizer_card", task3_svg, 1000, 440),
        ("task4_chatbot_card", task4_svg, 1000, 440),
        ("dashboard_light_preview", dashboard_svg, 1000, 440),
    ]

    for name, svg_data, w, h in assets:
        svg_file = IMAGES_DIR / f"{name}.svg"
        png_file = IMAGES_DIR / f"{name}.png"
        
        svg_file.write_text(svg_data.strip(), encoding="utf-8")
        print(f"Wrote SVG: {svg_file.name}")
        
        render_svg_to_png(svg_file, png_file, w, h)

    # Also copy linkedin_showcase to root as linkedin_showcase.png, linkedin_showcase.svg, and image.png
    li_png = IMAGES_DIR / "linkedin_showcase.png"
    li_svg = IMAGES_DIR / "linkedin_showcase.svg"
    if li_png.exists():
        (BASE_DIR / "linkedin_showcase.png").write_bytes(li_png.read_bytes())
        (BASE_DIR / "image.png").write_bytes(li_png.read_bytes())
        (BASE_DIR / "linkedin_showcase.svg").write_bytes(li_svg.read_bytes())
        print("Exported root LinkedIn graphics: linkedin_showcase.png, image.png, and linkedin_showcase.svg")

if __name__ == "__main__":
    main()
