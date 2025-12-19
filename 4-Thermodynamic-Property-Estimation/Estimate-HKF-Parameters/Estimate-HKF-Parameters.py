#!/usr/bin/env python
# coding: utf-8

# <left>
# <table style="margin-top:0px; margin-left:0px;">
# <tr>
#   <td><img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/style/worm.png" alt="WORM" title="WORM" width=50/></td>
#   <td><h1 style=font-size:30px>Estimating Thermodynamic Properties</h1><h2>Helgeson-Kirkham-Flowers (HKF) Parameters</h2></td>
# </tr>
# </table>
# </left>

# ### What is the HKF equation of state?
# 
# The Helgeson-Kirkham-Flowers (HKF) equation of state is widely used in aqueous geochemistry to model how the standard state Gibbs free energies of formation of solutes change with temperature and pressure. The equation is used by WORM tools like pyCHNOSZ and AqEquil to calculate reaction properties such as equilibrium constants at elevated temperatures and pressures.
# 
# The HKF equation requires seven parameters that depend on the aqueous species that is being modeled.
# 
# |**Symbol**|**Description**|
# |:---:|:---:|
# | $\omega$ | omega, the Born solvation coeffcient |
# | $a_1, a_2, a_3, a_4$ | the pressure-dependence parameters |
# | $c_1, c_2$ | the temperature-dependence parameters |
# 
# Most aqueous chemical species in the [WORM thermodynamic database](https://worm-portal.asu.edu/docs/database/) have values for all seven HKF parameters in addition to standard state properties like Gibbs free energy of formation (G), enthalpy (H), third law entropy (S), volume (V), and heat capacity (Cp).
# 
# **Note:** Non-aqueous molecules do not use HKF parameters. Instead, non-aqueous use a different equation called the Maier-Kelley equation of state. This equation of state has its own parameters ($a, b, c, d, e, f, \lambda$ (lambda)). The WORM database has entries for crystalline and gaseous chemical species. Their Maier-Kelley coefficients share columns with aqueous HKF coefficients. For example, the HKF omega parameter for an aqueous species shares the same column as the Maier-Kelley lambda parameter, so the column name is "omega.lambda". [This is described in more detail here.](https://worm-portal.asu.edu/docs/database/)
# 
# ---
# 
# ### Estimating HKF paramters for a new aqueous molecule
# 
# Let's say you're interested in obtaining an equilibrium constant for a reaction at elevated temperatures and pressures using the HKF equation (e.g. while using pyCHNOSZ or AqEquil). However, you realize that one of the molecules in your reaction is not in the thermodynamic database. For example, let's assume that aqueous **hexanoic acid** is missing from the database.
# 
# Normally, this would not be a problem. The aqueous organic estimator (AqOrg) tool on WORM was built to estimate properties and HKF parameters of aqueous organic nonelectrolytes (see demos 4-1-1 and 4-1-2 in the WORM Library). Aqueous hexanoic acid is an organic nonelectrolyte, so it seems like a perfect candidate for AqOrg. Unfortunately for us, there are no published methods for estimating the properties of a carboxylic acid functional group compatible with the group additivity scheme used by AqOrg. As a result, AqOrg will throw a big red error message saying that it cannot estimate the properties of hexanoic acid. 😔
# 
# So what now? Are we stuck? Not necessarily!
# 
# Digging through the literature, you'll be able to find experimental measurements of standard state properties that people have published for hexanoic acid at 25 °C and 1 bar. Let's say you gather these:
# 
# <center><b>Aqueous Hexanoic Acid</b></center>
# 
# |**Value**|**Unit**|**Standard State Property**|**Symbol**|
# |:---:|:---:|:---:|:---:|
# |-87080|cal/mol|Gibbs free energy of formation|$\Delta_f G^{\circ}$|
# |-139290|cal/mol|enthalpy of formation|$\Delta_f H^{\circ}$|
# |69.5|cal/K/mol|third law entropy|$S^{\circ}$|
# |116.55|cm$^3$/mol|volume|$V^{\circ}$|
# |125.2|cal/mol/K|isobaric heat capacity|$C_p^{\circ}$|
# 
# It's a great start that allows you to calculate properties of reactions at 25 °C and 1 bar... but what about higher temperatures and pressures? We'll need HKF parameters for that.
# 
# Fortunately, there are published strategies for estimating HKF paramters based on 25 °C and 1 bar standard state properties of aqueous molecules. These strategies are outlined in works such as [Shock and Helgeson 1988](https://doi.org/10.1016/0016-7037(88)90181-0) (for ionic species), [Shock and Helgeson 1990](https://doi.org/10.1016/0016-7037(90)90429-O) (for organic electrolytes and nonelectrolytes), [Plyasunov and Shock 2001](https://doi.org/10.1016/S0016-7037(01)00678-0) (for nonelectrolytes when starting with hydration properties), and [Sverjensky et al., 2014](https://doi.org/10.1016/j.gca.2013.12.019) (for solutes used with the Deep Earth Water, DEW, model).
# 
# These strategies have been coded into a function called `find_HKF` that is included in the `WORMutils` package. Let's use this function to estimate the HKF parameters of hexanoic acid!
# 
# First, let's load some functions from the `WORMutils` package. We'll load a couple of functions; `find_HKF` and another called `find_HKF_test` that will be discussed a little later.

# In[1]:


from wormutils import find_HKF, find_HKF_test


# Now we can input the 25 °C and 1 bar standard state properties of hexanoic acid into the `find_HKF` function along with charge and whether the molecule is an organic acid:

# In[2]:


hkf, eq = find_HKF(Gf = -87120, # Gibbs free energy of formation, cal/mol
                   Hf = -139290, # enthalpy of formation, cal/mol
                   Saq = 69.5, # third law entropy, cal/mol/K
                   V = 116.55, # volume, cm3/mol
                   Cp = 125.2, # isobaric heat capacity, cal/mol/K
                   Z = 0, # charge
                   organic = True, # is the molecule organic?
                   organic_acid = True, # is the molecule an organic acid?
                  )


# The `find_HKF` function produces two outputs:
# - The first is the suite of estimated HKF properties (stored in the `hkf` variable, above)
# - The second is a step-by-step list of the published equations used to obtain the estimates.
# 
# Let's take a look at the first output:

# In[3]:


hkf


# The first few lines show the properties that we input into the function, like Gibbs free energy, enthalpy, etc.
# 
# The estimated values for the HKF parameters a1-a4, c1-c2, and omega are included.
# 
# **VERY IMPORTANT NOTE:** the values of HKF parameters output by `find_HKF` are scaled according to common convention. Scaling conventions and HKF parameter units are shown in the second table [on the webpage that describes the WORM database](https://worm-portal.asu.edu/docs/database/). For example, the estimated value of omega is for hexanoic acid is shown above as $-0.712$, which actually means $\omega = -0.712 \cdot 10^{5}$ cal/mol because by convention, omega values are reported as $\omega \cdot 10^{-5}$. Be aware that each HKF parameter is scaled by a different magnitude:
# 
# 
# |**output name**|**scaling**|**unit**|
# |:---:|:---:|:---:|
# |omega|$\omega \cdot 10^{-5}$|cal/mol|
# |a1|$a_1 \cdot 10$|cal/mol/bar|
# |a2|$a_2 \cdot 10^{-2}$|cal/mol|
# |a3|$a_3$ (no scaling)|(cal*K)/mol/bar|
# |a4|$a_4 \cdot 10^{-4}$|(cal*K)/mol|
# |c1|$c_1$ (no scaling)|cal/mol/K|
# |c2|$c_2 \cdot 10^{-4}$|(cal*K)/mol|
# 
# Why are HKF parameters scaled like this? Traditionally, it was done to make tables of HKF parameters look tidier in published papers.
# 
# The upside of having the `find_HKF` function output scaled HKF parameters is that you can plug these numbers directly into the WORM database when creating a custom CSV for your own research. For example, the "omega.lambda" column, which contains the omega parameter for aqueous species, requires that scaled values be entered according to $\omega \cdot 10^{-5}$. In other words, you don't have to scale HKF parameters yourself,  and can enter them as-is into the WORM database.
# 
# Now let's look at the second output of `find_HKF`:

# In[4]:


eq


# We can get a neater version of this by setting up a little loop to print each line:

# In[5]:


for equation in eq:
    print(equation)


# These are the equations and constants that were used to estimate the HKF parameters of hexanoic acid. Equations are shown with source references, and the value and units that have been calculated at each step. Equations are shown in the order that they were used. Math operations are shown pythonically (e.g., 0.34*10\**5 represents $0.34 \cdot 10^{5}$).
# 
# Note that there are a few literature sources used in this example: [Shock and Helgeson 1988](https://doi.org/10.1016/0016-7037(88)90181-0), [Shock and Helgeson 1990](https://doi.org/10.1016/0016-7037(90)90429-O), and [Shock 1995](https://ajsonline.org/article/60689.pdf). This is because later papers provide updates to the methods established in the earlier papers.
# 
# ---
# 
# If you are curious about how well the `find_HKF` function is able to replicate published HKF parameters, check out the `find_HKF_test` function. It reports inputs and outputs for various aqueous species and compares output to published values. Note that hexanoic acid is included in the test along with its anion, hexanoate.

# In[6]:


find_HKF_test()


# ### Importing estimated HKF parameters into the database for calculations
# 
# What next? If hexanoic acid was actually absent from the WORM database then we might follow this procedure to get hexanoic acid to show up in our modeling calculations:
# 1. download a copy of the [WORM database CSV file](https://github.com/worm-portal/WORM-db/blob/master/wrm_data.csv)
# 2. add a new line for "hexanoic-acid" (be sure to replace spaces with dashes in chemical species names, and don't use a name that is already in the database)
# 3. fill out the columns for "hexanoic-acid" while referencing [the WORM database documentation](https://worm-portal.asu.edu/docs/database/)
#    - the "omega" HKF parameter goes in the "omega.lambda" column, the "a1" parameter goes in the "a1.a" column, etc.
#    - if you only need this database for a pyCHNOSZ calculation, you can ignore all of the columns to the right of "z.T".
#    - if you need this database for a speciation calculation with AqEquil, you need to fill out all of the columns in the CSV. The exception is the "dissrxn" column which you can leave blank if you'd prefer the chemical species' dissociation reaction to be generated automatically for you.
# 4. import your CSV into your tool of choice.
#   
# For example, importing a custom CSV database into pyCHNOSZ can be done with:
# 
# ```
# from pychnosz import *
# _ = thermo("WORM")
# _ = add_OBIGT("my_custom_database.csv")
# 
# # ... your calculation goes here, e.g., using subcrt()
# ```
# 
# Importing a custom database into AqEquil can be done with:
# ```
# import aqequil
# ae = aqequil.AqEquil(db="my_custom_database.csv")
# 
# # ... your speciation calculation goes here, e.g., using ae.speciate()
# ```
# 
# Working with thermodynamic databases can be tricky to get right the first time. If you reach a point where you get stuck and need clarification to proceed, feel free to reach out to the WORM administrator Grayson Boyer (email: gmboyer at asu dot edu) and ask to join the WORM Slack community where these kinds of questions get answered.

# End of demo.

# In[ ]:




