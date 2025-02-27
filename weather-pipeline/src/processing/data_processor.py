import pandas as pd

class DataProcessor:
    @staticmethod
    def process_silver(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and transform data for silver layer"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Convert date columns to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        
        return df

    @staticmethod
    def process_gold(df: pd.DataFrame) -> pd.DataFrame:
        """Transform data for gold layer (analytics-ready)"""
        # Add your aggregations here
        # Example: Calculate hourly averages
        if 'timestamp' in df.columns:
            df_gold = df.groupby(pd.Grouper(key='timestamp', freq='H')).mean()
            df_gold = df_gold.reset_index()
        else:
            df_gold = df
            
        return df_gold