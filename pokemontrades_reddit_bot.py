# pokemontrades_reddit_bot.py
#
# This program, as fo now, reads the top 10 new posts from the subbreddit
# r/pokemontrades and sends one email containing the title and message body
# for each of those 10 posts that matched the designated flair tags.
#
# Levester Williams
# 2 February 2024
#
# Platform info:
# - python 3.11.0
# - boto3==1.34.59
# - botocore==1.34.59
# - certifi==2024.2.2
# - charset-normalizer==3.3.2
# - idna==3.6
# - jmespath==1.0.1
# - praw==7.7.1
# - prawcore==2.4.0
# - python-dateutil==2.9.0.post0
# - requests==2.31.0
# - s3transfer==0.10.0
# - six==1.16.0
# - urllib3==2.0.7
# - websocket-client==1.7.0
# - update-checker==0.18.0
# - openai==1.14.3

import json
import praw
import boto3
import logging
from json import JSONDecodeError
import sys
import openai

logger = logging.getLogger()
logger.setLevel(logging.INFO)
AWS_REGION = "us-east-1"

def load_json_file(json_file):
    """
    Loads Reddit credentials from an external JSON file.

    Args:
        json_file (str): Path to the JSON file

    Returns:
        dict: Dictionary

    Notes:
        If error occurs in opening JSON file, the function will exit with an
        error message.
    """
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
    """
    Initializes a Reddit instance.

    Args:
        credentials (JSON): Reddit credentials.

    Returns:
        dict: Reddit
    """
    return praw.Reddit(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        user_agent=credentials['user_agent']
    )

def send_email(subject, body):
    """
    Sends an email via AWS SES.

    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.

    Returns:
        None

    Notes:
        Client must have an access key and secret access key defined in the
        config.json file.
    """
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
def fetch_and_send_posts(reddit, flair):
    """
    Fetches the subbreddit posts and sends them.

    Args:
        reddit (Reddit): The Reddit instance to fetch and send posts from
        designated email address.
        flair (str): The flair/tag of the subreddit posts.

    Returns:
        None
    """
    subreddit = reddit.subreddit('pokemontrades')
    email_body = (f'Hello Levester,\n\nHere are the posts that match your '
                  f'criteria:\n\n')
    found_posts = False

    for submission in subreddit.new(limit=10):
        if submission.link_flair_text == flair:
            found_posts = True
            email_body += f"**Title**: {submission.title}\n\n> {submission.selftext}\n\n"

    if found_posts:
        subject = "Reddit SV Flair Alert"
        print(f'The mail has been sent as the following:\n{email_body}')
        send_email(subject, email_body)
    else:
        print("No SV flair posts found.")


def lambda_handler(event, context):
    """
    Handles an incoming Lambda by processing the incoming request and sending
    it to the appropriate email addresses.

    Args:
        event(dict): Cron expression as defined in AWS EventBridge to invoke
        the Lambda function.
        context(string): Contains the AWS Lambda runtime information.

    Returns:
        dict: A response from the Lambda function that includes status code and
        body including any error information.

    """
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

        print("Fetched submissions successfully.")
    except Exception as e:
        logger.info(f"Cloudwatch logs group: {context.log_group_name}")
        # Handle other possible exceptions
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to load Reddit credentials:{e}')
        }
    flair = 'SV'
    fetch_and_send_posts(reddit, flair)
    logger.info(f"Cloudwatch logs group: {context.log_group_name}")
    return {
        'statusCode': 200,
        'body': json.dumps('Function executed successfully!')
    }

# only if running locally or outside of AWS Lambda
# if __name__ == "__main__":
#  lambda_handler(None, None)
