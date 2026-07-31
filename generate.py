#!/usr/bin/env python3
"""Generate the pirate treasure-hunt pages into c/<slug>/index.html.

Edit PAGES below, re-run `python3 generate.py`, commit and push.
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
}

# hide_at: where the physical QR for this page gets hidden (label on the print sheet).
PAGES = [
    {
        "slug": "ee3f9111",
        "hide_at": "Start card (hand to Brandon)",
        "mark": "I",
        "icon": "☠️",
        "title": "The Voyage Begins",
        "flavor": ("Ahoy, Brandon! Yer birthday treasure lies buried about this house. "
                   "Follow the map, solve the riddles, and claim yer plunder. "
                   "Stops: unknown. Booty: plentiful. Mutiny: discouraged."),
        "riddle": "I'm a <em>quiet</em> Italian, ticklish, and not your boyfriend.",
    },
    {
        "slug": "d13e91a0",
        "hide_at": "Piano (in the keys or bench)",
        "mark": "II",
        "icon": "🧭",
        "title": "Well Navigated, Matey",
        "flavor": "The keys sang true.",
        "riddle": "Find David at his fittest.",
    },
    {
        "slug": "bd0cc471",
        "hide_at": "David statue",
        "mark": "III",
        "icon": "🏺",
        "title": "Booty the First!",
        "gift": {
            "name": "Certificate o' the Lamplighter",
            "body": ("One bedside lamp, restored to full workin' glory by yer ship's engineer. "
                     "Redeemable anytime."),
            "fineprint": "Labor guaranteed by a man with a multimeter.",
        },
        "riddle": ("There be a thin mouth in the wall that swallows whatever strangers slip it. "
                   "It never chews &mdash; and today its belly holds more than usual."),
    },
    {
        "slug": "211bd549",
        "hide_at": "Mailbox",
        "mark": "IV",
        "icon": "📜",
        "title": "The Mail Run",
        "flavor": "No stamps needed where ye're goin'.",
        "riddle": "A voyage like this calls for a draught o' mead. Bottoms up, sailor.",
    },
    {
        "slug": "7fd44344",
        "hide_at": "Inside a mug (cupboard)",
        "mark": "V",
        "icon": "🍺",
        "title": "Bottoms Up!",
        "flavor": "Ye drained the tankard and found the truth at the bottom, like all good pirates.",
        "riddle": "Yer next clue lies wrapped and rolled, chillin' quietly with its identical siblings.",
    },
    {
        "slug": "4c919102",
        "hide_at": "Tortilla bag (fridge/pantry)",
        "mark": "VI",
        "icon": "🗝️",
        "title": "A Test o' Wits",
        "flavor": "Answer true, or walk the plank:",
        "gate": {
            "question": "What color be the cloth beneath the two figs?",
            "answers": ["red"],
            "placeholder": "one word",
            "unlocked": "Now find where red things go to ruin white things.",
        },
    },
    {
        "slug": "a8120a3f",
        "hide_at": "Washer (inside the drum)",
        "mark": "VII",
        "icon": "⚓",
        "title": "A Matter o' Duty",
        "flavor": "Cast yer mind back to Saturday, January 17th, 2026. Ye were there.",
        "gate": {
            "question": ("She had ____ job(s) to do on this ship, and she was going to do it. "
                         "How many?"),
            "answers": ["one", "1"],
            "placeholder": "how many?",
            "unlocked": ("Some souls would relive an ordinary day just to get it right. "
                         "We watched him do it. Yer clue sleeps in his case."),
        },
    },
    {
        "slug": "02c7edda",
        "hide_at": "About Time DVD case",
        "mark": "VIII",
        "icon": "⏳",
        "title": "About Time, Sailor",
        "flavor": "A fine film, a finer memory.",
        "riddle": ("Yer next clue stowed away inside a different game entirely &mdash; "
                   "boxed, shelved, and waitin' in the dark."),
    },
    {
        "slug": "642edf15",
        "hide_at": "Board game (games closet)",
        "mark": "IX",
        "icon": "🗺️",
        "title": "Booty the Second!",
        "gift": {
            "name": "The Locurio Expedition",
            "body": ("A treasure hunt hidden inside a treasure hunt: "
                     "Mysteries of Noximillian, an outdoor puzzle adventure. We sail together."),
            "fineprint": "locurio.com &mdash; date to be chosen by the birthday pirate.",
        },
        "gate": {
            "question": ("One more riddle before ye go. She's loved ye for a thousand years. "
                         "What does every heartbeat bring? (3 words &mdash; consult yer charts, "
                         "or the internet)"),
            "answers": ["one step closer", "closer"],
            "placeholder": "three words",
            "unlocked": ("One step closer&hellip; now look aloft! I spin above it all like a "
                         "crow's nest, and no one ever checks me back."),
        },
    },
    {
        "slug": "84d6146a",
        "hide_at": "Ceiling fan (top of a blade)",
        "mark": "X",
        "icon": "🌀",
        "title": "The Crow's Nest",
        "flavor": "Ye've climbed the riggin'. Now:",
        "riddle": ("Search where ye'd rather be right now: dead tired, face first, lights out. "
                   "Dig, sailor."),
    },
    {
        "slug": "3a260eec",
        "hide_at": "Bed (under the covers)",
        "mark": "XI",
        "icon": "🪂",
        "title": "Booty the Third: Ye're Going FLYING",
        "gift": {
            "name": "iFLY Indoor Skydiving &mdash; Seattle",
            "body": "Ye'll leave the deck entirely, ye magnificent airborne pirate.",
            "fineprint": ("Holder may exchange for one (1) less terrifying adventure. "
                          "No questions asked, minimal teasin'."),
        },
        "riddle": ("Yer final treasure can't be boxed, buried, or hidden. It be warm, it be yours, "
                   "and it's been pacin' the deck pretendin' not to watch ye this whole voyage. "
                   "Go claim it."),
    },
    {
        "slug": "ed471176",
        "hide_at": "Pinned to David's shirt",
        "mark": "X&nbsp;marks&nbsp;the&nbsp;spot",
        "icon": "❌",
        "title": "The Captain's Voucher",
        "finale": True,
        "gift": {
            "name": "Wednesday AND Thursday Night",
            "body": "Me. You. Any positions ye desire.",
            "fineprint": "Redeemable immediately. No expiration. X marks the spot.",
        },
        "closing": "Happy Birthday, Brandon. &mdash; Yer Captain",
    },
    {
        "slug": "0b94076d",
        "hide_at": "Elliptical (decoy)",
        "decoy": True,
        "icon": "🦜",
        "title": "Arr, a Sweaty Guess!",
        "flavor": "Wrong David &mdash; this one skips leg day. Back to the hunt, ye scallywag.",
    },
    {
        "slug": "6ef5d9a2",
        "hide_at": "Anywhere (decoy A)",
        "decoy": True,
        "icon": "🪵",
        "title": "Driftwood",
        "flavor": "Ye found&hellip; absolutely nothin'. This QR code be driftwood. Sail on.",
    },
    {
        "slug": "877274df",
        "hide_at": "Anywhere (decoy B)",
        "decoy": True,
        "icon": "👁️",
        "title": "A Decoy, Arr",
        "flavor": "The house be mockin' ye. It knows what ye did.",
    },
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Pirata+One&family=IM+Fell+English:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../style.css">
</head>
<body{body_class}>
<main class="parchment" style="--mx:{mx}%;--my:{my}%">
"""

