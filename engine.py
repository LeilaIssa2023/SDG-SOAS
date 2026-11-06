"""Free, CPU-only explainable CLO-to-SDG rule engine. Python standard library only."""
import argparse,csv,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
def load(path=None):
    return json.loads(Path(path or HERE/'concept_rules.json').read_text())
def units(text):
    text=re.split(r"(?im)^\s*(?:Teaching/Learning Methods|Course Grading and Performance Criteria|RELATIONSHIP BETWEEN COURSE OUTCOMES|Assessment Methods)\s*$",text,maxsplit=1)[0]
    text=re.split(r"(?im)^\s*Honors Course Distinction\s*$",text,maxsplit=1)[0]
    # Segment by CLO numbering, newline, and sentence; never join evidence across unrelated CLOs.
    text=re.sub(r"(?i)\bCLO\s*\d+\s*[:.)-]?", "\n", text)
    return [x.strip() for x in re.split(r"\n+|(?<=[.!?])\s+(?=[A-Z])",text) if x.strip()]
def matched_terms(text,terms):
    hits=[]
    for term in terms:
        pat=r"(?<![a-z])"+re.escape(term.lower()).replace(r"\-",r"[- ]")+r"(?![a-z])"
        if re.search(pat,text.lower()):
            hits.append(term)
    return hits
def classify(text, config=None):
    config=config or load()
    found={}
    for idx,unit in enumerate(units(text)):
        detected={key:matched_terms(unit,terms) for key,terms in config['concepts'].items()}
        for rule in config['rules']:
            if all(detected[c] for c in rule['all_of']) and not any(detected[c] for c in rule['none_of']):
                if rule['sdg']==3 and re.search(r"(?i)illness narratives?|literary|creative.critical writing|representations? of illness",unit):
                    continue
                sdg=str(rule['sdg'])
                found.setdefault(sdg,[]).append({"rule":rule['id'],"description":rule['description'],
                  "unit_index":idx,"evidence":{c:detected[c] for c in rule['all_of']},"text":unit[:400]})
    return {"sdgs":sorted(map(int,found)),"matches":found,"review_required":True}
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--text')
    p.add_argument('--input-csv')
    p.add_argument('--text-column',default='clo_text')
    p.add_argument('--id-column',default='course')
    p.add_argument('--output-csv',default='predictions.csv')
    p.add_argument('--rules')
    a=p.parse_args()
    config=load(a.rules)
    if a.text is not None:
        print(json.dumps(classify(a.text,config),indent=2,ensure_ascii=False));return
    if not a.input_csv:p.error('Provide --text or --input-csv')
    with open(a.input_csv,encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    with open(a.output_csv,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['course','predicted_sdgs','evidence_json','review_required'])
        w.writeheader()
        for row in rows:
            out=classify(row[a.text_column],config)
            w.writerow({'course':row[a.id_column],'predicted_sdgs':';'.join(map(str,out['sdgs'])),
                        'evidence_json':json.dumps(out['matches'],ensure_ascii=False),
                        'review_required':'Yes'})
    print(f'Processed {len(rows)} records -> {a.output_csv}')
if __name__=='__main__':main()
