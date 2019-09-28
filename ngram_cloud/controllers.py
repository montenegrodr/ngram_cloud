import ngram_cloud.orm as orm


class VocabWord:
    def __init__(self, word, occurrences):
        self.word = word
        self.occurrences = occurrences


class VocabController(orm.DataController):
    def list(self):
        return [VocabWord(v.word, v.hits)
                for v in self.db.list_vocab()]