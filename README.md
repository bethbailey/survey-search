# survey-search
Survey search project for CS 30122

Team: Bethany Bailey (Data Cleaning Queen), Ruixue Li (Interior Designer), Leoson Hoay (Django Janitor)


## Overall Code Structure

### Data Cleaning

Our code is structured in two main bits: (1) data cleaning and (2) Django site. The data cleaning was all done in jupyter notebooks, and took survey documentation from the web in four different formats - pdf, csv, rtf, and docx - and extracted the variables and put them into csvs with the variable names and text. During this process, the actual survey data was converted to csv and stored in the data folder for each survey as well as the Survey Detail folder (which is what we provide to the Django site for links).

### Django

The Django portion is structured as follows (the final site is in Final Site/surveysearch folder on github):


+---- documents
+---- manage.py
+---- search
 |        +---- __init__.py
 |        +---- __pycache__
 |        +---- admin.py
 |        +---- apps.py
 |        +---- forms.py
 |        +---- migrations
 |        +---- models.py
 |        +---- static
 |        +---- templates
 |        +---- urls.py
 |        +---- views.py
 +---- search_beta.sqlite3
 +---- surveysearch
 |        +---- __init__.py
 |        +---- __pycache__
 |        +---- settings.py
 |        +---- urls.py
 |        +---- wsgi.py

## Instructions

### Data Cleaning

#### Libraries to Install for Data Cleaning:
- PyPDF2 (sudo pip3 install PyPDF2)
- docx (sudo pip3 install python-docx)
- docx2txt (sudo pip3 install docx2txt)
- The regular expression library (re) should be installed on ths VMs already.

To rerun the data cleaning, go into each data folder, open the jupyter notebook (run "jupyter notebook" from the command line and go to the jupyter notebook document), and rerun the script. The data that was used to find the questions/variable names and descriptions is in each individual folder. All of these data sources were downloaded directly from online sources. 

### Running the Django Site

#### Libraries to Install for Django:
- wordcloud (sudo pip3 install wordcloud)
- sklearn (sudo pip3 install sklearn)
- Pillow and Matplotlib should already be installed on the VMs.

To run our site, please go into the Final Site/surveysearch folder and run "python3 manage.py runserver --nothreading". We have added "--nothreading" in order to ensure compatibility with matplotlib. Once you have run this, go to http://127.0.0.1:8000/search/ in your browser to access the homepage.

#### *Use Case 1: Testing Question Search*
Go to homepage -> click "Find relevant questions" button -> input keyword(s) separated by space -> click search button and you'll be redirected to a result page listing all the relevant questions from all the surveys in the database. You can then view the survey that contains a particular question by clicking on the title. While viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 2: Testing Survey Search*
Go to homepage -> click "Find relevant surveys" button -> input keyword(s) separated by space -> click search button and you'll be redirected to a result page listing all the relevant surveys in the database. You can then view the details of any survey by clicking on the title. Again, while viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 3: Browse Surveys*
Go to homepage -> click "Browse" button and you'll be redirected to a page listing all the surveys in the database. You can then view the details of any survey by clicking on the title. Once again, while viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 4: Testing Upload*
Test the upload portion of the site using either a handmade file or, if you are so inclined, the sample upload on our github in Sample Upload/student.csv. You can use any values for the upload parameters. Once you have uploaded this survey, you should be able to see it on the "Browse" page, and it will show up in keyword searches for questions and surveys (try searching "final" or "semester" before and after the upload). 
After you upload a new survey, the wordcloud on the homepage should update to reflect the the new data. If it does not automatically regenerate, clear the cache using Ctrl-Shift-R in the VM (or any Linux machine) or Cmd-Shift-R on Mac.

## Coding Breakdown

### Data Collection
The surveys were collected by all three members. The data that was in SPSS was converted to CSV by Leoson, and then Bethany completed all of the data cleaning and extraction.

### Django Site

#### Forms
Bethany and Ruixue completed the upload form. Together, all three team members figured out how to handle file processing in Django.

#### Search
Leoson completed the search by question, and Bethany completed the search by survey. Ruixue completed the ranking algorithm.

#### WordCloud

Ruixue completed the wordcloud. 

#### Templates/Formatting and HTML
All three team members participated in the page formatting and template creation. Ruixue applied styling to all pages with bootstrap and formatted the homepage (index.html).

## Documentation of Code Ownership  

Please see comments starting with "Code Ownership : " in files. The descriptions of code ownership are as the example provided by Professor Rogers, outlined below.

- "Direct copy" : Generated by installed package or online source (Django or other) and few edits made
- "Modified" : Generated by installed package or online source (Django or other) and meaningful edits made   OR   heavily utilized template(s) provided by tutorial sessions (TA- or Django-generated)                                     
- "Original" : Original code or heavily modified given structure  