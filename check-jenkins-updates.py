import json
import os
import re
import smtplib
import sys
from email.mime.text import MIMEText

import backoff
import requests

# get variables from environment
CHECK_JENKINS_UPDATES_SOURCE = os.getenv(
    'CHECK_JENKINS_UPDATES_SOURCE',
    'http://updates.jenkins-ci.org/stable/update-center.json')
CHECK_JENKINS_UPDATES_SMTP = os.getenv(
    'CHECK_JENKINS_UPDATES_SMTP',
    'localhost')
CHECK_JENKINS_UPDATES_FROM = os.getenv(
    'CHECK_JENKINS_UPDATES_FROM',
    'check-jenkins-updates@unknown')
CHECK_JENKINS_UPDATES_RECIPIENT = os.getenv(
    'CHECK_JENKINS_UPDATES_RECIPIENT',
    'root@localhost').split(',')
CHECK_JENKINS_UPDATES_CACHE = os.getenv(
    'CHECK_JENKINS_UPDATES_CACHE',
    '/tmp/check_jenkins_version.cache')
CHECK_JENKINS_UPDATES_RETRY_TIMEOUT = int(os.getenv(
    'CHECK_JENKINS_UPDATES_RETRY_TIMEOUT',
    '120'))
if os.getenv('CHECK_JENKINS_UPDATES_DEBUG', '0') == '1':
    DEBUG = True
else:
    DEBUG = False

def main():
    # load previous check results from cache
    if os.path.isfile(CHECK_JENKINS_UPDATES_CACHE):
        if DEBUG: print('found cache file')
        with open(CHECK_JENKINS_UPDATES_CACHE, 'r') as f:
            try:
                previous_check = json.load(f)
                cache_file_loaded = True
            except ValueError:
                if DEBUG: print('cache file does not contain valid JSON, '
                                'forcing update check')
                cache_file_loaded = False
    else:
        if DEBUG: print('no cache file found, forcing update check')
        cache_file_loaded = False

    if cache_file_loaded == False:
        previous_check = {
            'url': '',
            'sha1': '',
            'buildDate': '',
            'version': '',
            'name': ''
        }

    # get current version details from update source
    r = get_current_versions(CHECK_JENKINS_UPDATES_SOURCE)
    try:
        raw_json = re.search('\n(.*?)\n', r.text).group(1)
    except AttributeError:
        print('error: could not parse JSON from remote update source')
        sys.exit(1)
    current_json = json.loads(raw_json)

    # save current version to cache
    with open(CHECK_JENKINS_UPDATES_CACHE, 'w') as f:
        json.dump(current_json['core'], f)

    # check for version change
    if previous_check['version'] != current_json['core']['version']:
        output = (f"version change detected: {previous_check['version']} -> "
                  f"{current_json['core']['version']}")
        subject = ("new Jenkins release is available: "
                   f"{current_json['core']['version']}")
        if DEBUG: print(output)
        send_email(subject, output)
        if DEBUG: print('email sent!')
    else:
        if DEBUG: print(f"latest version has not changed (is: "
                        f"{current_json['core']['version']})")

@backoff.on_exception(backoff.expo,
                      requests.exceptions.ConnectionError,
                      max_time=CHECK_JENKINS_UPDATES_RETRY_TIMEOUT)
def get_current_versions(url):
    return requests.get(CHECK_JENKINS_UPDATES_SOURCE)

def send_email(msg_subject, msg_text):
    msg = MIMEText(msg_text)
    msg['Subject'] = msg_subject
    msg['From'] = CHECK_JENKINS_UPDATES_FROM
    msg['To'] = ','.join(CHECK_JENKINS_UPDATES_RECIPIENT)

    if DEBUG: print(f"sending email via mailserver "
                    f"{CHECK_JENKINS_UPDATES_SMTP}")
    s = smtplib.SMTP(CHECK_JENKINS_UPDATES_SMTP)
    s.sendmail(CHECK_JENKINS_UPDATES_FROM, CHECK_JENKINS_UPDATES_RECIPIENT,
               msg.as_string())
    s.quit()


if __name__ == "__main__":
    main()
