#!/usr/bin/env python
# coding: utf-8

# <left>
# <table style="margin-top:0px; margin-left:0px;">
# <tr>
#   <td><img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/style/worm.png" alt="WORM" title="WORM" width=50/></td>
#   <td><h1 style=font-size:30px>Water-Rock Reaction Modeling</h1><h2>Advanced WORM Workshop June 20, 2023</h2></td>
# </tr>
# </table>
# </left>

# Here is a general example of a water-rock reaction:
# 
# $$ \text{rain} + \text{rocks} \rightarrow \text{rivers} + \text{soil} $$
# 
# An particularly interesting example of this is called serpentinization. It happens is in places where the Earth's mantle is exposed to the surface and reacts with percolated rainwater. There are only a few places on Earth that we know of where scientists can study serpentinization, but it is thought to be one of the most common geologic processes in the universe.
# 
# <div>
# <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/2-Reaction-Properties/4-Univariant-Curves/oman.jpg" width="49%" align="center"/>     <img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/2-Reaction-Properties/4-Univariant-Curves/pigs.jpg" width="49%" align="center"/>
# </div>
# 
# Image credit: GEOPIG Lab
# 
# Left: a "river" produced from serpentinization water-rock reactions in Oman.
# 
# Right: a closeup of serpentine minerals with 1 inch-long piggies for scale
# 
# <br/>
# 
# <div>
# <img src="https://www.researchgate.net/publication/358894465/figure/fig1/AS:1136615871262720@1648001749066/Conceptual-diagram-of-the-process-of-serpentinization-in-Oman-Figure-adapted-from-Leong_W640.jpg" width="75%" align="center"/>
# </div>
# 
# From [Howells et al. 2022](http://dx.doi.org/10.1029/2021JG006317)
# 
# 
# 
# Serpentinization refers to an alteration process where minerals in the serpentine group of phyllosilicates replace minerals like olivine and pyroxene that form at high temperatures and pressures.
# 
# In this example, a low-temperature, pH 6 aqueous fluid defined in `rainpH6_input.csv` will be speciated and then reacted at ambient conditions with 1 mole of [forsterite](https://www.mindat.org/min-1584.html) (olivine) bit-by-bit until the reaction is complete. This should produce [brucite](https://www.mindat.org/min-820.html) and the serpentine mineral [chrysotile](https://www.mindat.org/min-975.html) and cause the pH of the fluid to dramatically increase until it is hyperalkaline (~pH 10).
# 
# 
# <div>
# <img src="https://www.mindat.org/imagecache/bc/ff/00522600016143865397075.jpg" width="32%" align="center"/>
# <img src="https://www.mindat.org/imagecache/1f/00/06966310014976637785495.jpg" width="32%" align="center"/>
# <img src="https://www.mindat.org/imagecache/32/b3/07772330016737181982378.jpg" width="32%" align="center"/>
# </div>
# 
# Left: forsterite (credit: Rudolf Watzl). Middle: brucite (credit: Matteo Chinellato). Right: chrysotile (credit: Jakub Jirásek).
# 
# Many different kinds of data are produced from the calculation that can be visualized with interactive plots. Most of these plots show how mineral masses or fluid compositions change as a function of reaction progress (Xi).
# 
# First, let's make a phase diagram in pressure-temperature space that shows what happens when forsterite (Mg$_2$SiO$_4$) is altered to brucite (Mg(OH)$_2$) and chrysotile (Mg$_3$Si$_2$O$_5$(OH)$_4$) by water.
# Using the clues above, we can write this balanced reaction:
# 
# $$ \mathop{\rm{2 Mg_{2}SiO_{4(cr)}}} \limits_{\text{(forsterite)}} + \rm{3H_{2}O} \rightarrow \mathop{\rm{Mg(OH)_{2(cr)}}} \limits_{\text{(brucite)}} + \mathop{\rm{Mg_{3}Si_{2}O_{5}(OH)_{4(cr)}}} \limits_{\text{(chrysotile)}}$$
# 
# This reaction tells us a great deal about the minerals, but nothing about changes in the aqueous solution involved in the alteration process, and gives us no information about the sequence of events during alteration. We actually want to know about all these things.
# 
# So, first we'll make a phase diagram...

# Load the Python package needed for univariant curves and tell it to use the WORM thermodynamic database.

# In[ ]:


from pyCHNOSZ import *
_ = thermo("WORM")


# Now we will use the univariant curve option in pyCHNOSZ to generate a P-T phase diagram for the mineral equilibrium reaction...

