import itertools
import ngram_cloud.orm as orm
import ngram_cloud.graph as graph


class VocabWord:
    def __init__(self, word, occurrences, id):
        self.word = word
        self.occurrences = occurrences
        self.id = id

    def __str__(self):
        return f'{self.word} {self.id}'


class NgramCloudException(Exception):
    pass


class VocabController(orm.DataController):
    def _all(self):
        return [VocabWord(v.word, v.hits, v.id)
                for v in self.db.list_vocab()]

    def all(self):
        return vocab

    def find(self, word):
        vocab_word = self.db.find_word_vocab(word)
        if not vocab_word:
            raise NgramCloudException(
                f'`{word}` does not exist in Vocabulary')
        return VocabWord(vocab_word.word,
                         vocab_word.hits,
                         vocab_word.id)

    @staticmethod
    def from_id(id):
        for vocab_word in vocab:
            if vocab_word.id == id:
                return vocab_word
        else:
            NgramCloudException(
                f'No word with id `{id}` found in Vocabulary')


class Association:
    def __init__(self, word1, word2, occurrences, rate, solved):
        self.word1 = word1
        self.word2 = word2
        self.occurrences = occurrences
        self.rate = rate
        self.solved = solved

    def __str__(self):
        return f'Association: ' \
               f'word1: {self.word1} ' \
               f'word2: {self.word2} ' \
               f'occurences: {self.occurrences}'


class CloudController(orm.DataController):
    def cloud(self, word, rate, solved):

        with VocabController() as vc:
            vocab_word = vc.find(word)

        associations = set(self.list(
            word_id=vocab_word.id,
            rate=rate,
            solved=solved
        ))

        neighbors_ids = set(itertools.chain.from_iterable(
            [[a.word1.id, a.word2.id] for a in associations]
        ))

        if vocab_word.id in neighbors_ids:
            neighbors_ids.remove(vocab_word.id)

        for neighbor_id in neighbors_ids:
            for a in set(self.list(neighbor_id, rate=rate, solved=solved)):
                associations.add(a)

        return graph.Graph.from_associations(associations)

    def list(self, word_id, limit=5, solved=1, rate=10):
        return [
            Association(
                word1=VocabController.from_id(a.word1_id),
                word2=VocabController.from_id(a.word2_id),
                occurrences=a.hits,
                rate=a.rate,
                solved=a.solved
            )
            for a in self.db.list_associations(
                word_id=word_id,
                limit=limit,
                solved=solved,
                rate=rate
            )
        ]


with VocabController() as vc:
    vocab = vc._all()
