// Configuration
const API_URL = 'http://localhost:3000';

// État de l'application
const state = {
    mode: 'push-to-talk', // 'push-to-talk' ou 'hands-free'
    isRecording: false,
    mediaRecorder: null,
    audioChunks: [],
    stream: null,
    avatarState: 'idle', // idle, listening, thinking, speaking, error
    conversationHistory: [], // Historique des messages
    userProfile: { // Profil utilisateur (sera personnalisable plus tard)
        prenom: 'ami',
        centres_interet: ['technologie', 'musique'],
        souvenirs: []
    },
    // NOUVEAU: Paramètres de personnalité
    caractere: 'joueur', // timide, joueur, sage, farceur
    public: 'tout_le_monde', // enfants, ados, adultes, tout_le_monde
    vad: {
        isActive: false,
        audioContext: null,
        analyser: null,
        microphone: null,
        silenceTimeout: null,
        isSpeaking: false,
        silenceDelay: 1500, // Délai de silence avant d'arrêter (ms)
        volumeThreshold: 30 // Seuil de volume pour détecter la parole
    }
};

// Éléments DOM
const elements = {
    avatar: document.getElementById('si-3abess-avatar'),
    avatarImage: document.getElementById('avatar-image'),
    statusText: document.getElementById('status-text'),
    talkButton: document.getElementById('talk-button'),
    resetButton: document.getElementById('reset-button'),
    buttonText: document.querySelector('.button-text'),
    listeningIndicator: document.getElementById('listening-indicator'),
    transcript: document.getElementById('transcript'),
    response: document.getElementById('response'),
    connectionStatus: document.getElementById('connection-status'),
    connectionText: document.getElementById('connection-text'),
    modeRadios: document.querySelectorAll('input[name="mode"]'),
    vadSettings: document.getElementById('vad-settings'),
    volumeThreshold: document.getElementById('volume-threshold'),
    thresholdValue: document.getElementById('threshold-value'),
    silenceDelay: document.getElementById('silence-delay'),
    delayValue: document.getElementById('delay-value'),
    // NOUVEAU: Sélecteurs de personnalité
    caractereSelect: document.getElementById('caractere-select'),
    publicSelect: document.getElementById('public-select')
};

// Images pour chaque état (9 émotions)
const avatarImages = {
    idle: '/assets/Repos.jpg',
    listening: '/assets/Écoute.jpg',
    thinking: '/assets/Réflexion.jpg',
    speaking: '/assets/Parole.jpg',
    error: '/assets/Erreur.jpg',
    happy: '/assets/Joyeux.jpg',
    sad: '/assets/Triste.jpg',
    surprised: '/assets/Surpris.jpg',
    curious: '/assets/Curieux.jpg'
};

// === GESTION DES ÉTATS DE L'AVATAR ===
function setAvatarState(newState) {
    state.avatarState = newState;
    elements.avatar.setAttribute('data-state', newState);
    
    // Changer l'image en fonction de l'état
    if (avatarImages[newState]) {
        elements.avatarImage.src = avatarImages[newState];
    }
    
    const statusMessages = {
        idle: 'En attente...',
        listening: 'J\'écoute... 🎤',
        thinking: 'Je réfléchis... 🤔',
        speaking: 'Je parle... 💬',
        error: 'Erreur de connexion ❌'
    };
    
    elements.statusText.textContent = statusMessages[newState] || 'En attente...';
}

// === VÉRIFICATION DE LA CONNEXION ===
async function checkConnection() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            elements.connectionStatus.classList.remove('offline');
            elements.connectionStatus.classList.add('online');
            elements.connectionText.textContent = 'En ligne';
            
            if (state.avatarState === 'error') {
                setAvatarState('idle');
            }
            return true;
        }
    } catch (error) {
        console.error('Erreur de connexion:', error);
        elements.connectionStatus.classList.remove('online');
        elements.connectionStatus.classList.add('offline');
        elements.connectionText.textContent = 'Hors ligne';
        setAvatarState('error');
        return false;
    }
}

