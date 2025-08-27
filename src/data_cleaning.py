#Import necessary libraries for data processing and NLP
import pandas as pd #For data manipulation and CSV handling
import re #For regular expressions (text pattern matching)
import nltk #Natural Language Toolkit for text processing
from nltk.corpus import stopwords #Common words to remove (the, and, is, etc.)
from nltk.stem import WordNetLemmatizer #For word normalization
import string #For punctuation characters
import os

#Download necessary NLTK datasets (first time only)
nltk.download('stopwords') #Download list of common stopwords
nltk.download('wordnet')   #Download WordNet database for lemmatization

def clean_tweet_text(text):
    """
    Clean and preprocess raw tweet text by removing noise and standardizing format.
    """
    #STEP 1: Convert all text to lowercase for consistency
    text = text.lower()
    
    #STEP 2: Remove URLs (http, https, www links)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    #STEP 3: Remove user mentions (@username) and hashtags (#topic)
    text = re.sub(r'@\w+|#\w+', '', text)
    
    #STEP 4: Remove punctuation and numbers from text
    text = text.translate(str.maketrans('', '', string.punctuation + string.digits))
    
    #STEP 5: Clean up extra whitespace and trim
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def main():
    """
    Main function to execute the data cleaning pipeline.
    """
    print("Starting data cleaning process...")
    
    #Define file paths for input and output
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', 'raw_tweets.csv')       #Raw data from Twitter API
    output_path = os.path.join(base_dir, 'data', 'cleaned_tweets.csv')  #Cleaned data destination
    
   
    #STEP 1: Load the raw tweet data from CSV

    try:
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} tweets from {input_path}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    #STEP 2: Apply text cleaning to each tweet

    print("Cleaning tweet text...")
    df['cleaned_text'] = df['text'].apply(clean_tweet_text)
    
    #STEP 3: Filter out empty tweets after cleaning

    initial_count = len(df)
    df = df[df['cleaned_text'].str.len() > 0] #Keep only non-empty tweets
    removed_count = initial_count - len(df)
    print(f"Removed {removed_count} empty tweets after cleaning")
    
    #STEP 4: Save the cleaned data to new CSV file

    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Cleaned data saved to: {output_path}")
    print(f"Final dataset: {len(df)} tweets")
    
    #STEP 5: Show sample results for verification

    print("\n📋 Sample of cleaned text:")
    for i, text in enumerate(df['cleaned_text'].head(3)):
        print(f"{i+1}. {text}")

#Run main() if script is executed directly
if __name__ == "__main__":
    main()