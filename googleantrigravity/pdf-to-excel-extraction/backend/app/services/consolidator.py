"""
Data consolidation service for merging multiple document extractions.
"""

from typing import List, Dict, Any
from loguru import logger
from app.models.schemas import DocumentExtraction, ExtractedField
import pandas as pd


class Consolidator:
    """Consolidates data from multiple document extractions."""
    
    def consolidate(
        self,
        extractions: List[DocumentExtraction]
    ) -> pd.DataFrame:
        """
        Consolidate multiple document extractions into a single DataFrame.
        
        Args:
            extractions: List of DocumentExtraction objects
        
        Returns:
            Consolidated pandas DataFrame
        """
        try:
            logger.info(f"Consolidating {len(extractions)} document extractions")
            
            # Convert extractions to list of dictionaries
            records = []
            
            for extraction in extractions:
                if not extraction.success:
                    logger.warning(f"Skipping failed extraction: {extraction.filename}")
                    continue
                
                # Create a record from extracted fields
                record = {
                    "filename": extraction.filename,
                    "file_id": extraction.file_id,
                    "document_type": extraction.document_type.value,
                    "extraction_time": extraction.extraction_time,
                }
                
                # Add extracted fields
                for field in extraction.fields:
                    record[field.field_name] = field.value
                    
                    # Add confidence if available
                    if field.confidence is not None:
                        record[f"{field.field_name}_confidence"] = field.confidence
                
                records.append(record)
            
            if not records:
                logger.warning("No successful extractions to consolidate")
                return pd.DataFrame()
            
            # Create DataFrame
            df = pd.DataFrame(records)
            
            # Sort by common fields if they exist
            sort_columns = []
            if "invoice_date" in df.columns:
                sort_columns.append("invoice_date")
            elif "bill_date" in df.columns:
                sort_columns.append("bill_date")
            
            if sort_columns:
                df = df.sort_values(sort_columns)
            
            logger.success(f"Consolidated {len(df)} records with {len(df.columns)} columns")
            
            return df
            
        except Exception as e:
            logger.error(f"Error consolidating data: {e}")
            return pd.DataFrame()
    
    def group_by_type(
        self,
        extractions: List[DocumentExtraction]
    ) -> Dict[str, pd.DataFrame]:
        """
        Group extractions by document type and consolidate each group.
        
        Args:
            extractions: List of DocumentExtraction objects
        
        Returns:
            Dictionary mapping document type to DataFrame
        """
        try:
            logger.info(f"Grouping and consolidating {len(extractions)} documents by type")
            
            # Group by document type
            grouped = {}
            for extraction in extractions:
                doc_type = extraction.document_type.value
                if doc_type not in grouped:
                    grouped[doc_type] = []
                grouped[doc_type].append(extraction)
            
            # Consolidate each group
            result = {}
            for doc_type, group_extractions in grouped.items():
                df = self.consolidate(group_extractions)
                if not df.empty:
                    result[doc_type] = df
            
            logger.success(f"Created {len(result)} consolidated DataFrames")
            return result
            
        except Exception as e:
            logger.error(f"Error grouping by type: {e}")
            return {}
    
    def calculate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate summary statistics from consolidated data.
        
        Args:
            df: Consolidated DataFrame
        
        Returns:
            Dictionary of summary statistics
        """
        try:
            summary = {
                "total_records": len(df),
                "columns": list(df.columns),
            }
            
            # Calculate numeric summaries
            numeric_columns = df.select_dtypes(include=['number']).columns
            for col in numeric_columns:
                if col.endswith("_confidence"):
                    continue  # Skip confidence columns
                
                summary[f"{col}_sum"] = float(df[col].sum())
                summary[f"{col}_mean"] = float(df[col].mean())
                summary[f"{col}_min"] = float(df[col].min())
                summary[f"{col}_max"] = float(df[col].max())
            
            # Date range if dates exist
            date_columns = df.select_dtypes(include=['datetime64']).columns
            for col in date_columns:
                if col != "extraction_time":
                    summary[f"{col}_earliest"] = df[col].min()
                    summary[f"{col}_latest"] = df[col].max()
            
            return summary
            
        except Exception as e:
            logger.error(f"Error calculating summary: {e}")
            return {"error": str(e)}


# Global instance
consolidator = Consolidator()
