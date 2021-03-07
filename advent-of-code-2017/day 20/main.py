"""Advent of Code 2017 Day 20."""
from collections import defaultdict
import re


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    particles = parse_particles(lines)
    particles_to_simulate = get_particles_with_lowest_acceleration(particles)
    closest_particle, _ = simulate_particles(particles_to_simulate, limit=1000)
    print(f'Closest particle in the long run: {closest_particle[1]}')
    _, particles = simulate_particles(parse_particles(lines), collisions=True)
    print(f'Number of not colliding particles: {len(particles)}')


def simulate_particles(particles, limit=None, collisions=False):
    """Simulate particles move.

    Up to limit, or until all particles have increasing distance."""
    closest_particle = None
    past_distances = get_particles_distances(particles)
    counter = 0
    while not limit or counter < limit:
        positions = defaultdict(list)
        for particle_number, particle in particles.items():
            update_particle(particle)
            particle_position = tuple(particle['position'])
            positions[particle_position].append(particle_number)
        if collisions and collide(particles, positions):
            particles = filter_active_particles(particles)
        distances = get_particles_distances(particles)
        particles_with_distance = [
            (distance, particle_number)
            for particle_number, distance in distances.items()]
        closest_particle = sorted(particles_with_distance)[0]
        if not limit and all_increasing(distances, past_distances):
            break
        counter += 1
    return closest_particle, particles


def filter_active_particles(particles):
    """Filter active particles from particles dict."""
    return {particle_number: particle
            for particle_number, particle in particles.items()
            if particle['active']}


def get_particles_distances(particles):
    """Get dict with particle_number: distance, for particles dict."""
    return {particle_number: get_distance(particle)
            for particle_number, particle in particles.items()}


def get_particles_with_lowest_acceleration(particles):
    """Get particles with lowest acceleration from particles."""
    particle_accelerations = [
        (sum(abs(num) for num in particle['acceleration']), particle_number)
        for particle_number, particle in particles.items()]
    minimum = sorted(particle_accelerations)[0][0]
    interesting_particles = [
        particle_number
        for acceleration, particle_number in particle_accelerations
        if acceleration == minimum]
    return {
        particle_number: particles[particle_number]
        for particle_number in interesting_particles}


def all_increasing(distances, past_distances):
    """Check if particles distances are all increasing."""
    for particle_number, distance in distances.items():
        if distance < past_distances[particle_number]:
            return False
    return True


def collide(particles, positions):
    """Mark colliding particles as not active.

    Returns True if any particles collide, otherwise returns False."""
    collisions = [collided for _, collided in positions.items()
                  if len(collided) > 1]
    if not collisions:
        return False
    for numbers in collisions:
        for number in numbers:
            particles[number]['active'] = False
    return True


def update_particle(particle):
    """Update particle's velocity and position."""
    for index, acceleration in enumerate(particle['acceleration']):
        particle['velocity'][index] += acceleration
        particle['position'][index] += particle['velocity'][index]
    return particle


def get_distance(particle):
    """Get Manhattan distance of particle."""
    return sum(abs(num) for num in particle['position'])


def parse_particles(lines):
    """Parse lines to dict with particles."""
    particles = {}
    for particle_number, line in enumerate(lines):
        particles[particle_number] = parse_particle(line)
    return particles


def parse_particle(line):
    """Parse line to dict particle."""
    regex = r'<(.*?)>'  # .*<([0-9+\-]+)>.*<([0-9+\-]+)>'
    position, velocity, acceleration = [[int(num) for num in part.split(',')]
                                        for part in re.findall(regex, line)]
    return {
        'position': position,
        'velocity': velocity,
        'acceleration': acceleration,
        'active': True,
    }


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
