module namespace movies = "com.movies";

declare function movies:searcher($search) as element()*{
  for $bs in collection('moviesDB')/movies/movie
  for $p in $bs/plot_keywords/keyword
  where contains(lower-case($bs/title/name),lower-case($search)) or contains(lower-case($p),lower-case($search))
  return $bs
};

declare function movies:dist_searcher($search) as element()*{
  let $s := movies:searcher($search)
  for $dist_names in distinct-values($s//title/name)
  let $d := $s//title/name[.=$dist_names]
  return $d[1]/../..
};

(: GET ALL functions :)
declare function movies:get_all_genres() as element()*{
  let $genres := doc("moviesDB")//genres
  for $genre in distinct-values($genres/genre)
  return <genre>{$genre}</genre>
};

declare function movies:get_all_ratings() as element()*{
  for $rating in distinct-values(doc("moviesDB")//@rating)
  return <rating>{$rating}</rating>
};

declare function movies:get_all_years() as element()*{
  for $year in distinct-values(doc("moviesDB")//year)
  order by $year
  return <year>{$year}</year>
};

declare function movies:get_all_plot_keywords() as element()*{
    let $plot_keywords := doc("moviesDB")//plot_keywords
    for $key_word in distinct-values($plot_keywords/keyword)
    return <text>{ $key_word }</text>
};

declare function movies:get_all_actors() as element()*{
  <actors>{
    let $people := doc("moviesDB")//person
    for $person in $people
    where matches(data($person//profession), "Actor")
    return $person//name
  }</actors>
};

declare function movies:get_all_directors() as element()*{
  <directors>{
    let $people := doc("moviesDB")//person
    for $person in $people
    where matches(data($person//profession), "Movie Director")
    return $person//name
  }</directors>
};

declare function movies:get_imdb_link($firstname, $lastname) as element()*{
    <links>{
        let $movies := doc("moviesDB")//movie
        for $movie in $movies
            for $name in $movie//person/name
            where matches(data($name/first_name), $firstname) and
                  matches(data($name/last_name), $lastname)
            return <link>{$movie//link}</link>
    }</links>
};

(: Get specific functions :)
(: Every movie of an actor 
declare function movies:get_movies_by_actor($a_first_name, $a_last_name) as item(){
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where matches(data($actors//first_name), $a_first_name) and matches(data($actors//last_name), $a_last_name)
      return $movie
};:)

(: Every actor of a movie :)
    (:1. No caso de escolhermos não haver atores secundários:)
declare function movies:get_actors_by_movie($movie_name) as element()*{
  let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//main_actors
};
    (:2. No caso de escolhermos haver atores secundários :)
(:declare function movies:get_actors_by_movie($movie_name as xs:string) as item(){
  <actors>{
    let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
    return
      if (exists($movie//secondary_actors)) then
        $movie//main_actors and $movie//secondary_actors
      else
        $movie//main_actors
  }</actors>
};
:)

(: Every movie of a director :)
declare function movies:get_movies_by_director($dir_first_name as xs:string, $dir_last_name as xs:string) as item(){
  <movies>{
      for $movie in doc("moviesDB")//movie
      where $movie//director//first_name=$dir_first_name and $movie//director//last_name=$dir_last_name
      return $movie
  }</movies>
};

declare function movies:dist_get_movies_by_director($a_first_name, $a_last_name) as element()*{
  let $s := movies:get_movies_by_director($a_first_name, $a_last_name)
  for $dist_names in distinct-values($s//title/name)
  let $d := $s//title/name[.=$dist_names]
  return $d[1]
};

(: Every movie that starts with a letter :)
declare function movies:get_movies_by_first_letter($letter) as item(){
  <movies>{
    for $movie in doc("moviesDB")//movie
    where starts-with($movie/title/name, $letter)
    return  $movie
  }</movies>
};

declare function movies:get_movie($movie_name) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    return $movie
};

(: Year of a specific movie :)
declare function movies:get_movie_year($movie_name) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//year
};

(: Genres of a specific movie :)
declare function movies:get_movie_genres($movie_name) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    for $genre in $movie//genre
      return $genre
};

(: Director of a specific movie :)
declare function movies:get_movie_director_name($movie_name as xs:string) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return string-join(($movie/director//first_name/text(), $movie/director//last_name/text())," ")
};

(: Main actors of a specific movie :)
declare function movies:get_movie_main_actors($movie_name as xs:string) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    for $actor in $movie//main_actors//name
      return <actor>{string-join(($actor/first_name/text(), $actor/last_name/text())," ")}</actor>
};

(: Secondary actors of a specific movie :)
declare function movies:get_movie_secondary_actors($movie_name) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    return
    if (exists($movie//secondary_actors)) then
        for $actor in $movie//secondary_actors//name
         return <actor>{string-join(($actor/first_name/text(), $actor/last_name/text())," ")}</actor>
};

(: Score of a specific movie :)
declare function movies:get_movie_score($movie_name) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return <score>{$movie//score/text()}</score>
};

(: Duration of a specific movie :)
declare function movies:get_movie_duration($movie_name) as item(){
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    return <duration>{data($movie/@duration)}</duration>
};

(: Plot keywords of a specific movie :)
declare function movies:get_movie_plot_keywords($movie_name) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    for $key in $movie//keyword
        return $key
};

(: SELECT functions :)
(: Every genre selected :)
declare function movies:selected_genres($genres) as element()*{
    <movies>{
      let $movies := doc("moviesDB")
      return if (data($genres//genre[1])="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                    for $m_genre in $movie//genre
                        for $q_genre in $genres//genre
                        where matches(data($q_genre), data($m_genre))
                        return $movie
    }</movies>
};

declare function movies:selected_rating($rating) as element()*{
    <movies>{
      let $movies := doc("moviesDB")
      return if  (data($rating//rating)="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                  where matches(data($movie//@rating), data($rating//rating))
                  return $movie
    }</movies>
};

declare function movies:selected_year($year) as element()*{
    <movies>{
      let $movies := doc("moviesDB")
      return if (data($year//year)="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                  where matches(data($movie//year), data($year//year))
                  return $movie
    }</movies>
};
(:
declare function movies:apply_filters($query) as element()*{
(: <query>  <genres>  <genre></genre>  </genres>    <rating></rating>    <year></year>  </query> :)
        let $movies := doc("moviesDB")
        let $selected_movies_by_year := movies:selected_year($query)
        let $selected_movies_by_rating := movies:selected_rating($query)
        let $selected_movies_by_genres := movies:selected_genres($query)
        for $movie_y in $selected_movies_by_year//movie
        for $movie_r in $selected_movies_by_rating//movie
        for $movie_g in $selected_movies_by_genres//movie
        where matches(data($movie_y//title/name), data($movie_r//title/name))
                and matches(data($movie_g//title/name), data($movie_r//title/name))
        return $movie_g
};
  :)
  
  declare function movies:apply_filters($query) as element()*{
(: <query>  <genres>  <genre></genre>  </genres>    <rating></rating>    <year></year>  </query> :)
        let $movies := doc("moviesDB")
        let $selected_movies_by_year := movies:selected_year($query)
        let $selected_movies_by_rating := movies:selected_rating($query)
        let $selected_movies_by_genres := movies:selected_genres($query)
        for $movie_y in $selected_movies_by_year//movie
        for $movie_r in $selected_movies_by_rating//movie
        for $movie_g in $selected_movies_by_genres//movie
        where matches(data($movie_y//title/name), data($movie_r//title/name))
                and matches(data($movie_g//title/name), data($movie_r//title/name))
                and matches(data($movie_y//title/name), data($movie_g//title/name))
        return $movie_g
};

declare function movies:selected_filters($query, $order) as element()*{
    let $filtered := movies:apply_filters($query)
    return if (data($order)='title') then 
      for $name in distinct-values($filtered//title/name)
      let $b := $filtered//title/name[.=$name]
      order by $b[1]/../..//title/name
      return $b[1]/../..
    else if (data($order)='score') then
      for $name in distinct-values($filtered//title/name)
      let $b := $filtered//title/name[.=$name]
      order by $b[1]/../..//imbd_info/score descending
      return $b[1]/../..
    else if (data($order)='year') then
      for $name in distinct-values($filtered//title/name)
      let $b := $filtered//title/name[.=$name]
      order by $b[1]/../..//title/year descending
      return $b[1]/../..
    else for $name in distinct-values($filtered//title/name)
      let $b := $filtered//title/name[.=$name]
      return $b[1]/../..
};

declare updating function movies:ins_movie($movie){
  let $bs := collection('moviesDB')//movies
  let $node := $movie//movie
  return insert node $node as first into $bs
};

(: UPDATE DB functions :)
(:
declare function local:update_names() as item(){
    let $people := doc("moviesDB")//person
    for $person in $people
        let $first_name := $person/first_name
        let $last_name := $person/last_name
        return (
            insert node <name>
                {$first_name}{$last_name}
            </name> as first into $person
            ,
            delete node $person/first_name,
            delete node $person/last_name
      )
};
:)
(:movies:selected_filters(<query><genres><genre>Action</genre><genre>Comedy</genre></genres><rating>PG-13</rating><year>2009</year></query>):)


declare updating function movies:del_movie($movie){
  let $movie := doc('moviesDB')//movie[title/name=$movie]
  return delete node $movie
};

declare function movies:searchActor($search) as element()*{
  let $people := doc("moviesDB")//person
  for $person in $people
  where matches(data($person//profession), "Actor") and contains(lower-case($person//name),lower-case($search))
  return $person//name
};

declare function movies:dist_searchActor($search) as element()*{
  let $s := movies:searchActor($search)
  for $dist_names in distinct-values($s)
  let $d := $s[.=$dist_names]
  return $d[1]/..
};

declare function movies:searchDirector($search) as element()*{
   let $people := doc("moviesDB")//person
  for $person in $people
  where matches(data($person//profession), "Movie Director") and contains(lower-case($person//name),lower-case($search))
  return $person//name
};

declare function movies:dist_searchDirector($search) as element()*{
  let $s := movies:searchDirector($search)
  for $dist_names in distinct-values($s)
  let $d := $s[.=$dist_names]
  return $d[1]/../..
};

declare function movies:get_movies_by_actor($a_first_name, $a_last_name) as element()*{
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where matches(data($actors//first_name), $a_first_name) and matches(data($actors//last_name), $a_last_name)
      return $movie
};

declare function movies:dist_get_movies_by_actor($a_first_name, $a_last_name) as element()*{
  let $s := movies:get_movies_by_actor($a_first_name, $a_last_name)
  for $dist_names in distinct-values($s//title/name)
  let $d := $s//title/name[.=$dist_names]
  return $d[1]
};