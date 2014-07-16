#!/usr/bin/env python

import urllib2, json, os, subprocess

def get_access_token():
    request = urllib2.Request("http://chunderbase.il.ot2.tv/oauth/token", "grant_type=client_credentials", {"Authorization" : "Basic YXNxM2FkZjJxa2doZGZzOnNka2ZqaGl1NTI5d2Vmc2IzNDJ0amhiNDN6OA=="})
    json_data = json.load(urllib2.urlopen(request))
    return json_data["access_token"]

def get_clip_link():
    data = urllib2.urlopen("http://storage.googleapis.com/storage.ch2news.info/Homepage.f14.json")
    json_data = json.load(data)
    clip_link = json_data["HOMEPAGE"]["VIDEO_PLAYER"]["CLIP_LINK"]
    is_live = clip_link.startswith("ch2news")
    return clip_link, is_live

def get_stream_url(access_token, clip_link, is_live):
    path = "vod"
    if is_live:
        path = "live"
    url = "http://chunderbase.il.ot2.tv/zuul/{}/HLS/{}".format(path, clip_link)
    auth = "Bearer " + access_token
    request = urllib2.Request(url, "platform=mobile", {"Authorization" : auth, "Accept" : "*/*"})
    json_data = json.load(urllib2.urlopen(request))
    return json_data["public_url"]

def main():
    access_token = get_access_token()
    clip_link, is_live = get_clip_link()
    stream_url = get_stream_url(access_token, clip_link, is_live)

    print "stream {} with your favorite player.".format(stream_url)
    if "Darwin" in os.uname():
        subprocess.call(["open", "-a" "QuickTime Player", stream_url])

if __name__ == "__main__":
    main()
