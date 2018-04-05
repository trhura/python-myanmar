from myanmar import language
from myanmar import encodings


def test_zawgyi_morpho_syllable_break():
    test = 'သီ|ဟို|ဠ္|မွ| |ဉာ|ဏ္|ႀကီး|ရွ|င္|သ|ည္| |' + \
        'အာ|ယု|ဝ|ဍ္|ဎ|န|ေဆး|ၫႊ|န္း|စာ|ကို| |' + \
        'ဇ|လြ|န္|ေဈး|ေဘး|ဗာ|ဒံ|ပ|င္|ထ|က္| |' + \
        'အ|ဓိ|႒|ာ|န္|လ်|က္| |ဂ|ဃ|န|ဏ|ဖ|တ္|ခဲ့|သ|ည္'

    syllables = test.split("|")
    text = "".join(syllables)

    zgyenc = encodings.ZawgyiEncoding()
    iterable = language.MorphoSyllableBreak(text=text, encoding=zgyenc)

    for i, item in enumerate(iterable):
        assert item['syllable'] == syllables[i]


def test_unicode_morpho_syllable_break():
    test = 'အ|ခု| |လ|က်|ရှိ| |သွ|င်း|နေ|တဲ့| |ကု|မ္ပ|ဏီ|က|' + \
        '၆| |လ| |အ|ထိ| |ပို|က်|ဆံ| |ပြ|န်|မ|ထု|တ်|ဘဲ|' + \
        'အ|ကြွေး|ပေး|ထား| |နို|င်|တ|ယ်|။|မ|င်း|တို့| |' + \
        'အဲ|ဒီ|လို|ပေး|နို|င်|ရ|င်|တော့| |ရ|နို|င်|တ|ယ်|' + \
        'ပြော|လို့| |တ|ပ်|လ|န်| |သွား|ခဲ့|ရ|ပါ|တ|ယ်|။|' + \
        'အဲ|ဒါ|နဲ့| |မြ|န်|မာ|ပြ|ည်|မှာ| |အ|ခု|မှ| |စ|ပြီး|' + \
        'ခေ|တ်|စား|လာ|တဲ့| |ပ|စ္စ|ည်း|တ|စ်|ခု|ကို|စျေး|ကွ|က်|ထဲ|' + \
        'ဖော|က်|ဖို့| |ကြံ|ပြ|န်| |ပါ|တ|ယ်|။|သူ|င|ယ်|ချ|င်း|' + \
        'တ|စ်|ယော|က်|နဲ့| |စ|ကား|စ|ပ်|မိ|တော့| |သူ|က|' + \
        'အဲ|ဒီ|ပ|စ္စ|ည်း|ကို| |ကွ|န်|တိ|န်|နာ| |အ|လုံး|လို|က်|သွ|င်း|ပြီး|' + \
        'ရော|င်း|နေ|တ|ယ်| |ဆို|တာ| |သိ|လို|က်|ရ| |ပြ|န်|ပါ|တ|ယ်|။'

    syllables = test.split("|")
    text = "".join(syllables)

    unienc = encodings.UnicodeEncoding()
    iterable = language.MorphoSyllableBreak(text=text, encoding=unienc)

    for i, item in enumerate(iterable):
        assert item['syllable'] == syllables[i]


def test_myanmar_phonemic_iter():
    test = "တ|ရား|စီ|ရင်|ရေး|အာ|ဏာ|နှင့်|ဥ|ပ|ဒေ|ပြု|ရေး|အာ|ဏာ|တို့|ကို|" + \
            "မည်|သူ|မ|ဆို| |ကြည့်|ရှု|ပြင်|ဆင်|နိုင်|သော| |" + \
            "အ|ခ|မဲ့|လွတ်|လပ်|စွယ်|စုံ|ကျမ်း| |ဖြစ်|ပါ|သည်|။|" + \
            "နာ|နို|တက္|က|နော်|လော်|ဂျီ|" + \
            "အို|ရှန်း|နီး|ယား"

    syllables = test.split("|")
    text = "".join(syllables)

    unienc = encodings.UnicodeEncoding()
    iterable = language.PhonemicSyllableBreak(text=text, encoding=unienc)

    for i, item in enumerate(iterable):
        assert item['syllable'] == syllables[i]
