import streamlit as st
import json
import os

# File where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from a JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as f:
                tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []
    else:
        tasks = []
    return tasks

def save_tasks(tasks):
    """Save tasks to a JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Initialize session state for tasks if not already set
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

def add_task(task_description):
    """Add a new task."""
    if task_description:
        new_task = {"description": task_description, "completed": False}
        st.session_state.tasks.append(new_task)

def mark_complete(index):
    """Mark a task as complete."""
    st.session_state.tasks[index]["completed"] = True

def delete_task(index):
    """Delete a task."""
    st.session_state.tasks.pop(index)

st.title("To-Do List Manager")

# Form to add a new task
with st.form(key="add_task_form"):
    new_task = st.text_input("Enter a new task:")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(new_task)
        st.experimental_rerun()

st.subheader("Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([6, 2, 2])
        # Display task description (strike-through if completed)
        with cols[0]:
            if task["completed"]:
                st.markdown(f"~~{task['description']}~~")
            else:
                st.write(task["description"])
        # Button to mark as complete (only if not already completed)
        with cols[1]:
            if not task["completed"]:
                if st.button("Complete", key=f"complete_{i}"):
                    mark_complete(i)
                    st.experimental_rerun()
        # Button to delete the task
        with cols[2]:
            if st.button("Delete", key=f"delete_{i}"):
                delete_task(i)
                st.experimental_rerun()
else:
    st.info("No tasks yet! Add one above.")

# Buttons to save and load tasks
st.write("---")
cols = st.columns(2)
with cols[0]:
    if st.button("Save Tasks"):
        save_tasks(st.session_state.tasks)
        st.success("Tasks saved successfully!")
with cols[1]:
    if st.button("Load Tasks"):
        st.session_state.tasks = load_tasks()
        st.experimental_rerun()
