module namespace people = "com.people";

declare function people:get_img($actor) as element()*{
  for $name in doc("peopleDB")//name
  where contains(data($name), data($actor//first_name)) and contains(data($name), data($actor//last_name))
  return $name/../img
};
(: $actor = <actor>Brad Pitt</actor>:)
declare function people:get_bio($actor) as element()*{
  for $name in doc("peopleDB")//name
  where contains(data($name), data($actor//first_name)) and contains(data($name), data($actor//last_name))
  return $name/../bio
};