#!/usr/bin/env python3
"""
Script to scan GitHub repositories for abandoned projects.
Analyzes repository activity and creates a markdown report.
"""

import requests
import json
from datetime import datetime, timedelta
import argparse
import sys

class GitHubRepoScanner:
    def __init__(self, username, token=None):
        self.username = username
        self.token = token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Scanner'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
        
        self.base_url = 'https://api.github.com'
        
    def get_repositories(self):
        """Fetch all public repositories for the user."""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.base_url}/users/{self.username}/repos"
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated',
                'direction': 'desc'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                print(response.text)
                break
            
            page_repos = response.json()
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
        return repos
    
    def get_repository_details(self, repo_name):
        """Get detailed information about a repository."""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_recent_commits(self, repo_name, since_days=365):
        """Get recent commits from the repository."""
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/commits"
        params = {
            'since': since_date,
            'per_page': 100
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_issues_and_prs(self, repo_name):
        """Get recent issues and pull requests."""
        issues_url = f"{self.base_url}/repos/{self.username}/{repo_name}/issues"
        params = {'state': 'all', 'per_page': 100}
        
        response = requests.get(issues_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def analyze_repository(self, repo):
        """Analyze a repository to determine if it's abandoned."""
        repo_name = repo['name']
        created_date = datetime.strptime(repo['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        updated_date = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        pushed_date = None
        if repo['pushed_at']:
            pushed_date = datetime.strptime(repo['pushed_at'], '%Y-%m-%dT%H:%M:%SZ')
        
        now = datetime.now()
        days_since_update = (now - updated_date).days
        days_since_push = (now - pushed_date).days if pushed_date else float('inf')
        days_since_creation = (now - created_date).days
        
        # Get additional details
        recent_commits = self.get_recent_commits(repo_name, 365)
        issues_and_prs = self.get_issues_and_prs(repo_name)
        
        # Count recent activity
        recent_issues = [i for i in issues_and_prs if 'pull_request' not in i]
        recent_prs = [i for i in issues_and_prs if 'pull_request' in i]
        
        # Analyze abandonment criteria
        abandonment_reasons = []
        is_abandoned = False
        
        # Primary criteria for abandonment
        if days_since_push > 730:  # 2 years without commits
            abandonment_reasons.append(f"No commits in {days_since_push} days (over 2 years)")
            is_abandoned = True
        elif days_since_push > 365 and len(recent_commits) == 0:  # 1 year without commits
            abandonment_reasons.append(f"No commits in {days_since_push} days (over 1 year)")
            is_abandoned = True
        
        # Additional indicators
        if repo['archived']:
            abandonment_reasons.append("Repository is archived")
            is_abandoned = True
        
        if days_since_creation > 30 and repo['size'] < 10:  # Very small repo, likely empty or minimal
            abandonment_reasons.append("Repository appears to be empty or minimal content")
            is_abandoned = True
        
        # Open issues without recent activity
        old_open_issues = [i for i in recent_issues if i['state'] == 'open']
        if len(old_open_issues) > 5 and days_since_push > 180:
            abandonment_reasons.append(f"{len(old_open_issues)} unresolved issues with no recent commits")
            is_abandoned = True
        
        # Low activity indicators (not necessarily abandoned, but worth noting)
        activity_notes = []
        if days_since_push > 180 and days_since_push <= 365:
            activity_notes.append(f"No commits in {days_since_push} days (6+ months)")
        
        if repo['stargazers_count'] == 0 and repo['forks_count'] == 0 and days_since_creation > 90:
            activity_notes.append("No stars or forks after 3+ months")
        
        if not repo.get('has_readme', False) or not repo['description']:
            activity_notes.append("Missing README or description")
        
        return {
            'name': repo_name,
            'url': repo['html_url'],
            'description': repo['description'] or 'No description',
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'pushed_at': repo['pushed_at'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'language': repo['language'],
            'size': repo['size'],
            'archived': repo['archived'],
            'days_since_update': days_since_update,
            'days_since_push': days_since_push,
            'days_since_creation': days_since_creation,
            'recent_commits_count': len(recent_commits),
            'open_issues_count': len([i for i in recent_issues if i['state'] == 'open']),
            'is_abandoned': is_abandoned,
            'abandonment_reasons': abandonment_reasons,
            'activity_notes': activity_notes
        }
    
    def generate_markdown_report(self, analyses, output_file='abandoned_repositories.md'):
        """Generate a markdown report of the analysis."""
        abandoned_repos = [a for a in analyses if a['is_abandoned']]
        inactive_repos = [a for a in analyses if not a['is_abandoned'] and a['activity_notes']]
        active_repos = [a for a in analyses if not a['is_abandoned'] and not a['activity_notes']]
        
        report = f"""# GitHub Repository Analysis for {self.username}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total repositories analyzed**: {len(analyses)}
- **Abandoned repositories**: {len(abandoned_repos)}
- **Inactive repositories**: {len(inactive_repos)}
- **Active repositories**: {len(active_repos)}

---

"""
        
        if abandoned_repos:
            report += "## 🚫 Abandoned Repositories\n\n"
            report += "These repositories show clear signs of abandonment:\n\n"
            
            for repo in sorted(abandoned_repos, key=lambda x: x['days_since_push'], reverse=True):
                report += f"### [{repo['name']}]({repo['url']})\n\n"
                report += f"**Description**: {repo['description']}\n\n"
                report += f"**Details**:\n"
                report += f"- Language: {repo['language'] or 'Not specified'}\n"
                report += f"- Created: {repo['created_at'][:10]}\n"
                report += f"- Last push: {repo['pushed_at'][:10] if repo['pushed_at'] else 'Never'}\n"
                report += f"- Stars: {repo['stars']} | Forks: {repo['forks']}\n"
                report += f"- Days since last push: {repo['days_since_push']}\n"
                if repo['archived']:
                    report += f"- Status: 🗄️ **Archived**\n"
                report += f"\n**Reasons for abandonment**:\n"
                for reason in repo['abandonment_reasons']:
                    report += f"- {reason}\n"
                report += "\n---\n\n"
        
        if inactive_repos:
            report += "## ⚠️ Inactive Repositories\n\n"
            report += "These repositories show signs of reduced activity but may not be fully abandoned:\n\n"
            
            for repo in sorted(inactive_repos, key=lambda x: x['days_since_push'], reverse=True):
                report += f"### [{repo['name']}]({repo['url']})\n\n"
                report += f"**Description**: {repo['description']}\n\n"
                report += f"**Details**:\n"
                report += f"- Language: {repo['language'] or 'Not specified'}\n"
                report += f"- Created: {repo['created_at'][:10]}\n"
                report += f"- Last push: {repo['pushed_at'][:10] if repo['pushed_at'] else 'Never'}\n"
                report += f"- Stars: {repo['stars']} | Forks: {repo['forks']}\n"
                report += f"- Days since last push: {repo['days_since_push']}\n"
                report += f"\n**Activity concerns**:\n"
                for note in repo['activity_notes']:
                    report += f"- {note}\n"
                report += "\n---\n\n"
        
        report += "## 📊 Repository Statistics\n\n"
        report += "| Repository | Language | Stars | Forks | Days Since Push | Status |\n"
        report += "|------------|----------|-------|-------|-----------------|--------|\n"
        
        for repo in sorted(analyses, key=lambda x: x['days_since_push'], reverse=True):
            status = "🚫 Abandoned" if repo['is_abandoned'] else ("⚠️ Inactive" if repo['activity_notes'] else "✅ Active")
            if repo['archived']:
                status += " (🗄️ Archived)"
            
            report += f"| [{repo['name']}]({repo['url']}) | {repo['language'] or 'N/A'} | {repo['stars']} | {repo['forks']} | {repo['days_since_push']} | {status} |\n"
        
        report += f"\n\n---\n\n*Report generated by GitHub Repository Scanner*"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Scan GitHub repositories for abandoned projects')
    parser.add_argument('username', help='GitHub username to scan')
    parser.add_argument('--token', help='GitHub personal access token (optional, for higher rate limits)')
    parser.add_argument('--output', default='abandoned_repositories.md', help='Output markdown file')
    
    args = parser.parse_args()
    
    scanner = GitHubRepoScanner(args.username, args.token)
    
    print(f"Fetching repositories for {args.username}...")
    repositories = scanner.get_repositories()
    
    if not repositories:
        print("No repositories found or error fetching repositories.")
        return
    
    print(f"Found {len(repositories)} repositories. Analyzing...")
    
    analyses = []
    for i, repo in enumerate(repositories, 1):
        print(f"Analyzing {repo['name']} ({i}/{len(repositories)})...")
        analysis = scanner.analyze_repository(repo)
        analyses.append(analysis)
    
    print(f"Generating report: {args.output}")
    scanner.generate_markdown_report(analyses, args.output)
    
    abandoned_count = len([a for a in analyses if a['is_abandoned']])
    print(f"\nAnalysis complete!")
    print(f"- Total repositories: {len(analyses)}")
    print(f"- Abandoned repositories: {abandoned_count}")
    print(f"- Report saved to: {args.output}")

if __name__ == "__main__":
    main()
