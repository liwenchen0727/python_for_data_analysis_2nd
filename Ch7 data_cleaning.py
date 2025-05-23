# -*- coding: utf-8 -*-
"""
Created on Wed May 7 2025

Python for Data Analysis (2nd ed) by Wes McKinney
Chapter 7: Data Cleaning and Preparation
7.1 Handling Missing Data
    7.1.1 Filtering Out Missing Data
    7.1.2 Filling In Missing Data
7.2 Data Transformation
    7.2.1 Removing Duplicates
    7.2.2 Transforming Data Using a Function or Mapping
    7.2.3 Replacing Values
    7.2.4 Renaming Axis Indexes
    7.2.5 Discretization and Binning
    7.2.6 Detecting and Filtering Outliers
    7.2.7 Permutation and Random Sampling
    7.2.8 Computing Indicator/Dummy Variables
7.3 String Manipulation
    7.3.1 String Object Methods
    7.3.2 Regular Expressions
    7.3.3 Vectorized String Functions in pandas
7.4 Conclusion

@author: E085828
"""

from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import numpy as np
# =============================================================================
# 7.1 Handling Missing Data
# =============================================================================
# pandas adopt R language convention NA (Not Available) for missing data
# np.nan (Not a Number) is floating-point value NaN
string_data = pd.Series(['aardvark', 'artichoke', np.nan, 'avocado'])
string_data
string_data.isnull()
string_data[0] = None # Python built-in None is also NA
string_data.isnull()

# 7.1.1 Filtering Out Missing Data
from numpy import nan as NA
data = pd.Series([1, NA, 3.5, NA, 7])
data.dropna()
data[data.notnull()] # alternatively

data = pd.DataFrame([[1., 6.5, 3.], [1., NA, NA],
                     [NA, NA, NA], [NA, 6.5, 3.]])
cleaned = data.dropna() # drop rows that have any NA
data.dropna(how='all')  # drop rows that are all NA
data[4] = NA
data.dropna(axis=1, how='all') # drop cols that are all NA
df = pd.DataFrame(np.random.randn(7, 3))
df.iloc[:4, 1] = NA
df.iloc[:2, 2] = NA
df
df.dropna()
df.dropna(thresh=2) # min # of non-NaNs to retain a row or col

# my script
# filter out rows with NA in specified column(s)
df[df[1].notnull()]
df[df[1].notnull() | df[2].notnull()]

# 7.1.2 Filling In Missing Data
df.fillna(0)
df.fillna({1: 0.5, 2: 0})
_ = df.fillna(0, inplace=True) # modify the object in-place
df = pd.DataFrame(np.random.randn(6, 3))
df.iloc[2:, 1] = NA
df.iloc[4:, 2] = NA
df.fillna(method='ffill')
df.fillna(method='ffill', limit=2)
data = pd.Series([1., NA, 3.5, NA, 7])
data.fillna(data.mean())
data = pd.Series([1., NA, 3.5, NA, 7])
data.fillna(data.mean())

# =============================================================================
# 7.2 Data Transformation
# =============================================================================
# 7.2.1 Removing Duplicates
data = pd.DataFrame({'k1': ['one', 'two'] * 3 + ['two'],
                     'k2': [1, 1, 2, 3, 3, 4, 4]})
data.duplicated()
data.drop_duplicates()
# Remove Partial Duplicates based on specified col(s)
data['v1'] = range(7)
data.drop_duplicates(['k1'])

data.drop_duplicates(['k1', 'k2'], keep='last') # drop_duplicates keep the first value by default

# 7.2.2 Transforming Data Using a Function or Mapping
data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon',
                              'Pastrami', 'corned beef', 'Bacon',
                              'pastrami', 'honey ham', 'nova lox'],
                     'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})

meat_to_animal = {
  'bacon': 'pig',
  'pulled pork': 'pig',
  'pastrami': 'cow',
  'corned beef': 'cow',
  'honey ham': 'pig',
  'nova lox': 'salmon'
}

lowercased = data['food'].str.lower()

# map() accepts a function or dict-like object containing a mapping
data['animal'] = lowercased.map(meat_to_animal)
data['animal'] = data['food'].map(lambda x: meat_to_animal[x.lower()]) #  pass a function does all the work

# 7.2.3 Replacing Values
data = pd.Series([1., -999., 2., -999., -1000., 3.])
data.replace(-999, np.nan) # produce a new Series unless passing inplace=True
data.replace([-999, -1000], np.nan)
data.replace([-999, -1000], [np.nan, 0])
data.replace({-999: np.nan, -1000: 0})

# 7.2.4 Renaming Axis Indexes
data = pd.DataFrame(np.arange(12).reshape((3, 4)),
                    index=['Ohio', 'Colorado', 'New York'],
                    columns=['one', 'two', 'three', 'four'])

