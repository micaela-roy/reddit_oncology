import praw
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os

if __name__ == "__main__":

    # Reddit API credentials
    REDDIT_CLIENT_ID = "hMGPCziTpNJ_f_2e0kqnlA"
    REDDIT_CLIENT_SECRET = "2JEZrTqpkziQAygS4r9mGLo0Uc3iag"
    REDDIT_USER_AGENT = "windows:BC_EOL_Scrape:v1.0 (by /u/Organic_Ear_9037)"
    
    # Initialize PRAW Reddit instance
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    subreddits = ["breastcancer", "ovariancancer", "prostatecancer", "coloncancer",
                  "lungcancer", "cancer", "leukemia", "lymphoma", "braincancer",
                  "pancreaticcancer", "melanoma", "kidneycancer", "testicularcancer"]
    post_limit = 1000
    posts = []
    
    # Loop through each subreddit
    for subreddit_name in subreddits:
        print(f'working on r/{subreddit_name}')
        try:
            submissions = reddit.subreddit(subreddit_name).new(limit=post_limit)
            for submission in submissions:
                posts.append({
                    "subreddit": subreddit_name,
                    "title": submission.title,
                    "text": submission.selftext,
                    "date": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "url": submission.url
                })
        except Exception as e:
            print(f"Error while processing r/{subreddit_name}: {e}")
    
    
    # Convert new posts to DataFrame
    new_df = pd.DataFrame(posts)
    csv_path = "data/reddit_posts.csv"
    
    # Load existing data if available
    if os.path.exists(csv_path):
        old_df = pd.read_csv(csv_path)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        # Drop duplicates based on PostID
        combined_df.drop_duplicates(inplace=True)
    else:
        combined_df = new_df
    
    # save to csv
    combined_df.to_csv(csv_path, index=False)