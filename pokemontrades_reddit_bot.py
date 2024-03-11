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

# Open and load JSON file
def load_json_file(json_file):
    # Load Reddit credentials from an external JSON file.
    try:
        with open(json_file, 'r') as f:
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
    emails = load_json_file('emails.json')
    sender_email = emails['sender_email']
    recipient_email = emails['recipient_email']
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
        if submission.link_flair_text == 'SV':
            subject = f"Reddit SV Alert: {submission.title}"
            body = submission.selftext
            send_email(subject, body)


# Lambda handler or main entry point
def lambda_handler(event, context):
    credentials = load_json_file('cred_reddit.json')
    if not credentials:
        logger.info(f"Cloudwatch logs group: {context.log_group_name}")
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
        logger.info(f"Cloudwatch logs group: {context.log_group_name}")
        # Handle other possible exceptions
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to load Reddit credentials:{e}')
        }

    fetch_and_send_posts(reddit)
    logger.info(f"Cloudwatch logs group: {context.log_group_name}")
    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully!')
    }

# only if running locally or outside of AWS Lambda
# if __name__ == "__main__":
#  lambda_handler(None, None)
