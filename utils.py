import os
from typing import List

def format_file_size(size_bytes: int) -> str:
    """
    Convert file size in bytes to human readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size = size_bytes
    unit_index = 0
    
    while size >= 1024 and unit_index < len(size_names) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {size_names[unit_index]}"
    else:
        return f"{size:.1f} {size_names[unit_index]}"

def validate_file_type(filename: str) -> bool:
    """
    Validate if the uploaded file type is supported.
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        True if file type is supported, False otherwise
    """
    supported_extensions = ['.pdf', '.txt', '.docx']
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in supported_extensions

def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension (including dot)
    """
    return os.path.splitext(filename)[1].lower()

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of text
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    if not text:
        return 0
    return len(text.split())

def estimate_reading_time(text: str, words_per_minute: int = 200) -> str:
    """
    Estimate reading time for text.
    
    Args:
        text: Text to estimate reading time for
        words_per_minute: Average reading speed
        
    Returns:
        Formatted reading time string
    """
    word_count = count_words(text)
    minutes = word_count / words_per_minute
    
    if minutes < 1:
        return "< 1 minute"
    elif minutes < 60:
        return f"{int(minutes)} minute{'s' if int(minutes) != 1 else ''}"
    else:
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        return f"{hours}h {remaining_minutes}m"

def clean_text_for_display(text: str, max_lines: int = 10) -> str:
    """
    Clean text for display purposes by limiting lines and removing excessive whitespace.
    
    Args:
        text: Text to clean
        max_lines: Maximum number of lines to display
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Split into lines and remove empty ones
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Limit number of lines
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines.append("... (text truncated)")
    
    return '\n'.join(lines)

def validate_api_keys() -> dict:
    """
    Check which API keys are available in environment variables.
    
    Returns:
        Dictionary with API key availability status
    """
    return {
        'openai': bool(os.getenv('OPENAI_API_KEY')),
        'anthropic': bool(os.getenv('ANTHROPIC_API_KEY'))
    }

def get_supported_file_types() -> List[str]:
    """
    Get list of supported file types.
    
    Returns:
        List of supported file extensions
    """
    return ['pdf', 'txt', 'docx']

def format_summary_stats(original_words: int, summary_words: int) -> dict:
    """
    Calculate and format summary statistics.
    
    Args:
        original_words: Number of words in original document
        summary_words: Number of words in summary
        
    Returns:
        Dictionary with formatted statistics
    """
    if original_words == 0:
        compression_ratio = 0
    else:
        compression_ratio = (1 - summary_words / original_words) * 100
    
    return {
        'original_words': f"{original_words:,}",
        'summary_words': f"{summary_words:,}",
        'compression_ratio': f"{compression_ratio:.1f}%",
        'reading_time_original': estimate_reading_time(' '.join(['word'] * original_words)),
        'reading_time_summary': estimate_reading_time(' '.join(['word'] * summary_words))
    }
