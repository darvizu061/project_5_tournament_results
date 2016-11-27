#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def make_groups(players, pair=2):
    """Pair up registered players"""
    pair = max(1, pair)
    return [players[i:i + pair] for i in range(0, len(players), pair)]


def refreshViews():
    """Refreshes Views"""
    DB = connect()
    c = DB.cursor()
    c.execute("REFRESH MATERIALIZED VIEW wins;")
    c.execute("REFRESH MATERIALIZED VIEW total_matches;")
    DB.commit()
    DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    q = "DELETE from matches WHERE match_id NOTNULL;"
    c.execute(q)
    DB.commit()
    DB.close()
    refreshViews()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM registered_players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count (*) AS num FROM registered_players;")
    total_players = c.fetchall()
    db.close()
    return total_players[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("""INSERT INTO registered_players (name)
                 VALUES (%s)""", (bleach.clean(name),))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    playertied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    refreshViews()
    db = connect()
    c = db.cursor()
    c.execute("""
            SELECT rp.id, rp.name, wins.wins, total_matches.matches
            FROM registered_players AS rp
            LEFT JOIN wins ON rp.id = wins.player
            LEFT JOIN total_matches ON rp.id = total_matches.player
            GROUP BY rp.id, rp.name, wins.wins, total_matches.matches
            ORDER BY wins.wins DESC;
              """)
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    q = "INSERT INTO matches (winner, loser) values (%s, %s);"
    c.execute(q, (bleach.clean(int(winner)), (bleach.clean(int(loser)))))
    db.commit()
    db.close()
    refreshViews()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    total_opponents = make_groups(standings, 2)
    opponents = list()

    for players in total_opponents:
        pairs = list()
        for player in players:
            pairs.append(player[0])
            pairs.append(player[1])
        opponents.append(pairs)

    return opponents
