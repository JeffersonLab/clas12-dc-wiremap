from __future__ import print_function

if __name__ == '__main__':
    from dc_tables import initialize_session
    from dc_fill_tables import dc_fill_tables
    from dc_queries import dc_find_connections

    print('connecting to database...')
    session = initialize_session()

    print('filling tables...')
    dc_fill_tables(session)

    find_connections = lambda **kw: dc_find_connections(session,**kw)

    parms = [
        dict(wire_type = 'sense'),
        dict(wire_type='sense',sector=0,superlayer=0,layer=0),
        dict(wire_type='sense',sector=0,superlayer=0,layer=0,wire=0),
    ]

    print('making queries:')
    for p in parms:
        print(p)
        print('   ',find_connections(**p))

    print('timing queries...')

    import timeit

    setup = '''\
from dc_tables import initialize_session
from dc_fill_tables import dc_fill_tables
from dc_queries import dc_find_connections
session = initialize_session()
dc_fill_tables(session)'''
    using_all = '''\
dc_find_connections.all = True
dc_find_connections(session)'''
    using_one = '''\
dc_find_connections.all = False
dc_find_connections(session)'''

    print('empty input')
    res = timeit.timeit(using_all,setup,number=20)
    print('  using all:',res)
    res = timeit.timeit(using_one,setup,number=20)
    print('  using one:',res)

    using_all = '''\
dc_find_connections.all = True
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0)'''
    using_one = '''\
dc_find_connections.all = False
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0)'''

    print('partial input')
    res = timeit.timeit(using_all,setup,number=20)
    print('  using all:',res)
    res = timeit.timeit(using_one,setup,number=20)
    print('  using one:',res)

    using_all = '''\
dc_find_connections.all = True
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0,layer=0,wire=0)'''
    using_one = '''\
dc_find_connections.all = False
dc_find_connections(session,wire_type='sense',sector=0,superlayer=0,layer=0,wire=0)'''

    print('full input')
    res = timeit.timeit(using_all,setup,number=20)
    print('  using all:',res)
    res = timeit.timeit(using_one,setup,number=20)
    print('  using one:',res)
