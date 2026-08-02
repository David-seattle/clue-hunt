#!/usr/bin/env python3
"""Generate the pirate treasure-hunt pages into c/<slug>/index.html.

Edit PAGES below, re-run `python3 generate.py`, commit and push.

Design: the full-bleed illustrated map is the page. Each stop pins a small torn
note at a different position/tilt, with a red thread leading to an X drawn at a
different spot on the map, so the trail appears to move across the chart.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).parent
BASE_URL = "https://david-seattle.github.io/clue-hunt/c"

# Per-page secret carried in the QR's ?k= param. Without it the page renders as a
# sealed scroll, so slugs alone (visible in the public repo) don't reveal clues.
KEYS = {
    "ee3f9111": "3ef5ddcefaf6",
    "d13e91a0": "1d906c9f3f85",
    "bd0cc471": "fbded66a2206",
    "211bd549": "e4ddd11159dd",
    "7fd44344": "5f189bc4ac4b",
    "4c919102": "35f9aef0fb92",
    "a8120a3f": "205771fac777",
    "02c7edda": "8a11dbccb5bd",
    "642edf15": "fa6fe5d5fb82",
    "84d6146a": "02f2dc803ba4",
    "3a260eec": "1be2f7b5ab2f",
    "ed471176": "5d82852b72c5",
    "0b94076d": "71d2cc698190",
    "6ef5d9a2": "034bd1cf49a8",
    "877274df": "0dfaadfe3481",
    "cb5b5963": "82b94935dc72",
    "2c997fc1": "85664864ea4e",
    "b2855fec": "40c8dfcc7ada",
    "0e346673": "2d898ebbf909",
    "41067d29": "856816a215fa",
    "73f71481": "e6e631492322",
}

# layout: (note_h, note_v, tilt_deg, x_pct, y_pct) — note grid position, note tilt,
# and where the map X (thread target) sits in the viewport. x/y None = no X (decoys).
# bg: which part of the square map illustration the viewport crops to.
PAGES = [
    {
        "slug": "ee3f9111",
        "hide_at": "Start card (hand to Brandon)",
        "mark": "I",
        "title": "The Voyage Begins",
        "flavor": ("Ahoy, Brandon! Yer birthday treasure lies buried about this house. "
                   "Follow the map, solve the riddles, and claim yer plunder. "
                   "Stops: unknown. Booty: plentiful. Mutiny: discouraged."),
        "riddle": ("The key to your treasure is a <em>quiet</em> Italian, ticklish, "
                   "but not your boyfriend."),
        "hint": "There be many keys to this treasure.",
        "hint2": "88 keys, to be exact.",
        "layout": ("center", "start", -2.4, 33, 82),
        "bg": (0, 0),
    },
    {
        "slug": "d13e91a0",
        "hide_at": "Piano (in the keys or bench)",
        "mark": "II",
        "title": "Well Navigated, Matey",
        "flavor": "The keys sang true.",
        "riddle": "Find David at his fittest.",
        "hint": "This David be stone cold.",
        "hint2": "The real David be in Florence.",
        "layout": ("end", "start", 1.8, 18, 72),
        "bg": (50, 0),
    },
    {
        "slug": "bd0cc471",
        "hide_at": "David statue",
        "mark": "III",
        "title": "Booty the First!",
        "gift": {
            "name": "Certificate o' the Lamplighter",
            "body": ("One bedside lamp, restored to full workin' glory by yer ship's engineer. "
                     "Redeemable anytime."),
            "fineprint": "Labor guaranteed by a pirate with a multimeter.",
        },
        "riddle": ("There be a thin mouth in the wall that swallows whatever strangers put in it. "
                   "It never bites, and today its belly holds more than usual."),
        "hint": "Only 82 cents to forever put yours inside.",
        "hint2": "One man puts his junk in here almost every day.",
        "layout": ("center", "center", -1.5, 78, 16),
        "bg": (100, 0),
    },
    {
        "slug": "211bd549",
        "hide_at": "Mailbox",
        "mark": "IV",
        "title": "The Mail Run",
        "flavor": "No stamps needed where ye're goin'.",
        "riddle": ("Gaze in the mirror, ye handsome devil. A bird of unusual size "
                   "holds the key below."),
        "hint": "Open the drawer.",
        "hint2": "Not in a bathroom.",
        "layout": ("start", "start", 2.2, 72, 78),
        "bg": (100, 50),
    },
    {
        "slug": "41067d29",
        "hide_at": "Hall tree drawer (front door)",
        "mark": "V",
        "title": "A Handsome Pirate Indeed",
        "flavor": "The mirror never lies, and the drawer never disappoints.",
        "riddle": "A voyage like this calls for a draught o' mead. Bottoms up, sailor.",
        "hint": "Head to the galley.",
        "hint2": "Pour in here, and bottoms up.",
        "layout": ("center", "start", 1.4, 25, 72),
        "bg": (25, 0),
    },
    {
        "slug": "7fd44344",
        "hide_at": "Inside a mug (cupboard)",
        "mark": "VI",
        "title": "Bottoms Up!",
        "flavor": "Not every tankard holds mead. This one held yer next headin'.",
        "riddle": ("What do ye do with a drunken sailor? "
                   "Ye have to get him drunk to find out!"),
        "hint": "Opposite of top shelf.",
        "hint2": "We uncork together.",
        "layout": ("end", "center", -1.8, 22, 18),
        "bg": (50, 50),
    },
    {
        "slug": "73f71481",
        "hide_at": "Wine drawer (fridge)",
        "mark": "VII",
        "title": "Booty the Second!",
        "flavor": "Ha! Ye found the good stuff.",
        "gift": {
            "name": "The Captain's Reserve",
            "body": "A sweet bottle o' wine. Ye found it, ye keep it.",
            "fineprint": "The Captain gets a glass.",
        },
        "riddle": ("Let us see if you can find yer next clue, waiting to be wrapped "
                   "or rolled, chillin' with its siblings."),
        "hint": "Tasty circles.",
        "hint2": "Brrr &mdash; a winter cold is blowing in.",
        "layout": ("start", "center", -1.7, 78, 80),
        "bg": (75, 50),
    },
    {
        "slug": "4c919102",
        "hide_at": "Tortilla bag (fridge/pantry)",
        "mark": "VIII",
        "title": "A Test o' Wits",
        "flavor": "Answer true, or walk the plank:",
        "gate": {
            "question": "What color be the cloth beneath the two figs?",
            "answers": ["red"],
            "placeholder": "one word",
            "hint": "You can't eat these figs.",
            "hint2": "This one be artistic.",
            "unlocked_hint": "Cold is best.",
            "unlocked_hint2": "Pick a spin, not a tumble.",
            "unlocked": "Now find where red things go to ruin white things.",
        },
        "layout": ("center", "start", 1.2, 80, 82),
        "bg": (0, 50),
    },
    {
        "slug": "a8120a3f",
        "hide_at": "Washer (inside the drum)",
        "mark": "IX",
        "title": "A Matter o' Duty",
        "gate": {
            "question": ("January 17th: The ship had a woman on the crew. "
                         "How many jobs did she have?"),
            "answers": ["one", "1"],
            "placeholder": "how many?",
            "hint": "She was on a quest.",
            "hint2": "By Grabthar&rsquo;s hammer&hellip;",
            "unlocked_hint": "Grab the Kleenex and the popcorn.",
            "unlocked_hint2": "A DVD case.",
            "success": "A smart pirate ye are! Now ye got one job to do.",
            "unlocked": "The case of a man, reliving an ordinary day.",
        },
        "layout": ("start", "center", -2.0, 82, 22),
        "bg": (0, 100),
    },
    {
        "slug": "02c7edda",
        "hide_at": "About Time DVD case",
        "mark": "X",
        "title": "Booty the Third!",
        "flavor": "A fine film, a finer memory.",
        "gift": {
            "name": "The Locurio Expedition",
            "body": ("A treasure hunt hidden inside a treasure hunt: "
                     "Mysteries of Noximillian, an outdoor puzzle adventure. We sail together."),
            "fineprint": ('<a href="https://www.locurio.com/outdoor-escape-game-mysteries-of-noximillian/">'
                          "Mysteries of Noximillian</a> &mdash; date to be chosen by the birthday pirate."),
        },
        "riddle": ("Captain a ship on the hunt for the underwater metal beast. "
                   "Can you find a crew of 8?"),
        "hint": "The treasure is boxed in.",
        "hint2": "2 to 8 players.",
        "layout": ("end", "end", 1.6, 28, 14),
        "bg": (50, 100),
    },
    {
        "slug": "642edf15",
        "hide_at": "Board game (games closet)",
        "mark": "XI",
        "title": "A Siren's Riddle",
        "gate": {
            "question": ("She's loved ye for M years. What does every heartbeat bring? "
                         "(3 words &mdash; consult yer charts, or the internet)"),
            "answers": ["one step closer", "closer"],
            "placeholder": "three words",
            "hint": "These people sparkle on the peninsula.",
            "hint2": "Song lyrics.",
            "unlocked_hint": "A swarthy mate like you needs no chair.",
            "unlocked_hint2": "Watch out for the dust.",
            "unlocked": "One step closer&hellip; the crow's nest is often untouched.",
        },
        "layout": ("center", "center", -1.2, 86, 60),
        "bg": (100, 100),
    },
    {
        "slug": "84d6146a",
        "hide_at": "Ceiling fan (top of a blade)",
        "mark": "XII",
        "title": "The Crow's Nest",
        "flavor": "Ye've climbed the riggin'. Now:",
        "riddle": ("Dead tired men tell no tales. Uncover the treasure, or ye'll be "
                   "sleeping with the fishes."),
        "hint": "If ye're stuck, ye might need a rest.",
        "hint2": "Uncover the foot.",
        "layout": ("start", "start", 2.4, 70, 66),
        "bg": (25, 25),
    },
    {
        "slug": "3a260eec",
        "hide_at": "Bed (under the covers)",
        "mark": "XIII",
        "title": "Booty the Fourth!",
        "gift": {
            "name": "iFLY Indoor Skydiving &mdash; Seattle",
            "body": "Ye'll leave the deck entirely, but not too far, ye sexy airborne pirate.",
            "fineprint": ('<a href="https://www.iflyworld.com/seattle">iflyworld.com/seattle</a> &mdash; '
                          "Holder may exchange for one (1) less terrifying adventure. "
                          "No questions asked, minimal teasin'."),
        },
        "riddle": ("Yer final treasure can't be boxed, buried, or hidden. It be warm, it be yours, "
                   "and it's been pacin' the deck pretendin' not to watch ye this whole voyage. "
                   "Go claim it."),
        "layout": ("center", "center", -1.6, 20, 84),
        "bg": (75, 25),
    },
    {
        "slug": "ed471176",
        "hide_at": "Pinned to David's shirt",
        "mark": "&#10008;",
        "title": "The Captain's Voucher",
        "finale": True,
        "gift": {
            "name": "Wednesday AND Thursday Night",
            "body": "Me. You. Any positions ye desire.",
            "fineprint": "Redeemable immediately. No expiration. X marks the spot.",
        },
        "closing": "Happy Birthday, Brandon. &mdash; Yer Captain",
        "layout": ("center", "center", 0.8, 50, 90),
        "bg": (50, 75),
    },
    {
        "slug": "0b94076d",
        "hide_at": "Elliptical (decoy)",
        "decoy": True,
        "title": "Arr, a Sweaty Guess!",
        "flavor": "Wrong David &mdash; this one skips leg day. Back to the hunt, ye scallywag.",
        "layout": ("end", "start", -3.0, None, None),
        "bg": (25, 75),
    },
    {
        "slug": "6ef5d9a2",
        "hide_at": "Anywhere (decoy A)",
        "decoy": True,
        "title": "Driftwood",
        "flavor": "Ye found&hellip; absolutely nothin'. This QR code be driftwood. Sail on.",
        "layout": ("center", "center", 2.6, None, None),
        "bg": (75, 75),
    },
    {
        "slug": "877274df",
        "hide_at": "Anywhere (decoy B)",
        "decoy": True,
        "title": "Yo Ho No",
        "flavor": "Yo ho? Yo NO. Nothing be buried here.",
        "layout": ("start", "end", -2.2, None, None),
        "bg": (50, 25),
    },
    {
        "slug": "cb5b5963",
        "hide_at": "Anywhere (decoy C)",
        "decoy": True,
        "title": "Ship Happens",
        "flavor": "Ye've run aground, sailor. Ship happens. Back to the map.",
        "layout": ("center", "start", 2.0, None, None),
        "bg": (0, 25),
    },
    {
        "slug": "2c997fc1",
        "hide_at": "Anywhere (decoy D)",
        "decoy": True,
        "title": "Close, But No Cannon",
        "flavor": "Fire again, gunner.",
        "layout": ("end", "center", -2.6, None, None),
        "bg": (100, 25),
    },
    {
        "slug": "b2855fec",
        "hide_at": "Anywhere (decoy E)",
        "decoy": True,
        "title": "Knot a Clue",
        "flavor": "Ye have knot a clue. Literally &mdash; this isn't one.",
        "layout": ("start", "center", 2.8, None, None),
        "bg": (25, 50),
    },
    {
        "slug": "0e346673",
        "hide_at": "Anywhere (decoy F)",
        "decoy": True,
        "title": "Whale, Whale, Whale",
        "flavor": "Whale, whale, whale&hellip; what have we here? Nothin'.",
        "layout": ("center", "end", -1.4, None, None),
        "bg": (75, 50),
    },
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏴&#8205;☠️</text></svg>">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=IM+Fell+English:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../style.css">
<script src="../../webaudiofont/WebAudioFontPlayer.js" defer></script>
<script src="../../webaudiofont/0210_Aspirin_sf2_file.js" defer></script>
<script src="../../webaudiofont/0250_Aspirin_sf2_file.js" defer></script>
<script src="../../shanty.js" defer></script>
</head>
<body{body_class} style="--bx:{bx}%;--by:{by}%">
<div id="content">
"""

