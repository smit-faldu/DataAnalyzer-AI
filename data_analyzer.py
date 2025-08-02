"""
Core DataAnalyzer Agent class
Handles AI agent creation, code execution, and data analysis workflows
"""

import os
import sys
import tempfile
import subprocess
import asyncio
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import pandas as pd

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage

from config import config
from csv_handler import DataFileHandler


class DataAnalyzer:
    """Main DataAnalyzer Agent class"""
    
    def __init__(self):
        self.config = config
        self.data_handler = DataFileHandler(max_file_size=config.max_file_size)
        self.model_client = None
        self.agent = None
        self.temp_dir = None
        self.current_data = None
        self.current_metadata = None
        
        # Initialize components
        self._setup_model_client()
        self._setup_temp_directory()
        self._create_agent()
    
    def _setup_model_client(self):
        """Setup the AI model client"""
        try:
            self.model_client = OpenAIChatCompletionClient(
                model=self.config.model_name,
                api_key=self.config.gemini_api_key,
            )
            print("✅ Model client setup complete!")
        except Exception as e:
            raise RuntimeError(f"Failed to setup model client: {str(e)}")
    
    def _setup_temp_directory(self):
        """Setup temporary directory for code execution"""
        self.temp_dir = tempfile.mkdtemp(dir=self.config.temp_dir)
        print(f"✅ Temporary directory created: {self.temp_dir}")
    
    def _create_agent(self):
        """Create the DataAnalyst Agent"""
        system_message = """You are a DataAnalyst Agent specialized in data analysis and visualization.

Your capabilities:
- Analyze data using pandas, numpy, matplotlib, and seaborn
- Write Python code to solve data analysis problems
- Create visualizations and statistical summaries
- Handle CSV files, data cleaning, and preprocessing
- Perform exploratory data analysis (EDA)
- Generate insights and recommendations

When writing code:
1. Always import required libraries (pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns)
2. IMPORTANT: The matplotlib backend is already set to 'Agg' - DO NOT use plt.use('Agg') or matplotlib.use('Agg') in your code
3. Write clean, well-commented code
4. Include print statements to show results
5. For plots, use plt.savefig() to save them with descriptive names
6. Handle errors gracefully with try-except blocks
7. Provide meaningful variable names and comments
8. Always use plt.close() after saving plots to free memory

Data context:
- The current dataset is available as 'df' variable
- Always check data shape, types, and missing values first
- Provide insights and interpretations of your analysis
- Suggest next steps or additional analyses when appropriate

Format your code in ```python code blocks for execution.
Always explain what your code does before and after the code block."""

        try:
            self.agent = AssistantAgent(
                name="DataAnalystAgent",
                model_client=self.model_client,
                system_message=system_message
            )
            print("✅ DataAnalyst Agent created successfully!")
        except Exception as e:
            raise RuntimeError(f"Failed to create agent: {str(e)}")
    
    def load_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from file
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Dictionary with loading results and metadata
        """
        try:
            print(f"📁 Loading data from: {file_path}")
            
            # Load data using handler
            df, metadata = self.data_handler.load_data(file_path)
            
            # Store current data
            self.current_data = df
            self.current_metadata = metadata
            
            # Save data to temp directory for agent access
            temp_data_path = Path(self.temp_dir) / "current_data.csv"
            df.to_csv(temp_data_path, index=False)
            
            print("✅ Data loaded successfully!")
            print(f"📊 Dataset shape: {df.shape}")
            print(f"📋 Columns: {list(df.columns)}")
            
            return {
                'success': True,
                'data': df,
                'metadata': metadata,
                'preview': self.data_handler.get_data_preview(df),
                'quality_report': self.data_handler.validate_data_quality(df)
            }
            
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def load_data_from_dataframe(self, df: 'pd.DataFrame', filename: str = "uploaded_data") -> Dict[str, Any]:
        """
        Load data from an existing DataFrame (for Streamlit file uploads)
        
        Args:
            df: Pandas DataFrame
            filename: Original filename for reference
            
        Returns:
            Dictionary with loading results and metadata
        """
        try:
            print(f"📁 Loading data from DataFrame: {filename}")
            
            # Create metadata for the DataFrame
            metadata = {
                'file_info': {
                    'name': filename,
                    'size_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
                    'format': filename.split('.')[-1] if '.' in filename else 'csv'
                },
                'data_info': {
                    'shape': df.shape,
                    'columns': list(df.columns),
                    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                    'null_counts': df.isnull().sum().to_dict(),
                    'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
                    'duplicate_rows': df.duplicated().sum()
                }
            }
            
            # Store current data
            self.current_data = df
            self.current_metadata = metadata
            
            # Save data to temp directory for agent access
            temp_data_path = Path(self.temp_dir) / "current_data.csv"
            df.to_csv(temp_data_path, index=False)
            
            print("✅ Data loaded successfully!")
            print(f"📊 Dataset shape: {df.shape}")
            print(f"📋 Columns: {list(df.columns)}")
            
            return {
                'success': True,
                'data': df,
                'metadata': metadata,
                'preview': self.data_handler.get_data_preview(df),
                'quality_report': self.data_handler.validate_data_quality(df)
            }
            
        except Exception as e:
            print(f"❌ Error loading DataFrame: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in isolated environment
        
        Args:
            code: Python code to execute
            
        Returns:
            Dictionary with execution results
        """
        print("🔧 Executing code...")
        
        # Prepare code with data loading if current data exists
        if self.current_data is not None:
            # Ensure current data is saved to CSV file
            current_data_path = Path(self.temp_dir) / "current_data.csv"
            try:
                self.current_data.to_csv(current_data_path, index=False)
                print(f"📊 Data saved to: {current_data_path}")
            except Exception as e:
                print(f"❌ Error saving data: {e}")
                return {
                    "success": False,
                    "error": f"Failed to save current data: {str(e)}",
                    "exit_code": -1
                }
            
            data_setup = f"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Load current dataset
