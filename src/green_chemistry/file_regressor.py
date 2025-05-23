import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import ydf
model_1 = ydf.load_model("buchwald_classifier_1")
model_2 = ydf.load_model("buchwald_regressor_1")
model_name = "DeepChem/ChemBERTa-77M-MLM"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#this tokenizes the incoming smiles
def tokenize(smiles):

    token_ids = tokenizer.encode(
        smiles,
        padding=False,
        truncation=False,
    )
    token_str = " ".join(map(str, token_ids))

    return (token_str)
#This function can tokenize the whole smile list
def tokenizing (reagent_smiles,solvent_smiles):

    reagent_tokens=[]
    for reagent in reagent_smiles:
        reagent_tokens.append(tokenize(reagent))

    solvent_tokens=[]
    for solvent in solvent_smiles:
        solvent_tokens.append(tokenize(solvent))

    return(reagent_tokens, solvent_tokens)

#This function takes our tokens classifies them as (Base,Ligand,Additive or Aryldahide) and returns the yield value
def classify_regress(reagent_tokens, solvent_tokens):
    ligand_list = []
    additive_list = []
    base_list = []
    for solvent in solvent_tokens:

        real = pd.DataFrame({
            "SMILES": [solvent],
        }, dtype=str)
        pred = model_1.predict_class(real)

        if pred == 'Ligand':
            ligand_list.append(solvent)
        elif pred == 'Additive':
            additive_list.append(solvent)
        elif pred == 'Base':
            base_list.append(solvent)

    if not ligand_list and len(additive_list) > 1:
        ligand_list.append(additive_list[1])
    else:
        ligand_list = [""]


    if base_list:
        base_list = [base_list[0]]
    elif len(additive_list) > 2:
        base_list = [additive_list[2]]
    else:
        base_list = [""]

    data_for_regression = pd.DataFrame({
        "Ligand": ligand_list,
        "Additive": additive_list[0],
        "Base": base_list,
        "Arylhalide": reagent_tokens,
    }, dtype=str)
    predicted_yield = model_2.predict(data_for_regression)
    return (predicted_yield)



