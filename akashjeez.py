__author__ = 'akashjeez'

import os, sys, re, math, json
from datetime import datetime, timedelta
import pandas as pd, numpy as np
import streamlit as st


## Use the Full Page Instead of Narrow Central Column.
st.beta_set_page_config(layout = 'wide')

st.title('Ak@$h😎J€€Z')


CATEGORIES_LIST: list = ['Age Calculator', 'Python Tutorial']
CATEGORIES_LIST.sort()


def execute_main() -> None:
	st.sidebar.subheader('Contribute')
	st.sidebar.info('''
		This is an Open Source Project and You are Very Welcome to Contribute 
		Your Awesome Comments, Questions, Resources and Apps as \
		[Issues] ( https://github.com/akashjeez/Streamlit-Apps/issues ) \
		of or [Pull Requests] ( https://github.com/akashjeez/Streamlit-Apps/pulls ) \
		to the [Source Code] ( https://github.com/akashjeez/Streamlit-Apps ).
	''')

	st.sidebar.subheader('About Me')
	st.sidebar.info('''
		Hi there, I am AkashJeez, I Love Coding and Racing :) \n
		Feel Free to Reach Out to Me Via \n
		[ << Website >> ] ( https://akashjeez.herokuapp.com/ ) \n
		[ << Blogspot >> ] ( https://akashjeez.blogspot.com/ ) \n
		[ << Instagram >> ] ( https://instagram.com/akashjeez/ ) \n
		[ << Twitter >> ] ( https://twitter.com/akashjeez/ ) \n
		[ << Github >> ] ( https://github.com/akashjeez/ ) \n
		[ << Tubmlr >> ] ( https://akashjeez.tumblr.com/ ) \n
		[ << LinkedIn >> ] ( https://linkedin.com/in/akash-ponnurangam-408363125/ ) \n
	''')

	CATEGORY = st.selectbox(label = 'Choose Micro App', options = CATEGORIES_LIST)

	st.write('*' * 100)

	if CATEGORY == 'Age Calculator':
		try:
			st.subheader('** Age Calculator **')
			input_date = st.date_input(label = 'Your Date-of-Birth', value = (datetime.today() - timedelta(days = 18250)) )
			result = round( ( ( datetime.now().date() - input_date ).days / 365 ), 2)
			st.write(f'\n ** Your Age is { result } ** ')
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')

	elif CATEGORY == 'Python Tutorial':
		try:
			st.subheader('** Python Tutorial **')
			st.write('Python is a Powerful General Purpose Programming Language. It is used in Web Development, Data Science, \
				Creating Software Prototypes etc. Python has Simple Easy-To-Use Syntax and Excellent Language to Learn to Program for Beginners.')
			OnlineCompilerLink = 'https://console.python.org/python-dot-org-console/'
			st.markdown("<a href = 'https://twitter.com/ThePSF' class = 'twitter-timeline'> Follow @ThePSF </a> ", unsafe_allow_html = True)
			st.write('** Python Online Compiler - Interactive Shell **')
			st.markdown(f"<iframe src = '{OnlineCompilerLink}' width = 700 height = 300 frameborder = 0> </iframe>", unsafe_allow_html = True)
			st.write('*' * 100)
			st.write('** Online Python Learning **')
			st.markdown(f"<a href = 'https://w3schools.com/python/' target = '_blank'> << W3Schools >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://pythonprogramming.net/' target = '_blank'> << PythonProgramming.Net >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://programiz.com/python-programming' target = '_blank'> << ProgramiZ >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://datacamp.com/' target = '_blank'> << DataCamp >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://awesome-python.com/' target = '_blank'> << Awesome Python >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://realpython.com/' target = '_blank'> << Real Python >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://guide.freecodecamp.org/python/' target = '_blank'> << Free-Code-Camp >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://sololearn.com/Course/Python/' target = '_blank'> << SoloLearn >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://web.programminghub.io/' target = '_blank'> << Programming Hub >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://youtu.be/_uQrJ0TkZlc' target = '_blank'> << Youtube - Python Absolute for Beginners >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://data36.com/' target = '_blank'> << Python Data Science for Beginners >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://tutorialsteacher.com/python' target = '_blank'> << Tutorials Teacher >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://morioh.com' target = '_blank'> << Morioh >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://tutorialedge.net/course/python/' target = '_blank'> << Tutorials Edge >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://listendata.com/search/label/Python' target = '_blank'> << Listen Data >> </a>", unsafe_allow_html = True)
			st.markdown(f"<a href = 'https://data-flair.training/blogs/python-tutorial/' target = '_blank'> << Data Flair >> </a>", unsafe_allow_html = True)
		except Exception as ex:
			st.write(f'\n ** Error : { ex } **')


if __name__ == '__main__':
	execute_main()
