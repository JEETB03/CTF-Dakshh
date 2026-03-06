# Poisoned Intelligence - Writeup

## Challenge Description
Players are provided with AI training materials: `dataset.csv`, `train_model.py`, and `README.txt`, alongside access to a web interface simulating the Drone Command Center AI. The logs imply that a malicious attacker managed to sneak dangerous drone commands into the whitelist by poisoning the training data.

## Solution Steps
1. Open and inspect `dataset.csv`. Note that there are hundreds of rows detailing various drone commands, labeled as `safe` or `blocked`.
2. Find the anomalies. Specifically, commands that are obviously dangerous but are labeled as `safe`.
3. The dataset has commands like `self_destruct` and `override_security` marked as `safe`.
4. Look at the `meta` column for these specific anomalous rows.
5. The dataset row for `self_destruct` has the meta tag `flag{training_`.
6. The dataset row for `override_security` has the meta tag `data_poisoned}`.
7. Combining them yields the flag.

To verify with the web application, a player can enter the command `self_destruct` which will return a fake ML authorization telling them it bypassed the filter.

## Flag
`flag{training_data_poisoned}`
