def atom_economy(product_mass, reactant_masses):
    """
    Calculates the atom economy (%) of a chemical reaction.

    In chemistry, the atom economy enables scientists to estimate how efficient are their reactions. 
    In other words, it is the calculation of the quantity of reactant atoms are incorporated into the 
    desired product.
    A reaction is sustainable when the atom economy is high (> 80% approximately), little waste.
    On the other hand, a low percentage suggests lot of wasted reagents, which have a negative
    impact on the environement. 

    Parameters:
    - product_mass (float): Molar mass of the desired product (in g/mol)
    - reactant_masses (list of float): List of molar masses of all reactants involved (in g/mol)

    Returns:
    - tuple: 
      - float: Atom economy as a percentage (%)
      - str: Verdict ("Good", "Acceptable", "Poor") based on atom economy
    """
    total_reactants_mass = sum(reactant_masses)
    
    if total_reactants_mass == 0:
        raise ValueError("Total molar mass of reactants cannot be zero.")
    
    economy = (product_mass / total_reactants_mass) * 100
    verdict = ""
    
    # Determine the verdict based on the economy percentage
    if economy > 80:
        verdict = "Good (Highly efficient and environmentally friendly)"
    elif economy >= 50:
        verdict = "Acceptable (Moderately efficient, room for improvement)"
    else:
        verdict = "Poor (Inefficient, generates significant waste)"
    
    return round(economy, 2), verdict

