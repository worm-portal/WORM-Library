cd ..
source /opt/conda/etc/profile.d/conda.sh
conda run -n python3 pytest --nbval 1-Introduction/1-Introduction.ipynb
conda run -n python3 pytest --nbval 1-Introduction/2-Notebook-Intro.ipynb
conda run -n python3 pytest --nbval 2-Reaction-Properties/1-Reaction-Properties.ipynb
conda run -n python3 pytest --nbval 2-Reaction-Properties/2-Activity-Diagrams.ipynb
sudo chmod 600 /home/shock/repos/pytest-worm-library/worm-library