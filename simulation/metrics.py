# simulation/metrics.py

def build_episode_results(world, brains=None) -> dict:

    results = world.summary()

    if brains:

        malformed_rates = {}

        for agent_id, brain in brains.items():

            if hasattr(brain, "malformed_rate"):

                malformed_rates[agent_id] = (
                    brain.malformed_rate
                )

        results["malformed_rates"] = malformed_rates

    return results