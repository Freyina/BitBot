sound_files = {
    "Wow": r"Sounds\owen-wilson-wow-made-with-Voicemod.mp3",
    "2 Hours": r"Sounds\two-hours-later-made-with-Voicemod.mp3",
    "Lego Yoda": r"Sounds\lego-yoda-death-made-with-Voicemod.mp3",
    "Doom": r"Sounds\doom-music-made-with-Voicemod.mp3",
    "Leviosaa": r"Sounds\ron-2-leviosa-made-with-Voicemod.mp3",
    "Sure": r"Sounds\are-you-sure-about-that_-made-with-Voicemod.mp3",
    "Scooby": r"Sounds\scooby-doo-laugh-sound-effect-made-with-Voicemod.mp3",
    "Lizard": r"Sounds\lizard-made-with-Voicemod.mp3",
    "Phasmo 1": r"Sounds\ghost-footsteps-phasmophobia-made-with-Voicemod.mp3",
    "Phasmo 2": r"Sounds\phasmophobia-attack-made-with-Voicemod.mp3",
    "Phasmo 3": r"Sounds\phasmophobia-made-with-Voicemod.mp3",
    "Phasmo 4": r"Sounds\phasmophobia-singing-ghost-made-with-Voicemod.mp3",
    "Clanka Card": r"Sounds\clanker-is-our-word-made-with-Voicemod.mp3",
    "Wrist Rockets": r"Sounds\watch-those-wrist-rockets-made-with-Voicemod.mp3",
    "Simulations": r"Sounds\just-like-the-simulation-(swbf2)-made-with-Voicemod.mp3",
    "Command Post": r"Sounds\“the-command-post-is-now-under-hostile-control”-made-with-Voicemod.mp3"
}



def get_sound_path(key):
    """Return full path for a sound name or None if missing."""
    return sound_files.get(key, None)

def list_sounds():
    """Return a list of available sound names (keys)."""
    return list(sound_files.keys())