// === GESTION DU MICROPHONE ===
async function requestMicrophonePermission() {
    try {
        state.stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            } 
        });
        console.log('✅ Permission microphone accordée');
        return true;
    } catch (error) {
        console.error('❌ Permission microphone refusée:', error);
        alert('Permission microphone refusée. si-3abess a besoin du microphone pour fonctionner.');
        return false;
    }
}

// === DÉTECTION DE VOIX (VAD) ===
async function initVAD() {
    if (!state.stream) {
        const hasPermission = await requestMicrophonePermission();
        if (!hasPermission) return false;
    }

    try {
        // Créer le contexte audio
        state.vad.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        state.vad.analyser = state.vad.audioContext.createAnalyser();
        state.vad.analyser.fftSize = 2048;
        
        // Connecter le microphone à l'analyseur
        state.vad.microphone = state.vad.audioContext.createMediaStreamSource(state.stream);
        state.vad.microphone.connect(state.vad.analyser);
        
        console.log('✅ VAD initialisé');
        return true;
    } catch (error) {
        console.error('❌ Erreur initialisation VAD:', error);
        return false;
    }
}

function getVolume() {
    if (!state.vad.analyser) return 0;
    
    const bufferLength = state.vad.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    state.vad.analyser.getByteFrequencyData(dataArray);
    
    // Calculer le volume moyen
    let sum = 0;
    for (let i = 0; i < bufferLength; i++) {
        sum += dataArray[i];
    }
    return sum / bufferLength;
}

function startVADDetection() {
    if (!state.vad.analyser) return;
    
    state.vad.isActive = true;
    console.log('🎤 Détection de voix activée');
    
    function detectVoice() {
        if (!state.vad.isActive) return;
        
        const volume = getVolume();
        
        // Détecter si l'utilisateur parle
        if (volume > state.vad.volumeThreshold) {
            // Parole détectée
            if (!state.vad.isSpeaking && !state.isRecording) {
                console.log('🗣️ Parole détectée, début de l\'enregistrement');
                state.vad.isSpeaking = true;
                startRecording();
            }
            
            // Réinitialiser le timeout de silence
            if (state.vad.silenceTimeout) {
                clearTimeout(state.vad.silenceTimeout);
            }
            
            // Démarrer un nouveau timeout de silence
            state.vad.silenceTimeout = setTimeout(() => {
                if (state.isRecording) {
                    console.log('🤫 Silence détecté, fin de l\'enregistrement');
                    state.vad.isSpeaking = false;
                    stopRecording();
                }
            }, state.vad.silenceDelay);
        }
        
        // Continuer la détection
        requestAnimationFrame(detectVoice);
    }
    
    detectVoice();
}

function stopVADDetection() {
    state.vad.isActive = false;
    state.vad.isSpeaking = false;
    
    if (state.vad.silenceTimeout) {
        clearTimeout(state.vad.silenceTimeout);
        state.vad.silenceTimeout = null;
    }
    
    if (state.isRecording) {
        stopRecording();
    }
    
    console.log('🔇 Détection de voix désactivée');
}

// === ENREGISTREMENT AUDIO ===
async function startRecording() {
    if (!state.stream) {
        const hasPermission = await requestMicrophonePermission();
        if (!hasPermission) return;
    }
    
    state.audioChunks = [];
    state.mediaRecorder = new MediaRecorder(state.stream, {
        mimeType: 'audio/webm'
    });
    
    state.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            state.audioChunks.push(event.data);
        }
    };
    
    state.mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(state.audioChunks, { type: 'audio/webm' });
        await sendAudioToServer(audioBlob);
    };
    
    state.mediaRecorder.start();
    state.isRecording = true;
    
    // Mise à jour de l'interface
    setAvatarState('listening');
    elements.talkButton.classList.add('recording');
    elements.buttonText.textContent = 'Relâchez pour envoyer';
    elements.listeningIndicator.classList.remove('hidden');
}

function stopRecording() {
    if (state.mediaRecorder && state.isRecording) {
        state.mediaRecorder.stop();
        state.isRecording = false;
        
        // Mise à jour de l'interface
        elements.talkButton.classList.remove('recording');
        elements.buttonText.textContent = 'Parler à si-3abess';
        elements.listeningIndicator.classList.add('hidden');
        setAvatarState('thinking');
    }
}

