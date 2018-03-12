# survey-search
Survey search project for CS 30122

Team: Bethany Bailey (Data Cleaning Queen), Ruixue Li (Interior Designer), Leoson Hoay (Django Janitor)


## Overall Code Structure

### Data Cleaning

Our code is structured in two main bits: (1) data cleaning and (2) Django site. The data cleaning was all done in jupyter notebooks, and took survey documentation from the web in four different formats - pdf, csv, rtf, and docx - and extracted the variables and put them into csvs with the variable names and text. During this process, the actual survey data was converted to csv and stored in the data folder for each survey as well as the Survey Detail folder (which is what we provide to the Django site for links).

### Django

The Django portion is structured as follows (the final site is in Final Site/surveysearch folder on github):

-  |-search
    * This is our main and only app. It is the root folder. It contains the files admin.py (Django admin file), views.py (the brunt of our Django python code), apps.py (our app), forms.py (the upload form), models.py (our survey and question models), urls.py (our urls file), and views.py (our views).
    * |  |-migrations
        * |  |  |-__pycache__
    *  |  |-__pycache__
    *  |  |-static
        * This folder contains bootstrap files (css, javascript) and images displayed on the website (including generated wordcloud image file).
        * |  |  |-css
        * |  |  |-js
        * |  |  |-img
    * |  |-templates
        * This folder contains the html templates for our site.
        * |  |  |-search
            * |  |  |  |-img
- |-documents
    * This is the folder where the user uploaded files are stored and processed.
-  |-surveysearch
    * This folder contains the Django site settings and back-end configuration.
    * |  |-__pycache__
- search_beta.sqlite3
    * SQL database for our models.

## Instructions

### Data Cleaning

To rerun the data cleaning, go into each data folder, open the jupyter notebook, and rerun the script. The data that was used to find the questions/variable names and descriptions is in each individual folder. All of these data sources were downloaded directly from online sources. 

#### Libraries to Install for Data Cleaning:
- PyPDF2
- docx
- docx2txt

### Running the Django Site

To run our site, please go into the Final Site/surveysearch folder and run "python3 manage.py runserver --nothreading". We have added "--nothreading" in order to ensure compatibility with matplotlib. Once you have run this, go to http://127.0.0.1:8000/search/ in your browser to access the homepage.

#### *Use Case 1: Testing Question Search*
Go to homepage -> click "Find relevant questions" button -> input keyword(s) separated by space -> click search button and you'll be redirected to a result page listing all the relevant questions from all the surveys in the database. You can then view the survey that contains a particular question by clicking on the title. While viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 2: Testing Survey Search*
Go to homepage -> click "Find relevant surveys" button -> input keyword(s) separated by space -> click search button and you'll be redirected to a result page listing all the relevant surveys in the database. You can then view the details of any survey by clicking on the title. Again, while viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 3: Browse Surveys*
Go to homepage -> click "Browse" button and you'll be redirected to a page listing all the surveys in the database. You can then view the details of any survey by clicking on the title. Once again, while viewing a survey, you can browse all the questions in that survey through the "See all variables and questions" link at the last cell of the form. 

#### *Use Case 4: Testing Upload*
Test the upload portion of the site using either a handmade file or, if you are so inclined, the sample upload on our github in Sample Upload/student.csv. You can use any values for the upload parameters. Once you have uploaded this survey, you should be able to see it on the "Browse" page, and it will show up in keyword searches for questions and surveys (try searching "final" or "semester" before and after the upload).

#### Libraries to Install for Django:
- wordcloud (sudo pip install wordcloud)
- sklearn (sudo pip install sklearn)
- Pillow and Matplotlib should already be installed on the VMs.

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