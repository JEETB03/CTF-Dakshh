Drone AI Training Instructions

1. Download the latest dataset.csv from the Drone Command Web Interface.
2. Run train_model.py to update the autonomous AI logic.
3. Once updated, drones will automatically follow the new model for their safe/blocked decisions.

Warning: Ensure training data maintains its integrity! We've had reports of malicious actors attempting to modify datasets to whitelist dangerous commands. As a security investigator, verify that no dangerous commands (like self_destruct or override_security) have been labeled "safe".
