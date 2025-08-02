"""
Configuration module for DataAnalyzer Agent
Handles environment variables and application settings
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Configuration class for DataAnalyzer Agent"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('MODEL_NAME', 'gemini-2.5-flash')
        
        # Application settings
        self.timeout = int(os.getenv('CODE_TIMEOUT', '60'))
        self.max_file_size = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB
        
        # Directories
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        # Windows-specific event loop setup
        self._setup_event_loop()
    
    def _setup_event_loop(self):
        """Setup proper event loop policy for Windows"""
        if sys.platform == 'win32':
            try:
                # Check if we're already in an event loop (like Jupyter)
                asyncio.get_running_loop()
                print("⚠️ Running in existing event loop")
            except RuntimeError:
                # Not in an event loop, safe to set policy
                asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                print("✅ Set Windows ProactorEventLoopPolicy")
        else:
            print("✅ Non-Windows system, no event loop policy change needed")
    
    def validate(self):
        """Validate configuration"""
        errors = []
        
        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY not found in environment variables")
        
        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(f"- {error}" for error in errors))
        
        return True
    
    def get_supported_file_types(self):
        """Get list of supported file types"""
        return ['.csv', '.xlsx', '.xls', '.json', '.parquet']
    
    def print_config(self):
        """Print current configuration"""
        print("\n" + "="*50)
        print("🔧 DATAANALYZER AI CONFIGURATION")
        print("="*50)
        print(f"📁 Base Directory: {self.base_dir}")
        print(f"📊 Data Directory: {self.data_dir}")
        print(f"📤 Output Directory: {self.output_dir}")
        print(f"🗂️ Temp Directory: {self.temp_dir}")
        print(f"🤖 AI Model: {self.model_name}")
        print(f"⏱️ Timeout: {self.timeout} seconds")
        print(f"📏 Max File Size: {self.max_file_size / 1024 / 1024:.1f} MB")
        print(f"🔑 API Key: {'✅ Set' if self.gemini_api_key else '❌ Not Set'}")
        print(f"📋 Supported Formats: {', '.join(self.get_supported_file_types())}")
        print("="*50)
    
    def __str__(self):
        """String representation of config (without sensitive data)"""
        return f"""DataAnalyzer Configuration:
- Model: {self.model_name}
- Timeout: {self.timeout}s
- Max file size: {self.max_file_size / 1024 / 1024:.1f}MB
- Data directory: {self.data_dir}
- Output directory: {self.output_dir}
- Supported formats: {', '.join(self.get_supported_file_types())}
- API Key: {'✅ Set' if self.gemini_api_key else '❌ Missing'}"""

# Global config instance
config = Config()