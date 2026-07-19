# Dataset Reproducibility Matrix

Last verified: **2026-07-18**

## Result

TrendSpider's public Market Data Library lists **27 data families** when “Bring Your Own Data” is excluded.

| Classification | Count | Meaning |
|---|---:|---|
| Direct/useful free substitute | 11 | Same primary public source or a close public reconstruction is practical |
| Free approximation | 8 | Useful MVP coverage is possible, but not the same breadth, latency, history, or rights |
| Paid/permissioned for useful parity | 8 | Free sources are too incomplete, fragile, restricted, or delayed for practical parity |
| **Total** | **27** | |

Therefore, **19 of 27 are available or reproducible online for free at some useful fidelity**, but only **11 of 27** are strong enough to call direct/useful free substitutes. A production-quality parity claim would still require paid data for many of the remaining families and may require licensing even for some “free” inputs when used commercially.

## Matrix

Legend: **Free-direct**, **Free-approx**, **Paid/permissioned**.

| # | TrendSpider family | Stated source / cadence | Classification | Candidate replacement | Parity caveat |
|---:|---|---|---|---|---|
| 1 | Listed equities | NYSE/Nasdaq/AMEX/NBBO; real time | Free-approx | Free brokerage/API tiers or delayed/EOD provider | IEX-only or delayed data is not consolidated SIP/NBBO; commercial display/redistribution rights vary. |
| 2 | US options | OPRA; real time | Paid/permissioned | Licensed OPRA vendor | Free pages or brokerage accounts do not provide a redistributable 1.5M-contract real-time/historical feed. |
| 3 | Listed ETFs | US exchange feeds; real time | Free-approx | Same delayed/EOD provider as equities | Price coverage is easy; full real-time consolidated coverage, reference data, and adjustments are licensed. |
| 4 | OTC & Pink Sheets | Nasdaq; delayed | Paid/permissioned | OTC Markets or licensed vendor | Public quote pages exist, but broad bulk history and production rights are not reliably free. |
| 5 | Futures | CME/NYMEX/COMEX/CBOT; real time | Paid/permissioned | Licensed CME vendor | Real-time and redistribution require exchange entitlements; free web quotes are delayed and unsuitable as a bulk feed. |
| 6 | CBOE indices | CBOE; delayed | Free-approx | Public delayed index pages, FRED/Stooq subsets | A useful subset is accessible, not the full licensed 200+ symbol history and methodology set. |
| 7 | Crypto digital assets | 100+ exchanges; real time | Free-direct | Coinbase, Kraken, Gemini and other exchange REST/WebSocket APIs; CoinGecko for normalized metadata | Near-parity is feasible for selected venues; 100+ venue normalization, symbol mapping, and history still require engineering. |
| 8 | Foreign exchange | 19+ banks; real time | Free-approx | ECB reference rates plus free-tier FX/broker APIs | ECB is reference-rate data, not a 3,200-pair institutional real-time composite. |
| 9 | Stock-market news | Benzinga; real time | Free-approx | SEC current filings, issuer RSS, GDELT, licensed publisher RSS | Different editorial content, entity tagging, speed, and redistribution rights; do not scrape publisher pages. |
| 10 | Corporate press releases | Benzinga; real time | Free-direct | Issuer IR feeds/sites, SEC 8-K/6-K, exchange/company feeds | Aggregation and issuer coverage are work, but the underlying announcements are generally public. |
| 11 | Crypto-market news | Industry news; real time | Free-approx | Publisher RSS, GDELT, project/exchange announcements | Coverage, licensing, deduplication, and real-time speed differ. |
| 12 | Federal Reserve Economic Data | Federal Reserve/FRED; real time | Free-direct | Official FRED/ALFRED API | Strong match. Respect each series' source notes and revisions. |
| 13 | Corporate fundamentals & financials | Benzinga/SimFin; daily | Free-direct | SEC EDGAR Company Facts/XBRL; SimFin free tier where permitted | US filers are strong; taxonomy normalization, restatements, non-US issuers, calculated metrics, and point-in-time history require care. |
| 14 | Analyst estimates | Benzinga; daily | Paid/permissioned | Benzinga, FactSet, LSEG, S&P/Capital IQ, Intrinio, Finnhub/FMP paid tiers | Broad historical consensus, broker actions, and estimate revisions are proprietary; public snippets are not a stable dataset. |
| 15 | Insider trading | Benzinga/Intrinio/SEC; daily | Free-direct | SEC Forms 3/4/5 and submissions API | Strong primary-source reconstruction; requires XML parsing, amendments, ownership codes, and issuer mapping. |
| 16 | Unusual options flow | Benzinga; real time | Paid/permissioned | Licensed OPRA trades plus an independently defined classifier, or a paid flow API | Both the underlying trade feed and high-quality sweep/block/aggressor inference are unavailable free at parity. |
| 17 | House & Senate member trading | Quiver Quant; daily | Free-direct | House Clerk and Senate eFD public disclosures | Primary documents are public, but PDFs/ranges, amendments, delays, entity mapping, and terms for commercial use require care. |
| 18 | Crypto Fear & Greed | Alternative.me; real time | Free-direct | Alternative.me API | Same named source is publicly reachable; comply with attribution and usage terms. |
| 19 | Reg SHO short volume/interest | FINRA; daily | Free-direct | FINRA files and Query API | Strong match for published aggregates. Short volume is not short interest; preserve definitions and venue coverage. |
| 20 | Corporate events | Benzinga; daily | Free-direct | SEC filings, issuer calendars, exchange calendars, corporate actions from the selected price provider | Splits/dividends are reconstructible; future earnings dates and estimates are less reliable and may change. |
| 21 | WallStreetBets mentions/sentiment | Quiver Quant; real time | Free-approx | Reddit's approved Data API or licensed third party, with an independent ticker/sentiment pipeline | API access and commercial use are permission/terms dependent; deleted content and history limit parity. Avoid scraping. |
| 22 | Retail trading activity | Nasdaq; real time | Paid/permissioned | Nasdaq Data Link/product license or a separately licensed retail-flow vendor | “Retail” is a vendor classification, not derivable reliably from ordinary consolidated trades. |
| 23 | Dark-pool/ATS volume | FINRA; daily | Free-direct | FINRA OTC Transparency ATS/non-ATS downloads/API | Strong source match for delayed aggregates, not real-time dark-pool prints. FINRA delays weekly security/venue publications. |
| 24 | Nasdaq Global Indexes | Nasdaq; real time | Paid/permissioned | Nasdaq Global Index Data Service or selected public substitutes | A few headline indexes are public/delayed; 47,000+ real-time symbols and history are licensed. |
| 25 | Market breadth | TrendSpider-derived; daily | Free-approx | Derive advances/declines, highs/lows, above-moving-average counts from licensed/free price universe | Formulae are reproducible; exact parity requires identical universe history, sessions, constituent membership, adjustments, and definitions. |
| 26 | Government trading data | Quiver Quant; daily | Free-direct | House Clerk and Senate eFD disclosures | Appears substantially overlapping with the Congressional-trading family; reproduce from primary filings and document the chosen semantics. |
| 27 | StockTwits social mentions | StockTwits; daily | Paid/permissioned | Authorized StockTwits API/data agreement or licensed social-data vendor | Public posts do not imply stable bulk API, history, commercial analysis, or redistribution rights. |

## Count methodology

- “Free” means no mandatory data subscription for a small legal prototype, not unlimited commercial redistribution.
- A public webpage is not automatically a permitted bulk dataset.
- Free API tiers can change and may prohibit display, caching, redistribution, or commercial use.
- `Free-approx` never supports a claim of real-time or universe parity.
- Two catalog entries—House & Senate Member Trading and Government Trading Data—appear highly overlapping. They are counted separately because TrendSpider catalogs them separately.
- `Bring Your Own Data` is an ingestion capability, not a TrendSpider-supplied dataset, and is excluded from the denominator.

## Recommended MVP subset

Start with these sources because they are authoritative and tractable:

1. SEC EDGAR submissions, filings, Company Facts/XBRL, and Forms 3/4/5
2. FRED/ALFRED macro series
3. FINRA short-sale volume and OTC/ATS transparency aggregates
4. issuer press releases and corporate-event disclosures
5. selected exchange crypto APIs
6. a documented delayed/EOD US-equity provider

Defer OPRA, futures, analyst estimates, unusual options, retail activity, broad Nasdaq indexes, and production social feeds until licensing and product economics are approved.
