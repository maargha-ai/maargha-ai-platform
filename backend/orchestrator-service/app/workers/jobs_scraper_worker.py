# app/workers/job_scraper_worker.py
import random
import time

from playwright.sync_api import sync_playwright

SITES = ["Indeed", "Naukri", "Internshala", "LinkedIn"]


def scrape_site(page, site_name, query, location):
    jobs = []

    try:
        print(f"Scraping {site_name}...", end=" ")

        if site_name == "Indeed":
            # Fixed URL: Exact phrase + recent jobs param to boost results & reduce caching
            base_query = query.replace(" ", "+")
            encoded_query = f"%22{base_query}%22"  # Exact "Data Science" match
            location_plus = location.replace(" ", "+")
            url = (
                "https://in.indeed.com/jobs?"
                f"q={encoded_query}&l={location_plus}&fromage=7"
            )
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(random.randint(3000, 5000))  # Random human pause
            # Enhanced scrolling: 3 gradual scrolls to load ~20-30 jobs
            for i in range(3):
                page.evaluate(f"window.scrollBy(0, {800 * (i + 1)})")
                page.wait_for_timeout(random.randint(1500, 3000))
            # === PRIORITY SELECTORS (Dec 2025 - India Layout) ===
            cards = page.query_selector_all('li[data-testid="jobsearch-JobCard"]')
            # Fallback 1: Grid item wrapper (common in mosaic view)
            if not cards:
                cards = page.query_selector_all('div[data-testid="job-container"]')
            # Fallback 2: Legacy with data-jk (still ~10% of pages)
            if not cards:
                cards = page.query_selector_all("div[data-jk]")
            # Fallback 3: Broad beacon (for beacon-tracked jobs)
            if not cards:
                cards = page.query_selector_all("div.job_seen_beacon")
            print(f"({len(cards)} cards found)", end=" -> ")
            success_count = 0
            for card in cards[:30]:  # Cap at 30 to avoid overload
                try:
                    # === Title (Multi-fallback) ===
                    title = "N/A"
                    title_elem = card.query_selector(
                        '[data-testid="jobTitle"] span[title]'
                    )
                    if title_elem:
                        title = title_elem.get_attribute("title")
                    else:
                        title_elem = card.query_selector("h2 a span[title]")
                        if title_elem:
                            title = (
                                title_elem.get_attribute("title")
                                or title_elem.inner_text()
                            )
                    # === Company ===
                    company = "N/A"
                    company_elem = card.query_selector('[data-testid="company-name"]')
                    if company_elem:
                        company = company_elem.inner_text()
                    else:
                        company_elem = card.query_selector("span.companyName")
                        if company_elem:
                            company = company_elem.inner_text()
                    # === Link ===
                    link = ""
                    link_elem = card.query_selector("a[data-jk]")
                    if link_elem:
                        href = link_elem.get_attribute("href")
                        link = (
                            f"https://in.indeed.com{href}"
                            if href and href.startswith("/")
                            else href
                        )
                    else:
                        link_elem = card.query_selector("h2 a")
                        if link_elem:
                            href = link_elem.get_attribute("href")
                            link = (
                                f"https://in.indeed.com{href}"
                                if href and href.startswith("/")
                                else href
                            )
                    # === Description ===
                    desc = ""
                    desc_elem = card.query_selector(
                        '[data-testid="jobsearch-JobCard-description"]'
                    )
                    if desc_elem:
                        desc = desc_elem.inner_text()
                    else:
                        desc_elems = card.query_selector_all(
                            'div[data-testid="jobsearch-JobCard-reqSnippet"] li'
                        )
                        desc_parts = []
                        for li in desc_elems[:3]:  # Top 3 bullets
                            text = li.inner_text()
                            if text:
                                desc_parts.append(text)
                        desc = " - ".join(desc_parts)
                    if title != "N/A" and link and "indeed" in link:
                        jobs.append(
                            {
                                "title": title.strip(),
                                "company": company.strip(),
                                "link": link,
                                "desc": (
                                    (desc.strip()[:400] + "...")
                                    if len(desc) > 400
                                    else desc.strip()
                                ),  # Truncate
                                "source": "Indeed",
                            }
                        )
                        success_count += 1
                except Exception:
                    continue  # Skip broken cards
            print(f"Success: {success_count} jobs")
            if success_count == 0:
                print(
                    "Debug: Check console for page errors or try without quotes "
                    "in query."
                )

        elif site_name == "Naukri":
            query_slug = query.replace(" ", "-")
            location_slug = location.replace(" ", "-")
            url = f"https://www.naukri.com/{query_slug}-jobs-in-{location_slug}"
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(5000)
            try:
                page.click("span.nI-gNb-icon-close", timeout=2000)
            except Exception:
                pass
            for _ in range(3):
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                page.wait_for_timeout(1500)
            cards = page.query_selector_all(".cust-job-tuple")
            print(f"({len(cards)} cards found)", end=" -> ")
            for card in cards[:20]:
                try:
                    title_elem = card.query_selector("a.title")
                    title = title_elem.inner_text() if title_elem else "N/A"
                    company_elem = card.query_selector("a.subTitle, span.comp-name")
                    company = company_elem.inner_text() if company_elem else "N/A"
                    link = title_elem.get_attribute("href") if title_elem else ""
                    desc_elem = card.query_selector(".job-desc")
                    desc = desc_elem.inner_text() if desc_elem else ""
                    if title != "N/A" and link:
                        jobs.append(
                            {
                                "title": title.strip(),
                                "company": company.strip(),
                                "link": link,
                                "desc": desc.strip(),
                                "source": "Naukri",
                            }
                        )
                except Exception:
                    continue
            print(f"Success: {len(jobs)} jobs")

        elif site_name == "Internshala":
            url = f"https://internshala.com/jobs/{query.replace(' ', '-')}-jobs/"
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(4000)
            cards = page.query_selector_all(".internship_meta")
            print(f"({len(cards)} cards found)", end=" -> ")
            for card in cards[:25]:
                try:
                    title_elem = card.query_selector("a[href*='/job/detail']")
                    title = title_elem.inner_text() if title_elem else "N/A"
                    company_elem = card.query_selector(".company-name")
                    company = company_elem.inner_text() if company_elem else "N/A"
                    link_elem = card.query_selector("a[href*='/job/detail']")
                    link = (
                        "https://internshala.com" + link_elem.get_attribute("href")
                        if link_elem
                        else ""
                    )
                    desc_elem = card.query_selector(".internship-details")
                    desc = desc_elem.inner_text() if desc_elem else ""
                    if title != "N/A" and link:
                        jobs.append(
                            {
                                "title": title.strip(),
                                "company": company.strip(),
                                "link": link,
                                "desc": desc.strip(),
                                "source": "Internshala",
                            }
                        )
                except Exception:
                    continue
            print(f"Success: {len(jobs)} jobs")

        elif site_name == "LinkedIn":
            query_encoded = query.replace(" ", "%20")
            url = (
                "https://www.linkedin.com/jobs/search?"
                f"keywords={query_encoded}&location={location}"
            )
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(8000)
            cards = page.query_selector_all(
                ".base-card, .jobs-search-results__list-item"
            )
            print(f"({len(cards)} cards found)", end=" -> ")
            for card in cards[:20]:
                try:
                    title_elem = card.query_selector("h3.base-search-card__title")
                    title = title_elem.inner_text() if title_elem else "N/A"
                    company_elem = card.query_selector(".base-search-card__subtitle")
                    company = company_elem.inner_text() if company_elem else "N/A"
                    link_elem = card.query_selector("a.base-card__full-link")
                    link = link_elem.get_attribute("href") if link_elem else ""
                    if title != "N/A" and link:
                        jobs.append(
                            {
                                "title": title.strip(),
                                "company": company.strip(),
                                "link": link.split("?")[0],
                                "desc": "",
                                "source": "LinkedIn",
                            }
                        )
                except Exception:
                    continue
            print(f"Success: {len(jobs)} jobs")

    except Exception as e:
        print(f"Failed: {str(e)[:60]}")

    return jobs


def scrape_jobs_sync(query: str, location: str, max_jobs: int = 200):
    all_jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1920, "height": 1080},
            locale="en-IN",
        )

        page = context.new_page()

        context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(
                navigator,
                'languages',
                { get: () => ['en-US', 'en'] }
            );
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            """
        )

        for site in SITES:
            jobs = scrape_site(page, site, query, location)
            all_jobs.extend(jobs)

            if len(all_jobs) >= max_jobs:
                break

            time.sleep(2)

        browser.close()

    return all_jobs[:max_jobs]
