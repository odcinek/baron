import string


class FlexibleIterator():
    def __init__(self, sequence):
        self.sequence = sequence
        self.position = -1

    def __iter__(self):
        return self

    def next(self):
        self.position += 1
        if self.position == len(self.sequence):
            raise StopIteration
        return self.sequence[self.position]

    def next_starts_with(self, sentence):
        size_of_choice = len(sentence)
        return self.sequence[self.position + 1: self.position + 1 + size_of_choice] == sentence

    def next_in(self, choice):
        if self.position + 1 == len(self.sequence):
            return False
        return self.sequence[self.position + 1] in choice

    def show_next(self):
        if self.position + 1 == len(self.sequence):
            return None
        return self.sequence[self.position + 1]

    def rest_of_the_sequence(self):
        return self.sequence[self.position + 1:]

    def end(self):
        return self.position == (len(self.sequence) - 1)

    def grab(self, test):
        to_return = ""
        current = None
        escaped = False
        while self.show_next() is not None and (escaped or test(self)):
            if escaped:
                escaped = False
            elif current == "\\":
                escaped == True
            current = self.next()
            to_return += current

        return to_return


def split(sequence):
    return list(split_generator(sequence))


def split_generator(sequence):
    iterator = iter(FlexibleIterator(sequence))
    while True:
        if iterator.end():
            return

        not_found = True

        if iterator.next_in("#"):
            not_found = False
            yield iterator.grab(lambda iterator: iterator.show_next() not in "\r\n")

        for section in ("'", '"'):
            not_found = False
            if iterator.next_starts_with(section*3):
                result = iterator.next()
                result += iterator.next()
                result += iterator.next()
                result += iterator.grab(lambda iterator: not iterator.next_starts_with(section*3))
                result += iterator.next()
                result += iterator.next()
                result += iterator.next()
                yield result
            elif iterator.next_in(section):
                result = iterator.next()
                result += iterator.grab(lambda iterator: iterator.show_next() not in section)
                result += iterator.next()
                yield result

        for section in (string.ascii_letters + "_" + "1234567890", " ", "\t"):
            if iterator.next_in(section):
                not_found = False
                yield iterator.grab(lambda iterator: iterator.show_next() in section)

        for one in "@,.;()=*:+-/^%&<>|\r\n~[]{}!``\\":
            if iterator.next_in(one):
                not_found = False
                yield iterator.next()

        if not_found:
            raise Exception("Untreaded elements: %s" % iterator.rest_of_the_sequence().__repr__()[:50])