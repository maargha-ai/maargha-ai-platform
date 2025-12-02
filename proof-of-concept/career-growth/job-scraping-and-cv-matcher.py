import asyncio, re, os
from playwright.async_api import async_playwright
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# List of sites to scrape (80%-90% coverage)
SITES = ["Indeed", "Naukri", "Internshala", "Glassdoor", "LinkedIn", "ZipRecruiter"]

async def scrape_jobs_from_site(page, site_name, query, location):
    jobs = []
    try:
        print(f"Scraping {site_name}...")

        if site_name == "Indeed":
            url = f"https://in.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)  # ← Changed
            await page.wait_for_timeout(5000)
            await page.wait_for_selector("ul.jobsearch-ResultsList", timeout=10000)
            cards = await page.query_selector_all("a[data-jk]")
            for card in cards[:25]:
                try:
                    title = await (await card.query_selector("h2 a span")).inner_text()
                    company = await (await card.query_selector(".companyName")).inner_text()
                    link = "https://in.indeed.com" + await (await card.query_selector("a")).get_attribute("href")
                    desc = await (await card.query_selector(".job-snippet")).inner_text() if await card.query_selector(".job-snippet") else ""
                    jobs.append({"title": title.strip(), "company": company.strip(), "link": link, "desc": desc.strip(), "source": "Indeed"})
                except: continue

        elif site_name == "Naukri":
            url = f"https://www.naukri.com/{query.replace(' ', '-')}-jobs"
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(4000)
            cards = await page.query_selector_all("article.jobTuple")
            for card in cards[:25]:
                title_elem = await card.query_selector("a.title")
                company_elem = await card.query_selector("a.subTitle")
                link_elem = await card.query_selector("a.title")
                desc_elem = await card.query_selector(".job-description")
                title = await title_elem.inner_text() if title_elem else "N/A"
                company = await company_elem.inner_text() if company_elem else "N/A"
                link = await link_elem.get_attribute("href") if link_elem else ""
                desc = await desc_elem.inner_text() if desc_elem else ""
                jobs.append({"title": title.strip(), "company": company.strip(), "link": link, "desc": desc.strip(), "source": site_name})

        elif site_name == "Internshala":
            url = f"https://internshala.com/jobs/{query.replace(' ', '-')}-jobs/"
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(4000)
            cards = await page.query_selector_all(".internship_meta")
            for card in cards[:25]:
                title_elem = await card.query_selector("a[href*='/job/detail']")
                company_elem = await card.query_selector(".company-name")
                link_elem = await card.query_selector("a[href*='/job/detail']")
                desc_elem = await card.query_selector(".internship-details")
                title = await title_elem.inner_text() if title_elem else "N/A"
                company = await company_elem.inner_text() if company_elem else "N/A"
                link = "https://internshala.com" + (await link_elem.get_attribute("href")) if link_elem else ""
                desc = await desc_elem.inner_text() if desc_elem else ""
                jobs.append({"title": title.strip(), "company": company.strip(), "link": link, "desc": desc.strip(), "source": site_name})

        elif site_name == "Glassdoor":
            url = f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={query.replace(' ', '%20')}"
            await page.goto(url, wait_until="networkidle", timeout=60000)
            await page.wait_for_timeout(4000)
            cards = await page.query_selector_all("li[data-test='job-listing']")
            for card in cards[:20]:
                title_elem = await card.query_selector("a.job-title")
                company_elem = await card.query_selector("a.employer-name")
                link_elem = await card.query_selector("a.job-title")
                desc_elem = await card.query_selector(".job-description")
                title = await title_elem.inner_text() if title_elem else "N/A"
                company = await company_elem.inner_text() if company_elem else "N/A"
                link = await link_elem.get_attribute("href") if link_elem else ""
                if link and not link.startswith("http"):
                    link = "https://www.glassdoor.co.in" + link
                desc = await desc_elem.inner_text() if desc_elem else ""
                jobs.append({"title": title.strip(), "company": company.strip(), "link": link, "desc": desc.strip(), "source": site_name})

        elif site_name == "LinkedIn":
            url = f"https://www.linkedin.com/jobs/search?keywords={query.replace(' ', '%20')}&location={location}"
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await page.wait_for_timeout(8000)
            await page.wait_for_selector(".jobs-search__results-list", timeout=15000)
            cards = await page.query_selector_all(".base-card")
            for card in cards[:20]:
                try:
                    title = await (await card.query_selector("h3")).inner_text()
                    company = await (await card.query_selector(".base-search-card__subtitle")).inner_text()
                    link = await (await card.query_selector("a")).get_attribute("href")
                    jobs.append({"title": title.strip(), "company": company.strip(), "link": link.split("?")[0], "desc": "", "source": "LinkedIn"})
                except: continue

        elif site_name == "ZipRecruiter":
            url = f"https://www.ziprecruiter.com/jobs/search?search={query.replace(' ', '+')}"
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await page.wait_for_timeout(6000)
            cards = await page.query_selector_all(".job_content")
            for card in cards[:20]:
                try:
                    title = await (await card.query_selector("h2 a")).inner_text()
                    company = await (await card.query_selector(".name")).inner_text()
                    link = "https://www.ziprecruiter.com" + await (await card.query_selector("a")).get_attribute("href")
                    jobs.append({"title": title.strip(), "company": company.strip(), "link": link, "desc": "", "source": "ZipRecruiter"})
                except: continue

            print(f" Got {len(jobs)} jobs from {site_name}")
    except Exception as e:
        print(f"Error on {site_name}: {e}")
    return jobs


