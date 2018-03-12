# survey-search
Survey search project for CS 30122

Team: Bethany Bailey (Data Cleaning Queen), Ruixue Li (Interior Designer), Leoson Hoay (Django Janitor)


## Overall Code Structure

Our code is structured in two main bits: (1) data cleaning and (2) Django site. The data cleaning was all done in jupyter notebooks, and took survey documentation from the web in four different formats - pdf, csv, rtf, and docx - and extracted the variables and put them into csvs with the variable names and text. During this process, the actual survey data was converted to csv and stored in the data folder for each survey as well as the Survey Detail folder (which is what we provide to the Django site for links).

The Django portion is structured as follows (the final portion is in Final\ Site/surveysearch):

  |-search
  |  |-migrations
  |  |  |-__pycache__
  |  |-__pycache__
  |  |-static
  |  |  |-css
  |  |  |-js
  |  |  |-img
  |  |-templates
  |  |  |-search
  |  |  |  |-img
  |-documents
  |-surveysearch
  |  |-__pycache__
  |-.idea
  |  |-libraries


## Instructions

### Data Cleaning

To rerun the data cleaning, go into each data folder, open the jupyter notebook, and rerun the script. The data that was used to find the questions/variable names and descriptions is in each individual folder. All of these data sources were downloaded directly from online sources. 

Libraries to Install:
- PyPDF2
- docx
- docx2txt

### Running the Django Site

#### Testing Upload
Please test the upload portion of the site using either a handmade file or, if you are so inclined, the sample upload on our github in Sample Upload/student.csv. You can use any values for the upload parameters. Once you have uploaded this survey, you should be able to see it on the "Browse" page, and it will show up in keyword searches (try searching "final" or "semester" before and after the upload).

Libraries to Install:
- pillow
- wordcloud

## Coding Breakdown

### Data Collection
The surveys were collected by all three members. The data that was in SPSS was converted to CSV by Leoson, and then Bethany completed all of the data cleaning and extraction.

### Django Site

#### Forms
Bethany and Ruixue completed the upload form.

#### Search
Leoson completed the search by question, and Bethany completed the search by survey. Ruixue completed the ranking algorithm.

#### WordCloud

Ruixue completed the wordcloud. 

#### Templates/Formatting and HTML
All three team members participated in the page formatting and template creation. Ruixue applied styling to all pages with bootstrap and formatted the homepage (index.html).

## Documentation of Code Ownership  

Please see files. The descriptions of code ownership are as the example provided by Professor Rogers, outlined below.

- "Direct copy" : Generated by installed package or online source (Django or other) and few edits made
- "Modified" : Generated by installed package or online source (Django or other) and meaningful edits made   OR   heavily utilized template(s) provided by tutorial sessions (TA- or Django-generated)                                     
- "Original": Original code or heavily modified given structure  