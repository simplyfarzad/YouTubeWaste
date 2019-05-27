"""
    Created by Farzad on 5/26/2019 at 9:14
"""

import json
import re
import datetime
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
import pandas as pd
import isodate
# import time
# import numpy as np

# Initialization
file_history = 'C:/Users/Farzad/Desktop/Takeout/YouTube/history/watch-history.json'
result_dir = 'C:/Users/Farzad/Desktop/Takeout/YouTube/result'


def add_id():  # Add video ID to contentDetail
    # Open the history file
    with open(file_history, 'r', encoding='utf8') as f:
        data = json.load(f)
    data_new = []
    # ids = ','.join(list(map(lambda content: re.match('.+=(.+)', content['titleUrl']).group(1), sub_data)))

    for contentDetail in data:
        try:
            title_url = re.match('.+=(.+)', contentDetail['titleUrl'])  # extract id from video
        except KeyError:  # for some reason, some videos does not have a url!
            continue

        contentDetail['id'] = title_url.group(1)  # extract id from video
        data_new.append(contentDetail)

    with open(result_dir + '/new_data_with_ID.txt', 'w', encoding='utf8') as result_file:
        json.dump(data_new, result_file, ensure_ascii=False)  # to write the persian chars correctly!


def add_duration():  # Add video Duration to contentDetail
    api_key = input("Give me the YouTube API Key: ")
    service = build('youtube', 'v3', developerKey=api_key)

    # Open the file
    with open(result_dir + "/new_data_with_ID.txt", 'r', encoding="utf8") as f:
        data = json.load(f)

    # YouTube API only allows 50 simultaneous ids query
    almost_all = int(len(data) / 50)
    residual = len(data) % 50
    lower_bound = 0
    upper_bound = 50

    for c in range(almost_all + 1):
        print(c)
        ids = ','.join(list(map(lambda item: item["id"], data[lower_bound:upper_bound])))

        # print(ids)
        request = service.videos().list(
            part="contentDetails",
            id=ids  # I can use response to find the video ID but
            # in order to get the response I have to provide the ID!
        )
        response = request.execute()

        for i in range(int(response["pageInfo"]["totalResults"])):  # some videos may not response
            # (deleted for copyright or country restrictions)
            for j in range(lower_bound, upper_bound):
                if response["items"][i]["id"] == data[j]['id']:
                    data[j]["duration"] = response["items"][i]["contentDetails"]["duration"]
                    break

        lower_bound += 50
        upper_bound += 50 if c != (almost_all - 1) else residual
        # time.sleep(1)

    with open(result_dir + '/new_data_with_ID_Duration.txt', 'w', encoding='utf8') as result_file:
        json.dump(data, result_file, ensure_ascii=False)  # to write the persian chars correctly!


def draw_graph():
    # Open the file
    with open(result_dir + "/new_data_with_ID_Duration.txt", 'r', encoding="utf8") as f:
        data = json.load(f)

    total_2019 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_2018 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total_2017 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # counter = 0
    for video_watched in data:
        # print(counter + 1)
        try:
            video_watched_time = datetime.datetime.strptime(video_watched['time'], '%Y-%m-%dT%H:%M:%S.%f%z')
        except:  # Some videos' time does not have %f (milliseconds)
            video_watched_time = datetime.datetime.strptime(video_watched['time'], '%Y-%m-%dT%H:%M:%S%z')

        try:
            video_watched_duration = float(isodate.parse_duration(video_watched["duration"]).total_seconds())
            if video_watched_duration > 5400:  # Do not count videos with more than half-hour duration,
                continue  # since I did not see them or they were live-streams
        except KeyError:  # Some videos does not have duration. Skip them!
            continue

        # Number of videos watched in a month
        # if video_watched_time.year == 2019:
        #     total_2019[video_watched_time.month - 1] += 1
        # elif video_watched_time.year == 2018:
        #     total_2018[video_watched_time.month - 1] += 1
        # elif video_watched_time.year == 2017:
        #     total_2017[video_watched_time.month - 1] += 1

        # Duration of videos watched in a month
        if video_watched_time.year == 2019:
            total_2019[video_watched_time.month - 1] += video_watched_duration
        elif video_watched_time.year == 2018:
            total_2018[video_watched_time.month - 1] += video_watched_duration
        elif video_watched_time.year == 2017:
            total_2017[video_watched_time.month - 1] += video_watched_duration

        # counter += 1

    print("Year 2019: Total -> {0}".format(str(sum(total_2019) / 3600)))
    print([d / 3600 for d in total_2019])
    print("Year 2018: Total -> {0}".format(str(sum(total_2018) / 3600)))
    print([d / 3600 for d in total_2018])
    print("Year 2017: Total -> {0}".format(str(sum(total_2017) / 3600)))
    print([d / 3600 for d in total_2017])

    # Make a data frame
    df = pd.DataFrame({'x': range(1, 13),
                       '2019': [d / 3600 for d in total_2019],
                       '2018': [d / 3600 for d in total_2018],
                       '2017': [d / 3600 for d in total_2017]})  # Converting seconds to minutes

    # style
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num = 0
    for column in df.drop('x', axis=1):
        num += 1
        plt.plot(df['x'], df[column], marker='', color=palette(num), linewidth=1, alpha=0.9, label=column)

    # Add legend
    plt.legend(loc=2, ncol=2)

    # Add titles
    plt.title("Total Hours Watched per Month", loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Month")
    plt.ylabel("Hours")

    plt.savefig('YouTubeWaste.png')


def main():
    # add_id()
    # add_duration()
    draw_graph()


if __name__ == "__main__":
    main()