# In[ ]:


out = univariant_TP(logK=0, # desired logK or list of logK values
                    species=["forsterite","H2O", "brucite","chrysotile"], # chemical species
                    state=["cr", "liq", "cr", "cr"], # aq, gas, liq, cr
                    coeff=[-2, -3, 1, 1], # reaction stoichiometry (negative for reactants, positive for products)
                    Trange=[0, 700], # temperature range to check, degrees C
                    Prange=[10, 500], # pressure range to check, bars
      )


# You can practice changing the axes with the plotting tools to make a really nice P-T figure...
# 
# Meanwhile, the point is that forsterite + H$_2$O are stable to the high-temperature side of this curve, and brucite + chrysotile are on the low-temperature side. It follows that forsterite being rained on at or near the Earth's surface is not stable relative to brucite and chrysotile!
# 
# Now let's do the mass transfer calculation for that alteration process.

# Load the Python package.

# In[ ]:


import AqEquil


# Load the thermodynamic database and exclude organics to cut down on calculation time.

# In[ ]:


ae = AqEquil.AqEquil(exclude_category={"category_1":["organic_aq", "organic_cr"]})


# Speciate the pH 6 fluid defined in `rainpH6_input.csv`.
# 
# Antigorite is not a stable serpentine mineral at the conditions of this calculation, so we will ensure its formation is suppressed using the `alter_options` parameter.

# In[ ]:


speciation = ae.speciate(input_filename="rainpH6_input.csv",
                         alter_options=[["antigorite", "Suppress"]],
                        )


# Prepare the reaction by selecting reactant minerals. In this case, we will prepare forsterite to react with the pH 6 fluid.
# 
# During early stages of reaction progress forsterite is dissolving into the water.
# This means that the dominant reaction is what's called the hydrolysis reaction for forsterite:
# 
# $$ \mathop{\rm{2 Mg_{2}SiO_{4(cr)}}} \limits_{\text{(forsterite)}} + \rm{4 H^{+}} \rightarrow \rm{2 Mg^{+2}} + \rm{SiO_{2(aq)}} + \rm{2 H_2O}$$
# 
# Therefore our expectation at the early stages is for pH to rise, and the concentrations of total dissolved Mg and Si to increase. But the situation will change if the fluid becomes saturated with a new mineral and we allow it to form!

# In[ ]:


Forst = AqEquil.Reactant(reactant_name="forsterite")

r = AqEquil.Prepare_Reaction(reactants=[Forst])


# Run the reaction.

# In[ ]:


speciation = AqEquil.react(speciation, r)


# Select the sample by its name, `pH6HCl`, for analysis and plotting.

# In[ ]:


m = speciation.mt("pH6HCl")


# ## Available plot types

# Plot pH as a function of reaction progress (Xi)

# In[ ]:


m.plot_pH()


# Hey! pH increases as we expected, and it has an elaborate path...
# 
# Let's plot concentrations of dissolved elements as functions of reaction progress (Xi)

# In[ ]:


m.plot_elements(log=False)


# Ok, the concentration of total dissolved Mg increases. The concentration of total dissolved Si starts to increase as well, but then falls to low concentrations.
# You can use the zoom tool to check out the early stages of reaction (up to log Xi = -5 or so). 
# Mouse over the points at 10$^{-7}$ and 10$^{-6}$ log Xi and see if the ratio of total Mg to total Si is 2 like the forsterite dissolution (hydrolysis) reaction would have us believe.
# 
# Ha! it's true.
# 
# It is also true at the maximum point on the Si curve -- check it out!
# 
# But right there, at log Xi = -5.134 something happens that causes the total Si curve to change course.
# A good guess would be the precipitation from solution of a silicate mineral. Let's see!
# 
# Plot the moles of minerals produced as functions of reaction progress (Xi)

# In[ ]:


m.plot_product_minerals(show_reactant_minerals=False)


