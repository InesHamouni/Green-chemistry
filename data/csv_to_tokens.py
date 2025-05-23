import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification


model_name = "DeepChem/ChemBERTa-77M-MLM"
tokenizer = AutoTokenizer.from_pretrained(model_name)

#this code covnverts
def tokenize_csv(data, low_lim, high_lim, pad, trunc, max_len):
    df = pd.read_csv(data)
    df = df.iloc[:, low_lim:high_lim]
    for col in df.columns:
        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .apply(lambda x: " ".join(
                map(str, tokenizer.encode(
                    x,
                    padding="max_length" if pad else False,
                    truncation=trunc,
                    max_length=max_len
                ))
            ))
        )

    new_name = data.rsplit('.', 1)[0] + "_tokenized.csv"
    df.to_csv(new_name, index=False)
    return new_name



tokenize_csv('buchwald_hartwig_components.csv',0,3,False,False,0)