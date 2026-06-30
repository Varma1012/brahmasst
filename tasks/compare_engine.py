from tasks.gff_engine import search_gene


TARGET_TRAIT = "Sugar Metabolism"


# gene → (variant_position , risk_base)
VARIANT_RULES = {

    "TCF7L2": (314, "T"),

    "INS": (150, "A"),

    "IRS1": (800, "C"),

    "PPARG": (1200, "G"),

    "SLC30A8": (900, "T")

}


def is_sex_chromosome(chromosome):

    chromosome = str(
        chromosome
    ).upper()

    return (

        chromosome.endswith("X")
        or
        chromosome.endswith("Y")

    )


def detect_variant(
    sequence,
    gene,
    parent
):

    print("\n------------------")
    print("[DEBUG]", gene)
    print("[DEBUG]", parent)

    if (
        not sequence
        or
        sequence
        ==
        "Sequence extraction disabled"
    ):

        print(
            "[DEBUG] Sequence unavailable"
        )

        return 0

    sequence = (
        sequence
        .replace(
            "\n",
            ""
        )
        .replace(
            " ",
            ""
        )
        .upper()
    )

    position, risk = (
        VARIANT_RULES[gene]
    )

    print(
        "[DEBUG] Sequence Length:",
        len(sequence)
    )

    print(
        "[DEBUG] Variant Position:",
        position
    )

    print(
        "[DEBUG] Expected Risk Base:",
        risk
    )

    if position >= len(sequence):

        print(
            "[DEBUG] Position outside sequence"
        )

        return 0

    actual = (
        sequence[position]
    )

    print(
        "[DEBUG] Actual Base:",
        actual
    )

    if actual == risk:

        print(
            "[DEBUG] Risk Variant FOUND"
        )

        return 1

    print(
        "[DEBUG] Variant normal"
    )

    return 0


def calculate_risk(

    elevated,
    moderate,
    total

):

    if total == 0:

        return "Low"

    score = (

        elevated * 2
        +
        moderate

    ) / (

        total * 2

    )

    print(
        "[DEBUG] Score:",
        score
    )

    if score >= 0.70:

        return "Elevated"

    if score >= 0.30:

        return "Moderate"

    return "Low"


def compare_traits(

    genome1,
    genome2

):

    print("\n===================")
    print("[DEBUG] START")
    print("===================")

    elevated = 0

    moderate = 0

    checked = 0

    checked_genes = []

    risky = []

    for gene in VARIANT_RULES:

        print(
            "\n[DEBUG] CHECK:",
            gene
        )

        checked_genes.append(
            gene
        )

        g1 = search_gene(
            genome1,
            gene
        )

        g2 = search_gene(
            genome2,
            gene
        )

        print(
            "[DEBUG] Parent1:",
            g1
        )

        print(
            "[DEBUG] Parent2:",
            g2
        )

        if (

            not g1.get(
                "found"
            )

            and

            not g2.get(
                "found"
            )

        ):

            print(
                "[DEBUG] Gene missing"
            )

            continue

        if (

            is_sex_chromosome(
                g1.get(
                    "chromosome",
                    ""
                )
            )

            or

            is_sex_chromosome(
                g2.get(
                    "chromosome",
                    ""
                )
            )

        ):

            print(
                "[DEBUG] Skipped sex chromosome"
            )

            continue

        checked += 1

        p1 = detect_variant(

            g1.get(
                "sequence",
                ""
            ),

            gene,

            "Parent1"

        )

        p2 = detect_variant(

            g2.get(
                "sequence",
                ""
            ),

            gene,

            "Parent2"

        )

        shared = (
            p1 + p2
        )

        print(
            "[DEBUG] Shared Risk:",
            shared
        )

        if shared == 2:

            elevated += 1

            risky.append(
                f"{gene}(both)"
            )

        elif shared == 1:

            moderate += 1

            risky.append(
                f"{gene}(one)"
            )

    final = calculate_risk(

        elevated,

        moderate,

        checked

    )

    print("\n===================")
    print("[DEBUG] COMPLETE")
    print("===================")

    print(
        "[DEBUG] Checked:",
        checked_genes
    )

    print(
        "[DEBUG] Risk Genes:",
        risky
    )

    print(
        "[DEBUG] Elevated:",
        elevated
    )

    print(
        "[DEBUG] Moderate:",
        moderate
    )

    print(
        "[DEBUG] Final:",
        final
    )

    return [

        {

            "gene":

            (
                ", ".join(
                    risky
                )

                if risky

                else

                ", ".join(
                    checked_genes
                )

            ),

            "trait":
            TARGET_TRAIT,

            "possible_effect":
            final,

            "shared":
            elevated

        }

    ]