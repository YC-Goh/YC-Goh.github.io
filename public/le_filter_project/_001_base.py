
import re, os
from pathlib import Path
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment
from typing import Union, Tuple
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Tuple

filepaths = dict()
filepaths["project"] = Path(".").absolute()
filepaths = {
    "filter_maker": filepaths["project"].joinpath("filter_maker"), 
    "affix_id": filepaths["project"].joinpath("affix_id"), 
    "item_id": filepaths["project"].joinpath("item_id"), 
    "unique_id": filepaths["project"].joinpath("unique_id"), 
    "condition_list": filepaths["project"].joinpath("condition_list"), 
}
filepaths["filter_maker"] = {
    "input": filepaths["filter_maker"].joinpath("input"), 
    "output": filepaths["filter_maker"].joinpath("output"), 
}
for key in ["affix_id", "item_id", "unique_id"]:
    filepaths[key] = {
        "combined": filepaths[key].joinpath("combined"), 
        "game_data": {
            "processed": filepaths[key].joinpath("game_data", "processed"), 
            "raw": filepaths[key].joinpath("game_data", "raw"), 
        }, 
        "details": {
            "processed": filepaths[key].joinpath("details", "processed"), 
            "raw": filepaths[key].joinpath("details", "raw"), 
        }, 
    }

def strip_ws(text: str) -> str:
    return re.compile(r"\s+").sub(" ", text)

'''
def format_sheet(
    sheet: Worksheet,
    h_alignment: str = "left",
    v_alignment: str = "top", 
    freeze_panes: Tuple[int, int] = (1, 1)
) -> None:
    """
    Format a single worksheet with alignment and freeze panes.
    
    Args:
        sheet: openpyxl Worksheet object
        h_alignment: Horizontal alignment - "left", "centre", or "right"
        v_alignment: Vertical alignment - "top", "centre", or "bottom" 
        freeze_panes: Tuple of (row, column) to freeze at
    """
    # Map alignment strings to openpyxl constants
    h_map = {"left": "left", "centre": "center", "right": "right"}
    v_map = {"top": "top", "centre": "center", "bottom": "bottom"}
    
    # Create alignment object
    alignment = Alignment(
        horizontal=h_map.get(h_alignment, "left"),
        vertical=v_map.get(v_alignment, "top")
    )
    
    # Apply alignment to all cells with data
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.alignment = alignment
    
    # Set freeze panes
    row, col = freeze_panes
    if row > 0 and col > 0:
        # Convert to cell reference (e.g., (2,2) -> "B2")
        freeze_cell = sheet.cell(row=row, column=col).coordinate
        sheet.freeze_panes = freeze_cell

def format_workbook(
    file: Union[str, Workbook], 
    h_alignment: str = "left", 
    v_alignment: str = "top", 
    freeze_panes: Tuple[int, int] = (1, 1)
) -> None:
    """
    Format all worksheets in a workbook with alignment and freeze panes.
    
    Args:
        file: Either a filepath (str) or an openpyxl Workbook object
        h_alignment: Horizontal alignment - "left", "centre", or "right" 
        v_alignment: Vertical alignment - "top", "centre", or "bottom"
        freeze_panes: Tuple of (row, column) to freeze at
    """
    # If file is a string, load the workbook and call recursively
    if isinstance(file, (str, Path)):
        wb = load_workbook(file)
        format_workbook(wb, h_alignment, v_alignment, freeze_panes)
        wb.save(file)  # Save changes back to file
        return
    
    # If file is a Workbook, format each sheet
    wb = file
    for sheet in wb.worksheets:
        format_sheet(sheet, h_alignment, v_alignment, freeze_panes)
'''

