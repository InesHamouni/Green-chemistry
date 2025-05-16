def temperature_efficiency(temperature):

    """
   Calculate the temperature efficiency of a reaction

   One of the twelve principles of green chemistry is energy efficiency.
   The principle is to reduce energy consumption as much as possible when carrying out a reaction.
   Unfortunately, it's difficult to quantify the energy used, but it is possible to assess the temperature of the reaction.
   One possible alternative for reducing the energy consumption of a reaction is the use of catalysts or enzymes (bio-catalysts).

       Args:
           Temperature (float): the temperature at which the reaction is carried out

       Returns:
           Temperature assessment

   """

    if temperature < 100:
      assessment_T = "low energy consumption"
    elif 100 <= temperature < 200:
      assessment_T = "moderate energy consumption"
    elif temperature >= 200:
     assessment_T = "high energy consumption"

    return assessment_T