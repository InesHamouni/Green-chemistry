import streamlit as st
import urllib.parse
import requests

@st.cache_data
def query_pubchem_api(compound_name):
    # make a GET HTTP request to the PubChem API
    urlencode_compound_name = urllib.parse.quote(compound_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urlencode_compound_name}/property/MolecularFormula,Title/JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        
        return data["PropertyTable"]["Properties"][0] if "PropertyTable" in data else None
    else:
        st.error(f"Error fetching data for {compound_name}: {response.status_code}")
        return None

# function to add compound name and get property
def add_compound(compound_name):
    compound_data = query_pubchem_api(compound_name)

    print(compound_data) # debugging
    
    if compound_data:
        st.session_state.compounds.append(compound_data)
        st.success(f"Compound '{compound_name}' added!")

    else:
        st.error(f"Failed to fetch data for {compound_name}")

# function to add solvant name and get property
def add_solvants(solvants_name):
    solvants_data = query_pubchem_api(solvants_name)

    print(solvants_data) # debugging
    
    if solvants_data:
        st.session_state.solvants.append(solvants_data)
        st.success(f"Compound '{solvants_name}' added!")
    else:
        st.error(f"Failed to fetch data for {solvants_name}")

# function to add catalyzer name and get property
def add_catalyzer(catalyzer_name):
    catalyzer_data = query_pubchem_api(catalyzer_name)

    print(catalyzer_data) # debugging
    
    if catalyzer_data:
        st.session_state.catalyzer.append(catalyzer_data)
        st.success(f"Compound '{catalyzer_name}' added!")
    else:
        st.error(f"Failed to fetch data for {catalyzer_name}")
    
def analyze():
    # Placeholder for analysis logic
    st.success("Analysis complete!")
    analyze_results = {
        "toxicity": "Low",
        "atom_economy": "High",
    }
    return analyze_results

with st.container():
    col1, col2, col3 = st.columns(3)

# compound addition in first column
    with col1:
        st.write("# Compound list")

        if "compounds" not in st.session_state:
            st.session_state.compounds = []
            st.write("No compounds found. Please add some compounds.")
        else:    
            for compound in st.session_state.compounds:
                st.write(compound.get("MolecularFormula"))

        st.text_input("Enter compound name", key="compound_name")
        if st.button("Add Compound"):
            compound_name = st.session_state.compound_name
            add_compound(compound_name)
            st.rerun()

# solvent addition in the interface in the second column
    with col2:
        st.write('# Solvants')
        if "solvants" not in st.session_state:
            st.session_state.solvants = []
            st.write("No solvants found. Please add some solvants.")
        else:    
            for solvants in st.session_state.solvants:
                st.write(solvants.get("MolecularFormula"))

        st.text_input("Enter solvants name", key="solvants_name")
        if st.button("Add Solvants"):
            solvants_name = st.session_state.solvants_name
            add_solvants(solvants_name)
            st.rerun()
        
            None

    # catalyzer addition in the interface in the second column        
        st.write('# Catalyzers')
        if "catalyzer" not in st.session_state:
            st.session_state.catalyzer = []
            st.write("No catalyzer found. Please add some catalyzers.")
        else:
            for catalyzer in st.session_state.catalyzer:
                st.write(catalyzer.get("MolecularFormula"))
                           
        st.text_input("Enter metal center name", key="catalyzer_name")
        if st.button("Add Catalyzer"):
            catalyzer_name = st.session_state.catalyzer_name
            add_catalyzer(catalyzer_name)
            st.rerun()

# addition of conditions
    with col3:
        st.write('# Conditions') 
        temp = st.slider("Temperature (°C)", 0, 300, 25)
        pressure = st.slider("Pressure (bar)", 0, 50, 1)
        if (st.button("Run Analysis")):
            result = analyze()
            st.session_state.result = result
            st.rerun()
 
with st.container():
    st.write("# Analysis results")
    result = st.session_state.get("result")
    if result:
        st.write(f"Toxicity: {result['toxicity']}")
        st.write(f"Atom Economy: {result['atom_economy']}")
    else:
        st.write("No analysis results available.")
