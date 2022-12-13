import pandas as pd
import re


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\w{2}'
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({'user_message': messages, 'message_dates': dates})
    df['message_dates'] = pd.to_datetime(df['message_dates'], infer_datetime_format=True)

    def decontracted(phrase):
        # specific
        phrase = re.sub(r'\[', " ", phrase)
        phrase = re.sub(r'\]', " ", phrase)
        phrase = re.sub(r'\n', " ", phrase)
        return phrase

    preprocessed_messages = []

    for sentence in df['user_message'].values:
        sentence = decontracted(sentence)
        preprocessed_messages.append(sentence.strip())
    df['preprocessed_messages'] = preprocessed_messages
    df.rename(columns={'preprocessed_messages': 'messages', "message_dates": 'dates'}, inplace=True)
    df.drop('user_message', axis=1, inplace=True)

    users = []
    clean_messages = []
    for message in df['messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            clean_messages.append(entry[2])
        else:
            users.append("Group Notification")
            clean_messages.append(entry[2])

    df['User'] = users
    df['Clean_messages'] = clean_messages
    df.drop(columns=['messages'], inplace=True)

    df['Year'] = df['dates'].dt.year
    df['only_date'] = df['dates'].dt.date
    df['month_num'] = df['dates'].dt.month
    df['Month'] = df['dates'].dt.month_name()
    df['Day'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['Hour'] = df['dates'].dt.hour
    df['Minutes'] = df['dates'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

