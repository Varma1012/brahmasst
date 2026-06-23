import pandas as pd
import re
import io

def parse_and_clean_bed(file_stream, species_name, chrom_format):
    """
    Robust backend task: Parses genomic data files while safely ignoring 
    metadata headers, track configurations, or comment lines.
    """
    raw_text = file_stream.read().decode("utf-8")
    
    # Clean up empty carriage returns but keep structural lines
    lines = raw_text.strip().split("\n")
    
    # Filter out common genomic headers (lines starting with 'track', 'browser', or '#')
    clean_lines = [
        line for line in lines 
        if line.strip() and not line.startswith(("track", "browser", "#"))
    ]
    
    # Reconstruct clean text block
    processed_text = "\n".join(clean_lines)
    
    # Read text split by tabs, explicitly allowing pandas to handle messy tail lengths
    df = pd.read_csv(
        io.StringIO(processed_text), 
        sep="\t", 
        header=None, 
        on_bad_lines='skip' # Automatically skips lines that don't match the column shape
    )
    
    # Standard BED structures column layout naming setup
    standard_cols = ["Chromosome", "Start_Position", "End_Position", "Feature_Description", "Drop", "Strand"]
    df.columns = [standard_cols[i] if i < len(standard_cols) else f"Extra_{i}" for i in range(len(df.columns))]
    
    # Filter down to core columns
    keep_cols = ["Chromosome", "Start_Position", "End_Position", "Feature_Description", "Strand"]
    clean_df = df[[col for col in keep_cols if col in df.columns]].copy()
    
    if "Feature_Description" in clean_df.columns:
        clean_df["Feature_Description"] = clean_df["Feature_Description"].str.strip()
    
    # Filter rows based on the custom Chromosome Regular Expression
    try:
        regex_pattern = re.compile(chrom_format)
        clean_df = clean_df[clean_df["Chromosome"].astype(str).str.match(regex_pattern)]
    except Exception as e:
        raise ValueError(f"Invalid Regular Expression format: {str(e)}")
        
    # Inject the custom Species column up front
    clean_df.insert(0, "Species", species_name)
    
    return clean_df