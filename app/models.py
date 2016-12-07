from collections import namedtuple

# temporary mock database
Journey = namedtuple('Journey', 'id name start finish stages')
mockDB = {
    1: Journey(1, "trial run", (-10, 10), (-150, 150), []),
    2: Journey(2, "ncl -> sun", (54.978252, -1.61778), (54.906869, -1.383801), [2450, 1376, 4409])
}
