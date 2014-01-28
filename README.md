## About

This module currently contains routines, ported from Thanlwinsoft's
javascript converter, for conversion between unicode and Myanmar
legacy encodings, such as zawgyi, wininwa.

This module also comes with a script, namely `myanmar-converter`, which
can be used to convert encodings from CLI.

## Install

Note: You must have python-chardet installed on your system.

To install, run this command.

    python setup.py install

## Usage

* Using myanmar python module

```python
>>> import myanmar.converter as converter
>>> converter.get_available_encodings ()
['zawgyi', 'wwin_burmese', 'wininnwa', 'unicode']
>>> print converter.convert (u'ydkifoGefy½dk*&rfrif;', 'wininnwa', 'unicode')
ပိုင်​သွန်​ပ​ရို​ဂ​ရမ်​မင်း
```

* Using myanmar-converter script

```sh
trhura @ ~ $ myanmar-converter -h
Usage: myanmar-converter [OPTIONS...] [FILE...]

Convert between Myanmar legacy encodings and unicode.

Options:
       --version             show program's version number and exit
       -h, --help            show this help message and exit
       -l, --list            List supported encodings.
       -f ENCODING, --from=ENCODING
                             Convert characters from ENCODING
       -t ENCODING, --to=ENCODING
                             Convert characters to ENCODING
        -o FILE, --output=FILE
                             Write output to FILE
```

```sh
trhura @ ~ $ echo 'wmrDe,frStokH;ðyykH' | myanmar-converter -f 'wwin_burmese' -t 'unicode'
တာ​မီ​နယ်​မှ​အသုံးပြု​ပုံ
```

* Convert filenames from zawgyi to unicode

```sh
trhura @ ~ $ for f in *;do mv "$f" $(echo "$f" | myanmar-converter -f 'zawgyi' -t 'unicode');done
# This command will rename every files in current directory from zawgyi encoding to unicode.
```

* Extract unicode text from pdf file

```sh
trhura @ ~ $ pdftotext some.pdf - | myanmar-converter -f 'wininnwa' -t 'unicode' -o some.txt
```
