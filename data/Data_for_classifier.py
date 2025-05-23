import pandas as pd
#This file is to convert my smiles files into a 2 colum file so i can the train the classifier


df=pd.read_csv('Data_Training/buchwald_hartwig_components_tokenized.csv')
#removing yield
df_useful=df[['Ligand','Additive','Base']]


#adding the smiles into 1 colum
df_useful_1=df_useful.melt(
                         value_vars=['Ligand','Additive','Base'],
                         value_name='SMILES',
                         var_name='molecule_class')


#checking everything worked realised there not that many unique points in this data set so need to add new bases and ligands

df_useful_1=df_useful_1.drop_duplicates(subset=['SMILES'])
print("Unique SMILES:", df_useful_1['SMILES'].nunique())

#Saving my new file
df_useful_1.to_csv('data_to_train_classifier.csv',index=False)










