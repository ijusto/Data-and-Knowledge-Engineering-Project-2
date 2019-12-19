# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import urllib3.request
import requests

xml = open("movies_short.xml", "r")
n3 = open("movies.n3", "w")

n3.write('@prefix mov: <http://moviesDB.com/entity/mov>.\n')
n3.write('@prefix person: <http://moviesDB.com/entity/person/>.\n')
n3.write('@prefix genres: <http://moviesDB.com/entity/genres/>.\n')
n3.write('@prefix ratings: <http://moviesDB.com/entity/ratings/>.\n')
n3.write('@prefix predicate: <http://moviesDB.com/predicate/>.\n')

n3.write('genres:horror predicate:name "Horror".\n')
n3.write('genres:mystery predicate:name "Mystery".\n')
n3.write('genres:thriller predicate:name "Thriller".\n')
n3.write('genres:action predicate:name "Action".\n')
n3.write('genres:adventure predicate:name "Adventure".\n')
n3.write('genres:fantasy predicate:name "Fantasy".\n')
n3.write('genres:sci_fi predicate:name "Sci-Fi".\n')
n3.write('genres:romance predicate:name "Romance".\n')
n3.write('genres:animation predicate:name "Animation".\n')
n3.write('genres:comedy predicate:name "Comedy".\n')
n3.write('genres:family predicate:name "Family".\n')
n3.write('genres:musical predicate:name "Musical".\n')
n3.write('genres:western predicate:name "Western".\n')
n3.write('genres:drama predicate:name "Drama".\n')
n3.write('genres:history predicate:name "History".\n')
n3.write('genres:crime predicate:name "Crime".\n')
n3.write('genres:war predicate:name "War".\n')
n3.write('genres:biography predicate:name "Biography".\n')
n3.write('genres:music predicate:name "Music".\n')

n3.write('ratings:r predicate:name "R".\n')
n3.write('ratings:pg predicate:name "PG".\n')
n3.write('ratings:pg_13 predicate:name "PG-13".\n')
n3.write('ratings:g predicate:name "G".\n')

person = {}
person_info = {}
read_movie = False
movies_dict = {}

line_t = ""

while "<movies>" not in line_t:
    # ?xml version="1.0"?>
    # <movies>
    line_t = xml.readline()
    print(line_t + "\n")

movie_dic = {}

