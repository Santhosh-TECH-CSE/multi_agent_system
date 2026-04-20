from llm import load_llm
from tools import web_search, scrape_url
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = load_llm()

# -------- Writer -------- #

writer_prompt = ChatPromptTemplate.from_template("""
You are an expert research analyst. Write a rigorous, well-structured research report
based strictly on the material provided. Do not fabricate facts, statistics, or sources.

Topic: {topic}

Research Material:
{research}

Using ONLY the information above, produce a report in this exact structure:

Introduction:
Provide 2–3 sentences establishing what the topic is, why it matters, and what this
report will cover.

Key Insights:
List the most important findings from the research. Each insight should be a specific,
evidence-backed point drawn directly from the material — not a generic statement.

Conclusion:
Summarise the core takeaways in 2–3 sentences and note any implications or open
questions the research raises.

Sources:
List any URLs or source references present in the research material. If none are
identifiable, write "Sources embedded in research material."

Output ONLY the report. Do not echo these instructions.
""")

writer_chain = writer_prompt | llm | StrOutputParser()

# -------- Critic -------- #

critic_prompt = ChatPromptTemplate.from_template("""
You are a rigorous editorial critic evaluating a research report for quality,
accuracy, clarity, and depth. Be specific and constructive — never vague.

Report:
{report}

Evaluate the report and respond in this exact structure:

Score: (a number out of 10)

Strengths:
Describe what the report does well with concrete references to its content.

Improvements:
Identify one specific weakness and explain exactly how the writer should address it.

Verdict:
One sentence on whether this report is ready to publish and why.

Output ONLY the critique. Do not echo these instructions.
""")

critic_chain = critic_prompt | llm | StrOutputParser()

def clean_output(text: str, kind: str = "report") -> str:
    """Clean model output by removing control tokens and any echoed prompt text.

    If `kind=='report'`, prefer returning the text starting at the first
    recognized report heading (e.g., 'Introduction:') to avoid exposing the
    prompt template in the UI. For `kind=='critique'`, remove leading
    'Report:' markers.
    """
    if not text:
        return ""

    # remove known control tokens and garbled assistant markers
    garbage = [
        "<|system|>", "<|user|>", "<|assistant|>", "</s>",
        "Write ONLY the final report", "Write ONLY the final report.",
        "Output ONLY the report", "Output ONLY the report.",
        "FORMAT:", "Topic:", "Research:", "Write a clean research report.",
        "Output ONLY the critique. Do not echo these instructions.",
        "Output ONLY the report. Do not echo these instructions.",
    ]

    for g in garbage:
        text = text.replace(g, "")

    text = text.strip()

    if kind == "report":
        # Prefer to return from the first good heading so prompts aren't shown
        for heading in ("Introduction:", "INTRODUCTION:", "Key Insights:", "Key insights:"):
            idx = text.find(heading)
            if idx != -1:
                return text[idx:].strip()

        # otherwise, if the model echoed the template, cut after the 'Format' marker
        m = "Format:"
        idx = text.find(m)
        if idx != -1:
            remainder = text[idx + len(m):].strip()
            # if remainder contains any heading, return from that heading
            for heading in ("Introduction:", "Key Insights:", "Conclusion:"):
                hidx = remainder.find(heading)
                if hidx != -1:
                    return remainder[hidx:].strip()
            return remainder

        return text

    # kind == 'critique'
    text = text.replace("Report:", "")
    return text.strip()

# -------- PIPELINE -------- #

def run_pipeline(topic: str):
    print("\n🔍 Searching...")
    search_results = web_search.invoke(topic)

    urls = []
    for line in search_results.split("\n"):
        if "|" in line:
            urls.append(line.split("|")[1].strip())

    print("\n🌐 Scraping...")
    scraped_data = ""

    for url in urls[:3]:
        data = scrape_url.invoke(url)
        if data:
            scraped_data += data + "\n\n"

    # 🚫 fallback if scraping fails
    if not scraped_data:
        scraped_data = "General knowledge about the topic."

    print("\n✍️ Writing...")
    report = writer_chain.invoke({
        "topic": topic,
        "research": scraped_data[:3000]
    })

    report = clean_output(report)

    print("\n🧠 Reviewing...")
    critique = critic_chain.invoke({
        "report": report
    })

    critique = clean_output(critique, kind="critique")

    return report, critique


# -------- RUN -------- #

if __name__ == "__main__":
    topic = input("Enter topic: ")

    report, critique = run_pipeline(topic)

    print("\n===== FINAL REPORT =====\n")
    print(report)

    print("\n===== CRITIQUE =====\n")
    print(critique)