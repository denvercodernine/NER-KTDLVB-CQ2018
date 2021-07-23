import typing


class tagged_word:
    "Tagged word for NER"

    def __init__(self, word=None, pos_tag=None, phrase_tag=None, ne_tag=None, ne_nested_tag=None) -> None:
        if word != None:
            self.word = word
        else:
            raise Exception("Did not find word.")
        self.pos = pos_tag
        self.phrase = phrase_tag
        self.ne = ne_tag
        self.ne_nested = ne_nested_tag
    
    def regular_word(self):
        temp = self.word.lower()
        return temp


class sentence:
    "Sentence of tagged words"

    def __init__(self) -> None:
        self.words = []
        self._index = 0

    def add_word(self, word):
        self.words.append(word)

    def __str__(self) -> str:
        string = ''
        for w in self.words:
            string = string + w.word + ' '
        string.strip()
        return string

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.words):
            result = self.words[self._index]
            self._index += 1
            return result
        raise StopIteration