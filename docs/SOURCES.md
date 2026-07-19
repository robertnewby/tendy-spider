# Evidence and Source Ledger

Last checked: **2026-07-18**

This ledger favors platform/vendor documentation for claims about TrendSpider and primary government/exchange sources for replacement data. Product pages establish what TrendSpider claims; they do not independently validate accuracy or performance.

## TrendSpider capability and coverage sources

- [Global Market Data Coverage Library](https://trendspider.com/marketdata/) — the 27 supplied data families, depths, cadences, and vendor names; excludes “Bring Your Own Data” from the audit denominator.
- [Market Data Sources help article](https://help.trendspider.com/kb/data-feeds/market-data-sources) — supported asset classes, real-time/delayed status, OPRA and futures add-on notes, and exchange families.
- [Introducing Sidekick Deep Research](https://trendspider.com/blog/introducing-sidekick-deep-research/) — per-symbol sub-chats, parent synthesis, and main-chat actions.
- [TC2000 comparison](https://trendspider.com/learning-center/tc2000-alternative/) — vendor description of chart context, model providers, multi-step agent actions, scanners, backtests, and data vendors.
- [TipRanks comparison](https://trendspider.com/learning-center/tipranks-alternative/) — vendor description of filings, transcripts, analyst/insider/Congressional data, charts, watchlists, and alternative-data access.

### Individual catalog pages

- [Listed equities](https://trendspider.com/marketdata/listed-equities/)
- [Options](https://trendspider.com/marketdata/options-data/)
- [OTC and Pink Sheets](https://trendspider.com/marketdata/otc-and-pink-sheets/)
- [Futures](https://trendspider.com/marketdata/futures-data/)
- [CBOE indices](https://trendspider.com/marketdata/indices/)
- [Crypto assets](https://trendspider.com/marketdata/crypto-digital-assets/)
- [Foreign exchange](https://trendspider.com/marketdata/foreign-exchange/)
- [Stock-market news](https://trendspider.com/marketdata/stock-market-news/)
- [Corporate press releases](https://trendspider.com/marketdata/corporate-press-releases/)
- [Crypto news](https://trendspider.com/marketdata/crypto-market-news/)
- [FRED](https://trendspider.com/marketdata/federal-reserve-economic-data/)
- [Corporate fundamentals](https://trendspider.com/marketdata/corporate-fundamentals-financials/)
- [Analyst estimates](https://trendspider.com/marketdata/analyst-estimates/)
- [Insider trading](https://trendspider.com/marketdata/insider-trading/)
- [Unusual options flow](https://trendspider.com/marketdata/unusual-options-flow/)
- [House and Senate trading](https://trendspider.com/marketdata/house-senate-member-trading/)
- [Crypto Fear and Greed](https://trendspider.com/marketdata/crypto-fear-greed/)
- [Reg SHO](https://trendspider.com/marketdata/reg-sho/)
- [Corporate events](https://trendspider.com/marketdata/corporate-events/)
- [WallStreetBets mentions](https://trendspider.com/marketdata/wall-street-bets-social-mentions/)
- [Retail trading activity](https://trendspider.com/marketdata/retail-trading-activity/)
- [Dark-pool/ATS volume](https://trendspider.com/marketdata/dark-pool-ats-volume/)
- [Nasdaq Global Indexes](https://trendspider.com/marketdata/nasdaq-global-indexes/)
- [Market breadth](https://trendspider.com/marketdata/market-breadth-data/)
- [Government trading](https://trendspider.com/marketdata/government-trades/)
- [StockTwits mentions](https://trendspider.com/marketdata/stocktwits-social-mentions/)

The catalog also separately labels listed ETFs; its linked page did not return usable text during this audit, so the matrix treats the family using the main catalog and US-equities feed description.

## Primary free/public replacement sources

### SEC EDGAR

- [EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) — submissions and extracted XBRL/company facts.
- [SEC developer resources and fair-access guidance](https://www.sec.gov/about/developer-resources)
- [SEC data API host](https://data.sec.gov/)

Use for filings, reported fundamentals, filing-derived corporate events, and Forms 3/4/5 insider disclosures. Supply a compliant User-Agent and obey current fair-access guidance.

### FRED and ALFRED

- [FRED API overview](https://fred.stlouisfed.org/docs/api/fred/overview.html)

ALFRED vintages matter for point-in-time backtests because macro observations are revised.

### FINRA

- [Daily short-sale volume files](https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data/daily-short-sale-volume-files)
- [Short-sale volume catalog and Query API](https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data)
- [Equity short-interest data](https://www.finra.org/finra-data/browse-catalog/equity-short-interest/data)
- [OTC/ATS and non-ATS transparency](https://www.finra.org/filing-reporting/otc-transparency)
- [OTC transparency API description](https://www.finra.org/sites/default/files/OTC-Transparency-Data-File-Download-API-v04.pdf)

FINRA short-sale volume, short interest, and ATS volume are different datasets with different definitions and publication schedules. Do not merge them under one label.

### Congressional disclosures

- [House Clerk financial disclosures](https://disclosures-clerk.house.gov/FinancialDisclosure)
- [House disclosure search](https://disclosures-clerk.house.gov/FinancialDisclosure/ViewSearch)
- [Senate electronic financial disclosure search](https://efdsearch.senate.gov/search/)

The primary disclosures are public, but they contain value ranges, can be delayed/amended, and require entity/ticker normalization. Review statutory and site restrictions before commercial use.

### Crypto and FX

- [Coinbase Exchange API](https://docs.cdp.coinbase.com/exchange/docs/welcome)
- [Kraken Spot REST API](https://docs.kraken.com/api/docs/rest-api/get-ohlc-data/)
- [CoinGecko API documentation](https://docs.coingecko.com/)
- [ECB data services](https://data.ecb.europa.eu/help/api/overview)
- [Alternative.me Fear and Greed API](https://alternative.me/crypto/fear-and-greed-index/)

Exchange APIs are venue-specific. ECB data is not a replacement for an institutional real-time FX composite.

### News and public documents

- [GDELT project](https://www.gdeltproject.org/)
- issuer investor-relations feeds and official newsroom pages
- SEC current filings and 8-K/6-K submissions

Public availability does not grant unrestricted republication. Store URLs and permitted metadata when full-text rights are unclear.

## License checks still required

Before enabling any live provider in a shared or commercial environment, record:

- source and contractual account type;
- personal/non-professional/professional classification;
- display and derived-use rights;
- storage, caching, history, and deletion rules;
- redistribution and model-training restrictions;
- rate and concurrency limits;
- geographic restrictions;
- attribution requirements;
- termination/export behavior.

Provider pricing and free-tier terms change frequently. Recheck official provider terms at implementation time rather than treating this ledger as a contract summary.
