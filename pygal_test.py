import os
import sys
base_path = os.path.dirname(os.path.abspath(__file__))

# Insert local directories into path
sys.path.append(os.path.join(base_path, 'lib'))

import pygal                                                       # First import pygal

from synodlnatrakt import db

bar_chart = pygal.Bar()                                            # Then create a bar graph object
bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values
bar_chart.render_to_file('bar_chart.svg')                          # Save the svg to a file


movies = len(db.session.query(db.Movies).all())
series = len(db.session.query(db.TVEpisodes).all())

pie_chart = pygal.Pie()
pie_chart.title = 'Series/Movies'
pie_chart.add('Episodes', series)
pie_chart.add('Movies', movies)
pie_chart.render_to_file('pie_chart.svg')                          # Save the svg to a file




print movies, series
