"""
Comprehensive real-world user scenarios for hardware recommender.
Covers various applications, contexts, and user descriptions.
"""

COMPREHENSIVE_SCENARIOS = {
    # Webcam/Camera - Application Specific
    "Webcam Upgrade": [
        # Zoom scenarios
        "zoom application not show my video",
        "zoom not showing my video",
        "zoom camera not working",
        "zoom video not working",
        "can't see myself in zoom",
        "zoom can't see my face",
        "zoom black screen camera",
        "zoom camera not detected",
        "zoom meeting camera not working",
        "zoom video call no video",
        
        # Teams scenarios
        "teams camera not working",
        "teams video not showing",
        "teams can't see myself",
        "teams camera not detected",
        "microsoft teams camera issue",
        "teams meeting no video",
        
        # Skype scenarios
        "skype camera not working",
        "skype video not showing",
        "skype can't see myself",
        "skype camera not detected",
        
        # General video call scenarios
        "video call camera not working",
        "video call no video",
        "video call can't see myself",
        "video conference camera not working",
        "online meeting camera not working",
        "meeting camera not showing",
        "video chat camera not working",
        
        # Gaming/Streaming scenarios
        "obs camera not working",
        "stream camera not showing",
        "streaming camera not detected",
        "twitch camera not working",
        "youtube camera not working",
        
        # General camera issues
        "camera not working in applications",
        "camera not detected in apps",
        "all apps camera not working",
        "camera works in some apps not others",
    ],
    
    # RAM - Application/Multitasking Specific
    "RAM Upgrade": [
        # Browser scenarios
        "chrome tabs closing automatically",
        "browser tabs closing",
        "many tabs slow pc",
        "chrome using too much memory",
        "firefox tabs closing",
        "edge tabs closing",
        "browser out of memory",
        
        # Application scenarios
        "photoshop slow",
        "premiere pro slow",
        "video editing slow",
        "after effects slow",
        "blender slow",
        "autocad slow",
        "solidworks slow",
        "many programs open slow",
        "opening many apps slow",
        
        # Gaming scenarios
        "game crashes when alt tab",
        "game closes when switching apps",
        "gaming and streaming slow",
        "game and discord slow",
        
        # Work scenarios
        "excel slow with large files",
        "word slow with many documents",
        "outlook slow with many emails",
        "many excel files open slow",
    ],
    
    # SSD - File/Application Loading Specific
    "SSD Upgrade": [
        # Application loading
        "photoshop takes long to open",
        "premiere pro slow to start",
        "games take long to load",
        "applications slow to open",
        "programs slow to launch",
        "software slow to start",
        
        # File operations
        "copying files very slow",
        "moving files slow",
        "saving files slow",
        "opening large files slow",
        "file explorer slow",
        "searching files slow",
        
        # System operations
        "windows slow to boot",
        "pc takes long to start",
        "startup very slow",
        "shutdown very slow",
        "restart takes long",
    ],
    
    # GPU - Gaming/Graphics Specific
    "GPU Upgrade": [
        # Game performance
        "valorant low fps",
        "csgo low fps",
        "fortnite lag",
        "pubg stuttering",
        "gta 5 low fps",
        "cyberpunk low fps",
        "minecraft lag",
        "roblox lag",
        "apex legends low fps",
        "warzone low fps",
        
        # Graphics quality
        "games look blurry",
        "graphics quality poor",
        "can't run games on high settings",
        "games on low settings only",
        "textures not loading",
        "game graphics bad",
        
        # Streaming/Recording
        "obs lag when streaming",
        "recording gameplay lag",
        "stream quality poor",
        "recording fps drops",
    ],
    
    # WiFi - Application/Connection Specific
    "WiFi Adapter Upgrade": [
        # Video streaming
        "netflix buffering",
        "youtube buffering",
        "disney plus buffering",
        "prime video buffering",
        "streaming video lag",
        "video calls lag",
        "zoom connection poor",
        "teams connection poor",
        
        # Gaming online
        "online games lag",
        "multiplayer games lag",
        "game ping high",
        "game connection poor",
        "valorant high ping",
        "csgo high ping",
        
        # Download/Upload
        "download speed slow",
        "upload speed slow",
        "file download slow",
        "uploading files slow",
    ],
    
    # Audio - Application Specific
    "Audio Issue": [
        # Communication apps
        "zoom no sound",
        "teams no audio",
        "skype no sound",
        "discord no sound",
        "whatsapp call no sound",
        
        # Media apps
        "youtube no sound",
        "netflix no audio",
        "spotify no sound",
        "vlc no sound",
        "media player no sound",
        
        # Games
        "games no sound",
        "game audio not working",
        "game music not playing",
    ],
    
    # Microphone - Application Specific
    "Microphone Upgrade": [
        # Communication apps
        "zoom microphone not working",
        "teams mic not working",
        "skype mic not working",
        "discord mic not working",
        "whatsapp mic not working",
        "can't hear me in zoom",
        "can't hear me in teams",
        "people can't hear me",
        
        # Recording
        "recording no audio",
        "obs mic not working",
        "stream mic not working",
        "podcast mic not working",
    ],
}

def create_comprehensive_training_data():
    """Create training data from comprehensive scenarios."""
    from pathlib import Path
    import pandas as pd
    import sys
    import io
    
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    HERE = Path(__file__).parent.resolve()
    DATA_DIR = (HERE.parent / "data").resolve()
    
    rows = []
    
    for component, scenarios in COMPREHENSIVE_SCENARIOS.items():
        for scenario in scenarios:
            rows.append({
                'user_text': scenario,
                'component_label': component,
                'component_definition': f"{component} is a hardware component or upgrade relevant to computer performance or repair.",
                'why_useful': f"{component} helps resolve the problem by improving stability, performance, or fixing failing hardware.",
                'extra_explanation': f"{component} may be required based on the symptoms described."
            })
    
    df = pd.DataFrame(rows)
    
    print(f"Created {len(df)} comprehensive scenario examples")
    print(f"\nComponent distribution:")
    print(df['component_label'].value_counts())
    
    # Load existing improved data
    existing_file = DATA_DIR / "hardware_component_dataset_improved.csv"
    if existing_file.exists():
        df_existing = pd.read_csv(existing_file)
        print(f"\n[INFO] Loaded {len(df_existing)} existing examples")
        
        # Normalize for comparison
        df_existing['text_normalized'] = df_existing['user_text'].astype(str).str.lower().str.strip()
        df['text_normalized'] = df['user_text'].astype(str).str.lower().str.strip()
        
        # Find new examples
        existing_texts = set(df_existing['text_normalized'].unique())
        df_new_unique = df[~df['text_normalized'].isin(existing_texts)]
        
        print(f"[INFO] {len(df_new_unique)} new unique examples (out of {len(df)})")
        
        # Drop normalized column
        df_existing = df_existing.drop(columns=['text_normalized'])
        df_new_unique = df_new_unique.drop(columns=['text_normalized'])
        
        # Combine
        df_combined = pd.concat([df_existing, df_new_unique], ignore_index=True)
        
        print(f"\n[INFO] Combined dataset: {len(df_combined)} examples")
        
        # Save
        output_file = DATA_DIR / "hardware_component_dataset_improved.csv"
        df_combined.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n{'='*80}")
        print(f"Comprehensive training data saved to: {output_file}")
        print(f"{'='*80}")
        
        return df_combined
    else:
        output_file = DATA_DIR / "hardware_component_dataset_improved.csv"
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\n{'='*80}")
        print(f"Training data saved to: {output_file}")
        print(f"{'='*80}")
        return df

if __name__ == "__main__":
    create_comprehensive_training_data()

