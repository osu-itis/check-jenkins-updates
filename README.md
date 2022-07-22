# check-jenkins-updates

A python script that checks for new Jenkins releases and sends email accordingly

## Requirements

* Python 3.8+

pip packages:

* [backoff](https://pypi.org/project/backoff/)
* [requests](http://docs.python-requests.org/)

Package requirements are defined in `requirements.txt`

## Configuration

Configuration is performed via environment variables:

| envvar | purpose | default value |
| - | - | - |
| `CHECK_JENKINS_UPDATES_DEBUG` | if set to 1, print debut output to stdout; if set to 0, no debug output | 0 |
| `CHECK_JENKINS_UPDATES_SOURCE` | URL to check for updates | http://updates.jenkins-ci.org/stable/update-center.json |
| `CHECK_JENKINS_UPDATES_SMTP` | SMTP server for sending email | localhost |
| `CHECK_JENKINS_UPDATES_FROM` | email address to send from | check-jenkins-updates@unknown |
| `CHECK_JENKINS_UPDATES_RECIPIENT` | email address(es) to send to; multiple email addresses must be comma-separated |
| `CHECK_JENKINS_UPDATES_CACHE` | path to cache file | `/tmp/check_jenkins_version.cache` |
| `CHECK_JENKINS_UPDATES_RETRY_TIMEOUT` | max time in seconds to retry failed connections to the updates source URL | 120 |

## Usage

```
$ python check-jenkins-updates.py
```
