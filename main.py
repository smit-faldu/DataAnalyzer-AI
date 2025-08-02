"""
DataAnalyzer AI - Complete Project Launcher
Unified interface to run all components of the DataAnalyzer system
"""

import asyncio
import argparse
import sys
import os
import subprocess
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from data_analyzer import DataAnalyzer
from config import config


class DataAnalyzerMain:
    """Main launcher for the complete DataAnalyzer system"""
    
    def __init__(self):
        self.analyzer = None
    
    async def initialize(self):
        """Initialize the DataAnalyzer"""
        try:
            print("🚀 Initializing DataAnalyzer AI...")
            config.print_config()
            
            self.analyzer = DataAnalyzer()
            print("✅ DataAnalyzer AI ready!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize DataAnalyzer: {str(e)}")
            return False
    
    def show_main_menu(self):
        """Show the main menu"""
        print("\n" + "=" * 60)
        print("🎯 DataAnalyzer AI - Complete Data Analysis System")
        print("=" * 60)
        print("Choose how you want to use DataAnalyzer:")
        print()
        print("1. 🌐 Web Application (Streamlit) - User-friendly interface")
        print("2. 🖥️  Command Line Interface - For developers and power users")
        print("3. 📊 Quick Analysis - Analyze a CSV file with one question")
        print("4. 🔄 Batch Analysis - Run multiple questions on a CSV file")
        print("5. 🎮 Interactive Mode - Step-by-step analysis session")
        print("6. ⚙️  Configuration Info - Show current settings")
        print("7. 🧹 Clean Temporary Files - Remove temp files and cache")
        print("8. ❌ Exit")
        print("=" * 60)
    
    def launch_web_app(self):
        """Launch the Streamlit web application"""
        print("\n🌐 Launching DataAnalyzer Web Application...")
        print("=" * 50)
        
        # Check if streamlit is available
        try:
            import streamlit
            print("✅ Streamlit found")
        except ImportError:
            print("❌ Streamlit not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "plotly"])
            print("✅ Streamlit installed")
        
        # Check for app file
        app_file = Path(__file__).parent / "app.py"
        if not app_file.exists():
            print("❌ Web app file not found")
            return
        
        print(f"📁 App file: {app_file}")
        print("🌐 Starting web server...")
        print("📱 The web app will open in your browser automatically")
        print("🔗 URL: http://localhost:8501")
        print("=" * 50)
        print("💡 To stop the web app, press Ctrl+C")
        print()
        
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", str(app_file),
                "--server.port", "8501",
                "--server.address", "localhost"
            ])
        except KeyboardInterrupt:
            print("\n👋 Web application stopped")
        except Exception as e:
            print(f"❌ Error starting web app: {e}")
    
    async def quick_analysis(self):
        """Quick analysis mode"""
        print("\n📊 Quick Analysis Mode")
        print("=" * 30)
        
        # Get file path
        file_path = input("📁 Enter path to your CSV file: ").strip().strip('"')
        if not file_path or not Path(file_path).exists():
            print("❌ File not found")
            return
        
        # Get question
        question = input("❓ Enter your question: ").strip()
        if not question:
            print("❌ No question provided")
            return
        
        print(f"\n🔄 Analyzing '{Path(file_path).name}'...")
        print(f"❓ Question: {question}")
        print("-" * 50)
        
        try:
            # Load data
            result = self.analyzer.load_data(file_path)
            if not result['success']:
                print(f"❌ Failed to load data: {result['error']}")
                return
            
            print("✅ Data loaded successfully!")
            
            # Ask question
            await self.analyzer.ask_agent(question, execute_code=True)
            
            # Auto-save outputs
            copied_files = self.analyzer.copy_outputs_to_output_dir()
            if copied_files:
                print(f"\n📁 Copied {len(copied_files)} files to output directory:")
                for file_path in copied_files:
                    print(f"• {Path(file_path).name}")
            
            # Cleanup
            self.analyzer.cleanup()
            print("🧹 Temporary files cleaned up")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    async def batch_analysis(self):
        """Batch analysis mode"""
        print("\n🔄 Batch Analysis Mode")
        print("=" * 30)
        
        # Get file path
        file_path = input("📁 Enter path to your CSV file: ").strip().strip('"')
        if not file_path or not Path(file_path).exists():
            print("❌ File not found")
            return
        
        # Get questions
        questions = []
        print("❓ Enter your questions (press Enter twice when done):")
        while True:
            question = input(f"Question {len(questions) + 1}: ").strip()
            if not question:
                if questions:
                    break
                else:
                    print("❌ Please enter at least one question")
                    continue
            questions.append(question)
        
        print(f"\n🔄 Running batch analysis on '{Path(file_path).name}'...")
        print(f"📝 {len(questions)} questions to process")
        print("-" * 50)
        
        try:
            # Load data
            result = self.analyzer.load_data(file_path)
            if not result['success']:
                print(f"❌ Failed to load data: {result['error']}")
                return
            
            print("✅ Data loaded successfully!")
            
            # Process each question
            for i, question in enumerate(questions, 1):
                print(f"\n🔄 Processing question {i}/{len(questions)}")
                print(f"❓ {question}")
                print("-" * 30)
                
                await self.analyzer.ask_agent(question, execute_code=True)
            
            # Auto-save outputs
            copied_files = self.analyzer.copy_outputs_to_output_dir()
            if copied_files:
                print(f"\n📁 Copied {len(copied_files)} files to output directory:")
                for file_path in copied_files:
                    print(f"• {Path(file_path).name}")
            
            # Cleanup
            self.analyzer.cleanup()
            print("🧹 Temporary files cleaned up")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    async def interactive_mode(self):
        """Interactive analysis mode"""
        print("\n🎮 Interactive Analysis Mode")
        print("=" * 40)
        print("Available commands:")
        print("  load <file_path> - Load a data file")
        print("  summary          - Show data summary")
        print("  ask <question>   - Ask the AI agent")
        print("  outputs          - List generated files")
        print("  save             - Copy outputs to output directory")
        print("  help             - Show this help")
        print("  quit/exit        - Exit interactive mode")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Enter command: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                # Parse command
                parts = user_input.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == 'load':
                    if not args:
                        print("❌ Please provide a file path: load <file_path>")
                        continue
                    await self._load_data_command(args)
                
                elif command == 'summary':
                    await self._summary_command()
                
                elif command == 'ask':
                    if not args:
                        print("❌ Please provide a question: ask <your question>")
                        continue
                    await self._ask_command(args)
                
                elif command == 'outputs':
                    await self._outputs_command()
                
                elif command == 'save':
                    await self._save_command()
                
                elif command == 'help':
                    print("\nAvailable commands:")
                    print("  load <file_path> - Load a data file")
                    print("  summary          - Show data summary")
                    print("  ask <question>   - Ask the AI agent")
                    print("  outputs          - List generated files")
                    print("  save             - Copy outputs to output directory")
                    print("  help             - Show this help")
                    print("  quit/exit        - Exit interactive mode")
                
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands or 'quit' to exit.")
            
            except KeyboardInterrupt:
                print("\n\n👋 Exiting interactive mode...")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    async def _load_data_command(self, file_path: str):
        """Handle load data command"""
        try:
            result = self.analyzer.load_data(file_path)
            
            if result['success']:
                print("\n📊 Data loaded successfully!")
                print(result['preview'])
                
                # Show quality report
                quality = result['quality_report']
                if quality['missing_data'] or quality['duplicates'] > 0 or quality['outliers']:
                    print("\n⚠️ Data Quality Issues:")
                    if quality['missing_data']:
                        print(f"• Missing data in columns: {list(quality['missing_data'].keys())}")
                    if quality['duplicates'] > 0:
                        print(f"• {quality['duplicates']} duplicate rows found")
                    if quality['outliers']:
                        print(f"• Outliers detected in columns: {list(quality['outliers'].keys())}")
                    
                    if quality['recommendations']:
                        print("\n💡 Recommendations:")
                        for rec in quality['recommendations']:
                            print(f"• {rec}")
                else:
                    print("\n✅ No major data quality issues detected")
            else:
                print(f"❌ Failed to load data: {result['error']}")
        
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
    
    async def _summary_command(self):
        """Handle summary command"""
        summary = self.analyzer.get_data_summary()
        print(summary)
    
    async def _ask_command(self, question: str):
        """Handle ask command"""
        try:
            result = await self.analyzer.ask_agent(question, execute_code=True)
            
            if not result['success']:
                print(f"❌ Error: {result['error']}")
        
        except Exception as e:
            print(f"❌ Error asking agent: {str(e)}")
    
    async def _outputs_command(self):
        """Handle outputs command"""
        try:
            files = self.analyzer.list_output_files()
            if files:
                print(f"\n📁 Generated files ({len(files)}):")
                for file_path in files:
                    file_name = Path(file_path).name
                    file_size = Path(file_path).stat().st_size / 1024  # KB
                    print(f"• {file_name} ({file_size:.1f} KB)")
            else:
                print("\n📁 No output files generated yet")
        except Exception as e:
            print(f"❌ Error listing outputs: {str(e)}")
    
    async def _save_command(self):
        """Handle save command"""
        try:
            copied_files = self.analyzer.copy_outputs_to_output_dir()
            if copied_files:
                print(f"\n💾 Copied {len(copied_files)} files to output directory:")
                for file_path in copied_files:
                    print(f"• {Path(file_path).name}")
            else:
                print("\n💾 No files to copy")
        except Exception as e:
            print(f"❌ Error saving outputs: {str(e)}")
    
    def clean_temp_files(self):
        """Clean temporary files and cache"""
        print("\n🧹 Cleaning temporary files...")
        
        cleaned_count = 0
        
        # Clean temp directory
        temp_dir = Path(__file__).parent / "temp"
        if temp_dir.exists():
            for item in temp_dir.iterdir():
                try:
                    if item.is_dir():
                        import shutil
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                    cleaned_count += 1
                except Exception as e:
                    print(f"⚠️ Could not remove {item}: {e}")
        
        # Clean __pycache__
        pycache_dir = Path(__file__).parent / "__pycache__"
        if pycache_dir.exists():
            try:
                import shutil
                shutil.rmtree(pycache_dir)
                cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove __pycache__: {e}")
        
        print(f"✅ Cleaned {cleaned_count} items")
    
    async def run_menu(self):
        """Run the main menu interface"""
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\n🎯 Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.launch_web_app()
                elif choice == '2':
                    print("\n🖥️ Command Line Interface")
                    print("Use: python main.py --help for CLI options")
                    print("Or continue with the menu for guided experience")
                elif choice == '3':
                    await self.quick_analysis()
                elif choice == '4':
                    await self.batch_analysis()
                elif choice == '5':
                    await self.interactive_mode()
                elif choice == '6':
                    config.print_config()
                elif choice == '7':
                    self.clean_temp_files()
                elif choice == '8':
                    print("\n👋 Thank you for using DataAnalyzer AI!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-8.")
                
                if choice in ['3', '4', '5']:
                    input("\n⏸️ Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thank you for using DataAnalyzer AI!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                input("\n⏸️ Press Enter to continue...")


async def main():
    """Main entry point"""
    
    # Set Windows event loop policy if on Windows
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("✅ Set Windows ProactorEventLoopPolicy")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="DataAnalyzer AI - AI-Powered Data Analysis (Web App by Default)")
    parser.add_argument('--ask', nargs=2, metavar=('FILE', 'QUESTION'), help='Quick analysis: file and question')
    parser.add_argument('--batch', nargs='+', metavar='FILE_AND_QUESTIONS', help='Batch analysis: file and questions')
    parser.add_argument('--interactive', action='store_true', help='Start in interactive mode')
    parser.add_argument('--config', action='store_true', help='Show configuration')
    parser.add_argument('--clean', action='store_true', help='Clean temporary files')
    
    args = parser.parse_args()
    
    # Initialize the main system
    main_system = DataAnalyzerMain()
    
    # Handle direct commands
    if args.config:
        config.print_config()
        return
    
    if args.clean:
        main_system.clean_temp_files()
        return
    
    # Initialize analyzer for other commands
    if not await main_system.initialize():
        return
    
    if args.ask:
        file_path, question = args.ask
        try:
            result = main_system.analyzer.load_data(file_path)
            if result['success']:
                await main_system.analyzer.ask_agent(question, execute_code=True)
                copied_files = main_system.analyzer.copy_outputs_to_output_dir()
                if copied_files:
                    print(f"\n📁 Copied {len(copied_files)} files to output directory")
                main_system.analyzer.cleanup()
            else:
                print(f"❌ Failed to load data: {result['error']}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        return
    
    if args.batch:
        file_path = args.batch[0]
        questions = args.batch[1:]
        try:
            result = main_system.analyzer.load_data(file_path)
            if result['success']:
                for i, question in enumerate(questions, 1):
                    print(f"\n🔄 Processing question {i}/{len(questions)}: {question}")
                    await main_system.analyzer.ask_agent(question, execute_code=True)
                copied_files = main_system.analyzer.copy_outputs_to_output_dir()
                if copied_files:
                    print(f"\n📁 Copied {len(copied_files)} files to output directory")
                main_system.analyzer.cleanup()
            else:
                print(f"❌ Failed to load data: {result['error']}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        return
    
    if args.interactive:
        await main_system.interactive_mode()
        return
    
    # If no arguments, launch web app directly
    main_system.launch_web_app()


if __name__ == "__main__":
    asyncio.run(main())