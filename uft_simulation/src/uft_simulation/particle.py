import numpy as np

class ChiParticle:
    def __init__(self):
        self.mass = 98.4  # GeV
        self.type = "Majorana fermion singlet"
        self.origin = "Emergent from AF's extended symmetry"
        self.stability = "Protected by Z2 discrete symmetry"
        self.cross_section = 1e-45  # Example weak-scale cross-section in cm^2

    def __repr__(self):
        return (
            f"ChiParticle(mass={self.mass} GeV, type='{self.type}', "
            f"origin='{self.origin}', stability='{self.stability}', "
            f"cross_section='{self.cross_section}')"
        )

    def interaction_probability(self, particle_density, distance):
        """
        Calculates the probability of a chi particle interacting with other particles.

        Args:
            particle_density (float): The density of particles in the medium (particles/cm^3).
            distance (float): The distance the chi particle travels through the medium (cm).

        Returns:
            float: The probability of an interaction.
        """
        return 1 - np.exp(-self.cross_section * particle_density * distance)
