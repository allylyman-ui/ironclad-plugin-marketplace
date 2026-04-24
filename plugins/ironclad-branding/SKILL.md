---
name: ironclad-branding
description: >
  Ironclad brand guidelines skill for creating on-brand assets — HTML pages, presentations,
  one-pagers, social posts, landing pages, event banners, email templates, and any visual
  content for Ironclad. Ensures correct colors, typography, tone, and layout patterns from
  the official Ironclad Brand Guide (March 2026). Use this skill whenever creating any
  Ironclad-branded content, including: HTML artifacts, React components, slide decks,
  one-pagers, social media graphics, email templates, landing pages, event invitations,
  infographics, internal documents, or any customer-facing material that should look and
  feel like Ironclad. Also use when the user asks to "make it look like Ironclad," "use
  Ironclad branding," "brand this," or references Ironclad visual identity. Trigger
  liberally — if the output will represent Ironclad visually, this skill applies.
---

# Ironclad Branding Skill

This skill contains Ironclad's official brand guidelines so that every asset you create looks and feels unmistakably Ironclad. The brand identity is modern, confident, and rooted in trust — Ironclad is an AI contracting company that accelerates business with every contract.

Before creating any branded asset, read `references/brand-spec.md` for the full color palette, typography details, and layout patterns. What follows here is the high-level guidance you need to internalize.

## Logo — Use the Real Thing

This skill bundles the actual Ironclad logo files. **Never try to recreate the logo with text or CSS** — always embed the real logo from the `assets/` directory.

Available Ironclad logo files in `assets/logos/`:
- `ironclad-logo-full.svg` — The full-color SVG logo (icon + wordmark). This is the best option for HTML — it's crisp at any size and lightweight. The SVG contains the green (#00CA88) icon and navy (#1C212B) wordmark.
- `ironclad-logo-navy.png` — Full-color PNG for use on cream/light backgrounds (green icon + navy wordmark)
- `ironclad-logo-cream.png` — Full-color PNG for use on navy/dark backgrounds (green icon + cream wordmark)
- `ironclad-logo-all-navy.png` — Single-color navy PNG (for non-standard backgrounds)
- `ironclad-logo-all-cream.png` — Single-color cream/white PNG (for non-standard backgrounds)