// === ENVOI DE L'AUDIO AU SERVEUR ===
async function sendAudioToServer(audioBlob) {
    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.webm');
        
        const response = await fetch(`${API_URL}/transcribe`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Erreur serveur: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayTranscript(data.text);
            // TODO: Envoyer le texte pour obtenir une réponse de si-3abess
            await getResponse(data.text);
        } else {
            throw new Error('Transcription échouée');
        }
        
    } catch (error) {
        console.error('Erreur lors de l\'envoi de l\'audio:', error);
        setAvatarState('error');
        displayError('Erreur lors de la transcription. Vérifiez votre connexion.');
        setTimeout(() => setAvatarState('idle'), 2000);
    }
}

// === OBTENIR UNE RÉPONSE DE si-3abess ===
async function getResponse(text) {
    try {
        setAvatarState('thinking');
        
        // Utiliser l'endpoint standard avec audio intégré
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                text,
                history: state.conversationHistory,
                profile: state.userProfile,
                caractere: state.caractere,
                public: state.public
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Afficher la réponse
            displayResponse(data.response);
            
            // Changer l'émotion de l'avatar
            if (data.emotion) {
                const emotionMap = {
                    'repos': 'idle',
                    'ecoute': 'listening',
                    'reflexion': 'thinking',
                    'parole': 'speaking',
                    'erreur': 'error',
                    'joyeux': 'happy',
                    'triste': 'sad',
                    'surpris': 'surprised',
                    'curieux': 'curious'
                };
                setAvatarState(emotionMap[data.emotion] || 'speaking');
            } else {
                setAvatarState('speaking');
            }
            
            // 🎵 NOUVEAU : Jouer l'audio si disponible
            if (data.audio_chunks && data.audio_chunks.length > 0) {
                console.log(`🎵 Lecture de ${data.audio_chunks.length} phrase(s) audio`);
                await playAudioChunks(data.audio_chunks);
            } else {
                // Pas d'audio, retour à idle après 3 secondes
                console.warn('⚠️ Pas de chunks audio reçus');
                setTimeout(() => {
                    if (state.avatarState === 'speaking') {
                        setAvatarState('idle');
                    }
                }, 3000);
            }
            
            // Sauvegarder dans l'historique
            state.conversationHistory.push(
                { role: 'user', content: text },
                { role: 'assistant', content: data.response }
            );
            
            // Limiter l'historique à 40 messages (20 échanges)
            if (state.conversationHistory.length > 40) {
                state.conversationHistory = state.conversationHistory.slice(-40);
            }
            
            // Afficher l'humeur détectée (optionnel, pour debug)
            if (data.humeur_utilisateur) {
                console.log('😊 Humeur détectée:', data.humeur_utilisateur);
            }
        }
        
    } catch (error) {
        console.error('Erreur lors de la requête chat:', error);
        setAvatarState('error');
        displayResponse('Désolé, je n\'ai pas pu traiter ta demande. Vérifie ta connexion.');
        setTimeout(() => setAvatarState('idle'), 2000);
    }
}

// === LECTURE AUDIO ===
let audioQueue = [];
let isPlayingAudio = false;
let currentAudio = null;

async function playAudioChunks(chunks) {
    // Ajouter les chunks à la file d'attente
    audioQueue.push(...chunks);
    
    // Démarrer la lecture si pas déjà en cours
    if (!isPlayingAudio) {
        playNextChunk();
    }
}

