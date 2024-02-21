#!/bin/bash
rm -f database.db
# Path to your Python script
PYTHON_SCRIPT="./social.py"

# Create the database and schema
python3 $PYTHON_SCRIPT create

# Number of users to add
NUM_USERS=20
# Add users and accounts in a loop
for i in $(seq 1 $NUM_USERS); do
    # Generate a unique username and email for each user
    USERNAME="User${i}"
    EMAIL="user${i}@example.com"
    
    # Add user
    python3 $PYTHON_SCRIPT adduser "$USERNAME" "$EMAIL"
    
    # Add account for user
    python3 $PYTHON_SCRIPT addaccount "$EMAIL" "${USERNAME}123"

    # Create a post for each user
    TITLE="${USERNAME}'s Post"
    CONTENT="This is a post by ${USERNAME}."
    python3 $PYTHON_SCRIPT createpost "${USERNAME}123" "$TITLE" "$CONTENT"
done

echo "Database populated with $NUM_USERS users, accounts, and posts."
