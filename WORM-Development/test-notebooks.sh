cd ..
source /opt/conda/etc/profile.d/conda.sh
conda run -n python3 pytest --nbval 1-Introduction/1-Introduction.ipynb
conda run -n python3 pytest --nbval 1-Introduction/2-Notebook-Intro.ipynb
conda run -n python3 pytest --nbval 2-Reaction-Properties/1-Reaction-Properties.ipynb
conda run -n python3 pytest --nbval 2-Reaction-Properties/2-Activity-Diagrams.ipynb
conda run -n python3 pytest --nbval 3-Aqueous-Speciation/1-Introduction-to-Aq-Speciation/1-Intro-to-Aq-Speciation.ipynb
conda run -n python3 pytest --nbval 3-Aqueous-Speciation/1-Introduction-to-Aq-Speciation/2-Intro-to-Multi-Aq-Speciation.ipynb
conda run -n python3 pytest --nbval 3-Aqueous-Speciation/2-Multi-Sample-Speciation/Multi-Sample-Speciation.ipynb
conda run -n python3 pytest --nbval 3-Aqueous-Speciation/3-Charge-Balancing/Charge-Balancing.ipynb
conda run -n python3 pytest --nbval 4-Custom-Database/Custom-Database.ipynb
conda run -n python3 pytest --nbval 5-Extras/speciate-3i-file/speciate-3i-file.ipynb