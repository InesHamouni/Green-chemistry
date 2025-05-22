def pressure_efficiency(pressure):
    """
    Calculate the pressure efficiency of a reaction

    One of the twelve principles of green chemistry is energy efficiency.
    The principle is to reduce energy consumption as much as possible when carrying out a reaction.
    Unfortunately, it's difficult to quantify the energy used, but it is possible to assess the pressure of the reaction.
    One possible alternative for reducing the energy consumption of a reaction is the use of catalysts or enzymes (bio-catalysts).

        Args:
            pressure (float): the pressure at which the reaction is carried out

        Returns:
            Pressure assessment

    """
    
    if pressure == 1:
        assessment_P = "atmospheric pressure, zero energy consumption"
    elif 1 < pressure < 5:
        assessment_P = "low energy consumption"
    elif 5 <= pressure < 30:
        assessment_P = "moderate energy consumption"
    elif pressure >= 30:
        assessment_P = "high energy consumption"
    return assessment_P


