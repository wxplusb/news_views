import nltk
from nltk.corpus import stopwords
import pymorphy2

nltk.download("stopwords")
stopws = stopwords.words("russian")

morph = pymorphy2.MorphAnalyzer()


def lemmatize(token):
    return morph.normal_forms(token)[0]

# удаление стоп-слов, лематизация


def clean_by_word(text, do_lemma=False):
    tokens = []
    for token in text.split():
        if len(token) < 2:
            continue

        if do_lemma and ("а" <= token[0] <= "я") and ("а" <= token[-1] <= "я"):
            token = lemmatize(token)

        if token not in stopws:
            tokens.append(token)

    return " ".join(tokens)


def clean_text(text_col, do_lemma=False):
    # понижение регистра, удаление ссылок и знаков препинания
    text_col = text_col.str.lower()
    text_col = text_col.str.replace(r"http\S+", "", regex=True)
    text_col = text_col.str.replace("[^A-Za-zА-Яа-я]+", " ", regex=True)

    # удаление стоп-слов, опечаток, лематизация
    text_col = text_col.apply(clean_by_word, args=(do_lemma,))

    return text_col
