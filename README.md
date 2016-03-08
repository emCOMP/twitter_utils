# Twitter Utils

A collection of random scripts that do various tasks for analyses. Currently, this is very lonely and has just one script. These rely on twitter credentials being placed in the directory you ran it from with the name `config.json`. 

Tools located in the bin directory:
* get_timeline.py


## get_timeline.py

get_timeline.py <user id file> <output filename> 

`user id file` - A list of user ids to grab. each on its own line.
`output filename` - the JSON to write out

Optional arguments: 
`--sincedate` an ISO formatted date that will be the earliest date from which to collect.
`--untildate` an ISO formatted date that will be the most recent date from which to collect.
`--configfile` path to the configfile. If not specified it will search the local directory for config.json. This will have your twitter API keys and access tokens. 

> Note that the Twitter API used for retrieving these is limited to retrieving only so many of the most recent 3200 Tweets for each user. For users that tweet a lot, you may not be able to retrieve more than a few days or weeks. You can read more about this at the [Twitter status/user_timeline API call](https://dev.twitter.com/rest/reference/get/statuses/user_timeline)



