import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights


def analyze(handle):
    """
    Function is used to retrieve and analyze
    the last 200 tweets of a Twitter handle
    using the Watson Personality Insights API
    """
    # Twitter API credentials - required
    twitter_consumer_key = ''
    twitter_consumer_secret = ''
    twitter_access_token = ''
    twitter_access_secret = ''

    # Invoke the Twitter API
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                              consumer_secret=twitter_consumer_secret,
                              access_token_key=twitter_access_token,
                              access_token_secret=twitter_access_secret)

    # Retrieve 200 tweets from user
    statuses = twitter_api.GetUserTimeline(
        screen_name=handle, count=200, include_rts=False)

    # Format all tweets into one block
    text = ""
    for status in statuses:
        if status.lang == 'en':
            text += status.text.encode('utf-8')

    # IBM Watson / Bluemix Credentials
    # Analyze tweets with Watson API
    pi_username = 'temp'
    pi_password = 'temp'
    personality_insights = PersonalityInsights(
        username=pi_username, password=pi_password)

    pi_result = personality_insights.profile(text)

    # Return the results
    return pi_result


def flatten(orig):
    """
    Flattens the JSON results
    returned by the Watson API
    """

    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                            data[c3['id']] = c3['percentage']

    # Return the flattened results
    return data


def compare(dict1, dict2):
    """
    Compares results of two strings,
    specifically the results returned
    by the Watson API
    """

    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
            compared_data[keys] = abs(dict1[keys] - dict2[keys])

    # Return the compared data
    return compared_data


# Twitter handles to analyze
user_handle = "@Codecademy"
celebrity_handle = "@IBM"

# Analyze tweets with Watson API
user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)

# Flatten results from Watson API
user = flatten(user_result)
celebrity = flatten(celebrity_result)

# Compare results between user and celebrity
compared_results = compare(user, celebrity)

# Sort results to find the most likely common traits
sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

# Print results for user
for keys, value in sorted_result[:5]:
    print(keys),
    print(user[keys]),
    print('->'),
    print(celebrity[keys]),
    print('->'),
    print(compared_results[keys])