SEALED = """</div>
</div>
<div class="scene" id="sealed-scene" hidden>
  <div class="note-wrap">
    <div class="pin"><span>&#128274;</span></div>
    <main class="note">
      <div class="eyebrow">Brandon&rsquo;s Treasure Hunt</div>
      <h1>This Scroll Be Sealed</h1>
      <p class="riddle">The wax holds fast. Only the true mark breaks it &mdash; go scan a proper QR code, ye sneaky dog.</p>
    </main>
  </div>
</div>
<script>
(function () {
  if (new URLSearchParams(location.search).get('k') !== 'PAGE_KEY') {
    document.getElementById('content').hidden = true;
    document.getElementById('sealed-scene').hidden = false;
  }
})();
</script>
</body>
</html>
"""

GATE_JS = """<script>
(function () {{
  var accepted = {answers};
  var quiz = document.getElementById('quiz');
  var form = document.getElementById('gate');
  var input = document.getElementById('answer');
  var wrong = document.getElementById('wrong');
  var reveal = document.getElementById('reveal');
  function normalize(s) {{ return s.toLowerCase().replace(/[^a-z0-9]/g, ''); }}
  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    if (accepted.indexOf(normalize(input.value)) !== -1) {{
      quiz.hidden = true;
      reveal.hidden = false;
      if (window.shantyBell) window.shantyBell();
    }} else {{
      wrong.hidden = false;
      input.select();
    }}
  }});
}})();
</script>
"""

