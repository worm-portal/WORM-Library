#!/usr/bin/env python
# coding: utf-8

# <left>
# <table style="margin-top:0px; margin-left:0px;">
# <tr>
#   <td><img src="https://raw.githubusercontent.com/worm-portal/WORM-Figures/master/style/worm.png" alt="WORM" title="WORM" width=50/></td>
#   <td><h1 style=font-size:30px>Mass Transfer and Reaction Paths</h1><h2>Breakout Session</h2></td>
# </tr>
# </table>
# </left>
# 
# Here are a couple of example activities involving water-rock reaction modeling. Pick the one that most interests you or go wild with your own ideas!
# 
# In case you need it, here is a link to [the WORM database table](https://tinyurl.com/wormdb). It can be helpful for looking up mineral names. Descriptions of columns and their units can be found in the [WORM database documentation](https://worm-portal.asu.edu/docs/database/). 
# 
# ---
# 
# ### Activity: Serpentinization, continued!
# 
# <img src="https://www.le-comptoir-geologique.com/_media/img/small/telechargement-6-2-2.png" alt="enstatite" title="enstatite" width=50%/>
# 
# [Enstatite](https://www.mindat.org/min-1384.html). Image credit: Y. Vessely
# <br/>
# 
# Forsterite can react with a pH 6 fluid to produce chrysotile and brucite. What happens if we change the Mg:Si ratio of the reactant mineral? Are different minerals produced? What happens to the pH of the fluid?
# 
# | Group | Mineral | Formula | Mg:Si | Reactive at surface conditions? | Product minerals | pH change? |
# |-------|---------|---------|-------|---------------------------------|------------------|------------|
# | olivine | forsterite | Mg2SiO4 | 2:1 | Yes | chrysotile, brucite | Big increase |
# | orthopyroxine | enstatite | MgSiO3 | 1:1 | Yes | ??? | ??? |
# | clinopyroxene | diopside | CaMgSi2O6 | 1:2 | No | ??? | ??? |
# 
# 1. Explore what is predicted to happen to these serpentinizing endmember minerals when they are reacted with speciated pH 6 fluid.
#     <ol type="a">
#       <li>Can you uncover the blanks in the table?</li>
#       <li>What can be said about Mg:Si in the types and abundance of product minerals?</li>
#     </ol><br>
#     
# 2. What happens when you react a rock made up of forsterite, enstatite, and diopside (each with ~0.33 mole fraction)?
# 
# ---
# 
# ### Activity: Destroyed by acid mine drainage!
# 
# <img src="https://files.structurae.net/files/photos/5256/2021-07-16/dsc03469.jpeg" alt="struts" title="Concrete Struts" width=50%/>
# Image credit: Nicolas Janberg
# <br/><br/>
# 
# The year is 2050. County officials in Shamokin, Pennsylvania are investigating reports of eroding infrastructure. The reports indicate degradation of the concrete struts that support a bridge spanning a large stagnant pond. An investigation reveals that polluted runoff from the abandoned Henry Clay Sterling Mine has contaminated the pond in contact with the struts.
# 
# A task force is assembled to gather evidence that the acid mine drainage is causing destruction of the bridge struts. It is your task to estimate the extent of the damage so the county can budget for bridge repair.
# 
# For every 10 kg of water in the pond, there is 1 mole of concrete in contact with water.
# 
# If there is < 10% disintegration of concrete volume after equilibration with the pond, then \\$1M will be needed to patch up the concrete. Any more than that and the struts will need to be completely replaced for \\$5M. What do you recommend based on your model?
# 
# Hint: assume portlandite (cement) is a stand-in for concrete.
# 
# (Acid mine drainage data is adapted from [Cravotta III 2008](https://doi.org/10.1016/j.apgeochem.2007.10.011))
# 
# ---
# 
# ### Activity: Lime the lake!
# 
# Honnedaga Lake in upstate New York is home to brook trout, *Salvelinus fontinalis*.
# 
# <img src="https://www.fws.gov/sites/default/files/styles/banner_image_xl/public/banner_images/2021-07/natdiglib_32715_full.jpg" alt="brook trout" title="Brook Trout" width=100%/>
# 
# Acidification of the lake from acid rain is suspected to have caused a marked decline in the population of brook trout [since the late 1960s](http://fish.dnr.cornell.edu/trout/honnedaga.htm).
# 
# You are investigating possible methods for improving the water quality of the lake. One technique for mitigating lake acidification is through a process called *liming*. This is where crushed agricultural limestone (CaCO$_3$) is spread evenly across the pond or lake with a barge. A crew of 3 can dispense around 10 tons of limestone per hour.
# 
# Model the water-rock reaction between Honnedaga Lake water and limestone.
# - What happens to the pH of the lake?
# - Acid rain has led to an increased concentration of dissolved sulfate in the lake. What happens to the speciation of sulfate when the lake is limed?
# - Why does the pH of the lake increase when limestone is added?
# - Lake Honnedaga has a surface area of 3.33 km$^2$ and an average depth of 15 m. About how many moles of limestone would be needed to saturate the lake? How many hours would it take a barge to dispense that much limestone?
# 
# Hint: assume limestone is mainly composed of calcite.
# 
# (Honnedaga Lake data is adapted from the [USGS Honnedaga Lake Tributary dataset](https://nwis.waterdata.usgs.gov/usa/nwis/qwdata/?site_no=0134277112&agency_cd=USGS&inventory_output=0&rdb_inventory_output=value&TZoutput=0&pm_cd_compare=Greater%20than&radio_parm_cds=all_parm_cds&format=html_table&qw_attributes=expanded&qw_sample_wide=separated_wide&rdb_qw_attributes=0&date_format=YYYY-MM-DD&rdb_compression=file&submitted_form=brief_list))
# 
# ---

