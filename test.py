import spacy

nlp = spacy.load("en_core_web_sm")

text = "US CPI rose 3.4% in December, exceeding market expectations."

doc = nlp(text)

print("Text:", text)


#tokens
for token in doc:
    print(
        f"{token.text:<12} "
        f"POS={token.pos_:<6} "
        f"DEP={token.dep_:<8} "
        f"HEAD={token.head.text}"
    )
print("\nsentences")


for sent in doc.sents:
    print(sent.text)
print("\nentities")


for ent in doc.ents:
    print(ent.text, "->", ent.label_)
print("\nverb root")


for token in doc:
    if token.dep_ == "ROOT":
        print("root:", token.text, "| lemma:", token.lemma_)
print("\nsubjects")


for token in doc:
    if token.dep_ in ("nsubj", "nsubjpass"):
        print("subj:", token.text)
