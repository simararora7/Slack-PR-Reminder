import os
import sys
import re

import requests
from github import Github

POST_URL = 'https://slack.com/api/chat.postMessage'
APPROVED_REGEX = '^(Approved|:shipit:|:\+1:|LGTM|theek_hai_bhai_theek_hai|THBTH|done_done|DD|:goat:|:fire:|:heart_eyes:)'
NON_REVIEWABLE_LABELS = ['wip', 'on-hold']

try:
    REPOSITORY = os.environ['REPOSITORY']
    GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']
    SLACK_API_TOKEN = os.environ['SLACK_API_TOKEN']
    SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
except KeyError as error:
    sys.stderr.write('Please set the environment variable {0}'.format(error))
    sys.exit(1)

INITIAL_MESSAGE = """\
Hi! There are a few open pull requests you should take a \
look at:

"""

def fetch_repo(client):
    for repo in client.get_user().get_repos():
        if repo.name == REPOSITORY:
            return repo

def is_open(pull):
    return pull.state == 'open'

def is_reviewable(pull):
    for label in pull.labels:
        if label.name in NON_REVIEWABLE_LABELS:
            return False
    return True

def is_approved(pull):
    for review in pull.get_reviews():
        if review.state == 'APPROVED':
            return True

    for comment in pull.get_issue_comments():
        matches = re.findall(APPROVED_REGEX, comment.body)
        if matches:
            return True

    return False

def is_valid_pull(pull):
    return is_open(pull) and is_reviewable(pull) and not is_approved(pull)

def fetch_pulls(repo):
    pulls = []
    for pull in repo.get_pulls():
        if is_valid_pull(pull):
            pulls.append(pull)
    return pulls

def format_pulls(pulls):
    message = INITIAL_MESSAGE
    for pull in pulls:
        line = '<{0}|{1}> - {2}\n'.format(pull.html_url, pull.title, pull.user.login)
        message += line
    return message

def send_to_slack(message):
    payload = {
        'token': SLACK_API_TOKEN,
        'channel': SLACK_CHANNEL,
        'username': 'Pull Request Reminder',
        'icon_emoji': ':goat:',
        'text': message
    }

    response = requests.post(POST_URL, data=payload)
    if not response.ok or not response.json()['ok']:
        raise Exception(response.json()['error'])

def send_pull_reminder():
    client = Github(GITHUB_API_TOKEN)
    repo = fetch_repo(client)
    pulls = fetch_pulls(repo)
    message = format_pulls(pulls)
    send_to_slack(message)

if __name__ == '__main__':
    send_pull_reminder()