async def scrape_all_jobs(query: str, location: str, max_jobs: int):
    all_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True
        )
        page = await context.new_page()

        for site in SITES:
            jobs = await scrape_jobs_from_site(page, site, query, location)
            all_jobs.extend(jobs)
            if len(all_jobs) >= max_jobs:
                break
            await page.wait_for_timeout(2000)

        await browser.close()
    return all_jobs


def extract_cv_text(path: str):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.lower()
    except Exception as e:
        print(f"CV Read Error: {e}")
        return ""
    

def match_and_rank(cv_text: str, jobs: list):
    if not cv_text or not jobs:
        return []
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=10000)
    try:
        texts = [cv_text] + [f"{j['title']} {j['company']}".lower() for j in jobs]
        matrix = vectorizer.fit_transform(texts)
        similarities = cosine_similarity(matrix[0:1], matrix[1:])[0]
        ranked = [(sim, job) for sim, job in zip(similarities, jobs)]
        ranked.sort(key=lambda x: x[0], reverse=True)
        return ranked[:50]
    except:
        return [(0.0, job) for job in jobs[:50]]
    

# Main
async def main():
    print("   JOB MATCHER   ")
    # cv_path = input("\nEnter your CV PDF path: ").strip().strip('"')
    # if not os.path.exists(cv_path):
    #     print("File not found!")
    #     return
    cv_path = "/MUHAMMED_SHAHAN_P_P_RESUME__Data_Scientist_ (1).pdf"

    cv_text = extract_cv_text(cv_path)
    if not cv_text:
        return
    
    query = input("\nEnter job title (e.g. Data Engineer, Python Developer, Intern): ").strip()
    location = input(f"\nSuggested role: {query}\nEnter location (e.g. Bangalore, Remote): ").strip() or ""

    print(f"\nScraping jobs for: '{query}' in '{location}'...")
    jobs = await scrape_all_jobs(query, location, max_jobs=400)

    if not jobs:
        print("No jobs found. Try different keywords.")
        return

    print(f"\nFound {len(jobs)} jobs. Matching to your CV...")
    ranked = match_and_rank(cv_text, jobs)

    print(f"\nTOP 50 BEST MATCHES FOR YOUR CV:")
    for i, (score, job) in enumerate(ranked, 1):
        print(f"{i:2}. [{job['source']:10}] {job['title'][:60]:60} at {job['company'][:30]:30}")
        print(f"     Match Score: {score:.3f} | Link → {job['link']}")
        print("-" * 100)


if __name__ == "__main__":
    asyncio.run(main())