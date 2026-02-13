"""
Loading state management and utilities for better UX during AI processing.
"""
import random

def get_loading_messages(context="general"):
    """
    Get context-aware loading messages for different operations.
    
    Args:
        context: Type of operation (insights, tips, tasks, general)
    
    Returns:
        List of messages to cycle through
    """
    messages = {
        "insights": [
            "🔍 Analyzing personality patterns...",
            "🧠 Understanding unique traits...",
            "✨ Discovering what makes your child special...",
            "🎯 Matching behavioral insights...",
            "💡 Almost there...",
        ],
        "tips": [
            "👨‍👩‍👧 Crafting personalized parenting tips...",
            "📚 Gathering expert advice...",
            "💝 Tailoring strategies for your child...",
            "🎨 Creating your custom guide...",
            "✅ Finalizing recommendations...",
        ],
        "tasks": [
            "🧩 Designing daily activities...",
            "🎯 Creating age-appropriate tasks...",
            "🌟 Building character development plan...",
            "📝 Personalizing your child's routine...",
            "🎉 Almost ready...",
        ],
        "general": [
            "⏳ Processing your request...",
            "🔄 Working on it...",
            "✨ Just a moment...",
            "🚀 Almost done...",
        ]
    }
    
    return messages.get(context, messages["general"])


def get_progress_stages(context="general"):
    """
    Get progress stages for different operations.
    
    Returns:
        List of tuples (progress_percentage, stage_name)
    """
    stages = {
        "insights": [
            (20, "Calculating astrological data"),
            (40, "Extracting personality traits"),
            (60, "Matching with database"),
            (80, "Preparing insights"),
            (100, "Complete!"),
        ],
        "tips": [
            (25, "Analyzing child's traits"),
            (50, "Consulting parenting strategies"),
            (75, "Personalizing recommendations"),
            (100, "Ready!"),
        ],
        "tasks": [
            (30, "Understanding personality"),
            (60, "Designing activities"),
            (90, "Age-appropriate adjustments"),
            (100, "Done!"),
        ],
        "general": [
            (33, "Processing"),
            (66, "Finalizing"),
            (100, "Complete!"),
        ]
    }
    
    return stages.get(context, stages["general"])


def get_fun_fact():
    """Get a random fun fact about child development."""
    facts = [
        "💡 Children learn best through play and exploration!",
        "🌈 Every child develops at their own unique pace.",
        "🧠 A child's brain forms 1 million neural connections per second!",
        "❤️ Positive reinforcement is more effective than criticism.",
        "🎨 Creative play boosts problem-solving skills.",
        "📚 Reading together builds emotional bonds and language skills.",
        "🤗 Hugs release oxytocin, the 'bonding hormone'.",
        "🎵 Music enhances cognitive development in children.",
        "🌟 Praising effort (not just results) builds resilience.",
        "👂 Active listening makes children feel valued and understood.",
    ]
    
    return random.choice(facts)


def get_estimated_time(context="general"):
    """
    Get estimated time message for different operations.
    
    Args:
        context: Type of operation
    
    Returns:
        Estimated time string
    """
    times = {
        "insights": "15-30 seconds",
        "tips": "20-40 seconds",
        "tasks": "15-25 seconds",
        "general": "a few moments",
    }
    
    return times.get(context, times["general"])
