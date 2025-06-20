import asyncio
from os import environ
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserSession, Controller
from pydantic import BaseModel
from dotenv import load_dotenv


class Post(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int

class Posts(BaseModel):
	posts: list[Post]
 
 
def environ_get_bool(key, default):
    value = environ.get(key, default)
    if not isinstance(value, bool):
        if value.lower() == "true":
             return True
        elif value.lower() == "false":
            return False
        else:
            raise ValueError(f"Unexpected value for environment variable: {key} - Expected True or False")
    else:
        return value
 
 
async def main(subreddit: str):
    browser_cdp = environ.get('CHROME_CDP_URL', 'http://localhost:9222')
    browser_profile_disable_security = environ_get_bool('BROWSER_PROFILE_DISABLE_SECURITY', False)
    browser_session = BrowserSession(cdp_url=browser_cdp)
    browser_session.browser_profile.disable_security = browser_profile_disable_security

    # Initialize the model
    model_id = environ.get('LLM_MODEL_ID', 'gpt-4o')
    llm = ChatOpenAI(
        model=model_id,
        temperature=0.0,
    )
    # Create agent with the model
    task=f"""Navigate to https://www.reddit.com/r/{subreddit}/new and extract all of the <article> elements to get post details.
If you've already extracted a post skip it.

If you have extracted all of the current posts on the page, scroll down to bottom of the current view and wait at least 10 seconds and more posts will load.

Continue extracting posts until you've either: 
- Gathered 10 posts
- The age of the oldest post is greater than 7 days ago
- Failed to extract posts from the page more than 3 times in a row
"""
    use_vision = environ_get_bool('LLM_USE_VISION', False)
    controller = Controller(output_model=Posts)

    agent = Agent(
        task=task,
        llm=llm,
        browser_session=browser_session,
        controller=controller,
        use_vision=use_vision,              # Enable vision capabilities
        save_conversation_path="logs/conversation"  # Save chat logs
    )
    
    history = await agent.run()
    result = history.final_result()
        
    await browser_session.close()
    
    return result

    
if __name__ == "__main__":
    load_dotenv()
    subreddit = environ.get('SUBREDDIT', 'all')
    result = asyncio.run(main(subreddit))
    print(result)
