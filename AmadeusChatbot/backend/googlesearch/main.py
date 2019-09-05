# for some questions not in the database, use google searchto find answers.
import pprint
import json

from googleapiclient.discovery import build


def main(query):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyBbwteroLbB4he4wyfYLjNgk-tBiKEyvRY")

  res = service.cse().list(
      q=query,
      cx='006514795798405018250:2wj6gbdzsbi',
      num=1,
    ).execute()

  return (res['items'][0]['link'])


