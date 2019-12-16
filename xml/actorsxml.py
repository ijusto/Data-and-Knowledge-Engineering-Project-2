# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import urllib3.request
import requests

count = 0
line_count = 0

def main():
    # people xml

    csv = open("movie_metadata_final.csv", "r")
    xml = open("people.xml", "w")

    xml.write("<?xml version=\"1.0\"?>\n")
    xml.write("<people>\n")
    actors_list = {}
    directors_list = {}

    while True:
        line_t = csv.readline()
        line = re.compile(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))").split(line_t)
        if not line or line[0] == "":
            break
        global line_count
        line_count += 1
        print("line: "+str(line_count))

        movie_imdb_link = line[17].replace("\"", "").strip()                            #  http: // www.imdb.com / title / tt2975590 /?ref_ = fn_tt_tt_1
        director_name = line[1].replace("\"", "").strip()
        print("\n--------------------------------------\ndir name: "+director_name)
        if director_name not in directors_list:
            director_url = find_dir_profile_link(movie_imdb_link, director_name)
            if director_url is not None:
                try:
                    image = (BeautifulSoup(requests.get
                                          (director_url).text, "html.parser").find
                                          ('img', {'id': 'name-poster'})['src'])
                    print("Image "+image+"\n")
                except :
                    image = None
                    print("Image None\n")
                bio = get_actor_bio(director_url)
                print("Bio "+bio+"\n")
                if image is not None:
                    print("writen")
                    directors_list[director_name] = [image, bio]
                    xml.write("\t\t<director>\n")
                    xml.write(f"\t\t\t<name>{director_name}</name>\n")
                    xml.write(f"\t\t\t<img>{image}</img>\n")
                    xml.write(f"\t\t\t<bio>{bio}</bio>\n")
                    xml.write("\t\t</director>\n")

        actor_2_name = line[6].replace("\"", "").strip()
        print("\n--------------------------------------\nactor name: "+actor_2_name)
        if actor_2_name not in actors_list:
            actor_url = find_profile_link(movie_imdb_link, actor_2_name)
            if actor_url is not None:
                try:
                    image = (BeautifulSoup(requests.get
                                          (actor_url).text, "html.parser").find
                                          ('img', {'id': 'name-poster'})['src'])
                    print("Image "+image+"\n")
                except :
                    image = None
                    print("Image None\n")
                bio = get_actor_bio(actor_url)
                print("Bio "+bio+"\n")
                if image is not None:
                    actors_list[actor_2_name] = [image, bio]
                    xml.write("\t\t<actor>\n")
                    xml.write(f"\t\t\t<name>{actor_2_name}</name>\n")
                    xml.write(f"\t\t\t<img>{image}</img>\n")
                    xml.write(f"\t\t\t<bio>{bio}</bio>\n")
                    xml.write("\t\t</actor>\n")

        actor_1_name = line[10].replace("\"", "").strip()
        print("\n--------------------------------------\nactor name: "+actor_1_name)
        if actor_1_name not in actors_list:
            actor_url = find_profile_link(movie_imdb_link, actor_1_name)
            if actor_url is not None:
                try:
                    image = (BeautifulSoup(requests.get
                                          (actor_url).text, "html.parser").find
                                          ('img', {'id': 'name-poster'})['src'])
                    print("Image "+image+"\n")
                except :
                    image = None
                    print("Image None\n")
                bio = get_actor_bio(actor_url)
                print("Bio "+bio+"\n")
                if image is not None:
                    actors_list[actor_1_name] = [image, bio]
                    xml.write("\t\t<actor>\n")
                    xml.write(f"\t\t\t<name>{actor_1_name}</name>\n")
                    xml.write(f"\t\t\t<img>{image}</img>\n")
                    xml.write(f"\t\t\t<bio>{bio}</bio>\n")
                    xml.write("\t\t</actor>\n")


        actor_3_name = line[14].replace("\"", "").strip()
        print("\n--------------------------------------\nactor name: "+actor_3_name)
        if actor_3_name not in actors_list:
            actor_url = find_profile_link(movie_imdb_link, actor_3_name)
            if actor_url is not None:
                try:
                    image = (BeautifulSoup(requests.get
                                          (actor_url).text, "html.parser").find
                                          ('img', {'id': 'name-poster'})['src'])
                    print("Image "+image+"\n")
                except:
                    print("Image None\n")
                    image = None
                bio = get_actor_bio(actor_url)
                print("Bio "+bio+"\n")
                if image is not None:
                    actors_list[actor_3_name] = [image, bio]
                    xml.write("\t\t<actor>\n")
                    xml.write(f"\t\t\t<name>{actor_3_name}</name>\n")
                    xml.write(f"\t\t\t<img>{image}</img>\n")
                    xml.write(f"\t\t\t<bio>{bio}</bio>\n")
                    xml.write("\t\t</actor>\n")

    csv.close()
    xml.write("</people>\n")
    xml.close()


def find_profile_link(url, actorname):
    soup= (BeautifulSoup(requests.get(url).text, "html.parser"))

    divs = soup.find_all('div', {'class':'credit_summary_item'})

    mydiv = None

    for div in divs:
        if "Stars:" in div.h4.text:
            mydiv = div

    actors = mydiv.find_all('a')

    for a in actors:
        if actorname in a.text:
            global count
            count += 1
            print("actor " + actorname + "count: " + str(count))
            return "http://www.imdb.com" + a['href']
    print("None actor")
    return None

def find_dir_profile_link(url, dirname):
    soup= (BeautifulSoup(requests.get(url).text, "html.parser"))

    divs = soup.find_all('div', {'class':'credit_summary_item'})

    mydiv = None

    for div in divs:
        if "Director:" in div.h4.text:
            mydiv = div

    if mydiv is not None:
        a = mydiv.find('a')
        if dirname in a.text:
            global count
            count += 1
            print("dir " + dirname + "count: " + str(count))
            return "http://www.imdb.com" + a['href']
    print("None director")

    return None

def get_actor_bio(url):
    link_bio = url + "bio"
    bio_text = (BeautifulSoup(requests.get
                              (link_bio).text, "html.parser").find
                              ('div', {'class': 'soda odd'}))

    bio = ""
    if bio_text is not None:
        bio_text = bio_text.find_all("p")
        for text in bio_text:
            bio += text.text

    return bio

if __name__ == '__main__':
    main()