# A-ha! Right there at log Xi = -5.134 chrysotile appears as a product. It's the first mineral to appear, but may not be the last in the alteration assemblage.
# 
# Comparing the last two plots, we can see that as chrysotile appears the total dissolved Si falls dramatically and the total dissolved Mg skyrockets! What is going on?
# 
# First, it may help to remind ourselves about the overall process we're modeling.
# 
# Forsterite is dissolving continuously. In fact, the way we keep track of reaction progress (Xi) is by quantifying the amount of forsterite that has dissolved. Mg and Si increase in the 2:1 ratio we expect from the forsterite hydrolysis reaction until the solution reaches saturation with chrysotile at log Xi = -5.134.
# 
# Now there is a second reaction involved, chrysotile formation!
# 
# $$ \rm{3 Mg^{+2}} + \rm{2 SiO_{2(aq)}} + \rm{5 H_2O} \rightarrow \mathop{\rm{Mg_{3}Si_{2}O_{5}(OH)_{4(cr)}}} \limits_{\text{(chrysotile)}} + \rm{6 H^+}$$
# 
# So that second reaction is removing Mg and Si from solution. But it does so in a 3:2 ratio.
# 
# And all the while forsterite is dissolving, contributing Mg and Si to solution in a 2:1 ratio.
# 
# Examining these ratios will reveal why chrysotile formation drives the total Si concentration down, as forsterite dissolves and chrysotile forms, and the total Mg concentration up: More Mg is being added than is being removed.
# 
# Now we can explain why the total Mg concentration climbs. Then, at log Xi = -3.77 the Mg curve goes flat!
# Looking at the other plot reveals what changes. This is the point that brucite can form. Precipitation of brucite will remove Mg from solution and maintain the Mg concentration at the equilibrium value.
# 
# $$ \rm{Mg^{+2}} + \rm{2 H_2O} \rightarrow \mathop{\rm{Mg(OH)_{2(cr)}}} \limits_{\text{(brucite)}} + \rm{2 H^+} $$
# 
# So, while reaction progress increases, and forsterite is dissolving and contributing Mg and Si in a 2:1 ratio, both chrysotile and brucite are forming... and the two curves showing total moles of minerals produced are on top of each other. Equal amounts of chrysotile and brucite are forming. Let's see why...
# 
# Brucite and chrysotile forming together means that Mg and Si are removed in a 4:2 ratio, which is the same as the 2:1 ratio that they are being added by forsterite dissolution!
# 
# We could anticipate this by writing an overall reaction involving mineral reactants and products like we did above for making the phase diagram for
# 
# 
# $$ \mathop{\rm{2 Mg_{2}SiO_{4(cr)}}} \limits_{\text{(forsterite)}} + \rm{3H_{2}O} \rightarrow \mathop{\rm{Mg(OH)_{2(cr)}}} \limits_{\text{(brucite)}} + \mathop{\rm{Mg_{3}Si_{2}O_{5}(OH)_{4(cr)}}} \limits_{\text{(chrysotile)}}$$
# 
# but, that overall reaction doesn't reveal anything about what goes on in the coexisiting solution.
# 
# It is not that it is wrong, it is just incomplete. Changes are happening to the minerals, and changes also happen to the solution!
# 
# We can view these changes simultaneously by following our reaction path on an activity diagram.
# Let's start with some basics. 
# 
# If we return to the forsterite dissolution reaction:
# 
# $$ \mathop{\rm{2 Mg_{2}SiO_{4(cr)}}} \limits_{\text{(forsterite)}} + \rm{4 H^{+}} \rightarrow \rm{2 Mg^{+2}} + \rm{SiO_{2(aq)}} + \rm{2 H_2O}$$
# 
# we realize that there are three aqueous solutes involved (Mg$^{+2}$, SiO$_{2(aq)}$, and H$^+$).
# 
# Rather than making a three-dimensional diagram to depict the path, we can stay in two dimensions by placing two of our variables in a ratio.
# Often the choice is made to do this with the cations as (a$_{\rm{Mg}^{+2}}$)/(a$^{2}_{\rm{H^{+}}}$), where a stands for activity.
# then if we plot the log of that activity ratio vs the log activity of SiO$_{2(aq)}$ we can generate an activity diagram.
# Let's do that!

# In[ ]:


fig_list = m.plot_reaction_paths(flip_xy=True, # flip variables on x and y axes?
                                 colormap="bw", # black and white colormap for the background
                                 minerals_to_show=["quartz"], # show the quartz saturation line for reference
                                 )

_ = [fig.show() for fig in fig_list]


