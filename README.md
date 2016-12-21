# check-jenkins-updates

A python script that checks for new Jenkins releases and sends email accordingly

## Requirements

* [Requests](http://docs.python-requests.org/) > 2.9.x

## Configuration

Configuration is performed via environment variables:

* `CHECK_JENKINS_UPDATES_DEBUG` - if set to 1, print debut output to stdout; if set to 0, no debug output (defaults to: 0)
* `CHECK_JENKINS_UPDATES_SOURCE` - update site to check for updates (defaults to: http://updates.jenkins-ci.org/update-center.json)
* `CHECK_JENKINS_UPDATES_SMTP` - SMTP server for sending email (defaults to: localhost)
* `CHECK_JENKINS_UPDATES_FROM` - email address to send from (defaults to: check-jenkins-updates@unknown)
* `CHECK_JENKINS_UPDATES_RECIPIENT` - email address(es) to send to; multiple email addresses must be comma-separated
* `CHECK_JENKINS_UPDATES_CACHE` - path to cache file (defaults to: `/tmp/check_jenkins_version.cache`)

## Usage

```
$ python check-jenkins-updates.py
```
