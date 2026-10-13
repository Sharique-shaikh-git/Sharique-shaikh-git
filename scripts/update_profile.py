"""Refresh the public-project section; never publish private repository metadata."""
import json
import os
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


def fetch_repositories(username):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'profile-public-work'}
    if os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    repositories = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{quote(username, safe="")}/repos?per_page=100&type=owner&page={page}'
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            batch = json.load(response)
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return sorted(
        [r for r in repositories if not r['private'] and not r['fork']
         and not r['archived'] and r['name'].lower() != username.lower() and r['size'] > 0],
        key=lambda r: r.get('pushed_at') or '', reverse=True,
    )[:3]


def safe_text(text, limit=110):
    value = re.sub(r'\s+', ' ', text or '').strip()
    if len(value) > limit:
        value = value[:limit - 1].rstrip() + '…'
    # Encode raw Markdown as text so repository descriptions cannot change layout.
    return ''.join(f'&#{ord(c)};' if c in '|[]*_`\\' else escape(c) for c in value)


def section(repositories):
    rows = ['| Public project | Repository description | Last push (UTC) |', '| :--- | :--- | :--- |']
    for repository in repositories:
        name = safe_text(repository['name'], 55)
        description = safe_text(repository.get('description')) or 'Explore the repository for project details.'
        date = (repository.get('pushed_at') or '')[:10] or 'Not available'
        rows.append(f'| [{name}]({repository["html_url"]}) | {description} | {date} |')
    if not repositories:
        rows = ['Public project updates will appear here as repositories become available.']
    rows.append('\n<sub>Last refreshed: ' + datetime.now(timezone.utc).strftime('%Y-%m-%d UTC') + '</sub>')
    return '\n'.join(rows)


def main():
    username = os.environ.get('GH_USERNAME')
    if not username:
        raise SystemExit('Set GH_USERNAME to the account to display.')
    path = Path(__file__).resolve().parents[1] / 'README.md'
    old = path.read_text(encoding='utf-8')
    pattern = r'(?s)(<!-- PUBLIC-WORK:START -->).*?(<!-- PUBLIC-WORK:END -->)'
    if len(re.findall(pattern, old)) != 1:
        raise SystemExit('Expected exactly one public-work section; README left unchanged.')
    content = section(fetch_repositories(username))
    new = re.sub(pattern, lambda match: match[1] + '\n' + content + '\n' + match[2], old)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(new, encoding='utf-8')
    temporary.replace(path)
    print('Refreshed public-project feed.')


if __name__ == '__main__':
    main()
