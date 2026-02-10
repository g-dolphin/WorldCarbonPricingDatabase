from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
import pandas as pd
from bs4 import BeautifulSoup

RAW_ROOT = Path("_raw/sources")
SOURCES_PATH = RAW_ROOT / "sources.csv"
SEEDS_PATH = RAW_ROOT / "discovery_seeds.csv"
SEARCH_QUERIES_PATH = RAW_ROOT / "discovery_queries.csv"
OUT_PATH = RAW_ROOT / "discovery_candidates.csv"

YEAR_RE = re.compile(r"(20\d{2})")
KEYWORD_PHRASES = [
    # English
    "emissions trading",
    "emission trading",
    "cap-and-trade",
    "cap and trade",
    "cap-and-invest",
    "cap and invest",
    "carbon pricing",
    "carbon tax",
    "carbon pricing mechanism",
    "emission allowance",
    "emissions allowance",
    "auction",
    # French
    "échange de droits d'émission",
    "échange de droits d emission",
    "système d'échange de quotas d'émission",
    "systeme d'echange de quotas d'emission",
    "plafonnement et échange",
    "plafonnement et echange",
    "plafonnement et investissement",
    "tarification du carbone",
    "taxe carbone",
    "mécanisme de tarification du carbone",
    "mecanisme de tarification du carbone",
    "quota d'émission",
    "quota d emission",
    "enchère",
    "enchere",
    "mise aux enchères",
    "mise aux encheres",
    # Spanish
    "comercio de emisiones",
    "sistema de comercio de emisiones",
    "tope y comercio",
    "tope e inversión",
    "tope e inversion",
    "precio del carbono",
    "impuesto al carbono",
    "mecanismo de fijación del precio del carbono",
    "mecanismo de fijacion del precio del carbono",
    "permiso de emisión",
    "permiso de emision",
    "subasta",
    # Portuguese
    "comércio de emissões",
    "comercio de emissoes",
    "sistema de comércio de emissões",
    "sistema de comercio de emissoes",
    "limite e comércio",
    "limite e comercio",
    "teto e comércio",
    "teto e comercio",
    "limite e investimento",
    "teto e investimento",
    "precificação do carbono",
    "precificacao do carbono",
    "imposto sobre carbono",
    "imposto de carbono",
    "mecanismo de precificação do carbono",
    "mecanismo de precificacao do carbono",
    "licença de emissão",
    "licenca de emissao",
    "permissão de emissão",
    "permissao de emissao",
    "leilão",
    "leilao",
    # Russian
    "торговля выбросами",
    "система торговли выбросами",
    "ограничение и торговля",
    "ограничение и инвестиции",
    "ценообразование на углерод",
    "углеродный налог",
    "механизм ценообразования на углерод",
    "квота на выбросы",
    "аукцион",
    # Turkish
    "emisyon ticareti",
    "emisyon ticaret sistemi",
    "üst sınır ve ticaret",
    "ust sinir ve ticaret",
    "üst sınır ve yatırım",
    "ust sinir ve yatirim",
    "karbon fiyatlandırması",
    "karbon fiyatlandirmasi",
    "karbon vergisi",
    "karbon fiyatlandırma mekanizması",
    "karbon fiyatlandirma mekanizmasi",
    "emisyon izni",
    "açık artırma",
    "acik artirma",
    # Chinese
    "排放交易",
    "排放权交易",
    "碳排放交易",
    "总量控制与交易",
    "总量控制与投资",
    "碳定价",
    "碳税",
    "碳定价机制",
    "排放配额",
    "拍卖",
    # Japanese
    "排出量取引",
    "排出量取引制度",
    "キャップアンドトレード",
    "キャップ・アンド・トレード",
    "キャップアンドインベスト",
    "炭素価格付け",
    "炭素税",
    "炭素価格付けメカニズム",
    "排出枠",
    "オークション",
    # Korean
    "배출권거래",
    "배출권 거래제",
    "캡 앤 트레이드",
    "캡 앤 인베스트",
    "탄소가격",
    "탄소 가격제",
    "탄소세",
    "탄소가격제 메커니즘",
    "배출권",
    "경매",
]


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    for dash in ["–", "—", "‑", "−"]:
        text = text.replace(dash, "-")
    return text


