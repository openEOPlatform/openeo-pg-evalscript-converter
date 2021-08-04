### Running notebooks

```
pipenv install --dev
```
 
Black will fail, run

```
pipenv lock --pre
```

```
pipenv run setup.py install
```

Start the notebooks

```
pipenv run jupyter notebook
```