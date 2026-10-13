# Install the redesigned profile

Repository: https://github.com/Sharique-shaikh-git/Sharique-shaikh-git

1. Extract the ZIP and upload `README.md`, `assets/`, `scripts/`, and `.github/` into the root of the profile repository. Preserve the folder structure.
2. Commit to the default branch. The new workflow will run when its file or script is added.
3. In Actions, select **Refresh public workspace → Run workflow** to refresh manually if needed.

If the earlier package is already installed, remove `.github/workflows/profile-stats.yml` from that repository so the old stats workflow no longer runs. The old `assets/github-stats.svg` and `scripts/update_stats.py` are no longer referenced and can also be removed. These files remain recoverable in Git history.

## What changed

- Broader Software & AI Engineer positioning, with six equal areas: web applications, mobile applications, AI, automation, business software, and custom engineering.
- CRMs, ERP modules, internal tools, and operational workflows are explicitly included as services. The profile does not invent completed CRM or ERP case studies.
- Trading appears only as one additional specialist capability, not as the main niche.
- Original navy, ivory, and blue visual design, with a new editorial header and delivery strip.
- No follower, star, fork, ranking, or repository-count panel.
- No code-language percentage chart. React, Next.js, Flutter, and other frameworks are explicitly listed in the curated toolkit rather than inferred from GitHub language bytes.
- A daily public-project feed replaces the stats panel. It displays the three most recently pushed eligible public repositories, their actual GitHub descriptions, links, and push dates. Forks, archived repositories, empty repositories, and the profile repository itself are excluded.

## Automatic updates

The feed pulls real data from GitHub's REST API. It uses the built-in GITHUB_TOKEN and needs no separate secret, installed Python package, or subscription. The schedule is approximately 07:17 Pakistan time each day; GitHub may delay scheduled runs. The refresh date is UTC.

The included feed is an API-derived snapshot created during this revision. Repository descriptions are displayed as data, not endorsements or verified claims. Edit a repository's About description on GitHub to improve its entry; the next successful refresh will pick it up.

Only the section between `PUBLIC-WORK` markers is automated. The rest of the README remains your editorial content. Private repository names, descriptions, and activity are not published. GitHub's native contribution graph remains available below your profile README.

If a request fails, the script leaves the previous README unchanged. If branch rules block workflow commits, follow your repository's permitted review process rather than disabling protections. Scheduled workflows can be disabled by GitHub after prolonged repository inactivity; re-enable them in Actions if needed.

The hosted workflow has not been run by the author of this package; it begins after you install it.
