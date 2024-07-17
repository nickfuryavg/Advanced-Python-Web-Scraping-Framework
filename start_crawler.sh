#!/bin/bash
LOG_FILE="/Users/sandipanray/Soket_Labs/start_crawler.log"
# Define the path to the Python script
SCRIPT_PATH="/Users/sandipanray/Soket_Labs/Modular_Advance_scrapping.py"

# Start the Python script in the background and save the PID to a fil
python3 "$SCRIPT_PATH" > /Users/sandipanray/Soket_Labs/log1.log 2>&1 &
# Get the PID of the last executed command (the Python script)
PID=$!

# Write the PID to the log file for reference
echo "Crawler started with PID $PID" >> "$LOG_FILE"
