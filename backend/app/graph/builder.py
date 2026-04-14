from langgraph.graph import StateGraph, START, END
from app.graph.state import QuizState
from app.graph.nodes import chunk_text, generate_questions, format_quiz


def build_quiz_graph():
    graph = StateGraph(QuizState)

    graph.add_node("chunk_text", chunk_text)
    graph.add_node("generate_questions", generate_questions)
    graph.add_node("format_quiz", format_quiz)

    graph.add_edge(START, "chunk_text")
    graph.add_edge("chunk_text", "generate_questions")
    graph.add_edge("generate_questions", "format_quiz")
    graph.add_edge("format_quiz", END)

    return graph.compile()


quiz_graph = build_quiz_graph()