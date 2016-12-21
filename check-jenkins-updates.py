import requests
import json
import re
import os
import sys
import smtplib
from email.mime.text import MIMEText

# get variables from environment
CHECK_JENKINS_UPDATES_SOURCE = os.getenv('CHECK_JENKINS_UPDATES_SOURCE', 'http://updates.jenkins-ci.org/update-center.json')
CHECK_JENKINS_UPDATES_SMTP = os.getenv('CHECK_JENKINS_UPDATES_SMTP', 'localhost')
CHECK_JENKINS_UPDATES_FROM = os.getenv('CHECK_JENKINS_UPDATES_FROM', 'check-jenkins-updates@unknown')
CHECK_JENKINS_UPDATES_RECIPIENT = os.getenv('CHECK_JENKINS_UPDATES_RECIPIENT', 'root@localhost').split(',')
CHECK_JENKINS_UPDATES_CACHE = os.getenv('CHECK_JENKINS_UPDATES_CACHE', '/tmp/check_jenkins_version.cache')
if os.getenv('CHECK_JENKINS_UPDATES_DEBUG', '0') == '1':
    DEBUG = True
else:
    DEBUG = False

def main():
    # load previous check results from cache
    if os.path.isfile(CHECK_JENKINS_UPDATES_CACHE):
        if DEBUG: print "found cache file"
        with open(CHECK_JENKINS_UPDATES_CACHE, 'r') as f:
            try:
                previous_check = json.load(f)
                cache_file_loaded = True
            except ValueError:
                if DEBUG: print "cache file does not contain valid JSON, forcing update check"
                cache_file_loaded = False
    else:
        if DEBUG: print "no cache file found, forcing update check"
        cache_file_loaded = False

    if cache_file_loaded == False:
        previous_check = {"url": "", "sha1": "", "buildDate": "", "version": "", "name": ""}

    # get current version details from update source
    r = requests.get(CHECK_JENKINS_UPDATES_SOURCE)
    try:
        raw_json = re.search('\n(.*?)\n', r.text).group(1)
    except AttributeError:
        print "error: could not parse JSON from remote update source"
        sys.exit(1)
    current_json = json.loads(raw_json)

    # save current version to cache
    with open(CHECK_JENKINS_UPDATES_CACHE, 'w') as f:
        json.dump(current_json['core'], f)

    # check for version change
    if previous_check['version'] != current_json['core']['version']:
        output = "version change detected: {} -> {}".format(previous_check['version'], current_json['core']['version'])
        if DEBUG: print output
        send_email(output)
        if DEBUG: print "email sent!"
    else:
        if DEBUG: print "latest version has not changed (is: {})".format(current_json['core']['version'])


def send_email(msg_text):
    msg = MIMEText(msg_text)
    msg['Subject'] = "New Jenkins release is available"
    msg['From'] = CHECK_JENKINS_UPDATES_FROM
    msg['To'] = ','.join(CHECK_JENKINS_UPDATES_RECIPIENT)

    s = smtplib.SMTP(CHECK_JENKINS_UPDATES_SMTP)
    s.sendmail(CHECK_JENKINS_UPDATES_FROM, CHECK_JENKINS_UPDATES_RECIPIENT, msg.as_string())
    s.quit()


if __name__ == "__main__":
    main()
