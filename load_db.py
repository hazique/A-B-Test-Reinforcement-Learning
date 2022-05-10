import requests
import random

def main():
    
    host_address = "http://localhost:5000"

    ep_get_sub_id = host_address + "/get-sub-id"
    ep_register_user = host_address + "/register-user"
    ep_update_result = host_address + "/update-result"

    fnames = ['Mike', 'Charlie', 'Romeo', 'Philip', 'Morgan', 'Kate', 'Anna', 'David', 'Fred', 'Wilma']
    lnames = ['Powers', 'Tyson', 'Smith', 'Freeman', 'Lahm', 'Mara', 'Vaughn', 'Rogers', 'Davidoff', 'Presley']

    N = 100

    for i in range(N):

        # Call Endpoint to get subject ID
        response = requests.get(ep_get_sub_id)
        sub_id = response.text

        fname = fnames[random.randint(0,9)]
        lname = lnames[random.randint(0,9)]

        # Register User
        req_data = {
            "sub_id": sub_id,
            "fname": fname,
            "lname": lname
        }

        response = requests.post(ep_register_user, json=req_data)
        register_res = response.json()
        
        test_name = register_res['test_name']
        variant = register_res['variant']

        # Update result for subject
        result = 0 if i%2 == 0 else 1
        test_done = 1

        req_data = {
            "sub_id": sub_id,
            "variant": variant,
            'result': result
        }

        response = requests.post(ep_update_result, json=req_data)
        if i % 10 == 0:
            print("Iteration {}, Response {}".format(i, response.text))


if __name__=="__main__":
    main()