transform = lambda x: x[:4].upper()
data.index.map(transform)

data.index = data.index.map(transform) # modify index in-place
# rename(index=, column=) accepts a function or dict-like object
data.rename(index=str.title, columns=str.upper)
data.rename(index={'OHIO': 'INDIANA'},
            columns={'three': 'peekaboo'})
data.rename(index={'OHIO': 'INDIANA'}, inplace=True)

# 7.2.5 Discretization and Binning
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
# cut() 
cats = pd.cut(ages, bins) # right=True by default
cats.codes
cats.categories
pd.value_counts(cats)

pd.cut(ages, [18, 26, 36, 61, 100], right=False)
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
pd.cut(ages, bins, labels=group_names)

data = np.random.rand(20) # uniform distribution between 0 and 1
pd.cut(data, 4, precision=2) # equal-length bins (based on min & max of data)

data = np.random.randn(1000)  # standard normal distribution ((mean 0, variance 1))
cats = pd.qcut(data, 4)  # Cut into quartiles with equal-size bins (each bin contain same counts of data)
pd.value_counts(cats)
pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])

# 7.2.6 Detecting and Filtering Outliers
data = pd.DataFrame(np.random.randn(1000, 4))
data.describe()

col = data[2]
col[np.abs(col) > 3]
data[(np.abs(data) > 3).any(axis=1)] # rows having a value exceeding 3 or –3
data[np.abs(data) > 3] = np.sign(data) * 3 # cap values
data.describe()

np.sign(data).head() # np.sign(data) produce 1 for pos & -1 for neg

# 7.2.7 Permutation and Random Sampling
df = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))
sampler = np.random.permutation(5)
df.take(sampler) # df.iloc[sampler]
df.sample(n=3) # without replacement
choices = pd.Series([5, 7, -1, 6, 4])
draws = choices.sample(n=10, replace=True) # with replacement

# 7.2.8 Computing Indicator/Dummy Variables
df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                   'data1': range(6)})
pd.get_dummies(df['key']).astype(int)
dummies = pd.get_dummies(df['key'], prefix='key')
df_with_dummy = df[['data1']].join(dummies)

# if a row belongs to multiple categories (>1 ones)
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('../datasets/movielens/movies.dat', sep='::',
                       header=None, names=mnames, engine='python')
movies[:10]

# Add indicator variables for each genre
# 1. extract a list of unique genres
all_genres = []
for x in movies.genres:
    all_genres.extend(x.split('|'))
genres = pd.unique(all_genres) # list(set(all_genres))
# 2. initiate the indicator df with all zeros
zero_matrix = np.zeros((len(movies), len(genres)))
dummies = pd.DataFrame(zero_matrix, columns=genres)
# 3. use the dummies.columns to compute the column indices for each genre
gen = movies.genres[0]
gen.split('|')
dummies.columns.get_indexer(gen.split('|'))
# 4. iterate through each movie and set entries in each row of dummies to 1
for i, gen in enumerate(movies.genres):
    indices = dummies.columns.get_indexer(gen.split('|'))
    dummies.iloc[i, indices] = 1
# 5. combine indicators with movies
movies_windic = movies.join(dummies.add_prefix('Genre_'))
movies_windic.iloc[0]

# create indicators based on bins (useful)
np.random.seed(12345)
values = np.random.rand(10)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
pd.get_dummies(pd.cut(values, bins)).astype(int)

# =============================================================================
# 7.3 String Manipulation
# =============================================================================
# 7.3.1 String Object Methods (Python built-in string methods)
val = 'a,b,  guido'
val.split(',')
pieces = [x.strip() for x in val.split(',')]
first, second, third = pieces
first + '::' + second + '::' + third
'::'.join(pieces)
'guido' in val
val.index(',')
val.find(':')
val.index(':')
val.count(',')
val.replace(',', '::')
val.replace(',', '')

# 7.3.2 Regular Expressions
import re
text = "foo    bar\t baz  \tqux"
re.split(r'\s+', text)
regex = re.compile(r'\s+')
regex.split(text)
regex.findall(text)

text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
# re.IGNORECASE makes the regex case-insensitive
regex = re.compile(pattern, flags=re.IGNORECASE)
regex.findall(text)
m = regex.search(text)
text[m.start():m.end()]
print(regex.match(text))
print(regex.sub('REDACTED', text))

pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)

m = regex.match('wesm@bright.net')
m.groups()
regex.findall(text)
print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))

# 7.3.3 Vectorized String Functions in pandas
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = pd.Series(data)
data.isnull()
data.str.contains('gmail')
pattern
data.str.findall(pattern, flags=re.IGNORECASE)
matches = data.str.match(pattern, flags=re.IGNORECASE)
matches.str.get(1)
matches.str[0]
data.str[:5]


    