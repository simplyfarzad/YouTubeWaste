YouTube Waste
=============
Inspired by Wasted Days
and
`YouTube Watched History Analyser <https://python-forum.io/Thread-Youtube-Watched-History-Analyzer>`_

This project calculates the hours one wasted watching YouTube videos.

In order to run this project you need to:

* Go `here <https://takeout.google.com/settings/takeout>`_ and download just the YouTube data in json format (under YouTube select Multiple formats and change History type from HTML to JSON). Wait for it to be prepared and download it.

* Get an `API Key <https://support.google.com/googleapi/answer/6158862>`_ (Do not share it with anyone!)

* Go to `Google API Library <https://console.developers.google.com/apis/library>`_ and enable **YouTube Data API v3**.

* Install YouTube API module `$ python3 -m pip install google-api-python-client`