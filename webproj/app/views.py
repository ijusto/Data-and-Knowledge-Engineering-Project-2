from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from webproj.settings import BASE_DIR
import os
import lxml.etree as ET
import xmltodict
from BaseXClient import BaseXClient
import requests
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


def new_movie(request):
    assert isinstance(request, HttpRequest)
    dict = {
        "movies": {
            "movie": {
                "@language": "XXX",
                "@rating": "",
                "@budget": 0,
                "@duration": "",
                "@country": "XXX",
                "title": {
                    "name": "",
                    "year": ""
                },
                "poster": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcT16wQWF2p4_8GBLCNAMR9tOfs-q7o1TpLN23n7obheV5IroABG&fbclid=IwAR0YOgN094aLmuX7Z0VMd9xyXgiBZDQu7-HXpB7NAEm8CKiWxz_8JUQJ1nE",
                "imbd_info": {
                    "score": "?",
                },
                "cast": {
                    "main_actors": {
                        "person": []
                    }
                },
                "director": "",
                "genres": {
                    "genre": []
                }
            }}}

    if 'title' in request.POST:
        if request.POST['title'] != "":
            dict['movies']['movie']['title']['name'] = request.POST['title']
    if 'year' in request.POST:
        if request.POST['year'] != "":
            dict['movies']['movie']['title']['year'] = request.POST['year']
    if 'first_name1' and 'last_name1' in request.POST:
        if request.POST['first_name1'] != "" and request.POST['last_name1']!="":
            dict["movies"]["movie"]['director'] = {
                "person" : {
                    "name" :{
                         "first_name" : request.POST['first_name1'],
                         "last_name" : request.POST['last_name1'],
                    }
                }
            }
    if 'first_name2' and 'last_name2' in request.POST:
        if request.POST['first_name2'] != "" and request.POST['last_name2'] != "":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name" :{
                                    "first_name" : request.POST['first_name2'],
                                    "last_name" : request.POST['last_name2'],
                                }
                            })
    if 'first_name3' and 'last_name3' in request.POST:
        if request.POST['first_name3'] != "" and request.POST['last_name3'] != "":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name":{
                                    "first_name" : request.POST['first_name3'],
                                    "last_name" : request.POST['last_name3'],
                                }
                            })
    if 'first_name4' and 'last_name4' in request.POST:
        if request.POST['first_name4'] != "" and request.POST['last_name4'] != "":
            dict["movies"]["movie"]['cast']['main_actors']['person'].append({
                                "name":{
                                    "first_name" : request.POST['first_name4'],
                                    "last_name" : request.POST['last_name4'],
                                }
                            })
    if 'genre1' in request.POST:
        if request.POST['genre1'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre1'])
    if 'genre2' in request.POST:
        if request.POST['genre2'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre2'])
    if 'genre3' in request.POST:
        if request.POST['genre3'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre3'])
    if 'genre4' in request.POST:
        if request.POST['genre4'] != "":
            dict["movies"]["movie"]['genres']['genre'].append(request.POST['genre4'])
    if 'budget' in request.POST:
        if request.POST['budget'] != "":
            dict["movies"]["movie"]['@budget'] = request.POST['budget']
    if 'country' in request.POST:
        if request.POST['country'] != "":
            dict["movies"]["movie"]['@country'] = request.POST['country']
    if 'duration' in request.POST:
        if request.POST['duration'] != "":
            dict["movies"]["movie"]['@duration'] = request.POST['duration']
    if 'rating' in request.POST:
        if request.POST['rating'] != "":
            dict["movies"]["movie"]['@rating'] = request.POST['rating']

    xml_newmovie=xmltodict.unparse(dict, pretty=True)
    xsd_name = 'moviesSchema.xsd'
    xsd_file = os.path.join(BASE_DIR, 'app/data/' + xsd_name)
    tree = ET.fromstring(bytes(xml_newmovie, 'utf-8'))
    xsd_parsed = ET.parse(xsd_file)
    xsd = ET.XMLSchema(xsd_parsed)

    if 'title' in request.POST:
        title = request.POST['title']
        year = request.POST['year']
        if xsd.validate(tree):
            session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

            session.execute("open moviesDB")
            xml_newmovie = xml_newmovie.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>", "")

            input1 = "import module namespace movies = 'com.movies' at '" \
                     + os.path.join(BASE_DIR, 'app/data/queries/queries.xq') \
                     + "';movies:ins_movie(" + xml_newmovie + ")"
            query1 = session.query(input1)
            query1.execute()

            session.close()
            return show_movie(request, title)
        else:
            return render(
                request,
                'newMovie.html',
                {
                    'error': True,
                }
            )
    else:
        return render(
            request,
            'newMovie.html',
            {
                'error': False,
            }
        )


def movies_news_feed(request):
    xml_link = "https://www.cinemablend.com/rss/topic/news/movies"
    xml_file = requests.get(xml_link)
    xslt_name = 'rss.xsl'
    xsl_file = os.path.join(BASE_DIR, 'app/data/xslts/' + xslt_name)
    tree = ET.fromstring(xml_file.content)
    xslt = ET.parse(xsl_file)
    transform = ET.XSLT(xslt)
    newdoc = transform(tree)

    tparams = {
        'content': newdoc,
    }

    return render(request, 'news.html', tparams)


def movies_feed(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
        PREFIX mov: <http://moviesDB.com/predicate/>
    SELECT distinct ?genre_name
    WHERE { 
    	?movie mov:genre ?genre .
        ?genre mov:name ?genre_name .
    	}
    """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            genres.append(v['value'])

    query = """
            PREFIX pred: <http://moviesDB.com/predicate/>
            SELECT distinct ?year
            WHERE {
	        ?movie pred:year ?year .
} order by ?year
        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    years = []
    for e in res['results']['bindings']:
        for v in e.values():
            years.append(v['value'])

    query = """
            PREFIX pred: <http://moviesDB.com/predicate/>
            SELECT distinct ?rating_name
            WHERE {
	            ?movie pred:rating ?rating .
                ?rating pred:name ?rating_name .
            }
            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    ratings = []
    for e in res['results']['bindings']:
        for v in e.values():
            ratings.append(v['value'])

    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT ?title ?pred ?obj
                WHERE{
                    ?movie ?pred ?obj .
                    ?movie pred:director ?year .
                    ?movie pred:name ?title .
                }
               """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    movies = {}
    for e in res['results']['bindings']:
        if (e['title']['value'] not in movies.keys()):
            if len(movies) == 0:
                movies = {e['title']['value']: {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}}
            else:
                movies.update({e['title']['value']: {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}})
        else:
            if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                obj = movies[e['title']['value']][e['pred']['value'].split("/")[-1]]
            else:
                obj = [e['obj']['value']]
            if e['pred']['value'].split("/")[-1] == 'genre':
                i = e['obj']['value'].split("genres/")[1]
                query = """
                                          PREFIX genres: <http://moviesDB.com/entity/genres/>
                                        prefix predicate: <http://moviesDB.com/predicate/>
                                         select ?name where{
                                        genres:""" + i + """ predicate:name ?name.
                    }
                                        """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'director':
                obj = [e['obj']['value'].split("person/")[1]]
                movie_director = e['obj']['value'].split("person/")[1]
                query = """
                                      PREFIX person: <http://moviesDB.com/entity/person/>
                                       PREFIX predicate: <http://moviesDB.com/predicate/>
                                       SELECT ?name WHERE{
                                       person:""" + movie_director + """ predicate:name ?name.
                           }
                                   """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'actor':
                i = e['obj']['value'].split("person/")[1]
                query = """
                                              PREFIX person: <http://moviesDB.com/entity/person/>
                                            prefix predicate: <http://moviesDB.com/predicate/>
                                             select ?name where{
                                            person:""" + i + """ predicate:name ?name.
                        }
                                            """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
                if len(res['results']['bindings']) == 0:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(i)
                    else:
                        obj = [i]
            movies[e['title']['value']].update({e['pred']['value'].split("/")[-1]: obj})
    tparams = {
        'movies' : movies,
        "genres": genres,
        "ratings": ratings,
        "years": years
     }
    return render(request, 'index.html', tparams)


def apply_filters(request):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    session.execute("open moviesDB")

    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
            PREFIX mov: <http://moviesDB.com/predicate/>
        SELECT distinct ?genre_name
        WHERE { 
        	?movie mov:genre ?genre .
            ?genre mov:name ?genre_name .
        	}
        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            genres.append(v['value'])

    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT distinct ?year
                WHERE {
    	        ?movie pred:year ?year .
    } order by ?year
            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    years = []
    for e in res['results']['bindings']:
        for v in e.values():
            years.append(v['value'])

    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT distinct ?rating_name
                WHERE {
    	            ?movie pred:rating ?rating .
                    ?rating pred:name ?rating_name .
                }
                """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    ratings = []
    for e in res['results']['bindings']:
        for v in e.values():
            ratings.append(v['value'])

    query = """
    PREFIX pred: <http://moviesDB.com/predicate/>
    SELECT distinct ?title ?pred ?obj
    WHERE {
        ?movie ?pred ?obj .
        ?movie pred:rating ?rating .
        ?movie pred:year ?year .
        ?movie pred:genre ?genre .
        ?rating pred:name ?rating_name .
        ?genre pred:name ?genre_name .
        ?movie pred:name ?title .
        ?movie pred:score ?score .
    """

    genresToQuery = []
    for g in genres:
        if g in request.POST:
            genresToQuery.append(g)

    if len(genresToQuery) != 0:
        aux = ""
        for g in genresToQuery:
            aux += "\""+g+"\","
        aux = aux[:-1]
        query += """FILTER(?genre_name IN("""+aux+"""))"""

    if 'ratings' in request.POST:
        query += """FILTER (?rating_name = \""""+request.POST['ratings']+"""\")"""

    if 'years' in request.POST:
        if request.POST['years'] != "":
            query += """FILTER (?year = \""""+request.POST['years']+"""\")"""

    query += """}"""

    if 'orderby' in request.POST:
        if request.POST['orderby'] != "":
            query += """ORDER BY ?"""+request.POST['orderby'].lower()+""""""

    movies = {}
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        if (e['title']['value'] not in movies.keys()):
            if len(movies) == 0:
                movies = {e['title']['value']: {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}}
            else:
                movies.update({e['title']['value']: {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}})
        else:
            if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                obj = movies[e['title']['value']][e['pred']['value'].split("/")[-1]]
            else:
                obj = [e['obj']['value']]
            if e['pred']['value'].split("/")[-1] == 'genre':
                i = e['obj']['value'].split("genres/")[1]
                query = """
                                              PREFIX genres: <http://moviesDB.com/entity/genres/>
                                            prefix predicate: <http://moviesDB.com/predicate/>
                                             select ?name where{
                                            genres:""" + i + """ predicate:name ?name.
                        }
                                            """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'director':
                obj = [e['obj']['value'].split("person/")[1]]
                movie_director = e['obj']['value'].split("person/")[1]
                query = """
                                          PREFIX person: <http://moviesDB.com/entity/person/>
                                           PREFIX predicate: <http://moviesDB.com/predicate/>
                                           SELECT ?name WHERE{
                                           person:""" + movie_director + """ predicate:name ?name.
                               }
                                       """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'actor':
                i = e['obj']['value'].split("person/")[1]
                query = """
                                                  PREFIX person: <http://moviesDB.com/entity/person/>
                                                prefix predicate: <http://moviesDB.com/predicate/>
                                                 select ?name where{
                                                person:""" + i + """ predicate:name ?name.
                            }
                                                """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
                if len(res['results']['bindings']) == 0:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(i)
                    else:
                        obj = [i]
            movies[e['title']['value']].update({e['pred']['value'].split("/")[-1]: obj})
    tparams = {
        'movies' : movies,
        "genres": genres,
        "ratings": ratings,
        "years": years
    }
    return render(request, 'index.html', tparams)


def apply_search(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
            PREFIX mov: <http://moviesDB.com/predicate/>
        SELECT distinct ?genre_name
        WHERE { 
        	?movie mov:genre ?genre .
            ?genre mov:name ?genre_name .
        	}
        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    genres = []
    for e in res['results']['bindings']:
        for v in e.values():
            genres.append(v['value'])

    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT distinct ?year
                WHERE {
    	        ?movie pred:year ?year .
    } order by ?year
            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    years = []
    for e in res['results']['bindings']:
        for v in e.values():
            years.append(v['value'])

    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT distinct ?rating_name
                WHERE {
    	            ?movie pred:rating ?rating .
                    ?rating pred:name ?rating_name .
                }
                """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    ratings = []
    for e in res['results']['bindings']:
        for v in e.values():
            ratings.append(v['value'])


    query = """
            PREFIX pred: <http://moviesDB.com/predicate/>
            SELECT  ?title ?pred ?obj
            WHERE {{
                ?movie ?pred ?obj .
                ?movie pred:name ?title .
                FILTER(CONTAINS(?title, \"""" + request.POST['search'] + """\"))
	        } UNION {
                ?movie ?pred ?obj .
                ?movie pred:name ?title .
                ?movie pred:plot_keyword ?keywords .
                FILTER(CONTAINS(?keywords, \""""+ request.POST['search'] +"""\"))
            }}
           """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    movies = {}
    for e in res['results']['bindings']:
        if(e['title']['value'] not in movies.keys()):
            if len(movies) == 0:
                movies = {e['title']['value'] : {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}}
            else:
                movies.update({e['title']['value'] : {e['pred']['value'].split("/")[-1]: [e['obj']['value']]}})
        else:
            if(e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                obj = movies[e['title']['value']][e['pred']['value'].split("/")[-1]]
            else:
                obj = [e['obj']['value']]
            if e['pred']['value'].split("/")[-1] == 'genre':
                i = e['obj']['value'].split("genres/")[1]
                query = """
                                      PREFIX genres: <http://moviesDB.com/entity/genres/>
                                    prefix predicate: <http://moviesDB.com/predicate/>
                                     select ?name where{
                                    genres:""" + i + """ predicate:name ?name.
                }
                                    """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'director':
                obj = [e['obj']['value'].split("person/")[1]]
                movie_director = e['obj']['value'].split("person/")[1]
                query = """
                                  PREFIX person: <http://moviesDB.com/entity/person/>
                                   PREFIX predicate: <http://moviesDB.com/predicate/>
                                   SELECT ?name WHERE{
                                   person:""" + movie_director + """ predicate:name ?name.
                       }
                               """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    obj = [f['name']['value']]
            elif e['pred']['value'].split("/")[-1] == 'actor':
                i = e['obj']['value'].split("person/")[1]
                query = """
                                          PREFIX person: <http://moviesDB.com/entity/person/>
                                        prefix predicate: <http://moviesDB.com/predicate/>
                                         select ?name where{
                                        person:""" + i + """ predicate:name ?name.
                    }
                                        """
                payload_query = {"query": query}
                res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
                res = json.loads(res)
                for f in res['results']['bindings']:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(f['name']['value'])
                    else:
                        obj = [f['name']['value']]
                if len(res['results']['bindings']) == 0:
                    if (e['pred']['value'].split("/")[-1] in movies[e['title']['value']].keys()):
                        obj.append(i)
                    else:
                        obj = [i]
            movies[e['title']['value']].update({e['pred']['value'].split("/")[-1] : obj})

        print(e)
    print(movies)
    tparams = {
        'movies' : movies,
        "genres": genres,
        "ratings": ratings,
        "years": years
    }
    return render(request, 'index.html', tparams)


def actors_list(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
                PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT distinct ?name
                WHERE { 
                    ?movie pred:actor ?actor .
                    ?actor pred:name ?name .
                    }
                """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    actors = []
    for e in res['results']['bindings']:
        for v in e.values():
            actors.append(v['value'].split(" "))
    print(actors)

    tparams = {
        'actors': actors,
    }
    return render(request, 'actors.html', tparams)

def apply_searchActor(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
        PREFIX pred: <http://moviesDB.com/predicate/>
        SELECT ?name
        WHERE { 
            ?movie pred:actor ?actor .
            ?actor pred:name ?name .
            FILTER (CONTAINS(?name, \""""+request.POST['search']+"""\"))
            }
                        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    actors = []
    for e in res['results']['bindings']:
        for v in e.values():
            actors.append(v['value'].split(" "))

    tparams = {
        'actors': actors,
    }
    return render(request, 'actors.html', tparams)


def apply_searchDirector(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
            PREFIX pred: <http://moviesDB.com/predicate/>
            SELECT ?name
            WHERE { 
                ?movie pred:director ?director .
                ?director pred:name ?name .
                FILTER (CONTAINS(?name, \"""" + request.POST['search'] + """\"))
                }
                            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    directors = []
    for e in res['results']['bindings']:
        for v in e.values():
            directors.append(v['value'].split(" "))

    tparams = {
        'directors': directors,
    }
    return render(request, 'directors.html', tparams)


def directors_list(request):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
                    PREFIX pred: <http://moviesDB.com/predicate/>
                    SELECT distinct ?name
                    WHERE { 
                        ?movie pred:director ?director .
                        ?director pred:name ?name .
	}
                    """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    directors = []
    for e in res['results']['bindings']:
        for v in e.values():
            directors.append(v['value'].split(" "))

    tparams = {
        'directors' : directors,
    }
    return render(request, 'directors.html', tparams)


def show_movie(request, movie):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
            PREFIX mov: <http://moviesDB.com/entity/mov>
        prefix predicate: <http://moviesDB.com/predicate/>
        select ?pred ?obj where{
            ?film ?pred ?obj.
            ?film predicate:name ?name
            filter regex(?name,\""""+movie+"""\",+\"i\").
    }
        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    movie_genres = []
    plot_keywords = []
    movie_secondary_actors = []
    movie_main_actors = []
    rating = ""
    for e in res['results']['bindings']:
        if "name" in e['pred']['value']:
            name = e['obj']['value']
        elif "year" in e['pred']['value']:
            year = e['obj']['value']
        elif "poster" in e['pred']['value']:
            poster = e['obj']['value']
        elif "poster" in e['pred']['value']:
            poster = e['obj']['value']
        elif "score" in e['pred']['value']:
            score = e['obj']['value']
        elif "actor" in e['pred']['value']:
            movie_main_actors.append(e['obj']['value'])
        elif "director" in e['pred']['value']:
            movie_director = e['obj']['value']
        elif "genre" in e['pred']['value']:
            movie_genres.append(e['obj']['value'])
        elif "plot_keyword" in e['pred']['value']:
            plot_keywords.append(e['obj']['value'])
        elif "country" in e['pred']['value']:
            country = e['obj']['value']
        elif "language" in e['pred']['value']:
            language = e['obj']['value']
        elif "rating" in e['pred']['value']:
            rating = e['obj']['value']
        elif "duration" in e['pred']['value']:
            duration = e['obj']['value']
        elif "budget" in e['pred']['value']:
            budget = e['obj']['value']

    rating = rating.split("ratings/")[1]
    query = """
               PREFIX ratings: <http://moviesDB.com/entity/ratings/>
                PREFIX predicate: <http://moviesDB.com/predicate/>
                SELECT ?name WHERE{
                ratings:"""+rating+""" predicate:name ?name.
    }
            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        rating = e['name']['value']


    genres=[]
    for i in movie_genres:
        i = i.split("genres/")[1]
        query = """
                      PREFIX genres: <http://moviesDB.com/entity/genres/>
                    prefix predicate: <http://moviesDB.com/predicate/>
                     select ?name where{
                    genres:"""+i+""" predicate:name ?name.
}
                    """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        for e in res['results']['bindings']:
            genres.append(e['name']['value'])

    movie_director = movie_director.split("person/")[1]
    query = """
                  PREFIX person: <http://moviesDB.com/entity/person/>
                   PREFIX predicate: <http://moviesDB.com/predicate/>
                   SELECT ?name WHERE{
                   person:""" + movie_director + """ predicate:name ?name.
       }
               """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        movie_director = e['name']['value']

    actors = []
    for i in movie_main_actors:
        i = i.split("person/")[1]
        query = """
                          PREFIX person: <http://moviesDB.com/entity/person/>
                        prefix predicate: <http://moviesDB.com/predicate/>
                         select ?name where{
                        person:""" + i + """ predicate:name ?name.
    }
                        """
        payload_query = {"query": query}
        res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
        res = json.loads(res)
        for e in res['results']['bindings']:
            actors.append(e['name']['value'])
        if len(res['results']['bindings']) == 0:
            actors.append(i)
    tparams = {
        'movie_name': name,
        'movie_img': poster,
        'movie_year': year,
        'movie_score': score,
        'movie_main_actors': actors,
        'movie_secondary_actors': movie_secondary_actors[1:],
        'movie_director': movie_director,
        'movie_genres': genres,
        'movie_rating': rating,
        'movie_language': language,
        'movie_country': country,
        'movie_duration': duration,
        'movie_plot_keywords': plot_keywords,
        'movie_budget': budget
    }
    return render(request, 'movie_page.html', tparams)


def actor_profile(request, actor):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
           PREFIX pred: <http://moviesDB.com/predicate/>
            PREFIX movies: <http://moviesDB.com/entity/movies/>
            SELECT distinct ?person ?pred ?obj
            WHERE {
                ?person pred:name \""""+actor.replace('_', ' ')+"""\".
                ?person ?pred ?obj.
            }
                        """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        if "name" in e['pred']['value']:
            name = e['obj']['value']
        elif "image" in e['pred']['value']:
            img = e['obj']['value']
        elif "bio" in e['pred']['value']:
            bio = e['obj']['value']

    query = """
              PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT ?mname
                WHERE { 
                    ?actor pred:name \""""+actor.replace('_',' ')+"""\" .
                    ?movie pred:actor ?actor .
                    ?movie pred:name ?mname .
                    }
                           """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    listMovies=[]
    for e in res['results']['bindings']:
        listMovies.append(e['mname']['value'])

    tparams = {
        'actor_img': img,
        'actor_bio': bio,
        'actor_name': name,
        'movies': listMovies,
    }
    return render(request, 'actor_profile.html', tparams)


def director_profile(request, director):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    query = """
               PREFIX pred: <http://moviesDB.com/predicate/>
                PREFIX movies: <http://moviesDB.com/entity/movies/>
                SELECT distinct ?person ?pred ?obj
                WHERE {
                    ?person pred:name \"""" + director.replace('_', ' ') + """\".
                    ?person ?pred ?obj.
                }
                            """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    for e in res['results']['bindings']:
        if "name" in e['pred']['value']:
            name = e['obj']['value']
        elif "image" in e['pred']['value']:
            img = e['obj']['value']
        elif "bio" in e['pred']['value']:
            bio = e['obj']['value']

    query = """
           PREFIX pred: <http://moviesDB.com/predicate/>
                SELECT ?mname
                WHERE { 
                    ?director pred:name \""""+director.replace('_',' ')+"""\" .
                    ?movie pred:director ?director .
                    ?movie pred:name ?mname .
                    }
                           """
    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    listMovies = []
    for e in res['results']['bindings']:
        print(e)
        listMovies.append(e['mname']['value'])

    tparams = {
        'director_img': img,
        'director_bio': bio,
        'director_name': name,
        'movies': listMovies,
    }
    return render(request, 'director_profile.html', tparams)


def delete_movie(request, movie):
    endpoint = "http://localhost:7200"
    repo_name = "moviesDB"
    client = ApiClient(endpoint=endpoint)
    accessor = GraphDBApi(client)
    update = """
        prefix predicate: <http://moviesDB.com/predicate/>
        DELETE {?film ?pred ?obj.} where{
        ?film ?pred ?obj.
        ?film predicate:name ?name.
        filter regex(?name,\""""+movie+"""\","i").
        }
        """
    payload_query = {"update": update}
    res = accessor.sparql_update(body=payload_query,
                                 repo_name=repo_name)
    return redirect('/')
