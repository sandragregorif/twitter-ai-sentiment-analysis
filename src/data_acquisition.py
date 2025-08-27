#Import the necessary libraries
import os #To interact with the operating system (paths, enviroment variables)
import tweepy #Main library to connect to the Twitter API
import pandas as pd #To manipulate and store data in table format
from dotenv import load_dotenv #To load environmet variables from a .env file

def main():
    """
    Main function that orchestrates the entire Twitter data extraction process.
    """

    #STEP 1: Load API credentials from the .env file

    #Build the path to the .env file located in the root folder of the project
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

    #Get the Bearer Token (API key) from environmet variables
    bearer_token = os.getenv("BEARER_TOKEN")
    
    #Check if the token is available
    if not bearer_token:
        print("ERROR: BEARER_TOKEN not found in the .env file")
        print("Please make sure you have a .env file with your token")
        return
    
    #STEP 2: Configure the Twitter API client

    try:
        #Create the Tweepy client using the Bearer Token for authentication
        client = tweepy.Client(bearer_token=bearer_token)
        print("Twitter client configured successfully")
    except Exception as e:
        #Handle any error that occurs during client setup
        print(f"Error configuring client: {e}")
        return
    
    #STEP 3: Define search parameters

    #Search tweets with #ArtificialIntelligence, exclude retweets, in English 
    query = "#ArtificialIntelligence -is:retweet lang:en"

    #Maximum number of tweets to retrieve (API limit)
    max_results = 100

    print(f"Searching tweets with: {query}")
    print(f"Limit: {max_results} tweets")
    
    #STEP 4: Perform the tweet search using the API

    try:
        #Execute the recent tweets search with the specified parameters
        tweets = client.search_recent_tweets(
            query=query, #Search terms
            tweet_fields=["author_id", "created_at", "text", "public_metrics"], #Additional fields to onclude
            max_results=max_results #Results limit
        )
        
        #Check if any tweets were found
        if not tweets.data:
            print("No tweets found with the specifed criteria")
            return
            
        print(f"Found {len(tweets.data)} tweets")
        
    except Exception as e:
        #Handle API errors (connection issues, exceeded limits, etc.)
        print(f"Search error: {e}")
        return
    
    #STEP 5: Process and transform the obtained data

    #List to store processed tweets
    tweet_data = []

    #Iterate over each tweet and extract the relevant information
    for tweet in tweets.data:
        tweet_data.append({
            "id": tweet.id, #Unique tweet ID
            "author_id": tweet.author_id, #ID of the user who posted the tweet
            "created_at": tweet.created_at, #Creation date and time
            "text": tweet.text, #Tweet text content
            "retweets": tweet.public_metrics["retweet_count"], #Number of retweets
            "likes": tweet.public_metrics["like_count"] #Number of likes
        })
    
    #Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(tweet_data)

    #STEP 6: Prepare the file system
    
    #Create the 'data' folder if it doesn't exist (avoid errors when saving)
    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    
    #STEP 7: Save the data into a CSV file

    #Build the full path of the output file
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_tweets.csv')

    #Save the DataFrame as CSV (withouy index, UTF-8 encoding for special characters)
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    #STEP 8: Show confirmation and sample data

    print(f"Data saved at: {output_path}")
    print("First 3 rows of the data:")
    #Show the first 3 rows to verify the data
    print(df.head(3))

#Entry point of the script - only run main() if this file is executed directly
if __name__ == "__main__":
    main()