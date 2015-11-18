__author__ = 'imalkov'
import pandas as pnd
import itertools
from argparse import ArgumentParser
import os

map_rule = {
    'natalia': lambda x: False,
    'sofia': lambda x: False,
    'jihan': lambda x: False,
    'marina': lambda x: False
}

index = pnd.MultiIndex.from_arrays([['sunday','sunday','sunday','sunday',
                                    'monday', 'monday','monday', 'monday',
                                    'tuesday', 'tuesday','tuesday', 'tuesday',
                                    'wednesday','wednesday','wednesday','wednesday',
                                    'thursday','thursday','thursday','thursday',
                                    'friday','friday'],
                                   ['morning', 'morning','evening', 'evening',
                                    'morning', 'morning','evening', 'evening',
                                    'morning', 'morning','evening', 'evening',
                                    'morning', 'morning','evening', 'evening',
                                    'morning', 'morning','evening', 'evening',
                                    'morning', 'morning'],
                                   ['employee 1','employee 2', 'employee 1','employee 2',
                                    'employee 1','employee 2', 'employee 1','employee 2',
                                    'employee 1','employee 2', 'employee 1','employee 2',
                                    'employee 1','employee 2', 'employee 1','employee 2',
                                    'employee 1','employee 2', 'employee 1','employee 2',
                                    'employee 1','employee 2']])
count_success = 0

def genpairs(l):
    res = []
    for n, el in enumerate(l):
        for sec_el in l[n + 1:]:
            res.append((el, sec_el))
    # print(res)
    return res


def is_consistent(solution, n):
    if n % 2 == 1 and n != len(solution):
        res = all(map_rule[name](solution[n], n) and
                  name not in solution[n-1]
                  for name in solution[n])
    else:
        res = all(map_rule[name](solution[n], n)
                   for name in solution[n])
    return res

def sidur_exec(solution, workers, pnd_data_frame, min_num, n):
    if len(solution) == n:
        s = pnd.Series(data=list(itertools.chain.from_iterable(solution)), index= index)
        if s.value_counts().argmax() == 'natalia' and s.value_counts().std() <= 1:
            if s.value_counts()['natalia'] >= min_num:
                pnd_data_frame['var_{0}'.format(pnd_data_frame.shape[1] + 1)] = s
    else:
        for tup in workers:
            solution[n] = tup
            if is_consistent(solution, n):
                sidur_exec(solution, workers, pnd_data_frame, min_num, n + 1)

def update_rules():
    global map_rule
    map_rule['natalia'] = lambda wrkrs, shift: 'marina' not in wrkrs
    map_rule['jihan'] = lambda wrkrs, shift: shift != 0
    map_rule['marina'] = lambda wrkrs, shift: 'natalia' not in wrkrs
    map_rule['sofia'] = lambda wrkrs, shift: (shift != 2 * 1 + 1) and (shift != 2 * 3 + 1)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-n", dest="min_num", help="configuration file for exucution states")
    kvargs = parser.parse_args()

    wrk_week = list(range(5 * 2 + 1))
    wrk_names = ['natalia', 'sofia', 'jihan', 'marina']
    update_rules()
    pnd_data_frame = pnd.DataFrame(data=None)
    sidur_exec(wrk_week, genpairs(wrk_names),pnd_data_frame, int(kvargs.min_num), 0)
    # pnd_data_frame.head()
    print(pnd_data_frame.shape)
    path = '/home/imalkov/Documents/pycharm_workspace/sidur/shifts_{0}_min{1}.csv'.format(os.getpid(),kvargs.min_num)
    print('saving to: {0}'.format(path))
    pnd_data_frame.to_csv(path)