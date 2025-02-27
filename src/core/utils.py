def log_chain(llm_chain):
    r = ""
    for i, chain in enumerate(llm_chain):
        r += f"{chain['role']}: {chain['content']}\n"
    r += "================\n"
    return r