def get_text_width_pixels(text: str, font_name: str = "calibri", font_size: int = 11) -> float:
    """
    Calculate the actual pixel width of text using PIL, accounting for font characteristics.
    
    Args:
        text: The text to measure
        font_name: Font name (calibri, arial, times, etc.)
        font_size: Font size in points
        
    Returns:
        Text width in pixels
    """
    try:
        # Create a dummy image for text measurement
        img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(img)
        
        """
        # Try to load the font - common font paths for different OS
        font_paths = [
            f"/mnt/c/Windows/Fonts/{font_name}.ttf",  # Windows
            f"/mnt/c/Windows/Fonts/{font_name}i.ttf",  # Windows italic variant
            f"/System/Library/Fonts/{font_name}.ttf",  # macOS
            f"/usr/share/fonts/truetype/{font_name}.ttf",  # Linux
        ]
        
        font = None
        for path in font_paths:
            if os.path.exists(path):
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except:
                    continue
        
        # Fall back to default font if specific font not found
        if font is None:
            font = ImageFont.load_default()
        """
        
        font = ImageFont.load_default(size=font_size)
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), str(text), font=font)
        width_pixels = bbox[2] - bbox[0]
        
        return width_pixels
        
    except Exception:
        # Fallback to character count method if PIL fails
        return len(str(text)) * 7  # Approximate pixels per character

def calculate_wrapped_lines(text: str, font_name: str, font_size: float, column_width_pixels: float) -> int:
    """
    Calculate how many lines text will wrap to in a given column width.
   
    Args:
        text: The text content
        font_name: Font name (e.g., "calibri")
        font_size: Font size in points
        column_width_pixels: Available width in pixels
   
    Returns:
        Number of lines the text will wrap to
    """
    if not text:
        return 1
   
    # Handle explicit line breaks
    lines = text.split('\n')
    total_lines = 0
   
    for line in lines:
        if not line:
            total_lines += 1
            continue
           
        # Calculate width of this line
        line_width_pixels = get_text_width_pixels(line, font_name, font_size)
       
        # Calculate how many visual lines this logical line will take
        if line_width_pixels <= column_width_pixels:
            total_lines += 1
        else:
            # Estimate wrapped lines - this is approximate
            wrapped_lines = max(1, int(line_width_pixels / column_width_pixels) + 1)
            total_lines += wrapped_lines
   
    return max(1, total_lines)

def pixels_to_excel_width(pixels: float) -> float:
    """
    Convert pixel width to Excel column width units.
    Excel width units are based on the width of '0' in the default font.
    
    Args:
        pixels: Width in pixels
        
    Returns:
        Width in Excel units
    """
    # Excel width unit is approximately 7 pixels for default font (Calibri 11pt)
    # This is a reasonable approximation
    return pixels / 7.0

def excel_width_to_pixels(excel_width: float) -> float:
    """
    Convert Excel column width units to pixels.
    Excel width is based on the width of '0' in the default font.
   
    Args:
        excel_width: Width in Excel units
       
    Returns:
        Width in pixels
    """
    # Approximate conversion: Excel width * 7 pixels per unit
    # This is based on default Calibri 11pt font
    return excel_width * 7