df = pd.read_csv(r'{current_data_path}')
print(f"Loaded dataset: {{df.shape[0]}} rows x {{df.shape[1]}} columns")
print(f"Columns: {{list(df.columns)}}")
print()

"""
            full_code = data_setup + code
        else:
            full_code = code
        
        # Create temporary Python file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, 
                                       dir=self.temp_dir, encoding='utf-8') as f:
            f.write(full_code)
            temp_file = f.name
        
        try:
            # Execute the Python file with proper encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                cwd=self.temp_dir,
                timeout=self.config.timeout,
                env=env,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                print("✅ Code executed successfully!")
                return {
                    "success": True,
                    "output": result.stdout,
                    "exit_code": result.returncode
                }
            else:
                print(f"❌ Code execution failed with exit code: {result.returncode}")
                return {
                    "success": False,
                    "error": result.stderr or result.stdout,
                    "exit_code": result.returncode
                }
        
        except subprocess.TimeoutExpired:
            print("❌ Code execution timed out")
            return {
                "success": False,
                "error": f"Code execution timed out ({self.config.timeout} seconds)",
                "exit_code": -1
            }
        except Exception as e:
            print(f"❌ Exception during code execution: {str(e)}")
            return {
                "success": False,
                "error": f"Exception: {str(e)}",
                "exit_code": -1
            }
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def _preprocess_code(self, code: str) -> str:
        """
        Preprocess code to fix common issues
        
        Args:
            code: Raw code from AI response
            
        Returns:
            Cleaned code ready for execution
        """
        # Remove problematic matplotlib backend calls since we set it in data_setup
        code = re.sub(r'plt\.use\([\'"]Agg[\'"]\)', '', code)
        code = re.sub(r'matplotlib\.use\([\'"]Agg[\'"]\)', '', code)
        
        # Remove redundant matplotlib imports since we already import it
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip redundant imports that are already in data_setup
            if (line.strip().startswith('import matplotlib') and 
                ('matplotlib.use' in line or line.strip() == 'import matplotlib')):
                continue
            if line.strip().startswith('matplotlib.use('):
                continue
            if line.strip().startswith('plt.use('):
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    async def ask_agent(self, question: str, execute_code: bool = True) -> Dict[str, Any]:
        """
        Send a question to the agent and optionally execute generated code
        
        Args:
            question: Question to ask the agent
            execute_code: Whether to execute any code blocks in the response
            
        Returns:
            Dictionary with agent response and execution results
        """
        print(f"🤖 Asking agent: {question}")
        print("=" * 50)
        
        try:
            # Add data context to question if data is loaded
            if self.current_data is not None:
                data_context = f"""
