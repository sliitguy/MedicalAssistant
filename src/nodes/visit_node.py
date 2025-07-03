from src.states.visitstate import VisitState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.visitstate import Visit 


class VisitNode:
    def __init__(self, llm):
        self.llm = llm
    
    def patient_verifier(self, state: VisitState) -> VisitState:
        return state
    
    def diagnosis_decision(self, state: VisitState) -> str:
        return "completed"
    
    def further_diagnosis_router(self, state:VisitState) -> str:
        return "valid"
    
    def further_diagnosis_checker(self, state:VisitState) -> VisitState: return state
    def patient_history_retriever(self, state: VisitState) -> VisitState: return state
    def general_medicine(self, state: VisitState) -> VisitState: return state
    def cardiologist(self, state: VisitState) -> VisitState: return state
    def neurologist(self, state: VisitState) -> VisitState: return state
    def orthopedist(self, state: VisitState) -> VisitState: return state
    def note_generation(self, state: VisitState) -> VisitState: return state
    def diagnosis_route(self, state: VisitState) -> VisitState: return state
    def diagnosis_aggregator(self, state: VisitState) -> VisitState: return state
    def medical_note_evaluator(self, state: VisitState) -> VisitState: return state
    def medical_note_optimizer(self, state: VisitState) -> VisitState: return state
    def route_medical_note_evaluation(self, state: VisitState) -> str: return "correct"
    def detect_changes_router(self, state: VisitState) -> VisitState: return state
    def update_changes_in_memory(self, state: VisitState) -> VisitState: return state
    def correct_with_llm(self, state: VisitState) -> VisitState: return state
    def transform_query(self, state: VisitState) -> VisitState: return state
    def grade_documents(self, state: VisitState) -> VisitState: return state
    def updateGraphDB(self, state: VisitState) -> VisitState: return state
    def save_notes_and_diagnoses(self, state: VisitState) -> VisitState: return state
    def save_images_audio_mood(self, state: VisitState) -> VisitState: return state
    def check_node_structure_router(self, state: VisitState) -> VisitState: return state
    def detect_changes_decision(self, state: VisitState) -> str: return "detected"
    def check_node_structure_decision(self, state: VisitState) -> str: return "valid"

    







