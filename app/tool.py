from langchain.tools import Tool
from datetime import datetime

def get_system_time(input: str = "") -> str:
    """Get the current system time as a formatted string.This function has no need any input."""
    
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ✅ Bu şekilde yapmak yerine @tool dekoratörü kullanılırsa hata aldım. O nedenle böyle yaptım.
tool_get_system_time = Tool.from_function(
    name="get_system_time",
    func=get_system_time,
    description="Returns the current system date and time in format YYYY-MM-DD HH:MM:SS. This function has no need any input."
)