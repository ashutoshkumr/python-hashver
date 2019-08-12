hashver
=======

Is a python module to derive a unique numeric value from a version string and vice versa, adhering to following constraints:
  - Resultant number must be unique for all possible values of a, b, c and d
  - Each of a, b, c and d needs to be below certain maximum unsigned int guided
    by max possible bits allotted to each version component
  - We should be able to derive unique a.b.c.d back from given number
  - If a.b.c.d => x and p.q.r.s => y then, a.b.c.d < p.q.r.s => x < y

### Usage

After performing **python -m pip install hashver**, execute python code as mentioned below.
```python
>>> from hashver import HashVer
>>> hob = HashVer()
>>> hob.get_num('1.0.6')
4294967302
>>> hob.get_version_str(8590000133)
2.1.5
>>> # if your version is of format a.b.c.d, each of which should be at most 2^16
>>> hob = HashVer(bits_per_component='16.16.16.16')
>>> hob.get_num('9.0.100.10')
2533274796949514
>>> hob.get_version_str(2533274796949514)
9.0.100.10
```

Or if you have curl,
```bash
curl -skL https://raw.githubusercontent.com/ashutoshkumr/python-hashver/master/hashver/hashver.py | python - 1.0.6 8590000133

1.0.6 : 4294967302
8590000133 : 2.1.5
```

### Modification and Testing

If any modification is done to hashver source, use following to validate changes,
```bash
# ensure various combinations of version string or number can be derived from each other
python -B ${hashver-root}/hashver.py 9.0.100.10 2533274796949514 --bpc 16.16.16.16

9.0.100.10 : 2533274796949514
2533274796949514: 9.0.100.10

# or simply add them to the existing test suite in hashver/test_hashver.py and run pytest
cd ${hashver-root} && pytest
```