Available Jurist (Ironclad's AI agent product) logo files in `assets/logos/`:
- `jurist-logo.png` — Standard Jurist wordmark logo (1620×580, transparent background)
- `jurist-logo-pill.png` — Jurist pill-shaped lockup (1620×580, transparent background) — use when you want the bordered/contained treatment

Use the Jurist logo when the asset is specifically about Jurist (the AI agent), product announcements that feature Jurist, or co-branded moments where Jurist is the headline product. For general Ironclad assets, use the Ironclad logo.

**How to use the logo in HTML assets:**

For HTML files, read the SVG file and embed it inline. This is the preferred approach because it produces a self-contained HTML file with a crisp, scalable logo:

```python
# Read the SVG file content
with open('assets/logos/ironclad-logo-full.svg', 'r') as f:
    svg_content = f.read()
# Then embed directly in HTML: <div class="logo">{svg_content}</div>
```

Alternatively, if you need a PNG (e.g., for email templates or the Jurist logos), read the PNG file, base64-encode it, and embed as a data URI:

```python
import base64
with open('assets/logos/ironclad-logo-navy.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()
# Then use: <img src="data:image/png;base64,{logo_b64}" alt="Ironclad" />
```

**Which logo to use where:**
- On cream (#F2F1EE) backgrounds → `ironclad-logo-navy.png` or the SVG (default)
- On navy (#1C212B) backgrounds → `ironclad-logo-cream.png`
- On green, purple, or other colored backgrounds → `ironclad-logo-all-cream.png` (white version)
- In SVG format (preferred for HTML) → `ironclad-logo-full.svg` works on cream backgrounds; for dark backgrounds, you can apply a CSS filter or use a PNG instead
- For Jurist assets → `jurist-logo.png` (standard) or `jurist-logo-pill.png` (pill lockup)

### NEVER stretch the logo — aspect ratio is sacred

Logos must always preserve their native aspect ratio. A stretched logo looks broken and cheap, and it will get noticed. To guarantee the logo never distorts, follow these rules in every asset you produce:

**In HTML/CSS — the safe pattern:**

1. **Set only one dimension.** Give the logo a `width` (or `max-width`) and let `height` default to `auto`. Never hard-code both `width` and `height` on the same `<img>` — that's what causes stretching.
   ```html
   <img src="..." alt="Ironclad" style="width: 140px; height: auto; display: block;" />
   ```
2. **If the logo is inside a fixed-size container** (a header, a pill, a card), constrain via `max-width`/`max-height` and use `object-fit: contain` so the image is letterboxed rather than squashed:
   ```css
   .logo {
     max-width: 160px;
     max-height: 40px;
     width: auto;
     height: auto;
     object-fit: contain;  /* preserves aspect ratio inside the box */
     display: block;
   }
   ```
3. **For background-image logos**, always use `background-size: contain` (never `100% 100%` or `cover`), plus `background-repeat: no-repeat` and `background-position: center`.
4. **For inline SVG**, keep the `viewBox` attribute intact and set only one of `width`/`height` in CSS. Do not override `preserveAspectRatio`.
5. **In PowerPoint (python-pptx)**, when adding a picture, pass only `width` OR only `height` to `add_picture()` — python-pptx preserves aspect ratio when only one dimension is given. Passing both will stretch the image:
   ```python
   from pptx.util import Inches
   slide.shapes.add_picture('assets/logos/jurist-logo.png', Inches(0.5), Inches(0.5), width=Inches(1.8))  # height auto-scales
   ```

**Reference dimensions (use these to compute safe sizing):**
- Ironclad wordmark SVG: aspect is roughly horizontal (icon + wordmark); default web width 120–160px, height auto.
- Jurist PNGs (`jurist-logo.png`, `jurist-logo-pill.png`): native 1620×580, aspect ratio ≈ 2.79:1. At 160px width, the height is ≈57px. At 200px width, the height is ≈72px. Never set a height that doesn't match this ratio.

Size the logo so the wordmark is clearly legible. A good default width is 120–160px for web layouts. Maintain at least one "bracket width" of clear space around the logo. Never apply `transform: scale()` with non-uniform x/y values, `object-fit: fill`, or `background-size: 100% 100%` — all of those distort.

## Brand Personality

Ironclad's brand sits at the intersection of **legal trust** and **tech innovation**. The visual language communicates:
- Confidence without arrogance
- Sophistication without stuffiness
- Innovation without gimmicks

The company purpose — "Accelerate business with every contract" — should infuse every asset. The tone is direct, smart, and human. Core values are intent, empathy, drive, and integrity.

## Color System

Ironclad's palette is distinctive and intentional. Green is the core brand color — it signals trust, growth, and the legal roots of the company. The palette creates hierarchy through careful color relationships.

**Core colors** (use these most often):
- **Cream** `#F2F1EE` — Primary light background. Warm, not stark white.
- **Navy** `#1C212B` — Primary dark background and text color on light. Deep, not pure black.
- **Logo Green** `#00CA88` — Reserved for the logo icon mark only. Do not use as a general accent.

**Primary accents** (the distinctive Ironclad feel):
- **Green** `#308970` — The main brand accent. Use for eyebrow text, emphasis, CTAs on light backgrounds.
- **Purple** `#B27BE1` — Tags, badges, category labels. The "pop" color.
- **Sand** `#DDC2A4` — Warm neutral accent for supporting graphics and backgrounds.

**Grays:**
- **Dark Gray** `#5F6674` — Secondary text, subtle UI elements.
- **Light Gray** `#ADB9C4` — Borders, disabled states, secondary on dark.

**Secondary accents** (use sparingly, for data viz, charts, multi-item lists):
- **Orange** `#F1643C`, **Pink** `#F5B0D2`, **Blue** `#6A85CF`

### Color balance rules

The most important thing about Ironclad's color usage is restraint. A typical asset uses 2-4 colors, heavily weighted toward cream/navy with green and purple as accents. Think of it like a well-composed photograph — cream and navy set the scene, green draws the eye to what matters, and purple adds a distinctive accent.

- **Light theme**: Cream background, Navy text, Green for emphasis/CTAs, Purple for tags
- **Dark theme**: Navy background, Cream text, Logo Green for the icon, Green for headings, Purple for tags
- Never put the full-color logo on a solid color background other than cream or navy
- On non-cream/navy backgrounds, use a single-color (white or black) logo version

## Typography

Ironclad uses two typeface families that create a distinctive pairing. The rules below are the favored usage — follow them by default on every asset:

**Moderat** — The workhorse sans-serif:
- **Moderat Medium** — favored for titles and headings. Default for any title sentence.
- **Moderat Regular** — favored for body copy. Default for any paragraph, caption, or supporting text.
- **Moderat Mono Medium** — used in ALL CAPS for tags, categories, code, and legends on infographics. Add roughly +10% letter spacing for the proper rhythm. This is not decorative — it's the dedicated typographic slot for categorical or metadata text.
- `Moderat Medium-Italic` / `Moderat Regular-Italic` — italic variants of Moderat, used for standard italic emphasis inside body or headings (not the signature accent — that's SangBleu below).

**SangBleu Kingdom Regular Italic** — The accent serif:
- Used **sparingly** — only to call attention to a specific part of a title sentence. Not for body copy, not for tags, not as a standalone heading font.
- Creates the signature Ironclad look: a clean Moderat Medium sentence with one key phrase set in elegant italic serif.
- Example: "The **last** CLM you'll *ever need*" where "ever need" is in SangBleu Kingdom Regular Italic.
- When mixing with Moderat in a headline, decrease SangBleu's size slightly so the x-heights match.
- Rule of thumb: at most one SangBleu italic phrase per headline, and never more than one headline-with-SangBleu per hero/slide. Overuse kills the effect.

**Quick slot map — what font goes where:**

| Slot | Font | Notes |
| --- | --- | --- |
| Title / headline | Moderat Medium | Default for H1/H2 title sentences |
| Accent phrase inside a title | SangBleu Kingdom Regular Italic | Sparingly — one phrase max |
| Body copy, paragraphs, captions | Moderat Regular | Default workhorse |
| Tags, categories, eyebrows | Moderat Mono Medium, ALL CAPS | +10% letter spacing |
| Code, inline code, infographic legends | Moderat Mono Medium, ALL CAPS | Same treatment as tags |

### Using the Actual Ironclad Fonts

This skill bundles the real Ironclad font files in `assets/fonts/`. For HTML assets, embed these fonts using base64-encoded `@font-face` declarations so the output is fully self-contained with the correct typography.

Available font files:
- `Moderat-Regular.otf` — Body text
- `Moderat-Medium.otf` — Headings (H1, H2)
- `Moderat-Regular-Italic.otf` — Body italic
- `Moderat-Medium-Italic.otf` — Heading italic
- `Moderat-Mono-Medium.otf` — Tags, eyebrows, categories
- `SangBleuKingdom-Regular.otf` — Accent serif (regular)
- `SangBleuKingdom-RegularItalic.otf` — Accent serif italic (the signature look)

**How to embed fonts in HTML:**

Read each font file, base64-encode it, and embed via `@font-face` in your CSS. This is the correct approach — it produces a self-contained HTML file with the real Ironclad typography:

```python
import base64

def font_face(family, filepath, weight='normal', style='normal'):
    with open(filepath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"""@font-face {{
  font-family: '{family}';
  src: url('data:font/otf;base64,{b64}') format('opentype');
  font-weight: {weight};
  font-style: {style};
}}"""

# Generate @font-face rules for all fonts
fonts_css = "\n".join([
    font_face('Moderat', 'assets/fonts/Moderat-Regular.otf', '400', 'normal'),
    font_face('Moderat', 'assets/fonts/Moderat-Medium.otf', '500', 'normal'),
    font_face('Moderat', 'assets/fonts/Moderat-Regular-Italic.otf', '400', 'italic'),
    font_face('Moderat', 'assets/fonts/Moderat-Medium-Italic.otf', '500', 'italic'),
    font_face('Moderat Mono', 'assets/fonts/Moderat-Mono-Medium.otf', '500', 'normal'),
    font_face('SangBleu Kingdom', 'assets/fonts/SangBleuKingdom-Regular.otf', '400', 'normal'),
    font_face('SangBleu Kingdom', 'assets/fonts/SangBleuKingdom-RegularItalic.otf', '400', 'italic'),
])
```

Then include `fonts_css` inside a `<style>` block in your HTML. This ensures every asset uses the real Ironclad fonts.

**Fallback approach:** If for some reason you can't embed fonts (file size constraints, etc.), fall back to Google Fonts as a reasonable substitute:
```
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Playfair+Display:ital@1&display=swap');
```
With fallback families: `Inter` for Moderat, `'SF Mono', monospace` for Moderat Mono, and `'Playfair Display', serif` with italic for SangBleu Kingdom.

### Type hierarchy

All titles (H1–H4) use **Moderat Medium**. Body uses **Moderat Regular**. Eyebrows use **Moderat Mono Medium in ALL CAPS**.

**On light (cream) backgrounds:**
- Eyebrow: Moderat Mono Medium, ALL CAPS, green `#308970`, +10% letter-spacing
- H1: Moderat Medium, navy `#1C212B`, ~36pt equivalent
- H2: Moderat Medium, dark purple `#7B5BA6` (darker shade for readability), ~28pt
- H3: Moderat Medium, navy, ~24pt
- H4: Moderat Medium, dark gray `#5F6674`, ~22pt
- Body: Moderat Regular, dark gray `#5F6674`, ~16–18pt
- Links: Moderat Regular, blue `#6A85CF`, underlined

**On dark (navy) backgrounds:**
- Eyebrow: Moderat Mono Medium, ALL CAPS, logo green `#00CA88`, +10% letter-spacing
- H1: Moderat Medium, cream `#F2F1EE`, ~36pt
- H2: Moderat Medium, purple `#B27BE1`, ~28pt
- H3: Moderat Medium, cream, ~24pt
- H4: Moderat Medium, light gray `#ADB9C4`, ~22pt
- Body: Moderat Regular, light gray `#ADB9C4`, ~16–18pt
- Links: Moderat Regular, blue `#6A85CF`

## Icons and Visual Elements — No Emojis

Ironclad has its own custom icon system — bold, thick-stroke line icons in navy/charcoal color. The brand never uses emoji characters (no checkmarks, no rocket ships, no sparkles, no pointing fingers). Emojis undermine the premium, professional feel of the brand.

### Bundled Ironclad Icons

This skill includes 22 official Ironclad icons in `assets/icons/`. These are ~600x600px PNGs with transparent backgrounds, featuring thick navy strokes in a clean line-art style. Use them in HTML by base64-encoding and embedding as `<img>` tags.

Available icons and when to use them:
- `shield-check.png` — Security, compliance, trust, protection
- `gavel.png` — Legal, law, contracts, compliance
- `pen-signature.png` — E-signature, signing, authoring
- `clipboard.png` — Documents, contracts, agreements
- `checklist.png` / `checklist-check.png` — Tasks, requirements, approvals
- `clock.png` — Time savings, speed, deadlines
- `calendar.png` — Scheduling, dates, events
- `bar-chart.png` — Analytics, reporting, metrics
- `chart-trend.png` — Growth, improvement, ROI
- `pie-chart.png` — Insights, breakdown, analysis
- `people.png` — Teams, collaboration, stakeholders
- `briefcase.png` — Business, enterprise, professional
- `book.png` — Knowledge, repository, library
- `atom-ai.png` — AI, automation, intelligence
- `refresh.png` — Workflow, cycle, renewal
- `home.png` — Home, overview, dashboard
- `id-card.png` — Identity, contacts, profiles
- `expand.png` — Fullscreen, scale, visibility

**How to embed icons in HTML:**

```python
import base64

def embed_icon(icon_name, size=48):
    with open(f'assets/icons/{icon_name}.png', 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<img src="data:image/png;base64,{b64}" alt="{icon_name}" width="{size}" height="{size}" />'
```

Typical usage: place the icon inside a navy circular background (`background: var(--ic-navy); border-radius: 50%; padding: 12px;`) or use on a cream/light background for a cleaner look.

### When icons aren't needed

For simple visual indicators that don't warrant a full icon:
- Use a thin green (#308970) horizontal line for section dividers
- Use colored dots (small CSS circles) for list decoration
- For numbered items, use `display: flex; align-items: center; justify-content: center;` on a fixed-size circle to ensure numbers are perfectly centered
- For category labels, use pill-shaped badges with Moderat Mono text

If you find yourself reaching for an emoji, stop and use a brand icon or CSS element instead.

## CSS Polish Guidelines

These patterns prevent common visual issues:

**Centered numbers in circles** — When placing numbers inside colored circles, use flexbox centering. This is the pattern that works reliably:
```css
.number-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--ic-green);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ic-font-sans);
  font-weight: 500;
  font-size: 14px;
  flex-shrink: 0;
}
```

**Decorative geometric elements** — When adding circles or shapes as decoration, make sure they don't overlap with content containers. Use `position: absolute` with `z-index: 0` for decorative shapes, and `z-index: 1` (or `position: relative`) for content. Keep decorative elements in corners or edges where they won't collide with text or cards. Use `overflow: hidden` on the parent container to clip shapes that extend beyond boundaries.

## Layout Patterns

Ironclad assets use geometric shapes — circles, quarter-circles, triangles, rectangles — as decorative elements. These shapes use the brand colors and create visual interest without being distracting.

**Common patterns:**
- Split backgrounds: cream on one side, navy on the other
- Rounded pill-shaped buttons/badges in purple or green
- Arch/rounded-rectangle photo frames for headshots
- Geometric color blocks as decorative corners or dividers
- Generous whitespace — the brand breathes

**Logo placement:**
- Primary logo (icon + wordmark) is the default
- Use the icon mark alone when space is tight or when other branding is present
- Maintain clear space around the logo equal to one bracket width of the icon
- Minimum logo width: 100px / 1.39"
- On cream/navy: use full-color logo (green icon, navy or cream wordmark)
- On any other background: use single-color logo (white or black)

## Asset-Specific Guidance

### HTML / React artifacts
- Use CSS custom properties for the brand colors so they're easy to maintain
- Default to cream background with navy text
- Use green for primary CTAs and accent borders
- Use purple pill badges for tags and categories
- The SangBleu italic accent works beautifully in hero headlines

### Presentations — ground everything in the bundled template
The skill bundles the official FY27 Ironclad Comprehensive Slide Template at `assets/templates/ironclad-template.pptx` — a 244-slide library that is **the Ironclad design system for presentations**. Every deck should look and feel like it came from this template: same colors, same fonts, same typographic hierarchy (mono eyebrow + headline + body), same geometric decoration vocabulary (circles, arches, pills, quarter-circles), same generous whitespace, same cream/navy rhythm.

Ground yourself in the template first. Open it, skim the section map, and read a few representative slides so you've absorbed the visual grammar. Then build the deck.

**The default workflow — copy template slides and edit copy:**
1. Copy `assets/templates/ironclad-template.pptx` to the output location as the starting file.
2. Pick template slides that match what's being presented. See the section map below.
3. Delete the slides you don't need (always delete Section 1 — it is instructional content for deck creators, not presentation material).
4. Edit the copy at the `run` level (not `paragraph.text`) so the template's fonts, colors, and sizes are preserved.
5. Replace any "Replace image" placeholder with the actual image.
6. Add the customer logo where appropriate (typically title slides and case-study slides).

This is the fastest, safest path to an on-brand deck — the template slides are already proven on-brand, so copy swaps stay on-brand by default.

**When to build a new slide:**

If no template slide fits the content cleanly — e.g. a specific 3-column-with-icons layout you need that the template doesn't have, or a hybrid that mixes the impact-statement header with a stats-grid body — build a new slide rather than jamming content into the wrong layout. The rule is: **new slide, same design system**. Look at how the template does similar things and mirror its patterns.

To stay grounded, a new slide must use:
- **Only** the Ironclad color palette (cream, navy, green `#308970`, logo green `#00CA88`, purple, sand, the grays, and the secondary accents if needed). No off-palette colors.
- **Only** Moderat (body + headings) and SangBleu Kingdom italic (accent serif for one key phrase). No other fonts.
- The template's typographic hierarchy: mono all-caps eyebrow → Medium-weight headline (with optional italic SangBleu phrase) → Regular body → optional footer.
- The template's decoration language: geometric shapes (circles, quarter-circles, pills, arches) used sparingly, never busy. No gradients, no drop shadows, no clip art, no emojis.
- Cream or navy as the dominant background. Accent colors are accents, not backgrounds for whole slides.
- Breathing room — generous margins, not every pixel filled.

The easiest way to build a new slide is to duplicate the closest template slide, then adjust. That way you inherit the layout master, color palette, and font settings automatically, and you only change what you need.

**Text that doesn't fit — the two moves:**

Stat boxes, headline boxes, and eyebrow boxes are sized for specific character counts. `$2.4M` is visually wider than `82`; `THE IRONCLAD DIFFERENCE` is wider than `OPTIONAL EYEBROW`. Two ways to handle overflow:

1. **Tighten the copy first.** Ironclad's voice is confident and direct — "One platform. Every contract." beats "One platform for every contract — from request to renewal." both on-brand and on-fit. Most overflows are a copy problem, not a layout problem. The brand rewards punchy.
2. **Then shrink the font** in 2–4pt steps with `run.font.size = Pt(N)` if the copy is already as tight as it can be. If a stat number won't fit even shrunk, the layout is wrong — pick a different stats slide with a bigger number box, or build a new one with the right proportions.

Don't just leave text overflowing. Always open the deck and verify it renders cleanly; python-pptx does not detect overflow.

**Section map — pick the right slides:**

Section 1 (slides 3–12) is always skipped; it's instructions, not content.

| Section | Slide range | Use for |
| --- | --- | --- |
| 2. Title slides | 13–31 | Cover slide / deck opener |
| 3. Section dividers | 32–40 | Transitions between major parts of the deck |
| 4. TOC & agenda | 41–57 | Agenda, table of contents |
| 5. Speaker slides | 58–73 | Introducing a person (bio, headshot) |
| 6. Card listings | 74–100 | 2–4 item grids (features, benefits, options) |
| 7. Paragraph slides | 101–114 | Longer-form single concept |
| 8. Impact statements | 115–121 | Big single headline, hero moment |
| 9. Image listing slides | 122–132 | Visual-forward lists with photos |
| 10. Icon listing slides | 133–137 | Lists using Ironclad icons |
| 11. Stats & data visuals | 138–154 | Numbers, charts, metrics |
| 12. Image only | 155–157 | Full-bleed photo moments |
| 13. Large quotes | 158–160 | Customer quotes, testimonials |
| 14. Chapter slides | 161–188 | Chapter openers inside a section |
| 15. Product visuals | 189–195 | Product screenshots, UI shots |
| 16. Timeline visuals | 196–204 | Roadmaps, phased plans |
| 17. Tables | 205–217 | Structured data, comparisons |
| 18. Goals & planning | 218–224 | OKRs, goals, planning frameworks |
| 19. Internal only | 225–229 | Internal-audience slides |
| 20. Grab-and-go assets | 230–244 | Reusable elements (dividers, callouts) |

Each section contains multiple variants (dark/light, left/right image, 2-col/3-col, etc.). Skim the section in the template file and pick the variant that best matches the content.

**Building the deck with python-pptx:**

Load the template, delete unwanted slides in reverse order (so indices don't shift), then edit text at the `run` level to preserve the original formatting:

```python
from pptx import Presentation
from pptx.util import Pt

src = Presentation('assets/templates/ironclad-template.pptx')

# 0-based indices of template slides you want, in the ORDER you want them in the output.
# python-pptx does NOT use this order automatically — see the reorder step below.
desired_order = [13, 159, 41, 138]   # e.g. cover, quote, agenda, stats

# Capture the XML elements for the slides you're keeping
xml_slides = src.slides._sldIdLst
slide_ids = list(xml_slides)
kept = [slide_ids[i] for i in desired_order]

# Drop everything else
for sid in slide_ids:
    if sid not in kept:
        src.part.drop_rel(sid.rId)
        xml_slides.remove(sid)

# Reorder: python-pptx preserves original template order after deletion, so you must
# explicitly remove-and-re-append the kept elements in your desired sequence
for elem in kept:
    xml_slides.remove(elem)
for elem in kept:
    xml_slides.append(elem)

# Edit text at the RUN level (not paragraph.text or text_frame.text) — those destroy
# the run-level font/color/size formatting the template has set up
for slide in src.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.text.strip() == 'Headline placed here':
                        run.text = 'Your actual headline'

src.save('output.pptx')
```

**Mechanics that bite every time — handle them explicitly:**

1. **Slide order after deletion.** python-pptx keeps slides in their original template order. If you want a different order in your output, you must remove and re-append the kept slide elements in the desired sequence (as shown above). Skipping this step is the single most common bug — content you wrote for slide 4 lands on whatever template slide happened to come 4th in the source.

2. **Multi-run headlines preserve whitespace in separate runs.** Template headlines are often split across runs — e.g. `'Headline'` + `' placed here'`, or `'Insert short impact statement '` + `'here'`. The joining space is part of one of the runs, not a separator. When you replace both runs, keep the leading/trailing space or your words will concatenate ("IroncladAutopilot", "forms,and"). Inspect the original runs first and mirror the spacing pattern. For a two-run headline, put the space on the second run: `runs[0].text = 'Ironclad'; runs[1].text = ' Autopilot'`.

3. **Grid layouts — match shapes by position, not enumeration order.** On slides with multiple columns (stats grids, card listings, timelines), `slide.shapes` does not iterate in visual left-to-right, top-to-bottom order. Walking the shapes and filling the Nth match of a placeholder string will scramble the pairing. Instead, inspect `shape.left` and `shape.top` on the template slide once to map each visual position to a shape index, then write to shapes by index:

   ```python
   # Inspect once to find the pairing
   for si, shape in enumerate(slide.shapes):
       if shape.has_text_frame and shape.text_frame.text.strip():
           print(si, shape.left//914400, shape.top//914400, shape.text_frame.text[:40])
   # Then use specific indexes
   col_map = [(7, 8), (10, 11), (13, 14), (16, 17)]  # (number_shape, label_shape)
   ```

4. **Clear every stale placeholder, including the ones in rows you don't use.** Some template slides have "extra" rows (e.g. a stats slide with both a big number row and a smaller "Additional body copy" row). If your content only fills one row, explicitly clear the others by setting `run.text = ''` on the shapes you're not using — otherwise the lorem/placeholder text ships in the final deck. Same goes for second and third paragraphs inside a text frame: a lorem body is often followed by another lorem paragraph in the same frame.

5. **Pills are one line. Always.** The oval pill shapes used for eyebrow/intro text (e.g. `INTRO TEXT HERE`, `OPTIONAL EYEBROW`) are part of the brand's visual language — they only look right with a single line of text inside. If your copy wraps to two lines, the pill looks broken. Two moves, in this order:
   1. **Shorten the copy to match the template placeholder length.** The original placeholders are ~14-18 characters for a reason. Punchier is more on-brand anyway. `SPRING 2026 PRODUCT LAUNCH` (25 chars) is both too long and redundant with a cover that already says `SPRING 2026` — `PRODUCT LAUNCH` (14 chars) is the better call.
   2. **If the specific copy is required and can't be shortened**, shrink the font until it fits one line: `run.font.size = Pt(9)` or `Pt(10)`. Never let it wrap.
   Stat boxes and chapter-slide titles have the same fixed-width constraint — same playbook applies.

6. **Stat numbers with wider characters need extra shrinkage.** `$1.8M` is visually ~30% wider than `94%` at the same font size because `$`, `.`, and `M` occupy more horizontal space than digits. At 56pt the stat-box design works for `94%` but crowds `$1.8M`. Rule of thumb: if the stat contains `$`, letters, or punctuation, drop 10-15pt below the other stats in the same grid (e.g. `Pt(44)` when others are at `Pt(56)`).

7. **python-pptx cannot detect overflow.** Always open the saved file and visually scan every slide before considering the deck done. Every bullet above produces a deck that looks fine in the terminal output but wrong in the file.

Always edit `run.text`, never `paragraph.text` or `text_frame.text` — the latter two destroy the run-level formatting (font, color, size) the template has set up.

### One-pagers / PDFs
- Follow the light-theme type hierarchy
- Green divider lines between sections
- Navy headers, dark gray body text on cream

### Social media / banners
- Bold, minimal text
- Strong color blocking with cream + navy + one accent
- Logo in upper-left when possible

## Voice & Tone

When writing copy for Ironclad assets, the voice is:
- **Confident**: "The last CLM you'll ever need" — not "We think our CLM is pretty good"
- **Direct**: Short sentences. Active voice. No jargon soup.
- **Smart**: Assumes the reader is intelligent. Doesn't over-explain.
- **Human**: Warm without being casual. Professional without being stiff.

Avoid: buzzword salads, wishy-washy hedging, overly technical language without context, exclamation points (very sparingly, if ever).

Favor: strong verbs, concrete specifics, the word "you" (address the reader directly), short punchy headlines with one italicized key phrase.

## Quick Reference: CSS Variables

When building any HTML/CSS asset, start with these variables:

```css
:root {
  /* Core */
  --ic-cream: #F2F1EE;
  --ic-navy: #1C212B;
  --ic-logo-green: #00CA88;

  /* Primary accents */
  --ic-green: #308970;
  --ic-purple: #B27BE1;
  --ic-sand: #DDC2A4;

  /* Grays */
  --ic-dark-gray: #5F6674;
  --ic-light-gray: #ADB9C4;

  /* Secondary accents */
  --ic-orange: #F1643C;
  --ic-pink: #F5B0D2;
  --ic-blue: #6A85CF;

  /* Typography — use the embedded @font-face fonts */
  --ic-font-sans: 'Moderat', 'Inter', system-ui, -apple-system, sans-serif;
  --ic-font-mono: 'Moderat Mono', 'SF Mono', 'Fira Code', monospace;
  --ic-font-serif: 'SangBleu Kingdom', 'Playfair Display', 'Georgia', serif;
}
```

For the complete color specifications (RGB, CMYK, Pantone), typography details, and additional layout examples, read `references/brand-spec.md`.

