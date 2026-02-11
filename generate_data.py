"""
Generate 10 000 fake posts split into per-page JSON files, plus a lightweight
search index for client-side full-text search.

Output layout (relative to this script):
  pages/0.json        → items 1-20   (full item data)
  pages/1.json        → items 21-40
  ...
  pages/499.json      → items 9981-10000
  search-index.json   → all 10 000 items (used by the search bar)
"""
import json, random, os

PAGE_SIZE  = 20
TOTAL      = 10_000

WORDS = (
    "apple banana cherry delta echo foxtrot golf hotel india juliet kilo lima"
    " mike november oscar papa quebec romeo sierra tango uniform victor whiskey"
    " xray yankee zulu alpha bravo cloud dawn earth flame grace hope ivory jade"
    " karma lunar magic noble ocean prism quest river solar tiger ultra vapor"
    " waltz xenon yellow zebra amber blaze coral dusty ember frost glade haven"
).split()

def sentence(n=8):
    return " ".join(random.choices(WORDS, k=n)).capitalize() + "."

def paragraph(sentences=4):
    return " ".join(sentence(random.randint(6, 12)) for _ in range(sentences))

random.seed(42)
items = [
    {
        "id": i,
        "userId": random.randint(1, 100),
        "title": sentence(random.randint(4, 8)).rstrip("."),
        "body": paragraph(random.randint(2, 5)),
    }
    for i in range(1, TOTAL + 1)
]

base_dir = os.path.dirname(os.path.abspath(__file__))

# ── per-page files ────────────────────────────────────────────────────────────
pages_dir = os.path.join(base_dir, "pages")
os.makedirs(pages_dir, exist_ok=True)

num_pages = TOTAL // PAGE_SIZE
for p in range(num_pages):
    page_items = items[p * PAGE_SIZE : (p + 1) * PAGE_SIZE]
    with open(os.path.join(pages_dir, f"{p}.json"), "w") as f:
        json.dump(page_items, f)

print(f"Generated {num_pages} page files in {pages_dir}/")

# ── search index ──────────────────────────────────────────────────────────────
search_index_path = os.path.join(base_dir, "search-index.json")
with open(search_index_path, "w") as f:
    json.dump(items, f)

print(f"Generated search index -> {search_index_path}")
