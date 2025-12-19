#!/usr/bin/env python
# coding: utf-8

# <left>
# <table style="margin-top:0px; margin-left:0px;">
# <tr>
#   <td><img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/style/worm.png" alt="WORM" title="WORM" width=50/></td>
#   <td><h1 style=font-size:30px>Modeling Water-Organic-Rock-Microbe<br>reactions with the WORM Portal</h1><br />
# </tr>
# </table>
# </left>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/title.png" title="WORM title" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/whyWORM.png" title="Why WORM?" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/aboutWORM.png" title="About WORM" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/outline.png" title="Outline" width=800/>

# ---

# ## Brief WORM Portal tour here...

# ---

# ## Aqueous speciation with AqEquil

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/speciation.png" title="speciation" width=800/>

# Split species into *basis* and *non-basis* to make setting up the problem easier.
# 
# $\color{magenta}{\text{Basis} : \text{SiO}_{2}, \text{H}_{2}\text{O}, \text{H}^{+}, \text{Mg}^{2+}, \text{Ca}^{2+}, \text{Na}^{+}, \text{HCO}_{3}^{-}}$
# 
# $\color{lime}{\text{Non-Basis} : \text{HSiO}_{3}^{-}, \text{Mg(HSiO}_{3}\text{)}^{+}, \text{Ca(HSiO}_{3}\text{)}^{+}, \text{NaHSiO}_{3(aq)}, \text{Mg(HCO}_{3}\text{)}^{+}, \text{Ca(HCO}_{3}\text{)}^{+}, \text{NaHCO}_{3}, \text{CO}_{3}^{2-}, \text{MgCO}_{3(aq)}, \text{CaCO}_{3(aq)}, \text{NaCO}_{3}^{-}}$
# 
# 
# \begin{align}
# \color{magenta}{\text{SiO}_{2}} + \color{magenta}{\text{H}_{2}\text{O}} &\rightleftharpoons \color{lime}{\text{HSiO}_{3}^{-}} + \color{magenta}{\text{H}^{+}} \\
# \color{magenta}{\text{SiO}_{2}} + \color{magenta}{\text{Mg}^{2+}} + \color{magenta}{\text{H}_{2}\text{O}} &\rightleftharpoons \color{lime}{\text{Mg(HSiO}_{3}\text{)}^{+}} + \color{magenta}{\text{H}^{+}} \\
# \color{magenta}{\text{SiO}_{2}} + \color{magenta}{\text{Ca}^{2+}} + \color{magenta}{\text{H}_{2}\text{O}} &\rightleftharpoons \color{lime}{\text{Ca(HSiO}_{3}\text{)}^{+}} + \color{magenta}{\text{H}^{+}} \\
# \color{magenta}{\text{SiO}_{2}} + \color{magenta}{\text{Na}^{+}} + \color{magenta}{\text{H}_{2}\text{O}} &\rightleftharpoons \color{lime}{\text{NaHSiO}_{3(aq)}} \\
# \end{align}
# 
# \begin{align}
# \color{magenta}{\text{HCO}_{3}^{-}} &\rightleftharpoons \color{lime}{\text{CO}_{3}^{2-}} + \color{magenta}{\text{H}^{+}} \\
# \color{magenta}{\text{HCO}_{3}^{-}} + \color{magenta}{\text{Mg}^{2+}} + &\rightleftharpoons \color{lime}{\text{Mg(HCO}_{3}\text{)}^{+}} + \color{magenta}{\text{H}^{+}} \\
# \text{...} & \text{and so on...}
# \end{align}
# 
# To find the concentrations of all basis and non-basis, you'd need to find the root of an enormous set of equilibrium equations. Not easy to do by hand!
# 
# Fortunately, computational tools exist to help.

# ---

# ### Example: submarine hydrothermal vent fluids
# 
# - <u>S&C10vents.csv</u> contains a variety of subsea hydrothermal vent fluids ([Shock & Canovas 2010](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1468-8123.2010.00277.x))
# 
# - Speciate these fluids and visualize the results
# 
# Load the AqEquil (aqueous equilibration) package:

# In[1]:


import AqEquil

