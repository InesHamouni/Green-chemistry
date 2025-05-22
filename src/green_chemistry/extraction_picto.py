import requests
import json

def get_hazard_from_pugview_data(compound_name: str):
    """
    Retrieves data from PubChem for a given chemical compound.

    Args:
        compound_name (str): The name of the chemical compound.       

    Returns:
        Json : A Json containing the requested data, or None if an error occurs.
              The Json structure depends on the data_type.
              If data_type is 'Hazard', returns a list of hazard statements
              under the key 'Hazard Statements'.
    """
    # Construct the API URL.  We'll use PUG REST.
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/"
    # Use 'name' as the identifier type, and specify JSON as the output format.
    url = f"{base_url}name/{compound_name}/property/CanonicalSMILES,MolecularFormula/JSON"

    try:
        # Send the API request.
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        # Extract relevant information
        if 'PropertyTable' in data and 'Properties' in data['PropertyTable']:
            properties = data['PropertyTable']['Properties'][0]

            # Fetch safety and hazard information using PUG View
            url_safety = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{properties['CID']}/JSON?heading=Safety+and+Hazards"
            response_safety = requests.get(url_safety)
            response_safety.raise_for_status()
            safety_data = response_safety.json()

            # Extract hazard statements
            hazard_statements = []
            if (safety_data and
                'Record' in safety_data and
                'Section' in safety_data['Record'] and
                len(safety_data['Record']['Section']) > 0):

                for section in safety_data['Record']['Section'][0]['Section']:
                    if section.get('TOCHeading') == 'Hazards Identification':
                        for subsection in section.get('Section', []):  # Iterate subsections, handle missing key
                            if subsection.get('TOCHeading') == 'GHS Classification':
                                for phrase in subsection.get('Information', []):
                                    if phrase.get('Name') == 'Pictogram(s)':
                                        hazard_statements.extend(phrase.get('Value').get('StringWithMarkup', ''))
                                    
                                        # break # Exit the phrase loop
                                break # Exit the subsection loop
                        break # Exit the section loop

            return hazard_statements

        else:
            return {'Error': 'Compound not found in PubChem'}

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {'Error': f'Request failed: {e}'}
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from PubChem")
        return {'Error': 'Invalid JSON response from PubChem'}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {'Error': f'An unexpected error occurred: {e}'}
    

def extract_pictogram_urls(hazard_data: json):
    """
    Extracts unique pictogram URLs from the PubChem hazard data.

    Args:
        hazard_data (json): The JSON data containing hazard information.

    Returns:
        list: A list of unique pictogram URLs.
    """
    unique_urls = set()
    if isinstance(hazard_data, list):
        for item in hazard_data:
            if isinstance(item, dict) and 'Markup' in item:
                for markup in item['Markup']:
                    if isinstance(markup, dict) and 'URL' in markup:
                        unique_urls.add(markup['URL'])
    elif isinstance(hazard_data, dict) and 'Error' in hazard_data:
        print(f"Error: {hazard_data['Error']}")
    else:
        print("Warning: Unexpected hazard data format.")
    return list(unique_urls)


def get_pictos(compound_name: str):

    """ 
    Retrieves hazard pictogram URLs for a given chemical compound.

    This function fetches hazard data using `get_hazard_from_pugview_data()`, then
    extracts the pictogram image URLs using `extract_pictogram_urls()` and stores 
    them in a list.

    Args:
        compound_name (str): The name of the chemical compound (e.g., "lead").

    Returns:
        list: A list of strings representing the URLs of the hazard pictograms.  
    
    """

    hazard_data = get_hazard_from_pugview_data(compound_name)
    pictogram_urls = []
    if hazard_data and 'Error' not in hazard_data:
        print(f"Compound: {compound_name}")
        print("Hazard Statements:")
        print(f"Safety and Hazards: {json.dumps(hazard_data, indent=4)}")

        # Extract URLs
        pictogram_urls = extract_pictogram_urls(hazard_data)
        if pictogram_urls:
            print("\nExtracted Unique Pictogram URLs:")
            for url in pictogram_urls:
                print(url)
        else:
            print("\nNo pictogram URLs found.")
    elif hazard_data:
        print(f"Error: {hazard_data['Error']}")

    return pictogram_urls

# test for function
if __name__ == "__main__":
    get_pictos("lead")