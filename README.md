# fpl-live

## About
This is a simple script to fetch the live scores from a [Fantasy Premier League](https://fantasy.premierleague.com) league. It is confirmed as working for the 2017/18 season's game.

## Usage
To run this program, you will need to know the ID for your league. When you visit your league page, you will see the ID in the URL. For example, the URL for the [Football365](http://football365.com)'s league is `https://fantasy.premierleague.com/a/leagues/standings/578679/classic`. The league ID is 578679.

To run the program, use the following command (while in the directory in which you've downloaded it), replacing 578679 with the ID of your league.

```./fpl_cli.py 578679```

## Background
My motivation for writing this was an excercise in [actor programming](http://en.wikipedia.org/wiki/Actor_model). It uses [pykka](https://github.com/jodal/pykka): a lightweight actor framework for Python that is inspired by the [akka](http://akka.io) actor programming language.

## Prerequisites
Requires [pykka](https://github.com/jodal/pykka) and [requests](https://github.com/kennethreitz/requests/) to be installed.

These can be installed by running the following:

```pip install pykka requests```