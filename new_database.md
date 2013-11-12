To include the new feautres mentioned in #28 i have to redesign the database...

Movies:
- id            INT
- imdb_id       INT
- tmdb_id       INT
- name          STRING
- year          INT
- description   STRING
- path          STRING
- duration      INT
- progress      INT
- scrobbled     INT
- rating        INT
- lastseen      TIMESTAMP
- added         TIMESTAMP
- synoindex     INT
- acodec        STRING
- vcodec        STRING
- vwidth        STRING

Trailers:
- id            INT
- name          STRING
- link          STRING

Genres:
- id            INT
- tmdb_id       INT
- name          STRING

Tags:
- id            INT
- tmdb_id       INT
- name          STRING

Actors:
- id            INT
- name          STRING
- tmdb_id       INT
- image         STRING

Directors:
- id            INT
- name          STRING
- tmdb_id       INT
- image         STRING

Movie Actor Link
- movie_id      INT
- acotor_id     INT

Movie Director Link
- movie_id      INT
- actor_id      INT

Movie Tag Link
- tag_id        INT
- movie_id      INT

Movie Trailer Link
- movie_id      INT
- trailer_id    INT

Movie Genre Link
- movie_id      INT
- genre_id      INT
