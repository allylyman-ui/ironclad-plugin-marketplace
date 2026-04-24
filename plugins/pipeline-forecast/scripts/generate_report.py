#!/usr/bin/env python3
"""
Pipeline Intelligence Report Generator
Generates Ironclad-branded HTML and PDF reports from deal assessments.

Designed as a linear, continuously scrolling document that renders cleanly
as both an HTML page and a paginated PDF. No dashboard grids — reads like
a professional one-pager per deal, flowing top to bottom.

Usage:
    python3 generate_report.py \
        --mode bootstrap \
        --date "4/17/26" \
        --assessments assessments.json \
        --brand-dir /path/to/ironclad-branding/assets \
        --output-dir /path/to/output

Input: assessments.json with structure documented in SKILL.md

Output:
    - pipeline-intelligence-{date}.html
    - pipeline-intelligence-{date}.pdf
"""

import argparse
import base64
import json
import os
from datetime import datetime
from pathlib import Path


def b64_file(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode()


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


def load_brand_assets(brand_dir):
    assets = {}
    logo_path = os.path.join(brand_dir, "logos", "ironclad-logo-full.svg")
    if os.path.exists(logo_path):
        assets["logo_svg"] = read_file(logo_path)

    font_map = {
        "moderat_regular": "Moderat-Regular.otf",
        "moderat_medium": "Moderat-Medium.otf",
        "moderat_mono": "Moderat-Mono-Medium.otf",
        "sangbleu_italic": "SangBleuKingdom-RegularItalic.otf",
    }
    assets["fonts"] = {}
    for key, fname in font_map.items():
        p = os.path.join(brand_dir, "fonts", fname)
        if os.path.exists(p):
            assets["fonts"][key] = b64_file(p)
    return assets


def cur(amount):
    if amount is None:
        return "—"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    return f"${amount:,.0f}"


def esc(text):
    if text is None:
        return ""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def nl2br(text):
    if not text:
        return ""
    return esc(text).replace("\n", "<br>")


def link_or_text(text, url=None):
    if url:
        return f'<a href="{esc(url)}" class="source-link">{esc(text)}</a>'
    return esc(text)


def font_faces(assets):
    css = ""
    pairs = [
        ("moderat_regular", "Moderat", "400", "normal"),
        ("moderat_medium", "Moderat", "500", "normal"),
        ("moderat_mono", "Moderat Mono", "500", "normal"),
        ("sangbleu_italic", "SangBleu Kingdom", "400", "italic"),
    ]
    for key, family, weight, style in pairs:
        if key in assets.get("fonts", {}):
            css += f"@font-face {{ font-family: '{family}'; src: url('data:font/otf;base64,{assets['fonts'][key]}') format('opentype'); font-weight: {weight}; font-style: {style}; }}\n"
    return css


def generate_html(data, assets):
    mode = data.get("mode", "weekly")
    date = data.get("date", datetime.now().strftime("%-m/%-d/%y"))
    summary = data.get("summary", {})
    deals = data.get("deals", [])

    mode_label = "Bootstrap Baseline" if mode == "bootstrap" else "Weekly Update"
    logo_svg = assets.get("logo_svg", "")
    ff = font_faces(assets)

    # Sort: mismatches first, then by ARR desc
    deals.sort(key=lambda d: (not d.get("arr_mismatch", False), -(d.get("current_arr") or 0)))

    # === SUMMARY SECTION ===
    arr_mismatches = summary.get("arr_mismatches", [])
    close_mismatches = summary.get("close_date_mismatches", [])
    dead_outs = summary.get("dead_out_candidates", [])

    by_cat = summary.get("by_category", {})
    cat_line = " · ".join(
        f"{name}: {d.get('count',0)} deals / {cur(d.get('arr',0))}"
        for name, d in by_cat.items()
    )

    by_stage = summary.get("by_stage", {})
    stage_line = " · ".join(
        f"{name}: {d.get('count',0)} ({cur(d.get('arr',0))})"
        for name, d in sorted(by_stage.items())
    )

    # Mismatch table rows
    mismatch_rows = ""
    if arr_mismatches:
        mismatch_rows += '<div class="subsection"><p class="eyebrow">ARR MISMATCHES</p><table>'
        mismatch_rows += "<tr><th>Account</th><th>Salesforce</th><th>Actual</th><th>Source</th></tr>"
        for m in arr_mismatches:
            src = link_or_text(m.get("source", ""), m.get("source_url"))
            mismatch_rows += f'<tr><td>{esc(m.get("account",""))}</td><td class="alert-text">{cur(m.get("sf_arr"))}</td><td>{cur(m.get("actual_arr"))}</td><td>{src}</td></tr>'
        mismatch_rows += "</table></div>"

    if close_mismatches:
        mismatch_rows += '<div class="subsection"><p class="eyebrow">CLOSE DATE MISMATCHES</p><table>'
        mismatch_rows += "<tr><th>Account</th><th>Salesforce</th><th>Discussed</th><th>Source</th></tr>"
        for m in close_mismatches:
            src = link_or_text(m.get("source", ""), m.get("source_url"))
            mismatch_rows += f'<tr><td>{esc(m.get("account",""))}</td><td class="alert-text">{esc(m.get("sf_date",""))}</td><td>{esc(m.get("discussed_date",""))}</td><td>{src}</td></tr>'
        mismatch_rows += "</table></div>"

    if dead_outs:
        mismatch_rows += '<div class="subsection"><p class="eyebrow">DEAD OUT CANDIDATES</p><table>'
        mismatch_rows += "<tr><th>Account</th><th>Reason</th></tr>"
        for d in dead_outs:
            mismatch_rows += f'<tr><td>{esc(d.get("account",""))}</td><td>{esc(d.get("reason",""))}</td></tr>'
        mismatch_rows += "</table></div>"

    # === DEAL SECTIONS ===
    deal_sections = ""
    for i, deal in enumerate(deals):
        # Category badge
        cat = deal.get("recommended_category") or deal.get("forecast_category", "Pipeline")
        cat_cls = {"Commit": "commit", "Best Case": "best-case", "Pipeline": "pipeline"}.get(cat, "pipeline")

        # Mismatch flags
        flags = ""
        if deal.get("arr_mismatch"):
            flags += '<span class="flag flag-alert">ARR MISMATCH</span> '
        if deal.get("close_date_mismatch"):
            flags += '<span class="flag flag-alert">CLOSE DATE MISMATCH</span> '

        # Metrics line
        arr_display = cur(deal.get("current_arr"))
        if deal.get("arr_mismatch") and deal.get("recommended_arr"):
            arr_display += f' <span class="alert-text">→ {cur(deal["recommended_arr"])}</span>'

        close_display = esc(deal.get("close_date", ""))
        if deal.get("close_date_mismatch") and deal.get("recommended_close_date"):
            close_display += f' <span class="alert-text">→ {esc(deal["recommended_close_date"])}</span>'

        # Confidence score
        conf_score = deal.get("confidence_score")
        conf_html = ""
        if conf_score is not None:
            conf_cls = "conf-high" if conf_score >= 8 else ("conf-mid" if conf_score >= 5 else "conf-low")
            conf_html = f'<span class="confidence {conf_cls}">{conf_score}/10</span>'
        conf_factors = deal.get("confidence_factors", "")

        # Key insight
        insight_html = ""
        insight = deal.get("insight", "")
        if insight:
            insight_html = f'<div class="insight-box"><span class="insight-icon">&#9670;</span> <span class="body-text">{nl2br(insight)}</span></div>'

        # Competitors
        competitors_html = ""
        competitors = deal.get("competitors", "")
        if competitors:
            if isinstance(competitors, list):
                comp_tags = " ".join(f'<span class="comp-tag">{esc(c)}</span>' for c in competitors)
            else:
                comp_tags = f'<span class="comp-tag">{esc(competitors)}</span>'
            competitors_html = f'<div class="competitors-row"><span class="metric-label">Competing with:</span> {comp_tags}</div>'

        # Milestones (bootstrap only)
        milestones_html = ""
        if deal.get("key_milestones") and mode == "bootstrap":
            ms_items = "".join(f"<li>{esc(ms)}</li>" for ms in deal["key_milestones"])
            milestones_html = f'<div class="subsection"><p class="eyebrow">KEY MILESTONES</p><ul class="milestones">{ms_items}</ul></div>'

        # Pricing history (bootstrap only)
        pricing_html = ""
        if deal.get("pricing_history") and mode == "bootstrap":
            pricing_html = f'<div class="subsection"><p class="eyebrow">PRICING HISTORY</p><p class="body-text">{nl2br(deal["pricing_history"])}</p></div>'

        # Evidence with source links
        def evidence_block(label, text_key, sources_key):
            text = deal.get(text_key, "No data")
            sources = deal.get(sources_key, [])
            links_html = ""
            if sources:
                link_items = " ".join(link_or_text(s.get("title", "Link"), s.get("url")) for s in sources)
                links_html = f'<div class="source-links">{link_items}</div>'
            return f'<div class="evidence-row"><span class="evidence-label">{label}:</span> <span class="body-text">{nl2br(text)}</span>{links_html}</div>'

        evidence_html = (
            evidence_block("Gong", "evidence_gong", "sources_gong")
            + evidence_block("Email", "evidence_email", "sources_email")
            + evidence_block("Calendar", "evidence_calendar", "sources_calendar")
            + evidence_block("Drive", "evidence_drive", "sources_drive")
        )

        # SF field updates
        sf_html = ""
        for field_name, field_key in [("Next Steps", "next_steps"), ("Sales Notes", "sales_notes"), ("Red Flags", "red_flags")]:
            val = deal.get(field_key, "")
            if val:
                sf_html += f'<div class="sf-field"><p class="sf-field-label">{field_name}</p><pre class="sf-field-value">{esc(val)}</pre></div>'

        # Notion link
        notion_url = deal.get("notion_url", "")
        notion_link = f' <a href="{esc(notion_url)}" class="notion-link">View in Notion</a>' if notion_url else ""

        deal_sections += f"""
    <div class="deal-section">
        <div class="deal-header-row">
            <div>
                <h2 class="deal-name">{esc(deal.get("account", ""))}{notion_link}</h2>
                <p class="deal-opp">{esc(deal.get("opportunity", ""))}</p>
            </div>
            <span class="cat-badge cat-{cat_cls}">{esc(cat)}</span>
        </div>
        {f'<div class="flags-row">{flags}</div>' if flags else ''}

        <div class="metrics-row">
            <span><span class="metric-label">Stage:</span> {esc(deal.get("current_stage", ""))}</span>
            <span><span class="metric-label">ARR:</span> {arr_display}</span>
            <span><span class="metric-label">Close:</span> {close_display}</span>
            <span><span class="metric-label">Age:</span> {deal.get("deal_age", "—")} days</span>
            {f'<span><span class="metric-label">Confidence:</span> {conf_html}</span>' if conf_html else ''}
        </div>
        {f'<p class="conf-factors">{esc(conf_factors)}</p>' if conf_factors else ''}

        {insight_html}
        {competitors_html}
        {milestones_html}
        {pricing_html}

        <div class="subsection">
            <p class="eyebrow">EVIDENCE</p>
            {evidence_html}
        </div>

        <details class="sf-details" open>
            <summary class="eyebrow sf-toggle">SALESFORCE FIELD UPDATES</summary>
            {sf_html}
        </details>

        <div class="divider"></div>
    </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Pipeline Intelligence — {esc(mode_label)} — {esc(date)}</title>
<style>
{ff}
:root {{
  --cream: #F2F1EE;
  --navy: #1C212B;
  --green: #308970;
  --logo-green: #00CA88;
  --purple: #B27BE1;
  --dark-gray: #5F6674;
  --light-gray: #ADB9C4;
  --orange: #F1643C;
  --blue: #6A85CF;
  --sans: 'Moderat', 'Inter', system-ui, sans-serif;
  --mono: 'Moderat Mono', 'SF Mono', monospace;
  --serif: 'SangBleu Kingdom', 'Playfair Display', serif;
}}
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: var(--sans);
  font-weight: 400;
  font-size: 13px;
  color: var(--navy);
  background: white;
  line-height: 1.55;
  max-width: 820px;
  margin: 0 auto;
  padding: 0;
  -webkit-font-smoothing: antialiased;
}}

/* --- HEADER --- */
.header {{
  background: var(--navy);
  color: var(--cream);
  padding: 32px 40px 28px;
}}
.header-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}}
.logo svg {{ width: 120px; height: auto; }}
.logo svg path[fill="#1C212B"] {{ fill: var(--cream); }}
.header-date {{
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--light-gray);
}}
.header h1 {{
  font-weight: 500;
  font-size: 26px;
  line-height: 1.2;
  margin-bottom: 4px;
}}
.header h1 em {{
  font-family: var(--serif);
  font-style: italic;
  font-weight: 400;
}}
.header-sub {{
  font-size: 13px;
  color: var(--light-gray);
}}

/* --- SUMMARY --- */
.summary {{
  padding: 24px 40px;
  border-bottom: 1px solid #e8e7e4;
}}
.summary-stats {{
  display: flex;
  gap: 32px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}}
.stat {{
  display: flex;
  flex-direction: column;
}}
.stat-num {{
  font-weight: 500;
  font-size: 22px;
  color: var(--navy);
}}
.stat-label {{
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--green);
}}
.summary-line {{
  font-size: 12px;
  color: var(--dark-gray);
  margin-bottom: 6px;
}}
.ml-row {{
  background: var(--navy);
  color: var(--cream);
  border-radius: 6px;
  padding: 14px 20px;
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.ml-label {{
  font-family: var(--mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--logo-green);
}}
.ml-value {{
  font-weight: 500;
  font-size: 24px;
}}

/* --- ALERTS --- */
.alerts {{
  padding: 20px 40px;
  border-bottom: 1px solid #e8e7e4;
}}
.alerts table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin-top: 6px;
}}
.alerts th {{
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--dark-gray);
  text-align: left;
  padding: 5px 8px;
  border-bottom: 1px solid #e8e7e4;
}}
.alerts td {{
  padding: 6px 8px;
  border-bottom: 1px solid #f2f1ee;
}}
.alert-text {{ color: var(--orange); font-weight: 500; }}

/* --- EYEBROW / LABELS --- */
.eyebrow {{
  font-family: var(--mono);
  font-weight: 500;
  font-size: 9px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--green);
  margin-bottom: 6px;
}}
.body-text {{
  font-size: 12px;
  color: var(--dark-gray);
  line-height: 1.55;
}}

/* --- DEAL SECTIONS --- */
.deals {{
  padding: 24px 40px;
}}
.deal-section {{
  margin-bottom: 8px;
}}
.deal-header-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 4px;
}}
.deal-name {{
  font-weight: 500;
  font-size: 18px;
  color: var(--navy);
  line-height: 1.25;
}}
.deal-opp {{
  font-size: 11px;
  color: var(--dark-gray);
  margin-top: 1px;
}}
.cat-badge {{
  font-family: var(--mono);
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 10px;
  white-space: nowrap;
  flex-shrink: 0;
}}
.cat-commit {{ background: rgba(48,137,112,0.12); color: var(--green); }}
.cat-best-case {{ background: rgba(178,123,225,0.12); color: #7B5BA6; }}
.cat-pipeline {{ background: rgba(106,133,207,0.12); color: var(--blue); }}

/* --- CONFIDENCE SCORE --- */
.confidence {{
  font-family: var(--mono);
  font-weight: 500;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
}}
.conf-high {{ color: var(--green); background: rgba(48,137,112,0.1); }}
.conf-mid {{ color: #B08A00; background: rgba(176,138,0,0.08); }}
.conf-low {{ color: var(--orange); background: rgba(241,100,60,0.1); }}
.conf-factors {{
  font-size: 10px;
  color: var(--dark-gray);
  font-style: italic;
  margin-top: -8px;
  margin-bottom: 10px;
}}

/* --- INSIGHT BOX --- */
.insight-box {{
  background: rgba(48,137,112,0.06);
  border-left: 3px solid var(--green);
  border-radius: 0 4px 4px 0;
  padding: 8px 12px;
  margin-bottom: 12px;
  font-size: 12px;
  color: var(--navy);
  line-height: 1.5;
}}
.insight-icon {{
  color: var(--green);
  font-size: 8px;
  margin-right: 4px;
}}

/* --- COMPETITORS --- */
.competitors-row {{
  margin-bottom: 12px;
  font-size: 12px;
}}
.comp-tag {{
  font-family: var(--mono);
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--orange);
  background: rgba(241,100,60,0.08);
  padding: 2px 8px;
  border-radius: 8px;
  margin-left: 4px;
}}

.flags-row {{ margin-bottom: 8px; }}
.flag {{
  font-family: var(--mono);
  font-size: 8px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 8px;
  margin-right: 4px;
}}
.flag-alert {{ background: rgba(241,100,60,0.1); color: var(--orange); }}

.metrics-row {{
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--navy);
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f2f1ee;
}}
.metric-label {{
  font-weight: 500;
  color: var(--dark-gray);
}}

.subsection {{
  margin-bottom: 12px;
}}
.milestones {{
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 4px 16px;
}}
.milestones li {{
  font-size: 11px;
  color: var(--dark-gray);
  position: relative;
  padding-left: 12px;
}}
.milestones li::before {{
  content: '';
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--green);
  position: absolute;
  left: 0;
  top: 5px;
}}

.evidence-row {{
  margin-bottom: 6px;
  font-size: 12px;
}}
.evidence-label {{
  font-weight: 500;
  color: var(--navy);
}}
.source-links {{
  margin-top: 2px;
  margin-left: 0;
}}
.source-link {{
  font-family: var(--mono);
  font-size: 9px;
  color: var(--blue);
  text-decoration: none;
  margin-right: 10px;
}}
.source-link:hover {{ text-decoration: underline; }}

.notion-link {{
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.04em;
  color: var(--blue);
  text-decoration: none;
  margin-left: 8px;
  vertical-align: middle;
  padding: 1px 6px;
  border: 1px solid rgba(106,133,207,0.3);
  border-radius: 4px;
}}
.notion-link:hover {{
  background: rgba(106,133,207,0.08);
  text-decoration: none;
}}

/* --- SF FIELDS --- */
.sf-details {{ margin-top: 10px; margin-bottom: 8px; }}
.sf-toggle {{
  cursor: pointer;
  list-style: none;
  padding: 4px 0;
}}
.sf-toggle::-webkit-details-marker {{ display: none; }}
.sf-field {{
  margin-top: 8px;
}}
.sf-field-label {{
  font-family: var(--mono);
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--dark-gray);
  margin-bottom: 3px;
}}
.sf-field-value {{
  font-family: var(--sans);
  font-size: 11px;
  color: var(--dark-gray);
  line-height: 1.55;
  white-space: pre-wrap;
  background: var(--cream);
  border-radius: 4px;
  padding: 10px 12px;
  border: none;
}}

.divider {{
  height: 1px;
  background: var(--green);
  opacity: 0.25;
  margin: 24px 0;
}}

/* --- FOOTER --- */
.footer {{
  padding: 20px 40px;
  text-align: center;
  font-size: 10px;
  color: var(--light-gray);
  border-top: 1px solid #e8e7e4;
}}

/* --- PRINT / PDF --- */
@page {{
  size: letter;
  margin: 0.4in 0.5in;
}}
@media print {{
  body {{ max-width: none; }}
  .deal-section {{ page-break-inside: avoid; }}
  .sf-details[open] > .sf-field {{ display: block; }}
}}
</style>
</head>
<body>

<div class="header">
    <div class="header-top">
        <div class="logo">{logo_svg}</div>
        <div class="header-date">{esc(date)}</div>
    </div>
    <h1>Pipeline <em>Intelligence</em></h1>
    <p class="header-sub">{esc(mode_label)} — Ally Lyman</p>
</div>

<div class="summary">
    <div class="summary-stats">
        <div class="stat"><span class="stat-num">{summary.get("total_deals", len(deals))}</span><span class="stat-label">DEALS</span></div>
        <div class="stat"><span class="stat-num">{cur(summary.get("total_arr", 0))}</span><span class="stat-label">TOTAL PIPELINE</span></div>
        <div class="stat"><span class="stat-num {'alert-text' if arr_mismatches else ''}">{len(arr_mismatches)}</span><span class="stat-label">ARR MISMATCHES</span></div>
        <div class="stat"><span class="stat-num {'alert-text' if dead_outs else ''}">{len(dead_outs)}</span><span class="stat-label">DEAD OUT</span></div>
    </div>
    <p class="summary-line"><span class="metric-label">By category:</span> {esc(cat_line)}</p>
    <p class="summary-line"><span class="metric-label">By stage:</span> {esc(stage_line)}</p>
    <div class="ml-row">
        <div><span class="ml-label">RECOMMENDED ML CALL</span></div>
        <span class="ml-value">{cur(summary.get("ml_call", 0))}</span>
    </div>
</div>

{'<div class="alerts">' + mismatch_rows + '</div>' if mismatch_rows else ''}

<div class="deals">
    <p class="eyebrow">DEAL ASSESSMENTS — {len(deals)} DEALS</p>
    {deal_sections}
</div>

<div class="footer">Pipeline Intelligence by Ironclad — {esc(date)} — Confidential</div>

</body>
</html>"""
    return html


def html_to_pdf(html_path, pdf_path):
    try:
        from weasyprint import HTML
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return True
    except ImportError:
        print("WeasyPrint not installed. pip install weasyprint --break-system-packages")
        return False
    except Exception as e:
        print(f"PDF generation failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate Ironclad-branded pipeline report")
    parser.add_argument("--mode", choices=["bootstrap", "weekly"], default="weekly")
    parser.add_argument("--date", default=datetime.now().strftime("%-m/%-d/%y"))
    parser.add_argument("--assessments", required=True)
    parser.add_argument("--brand-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    with open(args.assessments, "r") as f:
        data = json.load(f)
    data["mode"] = args.mode
    data["date"] = args.date

    assets = load_brand_assets(args.brand_dir)
    html = generate_html(data, assets)

    slug = args.date.replace("/", "-")
    html_path = Path(args.output_dir) / f"pipeline-intelligence-{slug}.html"
    pdf_path = Path(args.output_dir) / f"pipeline-intelligence-{slug}.pdf"
    os.makedirs(args.output_dir, exist_ok=True)

    with open(html_path, "w") as f:
        f.write(html)
    print(f"HTML: {html_path}")

    if html_to_pdf(html_path, pdf_path):
        print(f"PDF: {pdf_path}")


if __name__ == "__main__":
    main()