while True:
    # <movie color="Color"
    line_t = xml.readline()
    print("<movie color=\"Color\"\n"+ line_t+ "\n")

    if not line_t or line_t == "":
        break

    if "<movie " in line_t:
        read_movie = True
        movie_dic = {}

        color = line_t.split("\"")[1]
        print("<movie color=\"Color\"\n"+ color+ "\n")

        # rating="PG-13"
        rating = xml.readline().split("\"")[1].lower().replace("-","_")
        print("rating=\"PG-13\"\n"+rating+ "\n")

        # country="USA"
        country = xml.readline().split("\"")[1]
        print("country=\"USA\"\n"+country+ "\n")

        # language="English"
        language = xml.readline().split("\"")[1]
        print("language=\"English\"\n"+language+ "\n")

        # aspect_ratio="1.78"
        aspect_ratio = xml.readline().split("\"")[1]
        print("aspect_ratio=\"1.78\"\n"+aspect_ratio+ "\n")

        # duration="178"
        duration = xml.readline().split("\"")[1]
        print("duration=\"178\"\n"+duration+ "\n")

        # budget="237000000"
        budget = xml.readline().split("\"")[1]
        print("budget=\"237000000\"\n"+budget+ "\n")

        # fb_likes="33000"
        fb_likes = xml.readline().split("\"")[1]
        print("fb_likes=\"33000\"\n"+fb_likes+ "\n")

        # gross="760505847"
        gross = xml.readline().split("\"")[1]
        print("gross=\"760505847\"\n"+gross+ "\n")

        # num_user_for_reviews="3054"
        num_user_for_reviews = xml.readline().split("\"")[1]
        print("num_user_for_reviews=\"3054\"\n"+num_user_for_reviews+ "\n")

        # facenumber_in_poster="0"
        facenumber_in_poster = xml.readline().split("\"")[1]
        print("facenumber_in_poster=\"0\"\n"+facenumber_in_poster+ "\n")

        # >
        xml.readline()

        # <title>
        xml.readline()

        # <name>Avatar</name>
        name = xml.readline().split("name")[1].replace(">", "").replace("</", "").replace("/", " ").replace("!","")
        entname = name.strip().replace(" ", "_").replace("-","_").replace(":", "").replace(",","").replace(".","")
        print("<name>Avatar</name>\n"+entname+ "\n")
        n3.write("mov:" + entname.lower() + "\n")
        n3.write("\tpredicate:name \"" + name + "\";\n")

        # <year>2009</year>
        year = xml.readline().split("year")[1].replace(">", "").replace("</", "")
        print("<year>2009</year>\n"+year+ "\n")
        n3.write("\tpredicate:year \"" + year + "\";\n")

        # </title>
        xml.readline()

        # <poster>
        #xml.readline()

        # https://m.media-amazon.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_UX182_CR0,0,182,268_AL_.jpg
        poster = xml.readline().split("poster")[1].replace(">", "").replace("</", "")
        print("https://m.media-amazon.com/images/M/MV5BMTYwOTEwNjAzMl5BMl5BanBnXkFtZTcwODc5MTUwMw@@._V1_UX182_CR0,0,182,268_AL_.jpg\n"
              +poster+ "\n")

        # </poster>
        #xml.readline()

        # <imbd_info>
        xml.readline()

        # <score num_voted_users="886204"
        wtf = xml.readline().split("\"")
        print("AQUI: "+ str(wtf))
        num_voted_users = wtf[1]
        print("<score num_voted_users=\"886204\"\n"+num_voted_users+ "\n")

        # num_critic_for_reviews="723">
        num_critic_for_reviews = xml.readline().split("\"")[1]
        print("num_critic_for_reviews=\"723\">\n"+num_critic_for_reviews+ "\n")

        # 7.9
        score = xml.readline().strip()
        n3.write("\tpredicate:score \"" + score + "\";\n")
        print("7.9\n"+score+ "\n")

        # </score>
        xml.readline()

        # <link>http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1</link>
        link = xml.readline().split("link")[1].replace(">", "").replace("</", "")
        print("<link>http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1</link>\n"+link+ "\n")

        # </imbd_info>
        xml.readline()

        # <cast fb_likes="4834">
        xml.readline()

        # <main_actors>
        xml.readline()
        n3.write("\tpredicate:actor \n")

        # <person>
        xml.readline()
        person_info = {}

        # <name>
        xml.readline()

        # <first_name>CCH</first_name>
        first_name = xml.readline().strip().split("first_name")[1].replace(">", "").replace("</", "").replace("'","").replace("-", "_")
        print("<first_name>CCH</first_name>\n"+first_name+ "\n")

        # <last_name>Pounder</last_name>
        last_name = xml.readline().strip().split("last_name")[1].replace(">", "").replace("</", "").replace(".","").replace("'","").replace("-", "_")
        print("<last_name>Pounder</last_name>\n" + last_name + "\n")

        person_name = first_name + "_" + last_name
        n3.write("\t\t\tperson:" + person_name + ",\n")

        # </name>
        xml.readline()

        # <facebook_likes>1000</facebook_likes>
        person_info["facebook_likes"] = xml.readline().split("facebook_likes")[1].replace(
            ">", "").replace("</", "")

        # <profession>Actor</profession>
        person_info["profession"] = xml.readline().split("profession")[1].replace(">", "").replace("</", "")

        # </person>
        xml.readline()
        person[person_name] = person_info

        # <person>
        person_info = {}
        xml.readline()

        # <name>
        xml.readline()

        # <first_name>Joel</first_name>
        first_name = xml.readline().strip().split("first_name")[1].replace(">", "").replace("</", "").replace("'","").replace("-", "_")

        # <last_name>Moore</last_name>
        last_name = xml.readline().strip().split("last_name")[1].replace(">", "").replace("</", "").replace(".","").replace("'","").replace("-", "_")

        person_name = first_name + "_" + last_name
        n3.write("\t\t\tperson:" + person_name + ",\n")

        # </name>
        xml.readline()

        # <facebook_likes>936</facebook_likes>
        person_info["facebook_likes"] = xml.readline().split("facebook_likes")[1].replace(
            ">", "").replace("</", "")

        # <profession>Actor</profession>
        person_info["profession"] = xml.readline().split("profession")[1].replace(">", "").replace("</", "")

        # </person>
        xml.readline()
        person[person_name] = person_info

        # <person>
        xml.readline()
        person_info = {}

        # <name>
        xml.readline()

        # <first_name>Wes</first_name>
        first_name = xml.readline().strip().split("first_name")[1].replace(">", "").replace("</", "").replace("'","").replace("-", "_")

        # <last_name>Studi</last_name>
        last_name = xml.readline().strip().split("last_name")[1].replace(">", "").replace("</", "").replace(".","").replace("'","").replace("-", "_")

        person_name = first_name + "_" + last_name
        n3.write("\t\t\tperson:" + person_name + ";\n")

        # </name>
        xml.readline()

        # <facebook_likes>855</facebook_likes>
        person_info["facebook_likes"] = xml.readline().split("facebook_likes")[1].replace(
            ">", "").replace("</", "")

        # <profession>Actor</profession>
        person_info["profession"] = xml.readline().split("profession")[1].replace(">", "").replace("</", "")

        # </person>
        xml.readline()
        person[person_name] = person_info

        # </main_actors>
        xml.readline()

        # </cast>
        xml.readline()

        # <director>
        xml.readline()
        n3.write("\tpredicate:poster \"" + poster + "\";\n")
        n3.write("\tpredicate:director \n")

        # <person>
        xml.readline()
        person_info = {}

        # <name>
        xml.readline()

        # <first_name>James</first_name>
        first_name = xml.readline().strip().split("first_name")[1].replace(">", "").replace("</", "").replace("'","").replace("-", "_")

        # <last_name>Cameron</last_name>
        last_name = xml.readline().strip().split("last_name")[1].replace(">", "").replace("</", "").replace(".","").replace("'","").replace("-", "_")

        person_name = first_name + "_" + last_name
        n3.write("\t\t\tperson:" + person_name + ";\n")

        # </name>
        xml.readline()

        # <facebook_likes>0</facebook_likes>
        person_info["facebook_likes"] = xml.readline().split("facebook_likes")[1].replace(
            ">", "").replace("</", "")

        # <profession>Movie Director</profession>
        person_info["profession"] = xml.readline().split("profession")[1].replace(">", "").replace("</", "")

        # </person>
        xml.readline()
        person[person_name] = person_info

        # </director>
        xml.readline()

        # <genres>
        new_line_genres = xml.readline()
        n3.write("\tpredicate:genre \n")
        read_genres = False
        while "</genres>" not in new_line_genres.strip():
            new_line_genres = xml.readline()
            # </genres>
            if "</genres>" in new_line_genres:
                n3.write(";\n")
                break
            elif read_genres:
                n3.write(",\n")
            # <genre>Action</genre>
            if "<genre>" in new_line_genres:
                read_genres = True
                genre = new_line_genres.split("genre")[1].replace(">", "").replace("</", "")
                n3.write("\t\t\tgenres:" + genre.lower())

        # <plot_keywords>
        new_line_pkw = xml.readline()
        read_pkw = False
        n3.write("\tpredicate:plot_keyword \n")
        while "</plot_keywords>" not in new_line_pkw.strip():
            new_line_pkw = xml.readline()
            # </plot_keywords>
            if "</plot_keywords>" in new_line_pkw:
                n3.write(";\n")
                break
            elif read_pkw:
                n3.write(",\n")
            # <keyword>future</keyword>
            if "<keyword>" in new_line_pkw:
                read_pkw = True
                keyword = new_line_pkw.split("keyword")[1].replace(">", "").replace("</", "")
                n3.write("\t\t\t\"" + keyword.lower() + "\"")

        # 	</movie>
        xml.readline()
        # passar ao proximo filme
        read_movie = False
        n3.write("\tpredicate:country \"" + country + "\";\n")
        n3.write("\tpredicate:language \"" + language + "\";\n")
        n3.write("\tpredicate:rating ratings:" + rating + ";\n")
        n3.write("\tpredicate:duration \"" + duration + "\";\n")
        n3.write("\tpredicate:budget \"" + budget + "\".\n")