def _get_jurisdiction(row: dict[str, str] | pd.Series) -> str:
    if isinstance(row, pd.Series):
        return str(row.get("jurisdiction", "") or row.get("jurisdiction_code", "")).strip()
    return str(row.get("jurisdiction", "") or row.get("jurisdiction_code", "")).strip()


KEYWORD_PHRASES_NORM = [_normalize_text(k) for k in KEYWORD_PHRASES]
LOG_SEED_EVERY = 25


@dataclass
class Seed:
    url: str
    jurisdiction_code: str
    instrument_id: str
    source_id: str
    seed_type: str


def _target_years_arg(value: str | None) -> list[str]:
    if value:
        years = [y.strip() for y in value.replace(";", ",").split(",") if y.strip()]
        return [y for y in years if y.isdigit() and len(y) == 4]
    current_year = dt.datetime.now(dt.timezone.utc).year
    return [str(current_year - 1), str(current_year)]


def _normalize_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url.strip()
    normalized = parsed._replace(fragment="").geturl()
    if normalized.endswith("/") and len(normalized) > len(parsed.scheme) + 3:
        normalized = normalized.rstrip("/")
    return normalized


def _domain_root(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return ""
    return f"{parsed.scheme}://{parsed.netloc}"


def _guess_year(text: str, target_years: list[str]) -> str:
    if not text:
        return ""
    years = YEAR_RE.findall(text)
    if not years:
        return ""
    if target_years:
        for y in years:
            if y in target_years:
                return y
        return ""
    return years[-1]


def _score_candidate(
    url: str,
    title: str,
    year_guess: str,
    target_years: list[str],
    text_hint: str = "",
) -> int:
    score = 0
    text = _normalize_text(f"{url} {title} {text_hint}")
    if year_guess and (not target_years or year_guess in target_years):
        score += 5
    if url.lower().endswith(".pdf"):
        score += 2
    if any(k in text for k in KEYWORD_PHRASES_NORM):
        score += 2
    return score


def _candidate_id(url: str, method: str) -> str:
    digest = hashlib.md5(url.encode("utf-8")).hexdigest()[:10]
    return f"{method}-{digest}"


def _log(message: str) -> None:
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    print(f"[{timestamp}] {message}")


def _matches_keywords(text: str) -> bool:
    normalized = _normalize_text(text)
    return any(k in normalized for k in KEYWORD_PHRASES_NORM)


def _extract_sitemap_locs(xml_bytes: bytes) -> tuple[list[str], bool]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return ([], False)
    tag = root.tag.lower()
    is_index = tag.endswith("sitemapindex")
    locs: list[str] = []
    for loc in root.findall(".//{*}loc"):
        if loc.text:
            locs.append(loc.text.strip())
    return (locs, is_index)


def _fetch_xml(client: httpx.Client, url: str) -> bytes:
    resp = client.get(url, follow_redirects=True)
    resp.raise_for_status()
    content = resp.content
    if url.lower().endswith(".gz"):
        return gzip.decompress(content)
    return content


def _discover_sitemaps(client: httpx.Client, base_url: str) -> list[str]:
    sitemaps: list[str] = []
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        resp = client.get(robots_url, follow_redirects=True)
        if resp.status_code < 400:
            for line in resp.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    sitemaps.append(line.split(":", 1)[1].strip())
    except Exception:
        pass
    if not sitemaps:
        sitemaps.append(urljoin(base_url, "/sitemap.xml"))
    return list(dict.fromkeys(sitemaps))


def _parse_sitemap(
    client: httpx.Client,
    sitemap_url: str,
    max_urls: int,
    depth: int = 0,
) -> list[str]:
    if depth > 2 or max_urls <= 0:
        return []
    try:
        xml_bytes = _fetch_xml(client, sitemap_url)
    except Exception:
        return []
    locs, is_index = _extract_sitemap_locs(xml_bytes)
    if not locs:
        return []
    urls: list[str] = []
    if is_index:
        for loc in locs:
            urls.extend(_parse_sitemap(client, loc, max_urls - len(urls), depth + 1))
            if len(urls) >= max_urls:
                break
        return urls[:max_urls]
    for loc in locs:
        urls.append(loc)
        if len(urls) >= max_urls:
            break
    return urls


def _extract_links_from_page(
    client: httpx.Client,
    page_url: str,
    max_links: int,
    same_domain: bool = True,
) -> list[tuple[str, str]]:
    try:
        resp = client.get(page_url, follow_redirects=True)
        resp.raise_for_status()
    except Exception:
        return []
    try:
        soup = BeautifulSoup(resp.text, "lxml")
    except Exception:
        soup = BeautifulSoup(resp.text, "html.parser")
    base_domain = urlparse(page_url).netloc
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for link in soup.find_all("a", href=True):
        href = link.get("href", "").strip()
        if not href:
            continue
        full_url = urljoin(page_url, href)
        if same_domain and urlparse(full_url).netloc != base_domain:
            continue
        if full_url in seen:
            continue
        seen.add(full_url)
        out.append((full_url, link.get_text(" ", strip=True)))
        if len(out) >= max_links:
            break
    return out


def _load_search_queries(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    queries: list[dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = str(row.get("query", "")).strip()
            if not query:
                continue
            queries.append(
                {
                    "query": query,
                    "jurisdiction_code": _get_jurisdiction(row),
                    "instrument_id": str(row.get("scheme_id", "") or row.get("instrument_id", "")).strip(),
                    "source_seed": str(row.get("source_seed", "")).strip(),
                    "year": str(row.get("year", "")).strip(),
                }
            )
    return queries


def _auto_search_queries(target_years: list[str]) -> list[dict[str, str]]:
    queries: list[dict[str, str]] = []
    years = target_years or [""]
    for year in years:
        for phrase in KEYWORD_PHRASES:
            if year:
                query = f"\"{phrase}\" {year}"
            else:
                query = f"\"{phrase}\""
            queries.append(
                {
                    "query": query,
                    "jurisdiction_code": "",
                    "instrument_id": "",
                    "source_seed": "auto",
                    "year": str(year),
                }
            )
    return queries


def _serpapi_search(
    client: httpx.Client,
    api_key: str,
    query: str,
    num_results: int,
    hl: str | None,
    gl: str | None,
) -> list[dict[str, str]]:
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    resp = client.get("https://serpapi.com/search.json", params=params)
    resp.raise_for_status()
    data = resp.json()
    results: list[dict[str, str]] = []
    for item in data.get("organic_results", []) or []:
        link = str(item.get("link", "")).strip()
        if not link:
            continue
        results.append(
            {
                "url": link,
                "title": str(item.get("title", "")).strip(),
                "snippet": str(item.get("snippet", "")).strip(),
            }
        )
    for item in data.get("news_results", []) or []:
        link = str(item.get("link", "")).strip()
        if not link:
            continue
        results.append(
            {
                "url": link,
                "title": str(item.get("title", "")).strip(),
                "snippet": str(item.get("snippet", "")).strip(),
            }
        )
    return results


def _load_sources(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str)


def _load_seeds(sources_df: pd.DataFrame, seed_path: Path) -> list[Seed]:
    seeds: list[Seed] = []
    if not sources_df.empty and "url" in sources_df.columns:
        for _, row in sources_df.iterrows():
            url = str(row.get("url", "")).strip()
            if not url:
                continue
            seeds.append(
                Seed(
                    url=url,
                    jurisdiction_code=_get_jurisdiction(row),
                    instrument_id=str(row.get("scheme_id", "") or row.get("instrument_id", "")).strip(),
                    source_id=str(row.get("source_id", "")).strip(),
                    seed_type="sources.csv",
                )
            )
    if seed_path.exists():
        with seed_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = str(row.get("seed_url", "") or row.get("url", "")).strip()
                if not url:
                    continue
                seeds.append(
                    Seed(
                        url=url,
                        jurisdiction_code=_get_jurisdiction(row),
                        instrument_id=str(row.get("scheme_id", "") or row.get("instrument_id", "")).strip(),
                        source_id=str(row.get("source_id", "")).strip(),
                        seed_type="discovery_seeds.csv",
                    )
                )
    return seeds


def run_discovery(
    sources_path: Path,
    out_path: Path,
    seed_path: Path,
    target_years: list[str],
    max_sitemap_urls: int,
    max_links_per_seed: int,
    max_candidates: int,
    include_sitemaps: bool,
    include_page_links: bool,
    verbose: bool,
    require_keywords: bool,
    search_provider: str | None,
    search_api_key: str | None,
    search_queries_path: Path,
    search_max_queries: int,
    search_results_per_query: int,
    search_hl: str | None,
    search_gl: str | None,
    search_use_auto: bool,
) -> None:
    log = _log if verbose else (lambda _msg: None)
    log("Discovery start")
    sources_df = _load_sources(sources_path)
    seeds = _load_seeds(sources_df, seed_path)
    existing_urls: set[str] = set()
    if not sources_df.empty and "url" in sources_df.columns:
        existing_urls = set(
            _normalize_url(str(u)) for u in sources_df["url"].tolist() if str(u).strip()
        )
    log(
        "Loaded sources="
        f"{len(sources_df)} seeds={len(seeds)} existing_urls={len(existing_urls)} "
        f"years={','.join(target_years) if target_years else 'all'}"
    )
    log(
        "Limits: "
        f"max_candidates={max_candidates} "
        f"max_sitemap_urls={max_sitemap_urls} "
        f"max_links_per_seed={max_links_per_seed}"
    )
    log(
        "Keyword filter: "
        f"{'on' if require_keywords else 'off'} "
        f"({len(KEYWORD_PHRASES)} phrases)"
    )
    if search_provider:
        log(
            "Search: "
            f"provider={search_provider} "
            f"max_queries={search_max_queries} "
            f"results_per_query={search_results_per_query} "
            f"auto_queries={'on' if search_use_auto else 'off'}"
        )

    candidates: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    def add_candidate(
        url: str,
        title: str,
        method: str,
        seed_url: str,
        jurisdiction_code: str,
        instrument_id: str,
        text_hint: str = "",
    ) -> None:
        if len(candidates) >= max_candidates:
            return
        normalized = _normalize_url(url)
        if not normalized or normalized in seen_urls or normalized in existing_urls:
            return
        text_blob = f"{url} {title} {text_hint}"
        if require_keywords and not _matches_keywords(text_blob):
            return
        year_guess = _guess_year(text_blob, target_years)
        if target_years and year_guess not in target_years:
            return
        score = _score_candidate(url, title, year_guess, target_years, text_hint)
        candidates.append(
            {
                "candidate_id": _candidate_id(url, method),
                "url": url,
                "title": title,
                "year_guess": year_guess,
                "jurisdiction_code": jurisdiction_code,
                "instrument_id": instrument_id,
                "doc_hint": "pdf" if url.lower().endswith(".pdf") else "html",
                "method": method,
                "source_seed": seed_url,
                "discovered_at": dt.datetime.now(dt.timezone.utc).isoformat(
                    timespec="seconds"
                ),
                "score": str(score),
            }
        )
        seen_urls.add(normalized)

    # Template-based candidates
    if not sources_df.empty and "year_url_template" in sources_df.columns:
        before = len(candidates)
        for _, row in sources_df.iterrows():
            template = str(row.get("year_url_template", "")).strip()
            if not template:
                continue
            for year in target_years:
                try:
                    url = template.format(year=year)
                except Exception:
                    continue
                add_candidate(
                    url=url,
                    title=str(row.get("title", "")).strip(),
                    method="year_template",
                    seed_url=str(row.get("source_id", "")).strip(),
                    jurisdiction_code=_get_jurisdiction(row),
                    instrument_id=str(row.get("instrument_id", "")).strip(),
                )
        log(f"Year templates added: {len(candidates) - before}")

    client = httpx.Client(timeout=30)

    # Sitemap-based candidates
    if include_sitemaps:
        seeds_by_domain: dict[str, list[Seed]] = {}
        for seed in seeds:
            root = _domain_root(seed.url)
            if not root:
                continue
            seeds_by_domain.setdefault(root, []).append(seed)

        log(f"Sitemap discovery: {len(seeds_by_domain)} domains")
        for domain, domain_seeds in seeds_by_domain.items():
            juris_values = {s.jurisdiction_code for s in domain_seeds if s.jurisdiction_code}
            inst_values = {s.instrument_id for s in domain_seeds if s.instrument_id}
            juris = juris_values.pop() if len(juris_values) == 1 else ""
            inst = inst_values.pop() if len(inst_values) == 1 else ""

            domain_start = len(candidates)
            sitemap_urls = _discover_sitemaps(client, domain)
            total_urls = 0
            log(f"Sitemap domain {domain}: {len(sitemap_urls)} sitemap(s)")
            for sitemap_url in sitemap_urls:
                urls = _parse_sitemap(client, sitemap_url, max_sitemap_urls)
                total_urls += len(urls)
                for loc in urls:
                    add_candidate(
                        url=loc,
                        title="",
                        method="sitemap",
                        seed_url=domain,
                        jurisdiction_code=juris,
                        instrument_id=inst,
                    )
                    if len(candidates) >= max_candidates:
                        break
                if len(candidates) >= max_candidates:
                    break
            log(
                f"Sitemap domain {domain}: {total_urls} urls, "
                f"{len(candidates) - domain_start} candidates"
            )
            if len(candidates) >= max_candidates:
                log("Max candidates reached during sitemap discovery.")
                break

    # Page-link candidates
    if include_page_links:
        log(f"Page-link discovery: {len(seeds)} seeds")
        for idx, seed in enumerate(seeds, start=1):
            seed_start = len(candidates)
            links = _extract_links_from_page(client, seed.url, max_links_per_seed)
            for link_url, link_text in links:
                add_candidate(
                    url=link_url,
                    title=link_text,
                    method="page_links",
                    seed_url=seed.url,
                    jurisdiction_code=seed.jurisdiction_code,
                    instrument_id=seed.instrument_id,
                )
                if len(candidates) >= max_candidates:
                    break
            if idx == 1 or idx % LOG_SEED_EVERY == 0 or idx == len(seeds):
                log(
                    f"Page-link seed {idx}/{len(seeds)}: "
                    f"{seed.url} -> {len(links)} links, "
                    f"{len(candidates) - seed_start} candidates"
                )
            if len(candidates) >= max_candidates:
                log("Max candidates reached during page-link discovery.")
                break

    # Search API candidates
    if search_provider:
        if not search_api_key:
            log("Search API key missing; skipping search channel.")
        elif search_provider.lower() != "serpapi":
            log(f"Search provider '{search_provider}' not supported; skipping.")
        else:
            base_queries = _load_search_queries(search_queries_path)
            if search_use_auto or not base_queries:
                base_queries += _auto_search_queries(target_years)

            # De-duplicate queries while preserving order
            seen_queries: set[str] = set()
            queries: list[dict[str, str]] = []
            for q in base_queries:
                qtext = q.get("query", "").strip()
                if not qtext or qtext in seen_queries:
                    continue
                seen_queries.add(qtext)
                queries.append(q)

            if search_max_queries > 0:
                queries = queries[:search_max_queries]

            log(f"Search discovery: {len(queries)} queries")
            for idx, q in enumerate(queries, start=1):
                if len(candidates) >= max_candidates:
                    log("Max candidates reached during search discovery.")
                    break
                query = q.get("query", "")
                try:
                    results = _serpapi_search(
                        client=client,
                        api_key=search_api_key,
                        query=query,
                        num_results=search_results_per_query,
                        hl=search_hl,
                        gl=search_gl,
                    )
                except Exception as exc:  # noqa: BLE001
                    log(f"Search query failed: {query} ({exc})")
                    continue

                added_before = len(candidates)
                for item in results:
                    add_candidate(
                        url=item.get("url", ""),
                        title=item.get("title", ""),
                        method="serpapi",
                        seed_url=q.get("source_seed") or query,
                        jurisdiction_code=q.get("jurisdiction_code", ""),
                        instrument_id=q.get("instrument_id", ""),
                        text_hint=f"{item.get('snippet', '')} {query}",
                    )
                    if len(candidates) >= max_candidates:
                        break

                if idx == 1 or idx % 10 == 0 or idx == len(queries):
                    log(
                        f"Search query {idx}/{len(queries)}: "
                        f"{len(results)} results, "
                        f"{len(candidates) - added_before} candidates"
                    )

    client.close()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "candidate_id",
        "url",
        "title",
        "year_guess",
        "jurisdiction_code",
        "instrument_id",
        "doc_hint",
        "method",
        "source_seed",
        "discovered_at",
        "score",
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in candidates:
            writer.writerow(row)
    log(f"Wrote {len(candidates)} candidates to {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default=str(SOURCES_PATH))
    parser.add_argument("--out", default=str(OUT_PATH))
    parser.add_argument("--seed-file", default=str(SEEDS_PATH))
    parser.add_argument("--search-queries-file", default=str(SEARCH_QUERIES_PATH))
    parser.add_argument(
        "--years",
        help="Comma-separated years to target (default: current year and previous).",
    )
    parser.add_argument("--max-sitemap-urls", type=int, default=500)
    parser.add_argument("--max-links-per-seed", type=int, default=200)
    parser.add_argument("--max-candidates", type=int, default=2000)
    parser.add_argument("--no-sitemaps", action="store_true")
    parser.add_argument("--no-page-links", action="store_true")
    parser.add_argument(
        "--no-keyword-filter",
        action="store_true",
        help="Disable keyword filtering (useful for broad discovery).",
    )
    parser.add_argument(
        "--search-provider",
        choices=["serpapi"],
        help="Optional search API provider (enables API search channel).",
    )
    parser.add_argument(
        "--serpapi-key",
        default=os.environ.get("SERPAPI_KEY", ""),
        help="SerpAPI key (or set SERPAPI_KEY env var).",
    )
    parser.add_argument("--search-max-queries", type=int, default=50)
    parser.add_argument("--search-results-per-query", type=int, default=10)
    parser.add_argument("--search-hl", default="")
    parser.add_argument("--search-gl", default="")
    parser.add_argument(
        "--search-no-auto",
        action="store_true",
        help="Disable auto-generated search queries.",
    )
    parser.add_argument("--quiet", action="store_true", help="Disable progress logs")
    args = parser.parse_args()

    target_years = _target_years_arg(args.years)
    run_discovery(
        sources_path=Path(args.sources),
        out_path=Path(args.out),
        seed_path=Path(args.seed_file),
        target_years=target_years,
        max_sitemap_urls=args.max_sitemap_urls,
        max_links_per_seed=args.max_links_per_seed,
        max_candidates=args.max_candidates,
        include_sitemaps=not args.no_sitemaps,
        include_page_links=not args.no_page_links,
        verbose=not args.quiet,
        require_keywords=not args.no_keyword_filter,
        search_provider=args.search_provider,
        search_api_key=args.serpapi_key,
        search_queries_path=Path(args.search_queries_file),
        search_max_queries=args.search_max_queries,
        search_results_per_query=args.search_results_per_query,
        search_hl=args.search_hl or None,
        search_gl=args.search_gl or None,
        search_use_auto=not args.search_no_auto,
    )


if __name__ == "__main__":
    main()
