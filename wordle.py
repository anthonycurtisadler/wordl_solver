import os, random
import math
os.system('color F0')




class Wordle_Solver:


     def __init__ (self):

          name_dict = {1:'words.txt',
                      2:'smallwords.txt',
                      3:'smallerwords.txt',
                      4:'scrabblewords.txt'}

          self.words = []
          inp = None
          self.log = []
          self.saved = []
          self.saved_results = {}
          self.function = math.sqrt #FOR mode 5
          self.first_divider = 30 #For mode 3
          self.second_divider = 60 #For mode 4
          
          while inp not in name_dict:
               for x in sorted(name_dict):
                    print (str(x),' = ',name_dict[x])
                    
               inp = input('ENTER NUMBER TO LOAD WORDS ')
               print('\n\n')
               if inp.isnumeric():
                    inp = int(inp)
                    filename = name_dict[inp]
          
          
          
          # GET TEXT FILE
          self.textfile = None 
          if not filename == 'scrabblewords.txt':
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

          dictionaryfile = open('scrabblewords.txt','r', encoding='utf-8')
          self.dictionaryfile = dictionaryfile.read()
          print('scrabble.txt OPENED! \n')
          
     
          self.mode_descriptions = {0:"FREQUENCY",
                      1:"RANDOM",
                      2:"RANDOM+FREQUENCY /"+str(self.first_divider),
                      3:"RANDOM+FREQUENCY /"+str(self.second_divider),
                      4:"RANDOM+FREQUENCY Sqrt",
                      5:"RANDOM+FREQUENCY skimming",
                      6:"FREQUENCY BY CHARACTER"}
          
          
          self.about = """
          WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordle/)

          THE VOCABULARY IS VERY LARGE and STRANGE.

          APPLIES THREE DIFFERENT SOLVING APPROACHES:
               (1) Chooses the word with the most frequently appearing characters
               (2) Chooses the word randomly
               (3) Chooses randomly from a fraction of the frequently appearing characters
               (4) Choose word with the most frequent character by position.
               (5) Choose from the words that produce the small average result 

          YOU CAN ALSO PLAY THE WORDLE GAME IN BOTH EASY AND HARD MODE.
          IN THE HARD MODE, YOU HAVE TO SELECT WORDS FOLLOWING PREVIOUS CONSTRAINTS.
          

             """
     def constitute (self,word_length):

          """Loads in list of words from textfile"""

          self.word_length = word_length
          if self.textfile:
               self.words = [x.strip() for x in self.textfile.split(self.split_char) if len(x.strip()) == word_length and x.strip().lower()==x.strip() and x.strip().isalpha()]
               print('THERE ARE ',len(self.words),' WORDS IN THIS FILE')
          input('PRESS RETURN TO CONTINUE')
          self.histogram = None
          self.letter_histogram = None
          self.dictionary = {}
          
          
          for counter, line in enumerate(self.dictionaryfile.split('\n')):
               word, definition = line.split('\t')[0].lower().strip(),line.split('\t')[1].strip()
               if len(word) == self.word_length:
                         
                    self.dictionary[word] = definition
                    if  not self.textfile:
                         self.words.append(word)
          self.use_information = False
          if input('DO YOU WANT TO CREATE A FREQUENCY HISTOGRAM? This might take a while... ') in ['yes',' ','YES','Y','y','sure']:
               self.use_information = input('DO you want to use result size for mode 1?') in ['yes',' ','YES','Y','y','sure']
               
               self.histogram = self.make_histogram()
               self.make_letter_histogram()
               if self.use_information:
                    self.mode_descriptions[1] = "BY SIZE OF THE RESULT OF APPLYING TO WORDS"
          

     def make_histogram (self,by_letter=False,position=0):

          """Forms a histogram of the letters of the alphabet by frequency"""

          print("MAKING HISTOGRAM\n\n'")
          histogram = {}



          total_characters = 0
          histogram = {}

          if not by_letter:
               total_size = len(self.words) * len(self.words[0])
               for word in self.words:
                    for character in word:
                         if character not in histogram:
                              histogram[character] = 1
                         else:
                              histogram[character] = histogram[character]+1
                         total_characters += 1
                    if total_characters % 100==0:
                         print(total_characters,'/',total_size)
          else:

               total_size = len(self.words)
               for word in self.words:
                    if word[position] not in histogram:
                         histogram[word[position]] = 1
                    else:
                         histogram[word[position]] = histogram[word[position]]+1
                    total_characters += 1
                    if total_characters % 100==0:
                         print(total_characters,'/',total_size)
                         
          for character in histogram:
               histogram[character] = histogram[character]/total_characters


          print('_______________')
          return histogram

     def make_letter_histogram (self):

          """Form a histogram of frequency by individual letters"""

          self.letter_histogram = {}
          for position in range(self.word_length):
               self.letter_histogram[position] = self.make_histogram(by_letter=True,position=position)

               

     def value_word (self, word):

          """Returns a value indicating total of the frequency of each letter in a word"""

          total_value = 0
          for character in set(word):
               total_value += self.histogram[character]
          return total_value / self.word_length

     def value_word_by_char (self,word):

          """Returns a value indicating the total of the frequency of each letter in a word using
          a histogram that distinguishes frequency by position"""

          total_value = 0
          found_letters = set()
          for position, character in enumerate(word):
               if character  not in found_letters:
                    total_value += self.letter_histogram[position][character]
               found_letters.add(character)
          return total_value/len(set(word))

     def get_best_word_by_information (self, all_words,schema_string=None,already_chosen=None):

          """Returns the word that gives the smallest average result set when tested across all the words"""

         
          
          if schema_string is None:
               schema_string = '_'*self.word_length

          if self.saved_results and not already_chosen:
               results = self.saved_results
          else:
               
               up_to_here = int(len(all_words)**(1/3))
               
               results = {}
               
               for answer_word in sorted(all_words, key=lambda x:-(self.value_word(x)))[0:up_to_here]:
                    
                    results[answer_word] = []
                    for try_word in all_words:
                         solved, schema = self.compare_word (try_word, answer_word)
                         results[answer_word].append(self.get_possible_words(try_word,all_words,schema,length_only=True))
                    results[answer_word] = sum(results[answer_word])/len(results[answer_word])
                    print(answer_word,results[answer_word])
               if not already_chosen and not self.saved_results:
                    self.saved_results = results
          ordered_results = sorted([x for x in results.keys() if x not in already_chosen],key = lambda x:results[x])
          least_value = results[ordered_results[0]]
          
          pos = 0
          for pos, w in enumerate(ordered_results):
               if results[w] > least_value:
                    break
          
          return random.choice(ordered_results[0:pos+1])

          


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
     
               

     def get_possible_words (self, word, all_words, schema,length_only=False):

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

          if length_only:

               counter = 0
               

               for to_check in all_words:
                    if (apply_to_word(word, to_check, schema[0], fits_perfectly) and
                        apply_to_word(word, to_check, schema[1], fits_almost) and
                        apply_to_word(word, to_check, schema[2], fits_not_at_all)):

                         counter += 1
               return counter 
               

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
     
               

     def solve (self,to_solve,mode=1,printing=True,play_mode = False, hard=False, header='',show_definition=True,rank_position=0,first_word=''):

          """Basic routine for solving a wordl, applying different approaches"""
          
          override = False #If true, then shows dictionary definition when not in mode 6
          
          if not mode == 1 and not self.histogram:
               return 0
          elif (mode == 1 and not self.histogram) or play_mode:
               override = True 

          def get_letter (word,position):

               """Fetches the letter from the position in the word"""

               return word[position]

          def get_all_letters (word,position_set):

               """Gets all the letters from the word at the the given positions"""
               return_set = set()
               for position in position_set:
                    return_set.add(get_letter(word,position))
               return return_set
          

          def translate_schema (word,schema):

               """Translates the schema into characters"""
               return get_all_letters(word,schema[0]),get_all_letters(word,schema[1]),get_all_letters(word,schema[2])

          def format_alphabet (exact,almost,not_at_all):

               """For displaying the schema"""

               alphabet_list = []
               for letter in 'abcdefghijklmnopqrstuvwxyz':

                    if letter in exact:
                         alphabet_list.append('<<'+letter+'>>')
                    elif letter in almost:
                         alphabet_list.append('<'+letter+'>')
                    elif letter not in not_at_all:
                         alphabet_list.append(letter)
               return ' '.join(alphabet_list)

          def show_definition (definition):
               
               """Purges CAPITAL letters from definition"""
               
               definition = ' '+definition+' '
               for word in definition.split(' '):
                    if word.upper() == word:
                         definition = definition.replace(' '+word+' ',' '+'_'*len(word)+' ').strip()

               return definition
                                   

          

               

          """Solves the to_solve, appling the given mode.
               Mode 0 = Frequency
               Mode 1 = Random
               Mode 2-4 = Random + Frequency 10/20/30
               Mode 5 = Random + Frequency skimming
               Mode 6 = Positional Frequency
               """
          if header:
               print('\n'+header)
          already_chosen = set()
          all_words = list(self.words)
          

          counter = 1
          outcomes = []
          exact = set()
          almost = set()
          not_at_all = set()
          last_schema_string = '_'*self.word_length
          already_chosen = [] #This is necessary to keep get_word_by_information ending up in an infinite loop
          
                                   
          

          while True:

               try_this = None
               hinted = False

              
               if play_mode:
                    try_this = 'X'*self.word_length
                    print(format_alphabet(exact,almost,not_at_all))
                    while try_this not in all_words:
                         
                         print('TOTAL WORDS: ',len(all_words))
                         print()
                         try_this = input('ENTER '+str(self.word_length)+' DIGIT WORD, X(pose all), (L)ist by frequency (G)ive up, (H)int, (S)ave previous word ').lower()
                         if try_this == 'g':
                              try_this = to_solve
                         elif try_this in ['l']:
                              sorted_all_words = sorted(all_words, key=lambda x:-(self.value_word(x)))
                              print(', '.join([str(x[0])+' :'+x[1] for x in enumerate(sorted_all_words)]))
                         elif try_this == 'x':
                              print('\n'+', '.join([str(x[0])+': '+x[1] for x in enumerate(all_words)])+'\n')
                         elif try_this == 'h':
                              if to_solve in self.dictionary:
                                   if not hinted:
                                        if '(' in self.dictionary[to_solve] and ')' in self.dictionary[to_solve]:
                                             print(self.dictionary[to_solve].split('(')[1].split(')')[0])
                                        else:
                                             print('No specification')
                                        hinted = True
                                   elif hinted:
                                        print()
                                        print(show_definition(self.dictionary[to_solve]))
                                        print()
                         elif try_this == 's' and self.log:
                              self.saved.append(self.log[-1])
                              print('\nSAVED TO LOG: '+self.log[-1][0]+'\n')
                         elif len(try_this) < self.word_length:
                              print('TOO SHORT!')
                         elif len(try_this) > self.word_length:
                              print('TOO LONG!')
                         elif try_this not in self.words:
                              print('THIS IS NOT A VALID WORD')
                         elif try_this not in all_words:
                              print("INVALID CHOICE!")
                    

                              
                   
               elif mode==1:
##                    #Choosing the word randomly if no frequency dict or by information
##                    
##                    
                    if self.histogram and self.use_information:
                         try_this = self.get_best_word_by_information(list(all_words),schema_string=last_schema_string,already_chosen=already_chosen)
                    else:
                         try_this = random.choice(all_words)
                    
   
                    
               elif mode==2:
                    #Combining both methods
                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    try_this = random.choice(all_words[0:int(len(all_words)/self.first_divider)+1])


               elif mode==3:
                    #Combining both methods
                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    try_this = random.choice(all_words[0:int(len(all_words)/self.second_divider)+1])


               elif mode==4:
                    #Combining both methods
                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    up_to_here = int(self.function(len(all_words)))
                    if up_to_here < 1:
                         up_to_here = 1
                    try_this = random.choice(all_words[0:up_to_here])
                    


               elif mode==5:
                    #Combining both methods v.2
                    
                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    top_value = self.value_word(all_words[0])
                    pos = 0
                    for pos, w in enumerate(all_words):
                         if self.value_word(w) < top_value:
                              break
                    
                    try_this = random.choice(all_words[0:pos+1])


               elif mode==6 :


                    all_words = sorted(all_words,key=lambda x:-(self.value_word_by_char(x)))
                    top_value = self.value_word_by_char(all_words[0])
                    pos = 0
                    for pos, w in enumerate(all_words):
                         if self.value_word_by_char(w) < top_value:
                              break
                    
                    try_this = random.choice(all_words[0:pos+1])

                    
                    

               else:
                    
                    #Choosing the word with the highest frequency value

                    all_words = sorted(all_words,key=lambda x:-(self.value_word(x)))
                    if not first_word or counter>1:
                         try_this = all_words[int(len(all_words)*rank_position)]
                    else:
                         try_this = first_word 

                    
                    

               solved, schema = self.compare_word (try_this, to_solve)
               if play_mode:
                    a,b,c = translate_schema(try_this,schema)
                    exact.update(a)
                    almost.update(b)
                    not_at_all.update(c)
                    if self.histogram:
                         print('\nFREQUENCY VALUE ',self.value_word(try_this))
               last_schema_string = self.show(try_this, schema)
               if printing:
                    x = ' GUESS #'+str(counter)+' = '+try_this +' '+last_schema_string
                    if not play_mode:
               
                         print(x)
                    else:
                         outcomes.append(x)
                         print('\n'.join(outcomes))
                               
               