#for p, p_info in person.items():
#    n3.write("person:" + p + "\n")
#    print("person:" + p + "\n")
#    for k, v in p_info.items():
#        n3.write("\tpredicate:" + k + "\"" + v + "\"\n")
#        print("\tpredicate:" + k + "\"" + v + "\"\n")

xml.close()
xml = open("people.xml", "r")

# <?xml version="1.0"?>
line_t = xml.readline()
# people
line_t = xml.readline()
person = {}
while True:
    # <director> or <actor>
    line_t = xml.readline()
    if "</people>" in line_t:
        break
    print("<director> or <actor>\n"+line_t+ "\n")
    profession = ""
    if "director" in line_t:
        profession = "\"Director\""
    elif "actor" in line_t:
        profession = "\"Actor\""

    # <name>James Cameron</name>
    line_t = xml.readline()
    name = "\"" + line_t.split("name")[1].replace(">", "").replace("</", "").replace(".","").replace("'","") + "\""
    print("<name>James Cameron</name>\n"+name+ "\n")
    ent = name.strip().replace(" ", "_").replace("\"","").replace("-", "_")

    # <img> https: /... </img>
    img = "\"" + xml.readline().split("img")[1].replace(">", "").replace("</", "") + "\""

    # <bio>
    xml.readline()

    # first line bio
    line_t = xml.readline()

    bio = ""
    while "</bio>" not in line_t:
        bio += line_t.strip() + " "
        line_t = xml.readline()

    # </director>
    xml.readline()

    if ent in person.keys():
        if profession not in person[ent]["profession"]:
            person[ent]["profession"] += [profession]
    else:
        person_info = {}
        person_info["name"] = name
        person_info["ent"] = ent
        person_info["img"] = img
        person_info["bio"] = "\"" + bio.replace("\"", "\\\"") + "\""
        if profession != "":
            person_info["profession"] = [profession]
        person[ent] = person_info

xml.close()

for ent, person_info in person.items():
    n3.write("person:" + ent + "\n\t\tpredicate:name " + person_info["name"] + ";\n\t\tpredicate:profession ")
    profs = str(person_info["profession"]).replace("[","").replace("]",";").replace(",",",\n\t\t\t\t").replace("'","")
    n3.write(profs + "\n\t\tpredicate:image " + person_info["img"] + ";\n\t\tpredicate:bio " + person_info["bio"] + ".\n")
n3.close()