# Load the AqEquil Python package.

# In[ ]:


import AqEquil


# Load the thermodynamic database. Organics are excluded here to cut down on calculation time.

# In[ ]:


ae = AqEquil.AqEquil(exclude_category={"category_1":["organic_aq", "organic_cr"]})


# Load water chemistry data from a CSV file and perform the speciation calculation. The formation of certain minerals can be suppressed here, if desired. 

# In[ ]:


speciation = ae.speciate(input_filename="pH6-8_fluids.csv",
                         alter_options=[["antigorite", "Suppress"]],
                         )


# Save the speciation as a file. This allows you to load the speciation whenever the notebook is opened or the kernel is restarted. Not having to re-run the speciation saves time.

# In[ ]:


speciation.save("serp")


# The notebook can be safely shut down or restarted and resumed from this point.

# In[ ]:


import AqEquil
speciation = AqEquil.load("serp")


# In[ ]:


For = AqEquil.Reactant(reactant_name="forsterite",
                       amount_remaining=1, # moles of mineral to react per kg H2O
                       f_rate_law='Relative rate equation', # forward rate law
                       f_eq1=1, # dXi(n)/dXi (mol/mol), the mole fraction of this mineral in the rock
                       b_rate_law="Partial equilibrium", # backward rate law
                       )

# combine the mineral reactants in a list to repare the reaction
r = AqEquil.Prepare_Reaction(reactants=[For])


# React the minerals with the speciated fluids.

# In[ ]:


speciation = AqEquil.react(speciation, r)


# The `lookup()` function can be used to look up many things about the speciation, including sample names.

# In[ ]:


speciation.lookup('name')


# Select one of the samples for analysis and plotting.

# In[ ]:


# get mass transfer data for a sample
m = speciation.mt("pH6")


# ## Available plot types

# Plot pH as a function of reaction progress (Xi)

# In[ ]:


m.plot_pH()


# Plot concentrations of dissolved elements as a function of reaction progress (Xi)

# In[ ]:


m.plot_elements(log=True)


# Plot activity of aqueous basis species as a function of reaction progress (Xi)

# In[ ]:


m.plot_aqueous_species(plot_basis=True)


# Plot activity of non-basis aqueous species as a function of reaction progress (Xi)

# In[ ]:


m.plot_aqueous_species(plot_basis=False)


# Plot moles of product minerals as a function of reaction progress (Xi)

# In[ ]:


m.plot_product_minerals(show_reactant_minerals=False, log_y=True, y_type='mole')


# Create an interactive reaction path diagram with desired species as x, y, and balance variables. (It might take a minute to load the plot.)
# 
# Once it is ready, hover your mouse over the plot to see more.
# 
# The red line and dots indicate the reaction path of the fluid. Open circles represent 'projections', where the point is above or below the plane in multidimensional space. Closed circles indicate points along the reaction path that are interacting with activity fields and/or saturation lines present in the diagram.
# 
# We recommend setting `calculate_projected_points=False` when you are visualizing a sample that has many elements (e.g., the Henry Clay Sterling Mine example). This is because calculating whether a point is projected involves looping through every permutation of x, y, and balance variables. The more elements present, the longer it takes to finish.

# In[ ]:


e = m.plot_reaction_paths(["SiO2","Mg+2", "Ca+2"], # x, y, and balance variables
                          flip_xy=False, # flip variables on x and y axes?
                          res=300, # 300 calculations per axis. Higher is slower but makes smoother region lines
                          minerals_to_show=["quartz"], # ensure certain mineral saturation lines will appear
                          calculate_projected_points=True, # set to False if there are many elements in the system
                         )[0].show()


# The next cell will plot reaction paths with all permutations of x, y, and balance variables. This might take a minute or more.
# 
# Running this cell is not recommended when you have many elements of the system (e.g., the Henry Clay Sterling acid mine drainage example). This is because there are too many permutations of x, y, and balance variables to plot in one notebook. The cell will probably never finish running! Instead, use the technique shown in the cell directly above to define x, y, and balance variables manually and skip the next cell.

# In[ ]:


fig_list = m.plot_reaction_paths(res=150, # resolution of background mineral stability field
                                 flip_xy=False, # flip variables on x and y axes?
                                 minerals_to_show=["quartz"], # ensure certain mineral saturation lines will appear
                                 calculate_projected_points=True, # set to False if there are many elements in the system
                                )

_ = [fig.show() for fig in fig_list]


# Plot mass contribution of a basis species across reaction progress (Xi).

# In[ ]:


m.plot_mass_contribution("SiO2")


# ## Tables

# Print a list of available tables.

# In[ ]:


m.print_tabs()


# Display Table P by copy-pasting its full name from the list above

# In[ ]:


m.tab["Table P Moles of product minerals"]


# #### Display Table D1 in the same way

# In[ ]:


m.tab["Table D1 Solute basis species(total molality)"]


# Display a table of the log activity of aqueous species at different values of Xi. The `.head()` means only the first five rows are displayed in the notebook.

# In[ ]:


m.aq_distribution.head()


# Documentation is available for any function by including `?` at the end of the function name. For instance, here is the documentation for the `AqEquil.Reactant` function used earlier in the notebook to define forsterite and fayalite as minerals to react with speciated fluids:

# In[ ]:


get_ipython().run_line_magic('pinfo', 'AqEquil.Reactant')


# In[ ]:




