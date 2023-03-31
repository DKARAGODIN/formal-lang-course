from pyformlang.cfg import CFG, Variable


def cfg_to_weak_cnf(cfg: CFG) -> CFG:
    """
    Converts context free grammar (CFG) to weak chomsky normal form (WHNF)
    :param cfg: CFG to convert
    :return: WHNF
    """
    cleared_cfg = (cfg.eliminate_unit_productions().remove_useless_symbols())
    cleared_cfg_productions = cleared_cfg._decompose_productions(cleared_cfg._get_productions_with_only_single_terminals())
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=set(cleared_cfg_productions))


def get_cfg_from_file(file: str, start_symbol: Variable = Variable("S")) -> CFG:
    """
    Load CFG from file
    :param file: file path as a string
    :param start_symbol: Starting Symbol
    :return: CFG
    """
    with open(file) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
