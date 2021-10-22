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
* Then download the files (Transformation_final.py, readCoord.py, test_CH1903+_to_WGS.txt and test_WGS_to_CH1903+.txt).
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

* It usually happends that the program cannot open your .txt file because you wrote the full name with the extensio. Example: "test_CH1903+_to_WGS.txt". This won't work.
* It also happens that you have an error, that's because you have already did the transformation for that file. If you have that problem, open your .txt file and delete the last line to return to the basic .txt file

Example: 
![Test_fail](https://github.com/FlorentZolliker/IntroductionToResearchSkills/blob/main/Test_failed.PNG?raw=true)

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
