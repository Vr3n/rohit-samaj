#!/bin/bash

# Creat a new window and start debuggers
tmux new-window -n debuggers

# Start django debugger.
tmux send-keys "uv run manage.py runserver" C-m


# split the window.
tmux split-window -h

# start tailwind debugger.
tmux send-keys "pnpm run tw" C-m

# switch back to the first window (optional)
tmux select-window -t 1
