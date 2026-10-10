"""
🔬 Moniteur de performance pour si-3abess
Mesure la latence à chaque étape de la conversation
"""

import time
from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PerformanceMetrics:
    """Métriques de performance pour une requête"""
    request_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Temps de chaque étape (en secondes)
    silence_detection: Optional[float] = None  # Détection fin de phrase
    audio_upload: Optional[float] = None       # Envoi audio au serveur
    transcription: Optional[float] = None      # Whisper
    prompt_assembly: Optional[float] = None    # Assemblage du prompt
    llm_first_token: Optional[float] = None    # Premier mot du LLM
    llm_first_sentence: Optional[float] = None # Première phrase complète
    tts_first_chunk: Optional[float] = None    # Synthèse première phrase
    audio_send: Optional[float] = None         # Envoi + début lecture
    
    # Temps total
    total_time: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire pour JSON"""
        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "steps": {
                "silence_detection": self.silence_detection,
                "audio_upload": self.audio_upload,
                "transcription": self.transcription,
                "prompt_assembly": self.prompt_assembly,
                "llm_first_token": self.llm_first_token,
                "llm_first_sentence": self.llm_first_sentence,
                "tts_first_chunk": self.tts_first_chunk,
                "audio_send": self.audio_send,
            },
            "total_time": self.total_time
        }
    
    def summary(self) -> str:
        """Résumé lisible"""
        lines = [
            f"\n📊 Performance - {self.request_id}",
            f"   Transcription : {self.transcription:.3f}s" if self.transcription else "",
            f"   LLM 1er token : {self.llm_first_token:.3f}s" if self.llm_first_token else "",
            f"   LLM 1ère phrase : {self.llm_first_sentence:.3f}s" if self.llm_first_sentence else "",
            f"   TTS 1ère phrase : {self.tts_first_chunk:.3f}s" if self.tts_first_chunk else "",
            f"   ⏱️  TOTAL : {self.total_time:.3f}s" if self.total_time else "",
        ]
        return "\n".join(line for line in lines if line)


class PerformanceMonitor:
    """Moniteur de performance pour suivre les temps de réponse"""
    
    def __init__(self):
        self.current_metrics: Optional[PerformanceMetrics] = None
        self.start_time: Optional[float] = None
        self.step_starts: Dict[str, float] = {}
        self.enabled = True  # Désactiver en production si besoin
    
    def start_request(self, request_id: str):
        """Démarre le suivi d'une nouvelle requête"""
        if not self.enabled:
            return
        
        self.current_metrics = PerformanceMetrics(request_id=request_id)
        self.start_time = time.time()
        self.step_starts = {}
    
    def start_step(self, step_name: str):
        """Démarre le chronomètre pour une étape"""
        if not self.enabled or not self.current_metrics:
            return
        
        self.step_starts[step_name] = time.time()
    
    def end_step(self, step_name: str):
        """Termine le chronomètre pour une étape"""
        if not self.enabled or not self.current_metrics:
            return
        
        if step_name not in self.step_starts:
            return
        
        duration = time.time() - self.step_starts[step_name]
        
        # Enregistrer dans les métriques
        if step_name == "transcription":
            self.current_metrics.transcription = duration
        elif step_name == "llm_first_token":
            self.current_metrics.llm_first_token = duration
        elif step_name == "llm_first_sentence":
            self.current_metrics.llm_first_sentence = duration
        elif step_name == "tts_first_chunk":
            self.current_metrics.tts_first_chunk = duration
        elif step_name == "prompt_assembly":
            self.current_metrics.prompt_assembly = duration
    
    def end_request(self):
        """Termine le suivi de la requête"""
        if not self.enabled or not self.current_metrics or not self.start_time:
            return
        
        self.current_metrics.total_time = time.time() - self.start_time
        
        # Afficher le résumé
        print(self.current_metrics.summary())
        
        return self.current_metrics
    
    def get_metrics(self) -> Optional[PerformanceMetrics]:
        """Récupère les métriques actuelles"""
        return self.current_metrics


# Instance globale
performance_monitor = PerformanceMonitor()


def get_monitor() -> PerformanceMonitor:
    """Récupère le moniteur global"""
    return performance_monitor