# Congratulations! a logarithmic activity diagram is born!
# 
# (In this case, log activities of basis species SiO$_{2(aq)}$ and Mg$^{+2}$ are automatically chosen as axis variables because the system only has a limited number of elements. In more complex systems, multiple permutations of plots are shown.)
# 
# Once the plot is ready, hover your mouse over the plot to see more.
# 
# This plot shows the Mg$^{+2}$ to H$^+$ activity ratio vs the activity of aquoeus silica for our chosen T & P (and remember those are indicated in the .csv file with the initial fluid composition).
# The diagram features three dashed lines that show conditions where minerals are stable.
# These are called mineral saturation lines. 
# 
# Take, for example, the horizontal dashed line labeled brucite in the legend. This line corresponds to equilibrium with respect to the reaction
# 
# $$ \rm{Mg^{+2}} + \rm{2 H_2O} \leftrightharpoons \mathop{\rm{Mg(OH)_{2(cr)}}} \limits_{\text{(brucite)}} + \rm{2 H^+} $$
# 
# The numerical value of (a$_{\rm{Mg}^{+2}}$)/(a$^{2}_{\rm{H^{+}}}$) can be calculated directly form the equilibrium constant for this reaction. Above this line a solution would be supersaturated with brucite, and precipitation of brucite would help to lower the energy state of the system. Below this line the solution is undersaturated with brucite, and dissolution of brucite (if present) would help to lower the energy state of the system.
# 
# The same reasoning produces the saturation lines for quartz and chrysotile, with the same consequences for supersaturation and undersaturation.
# 
# The red reaction path shows the results of our mass transfer model. Mouse over the nodes on the path to reveal the corresponding values of Xi.
# 
# Note that early on the reaction path starts at low values of log a$_{\rm{SiO}_{2}}$ and log (a$_{\rm{Mg}^{+2}}$)/(a$^{2}_{\rm{H^{+}}}$).
# 
# The path is far away from the saturation lines. This is because only a small amount of forsterite has dissolved. As forsterite continues to dissolve the reaction path moves upward and across the diagram. 
# 
# This initial trajectory of the path incorporates the changes in pH, Mg, and Si as forsterite dissolves.
# 
# Then things change as the fluid reaches equilibrium with chrysotile (check out the value of Xi and see that it is matched in the other figures). Now as forsterite continues to dissolve and chrysotile precipitates the fluid composition moves up and to the left along the chrysotile saturation line. Again, this can be reconciled with the Mg:Si ratios in the dissolveing forsterite and precipitating chrysotile.
# 
# The Si content of the fluid decreases as the Mg content of the fluid continues to increase, and the Mg$^{+2}$/H$^+$ activity ratio changes in concert. 
# 
# Finally the fluid composition reaches saturation with brucite as well as chrysotile. Brucite joins the fun!
# 
# But notice that the fluid composition is stuck at the intersection of the chrysotile and brucite saturation lines. All the Mg and Si being contributed by forsterite dissolution reappear in solid form as brucite and chrysotile. This is, in a way, a disadvantage of the activity diagram if you want to know how much of a new mineral forms. That information is not shown by the activity diagram. Instead you can get that information from the plot showing moles of product minerals. It helps to have all of these various perspectives to fully grasp the transformations that happen to the minerals and to the coexisting aqueous solution.
# 
# Now let's find out more about the solutes.
# 
# Plot activities of basis aqueous species as functions of reaction progress (Xi)

# In[ ]:


m.plot_aqueous_species(plot_basis=True)


# This diagram show us how the activities of the forms of the elements selected as the basis for this calculation (basis species) change in response to reaction progress (Xi). Note the similarities between Mg$^{+2}$ and total Mg plotted above; likewise between SiO$_{2(aq)}$ and total Si.
# 
# We can reveal how all the ctivities of all forms of these elements change with reaction progress - remember pH is changing and that could have effects on speciaiton.
# 
# Plot activity of basis and non-basis aqueous species as a function of reaction progress (Xi)

# In[ ]:


m.plot_aqueous_species(plot_basis=False)


# Given all those aqueous species, how does reactions progress affect changes in speciation?
# In this case, how does the speciation of aqueous SiO$_{2}$ change with Xi?

# In[ ]:


m.plot_mass_contribution("SiO2")


# ## Tables

# Print a list of available tables.

# In[ ]:


m.print_tabs()


# Display Table P by copy-pasting its full name from the list above

# In[ ]:


m.tab["Table P Moles of product minerals"]


# Display Table D1 in the same way

# In[ ]:


m.tab["Table D1 Solute basis species(total molality)"]


# Display a table of the log activity of aqueous species at different values of Xi. The `.head()` means only the first five rows are displayed in the notebook.

# In[ ]:


m.aq_distribution.head()


# Documentation is available for any function by including `?` at the end of the function name. For instance, here is the documentation for the `AqEquil.Reactant` function used earlier in the notebook to define forsterite and fayalite as minerals to react with speciated fluids:

# In[ ]:


get_ipython().run_line_magic('pinfo', 'AqEquil.Reactant')


# In[ ]:




