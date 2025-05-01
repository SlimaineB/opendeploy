from service.task_service import TaskService
import streamlit as st
from graphviz import Digraph
import pandas as pd


def run():
    st.title("Deployment Application Interface")

    taskService = TaskService()

    # Création des onglets
    tab1, tab2, tab3 = st.tabs(["Preparation", "Deployment", "Configuration"])

    # Onglet Preparation
    with tab1:
        st.header("Preparation")
        st.write("Define the preparation tasks here.")

        # Exemple de données initiales
        prep_tasks = [
            {"name": "Task1", "description": "Setup database", "status": "done", "start_date": "2025-04-01", "duration": "2d", "team": "DBA","enabled": True},
            {"name": "Task2", "description": "Configure network", "status": "pending", "start_date": "2025-04-02", "duration": "1d", "team": "Ingé System","enabled": True},
        ]
        prep_df = pd.DataFrame(prep_tasks)

        # Conversion de la colonne start_date en type datetime
        prep_df["start_date"] = pd.to_datetime(prep_df["start_date"])

        # Configuration des colonnes pour le tableau éditable
        edited_df = st.data_editor(
            prep_df,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    options=["done", "in_progress", "pending"],
                    label="Status",
                ),
                "start_date": st.column_config.DateColumn(label="Start Date"),
                "team": st.column_config.SelectboxColumn(
                    options=["DBA", "Ingé System", "Support"],
                    label="Team",
                ),                
                "enable": st.column_config.CheckboxColumn(
                    label="Enabled",
                ),
            },
            use_container_width=True,
            num_rows="dynamic",
        )

        # Sauvegarder les modifications
        if st.button("Save Changes"):
            st.success("Changes saved successfully!")
            st.write(edited_df)

        # Visualiser les tâches
        if st.button("Visualize Preparation Tasks"):
            visualize_tasks(edited_df.to_dict(orient="records"), "Preparation Tasks")

    # Onglet Deployment
    with tab2:
        st.header("Deployment")
        st.write("Define the deployment tasks here.")
        # Similaire à l'onglet Preparation

    # Onglet Configuration
    with tab3:
        st.header("Configuration")
        st.write("Define the configuration tasks here.")
        # Similaire à l'onglet Preparation


def visualize_tasks(tasks, title):
    """
    Visualize tasks using Graphviz with colors based on status.
    """
    dot = Digraph(comment=title)
    dot.node("Start", "Start", shape="ellipse")

    # Define colors based on task status
    status_colors = {
        "done": "green",
        "in_progress": "yellow",
        "pending": "red"
    }

    at_least_one_enabled = any(task.get("enabled") for task in tasks)
    for i, task in enumerate(tasks):
        task_enabled = task.get("enabled")
        if  task_enabled:
            
            task_name = task.get("name", f"Task{i}")
            task_status = task.get("status", "pending")
            task_color = status_colors.get(task_status, "gray")
            task_team = task.get("team", "Unknown Team")

            # Add task node with color and label
            dot.node(f"Task{i}", f"{task_name}\n[{task_team}]", shape="box", style="filled", color=task_color)

            # Connect tasks sequentially or in parallel
            if i == 0:
                dot.edge("Start", f"Task{i}")
            else:
                dot.edge(f"Task{i-1}", f"Task{i}")

    dot.node("End", "End", shape="ellipse")
    if at_least_one_enabled:
        dot.edge(f"Task{len(tasks)-1}", "End")
    else:
        dot.edge("Start", "End")
    st.graphviz_chart(dot)