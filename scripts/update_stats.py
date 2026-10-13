"""Render public GitHub data into a self-contained SVG. Python standard library only."""

import json
import os
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


def api(path):
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'github-profile-stats',
    }
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    request = Request('https://api.github.com' + path, headers=headers)
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)


def fetch_public(username):
    user = quote(username, safe='')
    profile = api('/users/' + user)
    repositories = []
    page = 1
    while True:
        batch = api(f'/users/{user}/repos?type=owner&per_page=100&page={page}')
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    # Public endpoint only. Do not publish private repo names, metadata, or languages.
    repositories = [r for r in repositories if not r['private']]
    originals = [r for r in repositories if not r['fork']]
    languages = Counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        paths = ['/repos/' + r['full_name'] + '/languages' for r in originals if r['size'] > 0]
        for result in pool.map(api, paths):
            languages.update(result)
    metrics = [
        ('PUBLIC REPOS', profile['public_repos']),
        ('STARS RECEIVED', sum(r['stargazers_count'] for r in originals)),
        ('FOLLOWERS', profile['followers']),
        ('REPO FORKS', sum(r['forks_count'] for r in originals)),
    ]
    return metrics, languages


def render(metrics, languages, updated):
    colors = ['#bfd5c5', '#a2b9cb', '#d9c4a4', '#bcadd2', '#d5a6a6', '#90bbb5']
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="342" viewBox="0 0 1000 342" role="img" aria-labelledby="title desc">',
        '<title id="title">Public GitHub statistics</title>',
        '<desc id="desc">' + escape('; '.join(f'{label}: {value}' for label, value in metrics)) + '. Languages are measured by code bytes across owned non-fork public repositories.</desc>',
        '<rect width="1000" height="342" rx="16" fill="#172122"/>',
        '<g font-family="DejaVu Sans, Arial, sans-serif">',
        '<text x="32" y="39" fill="#bfd5c5" font-size="12" letter-spacing="2">THE PUBLIC FOOTPRINT</text>',
        f'<text x="968" y="39" text-anchor="end" fill="#a0b4ac" font-size="11">UPDATED {escape(updated)}</text>',
    ]
    for index, (label, value) in enumerate(metrics):
        x = 32 + index * 244
        parts.extend([
            f'<text x="{x}" y="101" fill="#f4f1e9" font-size="38" font-weight="700">{value:,}</text>',
            f'<text x="{x}" y="131" fill="#a0b4ac" font-size="10" letter-spacing="1.5">{escape(label)}</text>',
        ])
    parts.extend([
        '<path d="M32 161H968" stroke="#354644"/>',
        '<text x="32" y="194" fill="#f4f1e9" font-size="13">Language distribution</text>',
    ])
    ranked = languages.most_common()
    groups = ranked[:5]
    if len(ranked) > 5:
        groups.append(('Other', sum(value for _, value in ranked[5:])))
    total = sum(languages.values())
    if total:
        x = 32
        for index, (name, value) in enumerate(groups):
            width = value / total * 936
            parts.append(f'<rect x="{x:.3f}" y="211" width="{width:.3f}" height="9" fill="{colors[index]}"/>')
            x += width
            lx = 32 + (index % 3) * 312
            ly = 254 + (index // 3) * 29
            parts.append(f'<circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{colors[index]}"/>')
            parts.append(f'<text x="{lx + 16}" y="{ly}" fill="#d4dcda" font-size="12">{escape(name)} {value / total:.1%}</text>')
    else:
        parts.append('<text x="32" y="247" fill="#a0b4ac" font-size="12">No language data available in public repositories.</text>')
    parts.extend([
        '<text x="32" y="319" fill="#a0b4ac" font-size="10">GitHub API · Public data only · Language bytes across owned non-fork repositories</text>',
        '</g></svg>',
    ])
    return '\n'.join(parts) + '\n'


def main():
    username = os.environ.get('GH_USERNAME')
    if not username:
        raise SystemExit('Set GH_USERNAME to the GitHub account to display.')
    metrics, languages = fetch_public(username)
    updated = datetime.now(timezone.utc).strftime('%Y-%m-%d UTC')
    output = Path(__file__).resolve().parents[1] / 'assets' / 'github-stats.svg'
    output.parent.mkdir(parents=True, exist_ok=True)
    # Fetch everything before replacing the previous successful card.
    temporary = output.with_suffix('.tmp')
    temporary.write_text(render(metrics, languages, updated), encoding='utf-8')
    temporary.replace(output)
    print('Updated public stats card.')


if __name__ == '__main__':
    main()
