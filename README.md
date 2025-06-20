# Subreddit Scraper with Browser-Use

Just a proof of concept to get familiar with agentic browser use.

## TODO:
[_] Customisation of prompt
[_] Customisation of chat log emission
[_] Passing in args to override/instead of env variables
[_] Review the Browser-Use docs and try out observability features
[_] Review Browser-Use docs and try out using local LLM
[_] Review Browser-Use docs for adding own tool - e.g. extracting html by xpath pattern 

## setup

### dependencies
Assuming you've got a virtual env and uv installed. You can install uv with `pip install uv`.

```bash
uv pip install browser-use
uv run playwright install
```

### remote chrome debugger
Pull and run the following docker image `zenika/alpine-chrome` or start a chrome session with the chrome remote debugging tools enabled

### environment variables
Create a `.env` file in directory and fill in your values for:

```
OPENAI_API_KEY=<your_openai_key>
LLM_MODEL_ID=gpt-4o
LLM_USE_VISION=false
CHROME_CDP_URL=http://localhost:9222
ANONYMIZED_TELEMETRY=true
SUBREDDIT=<subreddit_id>
```
