import ydf
from green_chemistry.file_regressor import tokenize, tokenizing, classify_regress
from green_chemistry import notebooks
model_1 = ydf.load_model("buchwald_classifier_1")
model_2 = ydf.load_model("buchwald_regressor_1")
model_name = "DeepChem/ChemBERTa-77M-MLM"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)
tokenizer = AutoTokenizer.from_pretrained(model_name)

sample=[c1ccccc1]
tokenized_sample=[]


data_all=["CC(C)C(C=C(C(C)C)C=C1C(C)C)=C1C2=C(P([C@@]3(C[C@@H]4C5)C[C@H](C4)C[C@H]5C3)[C@]6(C7)C[C@@H](C[C@@H]7C8)C[C@@H]8C6)C(OC)=CC=C2OC","CC1=CC(C)=NO1","CN(C)P(N(C)C)(N(C)C)=NP(N(C)C)(N(C)C)=NCC"]
data_aryl=["ClC1=NC=CC=C1"]

full_data_tokenized = tokenizing(data_all,data_aryl)

def test_classify_regress(full_data_tokenized):

    assert classify_regress(full_data) == float

#If the test works it should return a float, but it appears as the idf.loadmodel is creating some issues for pytest