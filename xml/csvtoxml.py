# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import urllib3.request
import requests


csv = open("movie_metadata_final.csv", "r")
xml = open("movies.xml", "w")

xml.write("<?xml version=\"1.0\"?>\n<movies>\n")

while True:
    line_t = csv.readline()
    line = re.compile(",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))").split(line_t)
    if not line or line[0]=="":
        break

    color = line[0].replace("\"", "").strip()                                       #  Color
    director_name = line[1].replace("\"", "")                                       #  Zack Snyder
    d_fn = director_name.split(" ")[0].strip()
    d_ln = director_name.split(" ")[len(director_name.split(" "))-1].strip()
    num_critic_for_reviews = line[2].replace("\"", "").strip()                      #  673
    duration = line[3].replace("\"", "").strip()                                    #  183strip
    director_facebook_likes = line[4].replace("\"", "").strip()                     #  0
    actor_3_facebook_likes = line[5].replace("\"", "")  .strip()                    #  2000
    actor_2_name = line[6].replace("\"", "")                                        #  Lauren Cohan
    a2_fn = actor_2_name.split(" ")[0].strip()
    a2_ln = actor_2_name.split(" ")[len(actor_2_name.split(" "))-1].strip()
    actor_1_facebook_likes = line[7].replace("\"", "").strip()                      #  15000
    gross = line[8].replace("\"", "").strip()                                       #  330249062

    # list of diferent genres
    genres = line[9].split("|")                                                     #  Action | Adventure | Sci - Fi

    actor_1_name = line[10].replace("\"", "")                                       #  Henry Cavill
    a1_fn = actor_1_name.split(" ")[0].strip()
    a1_ln = actor_1_name.split(" ")[len(actor_1_name.split(" "))-1].strip()
    movie_title = line[11].replace("\"", "").strip()                                #  Batman v Superman: Dawn of Justice 
    num_voted_users = line[12].replace("\"", "").strip()                            #  371639
    cast_total_facebook_likes = line[13].replace("\"", "").strip()                  #  24450
    actor_3_name = line[14].replace("\"", "")                                       #  Alan D.Purwin
    a3_fn = actor_3_name.split(" ")[0].strip()
    a3_ln = actor_3_name.split(" ")[len(actor_3_name.split(" "))-1].strip()
    facenumber_in_poster = line[15].replace("\"", "").strip()                       #  0

    # list of keywords
    plot_keywords = line[16].split("|")                                             #  based on comic book | batman | sequel to a reboot | superhero | superman
    movie_imdb_link = line[17].replace("\"", "").strip()                            #  http: // www.imdb.com / title / tt2975590 /?ref_ = fn_tt_tt_1
    image = (BeautifulSoup(requests.get
                           (movie_imdb_link).text, "html.parser").find
                                ('div', {'class': 'poster'}).find('img')['src'])
    num_user_for_reviews = line[18].replace("\"", "").strip()                       #  3018
    language = line[19].replace("\"", "").strip()                                   #  English
    country = line[20].replace("\"", "").strip()                                    #  USA
    content_rating = line[21].replace("\"", "").strip()                             #  PG - 13
    budget = line[22].replace("\"", "").strip()                                     #  250000000
    title_year = line[23].replace("\"", "").strip()                                 #  2016
    actor_2_facebook_likes = line[24].replace("\"", "").strip()                     #  4000
    imdb_score = line[25].replace("\"", "").strip()                                 #  6.9
    aspect_ratio = line[26].replace("\"", "").strip()                               #  2.35
    movie_facebook_likes = line[27].replace("\"", "").strip()                       #  197000

    movie = f"\t<movie color=\"{color}\"\n" \
            f"\t\trating=\"{content_rating}\"\n" \
            f"\t\tcountry=\"{country}\"\n" \
            f"\t\tlanguage=\"{language}\"\n" \
            f"\t\taspect_ratio=\"{aspect_ratio}\"\n" \
            f"\t\tduration=\"{duration}\"\n" \
            f"\t\tbudget=\"{budget}\"\n" \
            f"\t\tfb_likes=\"{movie_facebook_likes}\"\n" \
            f"\t\tgross=\"{gross}\"\n" \
            f"\t\tnum_user_for_reviews=\"{num_user_for_reviews}\"\n" \
            f"\t\tfacenumber_in_poster=\"{facenumber_in_poster}\"\n" \
            f"\t>\n" \

    movie += f"\t\t<title>\n" \
             f"\t\t\t<name>{movie_title}</name>\n" \
             f"\t\t\t<year>{title_year}</year>\n" \
             f"\t\t</title>\n"

    movie += f"\t\t<poster>{image}</poster>\n"

    movie += f"\t\t<imbd_info>\n" \
             f"\t\t\t<score num_voted_users=\"{num_voted_users}\"\n" \
             f"\t\t\t\tnum_critic_for_reviews=\"{num_critic_for_reviews}\">\n" \
             f"\t\t\t\t{imdb_score}\n" \
             f"\t\t\t</score>\n" \
             f"\t\t\t<link>{movie_imdb_link}</link>\n" \
             f"\t\t</imbd_info>\n"

    movie += f"\t\t<cast fb_likes=\"{cast_total_facebook_likes}\">\n"\
             f"\t\t\t<main_actors>\n" \
             f"\t\t\t\t<person>\n" \
             f"\t\t\t\t\t<name>\n" \
             f"\t\t\t\t\t\t<first_name>{a1_fn}</first_name>\n" \
             f"\t\t\t\t\t\t<last_name>{a1_ln}</last_name>\n" \
             f"\t\t\t\t\t</name>\n" \
             f"\t\t\t\t\t<facebook_likes>{actor_1_facebook_likes}</facebook_likes>\n" \
             f"\t\t\t\t\t<profession>Actor</profession>\n" \
             f"\t\t\t\t</person>\n" \
             f"\t\t\t\t<person>\n" \
             f"\t\t\t\t\t<name>\n" \
             f"\t\t\t\t\t\t<first_name>{a2_fn}</first_name>\n" \
             f"\t\t\t\t\t\t<last_name>{a2_ln}</last_name>\n" \
             f"\t\t\t\t\t</name>\n" \
             f"\t\t\t\t\t<facebook_likes>{actor_2_facebook_likes}</facebook_likes>\n" \
             f"\t\t\t\t\t<profession>Actor</profession>\n" \
             f"\t\t\t\t</person>\n" \
             f"\t\t\t\t<person>\n" \
             f"\t\t\t\t\t<name>\n" \
             f"\t\t\t\t\t\t<first_name>{a3_fn}</first_name>\n" \
             f"\t\t\t\t\t\t<last_name>{a3_ln}</last_name>\n" \
             f"\t\t\t\t\t</name>\n" \
             f"\t\t\t\t\t<facebook_likes>{actor_3_facebook_likes}</facebook_likes>\n" \
             f"\t\t\t\t\t<profession>Actor</profession>\n" \
             f"\t\t\t\t</person>\n" \
             f"\t\t\t</main_actors>\n" \
             f"\t\t</cast>\n"

    movie += f"\t\t<director>\n" \
             f"\t\t\t<person>\n" \
             f"\t\t\t\t<name>\n" \
             f"\t\t\t\t\t<first_name>{d_fn}</first_name>\n" \
             f"\t\t\t\t\t<last_name>{d_ln}</last_name>\n" \
             f"\t\t\t\t</name>\n" \
             f"\t\t\t\t<facebook_likes>{director_facebook_likes}</facebook_likes>\n" \
             f"\t\t\t\t<profession>Movie Director</profession>\n" \
             f"\t\t\t</person>\n" \
             f"\t\t</director>\n"

    movie += f"\t\t<genres>\n"
    for genre in genres:
        genre_t = genre.replace("\"", "").strip()
        movie += f"\t\t\t<genre>{genre_t}</genre>\n"
    movie += f"\t\t</genres>\n"

    movie += f"\t\t<plot_keywords>\n"
    for keyword in plot_keywords:
        keyword_t = keyword.replace("\"", "").strip()
        movie += f"\t\t\t<keyword>{keyword_t}</keyword>\n"
    movie += f"\t\t</plot_keywords>\n"

    movie += f"\t</movie>\n"

    xml.write(movie)
    print("wrote movie " + movie_title)


xml.write("</movies>\n")

csv.close()
xml.close()