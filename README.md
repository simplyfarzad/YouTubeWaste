YouTube Waste
=============
*Inspired by Wasted Days
and
[YouTube Watched History Analyser](https://python-forum.io/Thread-Youtube-Watched-History-Analyzer)*

This project calculates the hours one wasted watching YouTube videos.

In order to run this project you need to:

1. Go [here](https://takeout.google.com/settings/takeout) and download just the YouTube data in json format (under YouTube select Multiple formats and change History type from HTML to JSON). Wait for it to be prepared and download it.

2. Get an [API Key](https://support.google.com/googleapi/answer/6158862) (Do not share it with anyone!)

3. Go to [Google API Library](https://console.developers.google.com/apis/library) and enable *YouTube Data API v3*.

4. Install YouTube API module `$ python3 -m pip install google-api-python-client`

Things to consider:

1. YouTube API does not allow more than 50 ids in one request.

2. [YouTube Data API](https://developers.google.com/youtube/v3/docs/videos/list) page was a great help, specially **Try this API** part.

3. Google does not allow more than 10,000 queries per day (Quotas). Keep it in mind!