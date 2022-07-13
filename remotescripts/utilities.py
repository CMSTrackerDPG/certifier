import re


def split_with_spaces_commas(value):
    return list(
        map(
            str,
            re.split(
                " , | ,|, |,| ",
                re.sub(r"\s+", " ", value).lstrip().rstrip(),
            ),
        )
    )