# Approximate viewport-percent center of the note for each grid slot, used as the
# thread's starting point.
NOTE_ANCHOR_H = {"start": 26, "center": 50, "end": 74}
NOTE_ANCHOR_V = {"start": 30, "center": 48, "end": 62}


def thread_svg(layout):
    h, v, tilt, xx, xy = layout
    if xx is None:
        return ""
    nx, ny = NOTE_ANCHOR_H[h], NOTE_ANCHOR_V[v]
    # Bow the thread sideways so it drapes rather than shooting straight.
    mx, my = (nx + xx) / 2 + (10 if tilt < 0 else -10), (ny + xy) / 2
    path = f"M{nx},{ny} Q{mx:.0f},{my:.0f} {xx},{xy}"
    return (f'<svg class="thread" viewBox="0 0 100 100" preserveAspectRatio="none" '
            f'aria-hidden="true"><path d="{path}" vector-effect="non-scaling-stroke"/></svg>\n'
            f'<div class="xmark" style="left:{xx}%;top:{xy}%">&#10008;</div>\n')



CHEST_SVG = ('<svg class="chest" viewBox="0 0 64 50" aria-hidden="true">'
             '<g stroke="#5e3f16" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">'
             '<g stroke="#b98a2e" stroke-width="1.5" opacity="0.75">'
             '<path d="M32 6 V1 M19 9 L15 5 M45 9 L49 5 M12 15 L7 13 M52 15 L57 13" fill="none"/></g>'
             '<path d="M12 20 Q12 8 32 8 Q52 8 52 20 L12 20 Z" fill="#8a5a24"/>'
             '<path d="M14 20 L50 20 L48 24 L16 24 Z" fill="#3a2410"/>'
             '<circle cx="23" cy="24" r="4" fill="#e3b13c"/>'
             '<circle cx="32" cy="22" r="4.5" fill="#c9962f"/>'
             '<circle cx="41" cy="24" r="4" fill="#e3b13c"/>'
             '<path d="M14 26 H50 V44 H14 Z" fill="#a06a2c"/>'
             '<path d="M14 34 H50" fill="none"/>'
             '<path d="M21 26 V44 M43 26 V44" fill="none"/>'
             '<rect x="28" y="29" width="8" height="9" rx="1.5" fill="#e3b13c"/>'
             '<circle cx="32" cy="33" r="1.2" fill="#3a2410" stroke="none"/>'
             '</g></svg>')


