import itertools
import numpy as np


class TextProfile:
    
    def __init__(self, text_list):
        self.source_list = text_list
        self.generate_profile()
        
    
    def generate_profile(self):
        new_profile = {}
        new_sentence_init_profile = {}
        
        for sentence in self.source_list:
            sentence_list = sentence.split()
            
            if len(sentence_list) < 1:
                continue
                
            first_word = sentence_list[0]
            if (first_word not in new_sentence_init_profile):
                    new_sentence_init_profile[first_word] = 0
            new_sentence_init_profile[first_word] += 1
            
            for curr_word, next_word in itertools.zip_longest(sentence_list, sentence_list[1:]):
                curr_word = self.make_lower(curr_word)
                next_word = self.make_lower(next_word)
                
                if (curr_word not in new_profile):
                    new_profile[curr_word] = {}
                
                if (next_word not in new_profile[curr_word]):
                    new_profile[curr_word][next_word] = 0
                
                new_profile[curr_word][next_word] += 1
        
        self.sentence_init_profile = new_sentence_init_profile
        self.profile = new_profile
    
    def generate_sentence(self):
        new_sentence = []
        
        curr_word = self.choose_word(self.sentence_init_profile)
        
        while curr_word is not None:
            new_sentence.append(curr_word)
            curr_word = self.choose_word(self.profile[self.make_lower(curr_word)])
            
        return (' '.join (word for word in new_sentence))
    
    def choose_word(self, word_dict):
        words = list(word_dict.keys())
        weights = list(word_dict.values())
        
        total = np.sum(weights)
        weights[:] = [x / total for x in weights]
        
        return np.random.choice(words, p=weights)
        
        
    def make_lower(self, text):
        if ((text is not None) and ("http" not in text)):
            return text.lower()
        else:
            return text
        
        
        
        
        
        
        