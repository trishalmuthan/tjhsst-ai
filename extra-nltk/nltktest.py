import nltk

from nltk.corpus import state_union

cfd = nltk.ConditionalFreqDist(
    (condition, fileid[:4])
    for fileid in state_union.fileids()
    for word in state_union.words(fileid)
    for condition in ['men', 'women', 'people']
    if word.lower().startswith(condition)
)

cfd.tabulate()
cfd.plot()