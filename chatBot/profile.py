import itertools
import numpy

class TextProfile:
    
    def __init__(self, text_list):
        self.source_list = text_list
        self.generate_profile()
        
    
    def generate_profile(self):
        new_profile = {}
        new_sentence_init_profile = {}
        
        for sentence in self.source_list:
            sentence_list = sentence.split()
            
            first_word = sentence_list[0].lower()
            if (first_word not in new_sentence_init_profile):
                    new_sentence_init_profile[first_word] = 0
            new_sentence_init_profile[first_word] += 1
            
            for curr_word, next_word in itertools.zip_longest(sentence_list, sentence_list[1:]):
                curr_word = curr_word.lower()
                next_word = next_word.lower()
                
                if (curr_word not in new_profile):
                    new_profile[curr_word] = {}
                
                if (next_word not in new_profile[curr_word]):
                    new_profile[curr_word][next_word] = 0
                
                new_profile[curr_word][next_word] += 1
        
        self.sentence_init_profile = new_sentence_init_profile
        self.profile = new_profile
    
    def generate_sentence(self):
        pass