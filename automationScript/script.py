import requests
import os
import subprocess

# Step 1: Fetch accepted submissions using Codeforces API
def get_accepted_submissions(user_handle):
    url = f"https://codeforces.com/api/user.status?handle={user_handle}"
    response = requests.get(url)
    submissions = response.json()

    if submissions['status'] == 'OK':
        # Filter for accepted submissions
        accepted = [
            submission for submission in submissions['result']
            if submission['verdict'] == 'OK'
        ]
        return accepted
    return []

# Step 2: Save accepted submissions to a local directory
def save_submissions(submissions, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for submission in submissions:
        problem_name = submission['problem']['name'].replace(' ', '_')
        contest_id = submission['contestId']
        index = submission['problem']['index']
        file_path = os.path.join(directory, f"{contest_id}_{index}_{problem_name}.py")
        
        # Only save if the file does not already exist
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as file:
                file.write(f"// {submission['programmingLanguage']}\n")
                file.write(submission.get('source', ''))

# Step 3: Commit changes to GitHub
def commit_and_push_to_github(repo_path):
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add new accepted submissions"])
    subprocess.run(["git", "push", "origin", "main"])  # Change 'main' to your branch name if different

# User inputs
user_handle = "abrish28"
local_repo_path = "C:\\codeforce submissions"
submissions_directory = os.path.join(local_repo_path, "submissions")

# Main logic
accepted_submissions = get_accepted_submissions(user_handle)
save_submissions(accepted_submissions, submissions_directory)
commit_and_push_to_github(local_repo_path)
