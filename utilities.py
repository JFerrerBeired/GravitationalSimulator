import math

def get_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def normalize_angle(angle):
    '''Converts an angle (in radians) to the (-pi, pi] interval.'''
    
    if angle == math.pi: return angle
    return angle - 2 * math.pi * (angle//math.pi)

def get_quadrant(angle):
    '''Get the quadrant of an angle (in radians) and return it.
    
    The angle has to be in the (-pi, pi] interval (use normalize_angle).'''
    
    if(angle < 0): angle += 2*math.pi
    
    return angle // (math.pi/2) + 1