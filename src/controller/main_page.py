from service.task_service import TaskService
import streamlit as st
from graphviz import Digraph
import pandas as pd


def run():
    st.title("Deployment Application Interface")

    taskService = TaskService()

    # Création des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["Preparation", "Deployment", "Configuration", "Help"])

    # Onglet Preparation
    with tab1:
        st.header("Preparation")
        st.write("Define the preparation tasks here.")

        # Exemple de données initiales
        prep_tasks = [
            {"name": "Task1","stage":"Stage1", "description": "Setup database", "status": "done", "start_date": "2025-04-01", "duration": "2d", "team": "DBA","enabled": True},
            {"name": "Task2", "stage":"Stage1", "description": "Configure network", "status": "pending", "start_date": "2025-04-02", "duration": "1d", "team": "Ingé System","enabled": True},
            {"name": "Task3", "stage":"Stage2", "description": "Configure network", "status": "pending", "start_date": "2025-04-02", "duration": "1d", "team": "Ingé System","enabled": True},
            {"name": "Task4", "stage":"Stage2", "description": "Configure network", "status": "pending", "start_date": "2025-04-02", "duration": "1d", "team": "Ingé System","enabled": True},
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

    # Onglet Help
    with tab4:
        st.header("Help")
        st.write("This is a help section where you can find more information about the application.")

        # Ajouter un lien vers la documentation officielle
        link_to_docs = "[Documentation](https://example.com/docs)"
        st.markdown(f"[{link_to_docs}]({link_to_docs})")

        # Ajouter une section pour les questions fréquentes
        faq_section = """
    Q: What is this application?
    A: This application is a deployment tool that helps you manage your tasks.

    Q: How do I use this application?
    A: To use this application, simply follow the instructions on each tab.
        """

        st.write(faq_section)


def visualize_tasks(tasks, title):
    """
    Visualize tasks using Graphviz with colors based on status,
    allowing parallel execution of tasks within the same stage.
    """
    dot = Digraph(comment=title)
    dot.node("Start", "Start", shape="ellipse")

    # Define colors based on task status
    status_colors = {
        "done": "green",
        "in_progress": "yellow",
        "pending": "red"
    }

    stages = {}
    at_least_one_enabled = any(task.get("enabled") for task in tasks)

    # Group tasks by stage
    for i, task in enumerate(tasks):
        if task.get("enabled"):
            stage_name = task.get("stage", "Unknown Stage")
            task_name = task.get("name", f"Task{i}")
            task_status = task.get("status", "pending")
            task_color = status_colors.get(task_status, "gray")
            task_team = task.get("team", "Unknown Team")

            dot.node(f"Task{i}", f"{task_name}\n[{task_team}]", shape="box", style="filled", color=task_color)

            if stage_name not in stages:
                stages[stage_name] = []
            stages[stage_name].append(f"Task{i}")

    # Connect nodes in parallel for each stage
    prev_stage_tasks = ["Start"]
    for stage_name, stage_tasks in stages.items():
        for prev_task in prev_stage_tasks:
            for task in stage_tasks:
                dot.edge(prev_task, task)
        prev_stage_tasks = stage_tasks

    dot.node("End", "End", shape="ellipse")
    if at_least_one_enabled:
        for task in prev_stage_tasks:
            dot.edge(task, "End")
    else:
        dot.edge("Start", "End")

    st.graphviz_chart(dot)