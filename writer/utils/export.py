"""
Export Utility Module

This module provides functionality for exporting content history to Excel files.
It includes functions for creating, formatting, and saving Excel exports.
"""
import io
import os
from datetime import datetime

import pandas as pd

from writer.utils.logging_config import get_logger

# Get logger for this module
logger = get_logger(__name__)


def export_history_to_excel(history, export_path=None):
    """
    Export content history to an Excel file on disk.
    
    This function creates a formatted Excel file from the content history
    and saves it to the specified path or the current directory.
    
    Args:
        history (list): List of content dictionaries containing campaign details and generated content
        export_path (str, optional): Path to save the Excel file. If None, saves to the current directory.
        
    Returns:
        str: Path to the saved Excel file
        
    Raises:
        ValueError: If history is empty
    """
    logger.info(f"Exporting {len(history) if history else 0} content items to Excel")
    
    if not history:
        logger.warning("No content to export")
        raise ValueError("No content to export")
    
    try:
        # Create DataFrame from history
        logger.debug("Creating DataFrame from history")
        df = create_export_dataframe(history)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_export_{timestamp}.xlsx"
        logger.debug(f"Generated filename: {filename}")
        
        # Set export path
        if export_path is None:
            export_path = os.path.join(os.getcwd(), filename)
            logger.debug(f"Using current directory for export: {export_path}")
        else:
            export_path = os.path.join(export_path, filename)
            logger.debug(f"Using provided directory for export: {export_path}")
        
        # Export to Excel
        logger.debug(f"Writing DataFrame to Excel file: {export_path}")
        df.to_excel(export_path, index=False)
        
        logger.info(f"Successfully exported content to: {export_path}")
        return export_path
        
    except Exception as e:
        logger.error(f"Error exporting content to Excel: {str(e)}", exc_info=True)
        raise

