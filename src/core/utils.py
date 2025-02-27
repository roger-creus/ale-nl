def log_chain(llm_chain):
    r = ""
    for i, chain in enumerate(llm_chain):
        r += f"{chain['role']}: {chain['content']}\n"
    r += "================\n"
    return r


from transformers import AutoModel, AutoModelForCausalLM
def get_model_clss(model_name):
    if model_name in [
        "meta-llama/Llama-3.2-1B-Instruct",
        "meta-llama/Llama-3.2-3B-Instruct",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "microsoft/phi-4",
        "mistralai/Mixtral-8x7B-Instruct-v0.1"
        "microsoft/Phi-3.5-mini-instruct",
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-14B"
    ]:
        return AutoModelForCausalLM
    elif model_name in [
        "Qwen/Qwen2.5-VL-3B-Instruct",
    ]:
        return AutoModel