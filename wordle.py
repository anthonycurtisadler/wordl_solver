import os, random
import math
import copy 
os.system('color F0')




class Wordle_Solver:


     def __init__ (self):

          name_dict = {1:'words.txt',
                      2:'smallwords.txt',
                      3:'smallerwords.txt',
                      4:'scrabblewords.txt'}

          word_list= []
          inp = None
          self.log = []
          self.saved = []
          self.saved_results = {}
          self.function = math.sqrt #FOR mode 5
          self.first_divider = 30 #For mode 3
          self.second_divider = 60 #For mode 4
          self.cut_off = 300
          self.words = []
          self.choose_words = []
          self.hard = True
          
          
          
          # GET TEXT FILE
          self.filename, self.textfile, self.split_char = self.open_file()


          dictionary_file_name = 'DIC_'+self.filename.split('_')[1]+'.txt'
          try:
               dictionaryfile = open(dictionary_file_name,'r', encoding='utf-8')
               self.dictionaryfile = dictionaryfile.read()
               print(dictionary_file_name+ ' OPENED!\n')
          except:
               print(dictionary_file_name+ ' COULD NOT OPEN!\n')
               self.dictionaryfile = None
          
     

          self.script_defaults = {0:'f',
                          1:'c',
                          2:'[60]ra',
                          3:'[60]rb',
                          4:'[120]ra',
                          5:'[120]*rb',
                          6:'{arise}[60]xa',
                          7:'1000.[60]ra;ta'}
                                  
          self.scripts = copy.deepcopy(self.script_defaults)

          self.about = """
          WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordle/)

          THE VOCABULARY IS VERY LARGE and STRANGE.

          YOU CAN ALSO PLAY THE WORDLE GAME IN BOTH EASY AND HARD MODE.
          IN THE HARD MODE, YOU HAVE TO SELECT WORDS FOLLOWING PREVIOUS CONSTRAINTS.
          

             """

          self.script_help = """
A STRATEGY SCRIPT CONSISTS OF A SERIES OF STRAGIES separated by SEMICOLONS.
    S1;S2;S3;S4

The FIRST STRATEGY may include a WORD to us in curly brackets
ALL may include a STRATEGY CODE and an optional DIVIDER, in square brackets

STRATEGY CODES INCLUDE:

* = to use frequency by char 
i = get best word by the least average size
     of the subsequent groups it generates (=information)
c = choose randomly from the group of words with highest frequency value
f = choose by frequency rank
r = choose word randomly from the top 1/DIVIDER of words 
x = choose word randomly from the top words, but applying formula (default = square root)
r and x can be combined with a and b, or used alone.
a = rank words by frequency but choose only from the smaller set of words to choose 
b = rank words by frequency but use any word
ta = top word by frequency
tb = top word by frequency from choice words

#. at beginning of STRATEGY to indicate the cut off in the size of the words for the strategy to be applicable.




"""
          
     def open_file (self):

          allfiles = os.listdir()
          filename, textfile, split_char = None, None, None 

          files_to_show = [x for x in allfiles if x.endswith('.txt') and x.startswith('WORDS_') and not 'freq' in x]
          for line, f in enumerate(files_to_show):
               print(line,' : ',f)

          while True:
               file_number = input('SELECT FILE TO LOAD?')
               if file_number.isnumeric() and 0<=int(file_number)<len(files_to_show):
                    filename = files_to_show[int(file_number)]
                    
                    
               if not filename.startswith('DIC_'):
                         print('GETTING '+filename+'! ')

                         textfile = open(filename,'r', encoding='utf-8')
                         textfile=textfile.read()
                         print(filename+' OPENED! \n')
                         break
               else:
                    break
                    
          split_char = '\n'
                         
                    #To find the character dividing the words in the file
          return filename, textfile, split_char 
               
               

          
          
               

     def constitute (self,word_length):

          """Loads in list of words from textfile"""

          self.word_length = word_length

          if '_NS_' in self.filename:
               new_file_name = self.filename.split('_NS_')[0]+'_S_'+self.filename.split('_NS_')[1]
               solutions = open(new_file_name,'r', encoding='utf-8')
               solutions = solutions.read()
               self.choose_words = [x.strip() for x in solutions.split('\n') if len(x.strip()) == 5]
              
          if self.textfile:
        
               self.choose_words = None
               self.words = [x.strip() for x in self.textfile.split(self.split_char)
                                  if len(x.strip()) == word_length and x.strip().lower()==x.strip() and x.strip().isalpha()]
               print('THERE ARE ',len(self.words),' WORDS IN THIS FILE')

          input('PRESS RETURN TO CONTINUE')
          self.histogram = None
          self.letter_histogram = None
          self.dictionary = {}
          if self.dictionaryfile:
          
               for counter, line in enumerate(self.dictionaryfile.split('\n')):
                    word, definition = line.split('\t')[0].lower().strip(),line.split('\t')[1].strip()
                    if len(word) == self.word_length:
                              
                         self.dictionary[word] = definition
                         if  not self.textfile:
                              self.words.append(word)

          self.use_information = input('DO you want to use result size for mode 1?') in ['yes',' ','YES','Y','y','sure']
          if self.choose_words:
               self.histogram = self.make_histogram(word_list=self.choose_words)
          else:
               self.histogram = self.make_histogram()
          self.make_letter_histogram()

                    
     def get_answer (self):

          if self.choose_words:
               return random.choice(self.choose_words)
          else:
               return random.choice(self.words) 

     def make_histogram (self,by_letter=False,position=0, word_list=None):

          """Forms a histogram of the letters of the alphabet by frequency"""
          if word_list is None:
               word_list = self.words

          if not by_letter:
               histogram = {}

               hist_textfile = self.filename.split('.')[0]+'freq'+str(self.word_length)+'.txt'
               
               histo_file = None
               try:
                    histo_file = open(hist_textfile,'r', encoding='utf-8')
                    histo_file_text = histo_file.read()
               except:
                    print("CAN'T READ!!!")
                    histo_file_text = ''
               if histo_file_text:
                    print('LOADING HISTOGRAM')

                    for line in histo_file_text.split('\n'):
                         if '\t' in line:
                              letter, value = line.split('\t')[0].strip(),line.split('\t')[1].strip()
                              if '/' not in letter:
                                   histogram[letter] = float(value)
                              else:
                                   letter, pos = key.split('/')[0].strip(), key.split('/')[1].strip()
                                   if pos == position:
                                        histogram[letter] = float(value)
                    histo_file.close()
                    
                    return histogram
               if not histo_file is None:
                    histo_file.close()
               
          
                         
          

          print("MAKING A HISTOGRAM FOR "+self.filename)
          print("THIS MAY TAKE A FEW MINUTES!!")
          
          
          

          total_characters = 0
          histogram = {}

          if not by_letter:
               total_size = len(word_list) * len(word_list[0])
               for word in word_list:
                    for character in word:
                         if character not in histogram:
                              histogram[character] = 1
                         else:
                              histogram[character] = histogram[character]+1
                         total_characters += 1
                    if total_characters % 1000==0:
                         print(total_characters,'/',total_size,end='; ')
                    
                         
          else:

               total_size = len(word_list)
               for word in word_list:
                    if word[position] not in histogram:
                         histogram[word[position]] = 1
                    else:
                         histogram[word[position]] = histogram[word[position]]+1
                    total_characters += 1
                    if total_characters % 1000==0:
                         print(total_characters,'/',total_size,end='; ')
                    
                         
          for character in histogram:
               histogram[character] = histogram[character]/total_characters


          print('_______________')

          if not by_letter:

               histo_file = open(hist_textfile,'at', encoding='utf-8')
          
               for chara in histogram:
                    print('SAVING ',chara)
                    histo_file.writelines(chara+'\t'+str(histogram[chara])+'\n')
               histo_file.close()
               
          print()
          return histogram

     def make_letter_histogram (self):

          """Form a histogram of frequency by individual letters"""


          hist_textfile = self.filename.split('.')[0]+'posfreq'+str(self.word_length)+'.txt'
          self.letter_histogram = {}
          
          
          histo_file = None
          try:
               histo_file = open(hist_textfile,'r', encoding='utf-8')
               histo_file_text = histo_file.read()
          except:
               print("CAN'T READ!!!")
               histo_file_text = ''
          if histo_file_text:
               print('LOADING HISTOGRAM')

               for line in histo_file_text.split('\n'):
                    if '\t' in line:
                         letter, value = line.split('\t')[0].strip(),line.split('\t')[1].strip()
                         if '/' in letter:
                              letter, pos = letter.split('/')[0].strip(), int(letter.split('/')[1].strip())
                              if not pos in self.letter_histogram:
                                   self.letter_histogram[pos] = {}
                              self.letter_histogram[pos][letter] = float(value)
               histo_file.close()
               return None 
                    
          if not histo_file is None:
               histo_file.close()
                    

          self.letter_histogram = {}
          histo_file = open(hist_textfile,'at', encoding='utf-8')

          
          for position in range(self.word_length):
               self.letter_histogram[position] = self.make_histogram(by_letter=True,position=position)
               for letter in self.letter_histogram[position]:
                    histo_file.writelines(letter+'/'+str(position)+'\t'+str(self.letter_histogram[position][letter])+'\n')
                    

               

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
                    average = sum(results[answer_word])/len(results[answer_word])
                    deviation = sum([abs(average-x) for x in results[answer_word]])/len(results[answer_word])
                    
                    results[answer_word] = average + deviation