FOOT = """</main>
<aside class="parchment" id="sealed" hidden>
  <div class="icon" aria-hidden="true">&#128274;</div>
  <div class="eyebrow">Brandon&rsquo;s Birthday Treasure Hunt</div>
  <h1>This Scroll Be Sealed</h1>
  <p class="flavor">The wax holds fast. Only the true mark breaks it &mdash; go scan a proper QR code, ye sneaky dog.</p>
</aside>
<script>
(function () {
  if (new URLSearchParams(location.search).get('k') !== 'PAGE_KEY') {
    document.querySelector('main').hidden = true;
    document.getElementById('sealed').hidden = false;
  }
})();
</script>
</body>
</html>
"""

GATE_JS = """<script>
(function () {{
  var accepted = {answers};
  var key = 'unlocked-' + location.pathname;
  var form = document.getElementById('gate');
  var input = document.getElementById('answer');
  var wrong = document.getElementById('wrong');
  var reveal = document.getElementById('reveal');
  function normalize(s) {{ return s.toLowerCase().replace(/[^a-z0-9]/g, ''); }}
  function unlock() {{
    form.hidden = true;
    wrong.hidden = true;
    reveal.hidden = false;
    try {{ localStorage.setItem(key, '1'); }} catch (e) {{}}
  }}
  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    if (accepted.indexOf(normalize(input.value)) !== -1) {{ unlock(); }}
    else {{ wrong.hidden = false; input.select(); }}
  }});
  try {{ if (localStorage.getItem(key)) unlock(); }} catch (e) {{}}
}})();
</script>
"""