def create_export_dataframe(history):
    """
    Create a pandas DataFrame from content history.
    
    This function transforms the content history list into a structured DataFrame
    with columns for campaign details and generated content.
    
    Args:
        history (list): List of content dictionaries containing campaign details and generated content
        
    Returns:
        pandas.DataFrame: DataFrame containing the content history with standardized columns
        
    Raises:
        ValueError: If history is empty
    """
    logger.debug(f"Creating export DataFrame from {len(history) if history else 0} content items")
    
    if not history:
        logger.warning("No content to export when creating DataFrame")
        raise ValueError("No content to export")
        
    try:
        # Create DataFrame from history
        df = pd.DataFrame([
            {
                "Campaign": item.get("campaign", ""),
                "Content Subject": item.get("content_subject", ""),
                "Target Audience": item.get("target_audience", ""),
                "LinkedIn": item.get("linkedin_content", ""),
                "X": item.get("x_content", ""),
                "Blog": item.get("blog_content", "")
            }
            for item in history
        ])
        
        logger.debug(f"Successfully created DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
        
    except Exception as e:
        logger.error(f"Error creating export DataFrame: {str(e)}", exc_info=True)
        raise

def get_excel_data(history):
    """
    Create Excel data in memory for download with proper formatting.
    
    This function is specifically designed for use with Streamlit's download_button,
    creating a formatted Excel file in memory and returning the bytes and filename.
    
    Args:
        history (list): List of content dictionaries containing campaign details and generated content
        
    Returns:
        tuple: (bytes, str) Excel file data as bytes and filename with timestamp
        
    Raises:
        ValueError: If history is empty
    """
    logger.info(f"Creating in-memory Excel data for {len(history) if history else 0} content items")
    
    if not history:
        logger.warning("No content to export for Excel download")
        raise ValueError("No content to export")
    
    try:
        # Process content to preserve formatting
        logger.debug("Processing content items for Excel export")
        processed_history = []
        for item in history:
            # Safely get content
            linkedin_content = item.get("linkedin_content", "") or ""
            x_content = item.get("x_content", "") or ""
            blog_content = item.get("blog_content", "") or ""
            
            processed_item = {
                "Campaign": item.get("campaign", ""),
                "Content Subject": item.get("content_subject", ""),
                "Target Audience": item.get("target_audience", ""),
                "LinkedIn": linkedin_content,
                "X": x_content,
                "Blog": blog_content
            }
            processed_history.append(processed_item)
        
        # Create DataFrame from processed history
        logger.debug("Creating DataFrame from processed history")
        df = pd.DataFrame(processed_history)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_export_{timestamp}.xlsx"
        logger.debug(f"Generated filename: {filename}")
        
        # Create a BytesIO object to hold the Excel data
        logger.debug("Creating in-memory Excel file")
        buffer = io.BytesIO()
        
        # Use xlsxwriter to create Excel file with custom formatting
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write the dataframe to the Excel file
            df.to_excel(writer, index=False, sheet_name='Content')
            logger.debug("Wrote DataFrame to Excel sheet")
            
            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Content']
            
            # Create a format for the cells with top-right alignment
            cell_format = workbook.add_format({
                'align': 'left',
                'valign': 'top',
                'text_wrap': True
            })
            
            # Apply the format to all cells
            logger.debug("Applying formatting to Excel columns")
            for col_num, col_name in enumerate(df.columns):
                # Set column width based on the maximum length of data in each column
                max_len = max(
                    df[col_name].astype(str).map(len).max(),
                    len(col_name)
                ) + 2
                worksheet.set_column(col_num, col_num, min(max_len, 50), cell_format)
            
            # Auto-fit row heights based on content
            logger.debug("Adjusting row heights based on content")
            for row_num in range(len(df) + 1):  # +1 for header row
                # Get the maximum number of lines in any cell in this row
                if row_num == 0:
                    # Header row
                    worksheet.set_row(row_num, 20)
                else:
                    # Data rows - calculate height based on content
                    row_data = df.iloc[row_num - 1]
                    max_lines = max([str(cell).count('\n') + 1 for cell in row_data])
                    # Set row height (approximately 15 points per line)
                    worksheet.set_row(row_num, max_lines * 15)
        
        logger.info("Successfully created formatted Excel data in memory")
        return buffer.getvalue(), filename
        
    except Exception as e:
        logger.error(f"Error creating Excel data: {str(e)}", exc_info=True)
        raise

def prepare_excel_export(history):
    """
    Prepare content history for Excel export by creating a temporary file.
    
    This function creates a temporary Excel file on disk, reads it into memory,
    and then deletes the file. This approach is an alternative to the in-memory
    approach used by get_excel_data.
    
    Args:
        history (list): List of content dictionaries containing campaign details and generated content
        
    Returns:
        tuple: (bytes, str) Excel file data as bytes and filename with timestamp
        
    Raises:
        ValueError: If history is empty
        Exception: If any error occurs during the export process
    """
    logger.info(f"Preparing Excel export for {len(history) if history else 0} content items using temp file")
    
    try:
        if not history:
            logger.warning("No content to export for Excel preparation")
            raise ValueError("No content to export")

        # Create DataFrame from history
        logger.debug("Creating DataFrame from history")
        df = create_export_dataframe(history)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_export_{timestamp}.xlsx"
        logger.debug(f"Generated filename: {filename}")
        
        # Create Excel file on disk
        logger.debug(f"Creating temporary Excel file: {filename}")
        excel_buffer = pd.ExcelWriter(filename, engine='xlsxwriter')
        df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        # Read the file as bytes
        logger.debug("Reading Excel file into memory")
        with open(filename, 'rb') as f:
            excel_data = f.read()
            
        # Remove the temporary file
        logger.debug(f"Removing temporary file: {filename}")
        os.remove(filename)
        
        logger.info("Successfully prepared Excel export data")
        return excel_data, filename
        
    except Exception as e:
        logger.error(f"Error preparing Excel export: {str(e)}", exc_info=True)
        raise Exception(f"Error preparing Excel export: {str(e)}")
