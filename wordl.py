import os, random


about = """
          WORDL solver

          by Anthony Curtis Adler
          2022

          
          (For the actual puzzle, see http://foldr.moe/hello-wordl/)

          THE VOCABULARY IS VERY LARGE and STRANGE, and the FIRST CHOICE is not optimized by frequency

             """

print(about)



class Wordl_Solver:


     def __init__ (self,word_length=5):

          self.words = []
          self.word_length = word_length 

          filename = 'words.txt'

          # GET TEXT FILE 
          while True:
               print('GETTING TEXT FILE!')
               try:
                    textfile = open(filename,'r', encoding='utf-8')
                    textfile=textfile.read()
                    print(filename+' OPENED! \n')
                    break
               except:
                    print(textfile+' NOT FOUND\n')
                    print('ENTER NEW WORD FILE!')
                    filename= input('textfile')
          # FIND THE CHARACTER DIVIDING THE WORDS
          for split_char in textfile:
               if split_char not in 'abcdefghijklomnopqrstuvwxyz0123456789':
                    split = split_char
                    break

          
          self.words = [x for x in textfile.split(split_char) if len(x) == word_length and x.lower()==x]

     def get_word (self):

          return random.choice(get_word)

     def compare_word (self, word_a, word_b):

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

          def fits_perfectly (letter, position, word):

               if position < len (word) and word[position] == letter:
                    return True
               return False

          def fits_almost (letter, position, word):

               if letter in word:
                    return True
               return False

          def apply_to_word (word_a, word_b, positions, function):

               for pos in positions:

                    if not function(word_a[pos],pos,word_b):
                         return False
               return True

          return_list = []
          for to_check in all_words:
               if (apply_to_word(word, to_check, schema[0], fits_perfectly) and
                   apply_to_word(word, to_check, schema[1], fits_almost)):

                    return_list.append(to_check)
          return return_list

     def show (self, word, schema):
          result = ''

          for position in range(len(word)):
               if position in schema[0]:
                    result+=word[position].upper()
               elif position in schema[1]:
                    result+=word[position]
               else:
                    result += '_'
          return result
     
               

     def solve (self,to_solve):

          already_chosen = set()
          all_words = list(self.words)

          counter = 1

          while True:

               while True:
                    try_this = random.choice(all_words)
                    if try_this not in already_chosen and not (counter==1 and not self.proper_first_word(try_this)):
                         
                         break
               already_chosen.add(try_this)
               
               print('GUESS #',counter,' = ',try_this)
               
               solved, schema = self.compare_word (try_this, to_solve)
               
               print(self.show(try_this, schema))
               
               all_words = self.get_possible_words (try_this,all_words, schema)


               if solved:
                    break
               counter += 1
               
     def test (self):

          answer = random.choice(self.words)
          print('ANSWER = ',answer)
          
          self.solve(answer)


if __name__ == "__main__":

     try:
          word_length = int(input('ENTER WORD LENGTH!'))
     except:
          word_length = 5
     wordl = Wordl_Solver(word_length)

     while True:

          answer  = input('ENTER A '+str(word_length)+' letter word or RETURN to choose a word at random')

          wordl = Wordl_Solver(word_length)
          if not answer:
               wordl.test()
          elif answer in wordl.words:
               if len(answer) == word_length:
                    wordl.solve(answer)
          else:
               print('I KNOW A LOT OF WORDS... but ',answer,'!!!! Really!!!')
               
                    
               
               

               

               

               
                    

          
                         
                    
          
          
                          

               
          
          


     
                
                



          
          


          
               
          
          





          
          


