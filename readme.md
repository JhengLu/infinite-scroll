# Infinite Scroll Demo

A self-contained infinite scroll webpage served via nginx inside a Docker container.
Scrolling down continuously loads batches of items until all **10 000** entries have been displayed.

## How it works

| Piece | Role |
|---|---|
| `index.html` | Single-page app — renders cards and drives scroll logic |
| `generate_data.py` | Generates `data.json` (10 000 fake posts) at Docker build time |
| `Dockerfile` | Multi-stage build: Python generates data → nginx serves it |
| `launch.sh` | Convenience script: builds the image and starts the container |

### Scroll mechanism

- An `IntersectionObserver` watches a sentinel `<div>` at the bottom of the list.
- When the sentinel comes within **400 px** of the viewport, the next page of 20 items is appended.
- `data.json` is fetched once and cached in memory; subsequent pages slice the in-memory array — no repeated network calls.
- An `AbortController` cancels any in-flight fetch if a new load is triggered before it completes.
- On error, a retry message is shown; scrolling down triggers another attempt.

## Quick start

```bash
./launch.sh          # build + run on port 8082 (default)
PORT=9090 ./launch.sh  # run on a custom port
```

Then open `http://localhost:8082` in a browser.

## Manual Docker commands

```bash
# Build
docker build -t infinite-scroll .

# Run
docker run -d --name infinite-scroll -p 8082:80 infinite-scroll

# Stop & remove
docker stop infinite-scroll && docker rm infinite-scroll

# View logs
docker logs -f infinite-scroll
```

## File structure

```
infinite_scroll/
├── index.html          # frontend
├── generate_data.py    # data generator (runs at build time)
├── Dockerfile          # multi-stage build
├── launch.sh           # build & run helper
└── readme.md           # this file
```

## Customisation

| What | Where |
|---|---|
| Items per page | `PAGE_SIZE` constant in `index.html` |
| Total items | `range(1, 10_001)` in `generate_data.py` + `MAX_PAGES` in `index.html` |
| Port | `PORT` env var passed to `launch.sh`, or `-p` flag in `docker run` |
| Real data source | Replace `fetchPage()` in `index.html` with a call to your own paginated API |
