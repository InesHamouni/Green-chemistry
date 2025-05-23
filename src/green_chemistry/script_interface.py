# import the needed package
import streamlit as st
import urllib.parse
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# FOR THE PREDICTED YIELD
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#import ydf
#import torch
# model_name = "DeepChem/ChemBERTa-77M-MLM"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model_1 = ydf.load_model("buchwald_classifier_1")
# model_2 = ydf.load_model("buchwald_regressor_1")

# import our functions
from green_chemistry.atom_economy import atom_economy
from green_chemistry.temperature_efficiency import temperature_efficiency
from green_chemistry.pressure_efficiency import pressure_efficiency
from green_chemistry.metal_center import get_metal_impact
from green_chemistry.convert_svg_pictograms_html import render_svg
from green_chemistry.extraction_picto import get_pictos
#from green_chemistry.file_regressor import tokenize, tokenizing, classify_regress : is for prediction of yield

# allows the page to field all the space
st.markdown("""
    <style>
        .block-container {
            max-width: 100% !important;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Call of PubChem API
@st.cache_data
def query_pubchem_api(compound_name):
    # make a GET HTTP request to the PubChem API
    urlencode_compound_name = urllib.parse.quote(compound_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urlencode_compound_name}/property/MolecularFormula,MolecularWeight,Title,SMILES/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        return data["PropertyTable"]["Properties"][0] if "PropertyTable" in data else None
    else:
        return None

# function to add molecular formula from chemical name of reagent
def add_reagent(reagent_name):
    reagent_data = query_pubchem_api(reagent_name)

    print(reagent_data) # debugging
    
    if reagent_data:
        st.session_state.reagents.append(reagent_data)
        st.success(f"reagent '{reagent_name}' added!")
        return True

    else:
        st.error(f"Failed to fetch data for {reagent_name}")
        return False

# function to add molecular formula from chemical name of product
def add_product(product_name):
        product_data = query_pubchem_api(product_name)
        
        print(product_data) # debugging
        
        if product_data:
            st.session_state.product.append(product_data)
            st.success(f"Product '{product_name}' added!")
            return True

        else:
            st.error(f"Failed to fetch data for {product_name}")
            return False


# function to add molecular formula from chemical name of solvents
def add_solvents(solvents_name):
    solvents_data = query_pubchem_api(solvents_name)

    print(solvents_data) # debugging
    
    if solvents_data:
        st.session_state.solvents.append(solvents_data)
        st.success(f"Solvent '{solvents_name}' added!")
        return True
    else:
        st.error(f"Failed to fetch data for {solvents_name}")
        return False

# function to add molecular formula from chemical name of catalyzers
def add_catalyzer(catalyzer_name):
    catalyzer_data = query_pubchem_api(catalyzer_name)

    print(catalyzer_data) # debugging
    
    if catalyzer_data:
        st.session_state.catalyzer.append(catalyzer_data)
        st.success(f"Catalyzer '{catalyzer_name}' added!")
        return True
    else:
        st.error(f"Failed to fetch data for {catalyzer_name}")
        return False

# calculation function    
def analyze():
    """
    Performs a green chemistry analysis based on user-provided reagents, products,
    solvents, catalysts, temperature, and pressure (if available).

    It calculates the atom economy, analyzes the environmental impact of metal
    catalysts, assesses temperature and pressure efficiency, and retrieves
    safety pictograms for the reagents, products, solvents, and catalysts.

    Args:
        None. The function relies on the `st.session_state` to access the data.
        Specifically, it expects the following keys to be present in the session state:
            - "reagents": A list of dictionaries, where each dictionary represents a reagent
                           and may contain a "MolecularWeight" and "Title".
            - "product": A list of dictionaries, where each dictionary represents a product
                         and should contain a "MolecularWeight" and "Title".
            - "solvents": A list of dictionaries, where each dictionary represents a solvent
                          and may contain a "Title".
            - "catalyzer": A list of dictionaries, where each dictionary represents a catalyst
                           and may contain a "MolecularFormula" and "Title".
            - "temperature": A numerical value representing the reaction temperature.
            - "pressure": A numerical value representing the reaction pressure.

    Returns:
        dict or None: A dictionary containing the analysis results if successful,
                     otherwise None. The dictionary has the following keys:
            - "atom_economy": A string representing the atom economy value and its verdict.
            - "metal_analysis": A string summarizing the environmental impact of metal catalysts.
            - "temperature_efficiency": A string assessing the temperature efficiency.
            - "pressure_efficiency": A string assessing the pressure efficiency.
            - "reagents_pictos": A list of URLs of safety pictograms for the reagents.
            - "products_pictos": A list of URLs of safety pictograms for the products.
            - "solvents_pictos": A list of URLs of safety pictograms for the solvents.
            - "catalyzers_pictos": A list of URLs of safety pictograms for the catalysts.

        If there's an error (e.g., missing data, invalid input), it prints an error
        message using `st.error` and returns None.
    """
    
    # Ensure data is present
    reagents = st.session_state.get("reagents", [])
    products = st.session_state.get("product", [])
    solvents = st.session_state.get("solvents", [])
    catalyzers = st.session_state.get("catalyzer", [])
    temperature = st.session_state.get("temperature")

    if not reagents or not products:
        st.error("Please add at least one reagent and one product to perform analysis.")
        return None

    # Get molar masses of reagents (reactants)
    reactant_masses = [
        float(reagent.get("MolecularWeight"))
        for reagent in reagents
        if reagent.get("MolecularWeight") is not None
    ]

    # Get molar mass of the main product (assume first product)
    product_mass = float(products[0].get("MolecularWeight"))

    if not product_mass:
        st.error("Product mass not available.")
        return None
    
    try:
        atom_econ_value, atom_econ_verdict = atom_economy(product_mass, reactant_masses)

        # Apply get_metal_impact to each catalyzer
        metal_analysis_lines = []
        for metal_data in catalyzers:
            formula = metal_data.get('MolecularFormula')
            if formula:
                analysis = get_metal_impact(formula)
                if analysis and not analysis.startswith("No data"):

                    lines = analysis.split('\n')
                    metal_name = lines[0].replace('---', '').strip()

                    properties = '\n\n'.join(
                        f"*{line.split(':', 1)[0].strip()}*: {line.split(':', 1)[1].strip()}"
                        for line in lines[1:] if ':' in line
                    )
                    metal_analysis_lines.append(f"**{metal_name}**\n\n{properties}")

        metal_analysis_str = "\n\n".join(metal_analysis_lines) if metal_analysis_lines else "No metal catalyst data"

        temperature_assessment = None
        if temperature is not None:
            temperature_assessment = temperature_efficiency(temperature)

        pressure_assessment = None
        if pressure is not None:
            pressure_assessment = pressure_efficiency(pressure)

        
        # create empty list for pictos   
        reagents_urls = []
        solvents_urls = []
        products_urls = []
        catalyzers_urls = []

        # Get pictograms for reagents
        for reagent_data in reagents:
            reagent_name = reagent_data.get("Title")
            if reagent_name:
                reagents_urls.extend(get_pictos(reagent_name))
            

        # Get pictograms for products
        for product_data in products:
            product_name = product_data.get("Title")
            if product_name:
                products_urls.extend(get_pictos(product_name))

        # Get pictograms for solvents
        for solvent_data in solvents:
            solvent_name = solvent_data.get("Title")
            if solvent_name:
                solvents_urls.extend(get_pictos(solvent_name))

        # Get pictograms for catalyzers
        for catalyzer_data in catalyzers:
            catalyzer_name = catalyzer_data.get("Title")
            if catalyzer_name:
                catalyzers_urls.extend(get_pictos(catalyzer_name))

#Getting all da SMILES
        reagent_smiles=[]
        solvent_smiles=[]
        for reagent_data in reagents:
            reagent_smile = reagent_data.get("SMILES")
            if reagent_smile:
                reagent_smiles.append(reagent_smile)
        for solvent_data in solvents:
            solvent_smile = solvent_data.get("SMILES")
            if solvent_smile:
                solvent_smiles.append(solvent_smile)

#Treating the SMILES data : is for prediction of yield
        # reagent_tokens, solvent_tokens = tokenizing(reagent_smiles, solvent_smiles)
        # predicted_yield=classify_regress(reagent_tokens, solvent_tokens)


    except ValueError as e:
        st.error(str(e))
        return None

    st.success("Analysis complete!")

    return {
        "atom_economy": f"{atom_econ_value}% - {atom_econ_verdict}",
        "metal_analysis": metal_analysis_str,
        "temperature_efficiency": temperature_assessment,
        "pressure_efficiency": pressure_assessment,
        "reagents_pictos": reagents_urls,
        "products_pictos": products_urls,
        "solvents_pictos": solvents_urls,
        "catalyzers_pictos": catalyzers_urls,
        #"predicted_yield": predicted_yield : is for prediction of yield
    }

#SET-UP of THE STREAMLIT INTERFACE

with st.container():
    col1, spacer1, col2, spacer2, col3 = st.columns([1.2, 0.1, 1.2, 0.1, 1.2])
# reagent addition in first column
    with col1:
        st.write("# Reagents")

        if "reagents" not in st.session_state:
            st.session_state.reagents = []
            st.write("No reagents found. Please add some reagents.")
        else:    
            for reagent in st.session_state.reagents:
                st.write(reagent.get("MolecularFormula"))
            if st.button("Remove Reagents"):
                st.session_state.reagents.pop()
                st.rerun() 

        st.text_input("Enter reagent name", key="reagent_name")
        if st.button("Add Reagent"):
            reagent_name = st.session_state.reagent_name
            ret = add_reagent(reagent_name)
            if ret: st.rerun()

        #Product list
        st.write("# Products")

        if "product" not in st.session_state:
            st.session_state.product = []
            st.write("No products found. Please add some products.")
        else:    
            for product in st.session_state.product:
                st.write(product.get("MolecularFormula"))
            if st.button("Remove Product"):
                st.session_state.product.pop()
                st.rerun()            

        st.text_input("Enter product name", key="product_name")
        if st.button("Add Product"):
            product_name = st.session_state.product_name
            ret = add_product(product_name)
            if ret: st.rerun()

        

# solvent addition in the interface in the second column
    with col2:
        st.write('# Solvents / Auxiliaries')
        if "solvents" not in st.session_state:
            st.session_state.solvents = []
            st.write("No solvents/auxiliaries found. Please add some solvents.")
        else:    
            for solvent in st.session_state.solvents:
                st.write(solvent.get("MolecularFormula"))
            if st.button("Remove Solvent/Auxiliaries"):
                st.session_state.solvents.pop()
                st.rerun() 

        st.text_input("Enter solvents/auxiliaries name", key="solvents_name")
        if st.button("Add Solvents/Auxiliaries"):
            solvents_name = st.session_state.solvents_name
            ret = add_solvents(solvents_name)
            if ret: st.rerun()


    # catalyzer addition in the interface in the second column        
        st.write('# Catalyzers')
        if "catalyzer" not in st.session_state:
            st.session_state.catalyzer = []
            st.write("No catalyzer found. Please add some catalyzers.")
        else:
            for catalyzer in st.session_state.catalyzer:
                st.write(catalyzer.get("MolecularFormula"))
                if st.button("Remove Catalyzer"):
                    st.session_state.catalyzer.pop()
                    st.rerun()
                           
        st.text_input("Enter metal center name", key="catalyzer_name")
        if st.button("Add Catalyzer"):
            catalyzer_name = st.session_state.catalyzer_name
            ret = add_catalyzer(catalyzer_name)
            if ret: st.rerun()

# addition of conditions
    with col3:
        st.write('# Conditions') 
        temp = st.slider("Temperature (°C)", -100, 300, 25)
        pressure = st.slider("Pressure (bar)", 0, 50, 1)
        st.session_state.temperature = temp
        st.session_state.pressure = pressure

        st.markdown("## ")

        with st.container():
            col_left, col_center, col_right = st.columns([1, 1, 1])
            with col_center:
                if st.button("RUN ANALYSIS", key="run_analysis", help="Click to start analysis", type="primary"):
                    result = analyze()
                    st.session_state.result = result
                    st.rerun()

st.markdown("---")

with st.container():
    st.write("# Analysis results")
    result = st.session_state.get("result")

    if result:
        if "atom_economy" in result:
            st.write(f"**Atom Economy:** {result['atom_economy']}")

        if "metal_analysis" in result:
            st.markdown(f"**Catalyst Metal Analysis:** {result['metal_analysis']}")

        # for prediction of yield
        # if "predicted_yield" in result:
        #     st.write(f"**Yield:** {result['predicted_yield']}")

        if "temperature_efficiency" in result and result["temperature_efficiency"]:
            st.write(f"**Temperature conditions:** {result['temperature_efficiency']}")

        if "pressure_efficiency" in result and result["pressure_efficiency"]:
            st.write(f"**Pressure conditions:** {result['pressure_efficiency']}")
    
        st.write("## Hazard Pictograms")
        if "reagents_pictos" in result and st.session_state.get("reagents"):
            st.subheader("reagents Hazard Pictograms")
            reagent_names = [c.get("Title") for c in st.session_state["reagents"]]
            reagent_pictos = result["reagents_pictos"]

            step = len(reagent_pictos) // len(reagent_names) if reagent_names else 0

            for i, name in enumerate(reagent_names):
                st.markdown(f"**{name}**")
                reagent_svg_list = reagent_pictos[i*step:(i+1)*step]
                render_svg(reagent_svg_list)
        else:
            st.info("reagent names don't have hazard pictograms.")

        
        
        if "products_pictos" in result and st.session_state.get("product"):
            st.subheader("Products Hazard Pictograms")
            product_names = [p.get("Title") for p in st.session_state["product"]]
            product_pictos = result["products_pictos"]

            step = len(product_pictos) // len(product_names) if product_names else 0

            for i, name in enumerate(product_names):
                st.markdown(f"**{name}**")
                product_svg_list = product_pictos[i*step:(i+1)*step]
                render_svg(product_svg_list)
        else:
            st.info("Product names don't have hazard pictograms.")
        
        if "solvents_pictos" in result and st.session_state.get("solvents"):
            st.subheader("Solvents Hazard Pictograms")
            solvent_names = [s.get("Title") for s in st.session_state["solvents"]]
            solvent_pictos = result["solvents_pictos"]

            step = len(solvent_pictos) // len(solvent_names) if solvent_names else 0

            for i, name in enumerate(solvent_names):
                st.markdown(f"**{name}**")
                solvent_svg_list = solvent_pictos[i*step:(i+1)*step]
                render_svg(solvent_svg_list)
        else:
            st.info("Solvent names don't have hazard pictograms.")

        if "catalyzers_pictos" in result and st.session_state.get("catalyzer"):
            st.subheader("Catalyzers Hazard Pictograms")
            catalyzer_names = [c.get("Title") for c in st.session_state["catalyzer"]]
            catalyzer_pictos = result["catalyzers_pictos"]

            step = len(catalyzer_pictos) // len(catalyzer_names) if catalyzer_names else 0

            for i, name in enumerate(catalyzer_names):
                st.markdown(f"**{name}**")
                catalyzer_svg_list = catalyzer_pictos[i*step:(i+1)*step]
                render_svg(catalyzer_svg_list)
        else:
            st.info("Catalyzer names don't have hazard pictograms.")



    else:
        st.write("No analysis results available.")

