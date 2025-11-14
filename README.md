# ATLAS
#### Video Demo:  https://youtu.be/25IqrPhxpWc
#### Description:

This Project is all about names of different places. You enter a name of place and the website returns another place starting with the last letter of your input.

The game continues in the same manner you again enter a place starting from the last letter of returned word. Remember the first word has to start with the letter "A".

At the beginning you have to enter the difficulty level and no. of passes, a pass will help you skip when you dont know any name with the given letter, when you have 0 passes left you loose.

Difficultly level can be any positive integer, a difficulty level of 10-20 is very easy and computer might lose in the first turn, a difficulty of 250 is moderate and keeps getting harder as you increase the number. Default value is 250 and 3 for passes.

If you enter any place not present in the database or in case of a typo, the website will return "Word not in database" which means you have to again enter another place with same letter.

You cannot use a name which has been already used in a particular session of game.

You can type pass when you dont have an answer.

When you dont know about a place you can search for it you will get a result from Wikipedia. At times it you might get an error or wrong info when there are multiple articles on Wikipedia with same name or there is no article.


About the files:-

app.py - is the main backend file where all the processing happens. That is later displayed on the website using flask. The main algorithm for game is implemented there.
Atlas.py - It contains functions which are used in app.py
Static folder
styles.css - css file for all html pages
atlas.txt - database for names of all places
Templates Folder
Contains the different html code for different pages of the website including layout.html which is common in all of them which is the logo, navbar, linking of bootstrap etc.
This project is also linked with wikipedia the details of the cities and countries are extracted from the same using python library.


 Prerequisites:
 Install newspaper3k python library if not installed
 command : pip3 install newspaper3k

 Use command flask run after entering the directory to host the website and use it.



 The pages first opens in index.html which explains the rules of the game with a lets begin button towards the end .
 Clicking that button with take you to start.html where you have to enter the difficulty level and the number of passes.
 If you directly click on start the default value of 250 and 3 will be taken
 Then it redirects to begin to html where you enter the word and submit and computer returns another place and game continues.
 You can search about an unknown place clicking on the search button.
 In case you dont know any place with that letter you can use your pass.
 When pass is less than 0 you loose and you are redirected to lost.html where your score is displayed and there is option to return to start page by clicking play again.
 You win the game if the program cannot randomly find an unused placed with the given letter in the number of tries entered in difficulty.
 After winning you are redirected to win.html which is similar to lost.html except for the emoji.
 This application is completed.

