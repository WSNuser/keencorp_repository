# -*- coding: utf-8 -*-
import time
import urllib
import zipfile
from xml.etree.ElementTree import iterparse

KNOWN_ENCODINGS = ["ascii","646","us-ascii","big5","big5-tw","csbig5","big5hkscs","big5-hkscs","hkscs","cp037","IBM037","IBM039","cp424","EBCDIC-CP-HE","IBM424","cp437","437","IBM437","cp500","EBCDIC-CP-BE","EBCDIC-CP-CH","IBM500","cp737","","cp775","IBM775","cp850","850","IBM850","cp852","852","IBM852","cp855","855","IBM855","cp856","","cp857","857","IBM857","cp860","860","IBM860","cp861","861","CP-IS","IBM861","cp862","862","IBM862","cp863","863","IBM863","cp864","IBM864","cp865","865","IBM865","cp866","866","IBM866","cp869","869","CP-GR","IBM869","cp874","","cp875","","cp932","932","ms932","mskanji","ms-kanji","cp949","949","ms949","uhc","cp950","950","ms950","cp1006","","cp1026","ibm1026","cp1140","ibm1140","cp1250","windows-1250","cp1251","windows-1251","cp1252","windows-1252","cp1253","windows-1253","cp1254","windows-1254","cp1255","windows-1255","cp1256","windows1256","cp1257","windows-1257","cp1258","windows-1258","euc_jp","eucjp","ujis","u-jis","euc_jis_2004","jisx0213","eucjis2004","euc_jisx0213","eucjisx0213","euc_kr","euckr","korean","ksc5601","ks_c-5601","ks_c-5601-1987","ksx1001","ks_x-1001","gb2312","chinese","csiso58gb231280","euc-cn","euccn","eucgb2312-cn","gb2312-1980","gb2312-80","iso-ir-58","gbk","936","cp936","ms936","gb18030","gb18030-2000","hz","hzgb","hz-gb","hz-gb-2312","iso2022_jp","csiso2022jp","iso2022jp","iso-2022-jp","iso2022_jp_1","iso2022jp-1","iso-2022-jp-1","iso2022_jp_2","iso2022jp-2","iso-2022-jp-2","iso2022_jp_2004","iso2022jp-2004","iso-2022-jp-2004","iso2022_jp_3","iso2022jp-3","iso-2022-jp-3","iso2022_jp_ext","iso2022jp-ext","iso-2022-jp-ext","iso2022_kr","csiso2022kr","iso2022kr","iso-2022-kr","latin_1","iso-8859-1","iso8859-1","8859","cp819","latin","latin1","L1","iso8859_2","iso-8859-2","latin2","L2","iso8859_3","iso-8859-3","latin3","L3","iso8859_4","iso-8859-4","latin4","L4","iso8859_5","iso-8859-5","cyrillic","iso8859_6","iso-8859-6","arabic","iso8859_7","iso-8859-7","greek","greek8","iso8859_8","iso-8859-8","hebrew","iso8859_9","iso-8859-9","latin5","L5","iso8859_10","iso-8859-10","latin6","L6","iso8859_13","iso-8859-13","iso8859_14","iso-8859-14","latin8","L8","iso8859_15","iso-8859-15","johab","cp1361","ms1361","koi8_r","","koi8_u","","mac_cyrillic","maccyrillic","mac_greek","macgreek","mac_iceland","maciceland","mac_latin2","maclatin2","maccentraleurope","mac_roman","macroman","mac_turkish","macturkish","ptcp154","csptcp154","pt154","cp154","cyrillic-asian","shift_jis","csshiftjis","shiftjis","sjis","s_jis","shift_jis_2004","shiftjis2004","sjis_2004","sjis2004","shift_jisx0213","shiftjisx0213","sjisx0213","s_jisx0213","utf_16","U16","utf16","utf_16_be","UTF-16BE","utf_16_le","UTF-16LE","utf_7","U7","utf_8","U8","UTF","utf8"]


def force_to_unicode(text):
    """Helper function to force text string to unicode in case of encoding issues.

    Args:
        text (str): string text

    Returns:
        atext (string): Unicode formatted string.
    """

    try:
        return unicode(text)
    except Exception, e:
        try:
            return unicode(text.decode("utf-8"))
        except Exception, e:
            for encoding in KNOWN_ENCODINGS:
                try:
                    atext = unicode(text, encoding)
                    return atext
                except Exception, e:
                    pass
    raise Exception("Could not convert to unicode!")


