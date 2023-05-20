import tweepy

all_keys = open('keys.txt', 'r').read().splitlines()
api_key = all_keys[0]
api_key_secret = all_keys[1]
access_token = all_keys[2]
access_token_secret = all_keys[3]

# Authenticate with Twitter API using Tweepy
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    with open("messaged_ids.txt", "r") as f:
        messaged_ids = [int(line.strip()) for line in f.readlines()]
except FileNotFoundError:
    messaged_ids = []

# Retrieve the tweet you want to target
tweet_id = '' # Replace with the ID of the tweet you want to target
tweet = api.get_status(tweet_id)

# List of user IDs who retweeted
retweeters = api.get_retweeter_ids(tweet_id)
for retweeter in retweeters:
    user = api.get_user(user_id=retweeter)
    print("Retweeter: " + user.screen_name + "\n\n")

# Retrieve all replies to the tweet
replies = api.search_tweets(q='to:NAME "send"', since_id=tweet_id, tweet_mode="extended")

# Iterate over the replies
for reply in replies:
    # Do something with the reply, such as print its text
    print("Reply: " + reply.user.screen_name + "\n\n")

    if reply.user.id in retweeters and reply.user.screen_name != 'NAME' and reply.user.id not in messaged_ids:
        print("Sending message to: " + reply.user.screen_name)
        message = "Add custom message here".format(reply.user.name)
        api.send_direct_message(reply.user.id, message)
        print("Message sent to " + reply.user.screen_name)
        messaged_ids.append(reply.user.id)
        print("Added " + reply.user.screen_name + " to the list")

    with open("messaged_ids.txt", "w") as f:
        f.write("\n".join(str(id) for id in messaged_ids))
    print("Updated the file")