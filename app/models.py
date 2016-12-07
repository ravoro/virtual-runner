from collections import namedtuple

# temporary mock database
Journey = namedtuple('Journey', 'id name start finish stages')
Coord = namedtuple('Coord', 'lat lng')
mockDB = {
    1: Journey(1, "trial run", Coord(50, 30), Coord(55, 25), []),
    2: Journey(2, "ncl -> sun", Coord(54.978252, -1.61778), Coord(54.906869, -1.383801), [2450, 1376, 4409])
}
