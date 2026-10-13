# Install your refreshed GitHub profile

Target repository: https://github.com/Sharique-shaikh-git/Sharique-shaikh-git

1. Extract the ZIP. Copy `README.md`, `assets/`, `scripts/`, and `.github/` into the root of that repository. Keep the folder structure, including `.github/workflows/profile-stats.yml`.
2. Commit these files to the default branch. The workflow runs when its script or workflow file is pushed.
3. In the repository's **Actions** tab, enable workflows if GitHub prompts you. Select **Refresh profile stats → Run workflow** to refresh immediately.
4. Check that the run succeeds. It then refreshes daily at approximately **07:17 Pakistan time**. Scheduled runs can be delayed by GitHub.

No personal access token, external stats server, Python package install, or subscription is needed. The workflow uses GitHub's automatically supplied repository token. The included stats card is a real API snapshot made when the package was created; the workflow replaces it with fresh data.

If the final commit step is blocked by repository or organization rules, permit Actions to write repository contents, or adapt the workflow to open a pull request under those rules. Do not disable branch protection just for this feature.

## What updates automatically

- Public repository count, including public forks, from the user profile API.
- Stars and forks received across owned, non-fork public repositories.
- Follower count.
- Language distribution by bytes across owned, non-fork public repositories. Archived repositories remain included. The five largest languages are shown individually; the rest are combined as Other.
- The last successful refresh date, in UTC.

Counts and percentages are fetched or calculated; none are hand-entered. Your identity, project descriptions, skills, and links are editorial content and remain intentionally editable. The username is inferred from the repository owner when Actions runs.

Private repositories are excluded, even though much of your work is private. The default repository token cannot read all your other private repositories. There are no invented commit counts, streaks, ranking scores, skill percentages, or visitor numbers. GitHub already displays your contribution graph below the README.

Stats are a daily snapshot, not a real-time feed. GitHub image caching can briefly delay a visible update. If an API request fails, the workflow fails and preserves the last successful SVG. GitHub may disable scheduled workflows in public repositories after prolonged inactivity; re-enable the workflow in Actions if that occurs.

## Local refresh (optional)

From the repository root, with Python 3.10 or newer:

```bash
GH_USERNAME=Sharique-shaikh-git python scripts/update_stats.py
```

PowerShell:

```powershell
$env:GH_USERNAME = "Sharique-shaikh-git"
python scripts/update_stats.py
```

An optional `GH_TOKEN` environment variable raises the API rate limit. Never commit a token.

## Design and research

The design uses an original charcoal-and-sage SVG header, compact navigation, specific project descriptions, and a matching statistics panel. SVGs are stored in the repository so the main visuals do not depend on public image-generator services. Tech badges use Shields.io.

Research references:

- https://github.com/abhisheknaiidu/awesome-github-profile-readme — profile examples covering minimal, dynamic, and Actions-based approaches.
- https://github.com/anuraghazra/github-readme-stats — the original service is marked unmaintained and recommends its successor or Actions-generated cards; its public endpoint is described as best-effort.
- https://github.com/stats-organization/github-readme-stats-action — repository-hosted SVG generation with GitHub Actions.
- https://docs.github.com/en/rest/users/users#get-a-user — live account data.
- https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user — repository data and pagination.
- https://docs.github.com/en/rest/repos/repos#list-repository-languages — language byte counts.
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule — schedule behavior and inactivity limits.

Validation: the custom generator was run against the public API; SVG XML, local image references, workflow YAML, and ZIP contents were checked. The hosted Actions run has not been executed because this package is supplied for you to install.
