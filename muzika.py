#!/usr/bin/env python
#walid.saad

import sys
import requests
from bs4 import BeautifulSoup as bs
import collections
from termcolor import colored
import argparse

class Pleer:
    def __init__(self):
        self.api_url = 'http://pleer.com/site_api/files/get_url'
        self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}

    def get_tracks(self,search_string, n):
        loop_counter = 0
        songlist=[]
        fsonglist={}
        page=5
        for x in xrange(1,page):
            url = 'http://pleer.com/search?q={0}&target=tracks&page={1}&quality=best&sort_mode=0&sort_by=0&onlydata=true'
            url = url.format(search_string, str(x))
            response = requests.get(url,headers=self.headers)
            soup = bs(response.text)
            results = soup.findAll('div', {'class': 'playlist'})
            for song_listing in results:
                songs = song_listing.findChildren('li')
                for song in songs:
                    s=collections.OrderedDict()
                    s["artist"] = song.get('singer')
                    s["title"] = song.get('song')
                    s["bitrate"] = song.get('rate')
                    s["size"] = song.get('size')
                    s['id']=str(song.get('link'))
                    songlist.append(s)
        return songlist[:n]
    def show_results(self,songlist):
        fsonglist={}
        for n,fsong in enumerate([x for x in songlist if "VBR" not in x.get("bitrate")]):
            fsonglist[n]=fsong
            artist=colored(fsong['artist'],'red')
            title=colored(fsong['title'],'green')
            bitrate=colored(fsong['bitrate'],'yellow')
            size=colored(fsong['size'],'blue')
            print "%s)\t%s -- %s,%s,%s" %(n,artist,title,bitrate,size)
        return fsonglist

    def api_call(self,song_id):
        post_data = {'action': 'download', 'id': song_id}
        response = requests.post(self.api_url, params=post_data)
        return response.json()


    def show_progressbar(self,current_value, max_value):
        percentage = (float(current_value) / float(max_value)) * 100.0
        sys.stdout.write('{0} of {1} bytes read. {2:.2f}% completed.'
                         .format(current_value, max_value, percentage))
        sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.flush()


    def download_file(self,url, local_filename):
        response = requests.get(url, stream=True,headers=self.headers)
        file_size = int(response.headers.get('content-length'))
        bytes_read = 0
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    self.show_progressbar(bytes_read, file_size)
                    f.write(chunk)
                    f.flush()
                    bytes_read += len(chunk)
        self.show_progressbar(file_size, file_size)

    def display_results(self,search_string, n):
        songlist= self.get_tracks(search_string,n)
        self.show_results(songlist)
        user_prompt = "Enter the song # to download, or press [Enter] to exit:"
        user_choice = raw_input(user_prompt)
        if user_choice:
            while int(user_choice) >=0:
                user_choice = int(user_choice)
                song_id = songlist[user_choice]['id']
                api_response = self.api_call(song_id)
                download_url = str(api_response['track_link'])
                print('Song found! Downloading..')
                file_name = u'{0}-{1}.mp3'.format(songlist[user_choice]['artist'],songlist[user_choice]['title'])
                self.download_file(download_url, file_name)
                print(('\nFile saved as \'{0}\''.format(file_name)))
                user_choice = raw_input(user_prompt)
            print "Enter right number:"
        else:
            sys.exit(1)
                
    def main(self):
        parser = argparse.ArgumentParser(usage="-h for full usage")
        parser.add_argument('query',help='search query',nargs='+')
        parser.add_argument('-n', dest="maxnumber", help="max number of results",type=int)
        args = parser.parse_args()
        print('Searching..')
        search_string = " ".join(args.query).replace(' ', '+')
        try:
            self.display_results(search_string,args.maxnumber)
        except requests.exceptions.ConnectionError:
            print("[ERROR] Server unreachable!")

if __name__ == "__main__":
        Pleer().main()
       

