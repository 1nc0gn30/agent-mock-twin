# Agent Mock Twin

![Agent Mock Twin Hero Banner](assets/hero-banner.svg)

**Agent Mock Twin** (`agent-mock-twin`) is a zero-dependency Python 3.10+ offline API mock server, LLM endpoint simulator (`/v1/chat/completions`, `/v1/messages`, `/v1/embeddings`), and telemetry workstation (`127.0.0.1:8097`). It ingests HAR 1.2 network captures and OpenAPI 3.0 specifications into SQLite (`agent_mock.db`) to replay deterministic responses with configurable latency, jitter, and chaos fault injection at `$0.00` token cost.

- **Zoth Studio v2 Dossier**: [https://zoth.nullai.tech/tools/agent-mock-twin](https://zoth.nullai.tech/tools/agent-mock-twin)
- **Repository**: [https://github.com/1nc0gn30/agent-mock-twin](https://github.com/1nc0gn30/agent-mock-twin)
- **Default Loopback Endpoint**: `http://127.0.0.1:8097`

---

## Overview

- **HAR 1.2 & OpenAPI 3.0 Ingestion (`HarParser`, `OpenAPIParser`)**: Converts captured network traces (such as exports from `agent-egress-sentinel`) or OpenAPI schemas into indexed SQLite mock routes.
- **Multi-Tier Request Matcher (`RequestMatcher`)**: Resolves incoming requests via exact signature hash, normalized path/body similarity, OpenAPI path-template matching, or built-in OpenAI/Anthropic LLM response synthesis.
- **Latency & Chaos Simulation**: Injects configurable base latency (`--latency`), random jitter (`--jitter`), and HTTP `429`/`500`/`503` chaos rates (`--chaos 0.0..1.0`) to stress-test agent retry and circuit-breaker logic offline.
- **Zero-Code Process Wrapper (`agent-mock run`)**: Launches child agent commands with `OPENAI_BASE_URL`, `OPENAI_API_BASE`, and `ANTHROPIC_BASE_URL` automatically pointed to `http://127.0.0.1:8097`.

---

## Architecture

```text
HAR 1.2 / OpenAPI 3.0 Spec ──► HarParser / OpenAPIParser ──► MockStorage (SQLite)
                                                                   │
Agent SDK / CLI (OPENAI_BASE_URL -> :8097/v1) ──► MockServer (:8097) + RequestMatcher
                                                       └── SSE Stream (/api/stream) + Web UI
```

---

## Quickstart

```bash
git clone https://github.com/1nc0gn30/agent-mock-twin.git
cd agent-mock-twin
python3 -m pip install -e .

# Start the Offline Mock Twin & Web Dashboard on 127.0.0.1:8097
agent-mock serve --host 127.0.0.1 --port 8097 --latency 25 --jitter 15
```

Or launch directly from the repository root:

```bash
python3 server.py --host 127.0.0.1 --port 8097
```

Open `http://127.0.0.1:8097` in your browser.

---

## CLI & ZothOS v3.4.0 Integration

`agent-mock` (`./bin/agent-mock`, `./bin/agent-mock-twin`, and `./bin/agent-mock-twin-tui`) imports specifications, inspects token/USD savings, and wraps agent runs:

```bash
# Inspect daemon health and cumulative token/USD savings
agent-mock --status
agent-mock --json
agent-mock stats --port 8097 --json

# Import a HAR 1.2 archive or OpenAPI 3.0 JSON file into agent_mock.db
agent-mock import path/to/agent-traffic.har

# Execute an agent command redirected to the local mock twin on :8097
agent-mock run --port 8097 -- python3 my_agent.py
```

---

## REST API Reference

Control-plane `POST` routes enforce local-origin CSRF validation (`127.0.0.1`, `localhost`, `[::1]`, or local SDK/CLI clients).

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Web dashboard (`public/index.html`) |
| `GET` | `/health`, `/api/health`, `/status` | Service health, active route count, total hits, and saved USD |
| `GET` | `/api/stats` | Detailed hit counters, saved tokens, provider list, and match-tier breakdown |
| `GET` | `/api/routes` | List all active mock routes stored in SQLite |
| `GET` | `/api/hits?limit=50` | Recent intercepted mock requests and match tiers |
| `GET` | `/api/config` | Current latency, jitter, and chaos injection settings |
| `GET` | `/api/stream` | Real-time Server-Sent Events (SSE) intercept stream |
| `POST` | `/api/upload` | Upload HAR 1.2 or OpenAPI 3.0 JSON payload into active mock storage |
| `POST` | `/api/config` | Dynamically update `base_latency_ms`, `jitter_ms`, or `chaos_rate` |
| `ANY` | `/v1/chat/completions`, `/v1/messages`, `/v1/embeddings`, `/*` | Deterministic mock replay & LLM twin endpoints |

---

## Testing & Verification

```bash
PYTHONPATH=src python3 -m pytest -q
./bin/agent-mock --help
./bin/agent-mock --json
```

---

## Support & License

100% free and open-source software under the MIT License.

- Optional support: [Buy Us a Coffee via Stripe](https://buy.stripe.com/3cIfZg27PdKo2D64Ocfw40X)
- Engineered by **1nc0gn30** (`@1nc0gn30`, [https://1nc0gn30.si](https://1nc0gn30.si)) • **NullAI** ([https://nullai.tech](https://nullai.tech))
