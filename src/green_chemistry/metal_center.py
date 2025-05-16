def get_metal_impact(metal):
    """
       Returns toxicity and environmental impact information for metals used mostly in cross-coupling reaction.


        One of the twelve principles of green chemistry is the use of catalytic processes.
        The principle is to achieve more efficient reactions using catalysts.
        If metals are used as catalysts, the metal centers must be as non-toxic as possible and non-persistent for the environment.
        The rarity and price of the metal also play an important role: the rarer the metal, the more difficult and environmentally polluting it is to extract.

           Args:
               metal (str): The chemical symbol of the metal center

           Returns:
               Toxicity of the metal : low, moderate or high
               Environmental impact : persistence, bioaccumulation, etc.
               Availability of the metal : abundant, accessible or rare/costly

       """
    metals_data = {
        "Pd": {
            "Name" : "Palladium",
            "Toxicity" : "Moderate, may cause allergic skin and respiratory reactions.",
            "Ecotoxicity" : "Moderate, potential bioaccumulation in the aquatic environment",
            "Availability" : "Rare",
        },
        "Ni": {
            "Name": "Nickel",
            "Toxicity": "Moderate to high, carcinogenic by inhalation, skin allergen",
            "Ecotoxicity": "Moderate, toxic to aquatic life at high concentrations",
            "Availability": "Moderate"
        },
        "Cu": {
            "Name": "Copper",
            "Toxicity": "Low to moderate, toxic at high doses",
            "Ecotoxicity": "Moderate, toxic to fish and invertebrates",
            "Availability": "Very abundant"
        },
        "Fe": {
            "Name": "Iron",
            "Toxicity": "Low",
            "Ecotoxicity": "Low, minimal environmental concerns",
            "Availability": "One of the most abundant on earth"
        },
        "Co": {
            "Name": "Cobalt",
            "Toxicity": "Moderate, neuro- and cardiotoxic at high doses",
            "Ecotoxicity": "Moderate, toxic to some aquatic organisms",
            "Availability": "moderate"
        },
        "Mn": {
            "Name": "Manganese",
            "Toxicity": "Low to moderate, neurotoxic in excess",
            "Ecotoxicity": "Low",
            "Availability": "Abundant"
        },
        "Zn": {
            "Name": "Zinc",
            "Toxicity": "Low, gastrointestinal effects at high doses",
            "Ecotoxicity": "Moderate, aquatic toxicity at high concentrations",
            "Availability": "Abundant"
        },
        "Cr": {
            "Name": "Chromium",
            "Toxicity": "High (carcinogenic) for Cr(VI), low for Cr(III)",
            "Ecotoxicity": "High for Cr(VI), aquatic and plant toxicity",
            "Availability": "Moderate"
        },
        "Ru": {
            "Name": "Ruthenium",
            "Toxicity": "Low to moderate",
            "Ecotoxicity": "Low, limited data",
            "Availability": "Rare"
        },
        "Rh": {
            "Name": "Rhodium",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "One of the rarest metal on earth, extremely expensive"
        },
        "Ir": {
            "Name": "Iridium",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "One of the rarest metal on earth, extremely expensive"
        },
        "Sc": {
            "Name": "Scandium",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "Rare"
        },
        "Ti": {
            "Name": "Titanium",
            "Toxicity": "Low, biologically inert",
            "Ecotoxicity": "Low",
            "Availability": "Very abundant"
        },
        "Mg": {
            "Name": "Magnesium",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "Very abundant"
        },
        "La": {
            "Name": "Lanthanum",
            "Toxicity": "Low to moderate, gastrointestinal effects at high doses",
            "Ecotoxicity": "Moderate, aquatic impact at high levels",
            "Availability": "Moderate but complex extraction"
        },
        "Sm": {
            "Name": "Samarium",
            "Toxicity": "Low",
            "Ecotoxicity": "Moderate, aquatic effects possible",
            "Availability": "Moderate but complex extraction"
        },
        "Pt": {
            "Name": "Platinum",
            "Toxicity": "Moderate, some complexes are toxic and allergenic",
            "Ecotoxicity": "Moderate, may bioaccumulate and persist in aquatic environments",
            "Availability": "Rare and expensive"
        },
        "Os": {
            "Name": "Osmium",
            "Toxicity": "High, OsO₄ is highly toxic and volatile",
            "Ecotoxicity": "High, OsO₄ is toxic to aquatic life and can bioaccumulate",
            "Availability": "Extremely rare and expensive"
        },
        "Re": {
            "Name": "Rhenium",
            "Toxicity": "Low to moderate",
            "Ecotoxicity": "Low",
            "Availability": "Extremely rare and expensive"
        },
        "V": {
            "Name": "Vanadium",
            "Toxicity": "Moderate to high, in pentavalent form (V₂O₅) can cause respiratory issues and is a potential carcinogen",
            "Ecotoxicity": "Moderate, toxic to aquatic organisms and plants at elevated concentrations",
            "Availability": "Moderate, relatively abundant"
        },
        "Mo": {
            "Name": "Molybdenum",
            "Toxicity": "Low to moderate, toxic at high doses",
            "Ecotoxicity": "Low to moderate, toxic to aquatic life at high concentrations",
            "Availability": "Moderate"
        },
        "W": {
            "Name": "Tungsten",
            "Toxicity": "Low toxicity in elemental form",
            "Ecotoxicity": "Low but limited data",
            "Availability": "Moderate, relatively abundant"
        },
        "Nb": {
            "Name": "Niobium",
            "Toxicity": "Low, elemental niobium is considered physiologically inert",
            "Ecotoxicity": "Low, minimal environmental impact",
            "Availability": "Moderate, production is limited to a few countries"
        },
        "Ta": {
            "Name": "Tantalum",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "Rare"
        },
        "Y": {
            "Name": "Yttrium",
            "Toxicity": "Low",
            "Ecotoxicity": "Low",
            "Availability": "moderate, relatively abundant"
        },
        "Eu": {
            "Name": "Europium",
            "Toxicity": "Low to moderate, soluble compounds can be toxic, but insoluble forms are largely inert",
            "Ecotoxicity": "Low but limited data",
            "Availability": "Rare"
        },
        "Ce": {
            "Name": "Cerium",
            "Toxicity": "Low to moderate, can cause skin irritation and respiratory issues in occupational settings",
            "Ecotoxicity": "Moderate, can damage aquatic organisms' cell membranes",
            "Availability": "low, most abundant rare earth element"
        }
    }

    if metal not in metals_data:
        return f"No data available for {metal}"

    m = metals_data[metal]
    return (
        f" {m['Name']} ({metal})"
        f" **Human toxicity**: {m['Toxicity']}|"
        f" **Environmental impact**: {m['Ecotoxicity']}|"
        f" **Availability**: {m['Availability']}"
    )