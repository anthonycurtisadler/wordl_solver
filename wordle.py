import os, random





class Wordle_Solver:


     def __init__ (self):

          self.words = []
          

          filename = 'words.txt'

          # GET TEXT FILE 
          while True:
               print('GETTING TEXT FILE!')
               try:
                    textfile = open(filename,'r', encoding='utf-8')
                    self.textfile=textfile.read()
                    print(filename+' OPENED! \n')
                    break
               except:
                    print(filename+' NOT FOUND\n')
                    print('ENTER NEW WORD FILE!')
                    filename= input('textfile')
          #To find the character dividing the words in the file
          for split_char in self.textfile:
               if split_char not in 'abcdefghijklomnopqrstuvwxyz0123456789':
                    self.split_char = split_char
                    break

          
          
          self.about = """
          WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordle/)

          THE VOCABULARY IS VERY LARGE and STRANGE.

          APPLIES THREE DIFFERENT SOLVING APPROACHES:
               (1) Chooses the word with the most frequently appearing characters
               (2) Chooses the word randomly
               (3) Chooses randomly from the top 10% of the words with the most frequently appearing characters

             """
     def constitute (self,word_length):

          """Loads in list of words from textfile"""

          self.word_length = word_length 
          self.words = [x.strip() for x in self.textfile.split(self.split_char) if len(x.strip()) == word_length and x.strip().lower()==x.strip() and x.strip().isalpha()]
          self.make_histogram()

     def make_histogram (self):

          """Forms a histogram of the letters of the alphabet by frequency"""

          print("MAKING HISTOGRAM")

          total_characters = 0
          self.histogram = {}
          total_size = len(self.words) * len(self.words[0])
          for word in self.words:
               for character in word:
                    if character not in self.histogram:
                         self.histogram[character] = 1
                    else:
                         self.histogram[character] = self.histogram[character]+1
                    total_characters += 1
               if total_characters % 100==0:
                    print(total_characters,'/',total_size)

          for character in self.histogram:
               self.histogram[character] = self.histogram[character]/total_characters

     def value_word (self, word):

          """Returns a value indicating total of the frequency of each letter in a word"""

          total_value = 0
          for character in set(word):
               total_value += self.histogram[character]
          return total_value


     def compare_word (self, word_a, word_b):

          """Compares one word A to another B and returns a boolean value (True if they are identical) and
          a schema in the form of a tuple indicating the match between the two words:
               (1) list of positions in A that match perfectly.
               (2) list of positions in B where the letter is found in B
               (3) list of positions in A that don't match at all.

               For example: word A=cat, word b=tab
               Returns False, ([1],[2],[0])
          """
               

          matches, perfect, almost, not_at_all = False, [],[],[]
          if word_a == word_b:
               matches = True
               perfect = list(range(len(word_a)))
               
          
          else:
               
               for position in range(len(word_a)):
                    if word_a[position] == word_b[position]:
                         perfect.append(position)
                         
                    elif word_a[position] in word_b:
                              almost.append(position)
                    else:
                         not_at_all.append(position)
          return matches, (perfect, almost, not_at_all)

     def proper_first_word (self, word):

          """Tests if the first guess contains more than one vowel"""

          if len(set(word)) != len(word):
               return False
          vowels = ''
          for vowel in 'aeouiy':
               if vowel in word:
                    vowels += vowel
          if len(vowels)==1:
               return False
          return True
     
               

     def get_possible_words (self, word, all_words, schema):

          """Returns all the words from the list that match the schema"""

          def fits_perfectly (letter, position, word):

               """True if letter is in the word at the given position"""


               if position < len (word) and word[position] == letter:
                    return True
               return False

          def fits_almost (letter, position, word):

               """True if letter is in the word, but not in the given position"""

               if letter in word:
                    return True
               return False
          def fits_not_at_all (letter, position, word):

               """True if letter is not found in the word"""
               
               if letter in word:
                    return False
               return True 

          def apply_to_word (word_a, word_b, positions, function):

               """Applies the given function to all the positions in word a
               comparing it to word b
               """

               for pos in positions:

                    if not function(word_a[pos],pos,word_b):
                         return False
               return True

          return_list = []
          for to_check in all_words:
               if (apply_to_word(word, to_check, schema[0], fits_perfectly) and
                   apply_to_word(word, to_check, schema[1], fits_almost) and
                   apply_to_word(word, to_check, schema[2], fits_not_at_all)):

                    return_list.append(to_check)
          return return_list

     def show (self, word, schema):

          """Returns a string display the result of a comparison"""
          
          result = ''

          for position in range(len(word)):
               if position in schema[0]:
                    result+=word[position].upper()
               elif position in schema[1]:
                    result+=word[position]
               else:
                    result += '_'
          return result
     
               

     def solve (self,to_solve,mode=1,printing=True):

          """Solves the to_solve, appling the given mode.
               Mode 0 = Frequency
               Mode 1 = Random
               Mode 2 = Random + Frequency
               """

          already_chosen = set()
          all_words = list(self.words)
          

          counter = 1

          while True:

               if mode==1:
                    #Choosing the word randomly
                    
                    try_this = random.choice(all_words)
                    
               elif mode==2:
                    #Combining both methods
                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    try_this = random.choice(all_words[0:int(len(all_words)/10)+1])

               else:
                    
                    #Choosing the word with the highest frequency value


                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    try_this = all_words[0]
                    
                    
               already_chosen.add(try_this)
               if printing:
               
                    print('GUESS #',counter,' = ',try_this)
               
               solved, schema = self.compare_word (try_this, to_solve)
               if printing:
                    print(self.show(try_this, schema))
               
               all_words = self.get_possible_words (try_this,all_words, schema)
               if try_this in all_words:
                    all_words.pop(all_words.index(try_this))


               if solved:
                    return counter 
               counter += 1
               
     def test (self,mode=0):

          """Tests with a randomly chosen word"""

          answer = random.choice(self.words)
          print('ANSWER = ',answer)
          print()
          
          self.solve(answer,mode=mode)

     def show_about (self):

          """Shows description of app"""
          
          print(self.about)


     def compare_methods (self,iterations=100):

          """Compares the results of the different methods for the given number of iterations"""
          

          results = {0:0,
                     1:0,
                     2:0}

          for iteration in range(1,iterations+1):

               
               answer = random.choice(self.words)
               result_list = []
               for mode in range(3):
                    
                    

                    how_many_tries = self.solve(answer,mode,printing=False)
                    results[mode] += how_many_tries
                    result_list.append(str(how_many_tries))
               print('ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))

          for mode in range(3):

               results[mode] = results[mode]/iteration
               print(mode,
                     '/',
                     {0:"FREQUENCY",
                      1:"RANDOM",
                      2:"RANDOM+FREQUENCY"}[mode],
                     ' = ',
                     results[mode])

 

if __name__ == "__main__":

     wordle = Wordle_Solver()
     wordle.show_about()
     try:
          word_length = int(input('ENTER WORD LENGTH!'))
     except:
          word_length = 5
     wordle.constitute(word_length)
     
     


     while True:

          answer  = input('\n\nENTER A '+str(word_length)+' letter word or RETURN to choose a word at random or X to compare ')

          if answer == 'X':
               while True:
                    iterations = input('How many iterations? ')
                    if iterations.isnumeric():
                         break
               iterations = int(iterations)
               wordle.compare_methods(iterations)
          elif not answer:
               print('CHOOSING WORDS RANDOMLY...')
               wordle.test(1)
               print()
               print('OPTIMIZING FOR FREQUENCY...')
               wordle.test(0)
               print()
               print('FREQUENCY WITH RANDOMNESS...')
               wordle.test(2)
               
          elif answer in wordle.words:
               if len(answer) == word_length:
                    print('CHOOSING WORDS RANDOMLY...')
                    wordle.solve(answer,1)
                    print()
                    print('OPTIMIZING FOR FREQUENCY...')
                    wordle.solve(answer,0)
                    print()
                    print('FREQUENCY WITH RANDOMNESS...')
                    wordle.solve(answer,2)
                    print()
          else:
               print('I KNOW A LOT OF WORDS... but ',answer,'!!!! Really!!!')
               
                    
               
               

               

               

               
                    

          
                         
                    
          
          
                          

               
          
          


     
                
                



          
          


          
               
          
          





          
          


