"""
    Created by Farzad on 5/26/2019 at 11:26
"""

# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

API_key = "-"

# scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes)
    # credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_key)

    request = youtube.videos().list(
        part="contentDetails",
        id="_sSNiH9nPR0,uykMPICGeqw"
    )
    response = request.execute()

    print(response) # ['items'][0]['contentDetails']['duration']
    print(len(response))


if __name__ == "__main__":
    main()
