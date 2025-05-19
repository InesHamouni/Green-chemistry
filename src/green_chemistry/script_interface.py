import streamlit as st
import urllib.parse
import requests

# import of our functions
from atom_economy import atom_economy
from temperature_efficiency import temperature_efficiency
from pressure_efficiency import pressure_efficiency
from metal_center import get_metal_impact
from convert_pictograms import render_svg
from picto import get_pictos

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


@st.cache_data
def query_pubchem_api(compound_name):
    # make a GET HTTP request to the PubChem API
    urlencode_compound_name = urllib.parse.quote(compound_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urlencode_compound_name}/property/MolecularFormula,MolecularWeight,Title/JSON"
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

# function to add product name and get property
def add_product(product_name):
        product_data = query_pubchem_api(product_name)
        
        print(product_data) # debugging
        
        if product_data:
            st.session_state.product.append(product_data)
            st.success(f"Product '{product_name}' added!")

        else:
            st.error(f"Failed to fetch data for {product_name}")


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

# calculation function    
def analyze():
    # Ensure data is present
    compounds = st.session_state.get("compounds", [])
    products = st.session_state.get("product", [])
    solvants = st.session_state.get("solvants", [])
    catalyzers = st.session_state.get("catalyzer", [])
    temperature = st.session_state.get("temperature")

    if not compounds or not products:
        st.error("Please add at least one compound and one product to perform analysis.")
        return None

    # Get molar masses of compounds (reactants)
    reactant_masses = [
        float(compound.get("MolecularWeight"))
        for compound in compounds
        if compound.get("MolecularWeight") is not None
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
                    # Nettoyage et formatage en une ligne
                    lines = analysis.split('\n')
                    metal_name = lines[0].replace('---', '').strip()
                    properties = ' | '.join(
                        f"{line.split(':')[0].strip()}: {line.split(':')[1].strip()}" 
                        for line in lines[1:] if ':' in line
                    )
                    metal_analysis_lines.append(f"{metal_name}{properties}")
        
        metal_analysis_str = " | ".join(metal_analysis_lines) if metal_analysis_lines else "No metal catalyst data"

        temperature_assessment = None
        if temperature is not None:
            temperature_assessment = temperature_efficiency(temperature)

        pressure_assessment = None
        if pressure is not None:
            pressure_assessment = pressure_efficiency(pressure)

        
        # create empty list for pictos   
        compounds_urls = []
        solvants_urls = []
        products_urls = []
        catalyzers_urls = []

        # Get pictograms for compounds
        for compound_data in compounds:
            compound_name = compound_data.get("Title")
            if compound_name:
                compounds_urls.extend(get_pictos(compound_name))
            

        # Get pictograms for products
        for product_data in products:
            product_name = product_data.get("Title")
            if product_name:
                products_urls.extend(get_pictos(product_name))

        # Get pictograms for solvents
        for solvant_data in solvants:
            solvant_name = solvant_data.get("Title")
            if solvant_name:
                solvants_urls.extend(get_pictos(solvant_name))

        # Get pictograms for catalyzers
        for catalyzer_data in catalyzers:
            catalyzer_name = catalyzer_data.get("Title")
            if catalyzer_name:
                catalyzers_urls.extend(get_pictos(catalyzer_name))


    except ValueError as e:
        st.error(str(e))
        return None

    st.success("Analysis complete!")

    return {
        "atom_economy": f"{atom_econ_value}% - {atom_econ_verdict}",
        "metal_analysis": metal_analysis_str,
        "temperature_efficiency": temperature_assessment,
        "pressure_efficiency": pressure_assessment,
        "compounds_pictos": compounds_urls,
        "products_pictos": products_urls,
        "solvants_pictos": solvants_urls,
        "catalyzers_pictos": catalyzers_urls,
    }


with st.container():
    col1, spacer1, col2, spacer2, col3 = st.columns([1.2, 0.1, 1.2, 0.1, 1.2])
# compound addition in first column
    with col1:
        st.write("# Compounds")

        if "compounds" not in st.session_state:
            st.session_state.compounds = []
            st.write("No compounds found. Please add some compounds.")
        else:    
            for compound in st.session_state.compounds:
                st.write(compound.get("MolecularFormula"))
            if st.button("Remove compound"):
                st.session_state.compounds.pop()
                st.rerun() 

        st.text_input("Enter compound name", key="compound_name")
        if st.button("Add Compound"):
            compound_name = st.session_state.compound_name
            add_compound(compound_name)
            st.rerun()

        #Product list
        st.write("# Products")

        if "product" not in st.session_state:
            st.session_state.product = []
            st.write("No products found. Please add some products.")
        else:    
            for product in st.session_state.product:
                st.write(product.get("MolecularFormula"))
            if st.button("Remove product"):
                st.session_state.product.pop()
                st.rerun()            

        st.text_input("Enter product name", key="product_name")
        if st.button("Add Product"):
            product_name = st.session_state.product_name
            add_product(product_name)
            st.rerun()

        

# solvent addition in the interface in the second column
    with col2:
        st.write('# Solvents / Auxiliaries')
        if "solvants" not in st.session_state:
            st.session_state.solvants = []
            st.write("No solvents found. Please add some solvents.")
        else:    
            for solvant in st.session_state.solvants:
                st.write(solvant.get("MolecularFormula"))
            if st.button("Remove solvent"):
                st.session_state.solvant.pop()
                st.rerun() 

        st.text_input("Enter solvents name", key="solvants_name")
        if st.button("Add Solvaents"):
            solvants_name = st.session_state.solvants_name
            add_solvants(solvants_name)
            st.rerun()


    # catalyzer addition in the interface in the second column        
        st.write('# Catalyzers')
        if "catalyzer" not in st.session_state:
            st.session_state.catalyzer = []
            st.write("No catalyzer found. Please add some catalyzers.")
        else:
            for catalyzer in st.session_state.catalyzer:
                st.write(catalyzer.get("MolecularFormula"))
                if st.button("Remove catalyzer"):
                    st.session_state.catalyzer.pop()
                    st.rerun()
                           
        st.text_input("Enter metal center name", key="catalyzer_name")
        if st.button("Add Catalyzer"):
            catalyzer_name = st.session_state.catalyzer_name
            add_catalyzer(catalyzer_name)
            st.rerun()

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

        if "temperature_efficiency" in result and result["temperature_efficiency"]:
            st.write(f"**Temperature conditions:** {result['temperature_efficiency']}")

        if "pressure_efficiency" in result and result["pressure_efficiency"]:
            st.write(f"**Pressure conditions:** {result['pressure_efficiency']}")
    
        st.write("## Hazard Pictograms")
        if "compounds_pictos" in result:
            st.subheader("Compounds Hazard Pictograms")
            render_svg(result["compounds_pictos"])
        else:
            st.info(f"Compound name doesn't have hazard pictograms")
        
        if "products_pictos" in result:
            st.subheader("Products Hazard Pictograms")
            render_svg(result["products_pictos"])
        else:
            st.info(f"Product name doesn't have hazard pictograms")
        
        if "solvants_pictos" in result:
            st.subheader("Solvents Hazard Pictograms")
            render_svg(result["solvants_pictos"])
        else:
            st.info(f"Solvent name doesn't have hazard pictograms")
        
        if "catalyzers_pictos" in result:
            st.subheader("Catalyzers Hazard Pictograms")
            render_svg(result["catalyzers_pictos"])
        else:
            st.info(f"Catalyzer name doesn't have hazard pictograms")

    else:
        st.write("No analysis results available.")

