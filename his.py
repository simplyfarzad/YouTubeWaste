#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import json
from datetime import datetime, timedelta
from apiclient import discovery
from googleapiclient.discovery import build

# Init
API_key = "REPLACE_ME"
# List of your watch-history files (allow several accounts)
files = ['/Path/to/watch-history.json', '/Path/to/watch-history.json']
results_dir = '/Path/to/Results_dir'
# Load only videos after this date
min_date = "01/01/00"  # DD/MM/YY
# List of allowed results files
results = {'clean_history': True, 'average': True, 'channels': True, 'topics': True, 'tags': True, 'days': True,
           'months': True, 'years': True}
# Average percentage of videos watched
watch_percentage = 60  # %

service = build("youtube", "v3", developerKey=API_key)
Day = ['Monday', 'Tuesday', 'Friday', 'Wednesday', 'Thursday', 'Sunday', 'Saturday']
PT_format = re.compile(r'PT((?P<hours>\d+?)hr)?((?P<minutes>\d+?)M)?((?P<seconds>\d+?)S)?')
min_date = datetime.strptime(min_date, '%d/%m/%y')
watch_percentage /= 100
date_sorter = []
videos = []
average_li = []
sorted_li = []

channel_hm = {}
topic_hm = {}
tag_hm = {}
duration_hm = {}
day_name_hm = {}
day_hm = {}
month_hm = {}
year_hm = {}


# remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if value:
                good_kwargs[key] = value
    return good_kwargs


