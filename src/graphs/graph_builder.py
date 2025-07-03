# src/graphs/graph_builder.py
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from src.llms.groqllm import GroqLLM
from src.nodes.visit_node import VisitNode
from src.states.visitstate import VisitState


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(VisitState)
        self.visit_node_obj = None

    def build_visit_graph(self):
        """
        Build a graph for visit
        """
        self.visit_node_obj = VisitNode(self.llm)
        
        # Nodes
        self.graph.add_node("Patient_Verifier", self.visit_node_obj.patient_verifier)
        self.graph.add_node("History_Retriever", self.visit_node_obj.patient_history_retriever)
        self.graph.add_node("General_Medicine", self.visit_node_obj.general_medicine)
        self.graph.add_node("Cardiologist", self.visit_node_obj.cardiologist)
        self.graph.add_node("Neurologist", self.visit_node_obj.neurologist)
        self.graph.add_node("Orthopedist", self.visit_node_obj.orthopedist)
        self.graph.add_node("Note_Creator", self.visit_node_obj.note_generation)
        self.graph.add_node("Diagnosis_Route", self.visit_node_obj.diagnosis_route)
        self.graph.add_node("Further_Diagnosis_Checker", self.visit_node_obj.further_diagnosis_checker)

        self.graph.add_node("Diagnosis_Aggregator", self.visit_node_obj.diagnosis_aggregator)
        self.graph.add_node("Note_Evaluator", self.visit_node_obj.medical_note_evaluator)
        self.graph.add_node("Note_Optimizer", self.visit_node_obj.medical_note_optimizer)
        self.graph.add_node("Evaluator_Route", self.visit_node_obj.route_medical_note_evaluation)
        self.graph.add_node("Detect_Correction", self.visit_node_obj.detect_changes_router)
        self.graph.add_node("Update_Memory_Note", self.visit_node_obj.update_changes_in_memory)
        self.graph.add_node("Correct_With_LLM", self.visit_node_obj.correct_with_llm)
        self.graph.add_node("Transform_Query", self.visit_node_obj.transform_query)
        self.graph.add_node("Grade_Documents", self.visit_node_obj.grade_documents)
        self.graph.add_node("Update_GraphDB", self.visit_node_obj.updateGraphDB)
        self.graph.add_node("Save_Notes_And_Diagnoses", self.visit_node_obj.save_notes_and_diagnoses)
        self.graph.add_node("Save_Images_Audio_Mood", self.visit_node_obj.save_images_audio_mood)
        self.graph.add_node("Check_Note_Structure", self.visit_node_obj.check_node_structure_router)

        # Edges
        self.graph.add_edge(START, "Patient_Verifier")
        self.graph.add_edge("Patient_Verifier", "History_Retriever")
        self.graph.add_edge("History_Retriever", "General_Medicine")
        self.graph.add_edge("History_Retriever", "Note_Creator")
        self.graph.add_edge("General_Medicine", "Diagnosis_Route")
        
        # Conditional edges
        self.graph.add_conditional_edges(
            "Diagnosis_Route",
            self.visit_node_obj.diagnosis_decision,
            {
                "cardiologist": "Cardiologist",
                "orthopedist": "Orthopedist",
                "neurologist": "Neurologist",
                "completed": "Diagnosis_Aggregator"
            }
        )

        self.graph.add_edge("Cardiologist", "Further_Diagnosis_Checker")
        self.graph.add_edge("Neurologist", "Further_Diagnosis_Checker")
        self.graph.add_edge("Orthopedist", "Further_Diagnosis_Checker")

        
        self.graph.add_edge("Note_Creator", "Diagnosis_Aggregator")
        self.graph.add_edge("Diagnosis_Aggregator", "Note_Evaluator")
        self.graph.add_edge("Note_Evaluator", "Evaluator_Route")

        self.graph.add_conditional_edges(
            "Further_Diagnosis_Checker",
            self.visit_node_obj.further_diagnosis_router,
            {
                "valid": "Diagnosis_Aggregator",
                "invalid": "Diagnosis_Route"
            }
        )

        self.graph.add_conditional_edges(
            "Evaluator_Route",
            self.visit_node_obj.route_medical_note_evaluation,  
            {
                "correct": "Detect_Correction",
                "incorrect": "Note_Optimizer"
            }
        )

        self.graph.add_edge("Note_Optimizer", "Check_Note_Structure")

        self.graph.add_conditional_edges(
            "Detect_Correction",
            self.visit_node_obj.detect_changes_decision,
            {
                "detected": "Update_Memory_Note",
                "undetected": "Correct_With_LLM"
            }
        )

        self.graph.add_edge("Update_Memory_Note", "Correct_With_LLM")
        self.graph.add_edge("Correct_With_LLM", "Check_Note_Structure")

        self.graph.add_conditional_edges(
            "Check_Note_Structure", 
            self.visit_node_obj.check_node_structure_decision,
            {
                "valid": "Update_GraphDB",
                "invalid": "Transform_Query"
            }
        )

        self.graph.add_edge("Transform_Query", "Grade_Documents")
        self.graph.add_edge("Grade_Documents", "Update_GraphDB")
        self.graph.add_edge("Update_GraphDB", "Save_Notes_And_Diagnoses")
        self.graph.add_edge("Save_Notes_And_Diagnoses", "Save_Images_Audio_Mood")
        self.graph.add_edge("Save_Images_Audio_Mood", END)

        # Return compiled graph
        return self.graph.compile()

# Module-level graph for langgraph_api
llm = GroqLLM().get_llm()
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_visit_graph()