# Serpentine walk across the shared map, so consecutive stops show adjacent
# fragments of one big chart. Decoys get leftover mid-map fragments.
TRAIL_FRAGMENTS = [(0, 0), (33, 0), (66, 0), (100, 0), (100, 50), (66, 50),
                   (33, 50), (0, 50), (0, 100), (33, 100), (66, 100), (100, 100)]
DECOY_FRAGMENTS = [(50, 25), (25, 75), (75, 75)]


def fragment_for(page):
    decoys = [p for p in PAGES if p.get("decoy")]
    if page.get("decoy"):
        return DECOY_FRAGMENTS[decoys.index(page) % len(DECOY_FRAGMENTS)]
    trail = [p for p in PAGES if not p.get("decoy")]
    return TRAIL_FRAGMENTS[trail.index(page) % len(TRAIL_FRAGMENTS)]


def render(page):
    body_class = ' class="decoy-page"' if page.get("decoy") else ""
    mx, my = fragment_for(page)
    out = [HEAD.format(title=html.escape(page["title"]), body_class=body_class, mx=mx, my=my)]
    if page.get("mark"):
        out.append(f'  <div class="seal"><span>{page["mark"]}</span></div>\n')
    out.append(f'  <div class="icon" aria-hidden="true">{page["icon"]}</div>\n')
    out.append('  <div class="eyebrow">Brandon&rsquo;s Birthday Treasure Hunt</div>\n')
    out.append(f'  <h1>{page["title"]}</h1>\n')
    if page.get("flavor"):
        out.append(f'  <p class="flavor">{page["flavor"]}</p>\n')
    if page.get("gift"):
        g = page["gift"]
        out.append('  <section class="booty">\n')
        out.append('    <div class="booty-label">&#9760; Booty Unlocked &#9760;</div>\n')
        out.append(f'    <h2>{g["name"]}</h2>\n')
        out.append(f'    <p>{g["body"]}</p>\n')
        out.append(f'    <p class="fineprint">{g["fineprint"]}</p>\n')
        out.append('  </section>\n')
    if page.get("gate"):
        gt = page["gate"]
        out.append('  <div class="rope"></div>\n')
        out.append(f'  <p class="riddle">{gt["question"]}</p>\n')
        out.append('  <form id="gate">\n')
        out.append(f'    <input id="answer" type="text" placeholder="{gt["placeholder"]}" '
                   'autocomplete="off" autocapitalize="off">\n')
        out.append('    <button type="submit">Unlock</button>\n')
        out.append('    <p id="wrong" hidden>Blimey, that be wrong. Try again.</p>\n')
        out.append('  </form>\n')
        out.append('  <div id="reveal" hidden>\n')
        out.append('    <div class="booty-label">The way forward:</div>\n')
        out.append(f'    <p class="riddle">{gt["unlocked"]}</p>\n')
        out.append('  </div>\n')
    elif page.get("riddle"):
        out.append('  <div class="rope"></div>\n')
        out.append('    <div class="booty-label">Yer next headin&rsquo;:</div>\n')
        out.append(f'  <p class="riddle">{page["riddle"]}</p>\n')
    if page.get("closing"):
        out.append(f'  <p class="closing">{page["closing"]}</p>\n')
    out.append(FOOT)
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