async function playNextChunk() {
    if (audioQueue.length === 0) {
        // Plus de chunks à jouer
        isPlayingAudio = false;
        currentAudio = null;
        
        console.log('✅ Lecture audio terminée');
        
        // Retour à l'état idle après une courte pause
        setTimeout(() => {
            if (state.avatarState === 'speaking') {
                setAvatarState('idle');
                console.log('🔄 Retour à l\'état idle');
            }
        }, 500);
        
        return;
    }
    
    isPlayingAudio = true;
    const chunk = audioQueue.shift();
    
    try {
        // Décoder l'audio base64
        const audioData = atob(chunk.audio);
        const arrayBuffer = new Uint8Array(audioData.length);
        for (let i = 0; i < audioData.length; i++) {
            arrayBuffer[i] = audioData.charCodeAt(i);
        }
        
        // Créer un blob audio
        const blob = new Blob([arrayBuffer], { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(blob);
        
        // Créer et jouer l'audio
        currentAudio = new Audio(audioUrl);
        
        // Passer en état "speaking"
        setAvatarState('speaking');
        
        // Promesse pour attendre la fin de la lecture
        const playPromise = new Promise((resolve, reject) => {
            // Événement de fin de lecture
            currentAudio.addEventListener('ended', () => {
                console.log(`✅ Chunk ${chunk.index} terminé`);
                URL.revokeObjectURL(audioUrl);
                resolve();
            });
            
            // Événement d'erreur
            currentAudio.addEventListener('error', (e) => {
                console.error(`❌ Erreur lecture audio chunk ${chunk.index}:`, e);
                URL.revokeObjectURL(audioUrl);
                reject(e);
            });
        });
        
        // Démarrer la lecture
        try {
            await currentAudio.play();
            console.log(`🔊 Lecture chunk ${chunk.index}: "${chunk.text}"`);
            
            // Attendre la fin de la lecture
            await playPromise;
            
        } catch (playError) {
            console.error('❌ Erreur play():', playError);
            URL.revokeObjectURL(audioUrl);
        }
        
        // Jouer le chunk suivant
        currentAudio = null;
        playNextChunk();
        
    } catch (error) {
        console.error('❌ Erreur lors de la création de l\'audio:', error);
        // Continuer avec le chunk suivant même en cas d'erreur
        currentAudio = null;
        playNextChunk();
    }
}

// Fonction pour arrêter la lecture audio (utile pour interruption future)
function stopAudio() {
    console.log('🛑 Arrêt de l\'audio demandé');
    
    // Vider la file d'attente
    audioQueue = [];
    
    // Arrêter l'audio en cours
    if (currentAudio) {
        try {
            currentAudio.pause();
            currentAudio.currentTime = 0;
        } catch (e) {
            console.error('Erreur lors de l\'arrêt:', e);
        }
        currentAudio = null;
    }
    
    isPlayingAudio = false;
    
    // Retour à l'état idle
    if (state.avatarState === 'speaking') {
        setAvatarState('idle');
    }
    
    console.log('🔇 Lecture audio arrêtée');
}

// === AFFICHAGE ===
function displayTranscript(text) {
    elements.transcript.innerHTML = `<p>${text}</p>`;
}

function displayResponse(text) {
    elements.response.innerHTML = `<p>${text}</p>`;
}

function displayError(message) {
    elements.transcript.innerHTML = `<p style="color: #ef4444;">${message}</p>`;
}

// === GESTION DES ÉVÉNEMENTS ===

// Changement de mode
elements.modeRadios.forEach(radio => {
    radio.addEventListener('change', async (e) => {
        state.mode = e.target.value;
        console.log('Mode changé:', state.mode);
        
        if (state.mode === 'hands-free') {
            // Activer le mode mains libres
            const vadReady = await initVAD();
            if (vadReady) {
                elements.buttonText.textContent = 'Parlez naturellement';
                elements.talkButton.classList.add('hands-free-active');
                elements.listeningIndicator.classList.remove('hidden');
                elements.listeningIndicator.querySelector('span').textContent = 'Mode mains libres actif';
                elements.vadSettings.classList.remove('hidden');
                startVADDetection();
            } else {
                alert('Impossible d\'activer le mode mains libres. Vérifiez les permissions du microphone.');
                // Revenir au mode push-to-talk
                document.querySelector('input[value="push-to-talk"]').checked = true;
                state.mode = 'push-to-talk';
            }
        } else {
            // Retour au mode push-to-talk
            stopVADDetection();
            elements.buttonText.textContent = 'Parler à si-3abess';
            elements.talkButton.classList.remove('hands-free-active');
            elements.vadSettings.classList.add('hidden');
            if (!state.isRecording) {
                elements.listeningIndicator.classList.add('hidden');
            }
        }
    });
});

// Contrôle de la sensibilité VAD
if (elements.volumeThreshold) {
    elements.volumeThreshold.addEventListener('input', (e) => {
        state.vad.volumeThreshold = parseInt(e.target.value);
        elements.thresholdValue.textContent = e.target.value;
        console.log('Seuil de volume:', state.vad.volumeThreshold);
    });
}

if (elements.silenceDelay) {
    elements.silenceDelay.addEventListener('input', (e) => {
        state.vad.silenceDelay = parseInt(e.target.value);
        elements.delayValue.textContent = (e.target.value / 1000).toFixed(1);
        console.log('Délai de silence:', state.vad.silenceDelay, 'ms');
    });
}

// Changement de personnalité
if (elements.caractereSelect) {
    elements.caractereSelect.addEventListener('change', (e) => {
        state.caractere = e.target.value;
        console.log('🎭 Caractère changé:', state.caractere);
        
        // Message de confirmation adapté au caractère
        const confirmations = {
            'timide': 'Euh... d\'accord, je serai plus timide maintenant.',
            'joueur': 'Super ! Je suis en mode joueur maintenant !',
            'sage': 'Très bien. J\'adopte une approche plus sage.',
            'farceur': 'Allez, mode farceur activé ! Prépare-toi aux blagues !'
        };
        
        // Afficher temporairement dans la réponse
        displayResponse(confirmations[state.caractere] || 'Caractère mis à jour !');
        setTimeout(() => {
            if (elements.response.textContent === (confirmations[state.caractere] || 'Caractère mis à jour !')) {
                elements.response.innerHTML = '<p class="placeholder">La réponse de si-3abess apparaîtra ici...</p>';
            }
        }, 3000);
    });
}

if (elements.publicSelect) {
    elements.publicSelect.addEventListener('change', (e) => {
        state.public = e.target.value;
        console.log('👥 Public changé:', state.public);
    });
}

// Mode Push-to-talk
elements.talkButton.addEventListener('mousedown', async () => {
    if (state.mode === 'push-to-talk' && !state.isRecording) {
        await startRecording();
    }
});

elements.talkButton.addEventListener('mouseup', () => {
    if (state.mode === 'push-to-talk' && state.isRecording) {
        stopRecording();
    }
});

// Support tactile pour mobile
elements.talkButton.addEventListener('touchstart', async (e) => {
    e.preventDefault();
    if (state.mode === 'push-to-talk' && !state.isRecording) {
        await startRecording();
    }
});

elements.talkButton.addEventListener('touchend', (e) => {
    e.preventDefault();
    if (state.mode === 'push-to-talk' && state.isRecording) {
        stopRecording();
    }
});

// Mode mains libres - info
elements.talkButton.addEventListener('click', async () => {
    if (state.mode === 'hands-free') {
        // En mode mains libres, le bouton sert juste d'indicateur
        if (state.vad.isActive) {
            alert('Mode mains libres actif ! Parlez naturellement, si-3abess vous écoute automatiquement.');
        }
    }
});

// === INITIALISATION ===
async function init() {
    console.log('🚀 Initialisation de si-3abess...');
    
    // Vérifier la connexion au serveur
    await checkConnection();
    
    // Vérifier la connexion toutes les 10 secondes
    setInterval(checkConnection, 10000);
    
    console.log('✅ si-3abess est prêt !');
}

// Démarrer l'application
init();

// === RÉINITIALISATION DE LA CONVERSATION ===
if (elements.resetButton) {
    elements.resetButton.addEventListener('click', () => {
        // Arrêter l'audio en cours
        stopAudio();
        
        // Réinitialiser l'historique
        state.conversationHistory = [];
        
        // Réinitialiser l'affichage
        elements.transcript.innerHTML = '<p class="placeholder">La transcription apparaîtra ici...</p>';
        elements.response.innerHTML = '<p class="placeholder">La réponse de si-3abess apparaîtra ici...</p>';
        
        // Retour à l'état idle
        setAvatarState('idle');
        
        // Notification
        console.log('🔄 Conversation réinitialisée');
        
        // Message temporaire
        elements.response.innerHTML = '<p style="color: #667eea; font-style: italic;">✨ Nouvelle conversation démarrée</p>';
        setTimeout(() => {
            if (elements.response.textContent.includes('Nouvelle conversation')) {
                elements.response.innerHTML = '<p class="placeholder">La réponse de si-3abess apparaîtra ici...</p>';
            }
        }, 2000);
    });
}
