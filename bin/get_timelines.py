import os
import sys
import argparse
import logging
import logging.config
from datetime import datetime
import json
import tweepy
import io
from ezconf import ConfigFile
from itertools import izip_longest
from twitter_utils.timestamp import convertIsoDateToSnowflake
from tweepy.error import TweepError


log = logging.getLogger(__name__)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("idfile", help="input id file")
    parser.add_argument("outfile", help="output json file")
    parser.add_argument(
        "--configfile",
        default="config.json",
        help="config file to use")
    parser.add_argument("--sincedate",
        help="earliest date to scrape. (ISO format)")
    parser.add_argument("--untildate",
        help="latest date to scrape. (ISO format)")
    args = parser.parse_args()

    # config file
    config = ConfigFile(args.configfile)

    # configure the logging
    if "logging" in config:
        logging.config.dictConfig(config["logging"])
    else:
        # set up some default logging options
        logging.basicConfig(
            format="%(asctime)s|%(levelname)s|%(name)s - %(message)s",
            level=logging.DEBUG)
        logging.getLogger(__name__).setLevel(logging.getLevelName('WARN'))


    # parse out date time stuff
    since_id = None
    until_id = None

    if args.sincedate is not None:
        since_id = convertIsoDateToSnowflake(args.sincedate)
    if args.untildate is not None:
        until_id = convertIsoDateToSnowflake(args.untildate)


    print args.sincedate, since_id
    print args.untildate, until_id


    # open input file
    with io.open(args.idfile, mode="r", encoding="utf-8") as inputfile:
        # read all ids
        input_ids = []
        try:
            input_ids = [l.strip() for l in inputfile if len(l.strip()) > 0]
        except Exception, e:
            print "error reading input ids from file: ", e
            raise e

        with io.open(args.outfile, mode="w+", encoding="utf-8") as outfile:

            # twitter auth
            twitter_auth = config.getValue("twitter_auth", None)

            # create auth item
            auth = tweepy.auth.OAuthHandler(
                twitter_auth["api_key"],
                twitter_auth["api_secret"])
            auth.set_access_token(
                twitter_auth["access_token"],
                twitter_auth["access_token_secret"])

            # api
            api = tweepy.API(
                auth,
                wait_on_rate_limit=True)

            total = len(input_ids)
            cur_count = 0


            missed_users = []

            for i, id in enumerate(input_ids):

                cursor = tweepy.Cursor(
                    api.user_timeline,
                    screen_name=id,
                    since_id=since_id,
                    max_id=until_id,
                    count=200,
                    include_rts=True)


                try:
                    # write output
                    for status in cursor.items():
                        outfile.write(json.dumps(status._json) + u"\n")
                        cur_count += 1
                except TweepError, e:
                    log.error("Tweepy error getting user '%s'" % id)
                    missed_users.append(id)
                    continue
                except Exception, e:
                    log.exception("Failed to get user '%s'" % id)
                    continue

                # update progress
                log.debug("%3.2f%% done. (%d of %d users. %d tweets)" % (
                    (float(i) * 100.0 / float(total)),
                    i, total, cur_count
                    ))

    if missed_users is not None and len(missed_users) > 0:
        log.warn(
            "failed to get the following users: %s",
            ",".join(missed_users))

    print "done!"
