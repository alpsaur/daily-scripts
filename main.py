#!/usr/bin/env python3
import os
import random
from datetime import datetime, timedelta

# Configuration
start_date = datetime(2024, 6, 25)
num_days = 30  # Total days to backfill
max_commits_per_day = 20  # Maximum commits per day

# Probability settings for realistic GitHub activity
zero_commit_probability = 0.7  # 70% chance of 0 commits (like real developers!)
low_commit_probability = 0.25   # 25% chance of 1-3 commits  
high_commit_probability = 0.05  # 5% chance of 4+ commits

# Remove existing file if it exists
if os.path.exists("backfill.txt"):
    os.remove("backfill.txt")

def get_realistic_commit_count():
    """Generate realistic commit counts with heavy bias toward 0"""
    rand = random.random()
    
    if rand < zero_commit_probability:
        return 0
    elif rand < zero_commit_probability + low_commit_probability:
        # 1-3 commits
        return random.randint(1, 3)
    else:
        # 4-20 commits (rare productive days)
        return random.randint(4, max_commits_per_day)

total_commits = 0

for day in range(num_days):
    # Calculate base date for this day
    base_date = start_date + timedelta(days=day)
    
    # Generate realistic number of commits for this day
    commits_today = get_realistic_commit_count()
    total_commits += commits_today
    
    print(f"Day {day + 1}: {commits_today} commits")
    
    # Skip days with 0 commits
    if commits_today == 0:
        continue
    
    # Create commits for this day
    for commit in range(commits_today):
        # Generate random time within the day (0-86399 seconds)
        seconds_in_day = random.randint(0, 86399)
        commit_time = base_date + timedelta(seconds=seconds_in_day)
        iso_date = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Create a dummy file
        with open("backfill.txt", "a") as f:
            f.write(f"Backfill commit for {iso_date}\n")
        
        # Stage the file
        os.system("git add backfill.txt")
        
        # Generate realistic commit messages
        commit_messages = [
            "Update utility functions",
            "Fix minor bug in script",
            "Add error handling",
            "Improve logging output", 
            "Refactor helper methods",
            "Update documentation",
            "Add input validation",
            "Optimize performance",
            "Clean up code",
            "Add new feature",
            "Fix edge case",
            "Update dependencies",
            "Improve error messages",
            "Add unit tests",
            "Fix formatting issues"
        ]
        
        message = random.choice(commit_messages)
        os.system(f'git commit --date="{iso_date}" -m "{message}"')

print(f"\nTotal commits created: {total_commits}")
print(f"Average commits per day: {total_commits/num_days:.1f}")

# Ask before pushing (safety feature!)
push_confirm = input("\nPush to GitHub? (y/N): ").lower().strip()
if push_confirm == 'y':
    os.system("git push origin main")
    print("Pushed to GitHub!")
else:
    print("Not pushed. You can manually push later with: git push origin main")
