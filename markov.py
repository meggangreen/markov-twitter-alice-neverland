"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import string
import twitter


def open_and_read_file(file_path):
    """ Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    filename = open(file_path)
    file_lines = filename.readlines()
    filename.close()

    # Choose 300 lines from extremely long text
    start_line = file_lines.index(choice(file_lines[:-300]))
    end_line = start_line + 300
    selected_lines = file_lines[start_line:end_line]
    long_text = " ".join(selected_lines)

    return long_text


def make_chains(text_string1, text_string2, n):
    """ Take input text as string; return dictionary of Markov chains. """

    chains = {}

    text_string = text_string1 + " " + text_string2

    text_list = text_string.split()
    text_list.append(None)

    for i in range(len(text_list) - n):
        text_snippet = tuple(text_list[i:i + n])
        follower = text_list[i + n]
        chains[text_snippet] = chains.get(text_snippet, [])
        chains[text_snippet].append(follower)

    return chains


def make_text(chains, n):
    """Return text from chains."""
    new_word = ""
    words = []
    i = 0

    bi_gram_tuple = choice(chains.keys())

    words.extend(bi_gram_tuple)

    while True:
        i += 1
        new_word = choice(chains[bi_gram_tuple])
        total_chars = sum(len(char) for char in words) + len(words)
        if new_word is None or total_chars + len(new_word) >= 139:
            if (words[-1][-1] in string.punctuation and
                words[-1][-1] not in (['.', '?', '!'])):
                words[-1] = words[-1][:-1] + choice((['.', '?', '!']))
            elif words[-1][-1] not in string.punctuation:
                words[-1] = words[-1] + choice((['.', '?', '!']))
            break
        words.append(new_word)
        bi_gram_tuple = tuple(words[i:i + n])

    words[0] = words[0].title()
    return " ".join(words)


def tweet(random_text):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    # print api.VerifyCredentials()
    status = api.PostUpdate(random_text)
    print status.text


# Get file text -- one at a time, static files, dynamic text
input_text1 = open_and_read_file("alice.txt")
input_text2 = open_and_read_file("neverland.txt")
n = 2

def want_to_tweet_again():

    while True:
        user_input = raw_input("Enter to tweet [q to quit] > ")
        if user_input == 'q':
            break

        # Get a Markov chain
        chains = make_chains(input_text1, input_text2, n)

        # Produce random text
        random_text = make_text(chains, n)

        # Tweet random text
        tweet(random_text)

want_to_tweet_again()
