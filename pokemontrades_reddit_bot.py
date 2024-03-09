import json
import praw
import boto3
import logging
from json import JSONDecodeError
import sys

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Constants
AWS_REGION = "us-east-1"


def load_reddit_credentials():
    # Load Reddit credentials from an external JSON file.
    try:
        with open('cred_reddit.json', 'r') as f:
            credentials = json.load(f)
            return credentials
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except JSONDecodeError as e:
        logger.error(f"The JSON file contains invalid JSON: "
                     f"{e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading Reddit credentials: {e}")
        sys.exit(1)


def load_emails():
    try:
        with open('emails.json', 'r') as f:
            credentials = json.load(f)
            return credentials['sender_email'], credentials['recipient_email']
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        sys.exit(1)
    except JSONDecodeError as e:
        logger.error(f"The JSON file contains invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading Reddit credentials: {e}")
        sys.exit(1)


# Initialize PRAW with credentials
def init_reddit(credentials):
    return praw.Reddit(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        user_agent=credentials['user_agent']
    )


# Function to send an email with AWS SES
def send_email(subject, body):
    ses = boto3.client('ses', region_name=AWS_REGION)
    emails_tuple = load_emails()
    sender_email = emails_tuple[0]
    recipient_email = emails_tuple[1]
    try:
        response = ses.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        logger.info(f"Email sent! Message ID: {response['MessageId']}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")


# Main function to fetch posts and send emails
def fetch_and_send_posts(reddit):
    subreddit = reddit.subreddit('pokemontrades')
    for submission in subreddit.new(limit=10):
        if 'giveaway' in submission.title.lower():
            subject = f"Reddit Giveaway Alert: {submission.title}"
            body = submission.selftext
            send_email(subject, body)


# Lambda handler or main entry point
def lambda_handler(event, context):
    credentials = load_reddit_credentials()
    if not credentials:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to load Reddit credentials.')
        }

    reddit = init_reddit(credentials)
    try:
        # Attempt to fetch the 10 most recent submissions from a subreddit
        submissions = reddit.subreddit('pokemontrades').new(limit=10)

        # Try accessing the fetched submissions to trigger any lazy-loading
        # exceptions
        for submission in submissions:
            print(submission.title)

        # If no exceptions were raised up to this point, the operation was
        # successful
        print("Fetched submissions successfully.")
    except Exception as e:
        # Handle other possible exceptions
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to load Reddit credentials:{e}')
        }

    fetch_and_send_posts(reddit)
    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully!')
    }

# Uncomment if running locally or outside of AWS Lambda
# if __name__ == "__main__":
#  lambda_handler(None, None)
