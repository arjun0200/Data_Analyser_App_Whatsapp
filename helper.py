from typing import List, Any

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user == 'Overall':
        # 1. fetch number of messages
        num_messages = df.shape[0]
        # 2. number of words
        words = []
        for message in df['Clean_messages']:
            words.extend(message.split())
        # 3. media omitted
        media = df[df['Clean_messages'].str.contains(pat=str('omitted'), case=False)]
        # 4. link shared
        links = []
        for link in df['Clean_messages']:
            links.extend(extractor.find_urls(link))
        return num_messages, len(words), len(media), len(links)
    else:
        new_df = df[df['User'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['Clean_messages']:
            words.extend(message.split())
        media = new_df[df['Clean_messages'].str.contains(pat=str('omitted'), case=False)]
        links = []
        for link in new_df['Clean_messages']:
            links.extend(extractor.find_urls(link))
        return num_messages, len(words), len(media), len(links)


def most_busy_users(df):
    x = df["User"].value_counts().head(2)
    new_df = round((df['User'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'User': 'Percent'})
    return x, new_df


def create_wordcloud(selected_user, df):
    f = open('hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    index = df[df['Clean_messages'].str.contains(pat=str('omitted'), case=False)].index
    temp = df.drop(axis=0, index=index)

    def remove_stop(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Clean_messages'] = temp['Clean_messages'].apply(remove_stop)
    df_wc = wc.generate(temp['Clean_messages'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    index = df[df['Clean_messages'].str.contains(pat=str('omitted'), case=False)].index
    temp = df.drop(axis=0, index=index)
    words = []
    for message in temp['Clean_messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(word.split())
    df_mc = pd.DataFrame(Counter(words).most_common(20))
    return df_mc


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Clean_messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    df_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return df_emoji


def month_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['Clean_messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline


def daily_time(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Clean_messages'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df_heat = df.pivot_table(index='day_name', columns='period', values='Clean_messages', aggfunc='count').fillna(0)
    return df_heat