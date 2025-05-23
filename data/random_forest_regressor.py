

import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import ydf
import matplotlib.pyplot as plt
import pandas as pd


model_name = "DeepChem/ChemBERTa-77M-MLM"
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1)
tokenizer = AutoTokenizer.from_pretrained(model_name)




# Download a classification dataset and load it as a Pandas DataFrame.
all_ds = pd.read_csv("Data_Training/Dreher_and_Doyle_tokenized_data.csv")

# This splits the data into a 90/10 percent split
all_ds = all_ds.sample(frac=1)
split_idx = len(all_ds) * 9// 10
train_ds = all_ds.iloc[:split_idx]
test_ds = all_ds.iloc[split_idx:]

# Print the first 5 training examples
print(train_ds.head(5))

#this is the model from ydf library
model = ydf.GradientBoostedTreesLearner(label="Yield",
                                task=ydf.Task.REGRESSION).train(train_ds)

#Model first evaluation
evaluation = model.evaluate(test_ds)
pred=model.predict(test_ds)
real=test_ds["Yield"]



#Plotting of the results
fig, ax = plt.subplots(figsize=(6,6))



ax.scatter(
    real, pred,
    s=40,           # marker size
    alpha=0.6,      # transparency
    edgecolor="w",  # white edge so points “pop”
    linewidth=0.5
)


lims = [
    np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
    np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
]
ax.plot(lims, lims, '--', color='gray', linewidth=1)
ax.set_xlim(lims)
ax.set_ylim(lims)

# Titles
ax.set_xlabel("Real yield (%)", fontsize=12, labelpad=8)
ax.set_ylabel("Predicted yield (%)", fontsize=12, labelpad=8)
ax.set_title("Predicted vs. Real Yields", fontsize=14, pad=12)

# Grid
ax.grid(True, linestyle='--', alpha=0.5)
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1)


plt.tight_layout()

plt.show()
print(evaluation)


# Saving model with wanted name
model.save("buchwald_regressor_1")