# sample python code for channels.list
def videos_list_by_id(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    return service.videos().list(**kwargs).execute()


def parse_time(time_str):
    parts = PT_format.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.iteritems():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def clear_videos_vars():
    video_title = video_description = video_duration = video_thumbnails = video_location = video_topics = video_tags = video_date = channel_id = channel_title = None


def count_data(hm_name, key):
    try:
        hm_name[key] = {'nb': hm_name[key]['nb'] + 1}
    except:
        hm_name[key] = {'nb': 1}


def average(dict):
    nb = 0
    length = 0
    for key in dict:
        nb += dict[key]['nb']
        length += 1
    return float(nb) / length


def sorted_list(hm_name):
    sorted_li = []
    for key in hm_name:
        sorted_li.append({'name': key, 'nb': hm_name[key]['nb']})
    return sorted(sorted_li, key=lambda k: k['nb'], reverse=True)


# create new path if necessary
if os.path.isdir(results_dir) == False:
    os.makedirs(results_dir)

# save watching date of videos
for f in files:
    for x in json.load(open(f)):
        date = datetime.strptime(x['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        delta_date = date - min_date
        if delta_date.total_seconds() > 0:
            date_sorter.append(date)

# sort videos per watching date
print(str(len(date_sorter)) + " videos detected")
date_sorter.sort(reverse=True)

for f in files:
    for x in json.load(open(f)):
        date = datetime.strptime(x['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        delta_date = date - min_date
        if delta_date.total_seconds() < 0:
            continue

        # define video position
        pos = 0
        for sorted_date in date_sorter:
            if sorted_date == date:
                break
            else:
                pos += 1

        # access to video data
        if x['snippet']['title'] != "Deleted video" and x['snippet']['title'] != "Private video":
            try:
                video_data = videos_list_by_id(service, part='snippet,contentDetails,topicDetails,recordingDetails',
                                               id=x['contentDetails']['videoId'])
                try:
                    video_location = (video_data['items'][0]['recordingDetails']['location']['latitude'],
                                      video_data['items'][0]['recordingDetails']['location']['longitude'])
                except KeyError:
                    video_location = None
                try:
                    video_topics = video_data['items'][0]['topicDetails']['topicCategories']
                except KeyError:
                    video_topics = []
                try:
                    video_tags = video_data['items'][0]['snippet']['tags']
                except KeyError:
                    video_tags = []

                video_title = video_data['items'][0]['snippet']['title']
                video_description = video_data['items'][0]['snippet']['description']
                video_duration = parse_time(video_data['items'][0]['contentDetails']['duration'])
                video_thumbnails = video_data['items'][0]['snippet']['thumbnails']['default']['url']
                video_date = datetime.strptime(video_data['items'][0]['snippet']['publishedAt'],
                                               '%Y-%m-%dT%H:%M:%S.000Z').strftime('%d/%m/%y %H:%M')

                channel_id = video_data['items'][0]['snippet']['channelId']
                channel_title = video_data['items'][0]['snippet']['channelTitle']

                # save video data in dicts
                for topic in video_topics:
                    count_data(topic_hm, topic)
                for tag in video_tags:
                    count_data(tag_hm, tag.lower())
                if pos > 0 and pos < len(date_sorter):
                    next_date = date_sorter[pos - 1]
                    if video_duration > next_date - date:
                        video_duration = next_date - date
                    else:
                        video_duration *= watch_percentage
                count_data(duration_hm, video_duration)
                count_data(channel_hm, channel_title)
            except (KeyError, IndexError):
                print("missing information for video '" + x['contentDetails']['videoId'] + "'")
                clear_videos_vars()
            except:
                print("unknown error for video '" + x['contentDetails']['videoId'] + "'")
                clear_videos_vars()
        else:
            print("unable to access video '" + x['contentDetails']['videoId'] + "'")
            clear_videos_vars()

        # save date data in dicts
        count_data(year_hm, str(date.year))
        count_data(month_hm, str(date.year) + "/" + str(format(date.month, '02')))
        count_data(day_hm, str(date.year) + "/" + str(format(date.month, '02')) + "/" + str(format(date.day, '02')))
        count_data(day_name_hm, date.strftime("%A"))

        # add all data to 'clean_history'
        videos.append({'pos': pos, 'date': date.strftime('%d/%m/%y %H:%M'),
                       'video': {'title': video_title, 'description': video_description,
                                 'duration': str(video_duration), 'thumbnails': video_thumbnails, 'date': video_date,
                                 'location': video_location, 'topics': video_topics, 'tags': video_tags},
                       'channel': {'title': channel_title, 'id': channel_id}})
    print("account " + str(json.load(open(f))[0]['snippet']['channelTitle']) + " done")

# sort and save dicts in results files
for list_result, value in results.iteritems():
    if value:
        if list_result == 'clean_history':
            with open(os.path.join(results_dir, "clean_history.json"), 'w') as outfile:
                json.dump(videos, outfile, indent=4)

        elif list_result == 'average':
            for day in Day:
                try:
                    day_name_hm[day]['nb'] = day_name_hm[day]['nb'] / (len(day_hm) / 7.0)
                except KeyError:
                    day_name_hm[day] = {'nb': 0}
            average_li.append({'videos per': {
                'day of the week': {Day[0]: day_name_hm[Day[0]]['nb'], Day[1]: day_name_hm[Day[1]]['nb'],
                                    Day[2]: day_name_hm[Day[2]]['nb'], Day[3]: day_name_hm[Day[3]]['nb'],
                                    Day[4]: day_name_hm[Day[4]]['nb'], Day[5]: day_name_hm[Day[5]]['nb'],
                                    Day[6]: day_name_hm[Day[6]]['nb']}, 'year': average(year_hm),
                'month': average(month_hm), 'day': average(day_hm), 'channel': average(channel_hm)}})

            nb = dur_sum = 0
            for key in duration_hm:
                dur_sum += duration_hm[key]['nb'] * key.total_seconds()
                nb += duration_hm[key]['nb']
            average_li.append({'video length (min)': dur_sum / nb / 60})

            with open(os.path.join(results_dir, "average.json"), 'w') as outfile:
                json.dump(average_li, outfile, indent=4)

        elif list_result == 'channels':
            with open(os.path.join(results_dir, "channels.json"), 'w') as outfile:
                json.dump(sorted_list(channel_hm), outfile, indent=4)
        elif list_result == 'topics':
            with open(os.path.join(results_dir, "topics.json"), 'w') as outfile:
                json.dump(sorted_list(topic_hm), outfile, indent=4)
        elif list_result == 'tags':
            with open(os.path.join(results_dir, "tags.json"), 'w') as outfile:
                json.dump(sorted_list(tag_hm), outfile, indent=4)

        elif list_result == 'days':
            with open(os.path.join(results_dir, "days.json"), 'w') as outfile:
                json.dump(sorted_list(day_hm), outfile, indent=4)
        elif list_result == 'months':
            with open(os.path.join(results_dir, "months.json"), 'w') as outfile:
                json.dump(sorted_list(month_hm), outfile, indent=4)
        elif list_result == 'years':
            with open(os.path.join(results_dir, "years.json"), 'w') as outfile:
                json.dump(sorted_list(year_hm), outfile, indent=4)