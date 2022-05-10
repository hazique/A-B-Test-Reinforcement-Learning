from cgi import test
from flask import Flask, request
from flask_cors import CORS
import time
import random

from collections import Counter

from init_db import init
from util.db_manager import *
from mab import *

app = Flask(__name__, static_url_path='', static_folder='ab-test-mab-ui/build')
CORS(app)

# init database connectivity
restore = init()

global reward_log, banditas, N_completed, N_threshold, N_participants
N_threshold = 100
reward_log, banditas, N = None, None, None

# Reconstruct results if the server was restarted
def reconstruct_results():
    global N_participants, N_completed

    all_rows = get_stored_rewards_log()
    N_participants = len(all_rows)

    # rows for which test has been completed
    test_completed = list(filter((lambda x: x[2] == '1'), all_rows))
    N_completed = len(test_completed)

    # get number of tests recorded for each variant
    all_variants = []
    for row in test_completed:
        all_variants.append(int(row[0]))
    
    variants = set(all_variants)
    variants_n = []
    for variant in variants:
        c = Counter(all_variants)
        variants_n.append(c[variant])

    # get successful results per variant to find the probability of success
    variants_n_good = []
    for variant in variants:
        variant_rows = list(filter((lambda x: x[0] == str(variant)), test_completed))
        # count successful variant rows
        variant_successful = list(filter((lambda x: x[1] == 1), variant_rows))
        variants_n_good.append(len(variant_successful))

    # Recontruct success probabilites for each variant
    probabilities = []
    for variant in variants:
        p = variants_n_good[variant] / variants_n[variant]
        probabilities.append(p)

    # Reconstruct bandits using the above probabilities
    bandits = [Bandit(probabilities[x], x) for x in variants]

    # Reconstruct reward log for the bandits
    reward_log = BanditRewardsLog()
    for row in test_completed:
        variant, result, test_done = row
        reward_log.record_action(bandits[int(variant)], result)

    return reward_log, bandits, N_participants


if restore:
    reward_log, banditas, N = reconstruct_results()
else:
    banditas = [Bandit(0.5, x) for x in range(2)]

global agent 
agent = EpsilonGreedyAgent(rewards_log=reward_log, banditas=banditas)
# agent.bandits(banditas)

@app.route("/")
def get_time():
    return {'time': time.time()}

@app.route("/get-sub-id")
def get_sub_id():
    # create a new user sid
    sub_id = random.randrange(1, 10**10)
    while db_has_sub_id(sub_id):
        sub_id = random.randrange(1, 10**10)

    return str(sub_id)


@app.route("/register-user", methods=['POST'])
def register_user():
    global agent

    json = request.get_json()

    sub_id = int(json['sub_id'])
    fname = json['fname']
    lname = json['lname']

    bandits = agent.bandits
    n_bandit_0 = get_record_count_for_variant(bandits[0].id)
    n_bandit_1 = get_record_count_for_variant(bandits[1].id)

    if n_bandit_0 + n_bandit_1 <= N_threshold:

        if n_bandit_0 > n_bandit_1:
            variant = 1
        elif n_bandit_0 < n_bandit_1:
            variant = 0
        else:
            variant = agent.get_random_bandit().id
    
    else:
        variant = agent.choose_bandit()

    test_done = 0
    test_name = "shopping_cart"
    data = (sub_id, fname, lname, test_name, variant, test_done)
    
    add_subject_to_table(data)
  
    return {
        "sub_id": str(sub_id),
        "test_name": test_name,
        "variant": variant
    }


@app.route("/update-result", methods=['POST'])
def update_result():
    json = request.get_json()

    sub_id = int(json['sub_id'])
    variant = json['variant']
    result = int(json['result'])
    test_done = 1

    data = (result, test_done, sub_id)
    
    try:
        update_sub_test_result(data)
        agent.take_action(variant, result) 
        return "True"
    except Exception as e:
        print(e)
        return "False"


@app.route("/get-test-results", methods=['GET'])
def get_test_results():
    return agent.rewards_log.record
