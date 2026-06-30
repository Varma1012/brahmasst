from tasks.trait_engine import TRAITS


def compare_offspring(
    parent1,
    parent2
):

    result = []

    genes1 = set(parent1)

    genes2 = set(parent2)

    common = (
        genes1
        &
        genes2
    )

    for gene in common:

        if gene in TRAITS:

            info = TRAITS[
                gene
            ]

            result.append({

                "gene":
                    gene,

                "trait":
                    info.get(
                        "trait"
                    ),

                "possible_effect":
                    info.get(
                        "advantage"
                    )
                    or
                    info.get(
                        "risk"
                    )
            })

    return result