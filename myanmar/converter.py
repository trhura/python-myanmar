#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""routines for conversion between unicode and Myanmar legacy encodings.
To get supported encodings –
>>> print myanmar.converter.get_available_encodings ()
>>> myanmar.converter.convert (u'
"""
_converters = {}


class _TlsMyanmarConverter():
    """
    Private class which convert unicode to/from legacy encoding.
    """

    def __init__(self, data):

        self.data = data
        self.useZwsp = False
        self.sourceEncoding = self.data['fonts'][0]
        self.unicodeSequence = [
            "kinzi", None, "lig", None, "cons", "stack", "asat", "yapin",
            "yayit", "wasway", "hatoh", "eVowel", "uVowel", "lVowel",
            "anusvara", "aVowel", "lDot", "asat", "lDot", "visarga"
        ]
        self.legacySequence = [
            "eVowel", "yayit", None, "lig", None, "cons", "stack", "kinzi",
            "uVowel", "anusvara", "asat", "stack", "yapin", "wasway", "hatoh",
            "wasway", "yapin", "kinzi", "uVowel", "lDot", "lVowel", "lDot",
            "anusvara", "uVowel", "lVowel", "aVowel", "stack", "lDot",
            "visarga", "asat", "lDot", "visarga", "lDot"
        ]
        self.minCodePoint = None
        self.reverse = {}
        self.unicodePattern = self.buildRegExp(self.unicodeSequence, True)
        self.legacyPattern = self.buildRegExp(self.legacySequence, False)
        self.fontFamily = ""
        i = 0
        for font in self.data['fonts']:
            if (i > 0):
                self.fontFamily += ","
            self.fontFamily += "'" + font + "'"
            i = i + 1

    def buildRegExp(self, sequence, isUnicode):
        import re
        pattern = ""
        escapeRe = re.compile(r"([\^\$\\\.\*\+\?\(\)\[\]\{\}\|])", re.UNICODE)
        if not self.reverse:
            self.reverse = {}

        if self.minCodePoint is None:
            self.minCodePoint = ord(self.data["cons"]["\u1000"][0])
            self.maxCodePoint = self.minCodePoint

        for i in range(0, len(sequence)):
            alternates = []
            if sequence[i] is None:
                continue
            if not sequence[i] in self.reverse:
                self.reverse[sequence[i]] = {}  # new Object()
                # print self.maxCodePoint, self.minCodePoint
            for j in self.data[sequence[i]]:
                # print 'j =  ', j.encode ('utf-8')
                if self.data[sequence[i]
                             ][j] and len(self.data[sequence[i]][j]) > 0:
                    for k in range(0, len(self.data[sequence[i]][j])):
                        codePoint = ord(self.data[sequence[i]][j][k])
                        if codePoint != 0x20:
                            if (codePoint > self.maxCodePoint):
                                self.maxCodePoint = codePoint
                            if (codePoint < self.minCodePoint):
                                self.minCodePoint = codePoint
                # print self.data[sequence[i]][j].encode ('utf-8')
                if (isUnicode):
                    # items with an underscore suffix are not put into the regexp
                    # but they are used to build the legacy to unicode map
                    underscore = j.find('_')
                    if (underscore == -1):
                        self.reverse[sequence[i]][self.data[sequence[i]][j]
                                                  ] = j
                        # FIXME:
                        # print 'j =  ', j.encode ('utf-8') , ' escapes= ', escapeRe.sub (ur"\1", j).encode ('utf-8')
                        alternates += [escapeRe.sub(r"\1", j)]
                    else:
                        self.reverse[sequence[i]][self.data[sequence[i]][j]
                                                  ] = j[0:underscore]
                else:
                    # FIXME
                    # print self.data[sequence[i]][j].encode ('utf-8')
                    # print 'j =  ', j.encode ('utf-8') , ' escapes= ', escapeRe.sub (ur"\1", j).encode ('utf-8')
                    escapedAlternate = escapeRe.sub(
                        r"\1", self.data[sequence[i]][j]
                    )
                    if escapedAlternate:
                        alternates += [escapedAlternate]

            alternates.sort(key=lambda a: len(a))
            if (sequence[i] == "cons"):
                pattern += "("
            elif (sequence[i] == "lig"):
                pattern += "("
            pattern += "("
            subPattern = ""

            # print "alternates .... = ", alternates
            if alternates is not None:
                first = True
                for k in alternates:
                    if first:
                        subPattern = subPattern + re.escape(k)
                        first = False
                    else:
                        subPattern = subPattern + "|" + re.escape(k)
            if sequence[i] == "stack":
                self.legacyStackPattern = re.compile(subPattern, re.UNICODE)
            if (sequence[i] == "kinzi"):
                self.legacyKinziPattern = re.compile(subPattern, re.UNICODE)
            if (sequence[i] == "lig"):
                self.legacyLigPattern = re.compile(subPattern, re.UNICODE)

            pattern += subPattern + ")"

            if (sequence[i] == "cons"):
                pass
            elif (sequence[i] == "lig"):
                pattern += "|"
            elif (sequence[i] == "stack" and sequence[i - 1] == "cons"):
                pattern += "?))"
            elif (
                sequence[i] == "wasway" or sequence[i] == "hatoh"
                or sequence[i] == "uVowel" or sequence[i] == "lVowel"
                or sequence[i] == "aVowel" or sequence[i] == "lDot"
                or sequence[i] == "visarga"
            ):
                if (isUnicode):
                    pattern += "?"
                else:
                    pattern += "*"  # these are frequently multi-typed
            else:
                pattern += "?"

        # if isUnicode:
        # print pattern
        return re.compile(pattern, re.UNICODE)

    def sortLongestFirst(self, a, b):
        # print a.encode ('utf-8'), b.encode ('utf-8')
        if len(a) > len(b):
            return -1
        elif len(a) < len(b):
            return 1
        elif (a < b):
            return -1
        elif (a > b):
            return 1
        return 0

    def convertToUnicodeSyllables(self, inputText):
        outputText = ""
        syllables = []
        pos = 0
        prevSyllable = None
        for match in self.legacyPattern.finditer(inputText):
            if (match.start() != pos):
                prevSyllable = None
                nonMatched = inputText[pos:match.start()]
                outputText += nonMatched
                syllables += nonMatched
            prevSyllable = self.toUnicodeMapper(
                inputText, match.group(), prevSyllable
            )
            syllables += prevSyllable
            outputText += prevSyllable
            pos = match.end()

        if (pos < len(inputText)):
            nonMatched = inputText[pos:len(inputText)]
            # print type(nonMatched), type(outputText)
            outputText += nonMatched
            syllables += nonMatched

        ret = {}
        ret['outputText'] = outputText
        ret['syllables'] = syllables
        return ret

    def toUnicodeMapper(self, inputText, matchData, prevSyllable):
        syllable = {}

        for match in matchData:
            for component in self.legacySequence:
                if component is None:
                    continue

                if match in self.reverse[component]:
                    syllable[component] = self.reverse[component][match]
                else:
                    continue

                # check a few sequences putting ligature components in right place
                if (len(syllable[component]) > 1):
                    if (component == "yapin"):
                        if (syllable[component][1] == "ွ"):
                            syllable["wasway"] = "ွ"
                            if (len(syllable[component]) > 2):
                                if (syllable[component][2] == "ှ"):
                                    syllable["hatoh"] = "ှ"
                                # else:
                                # self.debug.print("Unhandled yapin ligature: " + syllable[component])
                                syllable[component] = syllable[component][0:1]
                        elif (
                            syllable[component][1] == "ှ"
                            or len(syllable[component]) > 2
                        ):
                            syllable["hatoh"] = "ှ"
                            syllable[component] = syllable[component][0:1]
                    elif (component == "yayit"):
                        if (syllable[component][1] == "ွ"):
                            syllable["wasway"] = "ွ"
                        elif (syllable[component][1] == "ု"):
                            syllable["lVowel"] = "ု"
                        elif (
                            syllable[component][1] == "ိ"
                            and len(syllable[component]) > 2
                            and syllable[component][2] == "ု"
                        ):
                            syllable["uVowel"] = "ိ"
                            syllable["lVowel"] = "ု"

                        # else:
                        # self.debug.print("unhandled yayit ligature: " + syllable[component])
                        syllable[component] = syllable[component][0:1]
                    elif (component == "wasway"):
                        syllable["hatoh"] = syllable[component][1:2]
                        syllable[component] = syllable[component][0:1]
                    elif (component == "hatoh"):
                        syllable["lVowel"] = syllable[component][1:2]
                        syllable[component] = syllable[component][0:1]
                    elif (component == "uVowel"):
                        syllable["anusvara"] = syllable[component][1:2]
                        syllable[component] = syllable[component][0:1]
                    elif (component == "aVowel"):
                        syllable["asat"] = syllable[component][1:2]
                        syllable[component] = syllable[component][0:1]
                    elif (component == "kinzi"):
                        # kinzi is length 3 to start with
                        if (
                            (
                                len(syllable[component]) > 3
                                and syllable[component][3] == "ံ"
                            ) or (
                                len(syllable[component]) > 4
                                and syllable[component][4] == "ံ"
                            )
                        ):
                            syllable["anusvara"] = "ံ"
                        if (
                            len(syllable[component]) > 3 and (
                                syllable[component][3] == "ိ"
                                or syllable[component][3] == "ီ"
                            )
                        ):
                            syllable["uVowel"] = syllable[component][3]
                        syllable[component] = syllable[component][0:3]
                    elif (component == "cons"):
                        if (syllable[component][1] == "ာ"):
                            syllable["aVowel"] = syllable[component][1]
                            syllable[component] = syllable[component][0:1]
                    elif (component == "stack" or component == "lig"):
                        # should be safe to ignore, since the relative order is correct
                        pass
                    # else:
                    #   self.debug.print("unhandled ligature: " + component + " " + syllable[component])

        # now some post processing
        if "asat" in syllable:
            if (
                "eVowel" not in syllable and (
                    "yayit" in syllable or "yapin" in syllable
                    or "wasway" in syllable or "lVowel" in syllable
                )
            ):
                syllable["contraction"] = syllable["asat"]
                del syllable["asat"]
            if ("cons" in syllable and syllable["cons"] == "ဥ"):
                syllable["cons"] = "ဉ"

        if (
            "cons" in syllable and syllable["cons"] == "ဥ"
            and "uVowel" in syllable
        ):
            syllable["cons"] = "ဦ"
            if "uVowel" in syllable:
                del syllable["uVowel"]

        elif (
            "cons" in syllable and syllable["cons"] == "စ"
            and "yapin" in syllable
        ):
            syllable["cons"] = "ဈ"
            if "yapin" in syllable:
                del syllable["yapin"]

        elif (
            "cons" in syllable and syllable["cons"] == "သ"
            and "yayit" in syllable
        ):
            if (
                "eVowel" in syllable and "aVowel" in syllable
                and "asat" in syllable
            ):
                syllable["cons"] = "ဪ"
                if "yayit" in syllable:
                    del syllable["yayit"]
                if "eVowel" in syllable:
                    del syllable["eVowel"]
                if "aVowel" in syllable:
                    del syllable["aVowel"]
                if "asat" in syllable:
                    del syllable["asat"]
            else:
                syllable["cons"] = "ဩ"
                if "yayit" in syllable:
                    del syllable["yayit"]

        elif ("cons" in syllable and syllable["cons"] == "၀"):
            index = matchData.find('၀')

            def is_mynum(c):
                return (c >= '၁' and c <= '၉')

            if (index - 1 > 0 and not is_mynum(matchData[index - 1])):
                syllable["cons"] == 'ဝ'
            if (
                index + 1 < len(matchData)
                and not is_mynum(matchData[index + 1])
            ):
                syllable["cons"] = 'ဝ'

        elif (
            "cons" in syllable and syllable["cons"] == "၄"
            and matchData.find('င်း') != matchData.find('၄') + 1
        ):
            syllable["cons"] = '၎'

        elif (
            "cons" in syllable and syllable["cons"] == '၇' and (
                "eVowel" in syllable or "uVowel" in syllable
                or "lVowel" in syllable or "anusvara" in syllable
                or "aVowel" in syllable or "lDot" in syllable
                or "asat" in syllable or "wasway" in syllable
                or "hatoh" in syllable
            )
        ):
            syllable["cons"] = 'ရ'

        outputOrder = [
            "kinzi", "lig", "cons", "numbers", "stack", "contraction", "yapin",
            "yayit", "wasway", "hatoh", "eVowel", "uVowel", "lVowel",
            "anusvara", "aVowel", "lDot", "asat", "visarga"
        ]

        outputText = ""
        if (
            self.useZwsp and not syllable["kinzi"] and not syllable["lig"]
            and not syllable["stack"] and not syllable["contraction"]
            and not syllable["asat"] and (prevSyllable != "အ")
            and (prevSyllable is not None)
        ):
            outputText += "\u200B"

        for output in outputOrder:
            if output in syllable:
                outputText += "".join(syllable[output])

        return outputText

    def convertToUnicode(self, inputText):
        return self.convertToUnicodeSyllables(inputText)['outputText']

    def convertFromUnicode(self, inputText):
        import re
        inputText = re.sub(r'\u200B\u2060', '', inputText)
        outputText = ""
        pos = 0
        for match in self.unicodePattern.finditer(inputText):
            outputText += inputText[pos:match.start()]
            pos = match.end()
            # print match.groups ()
            outputText += self.fromUnicodeMapper(inputText, match.groups())

        if (pos < len(inputText)):
            outputText += inputText[pos:len(inputText)]
        return outputText

    def fromUnicodeMapper(self, inputText, matchData):
        # TODO
        unicodeSyllable = {}
        syllable = {}

        for i in range(0, len(matchData)):
            component = self.unicodeSequence[i]
            # match = match.decode ('utf8')
            if component is None or matchData[i] is None:
                continue
            unicodeSyllable[component] = matchData[i]
            syllable[component] = self.data[component].get(matchData[i], None)

        # print syllable, unicodeSyllable
        if "kinzi" in unicodeSyllable:
            if ("uVowel" in unicodeSyllable):
                if ("anusvara" in unicodeSyllable):
                    key = unicodeSyllable["anusvara"] + unicodeSyllable[
                        "uVowel"
                    ] + unicodeSyllable["anusvara"] + "_lig"
                    if (
                        self.data["kinzi"][key]
                        and len(self.data["kinzi"][key])
                    ):
                        syllable["kinzi"] = self.data["kinzi"][key]
                        del syllable["anusvara"]
                else:
                    key = unicodeSyllable["kinzi"] + unicodeSyllable["uVowel"
                                                                     ] + "_lig"
                    if (
                        self.data["kinzi"][key]
                        and len(self.data["kinzi"][key])
                    ):
                        syllable["kinzi"] = self.data["kinzi"][key]
                        del syllable["uVowel"]
            if ("anusvara" in unicodeSyllable):
                key = unicodeSyllable["kinzi"] + unicodeSyllable["anusvara"
                                                                 ] + "_lig"
                if (self.data["kinzi"][key] and len(self.data["kinzi"][key])):
                    syllable["kinzi"] = self.data["kinzi"][key]
                    del syllable["anusvara"]

        if (unicodeSyllable.get("cons", None) == "ဉ"):
            if ("asat" in unicodeSyllable):
                syllable["cons"] = self.data["cons"]["ဥ"]
            elif ("stack" in unicodeSyllable):
                syllable["cons"] = self.data["cons"]["ဉ_alt"]
            elif (
                "aVowel" in unicodeSyllable and "ဉာ_lig" in self.data["cons"]
            ):
                syllable["cons"] = self.data["cons"]["ဉာ_lig"]
                del syllable["aVowel"]
                # self hatoh can occur with aVowel, so no else
            if ("hatoh" in unicodeSyllable):
                syllable["hatoh"] = self.data["hatoh"]["ှ_small"]

        elif (unicodeSyllable.get("cons", None) == "ဠ"):
            if ("hatoh" in unicodeSyllable):
                syllable["hatoh"] = self.data["hatoh"]["ှ_small"]

        elif (
            unicodeSyllable.get("cons", None) == "ဈ"
            and len(self.data["cons"]["ဈ"]) == 0
        ):
            syllable["cons"] = self.data["cons"]["စ"]
            syllable["yapin"] = self.data["yapin"]["ျ"]

        elif (
            unicodeSyllable.get("cons", None) == "ဩ"
            and len(self.data["cons"]["ဩ"]) == 0
        ):
            syllable["cons"] = self.data["cons"]["သ"]
            syllable["yayit"] = self.data["yayit"]["ြ_wide"]

        elif (
            unicodeSyllable.get("cons", None) == "ဪ"
            and len(self.data["cons"]["ဪ"]) == 0
        ):
            syllable["cons"] = self.data["သ"]
            syllable["yayit"] = self.data["ြ_wide"]
            syllable["eVowel"] = self.data["ေ"]
            syllable["aVowel"] = self.data["ာ"]
            syllable["asat"] = self.data["်"]

        elif (
            unicodeSyllable.get("cons", None) == "၎င်း"
            and len(self.data["cons"]["၎င်း"]) == 0
        ):
            if (len(self.data["၎"])):
                syllable["cons"] = self.data["cons"]["၎"] + self.data["cons"]["င"] + \
                    self.data["asat"]["်"] + self.data["visarga"]["း"]
            else:
                syllable["cons"] = self.data["number"]["၄"] + self.data["cons"]["င"] + \
                    self.data["asat"]["်"] + self.data["visarga"]["း"]

        elif (
            unicodeSyllable.get("cons", None) == "န"
            or unicodeSyllable.get("cons", None) == "ည"
        ):
            if (
                "stack" in unicodeSyllable or "yapin" in unicodeSyllable
                or "wasway" in unicodeSyllable or "hatoh" in unicodeSyllable
                or "lVowel" in unicodeSyllable
            ):
                syllable["cons"] = self.data["cons"][unicodeSyllable["cons"]
                                                     + "_alt"]

        elif (unicodeSyllable.get("cons", None) == "ရ"):
            if (
                "yapin" in unicodeSyllable or "wasway" in unicodeSyllable
                or "lVowel" in unicodeSyllable
            ):
                syllable["cons"] = self.data["cons"][unicodeSyllable["cons"]
                                                     + "_alt"]
            elif (
                "hatoh" in unicodeSyllable
                and len(self.data["cons"][unicodeSyllable["cons"] + "_tall"])
            ):
                syllable["cons"] = self.data["cons"][unicodeSyllable["cons"]
                                                     + "_tall"]

        elif (unicodeSyllable.get("cons", None) == "ဦ"):
            if (len(self.data["cons"]["ဦ"]) == 0):
                syllable["cons"] = self.data["cons"]["ဥ"]
                syllable["uVowel"] = self.data["uVowel"]["ီ"]

        # stack with narrow upper cons
        if (
            (
                unicodeSyllable.get("cons", None) == "ခ"
                or unicodeSyllable.get("cons", None) == "ဂ"
                or unicodeSyllable.get("cons", None) == "င"
                or unicodeSyllable.get("cons", None) == "စ"
                or unicodeSyllable.get("cons", None) == "ဎ"
                or unicodeSyllable.get("cons", None) == "ဒ"
                or unicodeSyllable.get("cons", None) == "ဓ"
                or unicodeSyllable.get("cons", None) == "န"
                or unicodeSyllable.get("cons", None) == "ပ"
                or unicodeSyllable.get("cons", None) == "ဖ"
                or unicodeSyllable.get("cons", None) == "ဗ"
                or unicodeSyllable.get("cons", None) == "မ"
                or unicodeSyllable.get("cons", None) == "ဝ"
            ) and "stack" in unicodeSyllable
            and unicodeSyllable["stack"] + "_narrow" in self.data["stack"] and
            len(self.data["stack"][unicodeSyllable["stack"] + "_narrow"]) > 0
        ):
            syllable["stack"] = self.data["stack"][unicodeSyllable["stack"]
                                                   + "_narrow"]

        # yapin variants
        if (
            "yapin" in unicodeSyllable
            and ("wasway" in unicodeSyllable or "hatoh" in unicodeSyllable)
        ):
            if (len(self.data["yapin"]["ျ_alt"])):
                syllable["yapin"] = self.data["yapin"]["ျ_alt"]
            else:  # assume we have the ligatures
                key = "ျ" + ("wasway" in unicodeSyllable and "ွ" or "") + \
                    ("hatoh" in unicodeSyllable and "ှ" or "") + "_lig"
                if (self.data["yapin"][key]):
                    syllable["yapin"] = self.data["yapin"][key]
                    if ("wasway" in unicodeSyllable):
                        del syllable["wasway"]
                    if ("hatoh" in unicodeSyllable):
                        del syllable["hatoh"]
                else:
                    pass
                    # self.debug.print(key + " not found")
        if ("yayit" in unicodeSyllable):
            widthVariant = "_wide"
            upperVariant = ""
            if (
                unicodeSyllable.get("cons", None) == "ခ"
                or unicodeSyllable.get("cons", None) == "ဂ"
                or unicodeSyllable.get("cons", None) == "င"
                or unicodeSyllable.get("cons", None) == "စ"
                or unicodeSyllable.get("cons", None) == "ဎ"
                or unicodeSyllable.get("cons", None) == "ဒ"
                or unicodeSyllable.get("cons", None) == "ဓ"
                or unicodeSyllable.get("cons", None) == "န"
                or unicodeSyllable.get("cons", None) == "ပ"
                or unicodeSyllable.get("cons", None) == "ဖ"
                or unicodeSyllable.get("cons", None) == "ဗ"
                or unicodeSyllable.get("cons", None) == "မ"
                or unicodeSyllable.get("cons", None) == "ဝ"
            ):
                widthVariant = "_narrow"

            if (
                "uVowel" in unicodeSyllable or "kinzi" in unicodeSyllable
                or "anusvara" in unicodeSyllable
            ):
                upperVariant = "_upper"

            if ("wasway" in unicodeSyllable):
                if ("hatoh" in unicodeSyllable):
                    if (len(self.data["wasway"]["ွှ_small"])):
                        if (
                            len(
                                self.data["yayit"]["ြ" + upperVariant +
                                                   widthVariant]
                            )
                        ):
                            syllable["yayit"] = self.data["yayit"
                                                          ]["ြ" + upperVariant
                                                            + widthVariant]
                        else:
                            if (widthVariant == "_narrow"):
                                widthVariant = ""
                            syllable["yayit"] = self.data["yayit"
                                                          ]["ြ" + widthVariant]
                        syllable["wasway"] = self.data["wasway"]["ွှ_small"]
                        del syllable["hatoh"]
                    elif (len(self.data["yayit"]["ြ_lower" + widthVariant])):
                        if (
                            len(
                                self.data["yayit"]["ြ_lower" + upperVariant +
                                                   widthVariant]
                            )
                        ):
                            syllable["yayit"] = self.data[
                                "yayit"
                            ]["ြ_lower" + upperVariant + widthVariant]
                        else:
                            syllable["yayit"] = self.data["yayit"
                                                          ]["ြ_lower"
                                                            + widthVariant]

                elif (
                    len(
                        self.data["yayit"]["ြွ" + upperVariant + widthVariant]
                    )
                ):
                    syllable["yayit"] = self.data["yayit"]["ြွ" + upperVariant
                                                           + widthVariant]
                    del syllable["wasway"]

                elif (len(self.data["yayit"]["ြွ" + widthVariant])):
                    syllable["yayit"] = self.data["yayit"]["ြွ" + widthVariant]
                    del syllable["wasway"]

                elif (len(self.data["yayit"]["ြ_lower_wide"])):
                    if (
                        len(
                            self.data["yayit"]["ြ" + "_lower" + upperVariant +
                                               widthVariant]
                        )
                    ):
                        syllable["yayit"] = self.data["yayit"]["ြ" + "_lower" +
                                                               upperVariant +
                                                               widthVariant]
                    else:
                        syllable["yayit"] = self.data["yayit"]["ြ" + "_lower" +
                                                               widthVariant]

            elif ("hatoh" in unicodeSyllable):
                if (len(upperVariant) == 0 and widthVariant == "_narrow"):
                    widthVariant = ""
                if (
                    len(self.data["yayit"]["ြ" + upperVariant + widthVariant])
                ):
                    syllable["yayit"] = self.data["yayit"]["ြ" + upperVariant +
                                                           widthVariant]
                elif (len(self.data["yayit"]["ြ" + widthVariant])):
                    syllable["yayit"] = self.data["yayit"]["ြ" + widthVariant]
                else:
                    syllable["yayit"] = self.data["yayit"]["ြ"]
                syllable["hatoh"] = self.data["hatoh"]["ှ_small"]

            elif (
                "lVowel" in unicodeSyllable
                and unicodeSyllable["lVowel"] == "ု"
                and self.data["yayit"]["ြု_wide"]
            ):
                if (
                    syllable["uVowel"] == self.data["uVowel"]["ိ"]
                    and self.data["yayit"]["ြို" + widthVariant]
                ):
                    syllable["yayit"] = self.data["yayit"]["ြို"
                                                           + widthVariant]
                    del syllable["uVowel"]
                else:
                    if (
                        len(
                            self.data["yayit"]["ြု" + upperVariant +
                                               widthVariant]
                        )
                    ):
                        syllable["yayit"] = self.data["yayit"]["ြု"
                                                               + upperVariant +
                                                               widthVariant]
                    else:
                        syllable["yayit"] = self.data["yayit"]["ြု"
                                                               + widthVariant]
                del syllable["lVowel"]

            else:
                if (len(upperVariant) == 0 and widthVariant == "_narrow"):
                    widthVariant = ""
                syllable["yayit"] = self.data["yayit"]["ြ" + upperVariant +
                                                       widthVariant]

        if ("wasway" in syllable and "hatoh" in syllable):
            del syllable["hatoh"]
            syllable["wasway"] = self.data["wasway"]["ွှ_lig"]

        if (
            "hatoh" in syllable and "lVowel" in syllable
            and "yapin" not in syllable and "yayit" not in syllable
        ):
            syllable["hatoh"] = self.data["hatoh"]["ှ"
                                                   + unicodeSyllable["lVowel"]
                                                   + "_lig"]
            del syllable["lVowel"]

        if (
            "uVowel" in syllable and unicodeSyllable["uVowel"] == "ိ"
            and "anusvara" in syllable and unicodeSyllable["anusvara"] == "ံ"
        ):
            syllable["uVowel"] = self.data["uVowel"]["ိံ_lig"]
            del syllable["anusvara"]

        if (
            "lVowel" in syllable and (
                "yayit" in unicodeSyllable or "yapin" in unicodeSyllable
                or "wasway" in unicodeSyllable or "hatoh" in unicodeSyllable
                or "lig" in unicodeSyllable or "stack" in unicodeSyllable
                or unicodeSyllable.get("cons", None) == "ဍ"
                or unicodeSyllable.get("cons", None) == "ဋ"
                or unicodeSyllable.get("cons", None) == "ဌ"
                or unicodeSyllable.get("cons", None) == "ဈ"
                or unicodeSyllable.get("cons", None) == "ဥ"
                or unicodeSyllable.get("cons", None) == "ဠ"
            )
        ):
            syllable["lVowel"] = self.data["lVowel"][unicodeSyllable["lVowel"]
                                                     + "_tall"]

        if (
            "aVowel" in unicodeSyllable and "asat" in unicodeSyllable
            and unicodeSyllable["aVowel"] == "ါ"
        ):
            syllable["aVowel"] = self.data["aVowel"]["ါ်_lig"]
            del syllable["asat"]

        if (
            "lDot" in unicodeSyllable and (
                "aVowel" in unicodeSyllable or not (
                    "yayit" in unicodeSyllable or "lig" in unicodeSyllable
                    or "stack" in unicodeSyllable or "yapin" in unicodeSyllable
                    or "wasway" in unicodeSyllable or
                    "hatoh" in unicodeSyllable or "lVowel" in unicodeSyllable
                    or unicodeSyllable.get("cons", None) == "ဍ"
                    or unicodeSyllable.get("cons", None) == "ဋ"
                    or unicodeSyllable.get("cons", None) == "ဌ"
                    or unicodeSyllable.get("cons", None) == "ဈ"
                    or unicodeSyllable.get("cons", None) == "ရ"
                )
            )
        ):
            if (unicodeSyllable.get("cons", None) == "န"):
                syllable["lDot"] = self.data["lDot"]["့_alt"]
            else:
                syllable["lDot"] = self.data["lDot"]["့_left"]

        if (
            "lDot" in unicodeSyllable and "yayit" not in syllable
            and not (unicodeSyllable.get("cons", None) == "ရ") and (
                (
                    "hatoh" in syllable and len(syllable["hatoh"]) == 1
                    and "lVowel" not in syllable
                ) or (
                    "lVowel" in syllable
                    and syllable["lVowel"] == self.data["lVowel"]["ု"]
                )
            )
        ):
            syllable["lDot"] = self.data["lDot"]["့_alt"]

        if ("asat" in syllable):
            if (
                "eVowel" not in syllable and (
                    "yayit" in syllable or "yapin" in syllable
                    or "wasway" in syllable or "lVowel" in syllable
                )
            ):
                syllable["contraction"] = syllable["asat"]
                del syllable["asat"]

        outputOrder = [
            "eVowel", "yayit", "lig", "cons", "stack", "contraction", "yapin",
            "kinzi", "wasway", "hatoh", "uVowel", "lVowel", "anusvara",
            "aVowel", "asat", "lDot", "visarga"
        ]

        outputText = ""

        # print syllable
        for o in outputOrder:
            if (o in syllable and syllable[o]):
                outputText += syllable[o]

        return outputText


def get_available_encodings():
    """
    return a list of supported encodings.
    >>> myanmar.converter.get_available_encodings ()
    ['zawgyi', 'wwin_burmese', 'wininnwa', 'unicode']
    """
    global _converters
    return list(_converters.keys()) + ['unicode']


def convert(text, from_encoding, to_encoding):
    """
    convert from one encoding to another.
    from_encoding and to_encoding must be one of the encodings
    from get_available_encodings ()
    text must be a unicode string object.
    """
    if isinstance(type(text), type('')):
        try:
            text = text.decode('utf-8')
        except Exception:
            raise UnicodeDecodeError

    for encoding in [from_encoding, to_encoding]:
        if encoding not in get_available_encodings():
            raise ValueError('%s encoding is not available' % encoding)

    if from_encoding != 'unicode':
        utext = _converters[from_encoding].convertToUnicode(text)
    else:
        utext = text

    # print utext
    if to_encoding != 'unicode':
        rtext = _converters[to_encoding].convertFromUnicode(utext)
    else:
        rtext = utext

    return rtext


# return _converters['zawgyi'].convertToUnicode (text)


def _load_converters():
    """
    load available encodings from json files
    """
    global _converters
    import json
    import os
    import codecs

    _ROOT = os.path.dirname(os.path.abspath(__file__))

    def get_utf8_data(filename):
        _path = os.path.join(_ROOT, 'data', filename)
        data = ""

        try:
            with codecs.open(_path, 'r', 'utf8') as fil:
                data = json.loads(fil.read())
        except Exception:
            print(("Unable to load %s" % filename))

        return data

    for _file in ['zawgyi.json', 'wininnwa.json']:
        data = get_utf8_data(_file)
        _converters[os.path.splitext(_file)[0]] = _TlsMyanmarConverter(data)


_load_converters()
convert("wmrDe,frStokH;ðyykH", "zawgyi", "unicode")
convert("ကမၻာ", "zawgyi", "unicode")