ae = AqEquil.AqEquil()


# Speciate the submarine hydrothermal vent samples in "S&C10vents.csv" with `speciate()`:

# In[2]:


speciation = ae.speciate(input_filename="S&C10vents.csv",
                         report_filename="out.csv")


# In[3]:


speciation.barplot('CH4')


# In[10]:


speciation.barplot(["Ca+2", "Mg+2", "K+"])


# In[11]:


speciation.lookup(["Temperature", "Pressure", "SiO2", "Mg(HSiO3)+", "Ca(HSiO3)+", "NaHSiO3"])


# In[12]:


speciation.plot_mass_contribution("HCO3-", sort_by="pH")


# In[13]:


speciation.scatterplot("pH", "HS-")


# In[14]:


speciation.scatterplot("pH", ["HS-", "H2S"])


# In[15]:


speciation.plot_mineral_saturation('Lau')


# ---

# ### Microbial energy supply

# <img src="https://www.igpms.ucsb.edu/sites/default/files/styles/medium/public/2019-05/guaymas-microbial-mats.jpg" title="Credit: Professor Andreas Teske, UNC Chapel Hill" width=500/>
# 
# *Microbial mats on hydrothermal sediments in the Guaymas Basin*
# 
# *Methanopyrus kandleri* has been found in submarine hydrothermal systems, including the Guaymas Basin.

# <center>
# <img src="https://alchetron.com/cdn/methanopyrus-4b113cae-c869-47bb-8c69-1e113a1b9c8-resize-750.jpeg" title="Methanopyrus kandleri." width=200/>
# <\center>
# 
# <center><i>Methanopyrus kandleri<\i></center>

# These microbes can grow up to 122°C and produce CH$_4$ by reducing CO$_2$ with H$_2$:
# 
# \begin{align}
# \mathop{\rm{CO_{2}}} + \mathop{\rm{4H_{2}}} & \rightleftharpoons \rm{2H_{2}O} + \rm{CH_{4}} \\
# \end{align}

# What is the chemical affinity and energy supply in our vent fluid samples?

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/affinity.png" title="Affinity calculation" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/energy.png" title="Energy supply calculation" width=800/>

# In[16]:


import AqEquil

# get available redox half reactions
ae = AqEquil.AqEquil()
ae.half_cell_reactions


# In[17]:


ae.make_redox_reactions(redox_pairs=[12,18])


# In[18]:


_ = ae.show_redox_reactions()


# In[19]:


speciation = ae.speciate(input_filename="S&C10vents.csv",
                         report_filename="out.csv",
                         get_affinity_energy=True, # calculate energy supplies
                         negative_energy_supplies=True,
                         )


# Here's that reaction again:
# 
# \begin{align}
# \mathop{\rm{CO_{2}}} + \mathop{\rm{4H_{2}}} & \rightleftharpoons \rm{2H_{2}O} + \rm{CH_{4}} \\
# \end{align}

# In[20]:


# what names are used to refer to energy supplies here?
speciation.lookup("energy")


# In[21]:


speciation.lookup(["Temperature", 'red_CO2_CH4_ox_H2_H2O_0_energy', 'red_H2O_H2_ox_CH4_CO2_7_energy'])


# In[22]:


speciation.scatterplot("H2", 'red_CO2_CH4_ox_H2_H2O_0_energy')


# ---
# ## Reaction Property Calculations with pyCHNOSZ

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/pyCHNOSZ.png" title="AqOrg" width=800/>

# ### Example:
# 
# \begin{align}
# \mathop{\rm{K(AlSi_{3})O_{8}}}\limits_{\text{(K-feldspar)}} + \mathop{\rm{Al_{2}Si_{2}O_{5}(OH)_{4}}}\limits_{\text{(kaolinite)}} & \rightleftharpoons \rm{H_{2}O} + \rm{2SiO_{2(aq)}} + \mathop{\rm{KAl_{2}(AlSi_{3})O_{10}(OH)_{2}}}\limits_{\text{(muscovite)}} \\
# \end{align}
# 
# - What are the standard molal properties of this reaction from 0 to 350°C at saturation pressure?
# - At elevated pressure?
# 
# First, load up the pyCHNOSZ package:

# In[29]:


from pyCHNOSZ import *
_ = thermo("WORM")


# Check that these species are in the database with `info()`:

# In[30]:


info(info(["K-feldspar", "kaolinite", "SiO2", "muscovite"]))


# Calculate reaction properties with `subcrt()`:

# In[31]:


subcrt(species=["K-feldspar", "kaolinite", "H2O", "SiO2", "muscovite"],
       coeff=[-1, -1, 1, 2, 1])


# It is also possible to specify temperature and pressures:

# In[32]:


subcrt(species=["K-feldspar", "kaolinite", "H2O", "SiO2", "muscovite"],
       coeff=[-1, -1, 1, 2, 1],
       T=255, P=1100)


# Create a predominance diagram of minerals in the K$_2$O-Al$_2$O$_3$-SiO$_2$-H$_2$O system:

# In[33]:


# make HSiO4 available
add_OBIGT("AS04") 

# define basis and species in a mini-speciation calculation
basis(["Al+3", "H4SiO4", "K+", "H2O", "H+", "O2"])
species(["gibbsite", "muscovite", "kaolinite", "pyrophyllite", "K-feldspar"])

# what basis species should go on the x and y axes? Ranges? Number of calculations?
params = {"H4SiO4":[-8, 0, 600], "K+":[-1, 8, 600]}
a = affinity(**params)

# create the diagram
_ = diagram(a, xlab="log(aH4SiO4)", ylab="log(aK+/aH+)", fill="terrain")


# ---
# ## Estimate thermodynamic properties of aqueous organics with AqOrg

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/AqOrg_slide.png" title="AqOrg" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/4-Thermodynamic-Property-Estimation/1-Aq-Organics-Intro-Demo/Figure-1.png" width=800 height=600 style="background-color:white;padding:0px;"/>

# First, import the package:

# In[34]:


from AqOrg import Estimate


# Estimate the properties of the molecule with `Estimate()`

# In[35]:


hexanol = Estimate("1-hexanol")


# View group matches:

# In[36]:


hexanol.group_matches


# View estimated properties:

# In[37]:


hexanol.OBIGT


# ### Example: Archaeal Lipids

# Archaeol is a lipid biomarker for Archaea.

# <img src="http://www.clovegarden.com/ingred/img/archaea01l.jpg" title="archaeal membrane" width=600/>
# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/Archaeol_structure.png" title="archaeol" width=600 style="background-color:white;padding:20px;"/>
# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/Unsaturated_archaeol.png" title="unsaturated archaeol" width=600 style="background-color:white;padding:20px;"/>

# Estimate the properties of archaeol with `Estimate()`.

# In[38]:


archaeol = Estimate("archaeol", Cph=2633)


# In[39]:


archaeol.OBIGT


# In[47]:


unsaturated_archaeol = Estimate("2,3-Bis[[(2E,6E,10E)-3,7,11,15-tetramethylhexadeca-2,6,10,14-tetraenyl]oxy]-1-propanol", Cph=2593)


# Estimated properties can be imported into pyCHNOSZ with `mod_OBIGT()`:

# In[45]:


# make archaeol and unsaturated archaeol available to pyCHNOSZ
mod_OBIGT(archaeol.OBIGT)
mod_OBIGT(unsaturated_archaeol.OBIGT)


# Now that these lipids are loaded into pyCHNOSZ, we can create an activity diagram:

# In[46]:


# define basis and species in a mini-speciation calculation
basis(["CO2", "H2", "H2O"])
species(["archaeol", "2,3-Bis[[(2E,6E,10E)-3,7,11,15-tetramethylhexadeca-2,6,10,14-tetraenyl]oxy]-1-propanol"])

# what basis species should go on the x and y axes? Ranges? Number of calculations?
a = affinity(H2=[-30, 0, 600], T=[0, 350, 600])

# create the diagram
_ = diagram(a, names=["archaeol", "unsaturated archaeol"], fill='terrain')


# ---

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/outline.png" title="outline" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/wrapup.png" title="wrap up" width=800/>

# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/WORM-tour/thanks.png" title="acknowledgements" width=800/>
