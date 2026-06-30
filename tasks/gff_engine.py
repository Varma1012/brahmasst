import re


def parse_species_and_sex(path):

    species = "Unknown species"

    genes = set()

    print("\n[DEBUG] Reading genome...")

    with open(path, "r", errors="ignore") as f:

        for line in f:

            if '/organism="' in line:

                m = re.search(r'"(.+?)"', line)

                if m:
                    species = m.group(1)

            if '/gene="' in line:

                m = re.search(r'"(.+?)"', line)

                if m:
                    genes.add(
                        m.group(1).upper()
                    )

    sex = detect_sex(genes)

    print("[DEBUG] Species:", species)
    print("[DEBUG] Sex:", sex)

    return species, sex


def detect_sex(genes):

    genes = set(
        x.upper()
        for x in genes
    )

    if "SRY" in genes:
        return "Male"

    if "AMELY" in genes:
        return "Male"

    if "AMELX" in genes:
        return "Female"

    return "Undetermined"


def search_gene(path, target):

    target = target.upper()

    chromosome = None
    location = None

    found = False

    previous = ""

    with open(path, "r", errors="ignore") as f:

        for line in f:

            line = line.rstrip()

            # chromosome
            if line.startswith("LOCUS"):

                parts = line.split()

                if len(parts) > 1:
                    chromosome = parts[1]

            # detect gene
            if '/gene="' in line:

                m = re.search(
                    r'"(.+?)"',
                    line
                )

                if m:

                    gene = (
                        m.group(1)
                        .upper()
                    )

                    if gene == target:

                        found = True

                        m2 = re.search(
                            r'(\d+\.\.\d+)',
                            previous
                        )

                        if m2:

                            location = (
                                m2.group(1)
                            )

                        break

            previous = line

    if found:

        sequence = ""

        try:

            if location:

                start, end = (

                    int(x)

                    for x in location.split("..")

                )

                print("\n===================")
                print("[DEBUG] EXTRACT")
                print("===================")

                print(
                    "[DEBUG] Gene:",
                    target
                )

                print(
                    "[DEBUG] Location:",
                    location
                )

                inside_origin = False

                genome = []

                with open(
                    path,
                    "r",
                    errors="ignore"
                ) as f:

                    for line in f:

                        if line.startswith(
                            "ORIGIN"
                        ):

                            inside_origin = True
                            continue

                        if inside_origin:

                            if line.startswith(
                                "//"
                            ):
                                break

                            parts = (
                                line
                                .strip()
                                .split()
                            )

                            if len(parts) > 1:

                                genome.append(

                                    "".join(
                                        parts[1:]
                                    )

                                )

                genome = (
                    "".join(
                        genome
                    )
                    .upper()
                )

                print(
                    "[DEBUG] Genome Size:",
                    len(genome)
                )

                sequence = genome[
                    start - 1:end
                ]

                print(
                    "[DEBUG] Sequence Size:",
                    len(sequence)
                )

                print(
                    "[DEBUG] Sequence Preview:"
                )

                print(
                    sequence[:200]
                )

        except Exception as e:

            print(
                "\n[DEBUG] Sequence Error:"
            )

            print(e)

            sequence = ""

        return {

            "found": True,

            "chromosome":
            chromosome,

            "location":
            location,

            "sequence":

            (

                sequence

                if sequence

                else

                "Sequence unavailable"

            )

        }

    return {

        "found": False

    }
def extract_gene_set(path):

    print("\n======================")
    print("[DEBUG] EXTRACT GENES")
    print("======================")

    genes = []

    chromosome = None
    previous = ""

    count = 0

    with open(path, "r", errors="ignore") as f:

        for line in f:

            line = line.rstrip()

            # ------------------
            # Detect chromosome
            # ------------------
            if line.startswith("LOCUS"):

                parts = line.split()

                if len(parts) > 1:

                    chromosome = parts[1]

            # ------------------
            # Detect gene
            # ------------------
            if '/gene="' in line:

                m = re.search(
                    r'"(.+?)"',
                    line
                )

                if m:

                    gene = (
                        m.group(1)
                        .upper()
                    )

                    location = None

                    m2 = re.search(
                        r'(\d+\.\.\d+)',
                        previous
                    )

                    if m2:

                        location = (
                            m2.group(1)
                        )

                    genes.append({

                        "gene": gene,

                        "chromosome": (
                            chromosome
                            if chromosome
                            else "Unknown"
                        ),

                        "location": (
                            location
                            if location
                            else "-"
                        )

                    })

                    count += 1

                    if count % 1000 == 0:

                        print(
                            "[DEBUG] Parsed:",
                            count
                        )

            previous = line

    print(
        "[DEBUG] Total genes:",
        len(genes)
    )

    print(
        "[DEBUG] Sample:",
        genes[:5]
    )

    print("======================\n")

    return genes