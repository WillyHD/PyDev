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

    twitter_consumer_key = 'NAdGobZyRjWB55cdg6mF18waZ'
    twitter_consumer_secret = 'CmBynt2j3qzbhN2xuzjX9Ogn7QJ9NhITLWahCusS9zoNVFIBLZ'
    twitter_access_token = '284721234-cMnM0lWiWoVQCPE9m6KDfOw9GJejTexhPf7cuxca'
    twitter_access_secret = 'IBWTV7aU4x1lXtlFFXmJqjdqYAsvVmxH3U5rZ9qGK31h3'

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
