class StoryTeller {
    constructor() {
        this.apiBaseUrl = window.location.origin;
        this.audioPlayer = null;
        this.currentAudioUrl = null;
        this.lottieAnimation = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.audioPlayer = document.getElementById('audioPlayer');
        if (!this.audioPlayer) {
            console.error('Audio player element not found');
        }
    }

    setupEventListeners() {
        const form = document.getElementById('storyForm');
        const retryBtn = document.getElementById('retryBtn');
        const playBtn = document.getElementById('playBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const stopBtn = document.getElementById('stopBtn');
        const downloadBtn = document.getElementById('downloadBtn');

        if (form) form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        if (retryBtn) retryBtn.addEventListener('click', () => this.showForm());
        if (playBtn) playBtn.addEventListener('click', () => this.playAudio());
        if (pauseBtn) pauseBtn.addEventListener('click', () => this.pauseAudio());
        if (stopBtn) stopBtn.addEventListener('click', () => this.stopAudio());
        if (downloadBtn) downloadBtn.addEventListener('click', () => this.downloadAudio());

        if (this.audioPlayer) {
            this.audioPlayer.addEventListener('ended', () => this.handleAudioEnded());
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const character = document.getElementById('character').value.trim();
        const theme = document.getElementById('theme').value.trim();
        const duration = parseInt(document.getElementById('duration').value);
        const language = document.getElementById('language').value;

        if (!character && !theme) {
            this.showError('Please provide either a character or theme for your story.');
            return;
        }

        const requestData = {
            character: character || null,
            theme: theme || null,
            duration: duration,
            language: language
        };

        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/generate-story`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate story');
            }

            const data = await response.json();
            this.displayStory(data);
            
        } catch (error) {
            console.error('Error:', error);
            this.showError(error.message || 'Failed to generate story. Please try again.');
        }
    }

    showLoading() {
        this.hideAllSections();
        const loadingSection = document.getElementById('loadingSection');
        loadingSection.classList.remove('hidden');
        
        // Initialize Lottie animation
        this.initLottieAnimation();
    }

    initLottieAnimation() {
        const container = document.getElementById('lottieContainer');
        if (!container || !window.lottie) return;

        // Lottie animation data from the provided JSON
        const animationData = {
            "nm":"Flow 9","ddd":0,"h":20,"w":19,"meta":{"g":"LottieFiles Figma v86"},"layers":[{"ty":4,"nm":"Vector 3","sr":1,"st":0,"op":55.3,"ip":0,"hd":false,"ddd":0,"bm":0,"hasMask":false,"ao":0,"ks":{"a":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[2,2],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[2,2],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[4,4],"t":36},{"s":[2,2],"t":54}]},"s":{"a":0,"k":[100,-100]},"sk":{"a":0,"k":0},"p":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[4,16],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[4,16],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[4,14],"t":36},{"s":[4,16],"t":54}]},"r":{"a":0,"k":-180},"sa":{"a":0,"k":0},"o":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[30],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[30],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[100],"t":36},{"s":[30],"t":54}]}},"shapes":[{"ty":"sh","bm":0,"hd":false,"nm":"","d":1,"ks":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[2,4],[2.63,2.63],[4,2],[2.63,1.37],[2,0],[1.37,1.37],[0,2],[1.37,2.63],[2,4]]}],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[2,4],[2.63,2.63],[4,2],[2.63,1.37],[2,0],[1.37,1.37],[0,2],[1.37,2.63],[2,4]]}],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[4,8],[5.25,5.25],[8,4],[5.25,2.75],[4,0],[2.75,2.75],[0,4],[2.75,5.25],[4,8]]}],"t":36},{"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[2,4],[2.63,2.63],[4,2],[2.63,1.37],[2,0],[1.37,1.37],[0,2],[1.37,2.63],[2,4]]}],"t":54}]}},{"ty":"fl","bm":0,"hd":false,"nm":"","c":{"a":0,"k":[0.3804,0.3804,1]},"r":1,"o":{"a":0,"k":100}}],"ind":1},{"ty":4,"nm":"Vector 2","sr":1,"st":0,"op":55.3,"ip":0,"hd":false,"ddd":0,"bm":0,"hasMask":false,"ao":0,"ks":{"a":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[3,3],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[4,4],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[3,3],"t":36},{"s":[3,3],"t":54}]},"s":{"a":0,"k":[100,-100]},"sk":{"a":0,"k":0},"p":{"a":0,"k":[15,14]},"r":{"a":0,"k":-180},"sa":{"a":0,"k":0},"o":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[60],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[100],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[60],"t":36},{"s":[60],"t":54}]}},"shapes":[{"ty":"sh","bm":0,"hd":false,"nm":"","d":1,"ks":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[3,6],[3.94,3.94],[6,3],[3.94,2.06],[3,0],[2.06,2.06],[0,3],[2.06,3.94],[3,6]]}],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[4,8],[5.25,5.25],[8,4],[5.25,2.75],[4,0],[2.75,2.75],[0,4],[2.75,5.25],[4,8]]}],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[3,6],[3.94,3.94],[6,3],[3.94,2.06],[3,0],[2.06,2.06],[0,3],[2.06,3.94],[3,6]]}],"t":36},{"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[3,6],[3.94,3.94],[6,3],[3.94,2.06],[3,0],[2.06,2.06],[0,3],[2.06,3.94],[3,6]]}],"t":54}]}},{"ty":"fl","bm":0,"hd":false,"nm":"","c":{"a":0,"k":[0.3804,0.3804,1]},"r":1,"o":{"a":0,"k":100}}],"ind":2},{"ty":4,"nm":"Vector 1","sr":1,"st":0,"op":55.3,"ip":0,"hd":false,"ddd":0,"bm":0,"hasMask":false,"ao":0,"ks":{"a":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[6,6],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[3,3],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[2,2],"t":36},{"s":[6,6],"t":54}]},"s":{"a":0,"k":[100,100]},"sk":{"a":0,"k":0},"p":{"a":0,"k":[8,8]},"r":{"a":0,"k":0},"sa":{"a":0,"k":0},"o":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[100],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[60],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[30],"t":36},{"s":[100],"t":54}]}},"shapes":[{"ty":"sh","bm":0,"hd":false,"nm":"","d":1,"ks":{"a":1,"k":[{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[6,12],[7.88,7.88],[12,6],[7.88,4.12],[6,0],[4.12,4.12],[0,6],[4.12,7.88],[6,12]]}],"t":0},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[3,6],[3.94,3.94],[6,3],[3.94,2.06],[3,0],[2.06,2.06],[0,3],[2.06,3.94],[3,6]]}],"t":18},{"o":{"x":0,"y":0},"i":{"x":1,"y":1},"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[2,4],[2.63,2.63],[4,2],[2.63,1.37],[2,0],[1.37,1.37],[0,2],[1.37,2.63],[2,4]]}],"t":36},{"s":[{"c":true,"i":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"o":[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],"v":[[6,12],[7.88,7.88],[12,6],[7.88,4.12],[6,0],[4.12,4.12],[0,6],[4.12,7.88],[6,12]]}],"t":54}]}},{"ty":"fl","bm":0,"hd":false,"nm":"","c":{"a":0,"k":[0.3804,0.3804,1]},"r":1,"o":{"a":0,"k":100}}],"ind":3}],"v":"5.7.0","fr":60,"op":54.3,"ip":0,"assets":[]
        };

        try {
            this.lottieAnimation = lottie.loadAnimation({
                container: container,
                renderer: 'svg',
                loop: true,
                autoplay: true,
                animationData: animationData
            });
        } catch (error) {
            console.error('Failed to load Lottie animation:', error);
        }
    }

    showForm() {
        this.hideAllSections();
        document.querySelector('.story-form-container').classList.remove('hidden');
        
        // Stop Lottie animation if running
        if (this.lottieAnimation) {
            this.lottieAnimation.destroy();
            this.lottieAnimation = null;
        }
    }

    showError(message) {
        this.hideAllSections();
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        errorSection.classList.remove('hidden');
        
        // Stop Lottie animation if running
        if (this.lottieAnimation) {
            this.lottieAnimation.destroy();
            this.lottieAnimation = null;
        }
    }

    displayStory(data) {
        this.hideAllSections();
        
        // Stop Lottie animation if running
        if (this.lottieAnimation) {
            this.lottieAnimation.destroy();
            this.lottieAnimation = null;
        }
        
        const storySection = document.getElementById('storySection');
        const storyText = document.getElementById('storyText');
        const storyDuration = document.getElementById('storyDuration');
        const storyLanguage = document.getElementById('storyLanguage');

        if (!storySection || !storyText || !storyDuration || !storyLanguage) {
            this.showError('Story display elements not found');
            return;
        }

        storyText.textContent = data.story;
        storyDuration.textContent = `${data.duration} minutes`;
        storyLanguage.textContent = data.language === 'en' ? 'English' : 'Hindi';

        this.currentAudioUrl = `${this.apiBaseUrl}${data.audio_url}`;
        
        if (this.audioPlayer) {
            this.audioPlayer.src = this.currentAudioUrl;
            this.audioPlayer.classList.remove('hidden');
        }

        storySection.classList.remove('hidden');
        
        this.animateStoryAppearance();
    }

    animateStoryAppearance() {
        const storySection = document.getElementById('storySection');
        storySection.style.opacity = '0';
        storySection.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            storySection.style.transition = 'all 0.5s ease';
            storySection.style.opacity = '1';
            storySection.style.transform = 'translateY(0)';
        }, 100);
    }

    playAudio() {
        if (this.audioPlayer && this.audioPlayer.src) {
            this.audioPlayer.play();
            const playBtn = document.getElementById('playBtn');
            const pauseBtn = document.getElementById('pauseBtn');
            if (playBtn) playBtn.classList.add('hidden');
            if (pauseBtn) pauseBtn.classList.remove('hidden');
        }
    }

    pauseAudio() {
        if (this.audioPlayer) {
            this.audioPlayer.pause();
            const pauseBtn = document.getElementById('pauseBtn');
            const playBtn = document.getElementById('playBtn');
            if (pauseBtn) pauseBtn.classList.add('hidden');
            if (playBtn) playBtn.classList.remove('hidden');
        }
    }

    stopAudio() {
        if (this.audioPlayer) {
            this.audioPlayer.pause();
            this.audioPlayer.currentTime = 0;
            const pauseBtn = document.getElementById('pauseBtn');
            const playBtn = document.getElementById('playBtn');
            if (pauseBtn) pauseBtn.classList.add('hidden');
            if (playBtn) playBtn.classList.remove('hidden');
        }
    }

    handleAudioEnded() {
        const pauseBtn = document.getElementById('pauseBtn');
        const playBtn = document.getElementById('playBtn');
        if (pauseBtn) pauseBtn.classList.add('hidden');
        if (playBtn) playBtn.classList.remove('hidden');
    }

    async downloadAudio() {
        if (!this.currentAudioUrl) return;

        try {
            const response = await fetch(this.currentAudioUrl);
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `story_${Date.now()}.mp3`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
        } catch (error) {
            console.error('Download failed:', error);
            this.showError('Failed to download audio file.');
        }
    }

    hideAllSections() {
        const sections = [
            '.story-form-container',
            '#loadingSection',
            '#storySection',
            '#errorSection'
        ];
        
        sections.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                element.classList.add('hidden');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new StoryTeller();
});
