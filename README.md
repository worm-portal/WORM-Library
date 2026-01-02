# worm_library

Download Water-Organic-Rock-Microbe (WORM) Portal tutorial notebooks and demo files to your local environment.

## Installation

```bash
pip install worm_library
```

## Quick Start

After installation, run this in your computer's terminal to download the WORM-Library notebook to your current directory and launch Jupyter Lab:

**Windows:**
```powershell
python -c "import worm_library; worm_library.get_library_notebook()"; jupyter lab WORM-Library.ipynb
```

**Mac/Linux:**
```bash
python -c "import worm_library; worm_library.get_library_notebook()" && jupyter lab WORM-Library.ipynb
```

This should open the WORM-Library notebook in your Jupyter Lab in your browser. It allows you to download the latest versions of WORM tutorials by running cells containing the desired tutorials.

Click on a cell with a tutorial that you want and then run it (`SHIFT+ENTER` while the cell is selected). When it is finished running, it will display a message saying that the tutorial is ready. Check the file browser for the tutorial folder that was downloaded. Double click on the folder to open it and access the downloaded tutorial notebook(s).

If you quit Jupyter Lab and want to return to it later, open your terminal and enter:

```bash
jupyter lab WORM-Library.ipynb
```

## Usage

It is easiest for new users to use the WORM-Library.ipynb notebook to download desired tutorials.

More advanced users can use Python in a terminal to access demos:

```python
import worm_library

# Download the main WORM-Library notebook (index of all tutorials)
worm_library.get_library_notebook()

# Download specific tutorials
worm_library.get_introduction_demo()            # Basic introduction
worm_library.get_reaction_properties_demo()     # Reaction properties tutorials
worm_library.get_univariant_curve_demo()        # Univariant curves / geothermometry

# Aqueous speciation tutorials
worm_library.get_intro_aqueous_speciation_demo()
worm_library.get_multi_aqueous_speciation_demo()
worm_library.get_charge_balance_demo()
worm_library.get_heterogeneous_equilibrium_demo()
worm_library.get_heterogeneous_equilibrium_gas_demo()
worm_library.get_alter_suppress_demo()
worm_library.get_custom_data0_demo()
worm_library.get_EQ3_demo()
worm_library.get_EQ6_demo()

# Mass transfer tutorials
worm_library.get_intro_mass_transfer_demo()
worm_library.get_mass_transfer_feature_demo()
worm_library.get_mixing_demo()

# Additional tutorials
worm_library.get_speciation_datasets_demo()
worm_library.get_energy_supply_demo()

# Thermodynamic property estimation
worm_library.get_intro_aqorg_demo()
worm_library.get_aqorg_feature_demo()
worm_library.get_complicator_demo()
worm_library.get_estimate_HKF_demo()

# Community notebooks
worm_library.get_Weeks_2025_demo()
worm_library.get_Trinh_2026_demo()
worm_library.get_whats_in_water_demo()

# Workshop materials
worm_library.get_workshop_demo("workshop_name")

# Clean up all downloaded demos
worm_library.delete_all_demos()
```

Each function downloads the relevant notebooks and data files to a `Demo-*` folder in your current working directory.

## Links

- [WORM Portal](https://worm-portal.asu.edu/)
- [Full Tutorial Library on GitHub](https://github.com/worm-portal/WORM-Library)

## License

MIT License - see [LICENSE](LICENSE) for details.
