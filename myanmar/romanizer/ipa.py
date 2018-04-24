import json
import pkgutil


class IPA():
    table = json.loads(
        pkgutil.get_data('myanmar', 'data/ipa.json').decode('utf-8')
    )
    vowels = 'aáeèioóôu'

    @classmethod
    def normalize(cls, ipa, prev):
        ipa = ipa.replace('kj', 'tɕ')
        ipa = ipa.replace('kʰj', 'tɕʰ')
        ipa = ipa.replace('ɡj', 'dʑ')
        ipa = ipa.replace('j̥', 'ʃ')
        ipa = ipa.replace('ŋ̥', 'ŋ̊')
        ipa = ipa.replace('ŋj', 'ɲ')
        if prev:
            ipa = cls.add_ə(ipa, prev)
            ipa = cls.change_k_to_g(ipa, prev)
            ipa = cls.change_s_to_z(ipa, prev)
            ipa = cls.change_p_to_b(ipa, prev)
            ipa = cls.change_t_to_d(ipa, prev)
        return ipa

    @classmethod
    def add_ə(cls, ipa, prev):
        prev_len = 0
        if prev[-1] == 'ʰ' and len(prev[-2]) == 1:
            prev_len = 1
        if len(prev) == 1 or prev_len == 1:
            ipa = 'ə' + ipa
        return ipa

    @classmethod
    def change_k_to_g(cls, ipa, prev):
        # change k to g after vowel sound
        if ipa.startswith('k') and cls.ends_with_vowel(prev):
            ipa = 'g' + ipa[1:]
        return ipa

    @classmethod
    def change_s_to_z(cls, ipa, prev):
        # change s to z after vowel sound
        if ipa.startswith('s') and cls.ends_with_vowel(prev):
            ipa = 'z' + ipa[1:]
        return ipa

    @classmethod
    def change_p_to_b(cls, ipa, prev):
        # change pa to ba after vowel sound
        if ipa.startswith('p') and cls.has_vowel(ipa):
            ipa = 'b' + ipa[1:]
        return ipa

    @classmethod
    def change_t_to_d(cls, ipa, prev):
        # change t to d after vowel sound
        startswitht = ipa.startswith('t') and not ipa.startswith('th')
        if startswitht and cls.ends_with_vowel(prev):
            ipa = 'd' + ipa[1:]
        return ipa

    @classmethod
    def ends_with_vowel(cls, ipa):
        return ipa[-1] in 'aàeioun' or ipa.endswith('ng')

    @classmethod
    def has_vowel(cls, ipa):
        # if any of cls.vowels  exists in IPA
        return any(ipa.find(v) != -1 for v in cls.vowels)
