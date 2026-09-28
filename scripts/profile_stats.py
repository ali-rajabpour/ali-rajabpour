#!/usr/bin/env python3
"""Regenerate the activity block in README.md from the GitHub API.

Counts work in private repositories too, but only ever prints aggregates and
the project names listed in DOMAINS below - never a private repo's contents.

Usage: GH_TOKEN=<pat> python3 scripts/profile_stats.py [--check]
"""

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone

USER = "ali-rajabpour"
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
START, END = "<!-- stats:start -->", "<!-- stats:end -->"
FIRST_YEAR = 2019

# repo name -> domain. First matching prefix wins, so order matters.
# Client repos are named under NDA, so their prefixes live in the DOMAIN_MAP
# secret instead of here. Without it they just fall through to OTHER.
DOMAINS = [
    ("Healthcare", ("Phoenix-EMR", "OmanEMR", "MedResearchHub", "MedLitHarvester", "ResearchDataCleaner")),
    ("Trading systems", ("Phoenix", "phoenix", "ARPS", "MT5", "freqtrade", "metatrader", "tradingview", "Leverage", "TradingView")),
    ("Networking / infra", ("telemt", "gost-", "dokploy-", "Personal-DoH", "s-ui", "ServerMGMT", "Amnezia")),
    ("Blockchain", ("TRC20", "BEP20", "QURC", "MultiBC")),
]
if os.environ.get("DOMAIN_MAP"):
    DOMAINS = [(k, tuple(v)) for k, v in json.loads(os.environ["DOMAIN_MAP"])] + DOMAINS
OTHER = "Tooling / other"

# {"org-login": ["Display name", "What the work is"]}, from the ORG_LABELS secret.
# Only orgs listed here are shown; anything else is counted in the totals but
# never named, which is what keeps client orgs off a public page.
ORGS = json.loads(os.environ.get("ORG_LABELS") or "{}")

# Languages that are noise in a summary (config, generated, or vendored).
LANG_SKIP = {"Batchfile", "Makefile", "Roff", "Procfile", "Smarty"}

# Badge colors for the headline strip: teal marks the primary signal (commit
# volume), amber marks PRs (a different kind of contribution than raw
# commits), slate is the baseline reading for everything else.
BADGE_ACCENT, BADGE_HIGHLIGHT, BADGE_NEUTRAL = "12a594", "b8842f", "414a5a"


def badge(label, message, color):
    q = urllib.parse.urlencode(
        {"label": label, "message": message, "color": color, "style": "flat-square"},
        quote_via=urllib.parse.quote,
    )
    return f"![{label}](https://img.shields.io/static/v1?{q})"


def request(url, method="GET", data=None, accept="application/vnd.github+json"):
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is not set")
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", accept)
    req.add_header("User-Agent", "profile-stats")
    if data is not None:
        req.data = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    # Secondary rate limits show up as 403/429 and clear on their own.
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 429, 502, 504) and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 3:
                time.sleep(3)
                continue
            raise


def graphql(query, variables):
    out = request("https://api.github.com/graphql", "POST", {"query": query, "variables": variables})
    if "errors" in out:
        raise RuntimeError(out["errors"])
    return out["data"]


CONTRIB_QUERY = """
query($from:DateTime!,$to:DateTime!){
  viewer{
    contributionsCollection(from:$from,to:$to){
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar{totalContributions}
      commitContributionsByRepository(maxRepositories:100){
        repository{name nameWithOwner isPrivate owner{login}}
        contributions{totalCount}
      }
    }
  }
}"""


def domain_of(name):
    for domain, prefixes in DOMAINS:
        if name.startswith(prefixes):
            return domain
    return OTHER


