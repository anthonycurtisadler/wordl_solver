import os, random
import math
import copy
import datetime
os.system('color F0')





class Wordle_Solver:


     def __init__ (self):


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


          self.make_new_directory()       
          
          
          
          # GET TEXT FILE
          self.filename, self.textfile, self.split_char, self.language = self.open_file()


          dictionary_file_name = 'DIC_'+self.filename.split('_')[1]
          if not dictionary_file_name.endswith('.txt'):
                dictionary_file_name+='.txt'
          
     
          
          try:
               dictionaryfile = open('wordlists'+os.altsep+dictionary_file_name,
                                     'r', encoding='utf-8')
               self.dictionaryfile = dictionaryfile.read()
               print(dictionary_file_name+ ' OPENED!\n')
          except:
               print(dictionary_file_name+ ' COULD NOT OPEN!\n')
               self.dictionaryfile = None

     

          self.script_defaults = {0:'f',
                          1:'*f',
                          2:'**f',
                          3:'$f',
                          4:'$*f',
                          5:'$**f',
                          6:'{tares};i',
                          7:'{tares};$i',
                          8:'fr[60]'}
##          ,
##                          9:'~f',
##                          10:'{zylyl};~$i'
####

##          self.script_defaults = {0:'{stern};{yclad};fe$',
##                                  1:'{stern};{yclad};fe',
##                                  2:'{stern};{yclad};f$',
##                                  3:'{stern};{yclad};f'}
                                  
          self.scripts = copy.deepcopy(self.script_defaults)

          self.about = """
          WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordle/)

          YOU CAN USE ANY LIST OF WORDS, PLAY THE GAME OR SOLVE AUTOMATICALLY,
          AND AUTOMATICALLY TEST DIFFERENT SOLVING METHODS.

          YOU CAN ALSO PLAY THE WORDLE GAME IN BOTH EASY AND HARD MODE.
          IN THE HARD MODE, YOU HAVE TO SELECT WORDS FOLLOWING PREVIOUS CONSTRAINTS.
          

             """

          self.script_help = """
A STRATEGY SCRIPT CONSISTS OF A SERIES OF STRAGIES separated by SEMICOLONS.
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


"""
          
     def open_file (self):

          """To open file containing word lists"""

          allfiles = os.listdir(os.getcwd()+os.altsep+'wordlists'+os.altsep)
          filename, textfile, split_char, language = None, None, None, None 

          files_to_show = [x for x in allfiles if x.endswith('.txt') and (x.startswith('WORDS_') or x.startswith('DIC_')) and not 'freq' in x]
          for line, f in enumerate(files_to_show):
               print(line,' : ',f)

          while True:
               print()
               file_number = input('SELECT FILE TO LOAD?')
               if file_number.isnumeric() and 0<=int(file_number)<len(files_to_show):
                    filename = files_to_show[int(file_number)]
                    
                    
               if filename and not filename.startswith('DIC_'):
                         print('GETTING '+filename+'! ')

                         textfile = open('wordlists'+os.altsep+filename,'r', encoding='utf-8')
                         textfile=textfile.read()
                         print(filename+' OPENED! \n')
                         language = filename.split('_')[1].split('_')[0]
                         break
               elif filename:
                    language = filename.split('_')[1].split('_')[0].split('.')[0]
                    break
               
                    
          split_char = '\n'
          print()
                         
                    #To find the character dividing the words in the file
          return filename, textfile, split_char, language  
               
          

     def constitute (self,word_length):

          """Loads in list of words from textfile"""

          self.word_length = word_length
          self.choose_words = []

          if '_NS_' in self.filename:
               new_file_name = self.filename.split('_NS_')[0]+'_S_'+self.filename.split('_NS_')[1]
               solutions = open('wordlists'+os.altsep+new_file_name,'r', encoding='utf-8')
               solutions = solutions.read()
               self.choose_words = [x.strip() for x in solutions.split('\n') if len(x.strip()) == 5]
               print('THERE ARE ',len(self.choose_words),' SOLUTION WORDS')
              
          if self.textfile:
        
               
               self.words = [x.strip() for x in self.textfile.split(self.split_char)
                                  if len(x.strip()) == word_length and x.strip().lower()==x.strip() and x.strip().isalpha()]
               print('THERE ARE ',len(self.words),' WORDS IN THIS FILE')
               if self.choose_words:
                    self.words += self.choose_words

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
          

         
          if self.choose_words:
               self.histogram = self.make_histogram(word_list=self.choose_words)
               self.make_letter_histogram(word_list=self.choose_words)
          else:
               self.histogram = self.make_histogram()
               self.make_letter_histogram()
          self.dynamic_wordlist_storage = {}
          

     def make_new_directory (self,
                             directory_name='wordlists'):

        """Create a new directory to various types of folders"""

        full_path = os.getcwd()
        allfiles = os.listdir(full_path)
        return_text = ""

        if directory_name not in allfiles:
            try:
                os.mkdir(full_path+os.altsep+directory_name)
                return_text = 'NEW FOLDER CREATED: '+directory_name
            except:
                return_text = 'NEW FOLDER CREATION FAILED'
        if return_text:
             print (return_text)             

     def get_answer (self):

          """Chooses the answer to solve"""

          if self.choose_words:
               return random.choice(self.choose_words)
          else:
               return random.choice(self.words) 

     def make_histogram (self,by_letter=False,position=0, word_list=None,histo_object=None):

          """Forms a histogram of the letters of the alphabet by frequency"""
          self.make_new_directory('frequencylists')
          if histo_object is None:
                    histo_object = {}
          
          if word_list is None:
               word_list = self.words


          if not by_letter and (len(word_list) in (len(self.words),len(self.choose_words))):
               
               hist_textfile = self.filename.split('.')[0]+'freq'+str(self.word_length)+'.txt'
               
               histo_file = None
               try:
                    histo_file = open('frequencylists'+os.altsep+hist_textfile,
                                      'r', encoding='utf-8')
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
                                   histo_object[letter] = float(value)
                              else:
                                   letter, pos = key.split('/')[0].strip(), key.split('/')[1].strip()
                                   if pos == position:
                                        histo_object[letter] = float(value)
                    histo_file.close()
                    
                    return histo_object
               if not histo_file is None:
                    histo_file.close()
               
          
                    
          
          

          total_characters = 0 
          if not by_letter:


               total_number_of_words = len(word_list)
               all_letters = set()
               for word in word_list:
                    all_letters = all_letters.union(set(word))

               for letter in all_letters:
                    total_with_letter = 0
                    for word in word_list:
                         if letter in word:
                              total_with_letter += 1
                    histo_object[letter] = total_with_letter/total_number_of_words


                    
                         
          else:
               total_number_of_words = len(word_list)
               all_letters = set()
               for word in word_list:
                    all_letters.add(word[position])
        
               for letter in all_letters:
                    total_with_letter = 0
                    for word in word_list:
                         if letter == word[position]:
                              total_with_letter += 1
                    histo_object[letter] = total_with_letter/total_number_of_words


          if not by_letter and (len(word_list) in (len(self.words),len(self.choose_words))):

               histo_file = open('frequencylists'+os.altsep+
                                 hist_textfile,'at', encoding='utf-8')
          
               for chara in histo_object:
                    print('SAVING ',chara)
                    histo_file.writelines(chara+'\t'+str(histo_object[chara])+'\n')
               histo_file.close()
               
          return histo_object

     def make_letter_histogram (self,histo_object=None,word_list=None):

          """Form a histogram of frequency by individual letters"""

          if word_list is None:
               word_list = self.words
          
          if histo_object is None:
               self.letter_histogram = {}
               histo_object = self.letter_histogram

          if (len(word_list) in (len(self.words),len(self.choose_words))):
               hist_textfile = self.filename.split('.')[0]+'posfreq'+str(self.word_length)+'.txt'
          
               histo_file = None
               try:
                    histo_file = open('frequencylists'+os.altsep+hist_textfile,'r', encoding='utf-8')
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
                                   if not pos in histo_object:
                                        histo_object[pos] = {}
                                   histo_object[pos][letter] = float(value)
                    histo_file.close()
                    return histo_object
                         
               if not histo_file is None:
                    histo_file.close()
                         


               histo_file = open('frequencylists'+os.altsep+hist_textfile,'at', encoding='utf-8')

               
               for position in range(self.word_length):
                    histo_object[position] = self.make_histogram(by_letter=True,position=position,word_list=word_list)
                    for letter in histo_object[position]:
                         histo_file.writelines(letter+'/'+str(position)+'\t'+str(histo_object[position][letter])+'\n')
             
          else:

               for position in range(self.word_length):
                    histo_object[position] = self.make_histogram(by_letter=True,position=position,word_list=word_list)
          return histo_object
               

     def value_word (self,
                     word,
                     histo_tuple=None):

          

          """Returns a value indicating total of the frequency of each letter in a word"""
          if histo_tuple is None:
               histo_object = self.histogram
          else:
               histo_object = histo_tuple[0]
          total_value = 0
          for character in set(word):
               if character in histo_object:
                    total_value += histo_object[character]
          
          return total_value

     def value_word_by_char (self,
                             word,
                             histo_tuple=None):

          """Returns a value indicating the total of the frequency of each letter in a word using
          a histogram that distinguishes frequency by position"""
          if histo_tuple is None:
               histo_object = self.letter_histogram
          else:
               histo_object = histo_tuple[0]
          total_value = 0
          for position, character in enumerate(word):
               if position in histo_object and character in histo_object[position]:
                    total_value += histo_object[position][character]
          return total_value

     

     def compound_values (self,
                          word,
                          histo_tuple=None):

          """Combines application of value_word and value_by_char"""
          if histo_tuple is None:
               histo_object_one = None
               histo_object_two = None 
          else:
               histo_object_one = histo_tuple[0]
               histo_object_two = histo_tuple[1]
               
          return self.value_word(word,
                                 histo_tuple=(histo_object_one,))+self.value_word_by_char(word,
                                                                                    histo_tuple=(histo_object_two,))
     
          

     def get_best_word_by_information (self, all_words,over_list=None,choice_words=None,schema_string=None,already_chosen=None, mode=0):

          """Returns the word that gives the smallest average result set when tested across all the words"""

          if not choice_words:
               choice_words = all_words 
          
          if schema_string is None:
               schema_string = '_'*self.word_length


          
          results = {}
          if not already_chosen:
               already_chosen = []
          if over_list and len(over_list)==1:
               getting_entropy = True
          elif over_list:
               getting_entropy = False
          else:
               over_list = all_words
               getting_entropy = False          

          counter = 0
          for answer_word in over_list:
               if counter%50 ==0 and len(all_words)>1000:
                    print(counter, answer_word, end=' ')
               counter += 1
               
               
               results[answer_word] = {}
               temp_histo_dict = {}
               for try_word in all_words:
                    solved, schema = self.compare_word (try_word, answer_word)
                    schema = self.show(try_word,schema)
                    
                    if schema in temp_histo_dict:
                         temp_histo_dict[schema] += 1
                    else:
                         temp_histo_dict[schema] = 1
                    
               total_size = len(all_words)


