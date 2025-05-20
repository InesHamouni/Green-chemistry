<p align="center">
  <img src="assets/green.jpeg" alt="Project Logo" width="400"/>
</p>

<p align="center">
  <img src="assets/coverage-badge.svg" alt="Coverage Status"/>
</p>

<h1 align="center">
🌱 Green Chemistry 🌱
</h1>

<h2>
<strong>Using programming to reduce the Environmental and Human impact of Chemical Reactions, inspired by the 12 principles of Green Chemistry</strong>
</h2>

<br>

 
## 🧑‍🔬 Team
 
- Clara Veron
- Inès Hamouni 
- Thomas Cohen 
- Edward Vondoderer

## 📖 Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Usage](#-usage)
- [Installation](#-Setup)
- [Development installation](#-development-installation)
- [License](#-license)

## 🖊️ Introduction

Green Chemistry is a project based on chemical reaction sustainaility. In the context of growing environmental challenges and climate change, it is crucial for scientists to understand and minimize the ecological impact of their work. This tool is designed to raise awareness and support decision-making by evaluating the environmental and human impact of a given reaction—while also suggesting greener alternatives whenever possible. 
The project features an interactive Streamlit interface where users can input solvents, reactants, metal catalyst, products and reaction conditions (temperature and pressure). The interface output is then a summary of the reaction's environmental footprint. Green Chemistry is designed to evaluate all types of chemical reactions, however, the focus is put on coupling reactions, as they are among the most widely used transformations in chemistry. 
This project is inspired by the 12 principles of Green Chemistry. 

## 🌱 Features

This package allows users to: 

- Evaluates atom economy of their reaction 
- Estimate energy consumption based on temperature and pressure conditions
- Asses the toxicity of the metal catalyst used
- Identify GHS hazard pictograms for each compound involved
- Suggest greener alternatives when available to reduce environmental impact


## 🔥 Usage

```
git clone https://github.com/InesHamouni/Green-chemistry.git
cd Green-chemistry
conda env create -f env.yml
conda activate green_env
```

## 👩‍💻 Installation

Create a new environment, you may also give the environment a different name. 

```
conda create -n green_chemistry python=3.10 
```

```
conda activate green_chemistry
(conda_env) $ pip install .
```

If you need jupyter lab, install it 

```
(green_chemistry) $ pip install jupyterlab
```


## 🛠️ Development installation

Initialize Git (only for the first time). 

Note: You should have create an empty repository on `https://github.com:ineshamouni/Green-chemistry`.

```
git init
git add * 
git add .*
git commit -m "Initial commit" 
git branch -M main
git remote add origin git@github.com:ineshamouni/Green-chemistry.git 
git push -u origin main
```

Then add and commit changes as usual. 

To install the package, run

```
(green_chemistry) $ pip install -e ".[test,doc]"
```

### Run tests and coverage

(green_chemistry) $ pip install tox
(green_chemistry) $ tox



## 📖 Licence

This project is under the MIT licence.
The MIT License is a permissive open-source license that allows free use, modification, and distribution of the software. To have an overview of it, please refer to the LICENSE file included in the repository.

