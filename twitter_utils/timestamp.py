#! /usr/bin/env python
# -=- encoding: utf-8 -=-

from time import strptime
from calendar import timegm

#
# borrowed from Nick Galbreath
# source: https://github.com/client9/snowflake2time/
#


def utc2snowflake(stamp):
    return (int(round(stamp * 1000)) - 1288834974657) << 22


def convertIsoDateToSnowflake(datestr):
    return utc2snowflake(
        timegm(strptime(datestr, "%Y-%m-%dT%H:%M:%S")))