##               total = sum([x for x in temp_histo_dict.values()])
##               average = total/len(temp_histo_dict)
##               deviation = (sum([abs(average-temp_histo_dict[x]) for x in temp_histo_dict]))/len(temp_histo_dict)
##               
####
####           
##               
               entropy =  sum([(x/total_size)*math.log2(x/total_size) for x in temp_histo_dict.values()])
               

               results[answer_word]=entropy
##               results[answer_word] = deviation
               
          if len(all_words)>1000:
               print()
          

               

          if getting_entropy:
               return over_list[0], results[over_list[0]]
          ordered_results = sorted([x for x in results.keys() if x not in already_chosen and x in choice_words],key = lambda x:results[x])


          return ordered_results 

          


     def compare_word (self, word_a, word_b):

          """Compares one A to another B and returns a boolean value (True if they are identical) and
          a schema in the form of a tuple indicating the match between the two words:
               (1) list of positions in A that match perfectly.
               (2) list of positions in A where the letter is found in B
               (3) list of positions in A that don't match at all.

               For example: word A=cat, word b=tab
               Returns False, ([1],[2],[0])
          """
               

          matches, perfect, almost, not_at_all = False, [],[],[]
          word_a = list(word_a)
          word_b = list(word_b)
          if word_a == word_b:
               matches = True
               perfect = list(range(len(word_a)))
               
         
          
          else:
               
               for position in range(len(word_a)):
                    if word_a[position] == word_b[position]:
                         perfect.append(position)
                         word_a[position] = ' '
                         word_b[position] = ' '

               for position in range(len(word_a)):
                    if word_a[position] in word_b and not word_a[position]==' ':
                         word_b = list(''.join(word_b).replace(word_a[position],' '))
                         word_a[position] = ' '
                         almost.append(position)

               for position in range(len(word_a)):
                    if word_a[position] != ' ':
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
     
               

     def get_possible_words (self, word,
                             all_words,
                             schema,
                             length_only=False,
                             bypass_perfect=False,
                             bypass_almost=False,
                             bypass_not_at_all=False,
                             test_words=False):

          """Returns all the words from the list that match the schema"""

          def fits_perfectly (letter, position, word):

               """True if letter is in the word at the given position"""


               if position < len (word) and word[position] == letter:
                    return True
               return False

          def fits_almost (letter, position, word):

               """True if letter is in the word, but not in the given position"""

               if letter in word and not word[position] == letter:
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

          def is_other_word (word_a,word_b, schema):
               word_a = list(word_a)
               word_b = list(word_b)
               found_letters = []

               for position in schema[0]:

                    if word_a[position] != word_b[position]:

                         return False
                    else:
                         word_b[position] == ' '
                         found_letters.append(word_a[position])


               for position in schema[1]:
                    if word_a[position] in word_b and not word_a[position]==word_b[position]:
                         word_b[word_b.index(word_a[position])] == ' '
                         found_letters.append(word_a[position])
                    else:

                         return False
        
                    
               for position in schema[2]:
                    if word_a[position] in word_b and word_a[position] not in found_letters:
                         return False
                    elif word_a[position] in found_letters:
                         found_letters.pop(found_letters.index(word_a[position]))
                    
               return True 
          def is_test_word (word_a,word_b, schema):


               
               for position in schema[0]:

                    if not word_a[position] == word_b[position]:
                         return False
               temp_word_b = list(word_b)
               for position in schema[0]:
                    temp_word_b[position] = ' '
               
               
                    
               for position in schema[1]:
                    if word_a[position] not in temp_word_b:
                         return False
                    else:
                         for position in range(len(word_a)):
                              if temp_word_b[position]==word_a[position]:
                                   temp_word_b[position] = ' '
                                   break
                    
                    
               return True 
          if length_only:

               counter = 0

               if test_words and is_test_word(word, to_check, schema):

                    counter += 1


               if not test_words and  is_other_word(word, to_check, schema):

                         counter += 1
               return counter 
               

          return_list = []
          for to_check in all_words:


               if test_words and is_test_word(word, to_check, schema):

                    return_list.append(to_check)
                    
               elif not test_words and  is_other_word(word, to_check, schema):

                    return_list.append(to_check)

               
          return return_list

     def show (self, word, schema,information=False):

          """Returns a string display the result of a comparison"""

          if information:
               return schema[0:2]
          
          result = ''

          for position in range(len(word)):
               if position in schema[0]:
                    result+=word[position].upper()
               elif position in schema[1]:
                    result+=word[position]
               else:
                    result += '_'
          return result
     
               

     def solve (self,to_solve='',mode=1,script=None,printing=True,play_mode = False, hard=None, header='',show_definition=True,rank_position=0,first_word='',cut_off=300, fetch=False):

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
                                   

          

               

        
          if printing:
               print('\n'+header)
          already_chosen = set()
          testing_words = list(self.words)
          remaining_words = list(self.words)
               
          

          counter = 1
          outcomes = []
          exact = set()
          almost = set()
          not_at_all = set()
          last_schema_string = '_'*self.word_length
          already_chosen = [] #This is necessary to keep get_word_by_information ending up in an infinite loop



          def with_play_mode (all_words=None):

               """For where the user plays the wordl game"""
               

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
                              if not self.hinted:
                                   if '(' in self.dictionary[to_solve] and ')' in self.dictionary[to_solve]:
                                        print(self.dictionary[to_solve].split('(')[1].split(')')[0])
                                   else:
                                        print('No specification')
                                   self.hinted = True
                              elif self.hinted:
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


          def solve_mode (testing_words=None,remaining_words=None,script='r',schema_string=None,already_chosen=None,rank_position=None, count=None, return_all=False):

               """For solving by applying automatic strategies"""

               extract = lambda x,y,z: x.split(y)[1].split(z)[0].strip()
               outside =lambda x,y,z: x.split(y)[0]+x.split(z)[1]


               def solve_phrase (testing_words=None,
                                 remaining_words=None,
                                 phrase='r',
                                 schema_string=None,
                                 already_chosen=None,
                                 rank_position=None,
                                 count=None,
                                 printing=True,
                                 return_all=False):

                    """Interprets the phrase expressing the solving method"""



                    if ('i' in phrase  or 'f' in phrase) and 'e' in phrase:

                         testing_words = list(self.words)
                              
                    
                    if counter == 1:
                         if not 'i' in phrase:
                         
                              main_histo = self.histogram
                              letter_histo = self.letter_histogram

                             
                         else:
                              print()
                              
                    else:
                         if not 'i' in phrase:
                              main_histo = {}
                              letter_histo = {}

                              if printing:
                                   print('   MAKING NEW HISTOGRAM FOR ',len(remaining_words),' WORDS')
                              main_histo = self.make_histogram(word_list=remaining_words,histo_object=main_histo)
                              letter_histo = self.make_letter_histogram(word_list=remaining_words,histo_object=letter_histo)
                         else:
                              print()


                    if '$' in phrase:
                         testing_words = [x for x in testing_words if x in self.choose_words]

                    
                    
                    if '{' in phrase and '}' in phrase and count==1:
                         
                         try_this = extract(phrase,'{','}')
                         return try_this
                         
                         
                    if '[' in phrase and ']' in phrase:
                         divider = int(extract(phrase,'[',']'))
                         phrase = outside(phrase,'[',']')
                         add_to = 1 
                    else:
                         divider = 1
                         add_to = 0

                    if '<' in phrase and '>' in phrase:
                         rank_position = float(extract(phrase,'<','>'))
                         phrase = outside(phrase,'<','>')
                         if not 0<=rank_position<1:
                              rank_position = 0

                    if not rank_position:
                         rank_position = 0
                         
                         



                    #To determine function
                    if 'i' not in phrase:
                         if '**' in phrase:
                              value_function=  self.value_word_by_char
                              histo_tuple = (letter_histo,)
                              
                         
                         elif '*' in phrase:
                              
                              value_function = self.value_word
                              histo_tuple = (main_histo,)
                         else:
                              value_function = self.compound_values
                              histo_tuple = (main_histo, letter_histo)

                    if '$' in phrase and self.choose_words:
                         limit_to = self.choose_words
                    else:
                         limit_to = self.words 

                    #TO GET THE SET OF WORDS 
                         

                    

                    if 'f' in phrase:
                         testing_words = [x for x in sorted(testing_words,key=lambda x:-1*(value_function(x,histo_tuple=histo_tuple))) if x in limit_to]

                              
                         

                    elif 'i' in phrase:
                         choice_words = None
                         if not self.choose_words:
                              choice_words = testing_words

                         else:
                              choice_words = [x for x in testing_words if x in self.choose_words]
                              
                         
                         if '$' in phrase and self.choose_words:
                              testing_words = self.get_best_word_by_information(all_words=testing_words,
                                                                           choice_words=choice_words,
                                                                           over_list=remaining_words,
                                                                           schema_string=last_schema_string,
                                                                           already_chosen=already_chosen)
                         else:
                              
                             testing_words = self.get_best_word_by_information(all_words=testing_words,
                                                                           choice_words=choice_words,
                                                                           over_list=remaining_words,
                                                                           schema_string=last_schema_string,
                                                                           already_chosen=already_chosen)

                    if '~' in phrase:
                         testing_words = list(reversed(testing_words))
                         
                    
                         
                    if 's' in phrase:
                         
                         top_value = value_function(testing_words[0],histo_tuple=histo_tuple)
                         pos = 0
                         for pos, w in enumerate(testing_words):
                              if (('$' not in phrase and value_function(w,histo_tuple=histo_tuple) < top_value)
                                  or ('$' in phrase and self.choose_words and value_function(w,histo_tuple=histo_tuple) > top_value)):
                                   break
                         testing_words = testing_words[0:pos]
                         

                    if 'r' in phrase:
                         up_to_here = int(len(testing_words)/divider)+add_to
                         if up_to_here == 0:
                              up_to_here = 1
                         if up_to_here > len(testing_words):
                              up_to_here = len(testing_words)
                              
                         try_this = random.choice(testing_words[0:up_to_here])
                    elif 'p' in phrase: #F for by percentage
                         try_this = testing_words[int(len(testing_words)*rank_position)]
                    else:
                         try_this = testing_words[0]

                    if not return_all:
                         return try_this
                    return testing_words
     
                         
                                                   
                    #END OF SOLVE_PHRASE FUNCTION    
                    
              
                         

               if ';' not in script:
                    
                    y =solve_phrase(remaining_words=remaining_words,
                                    testing_words=testing_words,
                                    phrase=script,
                                    schema_string=last_schema_string,
                                    already_chosen=already_chosen,
                                    rank_position=rank_position,
                                    count=count,
                                    printing=printing,
                                    return_all=return_all)
                    return y,script
               
                    
               elif not script:
                    return solve_phrase(remaining_words=remaining_words,
                                        testing_words=testing_words,
                                        phrase='r',
                                        schema_string=last_schema_string,
                                        already_chosen=already_chosen,
                                        rank_position=rank_position,
                                        count=count,
                                        printing=printing,
                                        return_all=return_all),script
               else:

                    while (';' in script
                      and '.' in script.split(';')[0]
                      and script.split('.')[0].strip().isnumeric()):
                         cut_off = int(script.split('.')[0].strip())
                         if len(remaining_words) < cut_off:
                              script = ';'.join(script.split(';'))[1:]
                         else:
                           break
                         
                    phrase = script.split(';')[0]
                    script = ';'.join(script.split(';')[1:])
                    return solve_phrase(remaining_words=remaining_words,
                                        testing_words=testing_words,
                                        phrase=phrase,
                                        schema_string=last_schema_string,
                                        already_chosen=already_chosen,
                                        rank_position=rank_position,
                                        count=count,
                                        printing=printing),script

          if fetch:
                    return solve_mode(remaining_words=remaining_words,
                                      testing_words=testing_words,
                                      script = script,
                                      schema_string=None,
                                      already_chosen=None,
                                      rank_position=None,
                                      return_all=True)
                    
          if script is None:

               if mode in self.scripts:

                    script = self.scripts[mode]
               else:
                    script = 'r'
               print('SCRIPT = ',script)

          while True:

               try_this = None
               self.hinted = False 

              
               if play_mode:
                    
                    try_this = with_play_mode(all_words=remaining_words)
       
               else:

                    try_this, script = solve_mode(remaining_words=remaining_words,
                                                  testing_words=testing_words,
                                                  script = script,
                                                  schema_string=last_schema_string,
                                                  already_chosen=already_chosen,
                                                  rank_position=rank_position,
                                                  count=counter)



                    
                    

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
               
                         print(x, end='')
                    else:
                         outcomes.append(x)
                         print('\n'.join(outcomes))
                               
               
