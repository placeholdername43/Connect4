l[Column]:
    match check_any_empty_cell(c):
        case None:
            return None