##                    print(answer_word,' avr:',int(average),'dev:',int(deviation),'total:',
##                          int(results[answer_word]),'freq:',
##                          self.value_word(answer_word),'freq by char:',self.value_word_by_char(answer_word))
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

               if letter in word and not word[position]==letter:
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
     
               

     def solve (self,to_solve,mode=1,script=None,printing=True,play_mode = False, hard=None, header='',show_definition=True,rank_position=0,first_word='',cut_off=300):

          """Basic routine for solving a wordl, applying different approaches"""
          if hard is None:
               hard = self.hard
          
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


          def with_play_mode (all_words=None):

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
               return try_this


          def solve_mode (all_words=None,script='r',schema_string=None,already_chosen=None,rank_position=None):

               extract = lambda x,y,z: x.split(y)[1].split(z)[0].strip()
               outside =lambda x,y,z: x.split(y)[0]+x.split(z)[1]


               def solve_phrase (all_words=None,phrase='r',schema_string=None,already_chosen=None,rank_position=None):

                    if '{' in phrase and '}' in phrase:
                         if len(all_words) == len(self.words):
                              try_this = extract(phrase,'{','}')
                              return try_this
                         
                         
                    if '[' in phrase and ']' in phrase:
                         divider = int(extract(phrase,'[',']'))
                         phrase = outside(phrase,'[',']')
                         add_to = 1 
                    else:
                         divider = 1
                         add_to = 0

                    value_function = self.value_word

                    if '*' in phrase:
                         value_function = self.value_word_by_char  
                         
                    if 'i' in phrase:
                         if self.histogram and self.use_information:
                              try_this = self.get_best_word_by_information(list(all_words),schema_string=last_schema_string,already_chosen=already_chosen)
                         else:
                              try_this = random.choice(all_words)
                         return try_this
                    elif 'c' in phrase:
                         all_words = sorted(all_words,key=lambda x:-(value_function(x)))
                         top_value = value_function(all_words[0])
                         pos = 0
                         for pos, w in enumerate(all_words):
                              if value_function(w) < top_value:
                                   break
                         try_this = random.choice(all_words[0:pos+1])
                         return try_this
                    elif 'f' in phrase:
                         try_this = all_words[int(len(all_words)*rank_position)]
                         return try_this
                    elif 'r' in phrase and not 'a' in phrase and not 'b' in phrase:
                         up_to_here = int(len(all_words)/divider)+add_to
                         if up_to_here == 0:
                              up_to_here = 1
                         if up_to_here > len(all_words):
                              up_to_here = len(all_words)
                         try_this = random.choice(all_words[0:up_to_here])
                         return try_this
                    elif 'x' in phrase and not 'a' in phrase and not 'b' in phrase:
                         try_this = random.choice(all_words[0:int(self.function(len(all_words)))])
                    elif 'a' in phrase and self.choose_words:
                         all_words = [x for x in sorted(all_words,key=lambda x:-(value_function(x))) if x in self.choose_words]
                    elif 'b' in phrase:
                         all_words = sorted(all_words,key=lambda x:-(value_function(x)))
                    if 'r' in phrase or 'x' in phrase:
                         up_to_here = int(len(all_words)/divider)+add_to
                         if up_to_here == 0:
                              up_to_here = 1
                         if up_to_here > len(all_words):
                              up_to_here = len(all_words)
                              
                         try_this = random.choice(all_words[0:up_to_here])
                         return try_this
                    elif 't' in phrase:
                         try_this = all_words[0]
                         return try_this 
     
                         
                                                  
                                        
                    else:
                         return all_words[0]         
                         
                    
                         

               if ';' not in script:
                    y =solve_phrase(all_words=all_words,phrase=script,schema_string=last_schema_string,already_chosen=already_chosen, rank_position=rank_position)
                    return y,script
               
                    
               elif not script:
                    return solve_phrase(all_words=all_words,phrase='r',schema_string=last_schema_string,already_chosen=already_chosen, rank_position=rank_position),script
               else:

                    while (';' in script
                      and '.' in script.split(';')[0]
                      and script.split('.')[0].strip().isnumeric()):
                         cut_off = int(script.split('.')[0].strip())
                         if len(all_words) < cut_off:
                              script = ';'.join(script.split(';'))[1:]
                         else:
                           break
                         
                    phrase = script.split(';')[0]
                    script = ';'.join(script.split(';')[1:])
                    return solve_phrase(all_words=all_words,phrase=phrase,schema_string=last_schema_string,already_chosen=already_chosen, rank_position=rank_position),script
                    
          if script is None:

               script = self.scripts[mode]
               print('SCRIPT=',script)

          while True:

               try_this = None
               hinted = False

              
               if play_mode:
                    
                    try_this = with_play_mode(all_words=all_words)
       
               else:

                    try_this, script = solve_mode(all_words=all_words,
                                                  script = script,
                                                  schema_string=last_schema_string,
                                                  already_chosen=already_chosen,
                                                  rank_position=rank_position)



                    
                    

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
                    if show_definition and (override or mode == max(self.scripts.keys())) and to_solve in self.dictionary:
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

          answer = get_answer() 
          
          print('ANSWER = ',answer)
          print()
          
          self.solve(answer,mode=mode)


     def show_about (self):

          """Shows description of app"""
          
          print(self.about)

     def find_optimum_cut_off (self):


          def once_through (words,cut_off):

               total_count = 0
               worst_case = 0

               for answer in words:

                    how_many_tries = self.solve(answer,mode=3,printing=False,show_definition=False,cut_off=cut_off)
                    total_count += how_many_tries
                    if how_many_tries > worst_case:
                         worst_case = how_many_tries

               return total_count/len(words), worst_case
          
                    

          test_set = []
          constitute_test_set = [x[1] for x in enumerate(self.choose_words) if x[0]%10 == 0]
          for cut_off in [x*50 for x in range(1,40)]:

               print(cut_off, once_through(constitute_test_set, cut_off))
                     
   
               


     def compare_methods (self,iterations=100,limited_to=[0,1,2,3,4,5,6]):

          """Compares the results of the different methods for the given number of iterations"""

          results = {}
          for m in self.scripts:
               results[m]=0


          for iteration in range(1,iterations+1):

               
               answer = self.get_answer()
               print('ANSWER = ',answer)
               result_list = []
               for mode in self.scripts:
                    if mode in limited_to:
                         print(mode)
                         
                         

                         how_many_tries = self.solve(answer,mode,printing=True,show_definition=False)
                         results[mode] += how_many_tries
                         result_list.append(str(how_many_tries))
               print('ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))

          for mode in self.scripts:
               if mode in limited_to:

                    results[mode] = results[mode]/iteration
                    print('\n',mode,
                          '/',
                          self.scripts[mode],
                          ' = ',
                          results[mode])

     def word_compare (self,iterations=100,depth=300):

          """Compare results using different first words"""

          
          results = {}
          for word in sorted(self.words,key=lambda x:-(self.value_word(x)))[0:min([depth,len(self.words)])]:
               print(word,end='')
               results[word] = 0
               for iteration in range(1,iterations+1):

               
                    answer = self.get_answer()
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

               
                    answer = self.get_answer()
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
               print('FAILED')
               word_length = 5
          self.constitute(word_length)
          
          


          while True:

               answer  = input('\n\nENTER A '+str(word_length)
                               +' letter word, <ENTER> to choose a random word, (C)ompare, (E)dit modes, set(F)unction, R(ank compare) \n'+
                               'or (P)lay, or (H)ard play, (L)og,\n (S)ave last, (T)est a single word, (O)ptimize cutoff,\n'+
                               '  (A)pply schema, or (Q)uit  ').lower()
               

               if answer in ['c','r','w']:
                    while True:
                         iterations = input('How many iterations? ')
                         if iterations.isnumeric():
                              break
                    iterations = int(iterations)
                    if answer == 'c':
                         modes_to_use = [int(x.strip())
                                         for x in input('ENTER MODES to use from '
                                                        +', '.join(sorted([str(x) for x in self.scripts.keys()]))).split(',')
                                         if x.strip().isnumeric() and int(x.strip()) in self.scripts]
                                         
                       
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
               elif answer == 'o':
                    self.find_optimum_cut_off()
                    
                   
               
               elif answer == 'f':
                    while True:
                         funct = input("New function for f mode")
                         if not funct:
                              self.function  = math.sqrt
                              break
                         else:
                              try:
                                   function = eval(funct)
                                   print('100 / '+str(function(100)))
                                   
                                   self.function = function
                                   break
                              except:
                                   print('FUNCTION failed')

               elif answer == 'e':
          

                    while True:

                         print('ALL MODES')
                         for mode in sorted(list(self.scripts)):
                              print(mode,' = ',self.scripts[mode])
                         print()
                         command = input('(D)elete, (A)dd, (R)estore, (Q)uit, (C)lear, (H)elp').upper()
                         if command == 'D':
                              to_delete = input('DELETE #')
                              if to_delete.isnumeric() and int(to_delete) in self.scripts:
                                   del(self.scripts[int(to_delete)])
                         elif command == 'A':
                              new_script = input('ENTER NEW SCRIPT')
                              if self.scripts:
                                   maximum_key =max(list(self.scripts))
                              else:
                                   maximum_key = -1
                              new_key = maximum_key+1
                              self.scripts[new_key] = new_script
                         elif command == 'C':
                              self.scripts = {}
                         elif command == 'R':
                              self.scripts = copy.deepcopy(self.script_defaults)
                         elif command == 'H':
                              print(self.script_help)
                              
                         elif command == 'Q':
                              break
                         
                              
                    
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
                    answer = self.get_answer()
                    self.solve(to_solve=answer,play_mode=True,hard=hard)
                    
               elif not answer:
                    answer = self.get_answer()
                    print('ANSWER === ',answer)
                    for m in self.scripts:

                         self.solve(answer,mode=m,header=self.scripts[m])
                         
                 
               elif answer in self.words:
                    if len(answer) == word_length:

                         for m in self.scripts:
                              print(self.scripts[m])
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
          
               
               
          
          
     
        