##               if printing:
##                    print(self.show(try_this, schema))
               if not (play_mode and not hard):
                    all_words = self.get_possible_words (try_this,all_words, schema)
               if try_this in all_words:
                    all_words.pop(all_words.index(try_this))


               if solved:
                    to_solve = to_solve.lower()
                    definition = ''
                    if show_definition and (override or mode == 6) and to_solve in self.dictionary:
                         definition = self.dictionary[to_solve]
                         print('\n'+definition+'\n')
                    self.log.append((to_solve, counter, definition))
                    return counter
               already_chosen.append(try_this)
               counter += 1

     def apply (self, schema_list_string):

          """Applies a list of schemas to return all the matching words"""

          def decode (entry):

               tried_that, result = entry.split('/')[0],entry.split('/')[1] 
               exactly= []
               almost= []
               not_at_all = []
               for position, char in enumerate(result):
                    if char != '_':
                         if char.lower() == char:
                              almost.append(position)
                         else:
                              exactly.append(position)
               not_at_all = list([tried_that.index(x) for x in tried_that if x.lower() not in result and x.upper() not in result])

               return tried_that, (exactly, almost, not_at_all)


          all_words = list(self.words)
          for entry in [x.strip() for x in schema_list_string.split(',')]:
               if ' ' in entry:
                    entry = entry.replace(' ','/')
               tried_that, schema = decode(entry)
               all_words = self.get_possible_words (tried_that,
                                                    all_words,
                                                    schema)
          return all_words 
             
     
     def show_list (self,list_to_show):

          """To desplay a list of results"""

          return_list = []

          for count, line_tupple in enumerate(list_to_show):
               return_list.append('  '+str(count)+' : '+line_tupple[0]+' = '+line_tupple[2]+' ('+str(line_tupple[1])+')')
          return '\n'.join(return_list)

               
               
     def test (self,mode=0):

          """Tests with a randomly chosen word"""

          answer = random.choice(self.words)
          
          print('ANSWER = ',answer)
          print()
          
          self.solve(answer,mode=mode)

     def get_word (self):

          """Retrieves a word"""

          return random.choice(self.words)

     def show_about (self):

          """Shows description of app"""
          
          print(self.about)


     def compare_methods (self,iterations=100,limited_to=[0,1,2,3,4,5,6]):

          """Compares the results of the different methods for the given number of iterations"""

          results = {}
          for m in self.mode_descriptions:
               results[m]=0


          for iteration in range(1,iterations+1):

               
               answer = random.choice(self.words)
               print('ANSWER = ',answer)
               result_list = []
               for mode in self.mode_descriptions:
                    if mode in limited_to:
                         print(mode)
                         
                         

                         how_many_tries = self.solve(answer,mode,printing=True,show_definition=False)
                         results[mode] += how_many_tries
                         result_list.append(str(how_many_tries))
               print('ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))

          for mode in self.mode_descriptions:
               if mode in limited_to:

                    results[mode] = results[mode]/iteration
                    print('\n',mode,
                          '/',
                          self.mode_descriptions[mode],
                          ' = ',
                          results[mode])

     def word_compare (self,iterations=100,depth=300):

          """Compare results using different first words"""

          
          results = {}
          for word in sorted(self.words,key=lambda x:-(self.value_word(x)))[0:min([depth,len(self.words)])]:
               print(word,end='')
               results[word] = 0
               for iteration in range(1,iterations+1):

               
                    answer = random.choice(self.words)
                    result_list = []
               
                    how_many_tries = self.solve(answer,mode=0,printing=False,show_definition=False,first_word=word)
                    results[word] += how_many_tries
                    result_list.append(str(how_many_tries))
##                    print('Value= ',value,' ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))
               result = results[word]/iterations
               print(' = ',result)
               results[word]  = result
               
          for word in sorted(results.keys(),key = lambda x:results[x]):
               print(results[word],' / ',word+' ('+str(self.value_word(word))+'/'+str(self.value_word_by_char(word))+')')
               
               
          

               
     def rank_compare (self,iterations=100,gradations=10):

          """Compares by different rankings according to frequency, for example top 10 percent, to 20 percent
          Doesn't use randomness"""

          results = {}
          
          for count in range(int((100/gradations))-1):

               print('count:=',count)
               value = count*(1/gradations)
               print('value:=',value)

               results[value] = 0
               for iteration in range(1,iterations+1):

               
                    answer = random.choice(self.words)
                    result_list = []
               
                    how_many_tries = self.solve(answer,mode=0,printing=False,show_definition=False, rank_position=value)
                    results[value] += how_many_tries
                    result_list.append(str(how_many_tries))
##                    print('Value= ',value,' ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))
               results[value]  = results[value]/iterations
          for count, value in enumerate(results):

##               print(str(count)+' : '+str(value)+' = '+str(results[value]))
               print(str(value)+'\t'+str(results[value]))
               

     def run (self):

          """Runs main loop"""

          self.show_about()
          try:
               word_length = int(input('ENTER WORD LENGTH! '))
          except:
               word_length = 5
          self.constitute(word_length)
          
          


          while True:

               answer  = input('\n\nENTER A '+str(word_length)
                               +' letter word, <ENTER> to choose a random word, C(ompare),s(E)t dividers, set(F)unction, R(ank compare) \n'+
                               'or (P)lay, or (H)ard play, (L)og,\n (S)ave last, (T)est a single word, (A)pply schema, or (Q)uit  ').lower()
               

               if answer in ['c','r','w']:
                    while True:
                         iterations = input('How many iterations? ')
                         if iterations.isnumeric():
                              break
                    iterations = int(iterations)
                    if answer == 'c':
                         modes_to_use = input('ENTER MODES from 0,2,3,4,5,6')
                         modes_to_use = [x for x in range(7) if str(x) in modes_to_use]
                         
                         
                         self.compare_methods(iterations,modes_to_use)
                         
                    elif answer == 'r':
                         
                         self.rank_compare(iterations)
                    else:
                         while True:
                              depth = input('Depth?' )
                              if depth.isnumeric():
                                   break
                         depth = int(depth)
                                       
                         self.word_compare(iterations,depth=depth)
               elif answer == 'e':
                    for d in [1,2]:
                         while True:
                              div = input('Enter divider #'+str(d))
                              if div.isnumeric() and 0<int(div)<10000:
                                   div = int(div)
                              break
                         if d==1:
                              self.first_divider = div
                              self.mode_descriptions[2] = "RANDOM+FREQUENCY /"+str(self.first_divider)
                         else:
                              self.second_divider = div
                              self.mode_descriptions[3] = "RANDOM+FREQUENCY /"+str(self.second_divider)
               elif answer == 'f':
                    while True:
                         funct = input("New function for mode 5")
                         if not funct:
                              self.function  = math.sqrt
                              self.mode_descriptions[4] = "FUNCTION sqrt"
                              break
                         else:
                              try:
                                   function = eval(funct)
                                   print('100 / '+str(function(100)))
                                   
                                   self.function = function
                                   self.mode_descriptions[4] = "FUNCTION "+funct
                                   break
                              except:
                                   print('FUNCTION failed')
                         
                         
                              
                         
                    
               elif answer == 't':
                    while True:
                         word = input('WORD? ')
                         if len(word) == self.word_length:
                              break
                    while True:
                         iterations = input('How many iterations? ')
                         if iterations.isnumeric():
                              break
                    iterations = int(iterations)
                    while True:
                         mode = input('Mode? ')
                         if mode in ['0','1','2','3','4','5','6']:
                              mode = int(mode)
                              break
                    result = 0
                    for i in range(iterations):
                         attempts = self.solve(to_solve=word,mode=mode)
                         print(i,' / ',attempts)
                         result += attempts
                    print('I WAS ABLE TO SOLVE ',word,' in ',result/iterations,' attempts on average!')
                    
                         
               elif answer in ['s']:
                    if self.log:
                         self.saved.append(self.log[-1])
                         print('\nSAVED TO LOG: '+self.log[-1][0]+'\n')
               elif answer in ['q','l']:
                    print('\nLOG')
                    print('\n'+self.show_list(self.log)+'\n')
                    print('SAVED')
                    print('\n'+self.show_list(self.saved)+'\n')  
                    if answer == 'q':
                         return self.saved
               elif answer in ['a']:
                    schema_list_string = input('ENTER guess/answer SEPARATED BY COMMAS')
                    try:
                         results = self.apply(schema_list_string)
                         print('\n'+', '.join([str(x[0])+': '+str(x[1]) for x in enumerate(results)])+'\n')
                    except:
                         print('\nERROR!\n')
               elif answer in ['p','h']:
                    hard = (answer == 'h')
                    answer = self.get_word()
                    self.solve(to_solve=answer,play_mode=True,hard=hard)
                    
               elif not answer:
                    answer = self.get_word()
                    print('ANSWER === ',answer)
                    for m in self.mode_descriptions:
                         self.solve(answer,mode=m,header=self.mode_descriptions[m])
                         
                 
               elif answer in self.words:
                    if len(answer) == word_length:

                         for m in self.mode_descriptions:
                              print(self.mode_descriptions[m])
                              self.solve(answer,mode=m)


               else:
                    print('I KNOW A LOT OF WORDS... but ',answer,'!!!! Really!!!')


if __name__ == "__main__":

     while True:
          wordle = Wordle_Solver()
          saved_results = wordle.run()
          logfile = open('log.txt','at', encoding='utf-8')
          for line in saved_results:
               logfile.writelines(line[0]+'\t'+line[2]+'\n')
          logfile.close()
          
               
               
          
          
     
        
