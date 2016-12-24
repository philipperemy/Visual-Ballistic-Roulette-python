from __future__ import print_function

from datetime import datetime

from computations.Wheel import *

# From games.mov 11.35GB

origin = datetime.strptime('00:00.000', '%M:%S.%f')


def str_to_recorded_times(string):
    out = []
    for elt in string.split():
        dt = (datetime.strptime(elt, '%M:%S.%f') - origin).total_seconds()
        out.append(dt)
    return np.diff(np.array(out))


def mix_all_times_together(l):
    max_len = max([len(v) for v in l])
    out = []
    for elt in l:
        out.append((max_len - len(elt)) * [0] + list(elt))
    return np.array(out)


BS_1 = str_to_recorded_times(
    '10:44.733 10:45.266 10:45.816 10:46.466 10:47.183 10:47.975 10:49.016 10:50.366 10:51.983 10:53.800 10:55.916 10:58.350 11:01.366 11:04.049')

WS_1 = str_to_recorded_times('10:48.083 10:54.100 10:59.749')

# 10 is the number when the ball enters the diamonds ring at 11:04.049.
# 28 is the outcome
# no diamonds hit. Screen shot at diamond_1.png

BS_2 = str_to_recorded_times(
    '12:17.516 12:17.999 12:18.516 12:19.100 12:19.733 12:20.399 12:21.200 12:22.200 12:23.516 12:25.150 12:26.933 12:29.066 12:31.583 12:34.666 12:37.066')

WS_2 = str_to_recorded_times('12:17.149 12:23.716 12:30.733')

# 16 is the number when the ball enters the diamonds ring at 12:37.066.
# 31 is the outcome
# Diamond no 4 hit. Screen shot at diamond_2.png

BS_3 = str_to_recorded_times(
    '13:55.750 13:56.499 13:57.383 13:58.466 13:59.883 14:01.666 14:03.649 14:05.866 14:08.466 14:11.616 14:14.083')
WS_3 = str_to_recorded_times('13:55.383 14:00.983 14:06.499')

# 4 is the number when the ball enters the diamonds ring at 14:14.083.
# 16 is the outcome
# No diamonds hit. Screen shot at diamond_3.png

BS_4 = str_to_recorded_times('15:44.983 15:46.683 15:48.666 15:50.900 15:53.650 15:57.050 15:59.483')
WS_4 = str_to_recorded_times('15:44.183 15:50.183 15:55.983')

# 2 is the number when the ball enters the diamonds ring at 14:14.083.
# 5 is the outcome
# No diamonds hit. Screen shot at diamond_4.png

BS_5 = str_to_recorded_times('17:27.700 17:29.183 17:30.849 17:32.733 17:34.899 17:37.516 17:40.833 17:42.000')
WS_5 = str_to_recorded_times('17:26.800 17:32.666 17:38.349')

# 26 is the number when the ball enters the diamonds ring at 14:14.083.
# 19 is the outcome
# Diamond no 2 hit. Screen shot at diamond_5.png

BS_6 = str_to_recorded_times(
    '19:04.100 19:04.866 19:05.816 19:07.049 19:08.583 19:10.333 19:12.299 19:14.683 19:17.550 19:21.216 19:22.266')
WS_6 = str_to_recorded_times('19:03.866 19:10.050 19:15.483 19:20.949')

# 5 is the number when the ball enters the diamonds ring at 19:22.266.
# 1 is the outcome
# Diamond no 2 hit. Screen shot at diamond_6.png

BS_7 = str_to_recorded_times(
    '20:43.666 20:44.183 20:44.783 20:45.366 20:46.099 20:46.983 20:47.999 20:49.366 20:50.966 20:52.783 20:54.833 20:57.249 21:00.216 21:04.016')
WS_7 = str_to_recorded_times('20:43.733 20:49.283 20:54.583 20:59.733')

# 7 is the number when the ball enters the diamonds ring at 21:04.016.
# 29 is the outcome
# Diamond no 0 hit. Screen shot at diamond_7.png


BS_8 = str_to_recorded_times(
    '22:13.499 22:13.833 22:14.266 22:14.683 22:15.083 22:15.566 22:16.066 22:16.566 22:17.183 22:17.766 22:18.483 22:19.333 22:20.366 22:21.750 22:23.366 22:25.166 22:27.299 22:29.800 22:33.000 22:35.333')
WS_8 = str_to_recorded_times('22:13.300 22:19.683 22:26.399 22:33.350')

# 12 is the number when the ball enters the diamonds ring at 22:35.333.
# 24 is the outcome
# No diamond hit. Screen shot at diamond_8.png

BS_9 = str_to_recorded_times('24:06.466 24:07.950 24:09.600 24:11.550 24:13.766 24:16.483 24:19.966 24:20.266')
WS_9 = str_to_recorded_times('24:05.716 24:11.550 24:17.099')

# 14 is the number when the ball enters the diamonds ring at 24:20.266.
# 19 is the outcome
# No diamond hit. Screen shot at diamond_9.png

BS_10 = str_to_recorded_times('25:36.600 25:38.083 25:39.749 25:41.649 25:43.799 25:46.466 25:49.666 25:52.083')
WS_10 = str_to_recorded_times('25:36.116 25:41.833 25:47.816')

# 36 is the number when the ball enters the diamonds ring at 25:52.083.
# 2 is the outcome
# Diamond 4 hit. Screen shot at diamond_10.png

BS_11 = str_to_recorded_times(
    '27:16.233 27:17.500 27:19.066 27:20.849 27:22.866 27:25.133 27:27.900 27:31.183 27:31.733')
WS_11 = str_to_recorded_times('27:15.800 27:22.033 27:28.166')

# 9 is the number when the ball enters the diamonds ring at 27:31.733.
# 36 is the outcome
# No diamonds hit. Screen shot at diamond_11.png

X = mix_all_times_together([BS_1, BS_2, BS_3, BS_4, BS_5, BS_6, BS_7, BS_8, BS_9, BS_10, BS_11])

import matplotlib.pyplot as plt

plt.plot(np.transpose(X))
plt.show()

print(Wheel.distance_between_numbers(10, 28))
