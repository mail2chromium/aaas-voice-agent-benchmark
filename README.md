# AaaS Voice Agent Benchmark 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **SaaS charges for ACCESS. AaaS charges for OUTCOMES.**

Benchmark suite comparing traditional SaaS API workflows against** Agentic AI (AaaS)** replacements. Measures cost, latency, accuracy, and throughput - with real production data.

## Results Summary

| Metric | SaaS Stack | AaaS Agents | Improvement |
|--------|:----------:|:-----------:|:-----------:|
| Monthly Cost | $2,052 | $610 | **-70.3%** |
| Response Time | 4.2 hours | 12 seconds | **-99.9%** |
| Resolution Rate | 64% | 91% | **+42%** |
| Tasks/Day | 120 | 800 | **+567%** |
| Availability | 8 hrs/day | 24/7 | **+200%** |

## What's Inside

### Benchmarks (`benchmarks/`)
- `crm_workflow.py` — Salesforce CRM workflow vs AI Voice CRM Agent
- `support_workflow.py` — Zendesk support vs AI Voice Support Agent
- `analytics_workflow.py` — Mixpanel analytics vs AI Analytics Agent
- `scheduling_workflow.py` — Calendly scheduling vs AI Voice Booking Agent
- `cost_calculator.py` — Real pricing comparison with current API rates

### Production Agent Templates (`agents/`)
- `voice_crm_agent.py` — LiveKit-based voice CRM agent (replaces Salesforce + Calendly + email)
- `voice_support_agent.py` — Voice AI support agent with knowledge base and escalation
- `analytics_agent.py` — Automated analytics agent (replaces Mixpanel dashboards)
- `scheduling_agent.py` — Voice-based appointment booking agent

### Results (`results/`)
- Raw benchmark data (JSON)
- Comparison charts (PNG, SVG)
- Interactive HTML report

<img width="2752" height="1536" alt="Agentic as a Service - benchmark" src="https://github.com/user-attachments/assets/e6fae14d-bdaa-4311-a393-c62ce5407763" />

## Quick Start

```bash
# Clone
git clone https://github.com/mail2chromium/aaas-voice-agent-benchmark.git
cd aaas-voice-agent-benchmark

# Install
pip install -r requirements.txt

# Configure API keys
cp configs/example.env configs/.env
# Edit .env with your API keys

# Run all benchmarks
make benchmark

# Generate comparison charts
make charts

# Run the full report
make report
```

### Docker (Recommended)

```bash
docker-compose up --build
# Results available at http://localhost:8080
```

## Configuration

```yaml
# configs/benchmark.yaml
benchmark:
  iterations: 100          # calls per test
  warmup: 10               # warmup calls (excluded from results)
  regions:
    - us-east-1
    - eu-west-1
    - ap-south-1           # Lahore region

saas_stack:
  crm: salesforce
  support: zendesk
  analytics: mixpanel
  scheduling: calendly

aaas_stack:
  stt: deepgram-nova-3
  llm: gpt-4o
  tts: elevenlabs-flash-v2.5
  orchestrator: livekit-agents
```

## Methodology

1. **Identical tasks**: Both SaaS and AaaS systems perform the exact same operations
2. **Real APIs**: We call actual SaaS APIs (Salesforce, Zendesk) and measure real response times
3. **Production conditions**: Tests run with realistic data, concurrent loads, and network latency
4. **Cost accuracy**: Pricing pulled from current public pricing pages, verified against our invoices
5. **Statistical rigor**: P50, P95, P99 latency percentiles, confidence intervals reported

## Related Article

This benchmark accompanies the Medium article: **"SaaS is Dead, Welcome to AaaS (Agentic as a Service)"** by Muhammad Usman Bashir.

Read the full analysis: [Medium Article](https://medium.com/@BeingOttoman/-f0bf9b920b01)

## Author

**Muhammad Usman Bashir** — CTO @ [RTC League](https://rtcleague.com)
- U.S. Patent holder in WebRTC
- 2025 UAE Real-Time AI Award winner
- Forbes 40 Under 40

## License

MIT License — use freely, attribution appreciated.