def format_sheet(
    sheet: Worksheet,
    h_alignment: str = "left",
    v_alignment: str = "top", 
    freeze_panes: Tuple[int, int] = (1, 1),
    auto_width: bool = True,
    wrap_text: bool = False
) -> None:
    """
    Format a single worksheet with alignment, freeze panes, auto-width columns, and auto-height rows.
    
    Args:
        sheet: openpyxl Worksheet object
        h_alignment: Horizontal alignment - "left", "centre", or "right"
        v_alignment: Vertical alignment - "top", "centre", or "bottom" 
        freeze_panes: Tuple of (row, column) to freeze at
        auto_width: Whether to automatically adjust column widths
        wrap_text: Whether to enable text wrapping in cells
    """
    # Map alignment strings to openpyxl constants
    h_map = {"left": "left", "centre": "center", "right": "right"}
    v_map = {"top": "top", "centre": "center", "bottom": "bottom"}
    
    # Create alignment object
    alignment = Alignment(
        horizontal=h_map.get(h_alignment, "left"),
        vertical=v_map.get(v_alignment, "top"),
        wrap_text=wrap_text
    )
    
    # Apply alignment to all cells with data
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.alignment = alignment
    
    # Set freeze panes
    row, col = freeze_panes
    if row > 0 and col > 0:
        # Convert to cell reference (e.g., (2,2) -> "B2")
        freeze_cell = sheet.cell(row=row, column=col).coordinate
        sheet.freeze_panes = freeze_cell
   
    # Store column widths for row height calculation
    column_widths = {}
    
    # Auto-adjust column widths using PIL for accurate text measurement
    if auto_width:
        for column in sheet.columns:
            max_width_pixels = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if cell.value:
                        # Get the font info from the cell (if available)
                        font_name = "calibri"  # Default Excel font
                        font_size = 11  # Default Excel font size
                        
                        # Try to get actual font from cell formatting
                        if cell.font and cell.font.name:
                            font_name = cell.font.name.lower()
                        if cell.font and cell.font.size:
                            font_size = cell.font.size
                        
                        # Calculate actual text width in pixels
                        text_width_pixels = get_text_width_pixels(
                            str(cell.value), font_name, font_size
                        )
                        
                        if text_width_pixels > max_width_pixels:
                            max_width_pixels = text_width_pixels
                except:
                    pass
            
            # Convert pixels to Excel width units and add padding
            if max_width_pixels > 0:
                excel_width = pixels_to_excel_width(max_width_pixels) + 4  # Add padding
                # Cap maximum width at reasonable size (equivalent to ~50 characters)
                excel_width = min(excel_width, 50)
                sheet.column_dimensions[column_letter].width = excel_width
                column_widths[column_letter] = excel_width
            else:
                # Store default width for empty columns
                column_widths[column_letter] = sheet.column_dimensions[column_letter].width or 8.43
    else:
        # If auto_width is disabled, get existing column widths
        for column in sheet.columns:
            column_letter = column[0].column_letter
            column_widths[column_letter] = sheet.column_dimensions[column_letter].width or 8.43
   
    # Auto-adjust row heights when wrap_text is enabled
    if wrap_text:
        for row_cells in sheet.iter_rows():
            max_height_needed = 15  # Default Excel row height in points
            row_number = row_cells[0].row
           
            for cell in row_cells:
                if cell.value is not None:
                    try:
                        # Get font info
                        font_name = "calibri"
                        font_size = 11
                       
                        if cell.font and cell.font.name:
                            font_name = cell.font.name.lower()
                        if cell.font and cell.font.size:
                            font_size = cell.font.size
                       
                        # Get column width in pixels
                        column_letter = cell.column_letter
                        column_width_excel = column_widths.get(column_letter, 8.43)
                        column_width_pixels = excel_width_to_pixels(column_width_excel)
                       
                        # Calculate how many lines the text will wrap to
                        text = str(cell.value)
                        lines_needed = calculate_wrapped_lines(
                            text, font_name, font_size, column_width_pixels
                        )
                       
                        # Calculate required height (font_size + padding per line)
                        line_height = font_size * 1.2  # Line spacing factor
                        required_height = lines_needed * line_height + 3  # Add padding
                       
                        if required_height > max_height_needed:
                            max_height_needed = required_height
                   
                    except:
                        pass
           
            # Set row height if it needs to be taller than default
            if max_height_needed > 15:
                sheet.row_dimensions[row_number].height = max_height_needed

def format_workbook(
    file: Union[str, Workbook], 
    h_alignment: str = "left", 
    v_alignment: str = "top", 
    freeze_panes: Tuple[int, int] = (1, 1),
    auto_width: bool = True,
    wrap_text: bool = False
) -> None:
    """
    Format all worksheets in a workbook with alignment, freeze panes, and auto-width.
    
    Args:
        file: Either a filepath (str) or an openpyxl Workbook object
        h_alignment: Horizontal alignment - "left", "centre", or "right" 
        v_alignment: Vertical alignment - "top", "centre", or "bottom"
        freeze_panes: Tuple of (row, column) to freeze at
        auto_width: Whether to automatically adjust column widths
    """
    # If file is a string, load the workbook and call recursively
    if isinstance(file, (str, Path, )):
        wb = load_workbook(file)
        format_workbook(wb, h_alignment, v_alignment, freeze_panes, auto_width, wrap_text)
        wb.save(file)  # Save changes back to file
        return
    
    # If file is a Workbook, format each sheet
    wb = file
    for sheet in wb.worksheets:
        format_sheet(sheet, h_alignment, v_alignment, freeze_panes, auto_width, wrap_text)
