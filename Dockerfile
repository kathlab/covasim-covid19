# syntax=docker/dockerfile-upstream:master-labs
FROM ubuntu:jammy

# ______     ______     ______   ______     ______     ______   __  __    
# /\  == \   /\  ___\   /\  == \ /\  == \   /\  __ \   /\  == \ /\ \_\ \   
# \ \  __<   \ \  __\   \ \  _-/ \ \  __<   \ \ \/\ \  \ \  _-/ \ \____ \  
#  \ \_\ \_\  \ \_____\  \ \_\    \ \_\ \_\  \ \_____\  \ \_\    \/\_____\ 
#   \/_/ /_/   \/_____/   \/_/     \/_/ /_/   \/_____/   \/_/     \/_____/ 

### args
ARG PROJECT="covasimcovid19"
ARG PACKAGES="git libjpeg-turbo8 ca-certificates"

### reproducible python (repropy)
# based on mamba: https://github.com/conda-forge/miniforge
ARG REPROPY_DIR="/repropy"
ARG REPROPY_ENV="${PROJECT}"
ARG REPROPY_PREFIX="${REPROPY_DIR}"
ARG REPROPY_REQS="requirements.yaml"
ARG REPROPY_VERSION="24.11.0-1"
ARG REPROPY_ARCH="Linux-x86_64"
ARG REPROPY_SETUP="Miniforge3-${REPROPY_VERSION}-${REPROPY_ARCH}.sh"
ARG REPROPY_URL="https://github.com/conda-forge/miniforge/releases/download/${REPROPY_VERSION}/${REPROPY_SETUP}"

### setup env for using conda
ENV PATH="${REPROPY_PREFIX}/bin:${PATH}"
ENV LD_LIBRARY_PATH="${REPROPY_PREFIX}/lib/:\$LD_LIBRARY_PATH"

### covasim
ARG COVASIM_DIR=/covasim
# ARG COVASIM_WEBAPP="https://github.com/InstituteforDiseaseModeling/covasim_webapp.git"
ARG COVASIM_APP="https://github.com/InstituteforDiseaseModeling/covasim.git"
ARG COVASIM_APP_TAG="v3.1.4"  # add empty string to clone latest files

### install packages
RUN apt update && apt install -y ${PACKAGES}

# install Mambaforge
ADD --checksum=sha256:936836bb2dd546a7ab5999bed2a2d1ce8416c5359e28199df8b384529a85dcac ${REPROPY_URL} /
RUN chmod a+x /${REPROPY_SETUP}
RUN /bin/bash /${REPROPY_SETUP} -b -p ${REPROPY_PREFIX}

# update conda if current version is not up-to-date (recommended by mamba)
RUN conda update -n base -c conda-forge conda

### setup mamba environment
COPY ${REPROPY_REQS} /tmp/${REPROPY_REQS}

### add default container user
RUN groupadd -g 1000 vscode
RUN useradd -rm -d /home/vscode -s /bin/bash -g root -G sudo -u 1000 vscode

## fix directory rights
RUN chown --recursive vscode:vscode ${REPROPY_DIR}/

### setup default mamba environment for vscode user
USER vscode
RUN mamba env create -n ${REPROPY_ENV} -f /tmp/${REPROPY_REQS}
RUN mamba shell init -s bash
RUN echo "mamba activate ${REPROPY_ENV}" >> /home/vscode/.bashrc

# switch back to root
USER root

### by default activate custom mamba env (root)
# necessary to run on HPCs
RUN echo "mamba activate ${REPROPY_ENV}" >> /root/.bashrc

###############################################################################
# add custom commands here

# all following RUNs should run in a real login shell and activated conda environment
SHELL [ "mamba", "run", "-n", "covasimcovid19", "/bin/bash", "--login", "-c" ]

### create covasim webapp directory
RUN mkdir ${COVASIM_DIR}

### install covasim
RUN git clone --depth=1 -b ${COVASIM_APP_TAG} ${COVASIM_APP} ${COVASIM_DIR}/covasim
# fix: no tags, no releases, unmaintained -> deactivated
# RUN git clone --depth=1 ${COVASIM_WEBAPP} ${COVASIM_DIR}/webapp

# install covasim
WORKDIR ${COVASIM_DIR}/covasim
RUN python3 -m pip install .

# bytecode compile python libraries to improve startup times
RUN python3 -m compileall $(python3 -c "import covasim,os;print(os.path.dirname(covasim.__file__))" | tail -n 1)

# scrapers
# fix: fails scraper if directory does not exist
RUN mkdir -p /covasim/covasim/data/epi_data/ecdp/
# fix: 2 of 3 urls broken (load_corona_data_scraper_data.py points to a scam domain)
# RUN cd data && ./run_scrapers
RUN cd data && python3 load_ecdp_data.py

### install covasim webapp
# WORKDIR ${COVASIM_DIR}/webapp
# RUN python3 -m pip install .

# end of custom commands
###############################################################################

# change workdir to make notebooks browseable in jupyter notebooks
WORKDIR /workspaces

### setup volumes

# jupyter notebooks
VOLUME [ "/notebooks" ]

# vscode workspace
VOLUME [ "/workspaces/${PROJECT}" ]

# vscode extensions
VOLUME [ "/home/vscode/.vscode-server"]

# document ports
EXPOSE 8888/tcp
EXPOSE 8889/tcp

### set container entry
# ENTRYPOINT [ "/bin/bash" ]