import os
import imp

# FIXME:
enc = imp.load_source ('encodings',
                       os.path.join (os.path.dirname (os.path.abspath (__file__)),
                                     'encodings.py'))

class SyllableIter ():
    """
    Return an iterator of clusters, in given encoding.
    """
    def __init__ (self, text, encoding):
        if not isinstance(encoding, enc.BaseEncoding):
            raise TypeError ("is not a valid encoding.")

        self.text = text
        self.pattern  = encoding.get_compiled_pattern ()
        self.start = 0

    def __iter__ (self):
        return self

    def __next__ (self):
        match = self.pattern.search (self.text, self.start)
        if not match:
            raise StopIteration

        if match.start () == self.start:
            # no unmatched text
            self.start = match.end ()
            ret = { k: v for k , v in match.groupdict().items() if v }
        else:
            # if there is unmatched text,
            ret = {'syllable': self.text[self.start:match.start()]}
            self.start = match.start ()
        return ret
