from surreal.env import *
from surreal.session import *
import surreal.utils as U
from surreal.agent import agentFactory

def eval_parser_setup(parser):
    parser.add_argument('--mode', type=str, required=True)
    parser.add_argument('--id', type=int, default=0)
    parser.add_argument('--render', action='store_true', default=False)

def run_eval_main(args, config):
    session_config, learner_config, env_config = config.session_config, config.learner_config, config.env_config

    env, env_config = make_env(env_config)

    agent_mode = AgentMode[args.mode]
    assert agent_mode != AgentMode.training

    if agent_mode == AgentMode.eval_deterministic:
        eval_id = 'deterministic-{}'.format(args.id)
    else:
        eval_id = 'stochastic-{}'.format(args.id)

    agent_class = agentFactory(learner_config.algo.agent_class)
    agent = agent_class(
        learner_config=learner_config,
        env_config=env_config,
        session_config=session_config,
        agent_id=eval_id,
        agent_mode=agent_mode,
    )

    env = EvalTensorplexMonitor(
        env,
        eval_id=eval_id,
        fetch_parameter=agent.fetch_parameter,
        session_config=session_config,
    )


    obs, info = env.reset()
    while True:
        action = agent.act(U.to_float_tensor(obs))
        if args.render:
            env.render()
        obs, reward, done, info = env.step(action)
        if done:
            obs, info = env.reset()