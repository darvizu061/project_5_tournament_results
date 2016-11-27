-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament

\c tournament


CREATE TABLE registered_players(
  id SERIAL PRIMARY KEY,
  name TEXT
)


CREATE TABLE matches(
  match_id SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES registered_players(id),
  loser INTEGER REFERENCES registered_players(id)
)


CREATE MATERIALIZED VIEW wins AS
  SELECT rp.id AS player, count(matches.winner) AS wins
  FROM registered_players as rp
  LEFT JOIN matches ON rp.id = matches.winner
  GROUP BY rp.id, matches.winner
  ORDER BY rp.id


CREATE MATERIALIZED VIEW total_matches AS
  SELECT rp.id AS player, count(matches) AS matches
  FROM registered_players as rp
  LEFT JOIN matches ON(rp.id=matches.winner) OR(rp.id=matches.loser)
  GROUP BY rp.id
  ORDER BY rp.id ASC
