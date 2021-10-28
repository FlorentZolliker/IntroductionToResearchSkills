# IntroductionToResearchSkills
 project managment

# Transformation of coordinates

This program will help you to do some coordinate transformation in the domain of satellite localisation.

## Description

This program is usefull to go eather:
* From ellipsoidal coordinate in the CHTRF95(WGS84) system to plane coordinate in the CH1903+ system
* From plane coordinate in the CH1903+ system to ellipsoidal coordinate in the CHTRF95(WGS84) system

## Getting Started

### Dependencies

*Python3.10

### Installing

* First you need to have python installed on your machine. This is the link to download the latest version: https://www.python.org/downloads/
* Then download the "Documents_and_code" file. (Transformation_final.py, readCoord.py, test_CH1903+_to_WGS.txt and test_WGS_to_CH1903+.txt).
* The files have to be in the same folder one from the others.

### Executing program

* Just double click on the "Transformation_final.py" file, this should open the python3.10 prompt and ask you a question.
* The question asked should be: "Entrer le nom du fichier .txt (sans le .txt):"
* You will now need to take the name of one of the 2 .txt file. For example "test_CH1903+_to_WGS".
* Copy paste that name just afte the ":" of the end of the question and press the "Enter" button of your keyboard.
* A new question will appear, it should be: "Voulez vous transformer des coordonnées de CHTRF95(WGS84) jusqu'à CH1903+? [oui/non]"
* Answer that question (no, if you don't want to do that, yes if you want to do that). Here in our example the answer is no, we want to go from CH1903+ to WGS (as writtent in the name of the .txt file).
* If you answered yes, the program is ended, if you answered no, another question is asked: "Voulez vous transformer des coordonnées de CH1903+ jusqu'à CHTRF95(WGS84)? [oui/non]".
* Answer that new question. In our example, the answer is now yes, we want to go from CH1903+ to CHTRF95(WGS84).
* If you answered yes, the program is ended.
* You can open your .txt file and you'll see that a new line has appeared with new values. Theses values are the coordinates after transformation.

## Help

* If you can't open the file just with a double click (usually if you are on Apple device):

1.Open IDLE (python3 prompt)

2.Right click on "Transformation_final.py" and select "Open with" --> IDLE (python 3)

* To have an idea if the code works or not:

The solution obtained in the last lane when you gave as entry one of the .txt file, is the entry of the other txt file.

This is the output of your file:

![Test_end](https://github.com/FlorentZolliker/IntroductionToResearchSkills/blob/main/Test_ended.PNG?raw=true)

This is the imput of the other file:

![Test_solutions_that_you_should_obtain](https://github.com/FlorentZolliker/IntroductionToResearchSkills/blob/main/Test_solution.PNG?raw=true)

Now compare the two. If it's the same, your program worked well.

* It usually happends that the program cannot open your .txt file because you wrote the full name with the extensio. Example: "test_CH1903+_to_WGS.txt". This won't work.
* It also happens that you have an error, that's because you have already did the transformation for that file. If you have that problem, open your .txt file and delete the last line to return to the basic .txt file

_Example:_

This txt file will lead to a fail:

![Test_fail](https://github.com/FlorentZolliker/IntroductionToResearchSkills/blob/main/Test_failed.PNG?raw=true)

This txt file will lead into a success:

![Test_will_not_fail](https://github.com/FlorentZolliker/IntroductionToResearchSkills/blob/main/Test_will_not_anymore_fail.PNG?raw=true)

## Authors

Florent Zolliker

Contributors names and contact info

Lander Verlinde  
[@Linkedin](https://be.linkedin.com/in/lander-verlinde-485795218)

## Acknowledgments

Inspiration, code snippets, etc.
* [Read me template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
