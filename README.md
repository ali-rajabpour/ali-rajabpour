## Ali Rajabpour Sanati

Medical doctor. I write software for clinical work, automated trading, and the infrastructure both of them run on. Most of it ships privately, so the numbers below cover public and private repositories alike.

[rajabpour.com](https://rajabpour.com) · [LinkedIn](https://www.linkedin.com/in/alirajabpour/) · [ali.poursanati@gmail.com](mailto:ali.poursanati@gmail.com) · [Telegram](https://t.me/ali_rps) · [X](https://twitter.com/A_Rajabpour)

---

### Activity

<!-- stats:start -->

| | |
|---|---|
| Commits, all repositories | **4,111** (1,956 in 2026) |
| Contributions, all time | **4,227** |
| Pull requests merged | **8** (5 to repositories I don't own) |
| Repositories | **86** (36 private) |
| Repositories touched in 2026 | **64** |
| Organizations | **3** (5 further repositories, 216 commits) |

**Organizations I build in**

| Organization | Repositories | Commits | Work |
|---|---|---|---|
| AITB | 3 private | 200 | Crypto trading automation |
| Trading client | 1 private | 8 | MQL5 strategy development |
| Healthcare client | 1 private | 8 | Clinic web platform |

**Where the commits go**

| Area | Share | Visibility |
|---|---|---|
| Trading systems | 86% | public + private |
| Tooling / other | 9% | public + private |
| Networking / infra | 2% | public + private |
| Blockchain | 2% | public + private |
| Healthcare | 1% | public + private |

**Languages by volume** (source bytes across public and private repositories)

| Language | Share | |
|---|---|---|
| TypeScript | 32.6% | `█████████████` |
| Python | 26.5% | `███████████` |
| MQL5 | 15.8% | `██████` |
| PHP | 5.4% | `██` |
| Solidity | 3.7% | `█` |
| Jupyter Notebook | 3.0% | `█` |
| TeX | 2.6% | `█` |
| HTML | 2.6% | `█` |

<sub>Generated 24 Aug 2026 by [`scripts/profile_stats.py`](scripts/profile_stats.py). Private repositories are counted, never named beyond the list below.</sub>

<!-- stats:end -->

---

### Public work

| Project | What it does | Stack |
|---|---|---|
| [tradingview-mcp](https://github.com/ali-rajabpour/tradingview-mcp) | MCP server that pulls TradingView chart snapshots through Playwright, so an agent can look at a chart instead of guessing from OHLC | Python, Playwright |
| [metatrader-mcp](https://github.com/ali-rajabpour/metatrader-mcp) | MCP server for MetaTrader 5: real chart screenshots and live market data from a running terminal | Python, MT5 |
| [PDF-LLMizer](https://github.com/ali-rajabpour/PDF-LLMizer) | Splits PDFs along their bookmark tree and converts each piece to structured markdown for LLM ingestion | Python |
| [gost-dpi-evader](https://github.com/ali-rajabpour/gost-dpi-evader) | DPI-resistant HTTPS proxy on GOST + Traefik; one domain and a few variables to deploy | Shell, Docker |
| [dokploy-9router-private](https://github.com/ali-rajabpour/dokploy-9router-private) | 9Router behind a Tailscale sidecar, reachable only from the tailnet — no public exposure | Shell, Tailscale |
| [Personal-DoH](https://github.com/ali-rajabpour/Personal-DoH) | Self-hosted DNS-over-HTTPS resolver | Shell |
| [NameMimicker](https://github.com/ali-rajabpour/NameMimicker) | Generates Unicode lookalike strings for homoglyph and phishing-surface research | Python |
| [FileFlow](https://github.com/ali-rajabpour/FileFlow) | Maps file-to-file import dependencies in a Python project and writes a diagram plus markdown report, standard library only | Python |
| [Discord-Automation](https://github.com/ali-rajabpour/Discord-Automation) | Chrome extension with a Python backend for multi-account message scheduling, with batching and account rotation | TypeScript, Python |
| [persian-google-calendar](https://github.com/ali-rajabpour/persian-google-calendar) | Google Calendar viewed and edited through a Jalali calendar interface | TypeScript, SCSS |
| [QURC](https://github.com/ali-rajabpour/QURC) | Infrastructure for a TRC20 token: landing page, Telegram mini app, contract tooling | HTML, Solidity |
| [ResearchDataCleaner](https://github.com/ali-rajabpour/ResearchDataCleaner) | Preprocesses raw patient data for rare neurological disease studies — missing values, normalisation, export | Python, pandas |
| [Leverage_PosSize_RR_TelegramBot](https://github.com/ali-rajabpour/Leverage_PosSize_RR_TelegramBot) | Telegram bot that sizes a position from account risk, stop distance and target R | Python |
| [Automated-Traffic-Tickets-Device](https://github.com/ali-rajabpour/Automated-Traffic-Tickets-Device) | Roadside unit that recognises, records and uploads traffic violations | Arduino, Processing |
| [CIDR-to-IP-List](https://github.com/ali-rajabpour/CIDR-to-IP-List) | Expands CIDR blocks into flat address lists for firewall and routing config | Python |

Upstream contributions include a merged performance patch to [telemt](https://github.com/telemt/telemt), a Rust MTProto proxy, cutting per-session allocations on the hot path.

---

### Private work

Client and production systems. Named here because the work is real; code stays closed.

**Healthcare**

| Project | What it does | Stack |
|---|---|---|
| OmanEMR | Electronic medical record system for clinical use in Oman. Largest single codebase I maintain. | TypeScript, Node |
| MedLitHarvester | Retrieves, downloads and segments full-text medical literature for systematic review work | Python |

**Trading systems**

| Project | What it does | Stack |
|---|---|---|
| Phoenix | Automated trading platform, 21 services — broken out below | Python, TypeScript, MQL5, Shell |
| AITB Crypto Trade Bot | Research and execution notebooks for a crypto trading desk, plus its operator front end | Jupyter, Python, TypeScript |
| Box Strategy EA | Box-breakout expert advisor written for a client, sized for prop firm and retail accounts alike | MQL5 |

<details>
<summary>Phoenix, by layer</summary>

<br>

| Layer | Services |
|---|---|
| Execution | `PhoenixTradingBot` orchestrator · `Phoenix-Core` MT5 instance behind FastAPI · `Phoenix-MT5-Headless` terminal on a headless host · `Phoenix-FtCrypto` Freqtrade arm for crypto · `Phoenix-Strategy` MQL5 strategy set · `Phoenix-Backtest` |
| Data and messaging | `Phoenix_Kafka` broker and console · `Phoenix_KafkaHandler` Kafka RPC for Freqtrade · `Phoenix_FTCore_RESTAPI` REST to Kafka bridge · `Phoenix-CurrencyRate` · `Phoenix-TV-Shotter` time-stamped chart capture · `Phoenix-Trade-Synchronizer` |
| Interfaces | `Phoenix-API` · `Phoenix_UI` · `Phoenix-Telegram-MiniApp` · `Phoenix-TGFW` signal forwarder |
| Platform and operations | `Phoenix-Auth` · `Phoenix-Traefik` edge · `Phoenix-Mail` · `Phoenix-Glitchtip` error tracking · `Phoenix-AdminTools` |

</details>

**Infrastructure and blockchain**

| Project | What it does | Stack |
|---|---|---|
| ServerMGMT | Provisioning and maintenance scripts for my server fleet | Shell |
| TRC20-Token / BEP20-Token-Generator | Contract generators and deployment tooling for TRC20 and BEP20 tokens | Solidity |
| MultiBC_Faucet | Multi-chain testnet faucet | Solidity, Python |
| Rajabpour.com | Personal site and writing platform | TypeScript |

---

### ARPS — trading indicators and strategies

Written under the ARPS name since 2020. Thirty-two are published for TradingView in Pine Script; the MetaTrader 5 expert advisors stay private because they run live capital.

**Ichimoku and Gann**

[Super Ichimoku 2025](https://github.com/ali-rajabpour/ARPS-Super-Ichimoku-2025) ·
[Super Ichimoku System](https://github.com/ali-rajabpour/ARPS-Super-Ichimoku-System) ·
[Super Ichimoku v5](https://github.com/ali-rajabpour/ARPS-Super-Ichimoku-v5) ·
[Super Ichimoku v4](https://github.com/ali-rajabpour/ARPS-Super-Ichimoku-v4) ·
[Zenith Ichimoku Framework](https://github.com/ali-rajabpour/ARPS-Zenith-Ichimoku-Framework) ·
[Ichimoku-Gann Hybrid](https://github.com/ali-rajabpour/ARPS-Ichimoku-Gann-Hybrid-Indicator)

**Market structure and smart money**

[ICT Smart Money Assistant](https://github.com/ali-rajabpour/ARPS-ICT-Smart-Money-Assistant) ·
[OB Scalp](https://github.com/ali-rajabpour/ARPS-OB-Scalp) ·
[Multidimensional Trend & Pivot Alerts](https://github.com/ali-rajabpour/ARPS-Multidimensional-Trend-Pivot-Alerts) ·
[Pivots](https://github.com/ali-rajabpour/ARPS-Pivots)

**Scalping and intraday**

[Scalp Suite](https://github.com/ali-rajabpour/ARPS-Scalp-Suite) ·
[Scalp Strategy](https://github.com/ali-rajabpour/ARPS-Scalp-Strategy) ·
[Scalp Short Indicator](https://github.com/ali-rajabpour/ARPS-Scalp-Short-Indicator) ·
[Ultra Scalper](https://github.com/ali-rajabpour/ARPS-Ultra-Scalper) ·
[FastScalping](https://github.com/ali-rajabpour/ARPS-FastScalping-Indicator) ·
[RSI-MA Scalping](https://github.com/ali-rajabpour/ARPS-RSI-MA-Scalping-Strategy) ·
[Intraday Signal](https://github.com/ali-rajabpour/ARPS-Intraday-Signal)

**Multi-signal frameworks**

[Ultimate Signal Framework](https://github.com/ali-rajabpour/ARPS-Ultimate-Signal-Framework-USF) ·
[Ultimate MultiStrategy Trading](https://github.com/ali-rajabpour/ARPS-Ultimate-MultiStrategy-Trading) ·
[Ultimate Trading Solution A-6H](https://github.com/ali-rajabpour/ARPS-Ultimate-Trading-Solution-A-6H) ·
[Ult Solution A 30m](https://github.com/ali-rajabpour/ARPS-Ult-Solution-A-30m-pinev5) ·
[Ultimate Advanced Trade Toolkit](https://github.com/ali-rajabpour/ARPS-Ultimate-Advanced-Trade-Toolkit-Alert) ·
[OmniFusion Technical Suite](https://github.com/ali-rajabpour/ARPS-OmniFusion-Technical-Suite) ·
[Convergent Pro V5](https://github.com/ali-rajabpour/ARPS-Convergent-Pro-V5) ·
[Long Term Strategy](https://github.com/ali-rajabpour/ARPS-Long-Term-Strategy)

**Oscillators, filters, divergence**

[Advanced Synergistic Oscillators & Filters](https://github.com/ali-rajabpour/ARPS-Advanced-Synergistic-Oscillators-Filters) ·
[Stochastic Alligator Divergence System](https://github.com/ali-rajabpour/ARPS-Stochastic-Alligator-Divergence-System-SADS) ·
[ZEMA Cross](https://github.com/ali-rajabpour/ARPS-ZEMA-Cross)

**Tables and execution helpers**

[MACD + ATR Table](https://github.com/ali-rajabpour/ARPS-MACD-ATR-Table) ·
[Info Table](https://github.com/ali-rajabpour/ARPS-info-Table) ·
[Stoploss Indicator](https://github.com/ali-rajabpour/ARPS-Stoploss-Indicator) ·
[Candlestick Patterns](https://github.com/ali-rajabpour/ARPS-Candlestick-Patterns)

**MetaTrader 5, private**

Forex SuperIchi, a multi-timeframe Ichimoku expert advisor, and FCR, a First Candle Rule breakout system. Both trade live on prop firm and retail accounts, and share the strategy layer with Phoenix.

---

### Tools

Python, TypeScript, Rust, MQL5, Solidity, PHP, Shell · FastAPI, Flask, Next.js, React, Vue, Laravel · PostgreSQL, MySQL, SQLite, Redis, Kafka · Docker, Traefik, Nginx, Dokploy, Tailscale, Debian/Ubuntu · pandas, NumPy, Jupyter, SPSS

---

<details>
<summary><b>Forks I work in</b></summary>

<br>

[telemt](https://github.com/ali-rajabpour/telemt) (Rust MTProto proxy) ·
[freqtrade](https://github.com/ali-rajabpour/freqtrade) ·
[s-ui](https://github.com/ali-rajabpour/s-ui) and [s-ui-frontend](https://github.com/ali-rajabpour/s-ui-frontend) (sing-box panel) ·
[tgcf](https://github.com/ali-rajabpour/tgcf) (Telegram forwarding) ·
[github-readme-stats](https://github.com/ali-rajabpour/github-readme-stats)

</details>