def collect():
    now = datetime.now(timezone.utc)
    years, commits_by_repo = {}, {}
    totals = Counter()

    for year in range(FIRST_YEAR, now.year + 1):
        data = graphql(CONTRIB_QUERY, {"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        c = data["viewer"]["contributionsCollection"]
        years[year] = {
            "commits": c["totalCommitContributions"],
            "prs": c["totalPullRequestContributions"],
            "total": c["contributionCalendar"]["totalContributions"],
            "repos": sum(1 for e in c["commitContributionsByRepository"] if e["contributions"]["totalCount"]),
        }
        totals["commits"] += c["totalCommitContributions"]
        totals["prs"] += c["totalPullRequestContributions"]
        totals["contributions"] += c["contributionCalendar"]["totalContributions"]
        for entry in c["commitContributionsByRepository"]:
            repo = entry["repository"]
            rec = commits_by_repo.setdefault(
                repo["nameWithOwner"],
                {"n": 0, "private": repo["isPrivate"], "name": repo["name"], "owner": repo["owner"]["login"]},
            )
            rec["n"] += entry["contributions"]["totalCount"]

    repos = []
    for page in range(1, 6):
        batch = request(
            "https://api.github.com/user/repos?per_page=100&page=%d&affiliation=owner,collaborator,organization_member" % page
        )
        repos += batch
        if len(batch) < 100:
            break

    langs = Counter()
    for repo in repos:
        if repo["fork"]:
            continue
        for lang, size in (request("https://api.github.com/repos/%s/languages" % repo["full_name"]) or {}).items():
            if lang not in LANG_SKIP:
                langs[lang] += size

    def search(q):
        out = request("https://api.github.com/search/issues?per_page=1&advanced_search=true&q=" + urllib.parse.quote(q))
        time.sleep(2)  # search API has its own, much lower rate limit
        return out["total_count"]

    return {
        "generated": now.strftime("%d %b %Y"),
        "years": years,
        "totals": totals,
        "commits_by_repo": commits_by_repo,
        "langs": langs,
        "repos": repos,
        "merged_prs": search(f"type:pr author:{USER} is:merged"),
        "external_prs": search(f"type:pr author:{USER} -user:{USER}"),
    }


def render(d):
    owned = [r for r in d["repos"] if r["owner"]["login"] == USER and not r["fork"]]
    private = sum(1 for r in owned if r["private"])
    forks = sum(1 for r in d["repos"] if r["owner"]["login"] == USER and r["fork"])
    active_year = max(d["years"])
    lang_total = sum(d["langs"].values()) or 1
    top_langs = [(k, v / lang_total * 100) for k, v in d["langs"].most_common(8)]

    org_commits = Counter()
    for rec in d["commits_by_repo"].values():
        org_commits[rec["owner"]] += rec["n"]
    orgs = []
    for login, (label, focus) in ORGS.items():
        repos = [r for r in d["repos"] if r["owner"]["login"] == login]
        orgs.append((label, len(repos), sum(1 for r in repos if r["private"]), org_commits.get(login, 0), focus))
    orgs.sort(key=lambda o: o[3], reverse=True)

    domains = Counter()
    domain_private = {}
    for full, rec in d["commits_by_repo"].items():
        dom = domain_of(rec["name"])
        domains[dom] += rec["n"]
        domain_private.setdefault(dom, [True, False])
        domain_private[dom][1 if rec["private"] else 0] = True
    commit_total = sum(domains.values()) or 1

    badges = [
        badge("Commits", f"{d['totals']['commits']:,}", BADGE_ACCENT),
        badge("Contributions", f"{d['totals']['contributions']:,}", BADGE_NEUTRAL),
        badge("PRs merged", str(d["merged_prs"]), BADGE_HIGHLIGHT),
        badge("Repositories", str(len(owned)), BADGE_NEUTRAL),
    ]
    if orgs:
        badges.append(badge("Organizations", str(len(orgs)), BADGE_NEUTRAL))

    lines = [START, "", " ".join(badges), ""]
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append(f"| Commits, all repositories | **{d['totals']['commits']:,}** ({d['years'][active_year]['commits']:,} in {active_year}) |")
    lines.append(f"| Contributions, all time | **{d['totals']['contributions']:,}** |")
    lines.append(f"| Pull requests merged | **{d['merged_prs']}** ({d['external_prs']} to repositories I don't own) |")
    lines.append(f"| Repositories | **{len(owned)}** ({private} private) |")
    lines.append(f"| Forks maintained | **{forks}** |")
    lines.append(f"| Repositories touched in {active_year} | **{d['years'][active_year]['repos']}** |")
    if orgs:
        org_repos = sum(o[1] for o in orgs)
        lines.append(f"| Organizations | **{len(orgs)}** ({org_repos} further repositories, {sum(o[3] for o in orgs):,} commits) |")
    lines.append("")
    if orgs:
        lines.append("**Organizations I build in**")
        lines.append("")
        lines.append("| Organization | Repositories | Commits | Work |")
        lines.append("|---|---|--:|---|")
        for label, n_repos, n_private, commits, focus in orgs:
            count = f"{n_repos} private" if n_private == n_repos else f"{n_repos} ({n_private} private)"
            lines.append(f"| {label} | {count} | {commits:,} | {focus} |")
        lines.append("")
    lines.append("**Where the commits go**")
    lines.append("")
    lines.append("| Area | Share | Visibility |")
    lines.append("|---|--:|---|")
    for dom, n in domains.most_common():
        pub, priv = domain_private[dom]
        vis = "public + private" if (pub and priv) else ("private" if priv else "public")
        lines.append(f"| {dom} | {n / commit_total * 100:.0f}% | {vis} |")
    lines.append("")
    lines.append("**Languages by volume** (source bytes across public and private repositories)")
    lines.append("")
    lines.append("| Language | Share | |")
    lines.append("|---|--:|---|")
    for lang, pct in top_langs:
        # One cell per 2.5%, so the smallest listed language still shows something.
        bar = "█" * max(1, round(pct / 2.5))
        lines.append(f"| {lang} | {pct:.1f}% | `{bar}` |")
    lines.append("")
    lines.append(f"<sub>Generated {d['generated']} by [`scripts/profile_stats.py`](scripts/profile_stats.py). "
                 "Private repositories are counted, never named beyond the list below.</sub>")
    lines.append("")
    lines.append(END)
    return "\n".join(lines)


def main():
    path = os.path.abspath(README)
    old = open(path, encoding="utf-8").read()
    if START not in old or END not in old:
        sys.exit("markers %s / %s not found in README.md" % (START, END))
    block = render(collect())
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, old, flags=re.S)
    if "--check" in sys.argv:
        print("changed" if new != old else "unchanged")
        return
    if new != old:
        open(path, "w", encoding="utf-8").write(new)
    print("README.md " + ("updated" if new != old else "already current"))


if __name__ == "__main__":
    main()
