import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights


def analyze(handle):
    """
    Docstring
    """

    twitter_consumer_key = ''
    twitter_consumer_secret = ''
    twitter_access_token = ''
    twitter_access_secret = ''

    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret,
                              access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

    statuses = twitter_api.GetUserTimeline(
        screen_name=handle, count=200, include_rts=False)

    text = ""

    for status in statuses:
        if (status.lang == 'en'):
            text += status.text.encode('utf-8')

    pi_username = 'temp'
    pi_password = 'temp'
    personality_insights = PersonalityInsights(
        username=pi_username, password=pi_password)

    pi_result = personality_insights.profile(text)

    return pi_result


def flatten(orig):
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
    return data
