# Start from a core stack version
FROM jupyter/allspark-notebook:latest
# Install from requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN mkdir -p /home/jovyan/.kaggle
COPY --chown=${NB_UID}:${NB_GID} .kaggle/kaggle.json /home/jovyan/.kaggle
RUN conda config --add channels anaconda
RUN conda config --add channels solutionsdev
RUN conda install --yes --file /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
