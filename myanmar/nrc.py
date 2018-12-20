# nrc.py - myanmar nrc validation & normalization module
# coding: utf-8
# The MIT License (MIT)
# Copyright (c) 2018 Soe Zayar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import re

all_township_names = {
              1: {'bkn': 'bakana', 'pmn': 'pamana', 'htn': 'ahtana',
                  'mtn': 'matana', 'khphn': 'khaphana', 'tnn': 'tanana',
                  'phkn': 'phakana', 'kmn': 'kamana', 'khlph': 'khalapha',
                  'mkhb': 'makhaba', 'msn': 'masana', 'mkt': 'makata',
                  'mnyn': 'manyana', 'hpn': 'hapana', 'mkth': 'makatha',
                  'mmn': 'mamana', 'mkn': 'makana', 'skn': 'sakana',
                  'kmt': 'kamata', 'sbt': 'sabata', 'mgd': 'magada',
                  'hgy': 'ahgaya', 'nmn': 'namana', 'pth': 'pataah',
                  'ykn': 'yakana', 'sbn': 'sabana', 'sln': 'salana',
                  'wmn': 'wamana'},
              2: {'blkh': 'balakha', 'dms': 'damasa', 'ssn': 'sasana',
                  'phsn': 'phanasa', 'http': 'htatapa', 'khsn': 'khasana',
                  'phls': 'phalasa', 'phys': 'phayasa', 'lkn': 'lakana',
                  'msn': 'masana', 'ytn': 'yatana'},
              3: {'lbn': 'labana', 'pkn': 'pakana', 'yyth': 'yayatha',
                  'phhn': 'phaahna', 'bhn': 'baahna', 'phpn': 'phapana',
                  'kmm': 'kamama', 'kky': 'kakaya', 'kdn': 'kadana',
                  'ksk': 'kasaka', 'mwt': 'mawata', 'skl': 'sakala',
                  'msl': 'masala', 'ktkh': 'katakha', 'wlm': 'walama',
                  'bgl': 'bagala', 'lthn': 'lathana', 'thtn': 'thatana',
                  'thtk': 'thataka'},
              4: {'phln': 'phalana', 'hkhn': 'hakhana', 'kpl': 'kapala',
                  'mtn': 'matana', 'plw': 'palawa', 'ttn': 'tatana',
                  'httl': 'htatala', 'tzn': 'tazana'},
              5: {'hyt': 'ahyata', 'bmn': 'bamana', 'btl': 'batala',
                  'khn': 'khauna', 'khtn': 'khatana', 'hml': 'hamala',
                  'htn': 'ahtana', 'hhtn': 'ahhtana', 'kln': 'kalana',
                  'klht': 'kalahta', 'klw': 'kalawa', 'kbl': 'kabala',
                  'knn': 'kanana', 'kthn': 'kathana', 'klt': 'kalata',
                  'ksl': 'kasala', 'htpkh': 'htapakha', 'lhn': 'lahana',
                  'lyn': 'layana', 'mpl': 'mapala', 'smy': 'samaya',
                  'mln': 'malana', 'mkn': 'makana', 'myn': 'mayana',
                  'mmn': 'mamana', 'dhn': 'dahana', 'nyn': 'nayana',
                  'psn': 'pasana', 'pln': 'palana', 'phpn': 'phapana',
                  'plb': 'palaba', 'skn': 'sakana', 'slk': 'salaka',
                  'kmn': 'kamana', 'ybn': 'yabana', 'dpy': 'dapaya',
                  'tmn': 'tamana', 'mthn': 'mathana', 'tsn': 'tasana',
                  'htkhn': 'htakhana', 'klth': 'kalatha', 'ngsn': 'ngasana',
                  'dkn': 'dakana', 'hmz': 'ahmaza', 'wln': 'walana',
                  'wthn': 'wathana', 'yn': 'yauna', 'ymp': 'yamapa'},
              6: {'bpn': 'bapana', 'htwn': 'htawana', 'kyy': 'kayaya',
                  'kpn': 'kapana', 'kthm': 'kathama', 'htht': 'hathata',
                  'khmk': 'khamaka', 'mml': 'mamala', 'kthn': 'kathana',
                  'ksn': 'kasana', 'mhn': 'maahna', 'lln': 'lalana',
                  'mmn': 'mamana', 'mhy': 'maahya', 'hmy': 'ahmaya',
                  'pln': 'palana', 'tthy': 'tathaya', 'thykh': 'thayakha',
                  'yphn': 'yaphana'},
              7: {'pkhn': 'pakhana', 'mwt': 'mawata', 'dn': 'dauna',
                  'kpk': 'kapaka', 'http': 'htatapa', 'kwn': 'kawana',
                  'kkn': 'kakana', 'ktkh': 'katakha', 'ktn': 'katana',
                  'lpt': 'lapata', 'mln': 'malana', 'mnyn': 'manyana',
                  'ntl': 'natala', 'nylp': 'nyalapa', 'hphn': 'ahphana',
                  'htn': 'ahtana', 'ptn': 'patana', 'pkht': 'pakhata',
                  'ptt': 'patata', 'phmn': 'phamana', 'pst': 'pasata',
                  'pmn': 'pamana', 'ytn': 'yatana', 'ykn': 'yakana',
                  'tngn': 'tangana', 'thnp': 'thanapa', 'thwt': 'thawata',
                  'thkn': 'thakana', 'wmn': 'wamana', 'yty': 'yataya',
                  'zkn': 'zakana'},
              8: {'hln': 'ahlana', 'mhtn': 'mahtana', 'khmn': 'khamana',
                  'bkl': 'bakala', 'ggn': 'gagana', 'kmn': 'kamana',
                  'mkn': 'makana', 'mbn': 'mabana', 'mtn': 'matana',
                  'mln': 'malana', 'mmn': 'mamana', 'mthn': 'mathana',
                  'nmn': 'namana', 'ngphn': 'ngaphana', 'pkhk': 'pakhaka',
                  'pmn': 'pamana', 'pphn': 'paphana', 'sln': 'salana',
                  'khtn': 'kahtana', 'sphn': 'saphana', 'sty': 'sataya',
                  'spw': 'sapawa', 'mys': 'mayasa', 'mgd': 'magada',
                  'mhtl': 'mahtala', 'ttk': 'tataka', 'thyn': 'thayana',
                  'htln': 'htalana', 'ynkh': 'yanakha', 'ysk': 'yasaka'},
              9: {'hmy': 'ahmaya', 'khms': 'khamasa', 'khmkh': 'khamakha',
                  'hyt': 'ahyata', 'thty': 'thataya', 'khmz': 'khamaza',
                  'nnm': 'nanama', 'pkhm': 'pakhama', 'kmn': 'kamana',
                  'hmz': 'ahmaza', 'mnm': 'manama', 'khhz': 'khaahza',
                  'khmth': 'khamatha', 'kpt': 'kapata', 'khmn': 'khamana',
                  'ksn': 'kasana', 'ntk': 'nataka', 'skt': 'sakata',
                  'msn': 'masana', 'lkn': 'lakana', 'yn': 'yauna',
                  'myt': 'mayata', 'mtn': 'matana', 'mty': 'mataya',
                  'mhm': 'mahama', 'mln': 'malana', 'mhtl': 'mahtala',
                  'mkn': 'makana', 'mkhn': 'makhana', 'mthn': 'mathana',
                  'nmn': 'namana', 'mtl': 'matala', 'nhtk': 'nahtaka', 'ngzn':
                  'ngazana', 'nyn': 'nyauna', 'khn': 'kahana',
                  'pthk': 'pathaka', 'pbn': 'pabana', 'pkkh': 'pakakha',
                  'hmb': 'ahmaba', 'hsn': 'ahsana', 'khmm': 'khamama',
                  'mkkh': 'makakha', 'mnt': 'manata', 'mym': 'mayama',
                  'pkhk': 'pakhaka', 'thwn': 'thawana', 'pl': 'paula',
                  'mmn': 'mamana', 'skn': 'sakana', 'tt': 'tatau',
                  'tthn': 'tathana', 'thpk': 'thapaka', 'thsn': 'thasana',
                  'wtn': 'watana', 'ymth': 'yamatha', 'dkhth': 'dakhatha',
                  'lwn': 'lawana', 'utth': 'utatha', 'pbth': 'pabatha',
                  'pmn': 'pamana', 'tkn': 'takana', 'zbth': 'zabatha',
                  'zyth': 'zayatha', 'hkhn': 'ahkhana'},
              10: {'bln': 'balana', 'khsn': 'khasana', 'kmy': 'kamaya',
                   'bhn': 'baahna', 'khtn': 'kahtana', 'hthtn': 'htahtana',
                   'kml': 'kamala', 'phpn': 'phapana', 'msn': 'masana',
                   'mlm': 'malama', 'mdn': 'madana', 'pmn': 'pamana',
                   'thphy': 'thaphaya', 'thhtn': 'thahtana',
                   'khzn': 'khazana', 'lmn': 'lamana', 'ymn': 'yamana'},
              11: {'btht': 'bathata', 'gmn': 'gamana', 'ktl': 'katala',
                   'kphn': 'kaphana', 'ktn': 'katana', 'mmn': 'mamana',
                   'mtn': 'matana', 'tpw': 'tapawa', 'mn': 'mauna',
                   'mpn': 'mapana', 'ptn': 'patana', 'pnk': 'panaka',
                   'ybn': 'yabana', 'hmn': 'ahmana', 'ytht': 'yathata',
                   'ytn': 'yatana', 'mpt': 'mapata', 'ytth': 'yatatha',
                   'lmt': 'lamata', 'stn': 'satana', 'thtn': 'thatana',
                   'mhn': 'maahna', 'tkn': 'takana'},
              12: {'hln': 'ahlana', 'bhn': 'bahana', 'btht': 'batahta',
                   'kkk': 'kakaka', 'dgn': 'dagana', 'dgs': 'dagasa',
                   'dln': 'dalana', 'dpn': 'dapana', 'dgy': 'dagaya',
                   'lmn': 'lamana', 'lthy': 'lathaya', 'lkn': 'lakana',
                   'mbn': 'mabana', 'http': 'htatapa', 'hsn': 'ahsana',
                   'kmy': 'kamaya', 'skkh': 'sakakha', 'kmn': 'kamana',
                   'khyn': 'khayana', 'kkhk': 'kakhaka', 'ktt': 'katata',
                   'ktn': 'katana', 'kmt': 'kamata', 'lmt': 'lamata',
                   'lthn': 'lathana', 'myk': 'mayaka', 'mgd': 'magada',
                   'mgt': 'magata', 'dgm': 'dagama', 'mk': 'mauka',
                   'km': 'ukama', 'pbt': 'pabata', 'pzt': 'pazata',
                   'skhn': 'sakhana', 'skn': 'sakana',
                   'ypth': 'yapatha', 'dgt': 'dagata', 'kt': 'ukata',
                   'tk': 'tauka', 'tkn': 'takana', 'tmn': 'tamana',
                   'thkt': 'thakata', 'thln': 'thalana', 'thgk': 'thagaka',
                   'thkhn': 'thakhana', 'ttn': 'tatana', 'ykn': 'yakana'},
              13: {'mmn': 'mamana', 'mpn': 'mapana', 'hpn': 'hapana',
                   'thnn': 'thanana', 'ssn': 'sasana', 'thpn': 'thapana',
                   'knl': 'kalana', 'ktn': 'katana', 'kkn': 'kakana',
                   'mhtt': 'mahtata', 'khn': 'kahana', 'kkhn': 'kakhana',
                   'tmny': 'tamanya', 'kmn': 'kamana', 'mngn': 'mangana',
                   'kthn': 'kathana', 'lkhn': 'lakhana', 'hmn': 'hamana',
                   'lyn': 'layana', 'khyh': 'khayaha', 'lkn': 'lakana',
                   'ysn': 'yasana', 'lln': 'lalana', 'mbn': 'mabana',
                   'mtn': 'matana', 'mkht': 'makhata', 'msn': 'masana',
                   'mpht': 'maphata', 'mphn': 'maphana', 'mln': 'malana',
                   'mnn': 'manana', 'ttn': 'tatana', 'ppk': 'papaka',
                   'myt': 'mayata', 'myn': 'mayana', 'mhy': 'mahaya',
                   'mkn': 'makana', 'mst': 'masata', 'wkn': 'wakana',
                   'nkhn': 'nakhana', 'nsn': 'nasana', 'nphn': 'naphana',
                   'khln': 'khalana', 'ntn': 'natana', 'nmt': 'namata',
                   'nyyn': 'nyayana', 'mkhn': 'makhana', 'psn': 'pasana',
                   'pwn': 'pawana', 'phkhn': 'phakhana', 'pty': 'pataya',
                   'pln': 'palana', 'tkhl': 'takhala', 'tyn': 'tayana',
                   'tkn': 'takana', 'ktl': 'katala', 'ynyn': 'yanyana',
                   'yngn': 'yangana'},
              14: {'bkl': 'bakala', 'dnph': 'danapha', 'ddy': 'dadaya',
                   'kmn': 'kamana', 'pkkh': 'pakakha', 'htht': 'hathata',
                   'hgp': 'ahgapa', 'tmn': 'tamana', 'kkht': 'kakahta',
                   'kln': 'kalana', 'kkhn': 'kakhana', 'kkn': 'kakana',
                   'kpn': 'kapana', 'lpt': 'lapata', 'psl': 'pasala',
                   'lmn': 'lamana', 'mhp': 'maahpa', 'mmk': 'mamaka',
                   'mhn': 'maahna', 'hpn': 'ahpana', 'mmn': 'mamana',
                   'hkk': 'hakaka', 'ngpt': 'ngapata', 'ngyk': 'ngayaka',
                   'nytn': 'nyatana', 'ptn': 'patana', 'ythy': 'yathaya',
                   'myk': 'mayaka', 'hsn': 'ahsana', 'pthy': 'pathaya',
                   'pthn': 'pathana', 'ngsn': 'ngasana', 'hmn': 'ahmana',
                   'kmth': 'kamatha', 'phpn': 'phapana', 'thpn': 'thapana',
                   'wkhm': 'wakhama', 'ykn': 'yakana', 'ngthkh': 'ngathakha',
                   'zln': 'zalana'}
            }

