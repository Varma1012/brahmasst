from flask import Flask, render_template, request
# Import your custom task module from the tasks folder
from tasks.data_cleaner import parse_and_clean_bed

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "bed_file" not in request.files:
            return render_template("index.html", error="No file selected.")
            
        file = request.files["bed_file"]
        species_name = request.form.get("species_name", "Unknown Species")
        chrom_format = request.form.get("chrom_format", ".*")
        
        if file.filename == "":
            return render_template("index.html", error="No file selected.")
            
        try:
            # Execute the isolated task from your tasks folder
            cleaned_df = parse_and_clean_bed(file, species_name, chrom_format)
            
            if cleaned_df.empty:
                return render_template("index.html", error="No rows matched your chromosome format pattern!")
                
            # Convert to HTML presentation layer
            table_html = cleaned_df.to_html(classes="table table-bordered table-striped mt-3", index=False)
            return render_template("index.html", table_html=table_html, species=species_name)
            
        except Exception as e:
            return render_template("index.html", error=f"Processing Error: {str(e)}")
            
    return render_template("index.html", table_html=None)

if __name__ == "__main__":
    app.run(debug=True)