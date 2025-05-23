import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import ydf
import matplotlib.pyplot as plt
import pandas as pd


all_ds = pd.read_csv("Data_Training/data_to_train_classifier.csv")

# This splits the data into a 90/10 percent split
all_ds = all_ds.sample(frac=1)
split_idx = len(all_ds) * 9// 10
train_ds = all_ds.iloc[:split_idx]
test_ds = all_ds.iloc[split_idx:]


#this is the model from ydf library
model = ydf.GradientBoostedTreesLearner(label="molecule_class",
                                task=ydf.Task.CLASSIFICATION).train(train_ds)

#Model first evaluation
evaluation = model.evaluate(test_ds)
pred=model.predict(test_ds)
real=test_ds["SMILES"]

plt.show()
print(evaluation)


# Saving model with wanted name
model.save("buchwald_classifier_1")