ccode = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

nation_dict = {'naing': 'n', 'pyu': 'p', 'ae': 'a',
               'n': 'n', 'p': 'p', 'e': 'e'}


"""
Valid nrc format is ./...(.)......
But with this program,
user can write ',''.'' ' instead of '/'
and ','''.'' ' instead of '()'
"""
city_code_re = r'(\d{1,2}?)\s*'
township_name_re = r'\s*(\b\w.*\s*\w.*\s*\b)\s*'
nation_re = r'(\b\w.*\s*\w*.*\s*\b)'
number_re = r'\s*(\b[0-9][0-9]{5}\b)'

nrc_format = re.compile(
    city_code_re + r'[/ .,]' + township_name_re +
    r'[( .,]' + nation_re + r'[,. )]' + number_re
)


def is_valid_nrc(nrc):
    """
    Check whether the given string is
    valid Myanmar national registration ID or not

    >>> is_valid_nrc('12/LMN (N) 144144')
    True
    >>> is_valid_nrc('9/PMN (N) 1234567')
    False
    """
    nrc = nrc.lower()
    match = nrc_format.search(nrc)

    if not match:
        raise RuntimeError(
            "%s is not a valid Myanmar nrc number." % nrc)

    city_code = int(match.group(1))
    township_name = match.group(2)
    nation = match.group(3)

    cname_no_space = township_name.replace(' ', '')
    cname_no_vowel = re.sub(r'[aeiou]', '', cname_no_space)

    if city_code not in ccode:
        return False

    if cname_no_vowel not in all_township_names[city_code]:
        return False

    if nation not in nation_dict:
        return False
    else:
        nrc
    return nrc is not None


def normalize_nrc(nrc):
    """
    >>> normalize_nrc('9/pmn(n)217289')
    9 pamana n 217289
    >>> normalize_nrc('5/pmn(n)217289')
    This nrc is not a valid myanmar nrc
    """
    nrc = nrc.lower()
    search = is_valid_nrc(nrc)

    if not search:
        raise RuntimeError(
            "%s is not a valid Myanmar nrc number." % nrc)

    match = nrc_format.search(nrc)
    city_code = int(match.group(1))
    township_name = match.group(2)
    nation = match.group(3)
    number = match.group(4)

    cname_no_space = township_name.replace(' ', '')
    cname_no_vowel = re.sub(r'[aeiou]', '', cname_no_space)
    nation_no_space = nation.replace(' ', '')

    nrc_normalize = (str(city_code) + ' '
                     + all_township_names[city_code][cname_no_vowel]
                     + ' ' + nation_dict[nation_no_space] + ' ' + number)

    return nrc_normalize
