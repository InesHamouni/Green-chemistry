def energy_efficiency(temperature, pressure):
    """
    Calculate the energy efficiency of a reaction

    One of the twelve principles of green chemistry is energy efficiency.
    The principle is to reduce energy consumption as much as possible when carrying out a reaction.
    Unfortunately, it's difficult to quantify the energy used, but it is possible to assess the temperature and pressure of the reaction.
    One possible alternative for reducing the energy consumption of a reaction is the use of catalysts or enzymes (bio-catalysts).

        Args:
            temperature (float): the temperature at which the reaction is carried out
            pressure (float): the pressure at which the reaction is carried out

        Returns:
            Tuple (Temperature assessment, Pressure assessment)

    """

    if temperature < 100:
        assessment_T = "Temperature conditions are good"
    elif 100 <= temperature < 200:
        assessment_T = "Temperature conditions are not great"
    elif temperature >= 200:
        assessment_T = "Temperature conditions consume a lot of energy"


    if pressure < 5:
        assessment_P = "Pressure conditions are good"
    elif 5 <= pressure < 30:
        assessment_P = "Pressure conditons are not great"
    elif pressure >= 30:
        assessment_P = "Pressure conditions consume a lot of energy"

    return assessment_T, assessment_P