def hint_html(text, text2=None):
    more = ''
    if text2:
        more = ('<details class="hint hint-more"><summary>Still lost? One more hint</summary>'
                f'<p>{text2}</p></details>')
    return ('  <details class="hint"><summary>Need a hint, sailor?</summary>'
            f'<p>{text}</p>{more}</details>\n')

def render(page):
    h, v, tilt, xx, xy = page["layout"]
    bx, by = page["bg"]
    body_class = ' class="decoy-page"' if page.get("decoy") else ""
    wide = " note-wide" if page.get("gift") or page.get("gate") else ""
    out = [HEAD.format(title=html.escape(page["title"]), body_class=body_class, bx=bx, by=by)]
    out.append(thread_svg(page["layout"]))
    out.append(f'<div class="scene" style="--jc:{h};--ai:{v}">\n')
    out.append(f'<div class="note-wrap" style="--tilt:{tilt}deg">\n')
    if page.get("mark"):
        out.append(f'  <div class="pin"><span>{page["mark"]}</span></div>\n')
    out.append(f'  <main class="note{wide}">\n')
    out.append('  <div class="eyebrow">Brandon&rsquo;s Treasure Hunt</div>\n')
    out.append(f'  <h1>{page["title"]}</h1>\n')
    if page.get("flavor"):
        out.append(f'  <p class="flavor">{page["flavor"]}</p>\n')
    if page.get("gift"):
        g = page["gift"]
        out.append('  <section class="booty">\n')
        out.append(f'    {CHEST_SVG}\n')
        out.append('    <div class="booty-label">Treasure Found</div>\n')
        out.append(f'    <h2>{g["name"]}</h2>\n')
        out.append(f'    <p>{g["body"]}</p>\n')
        out.append(f'    <p class="fineprint">{g["fineprint"]}</p>\n')
        out.append('  </section>\n')
    if page.get("gate"):
        gt = page["gate"]
        out.append('  <div id="quiz">\n')
        out.append(f'  <p class="riddle">{gt["question"]}</p>\n')
        out.append('  <form id="gate">\n')
        out.append(f'    <input id="answer" type="text" placeholder="{gt["placeholder"]}" '
                   'autocomplete="off" autocapitalize="off">\n')
        out.append('    <button type="submit">Unlock</button>\n')
        out.append('    <p id="wrong" hidden>Blimey, that be wrong. Try again.</p>\n')
        out.append('  </form>\n')
        if gt.get("hint"):
            out.append(hint_html(gt["hint"], gt.get("hint2")))
        out.append('  </div>\n')
        out.append('  <div id="reveal" hidden>\n')
        if gt.get("success"):
            out.append(f'    <p class="flavor">{gt["success"]}</p>\n')
        else:
            out.append('    <div class="label">The way forward</div>\n')
        out.append(f'    <p class="riddle">{gt["unlocked"]}</p>\n')
        if gt.get("unlocked_hint"):
            out.append(hint_html(gt["unlocked_hint"], gt.get("unlocked_hint2")))
        out.append('  </div>\n')
    elif page.get("riddle"):
        if page.get("gift"):
            out.append('    <div class="label">Yer next headin&rsquo;</div>\n')
        out.append(f'  <p class="riddle">{page["riddle"]}</p>\n')
        if page.get("hint"):
            out.append(hint_html(page["hint"], page.get("hint2")))
    if page.get("closing"):
        out.append(f'  <p class="closing">{page["closing"]}</p>\n')
    out.append('  </main>\n</div>\n')
    out.append(SEALED)
    html_text = "".join(out).replace("PAGE_KEY", KEYS[page["slug"]])
    if page.get("gate"):
        answers = "[" + ", ".join(f'"{a.replace(" ", "")}"' for a in page["gate"]["answers"]) + "]"
        html_text = html_text.replace("</body>", GATE_JS.format(answers=answers) + "</body>")
    return html_text


def main():
    urls = []
    for i, page in enumerate(PAGES, 1):
        d = ROOT / "c" / page["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(page))
        url = f'{BASE_URL}/{page["slug"]}/?k={KEYS[page["slug"]]}'
        name = f'{i:02d}-' + "".join(
            ch for ch in page["hide_at"].split("(")[0].strip().lower().replace(" ", "-")
            if ch.isalnum() or ch == "-")
        urls.append(f"{name}\t{page['hide_at']}\t{url}")
        print(f'{page["slug"]}  {page["hide_at"]}')
    (ROOT / "urls.tsv").write_text("\n".join(urls) + "\n")


if __name__ == "__main__":
    main()
