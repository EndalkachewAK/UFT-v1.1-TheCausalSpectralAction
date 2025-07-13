from src.uft_simulation.simulation import Simulation
import matplotlib.pyplot as plt

def main():
    # Simulation parameters
    particle_density = 1e-5  # particles/cm^3 (typical for dark matter)
    distance = 1e24  # cm (a large cosmological distance)
    num_particles = 1000000

    # Create and run the simulation
    sim = Simulation(particle_density, distance, num_particles)
    interactions = sim.run()
    results = sim.analyze_results(interactions)

    # Print the results
    print("Simulation Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")

    # Visualize the results
    plt.figure(figsize=(10, 6))
    plt.bar(
        ["Interactions", "No Interactions"],
        [results["interactions"], num_particles - results["interactions"]],
    )
    plt.title("Chi Particle Interactions")
    plt.ylabel("Number of Particles")
    plt.savefig("interactions.png")
    print("\nSaved a plot of the interaction results to interactions.png")

if __name__ == "__main__":
    main()
