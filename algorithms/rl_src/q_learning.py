import os
import random
from collections import defaultdict
import numpy as np
# import uuid


def eval(env, Q):
    total_reward = 0

    done = False
    (flag, state), _ = env.reset()
    while not done:
        a = np.argmax(Q[flag, state,:])
        (flag, state), r, term, trunc, _ = env.step(a)

        done = term or trunc
        total_reward += r

    return total_reward


def q_learning(env, lr=0.01, discount=0.9, num_steps=100_000, savedir=None, seed=None, return_history=False, eps_coef=0.7):
    trajectories = defaultdict(list)
    Q = np.zeros(shape=(2, env.unwrapped.size * env.unwrapped.size, env.action_space.n))

    rewards_history = []
    episode_reward = 0

    eps = 1.
    eps_diff = eps_coef / num_steps

    (flag, state), _ = env.reset(seed=seed)
    term, trunc = False, False
    # for i in trange(1, num_steps + 1):
    for i in range(1, num_steps + 1):
        if term or trunc:
            (flag, state), _ = env.reset()
            rewards_history.append(episode_reward)
            episode_reward = 0

        if random.random() < eps:
            a = env.action_space.sample()
        else:
            a = np.argmax(Q[flag, state, :])

        (next_flag, next_state), r, term, trunc, _ = env.step(a)
        episode_reward += r
        if term:
            Q[next_flag, next_state, :] = 0

        # Collect trajectories with exploratory actions
        if savedir is not None:
            trajectories['states'].append(state)
            trajectories['actions'].append(a)
            trajectories['rewards'].append(r)
            trajectories['terminateds'].append(term)
            trajectories['truncateds'].append(trunc)

        #Update Q-Table with new knowledge
        Q[flag, state, a] += lr * (r + discount * np.max(Q[next_flag, next_state, :]) - Q[flag, state, a])

        state = next_state
        flag = next_flag
        eps = max(0, eps - eps_diff)

    if return_history:
        return Q, rewards_history
    return Q