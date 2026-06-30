from flask import (
    Flask,
    render_template,
    request,
    session
)

from tasks.genome_loader import (
    save_uploaded_file
)

from tasks.gff_engine import (
    parse_species_and_sex,
    search_gene
)

from tasks.compare_engine import (
    compare_traits
)


app = Flask(__name__)

app.secret_key = "genome_key"


@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    profile = session.get(
        "profile"
    )

    processing_complete = session.get(
        "processing_complete",
        False
    )

    parent2_ready = session.get(
        "parent2_ready",
        False
    )

    gene_result = []

    comparison = []

    error = None

    try:

        if request.method == "POST":

            # ====================
            # FIRST GENOME
            # ====================

            if "genome_file" in request.files:

                file = request.files[
                    "genome_file"
                ]

                if (
                    file.filename == ""
                ):
                    raise Exception(
                        "Select genome"
                    )

                session.clear()

                print(
                    "[DEBUG] Parent1 upload"
                )

                path = (
                    save_uploaded_file(
                        file,
                        "parent1"
                    )
                )

                species, sex = (
                    parse_species_and_sex(
                        path
                    )
                )

                profile = {

                    "species":
                    species,

                    "sex":
                    sex
                }

                session[
                    "profile"
                ] = profile

                session[
                    "uploaded_file"
                ] = path

                session[
                    "processing_complete"
                ] = True

                processing_complete = True

            # ====================
            # SECOND GENOME
            # ====================

            elif "partner_file" in request.files:

                file = request.files[
                    "partner_file"
                ]

                if (
                    file.filename == ""
                ):
                    raise Exception(
                        "Select second genome"
                    )

                print(
                    "[DEBUG] Parent2 upload"
                )

                path = (
                    save_uploaded_file(
                        file,
                        "parent2"
                    )
                )

                session[
                    "partner_file"
                ] = path

                session[
                    "parent2_ready"
                ] = True

                parent2_ready = True

            # ====================
            # GENE SEARCH
            # ====================

            elif request.form.get(
                "gene"
            ):

                genes = (
                    request.form
                    .get(
                        "gene"
                    )
                    .strip()
                )

                path = session.get(
                    "uploaded_file"
                )

                for gene in [

                    x.strip()

                    for x
                    in genes.split(",")

                    if x.strip()

                ]:

                    result = (
                        search_gene(
                            path,
                            gene
                        )
                    )

                    if not result:

                        result = {

                            "found":
                            False
                        }

                    result[
                        "gene"
                    ] = gene

                    gene_result.append(
                        result
                    )

            # ====================
            # COMPARE
            # ====================

            elif request.form.get(
                "compare"
            ):

                p1 = session.get(
                    "uploaded_file"
                )

                p2 = session.get(
                    "partner_file"
                )

                if not p1:

                    raise Exception(
                        "Genome 1 missing"
                    )

                if not p2:

                    raise Exception(
                        "Genome 2 missing"
                    )

                comparison = (
                    compare_traits(
                        p1,
                        p2
                    )
                )

    except Exception as e:

        error = str(
            e
        )

        print(
            "\n[ERROR]"
        )

        print(
            error
        )

    return render_template(

        "index.html",

        profile=profile,

        processing_complete=processing_complete,

        parent2_ready=parent2_ready,

        gene_result=gene_result,

        comparison=comparison,

        error=error
    )


@app.route(
    "/reset"
)
def reset():

    session.clear()

    return render_template(
        "index.html"
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )