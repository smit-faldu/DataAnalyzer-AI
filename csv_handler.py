"""
CSV and data file handler for DataAnalyzer Agent
Supports multiple file formats and provides data validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
import json
import logging

class DataFileHandler:
    """Handler for various data file formats"""
    
    def __init__(self, max_file_size: int = 10485760):  # 10MB default
        self.max_file_size = max_file_size
        self.supported_formats = {
            '.csv': self._read_csv,
            '.xlsx': self._read_excel,
            '.xls': self._read_excel,
            '.json': self._read_json,
            '.parquet': self._read_parquet
        }
        
    def load_data(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load data from file and return DataFrame with metadata
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Tuple of (DataFrame, metadata_dict)
        """
        file_path = Path(file_path)
        
        # Validate file
        self._validate_file(file_path)
        
        # Get file extension
        ext = file_path.suffix.lower()
        
        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}. Supported: {list(self.supported_formats.keys())}")
        
        # Load data using appropriate method
        df = self.supported_formats[ext](file_path)
        
        # Generate metadata
        metadata = self._generate_metadata(df, file_path)
        
        return df, metadata
    
    def _validate_file(self, file_path: Path):
        """Validate file exists and size is acceptable"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.1f}MB (max: {self.max_file_size / 1024 / 1024:.1f}MB)")
        
        if file_size == 0:
            raise ValueError("File is empty")
    
    def _read_csv(self, file_path: Path) -> pd.DataFrame:
        """Read CSV file with automatic encoding detection"""
        try:
            # Try UTF-8 first
            return pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Try common encodings
                for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                    try:
                        return pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                raise ValueError("Could not determine file encoding")
            except Exception as e:
                raise ValueError(f"Error reading CSV file: {str(e)}")
    
    def _read_excel(self, file_path: Path) -> pd.DataFrame:
        """Read Excel file"""
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
    
    def _read_json(self, file_path: Path) -> pd.DataFrame:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to convert dict to DataFrame
                return pd.DataFrame([data])
            else:
                raise ValueError("JSON structure not supported")
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {str(e)}")
    
    def _read_parquet(self, file_path: Path) -> pd.DataFrame:
        """Read Parquet file"""
        try:
            return pd.read_parquet(file_path)
        except Exception as e:
            raise ValueError(f"Error reading Parquet file: {str(e)}")
    
    def _generate_metadata(self, df: pd.DataFrame, file_path: Path) -> Dict[str, Any]:
        """Generate metadata about the loaded dataset"""
        metadata = {
            'file_info': {
                'name': file_path.name,
                'path': str(file_path),
                'size_mb': file_path.stat().st_size / 1024 / 1024,
                'format': file_path.suffix.lower()
            },
            'data_info': {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
                'null_counts': df.isnull().sum().to_dict(),
                'duplicate_rows': df.duplicated().sum()
            },
            'summary_stats': {}
        }
        
        # Add summary statistics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            metadata['summary_stats']['numeric'] = df[numeric_cols].describe().to_dict()
        
        # Add info about categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            metadata['summary_stats']['categorical'] = {}
            for col in categorical_cols:
                metadata['summary_stats']['categorical'][col] = {
                    'unique_count': df[col].nunique(),
                    'top_values': df[col].value_counts().head(5).to_dict()
                }
        
        return metadata
    
    def save_data(self, df: pd.DataFrame, file_path: str, format: str = 'csv') -> str:
        """
        Save DataFrame to file
        
        Args:
            df: DataFrame to save
            file_path: Output file path
            format: Output format ('csv', 'excel', 'json', 'parquet')
            
        Returns:
            Path to saved file
        """
        file_path = Path(file_path)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format.lower() == 'csv':
                df.to_csv(file_path, index=False)
            elif format.lower() in ['excel', 'xlsx']:
                df.to_excel(file_path, index=False)
            elif format.lower() == 'json':
                df.to_json(file_path, orient='records', indent=2)
            elif format.lower() == 'parquet':
                df.to_parquet(file_path, index=False)
            else:
                raise ValueError(f"Unsupported output format: {format}")
            
            return str(file_path)
        except Exception as e:
            raise ValueError(f"Error saving file: {str(e)}")
    
    def get_data_preview(self, df: pd.DataFrame, n_rows: int = 5) -> str:
        """Get a formatted preview of the data"""
        preview = f"Dataset Preview ({df.shape[0]} rows × {df.shape[1]} columns):\n"
        preview += "=" * 50 + "\n"
        preview += df.head(n_rows).to_string() + "\n\n"
        
        # Add column info
        preview += "Column Information:\n"
        preview += "-" * 20 + "\n"
        for col in df.columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            preview += f"• {col}: {dtype} ({null_count} nulls)\n"
        
        return preview
    
    def validate_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data quality and return issues"""
        issues = {
            'missing_data': {},
            'duplicates': 0,
            'data_types': {},
            'outliers': {},
            'recommendations': []
        }
        
        # Check for missing data
        null_counts = df.isnull().sum()
        issues['missing_data'] = {col: int(count) for col, count in null_counts.items() if count > 0}
        
        # Check for duplicates
        issues['duplicates'] = int(df.duplicated().sum())
        
        # Check data types
        issues['data_types'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # Check for potential outliers in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            if len(outliers) > 0:
                issues['outliers'][col] = len(outliers)
        
        # Generate recommendations
        if issues['missing_data']:
            issues['recommendations'].append("Consider handling missing data before analysis")
        if issues['duplicates'] > 0:
            issues['recommendations'].append("Consider removing duplicate rows")
        if issues['outliers']:
            issues['recommendations'].append("Review outliers in numeric columns")
        
        return issues