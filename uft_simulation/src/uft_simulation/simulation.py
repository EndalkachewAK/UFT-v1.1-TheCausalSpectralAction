from .particle import ChiParticle
import numpy as np

class Simulation:
    def __init__(self, particle_density, distance, num_particles):
        self.chi_particle = ChiParticle()
        self.particle_density = particle_density
        self.distance = distance
        self.num_particles = num_particles

    def run(self):
        """
        Runs the simulation and returns the number of interactions.
        """
        interaction_prob = self.chi_particle.interaction_probability(
            self.particle_density, self.distance
        )
        interactions = np.random.binomial(self.num_particles, interaction_prob)
        return interactions

    def analyze_results(self, interactions):
        """
        Analyzes the simulation results and returns a summary.
        """
        interaction_rate = interactions / self.num_particles
        return {
            "num_particles": self.num_particles,
            "interaction_prob": self.chi_particle.interaction_probability(
                self.particle_density, self.distance
            ),
            "interactions": interactions,
            "interaction_rate": interaction_rate,
        }
