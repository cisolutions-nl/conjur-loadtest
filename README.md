# Load Testing Conjur

The load test of the Conjur server is done using the Python script `loadtest.py`.
The script uses the `requests` library to make HTTP requests to the Conjur server.
The script is designed to simulate a large number of clients making requests to the
Conjur server at the same time. The script can be used to test the performance of
the Conjur server under load.

## Installation
The script requires Python 3.9 or later. Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage
Usage of the Python `loadtest.py` (or run `python loadtest.py –help`):

Example: 
```bash
python loadtest.py --concurrency=250 --base-url=https://conjur.url --user-name=test --secret-id=test-path --account=organizationxyz [–-api-key=abc123]
```

Or with short options:
```bash
python loadtest.py -c 250 -b https://conjur.url -u test -s test-path -a organizationxyz [-k abc123]
```

Example output:
```base
Finished 250 requests. Average response time: 0.9126874418258667
Finished 250 requests. Average response time: 0.974892149925232
Finished 250 requests. Average response time: 0.9756416006088257
Finished 250 requests. Average response time: 0.9037885036468506
Finished 250 requests. Average response time: 0.8921614294052124
Finished 250 requests. Average response time: 0.9250940265655517
Finished 250 requests. Average response time: 0.978875904083252
Finished 250 requests. Average response time: 0.9840988664627075
Finished 250 requests. Average response time: 0.9546800537109374
Finished 250 requests. Average response time: 0.9395519971847535
```

### Important notes:
- #1: We highly recommend creating a test branch with a test user, host, and secrets to test the load on your Conjur environment.
- #2: Ensure you rotate the API key after testing.
- #3: This load test generates a significant amount of logging. Make sure your Conjur logging settings are properly configured.
