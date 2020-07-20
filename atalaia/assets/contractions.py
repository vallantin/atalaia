contractions_pt_br = {
    # da, do, dos, deste, disso, daquilo...
    r'\b(D|d)(\')?(ele|el|est|este|aquel|aquele|ist|iss|ess|esse|aquil)?(a|o)?(s)?':'\\1e \\3\\4\\5',
    # na, no, nos, neste, nisso, naquilo...
    r'\bN(\')?(ele|el|est|este|aquel|aquele|ist|iss|ess|esse|aquil)?(a|o)?(s)?':'Em \\2\\3\\4',
    r'\bn(\')?(ele|el|est|este|aquel|aquele|ist|iss|ess|esse|aquil)?(a|o)?(s)?':'em \\2\\3\\4',
    # à
    r'\bà[\b]?':'a a',
    r'\bÀ[\b]?':'A a',
    # ao...
    r'\b(a|A)o(s)?\b':'\\1 o\\2',
    # não
    r'\b(n|N)\b':'\\1ão',
    # que
    r'\b(q|Q)\b':'\\1ue',
    # pra
    r'\b(p|P)ra\b':'\\1ara',
    r'\b(p|P)ras\b':'\\1ara as',
    r'\b(p|P)ro(s)\b':'\\1ara o\\2',
    # num, numa
    r'\bnum(a)?\b':'em um\\1',
    r'\bNum(a)?\b':'Em um\\1'
    }

contractions_fr ={    
    # l', d', j', n', t', m'
    r'\b(m|M|t|T|n|N|j|J|l|L|d|D)\'':'\\1e ',
    # du
    r'\b(D|d)u':'\\1e le',
    # au
    r'\bAu\b':'À le',
    r'\bau\b':'à le',
    # aux
    r'\bAux\b':'À les',
    r'\baux\b':'à les',
    # des
    r'\b(d|D)es':'\\1e les',
    # qu'
    r'\b(q|Q)u\'':'\\1ue ', 
}

contractions_en ={
    r'\'m\b':' am',
    r'\'re\b':' are',
    # can't, cannot...
    r'\b(c|C)an+[o]?[\']?t\b':'\\1an not',
    #shouldn't, couldn't
    r'\b(C|W|S)(h)?ouldn\'t\b':'\\1\\2ould not',
    r'\b(c|w|s)(h)?ouldn\'t\b':'\\1\\2ould not',
    # I amn't
    r'\b(a|A)mn\'t\b':'\\1m not',
    # ren't
    r'\b(a)?ren\'t\b':'are not',
    # is
    r'\b(s|S)?(H|h|i|I)(e|t)\'s\b':'\\1\\2\\3 is',
    # isn't
    r'\b(i|I)sn\'t\b':'\\1s not',
    # won't
    r'\b(w|W)on\'t\b':'\\1ill not',
    # needn't
    r'\b(n|N)eedn\'t\b':'\\1eed not',
    # haven't, hadn't, hasn't
    r'\b(h|H)a(ve|d|s)n\'t\b':'\\1a\\2 not',
    # ain't
    r'\b(a|A)in\'t\b':'\\1m not',
    # 've'
    r'\'ve\b':' have',
    # didn't, doesn't
    r'(d|D)(id|oes)n\'t':'\\1\\2 not',
    # 'll
    r'\'ll\b':' will',
    # 'd
    r'\'d\b':' would',
    # let's
    r'\b(l|L)et\'s\b':'\\1et us',
    # mayn't
    r'\b(m|M)ayn\'t\b':'\\1ay not',
    # may've
    r'\b(m|M)ay\'ve\b':'\\1ay have',
    # mightn't, mustn't 
    r'\b(m|M)(ight|ust)n\'t\b':'\\1\\2 not',
    # might've, must've
    r'\b(m|M)(ight|ust)\'ve\b':'\\1\\2 have',
    # shalln't
    r'\b(s|S)ha(ll)?n\'t\b':'\\1hall not',
}
