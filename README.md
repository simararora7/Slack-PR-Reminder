# Slack-PR-Reminder

## Usage 

### Python
```python 
SLACK_API_TOKEN="slack-token" GITHUB_API_TOKEN="github-token" REPOSITORY="repo-name" SLACK_CHANNEL="#channel-name" python slack_pull_reminder.py
```

### Docker
```python
docker build -t slack-pull-reminder .
docker run -e SLACK_API_TOKEN='slack-token' -e GITHUB_API_TOKEN='github-token' -e REPOSITORY='repo-name' -e SLACK_CHANNEL='#channel-name' slack-pull-reminder
```
