class Agent:
    def __init__(self):
        self.program = lambda percept: None

    def sense(self, env):
        self.percept = env.getPercept(self)

    def run_once(self, env):
        self.sense(env)
        action = self.program(self.percept)
        env.apply_action(action)


class SimpleReflexVacuumAgent(Agent):
    def __init__(self):
        super().__init__()
        self.location = 'A'   
        def program(percept):
            location, status = percept
            if status == 'Dirty':
                return 'Suck'
            else:

                return 'Right' if location == 'A' else 'Left'

        self.program = program


class VacuumEnvironment:
    def __init__(self, agent, initial_state=None, verbose=True):
        self.agent = agent
        self.verbose = verbose
        self.state = initial_state or {'A': 'Dirty', 'B': 'Dirty'}

    def getPercept(self, agent):
        return (agent.location, self.state[agent.location])

    def apply_action(self, action):
        if action == 'Suck':
            self.state[self.agent.location] = 'Clean'
            if self.verbose:
                print(f"Action: Suck -> {self.agent.location} cleaned")
        elif action == 'Right':
            self.agent.location = 'B'
            if self.verbose:
                print("Action: Right -> move to B")
        elif action == 'Left':
            self.agent.location = 'A'
            if self.verbose:
                print("Action: Left -> move to A")
        else:
            if self.verbose:
                print(f"Action: {action}")

    def is_done(self):
        return self.state['A'] == 'Clean' and self.state['B'] == 'Clean'

    def run(self, max_steps=10):
        steps = 0
        if self.verbose:
            print("Initial world:", self.state, "Agent at", self.agent.location)
        while steps < max_steps and not self.is_done():
            self.agent.run_once(self)
            steps += 1
        if self.verbose:
            print("Final world:", self.state, "Agent at", self.agent.location)
        return steps


if __name__ == "__main__":
    agent = SimpleReflexVacuumAgent()
    env = VacuumEnvironment(agent, {'A': 'Dirty', 'B': 'Dirty'}, verbose=True)
    env.run()