def read_xlsx(filename):
    """Helper function to read the cluster definition stored in an Excel file.

        Args:
            filename (str): string text of the filename.

        Returns:
            cluster_listing (dict): A dictionary with emailaddresses as keys and a list of clusters (strings) as items.
        """

    rows = []
    row = {}
    header = {}
    z = zipfile.ZipFile(filename)

    # Get shared strings
    strings = [el.text for e, el in iterparse(z.open( 'xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    value = ''

    # Open specified worksheet
    for e, el in iterparse(z.open('xl/worksheets/sheet%d.xml' % 1)):
        # get value or index to shared strings
        if el.tag.endswith('}v'):                                   # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'):                                   # <c r="A3" t="s"><v>84</v></c>

            # If value is a shared string, use value as an index
            if el.attrib.get('t') == 's':
                value = strings[int(value)]

            # split the row/col information so that the row letter(s) can be separate
            letter = el.attrib['r']                                   # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]

            # if it is the first row, then create a header hash for the names
            # that COULD be used
            if rows == []:
                header[letter]= value
            else:
                if value != '':
                    # if there is a header row, use the first row's names as the row hash index
                    row[header[letter]] = value

            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    z.close()

    cluster_listing = {}
    for i in rows:
        if i != {}:
            if 'Employee.Email' in i:
                cluster_listing[i['Employee.Email']] = [j+":"+i[j].replace(' ','_') for j in i if j != 'Employee.Email' and i[j] != None]
    return cluster_listing

def __toTimeStamp(timestamp):
    return int(time.mktime(timestamp.timetuple()))


def timeToEpoch(ex_datetime):
    return __toTimeStamp(ex_datetime)

def removeSignature(text):
    if 'Met vriendelijke groet / Kind regards,' in text:
        text = text.split('Met vriendelijke groet / Kind regards,')[0]
    if '-------- Oorspronkelijk bericht --------' in text:
        text = text.split('-------- Oorspronkelijk bericht --------')[0]
    if 'Verzonden vanaf Samsung Mobile.' in text:
        text = text.split('Verzonden vanaf Samsung ')[0]
    if 'Verzonden vanaf mijn Samsung ':
        text = text.split('Verzonden vanaf mijn Samsung ')[0]
    return text

def removeHTML(text):
    try:
        while "<head>" in text:
            text = text.split("</head>", 1)[1]

        while "<script>" in text:
            i1 = text.index("<script>")
            i2 = text.index("</script>")
            if i2 > i1:
                t1 = text.split("<script>", 1)[0]
                t2 = text.split("</script>", 1)[1]
                text = t1 + " " + t2
            else:
                text = text.split("</script>", 1)[1]
        while "<style>" in text:
            i1 = text.index("<style>")
            i2 = text.index("</style>")
            if i2 > i1:
                t1 = text.split("<style>", 1)[0]
                t2 = text.split("</style>", 1)[1]
                text = t1 + " " + t2
            else:
                text = text.split("</style>", 1)[1]
    except:
        pass

    on = 1
    outtxt = ""
    for i in text:
        if i == "<":
            on = 0
        if on == 1:
            outtxt += i
        if i == ">":
            on = 1

    return urllib.unquote(outtxt)

def removeForwards(text):
    first_index = 10000000000000000

    patterns = ["----- Reply message -----",
                "Begin doorgestuurd bericht:",
                "Begin forwarded message:",
                "---------- Forwarded message ----------",
                "-------- Originele bericht --------",
                "-----Oorspronkelijk bericht-----",
                "-----Original Message",
                "----- Forwarded by ",
                "------Sent from"
                ]
    for i in patterns:
        if i in text:
            if text.index(i) < first_index:
                first_index = text.index(i)

    stext = text.split(" ")

    candidates = []
    a = 0
    text_index = 0
    for s in range(0, len(stext)):
        text_index += len(stext[s]) + 1
        for x in ["wrote:", "schreef:", "volgende:"]:
            if x in stext[s]:
                if s > 6:
                    year = False
                    date = False
                    for c in stext[(s - 6):s]:
                        if c.isdigit():
                            if (int(c) > 1) and (int(c) < 32):
                                date = True
                            if (int(c) > 1900) and (int(c) < 2050):
                                year = True
                        for splitters in ["-", "/"]:
                            for z in c.split(splitters):
                                if z.isdigit():
                                    if (int(z) > 1) and (int(z) < 32):
                                        date = True
                                    if (int(z) > 1900) and (int(z) < 2050):
                                        year = True
                    if (year == True) and (date == True):
                        if text_index < first_index:
                            first_index = text_index

        if a > 0:
            candidates.append(stext[s])
            a += 1
        if a > 10:
            year = False
            date = False
            for c in candidates:
                if c.isdigit():
                    if (int(c) > 1) and (int(c) < 32):
                        date = True
                    if (int(c) > 1900) and (int(c) < 2050):
                        year = True
                for splitters in ["-", "/"]:
                    for z in c.split(splitters):
                        if z.isdigit():
                            if (int(z) > 1) and (int(z) < 32):
                                date = True
                            if (int(z) > 1900) and (int(z) < 2050):
                                year = True
            if (year == True) and (date == True):
                if text_index < first_index:
                    first_index = text_index
            candidates = []
            a = 0
        if "@" in stext[s]:
            a = 1
            candidates.append(stext[s])

    if first_index != 10000000000000000:
        text = text[0:first_index]

    n_text = text.replace("\r\n", "\n")
    s_text = n_text.split("\n\n")

    if len(s_text) > 1:
        return "\n\n".join(s_text[:-1])
    else:
        return text