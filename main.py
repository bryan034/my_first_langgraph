from typing import TypedDict
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END



class JobEvaluation(BaseModel):
    fit_score: int = Field(ge=0, le=100)
    reasoning: str

class JobState(TypedDict):
    job_description: str
    resume: str
    fit_score: int
    reasoning: str
    status: str

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
# temperature controls how much randomness is introduced when model selects its next token
# | Temperature | Behaviour | Suitable use cases |
# |---|---|---|
# | 0 | Less randomness; more consistent outputs | Classification, extraction, scoring |
# | 0.3 | Relatively consistent | Summarisation, technical explanations |
# | 0.7 | More varied responses | Conversational assistants, brainstorming |
# | 1.0 | Greater variation | Creative writing, idea generation |
structured_llm = llm.with_structured_output(JobEvaluation, method="json_schema")

def evaluate_candidate(state: JobState):
    prompt = f"""Evaluate this candidate for this job
    job: {state['job_description']}
    candidate: {state['resume']}
    """
    try: 
        # result = structured_llm.invoke(prompt)
        raise RuntimeError("simulated API failure")
        return {
            "fit_score":result.fit_score,
            "reasoning":result.reasoning,
            "status":"evaluated",
        }
    except Exception as e:
        return {"reasoning":f"Gemini evaluation failed: {type(e).__name__}: {e}",
                }

def decide(state: JobState):
    if state["status"]!="evaluated":
        return "error"
    if state['fit_score']>=80:
        return "approve"
    elif state['fit_score']>=50:
        return "review"
    return "reject"

def approve(state: JobState):
    return {"status":"approved"}

def review(state: JobState):
    return {"status":"review"}

def reject(state: JobState):
    return {"status":"rejected"}

def error(state: JobState):
    return {"status":"error"}

builder = StateGraph(JobState)
builder.add_node("evaluate", evaluate_candidate)
builder.add_node("approve", approve)
builder.add_node("review", review)
builder.add_node("reject", reject)
builder.add_node("error", error)

builder.add_edge(START, "evaluate")
builder.add_conditional_edges("evaluate",decide,
                              {
                                  "approve":"approve",
                                  "review":"review",
                                  "reject":"reject", 
                                  "error":"error"
                              })
builder.add_edge("approve", END)
builder.add_edge("review", END)
builder.add_edge("reject", END)
builder.add_edge("error", END)

graph = builder.compile()
r = graph.invoke({
    "job_description": "AI Engineer Intern requiring Python, FastAPI, REST APIs, SQL, LLM integration, and Docker.",
    "resume": "Business student with experience in event planning, social media marketing, customer service, and retail sales. Proficient in Microsoft PowerPoint and Canva. No programming, software development, or AI engineering experience.",
    "fit_score": 0,
    "reasoning": "",
    "status": "pending",
})
print(r)

