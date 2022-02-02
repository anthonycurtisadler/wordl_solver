# wordle_solver




WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordle/)

1) ALLOWS YOU to PLAY wordles in EASY and HARD mode with from various word lists and of various word lengths.
2) ALLOWS YOU to find eligible words matching guesses and responses already given.
3) PROVIDES definitions for words 
4) ALLOWS you to save interesting words and definitions to a textfile
5) ALLOWS YOU to test various strategies for solving.


STRATEGY SCRIPT CONSISTS OF A SERIES OF STRAGIES separated by SEMICOLONS.
    S1;S2;S3;S4

The FIRST STRATEGY may include a WORD to us in curly brackets
ALL may include a STRATEGY CODE and an optional DIVIDER, in square brackets

STRATEGY CODE CONSISTS OF SEVERAL PARTS

(1) DETERMINANTS 

STAR (*)         =  to use only frequency by letter in word
STAR STAR (**)   =  to use only frequency by letter in exact position
[no star]  =  to combine both
~          =  to invert ordering 

(2) ORDERING METHOD

i  = rank words by least average size
     of the subsequent groups it generates (=entropy)
f  = rank words by frequency according to function

(3) RESTRICTING METHOD

$  = to limit to words from the "solutions" set 
s  = gets the "slice" sharing the highest value from the sorting function


(4) SELECTING METHOD 

r   = get a random word from almost the 1/INT "best" words
     [INT] / TO set value
p   = get the word at the LENGTH*1/FLOAT index
     0<=1 [FLOAT] < 1
t   = get the topmost ranked word

INT.  = at beginning of strategy to indicate maximum sent on which the given method is to be applied

{WORD} = to automatically choose word



Using the standard wordle list of words, {tares};$i and {alter};$i yield an average of around 3.6 guesses.


THE FOLLOWING IS THE RESULTS FROM RUNNING ALL THE PRE-DEFINED SOLVING METHODS AGAINST THE STANDARD WORDLE WORD SET


 1/*f = 4.698488120950324
HISTOGRAM <1> 2=28, 3=331, 4=836, 5=615, 6=283, 7=126, 8=59, 9=20, 10=12, 11=3, 12=2

 2/**f = 4.866090712742981
HISTOGRAM <2> 2=25, 3=282, 4=723, 5=655, 6=377, 7=149, 8=64, 9=24, 10=10, 11=3, 12=3

 3/$f = 3.7900647948164146
HISTOGRAM <3> 1=1, 2=132, 3=823, 4=899, 5=346, 6=89, 7=21, 8=3, 9=1

 4/$*f = 3.8099352051835855
HISTOGRAM <4> 1=1, 2=133, 3=788, 4=930, 5=347, 6=89, 7=18, 8=7, 9=2

 5/$**f = 3.8397408207343413
HISTOGRAM <5> 1=1, 2=146, 3=752, 4=910, 5=368, 6=110, 7=24, 8=4

 6/{tares};i = 3.6984881209503238
HISTOGRAM <6> 2=128, 3=887, 4=943, 5=285, 6=59, 7=10, 8=3

 7/{tares};$i = 3.6483801295896328
HISTOGRAM <7> 2=128, 3=922, 4=960, 5=255, 6=42, 7=7, 8=1

 8/fr[60] = 4.518790496760259
HISTOGRAM <8> 1=3, 2=50, 3=394, 4=857, 5=592, 6=248, 7=105, 8=42, 9=15, 10=6, 11=2, 12=1