Current dataset information:
- Shape: {self.current_data.shape}
- Columns: {list(self.current_data.columns)}
- Data types: {dict(self.current_data.dtypes)}

Question: {question}
"""
            else:
                data_context = question
            
            # Create message for the agent
            message = TextMessage(content=data_context, source="user")
            
            # Get agent response
            response = await self.agent.on_messages([message], CancellationToken())
            
            print("🤖 Agent Response:")
            print(response.chat_message.content)
            print("\n" + "=" * 50)
            
            result = {
                'success': True,
                'response': response.chat_message.content,
                'code_blocks': [],
                'execution_results': []
            }
            
            if execute_code:
                # Extract and execute code blocks
                code_blocks = re.findall(r'```python\n(.*?)\n```', response.chat_message.content, re.DOTALL)
                
                if code_blocks:
                    print(f"\n🔧 Found {len(code_blocks)} code block(s) to execute...\n")
                    
                    for i, code in enumerate(code_blocks, 1):
                        print(f"--- Executing Code Block {i} ---")
                        
                        # Preprocess code to fix common issues
                        cleaned_code = self._preprocess_code(code.strip())
                        exec_result = self.execute_code(cleaned_code)
                        
                        result['code_blocks'].append(code.strip())
                        result['execution_results'].append(exec_result)
                        
                        if exec_result["success"]:
                            print("Output:")
                            print(exec_result["output"])
                        else:
                            print("Error:")
                            print(exec_result["error"])
                        print()
                else:
                    print("\nℹ️ No code blocks found in agent response.")
            
            return result
            
        except Exception as e:
            print(f"❌ Error communicating with agent: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_data_summary(self) -> Optional[str]:
        """Get summary of currently loaded data"""
        if self.current_data is None:
            return "No data currently loaded."
        
        summary = f"""
📊 Current Dataset Summary:
{'=' * 30}
• File: {self.current_metadata['file_info']['name']}
• Shape: {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns
• Size: {self.current_metadata['file_info']['size_mb']:.2f} MB
• Memory usage: {self.current_metadata['data_info']['memory_usage_mb']:.2f} MB

📋 Columns ({len(self.current_data.columns)}):
{', '.join(self.current_data.columns)}

🔍 Data Quality:
• Missing values: {sum(self.current_metadata['data_info']['null_counts'].values())} total
• Duplicate rows: {self.current_metadata['data_info']['duplicate_rows']}

📈 Data Types:
"""
        for col, dtype in self.current_metadata['data_info']['dtypes'].items():
            null_count = self.current_metadata['data_info']['null_counts'][col]
            summary += f"• {col}: {dtype} ({null_count} nulls)\n"
        
        return summary
    
    def list_output_files(self) -> List[str]:
        """List files created in the temp directory (plots, exports, etc.)"""
        temp_path = Path(self.temp_dir)
        files = []
        
        for file_path in temp_path.iterdir():
            if file_path.is_file() and file_path.name != "current_data.csv":
                files.append(str(file_path))
        
        return files
    
    def copy_outputs_to_output_dir(self) -> List[str]:
        """Copy generated files to the output directory"""
        import shutil
        
        output_files = self.list_output_files()
        copied_files = []
        
        for file_path in output_files:
            file_path = Path(file_path)
            dest_path = self.config.output_dir / file_path.name
            
            try:
                shutil.copy2(file_path, dest_path)
                copied_files.append(str(dest_path))
                print(f"📁 Copied: {file_path.name} → {dest_path}")
            except Exception as e:
                print(f"❌ Failed to copy {file_path.name}: {str(e)}")
        
        return copied_files
    
    def cleanup(self):
        """Clean up temporary files and directories"""
        if self.temp_dir and Path(self.temp_dir).exists():
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
                print("🧹 Temporary files cleaned up")
            except Exception as e:
                print(f"⚠️ Warning: Could not clean up temp directory: {str(e)}")
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()