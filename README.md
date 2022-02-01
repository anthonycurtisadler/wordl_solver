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

*          =  to use only frequency by letter in word
**         =  to use only frequency by letter in exact position
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

