import numpy as np
import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform
from pycbc.types import TimeSeries

# --- Chi Particle Simulation ---

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
        return 1 - np.exp(-self.cross_section * particle_density * distance)

class ChiParticleSimulation:
    def __init__(self, particle_density, distance, num_particles):
        self.chi_particle = ChiParticle()
        self.particle_density = particle_density
        self.distance = distance
        self.num_particles = num_particles

    def run(self):
        interaction_prob = self.chi_particle.interaction_probability(
            self.particle_density, self.distance
        )
        interactions = np.random.binomial(self.num_particles, interaction_prob)
        return interactions

    def analyze_results(self, interactions):
        interaction_rate = interactions / self.num_particles
        return {
            "num_particles": self.num_particles,
            "interaction_prob": self.chi_particle.interaction_probability(
                self.particle_density, self.distance
            ),
            "interactions": interactions,
            "interaction_rate": interaction_rate,
        }

# --- Gravitational Wave Simulation ---

def simulate_bh_merger():
    m1 = 36.0
    m2 = 29.0
    spin1z = 0.4
    spin2z = 0.3
    inclination = np.pi / 4
    distance = 410.0
    f_lower = 20.0

    hp, hc = get_td_waveform(
        approximant="SEOBNRv4_opt",
        mass1=m1,
        mass2=m2,
        spin1z=spin1z,
        spin2z=spin2z,
        inclination=inclination,
        distance=distance,
        f_lower=f_lower,
        delta_t=1.0 / 4096,
    )
    return hp

def inject_residuals(waveform, residual_template_path):
    residuals = np.loadtxt(residual_template_path, skiprows=1)
    residual_waveform = TimeSeries(
        residuals[:, 1], delta_t=waveform.delta_t, epoch=waveform.start_time
    )
    residual_waveform.resize(len(waveform))
    start_index = len(waveform) - len(residual_waveform)
    waveform[start_index:] += residual_waveform
    return waveform

# --- Analysis Framework ---

class AnalysisFramework:
    def __init__(self):
        self.results = {}

    def run_chi_particle_simulation(self, particle_density, distance, num_particles):
        chi_sim = ChiParticleSimulation(particle_density, distance, num_particles)
        interactions = chi_sim.run()
        self.results["chi_particle"] = chi_sim.analyze_results(interactions)

    def run_gravitational_wave_simulation(self, residual_template_path):
        waveform = simulate_bh_merger()
        waveform_with_residuals = inject_residuals(
            waveform.copy(), residual_template_path
        )
        self.results["gravitational_wave"] = {
            "original_waveform": waveform,
            "waveform_with_residuals": waveform_with_residuals,
        }

    def plot_results(self):
        # Plot chi particle results
        chi_results = self.results.get("chi_particle")
        if chi_results:
            num_particles = chi_results["num_particles"]
            plt.figure(figsize=(10, 6))
            plt.bar(
                ["Interactions", "No Interactions"],
                [chi_results["interactions"], num_particles - chi_results["interactions"]],
            )
            plt.title("Chi Particle Interactions")
            plt.ylabel("Number of Particles")
            plt.savefig("interactions.png")
            print("\nSaved chi particle interaction plot to interactions.png")

        # Plot gravitational wave results
        gw_results = self.results.get("gravitational_wave")
        if gw_results:
            waveform = gw_results["original_waveform"]
            waveform_with_residuals = gw_results["waveform_with_residuals"]
            plt.figure(figsize=(12, 6))
            plt.plot(waveform.sample_times, waveform, label="Original Waveform")
            plt.plot(
                waveform_with_residuals.sample_times,
                waveform_with_residuals,
                label="Waveform with Residuals",
                alpha=0.7,
            )
            plt.xlabel("Time (s)")
            plt.ylabel("Strain")
            plt.title("Gravitational Waveform from a Binary Black Hole Merger")
            plt.legend()
            plt.savefig("gravitational_wave_comparison.png")
            print("\nSaved gravitational wave comparison plot to gravitational_wave_comparison.png")

# --- Main ---

def main():
    framework = AnalysisFramework()

    # Run simulations
    framework.run_chi_particle_simulation(1e-5, 1e24, 1000000)
    framework.run_gravitational_wave_simulation("residual_template.dat")

    # Plot results
    framework.plot_results()

    # Print results
    print("\n--- Simulation Results ---")
    for sim, results in framework.results.items():
        print(f"\n{sim.replace('_', ' ').title()}:")
        if isinstance(results, dict):
            for key, value in results.items():
                if not isinstance(value, (np.ndarray, TimeSeries)):
                    print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
