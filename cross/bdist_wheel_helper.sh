#!/bin/bash
set -e

# supported python verions
TARGET_PY_VER="35 36 37 38"

# build raw bdist_wheels
eval "$(~/miniconda3/bin/conda shell.bash hook)"
for ver in ${TARGET_PY_VER}; do
    conda activate py${ver}
    python setup.py bdist_wheel
    conda deactivate
done

# audit wheels
for whl in dist/*.whl; do
    auditwheel repair ${whl} \
      -w dist \
      --plat ${AUDITWHEEL_PLAT}
done
