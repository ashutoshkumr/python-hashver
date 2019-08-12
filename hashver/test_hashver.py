from hashver import HashVer


class TestHashVer(object):

    def test_compare_four_component_versions(self):
        builds = [
            '6.90.0.21',
            '8.13.1260.16',
            '8.20.1300.14',
            '8.20.1300.20',
            '8.20.1300.24',
            '8.21.1310.5',
            '8.30.1350.13',
            '8.30.1350.19',
            '8.31.1360.8',
            '8.40.1400.5',
            '8.40.1400.8',
            '8.40.1400.11',
            '8.41.1410.5',
            '8.42.1410.12',
            '8.42.1410.18',
            '8.50.1700.5',
            '8.50.1700.11',
            '8.51.1800.5',
            '8.51.1800.7',
            '8.52.1810.4',
            '9.0.0.50'
        ]

        bpc_list = [[16, 16, 16, 16], '8.8.16.8']

        for bpc in bpc_list:
            hob = HashVer(bpc)
            prev = 0
            for ver in builds:
                print('Testing %s with bpc %s' % (ver, str(bpc)))
                try:
                    num = hob.get_num(ver)
                    ver_str = hob.get_version_str(num)
                    assert ver == ver_str
                    assert prev < num
                    prev = num
                    print('PASSED')
                except Exception as err:
                    print('FAILED: %s => %d => %s: %s' % (
                        ver, num, ver_str, str(err))
                    )

    def test_compare_semvers(self):
        builds = [
            '0.0.1',
            '0.5.2',
            '0.6.3',
            '0.6.4-rc1',
            '1.5.1-rc2',
            '2.0.2'
        ]

        bpc_list = [[16, 16, 16], '8.8.16']

        for bpc in bpc_list:
            hob = HashVer(bpc)
            prev = 0
            for ver in builds:
                print('Testing %s with bpc %s' % (ver, str(bpc)))
                try:
                    num = hob.get_num(ver)
                    ver_str = hob.get_version_str(num)
                    assert ver.split('-')[0] == ver_str
                    assert prev < num
                    prev = num
                    print('PASSED')
                except Exception as err:
                    print('FAILED: %s => %d => %s: %s' % (
                        ver, num, ver_str, str(err))
                    )