##               if printing:
##                    print(self.show(try_this, schema))

               
               
               remaining_words, testing_words = (self.get_possible_words (try_this,remaining_words, schema,test_words = False),
                                             self.get_possible_words (try_this,testing_words, schema,test_words = True))
               

               

               


               
               if try_this in remaining_words:
                    remaining_words.pop(remaining_words.index(try_this))
               if try_this in testing_words:
                    testing_words.pop(testing_words.index(try_this))

               if self.show_length and len(remaining_words)>0:
                    print('THERE ARE ',len(remaining_words),' REMAINING WORDS')
               if self.show_words and 0<len(remaining_words)<100:
                    print(', '.join(remaining_words))    
               if solved:
                    to_solve = to_solve.lower()
                    definition = ''
                    if show_definition and (override or mode == max(self.scripts.keys())) and to_solve in self.dictionary:
                         definition = self.dictionary[to_solve]
                         print()
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
                     
   
               


     def compare_methods (self,iterations=100,iterate_over=None,limited_to=[0,1,2,3,4,5,6]):

          

          """Compares the results of the different methods for the given number of iterations"""

          results = {}
          result_list = []
          result_histogram = {}
          for m in self.scripts:
               results[m]=0
               result_histogram[m] = {}
          if iterate_over:
               iterations = len(iterate_over)
               


          for iteration in range(1,iterations+1):

               if not iterate_over:
                    answer = self.get_answer()
               else:
                    answer = iterate_over[iteration-1]
                    
               
               result_list = []
               for mode in self.scripts:
                    if mode in limited_to:
                         print('ANSWER = ',answer,' MODE = ',mode)
                         

                         how_many_tries = self.solve(answer,mode,printing=(iterations<100),show_definition=False)
                         results[mode] += how_many_tries
                         if how_many_tries not in result_histogram[mode]:
                              result_histogram[mode][how_many_tries] = 1
                         else:
                              result_histogram[mode][how_many_tries] += 1
                         result_list.append(str(how_many_tries))
               print('ITERATION = ',iteration,' / ',answer,' :: ',', '.join(result_list))

          for mode in self.scripts:
               if mode in limited_to:

                    results[mode] = results[mode]/iteration

                    to_print = ' '+str(mode)+'/'+self.scripts[mode]+' = '+str(results[mode])
                    print('\n'+to_print)
                    result_list.append(str(datetime.datetime.now())+':'+'<'+self.language+'/'+self.filename+'>'+': '+to_print+'\n')
                    
                    histo_print ='HISTOGRAM ' + '<' +str(mode)+'> '+ ', '.join([str(x)+'='+str(result_histogram[mode][x]) for x in sorted(result_histogram[mode])])
                    print(histo_print)
                    result_list.append(histo_print)
                    
          return result_list
     
                    

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

               result = results[word]/iterations
               print(' = ',result)
               results[word]  = result
               
          for word in sorted(results.keys(),key = lambda x:results[x]):
               print(results[word],' / ',word+' ('+str(self.value_word(word))+'/'+str(self.value_word_by_char(word))+')')
               
               
     def log_lines (self,filename='log.txt',lines=None):

          """Adds a lines to the end of the log file"""

          self.make_new_directory('logs')
          logfile = open('logs'+os.altsep+filename,'at', encoding='utf-8')
          for line in lines:
               logfile.writelines(line)
          logfile.close()
          

               
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
          self.show_words = False
          self.show_length = False
          
          while True:
               
               word_length = input('ENTER WORD LENGTH OR A(analyse)! ')
               if not word_length:
                    word_length = 5
                    break
               elif word_length.isnumeric():
                    word_length = int(word_length)
                    break
               elif word_length.lower() == 'a':
                    temp_histo = {}
                    
                    for line in self.textfile.split('\n'):
                         line = len(line.split('\t')[0])
                         if line not in temp_histo:
                              temp_histo[line] = 1
                         else:
                              temp_histo[line] += 1
                    histo_print ='HISTOGRAM ' + ', '.join([str(x)+'='+str(temp_histo[x]) for x in sorted(temp_histo)])
                    print(histo_print)
                    
                    
                    
          
          self.constitute(word_length)
          
          


          while True:

               answer  = input('\n\nENTER A '+str(word_length)
                               +' letter word, <ENTER> to choose a random word, (C)ompare, (E)dit modes, set(F)unction, R(ank compare) \n'+
                               'or (P)lay, or (H)ard play, (L)og, (S)ave last, \nSho(W) Words, Show Si(Z)e, (T)est a single word, (O)ptimize cutoff,\n'+
                               '  (A)pply schema, or (Q)uit, (G)et entropy, or (D)ISPLAY ALL WORDS  ').lower()

               if answer in ['z']:
                    self.show_length = not self.show_length
                    print('SHOWING LENGTH '+{False:'OFF',True:'ON'}[self.show_length])
               
               if answer in ['w']:
                    self.show_words = not self.show_words
                    print('SHOWING WORDS '+{False:'OFF',True:'ON'}[self.show_words])
               if answer in ['c','r']:
 
                    while True:
                         iterations = input('How many iterations or RETURN to use entire wordset? ')
                         if iterations.isnumeric() or (answer=='c' and not iterations):
                              break
                    if not iterations:
                         iterations = None
                         if self.choose_words:
                              iterate_over = self.choose_words
                         else:
                              iterate_over = self.words
                         print('ITERATING OVER ',len(iterate_over),' WORDS!')
                    else:
                         iterate_over = None
                         iterations = int(iterations)
                              
                              
                    
                    if answer == 'c':
                         modes_to_use = [int(x.strip())
                                         for x in input('ENTER MODES to use from '
                                                        +', '.join(sorted([str(x) for x in self.scripts.keys()]))).split(',')
                                         if x.strip().isnumeric() and int(x.strip()) in self.scripts]

                         results = self.compare_methods(iterations=iterations,iterate_over=iterate_over,limited_to=modes_to_use)
                         self.log_lines(filename='tests.txt',lines=results)
                                       
                                       
                    
                    elif answer == 'r' and isinstance(iterations,int):
                         
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
               elif answer == 'g':
                    if self.choose_words:
                         print('CHOICE')
                         print(self.get_best_word_by_information(self.choose_words,over_list=[input('word?')]))
                    else:
                         print(self.get_best_word_by_information(self.words,over_list=[input('word?')]))

               elif answer == '+':

                    def is_other_word (word_a,word_b, schema):
                         word_a = list(word_a)
                         word_b = list(word_b)
                         found_letters = set()

                         for position in schema[0]:

                              if word_a[position] != word_b[position]:

                                   return False
                              else:
                                   word_b[position] == ' '
                                   found_letters.add(word_a[position])


                         for position in schema[1]:
                              if word_a[position] in word_b and not word_a[position]==word_b[position]:
                                   word_b[word_b.index(word_a[position])] == ' '
                                   found_letters.add(word_a[position])
                              else:

                                   return False
                  
                              
                         for position in schema[2]:
                              if word_a[position] in word_b and word_a[position] not in found_letters:
                                   return False
                         return True
                    
                    c_x = 0
                    
                    for word1 in self.words:
                         for word2 in self.words:
                              c_x+=1
                              solve, schema = self.compare_word(word1,word2)
                              
                              satisfies = is_other_word(word1,word2,schema)
                              if not satisfies:
                                   print('A',word1,word2,schema)
                              else:
                                   pass
                              if c_x % 1000 == 0:
                                   print(c_x)
                              
                          
                              
                         
               elif answer == 'd':

                    inp = input('ENTER SCRIPT')
                    up_to = input('UP TO, RETURN for the first WORD, or DASH for ALL?')
                    if up_to == '-':
                         up_to = -1
                    try:
                         up_to = int(up_to)
                    except:
                         up_to = 0


                    if up_to >= 0:
                         print(', '.join([str(x[0])+' : '+x[1] for x in enumerate(self.solve(script=inp,fetch=True)[0][0:up_to])]))
                              
                    else:
                         print(', '.join([str(x[0])+' : '+x[1] for x in enumerate(self.solve(script=inp,fetch=True)[0])]))

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
                    hard_mode = (answer=='h')
                    answer = self.get_answer()
                    self.solve(to_solve=answer,play_mode=True,hard=hard_mode)
             
               elif not answer:
                    answer = self.get_answer()
                    print('ANSWER === ',answer)
                    for m in self.scripts:

                         self.solve(answer,mode=m)
                         
                 
               elif answer in self.words:
                    if len(answer) == word_length:

                         for m in self.scripts:
                              self.solve(answer,mode=m)


               else:
                    print('I KNOW A LOT OF WORDS... but ',answer,'!!!! Really!!!')


if __name__ == "__main__":

     while True:
          wordle = Wordle_Solver()
          saved_results = wordle.run()
          wordle.log_lines(lines=[wordle.language+'\t'+str(wordle.word_length)+'\t'+str(line[0])+'\t'+'<<'+str(line[2])+'>>\n' for line in saved_results])
          
          
               
               
          
          
     
        
