from django.test import TestCase

# Create your tests here.
all_times = {0: 1, 2: 3, 3: 2}
for d in range(len(all_times)):
    print(d)
    for k in all_times[d]:
        print(k)
