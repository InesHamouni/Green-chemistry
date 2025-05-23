from transformers import AutoTokenizer, AutoModelForSequenceClassification


model_name = "DeepChem/ChemBERTa-77M-MLM"

tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(smiles):
    token=tokenizer.encode(
        smiles,
        padding=False,
        truncation=False,)


    return(token)