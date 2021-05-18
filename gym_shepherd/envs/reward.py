from scipy.spatial import distance
from math import sqrt

# funkcija dist_herd_center sprejme položaj ovc in izračuna njihovo središče
# vrne (x,y) kooridnato središča in najdaljšo izmed razdalj ovc do središča
def dist_herd_center(herd):
    seznam_x = list(map(lambda i: i[0], herd))
    seznam_y = list(map(lambda i: i[1], herd))
    x = sum(seznam_x)/len(seznam_x)
    y = sum(seznam_y)/len(seznam_y)
    center = (x,y)
    distances = []
    for i in range(len(herd)):        
        distances.append(distance.euclidean(herd[i], center))
    return center, max(distances)

# funkcija dist_herd_dog izračuna razdaljo vsake ovce do psa in vrne najkrajšo razdaljo
def dist_herd_dog(herd, dog):
    distances = []
    for i in range(len(herd)):        
        distances.append(distance.euclidean(herd[i], dog))
    return min(distances)


# funcija closenes_sheep_sheep sprejme seznam ovc, velikost polja in radij za ovce pri katerem je dosežen cilj
# vrne nagrado glede na stanje razpršenosti ovc (glede na to koliko je najdaljša razdalja ovce do njihovega središča)
# razpon vrednosti je (goal_radius, diagonala polja)
def closenes_sheep_sheep(herd, field_size, goal_radius):
    h = (field_size*sqrt(2)-goal_radius)/4
    center, max_distance = dist_herd_center(herd)
    max_distance = max_distance - goal_radius
    if (max_distance >= 0 ) and (max_distance <= h):
        reward = 1
    elif (max_distance > h ) and (max_distance <= 2*h):
        reward = 0.75
    elif (max_distance > 2*h ) and (max_distance <= 3*h):
        reward = 0.25
    elif (max_distance > 3*h ) and (max_distance <= 4*h):
        reward = 0
    else:
        reward = 100
        print("Distance < 0, done.")

    return reward

# funkcija closenes_sheep_dog sprejme seznam ovc, pozicijo psa, velikost polja in razdaljo pri kateri pes vpliva na ovce
# izračuna razdaljo psa do najbližje ovce in vrne temu primerno nagrado
# razpon je (dog_impact, diagonala polja)
def closenes_sheep_dog(herd, dog, field_size, dog_impact):
    h = (field_size*sqrt(2)-dog_impact)/4
    min_distance = dist_herd_dog(herd, dog)
    min_distance = min_distance - dog_impact
    if (min_distance > 0 ) and (min_distance <= h):
        reward = 1
    elif (min_distance > h ) and (min_distance <= 2*h):
        reward = 0.75
    elif (min_distance > 2*h ) and (min_distance <= 3*h):
        reward = 0.25
    elif (min_distance > 3*h ) and (min_distance <= 4*h):
        reward = 0
    else:
        reward = 1
        print("Dog can impact herd.")

    return reward

# funkcija areas sprejme pozicije ovc in pozicijo psa ter prešteje v koliko območjih okoli psa se nahajajo ovce. 
# vrne nagrado glede na število območij.
def areas(herd, dog, field_size):
    rewards = {1:1, 2:0.75, 3:0.25,4:0}
    herd = list(map(lambda i: (i[0], field_size-i[1]), herd))
    dog = (dog[0], field_size - dog[1])
    point1 = (dog[0] + 1,dog[1]+1)
    point2 = (dog[0] - 1,dog[1]+1)
    seznam_up = []
    seznam_down = []
    seznam_left = []
    seznam_right = []
    nic = 0
    #d=(x-x1)(y2-y1) - (y-y1)(x2-x1)
    for i in herd: 
        d1 = (i[0]-dog[0])*(point1[1]-dog[1]) - (i[1]-dog[1])*(point1[0]-dog[0])
        d2 = (i[0]-dog[0])*(point2[1]-dog[1]) - (i[1]-dog[1])*(point2[0]-dog[0])
        if (d1 < 0) and (d2 >= 0):
            seznam_up.append(i)
        elif (d1 >= 0) and (d2 > 0):
            seznam_right.append(i)
        elif (d1 > 0) and (d2 <= 0):
            seznam_down.append(i)
        elif (d1 <= 0) and (d2 < 0):
            seznam_left.append(i)
        else: nic += 1
    seznam = [seznam_up, seznam_right, seznam_down, seznam_left]
    no_of_areas = 0
    for j in seznam:
        if len(j) != 0:
            no_of_areas += 1

    reward = rewards[no_of_areas]

    return reward

# parametri
"""
herd = [(13, 10), (6, 14), (14, 1), (2, 7), (15, 16), (9, 5), (12, 12), (1, 8), (7, 19), (8, 2)]
dog = (5,5)
goal_radius = 1
field_size = 20
dog_impact = 5 #razdalja pri kateri pes vpliva na ovce
print(closenes_sheep_sheep(herd, field_size, goal_radius), "sheep-sheep")
print(closenes_sheep_dog(herd, dog, field_size, dog_impact), "sheep-dog")
print(areas(herd, dog),"areas")
"""