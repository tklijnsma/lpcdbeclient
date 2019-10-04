# LPC DBE Client

To set up the environment, first install `conda`, and run:

```
wget https://raw.githubusercontent.com/tklijnsma/lpcdbeclient/master/environment.yml
conda env create -f environment.yml
conda activate inferedge2
```

To install this package, either:

```
pip install lpcdbeclient
```

Or:

```
git clone https://github.com/tklijnsma/lpcdbeclient.git
pip install -e lpcdbeclient
```

To run:

```
wget https://www.dropbox.com/s/qb6tozu1gdrfdfu/test_file_0.h5?dl=1 -O test_file_0.h5
lpcdbe-run --testfile test_file_0.h5 -a test-module-kl3
```
