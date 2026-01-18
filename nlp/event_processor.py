from typing import List, Dict
import spacy

nlp=spacy.load("en_core_web_sm")

def process_events(text: str)->List[Dict]:
    doc=nlp(text)
    events=[]

    UP_VERBS={"rise", "increase", "grow", "climb", "surge"}
    DOWN_VERBS={"fall", "decrease", "drop", "decline", "plunge"}

    for sent in doc.sents:
        sent_doc=nlp(sent.text)
        event={}

        root_verb=None
        for token in sent_doc:
            if token.dep_ =="ROOT":
                root_verb=token
                break

        if root_verb is None:
            continue

        if root_verb.lemma_ in UP_VERBS:
            event["direction"]="UP"
        elif root_verb.lemma_ in DOWN_VERBS:
            event["direction"]="DOWN"
        else:
            continue

        for token in sent_doc:
            if token.dep_ in ("nsubj", "nsubjpass") and token.head== root_verb:
                event["metric"]=token.text
                break

        for ent in sent_doc.ents:
            if ent.label_ in ("PERCENT", "MONEY", "QUANTITY"):
                event["value"]=ent.text
            if ent.label_ == "DATE":
                event["time"]=ent.text

        event["sentence"]=sent.text.strip()

        if "metric" in event:
            events.append(event)

    return events


# text="""
# US CPI rose 3.4% in December.
# European inflation fell last month.
# Markets reacted cautiously.
# """

# print(process_events(text))
