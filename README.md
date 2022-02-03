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

0/f = 4.702375809935205
HISTOGRAM <0> 2=35, 3=348, 4=802, 5=608, 6=288, 7=134, 8=62, 9=23, 10=11, 11=3, 12=1

 1/*f = 4.752915766738661
HISTOGRAM <1> 2=16, 3=285, 4=855, 5=630, 6=312, 7=127, 8=47, 9=27, 10=12, 11=2, 12=2

 2/**f = 5.232829373650108
HISTOGRAM <2> 2=12, 3=156, 4=592, 5=721, 6=471, 7=203, 8=83, 9=47, 10=19, 11=8, 12=2, 13=1

 3/$f = 3.711879049676026
HISTOGRAM <3> 1=1, 2=132, 3=866, 4=940, 5=309, 6=50, 7=12, 8=4, 9=1

 4/$*f = 3.749460043196544
HISTOGRAM <4> 1=1, 2=133, 3=829, 4=954, 5=304, 6=74, 7=14, 8=6

 5/$**f = 3.7533477321814255
HISTOGRAM <5> 1=1, 2=146, 3=813, 4=934, 5=330, 6=68, 7=21, 8=2

 6/{tares};i = 4.665658747300216
HISTOGRAM <6> 2=19, 3=296, 4=858, 5=674, 6=303, 7=101, 8=42, 9=13, 10=6, 11=1, 12=2

 7/{tares};$i = 3.653131749460043
HISTOGRAM <7> 2=128, 3=919, 4=956, 5=262, 6=41, 7=8, 8=1

 8/fr[60] = 4.6855291576673865
HISTOGRAM <8> 2=22, 3=311, 4=843, 5=657, 6=286, 7=119, 8=46, 9=19, 10=7, 11=5

 9/~f = 6.8151187904967605
HISTOGRAM <9> 2=6, 3=45, 4=159, 5=321, 6=464, 7=508, 8=437, 9=245, 10=95, 11=24, 12=9, 13=2

 10/{zylyl};~$i = 6.007343412526998
HISTOGRAM <10> 2=22, 3=127, 4=299, 5=444, 6=547, 7=439, 8=288, 9=98, 10=38, 11=11, 12=2
