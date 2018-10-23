from flow.core.vehicles import Vehicles
from flow.controllers.car_following_models import IDMController
from flow.controllers.routing_controllers import GridRouter
from flow.core.params import SumoParams, EnvParams, InitialConfig, NetParams
from flow.core.experiment import SumoExperiment

from one_junction_scenario import OneJunctionScenario #scenario class
from gen_one_junction import OneJunctionGenerator #generator class
from crash import OneJuntionCrashEnv, ADDITIONAL_ENV_PARAMS



def main():
	#1. Create a Vehicle object containing the vehicles that will be in the simulation
	vehicles = Vehicles()
	vehicles.add(veh_id="idm",
             acceleration_controller=(IDMController, {}), ########### STILL HAVE TO CREATE THE CONTROLLER ###########
             routing_controller=(GridRouter, {}),
             num_vehicles=2)

	#2. Initite the parameters for a sumo simulation and the initial configurations of the simulation
	sumo_params = SumoParams(sim_step=0.1, render=True)

	edges_distribution = ['bottom', 'right'] #set the vehicles to just star on the bottom and right edges
	initial_config = InitialConfig(edges_distribution=edges_distribution, spacing='custom')


	#3. Set the environment parameter
	env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

	#4. Set the netfile parameters with the path to the .net.xml network file
	net_params = NetParams(netfile='/mnt/c/Users/caiof/Desktop/IC-Lancaster/TrafficBayesianDDQN/sumo/one_junction.net.xml')

	#5. Create instances of the scenario and environment
	scenario = OneJunctionScenario(  # we use the NetFileScenario scenario class for one junction scenario... 
	    name="test_NetFile_scenario",
	    generator_class=OneJunctionGenerator,  # ... as well as the newly netfile generator class
	    vehicles=vehicles,
	    net_params=net_params,
	    initial_config=initial_config
	)

	env = OneJuntionCrashEnv(env_params, sumo_params, scenario)

	#6. create a instance of a sumo experiment
	exp = SumoExperiment(env, scenario)

	#7. Run the sumo simulation for a set number of time steps
	exp.run(1, 1500)


if __name__ == "__main__":
    main()