#!/usr/bin/env python

"""
For any given version, say a.b.c.d, we can derive a numeric equivalent with
following constraints:
  - Resultant number must be unique for all possible values of a, b, c and d
  - Each of a, b, c and d needs to be below certain maximum unsigned int guided
    by max possible bits allotted to each version component
  - We should be able to derive unique a.b.c.d back from given number
  - If a.b.c.d => x and p.q.r.s => y then, a.b.c.d < p.q.r.s => x < y

This module solves the problem!
"""

import sys


class HashVerException(BaseException):
    pass


class HashVer(object):

    def __init__(self, bits_per_component=[16, 16, 16]):
        """
        `bits_per_component` indicates the number of numeric components a
        version string may have and max numeric value held by each component.
        e.g. [16, 16, 16] implies version string of format a.b.c where values
        in a, b and c are within range [0, 2^16)
        """
        if isinstance(bits_per_component, str):
            self.bits_per_component = [
                int(x) for x in bits_per_component.split('.')
            ]
        else:
            self.bits_per_component = bits_per_component

    def get_num(self, version_str):
        """
        Returns a numeric value for a given version_str based on contents of
        `bits_per_component`.
        Raises HashVerException upon parsing or compatibility error.
        """
        try:
            bpc = self.bits_per_component
            # this will store numeric value for each component
            vpc = []

            components = version_str.split('.')
            for comp in components[:-1]:
                try:
                    vpc.append(int(comp))
                except Exception as err:
                    msg = (
                        'All version components except the last one  must be a'
                        ' numeric value. Current component value: %s: %s'
                    ) % (str(comp), str(err))

                    raise HashVerException(msg)

            # since semver supports alphanumeric suffix for the last component,
            # extract first occuring numeric value before `-`. e.g. 0.0.1.8-rc1
            try:
                vpc.append(int(components[-1].split('-')[0]))
            except Exception as err:
                msg = (
                    'Value of last component can only be a numeric value or a '
                    'hyphen separated alphanumeric like 8-rc1. Current value: '
                    '%s: %s'
                ) % (str(components[-1]), str(err))

                raise HashVerException(msg)

            if len(bpc) != len(vpc):
                msg = '%s must have as many dot separated components as %s' % (
                    version_str, str(bpc)
                )
                raise HashVerException(msg)

            num = 0
            shift = False
            for cur_val, num_of_bits in zip(vpc, bpc):
                if shift:
                    num = num << num_of_bits
                else:
                    shift = True
                num += cur_val

            return num
        except Exception as err:
            msg = 'Parsing Error: %s' % str(err)
            raise HashVerException(msg)

    def get_version_str(self, num):
        """
        Returns a version string for a given numeric value based on contents of
        `bits_per_component`.
        Raises HashVerException upon parsing or compatibility error.
        """
        try:
            bpc = self.bits_per_component
            mut_num = num
            components = []
            for num_of_bits in reversed(bpc):
                max_val = (2 ** num_of_bits) - 1
                components.insert(0, str(mut_num & max_val))
                mut_num = mut_num >> num_of_bits

            if mut_num:
                msg = '%d is not compatible with %s' % (num, str(bpc))
                raise HashVerException(msg)

            return '.'.join(components)
        except Exception as err:
            msg = 'Parsing Error: %s' % str(err)
            raise HashVerException(msg)


def main():
    if len(sys.argv) == 1:
        msg = (
            'Usage:\n %s %s X1 X2 ... Xn [--bpc version_str] \nWhere each Xi'
            ' must be a number or a version string and bpc represents bits per'
            ' component which indicates format of versioning in use.'
        ) % (sys.executable, sys.argv[0])

        print(msg)
    else:
        try:
            index = sys.argv.index('--bpc')
            bpc = sys.argv[index + 1]
            del sys.argv[index]
            del sys.argv[index]
        except ValueError:
            bpc = [16, 16, 16]

        hob = HashVer(bpc)
        for ver in sys.argv[1:]:
            try:
                if ver.isdigit():
                    ret = hob.get_version_str(int(ver))
                else:
                    ret = hob.get_num(ver)
                print('%s : %s' % (ver, str(ret)))
            except Exception as err:
                print("%s : ERROR: %s" % (ver, str(err)))


if __name__ == "__main__":
    main()
