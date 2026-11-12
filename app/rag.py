
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.pdf_processor import load_documents


class SOPRetriever:
    """
    Retrieves relevant SOP and manual passages
    using TF-IDF and cosine similarity.
    """

    def __init__(self):
        print("Loading manufacturing documents...")

        self.chunks = load_documents()

        if not self.chunks:
            raise ValueError("No document chunks available.")

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        self.document_vectors = self.vectorizer.fit_transform(
            [chunk["text"] for chunk in self.chunks]
        )

        # Find the highest revision available for each document.
        self.latest_revisions = {}

        for chunk in self.chunks:
            doc_no = chunk["doc_no"]
            revision = chunk["revision"]

            if revision is not None:
                current = self.latest_revisions.get(doc_no)

                if current is None or revision > current:
                    self.latest_revisions[doc_no] = revision

        print(f"Loaded {len(self.chunks)} searchable chunks.")

    def is_revision_question(self, question):
        """Check whether the user specifically asks about revisions."""

        revision_terms = [
            "revision",
            "rev 03",
            "rev 04",
            "older version",
            "previous version",
            "compare versions",
            "revision history"
        ]

        question = question.lower()

        return any(term in question for term in revision_terms)

    def search(self, question, top_k=5, min_score=0.08):
        """Find the most relevant document passages."""

        if not question or not question.strip():
            return []

        query_vector = self.vectorizer.transform([question])

        scores = cosine_similarity(
            query_vector,
            self.document_vectors
        ).flatten()

        revision_question = self.is_revision_question(question)

        results = []

        for index, score in enumerate(scores):

            if score < min_score:
                continue

            chunk = self.chunks[index]

            # Exclude older revisions for normal operational questions.
            if not revision_question:
                revision = chunk["revision"]
                doc_no = chunk["doc_no"]

                latest = self.latest_revisions.get(doc_no)

                if revision is not None and latest is not None:
                    if revision < latest:
                        continue

            result = chunk.copy()
            result["similarity_score"] = round(float(score), 4)

            results.append(result)

        results.sort(
            key=lambda item: item["similarity_score"],
            reverse=True
        )

        return results[:top_k]


if __name__ == "__main__":

    retriever = SOPRetriever()

    print("\nManufacturing SOP Copilot Retrieval Test")

    while True:

        question = input("\nAsk a question (or type exit): ")

        if question.lower().strip() == "exit":
            break

        results = retriever.search(question)

        if not results:
            print("\nNo sufficiently relevant information was found.")
            continue

        print("\nRelevant information:\n")

        for result in results:
            print("------------------------------------")
            print(f"Document: {result['source']}")
            print(f"Revision: {result['revision']}")
            print(f"Page: {result['page']}")
            print(f"Relevance: {result['similarity_score']}")
            print(f"Text: {result['text'][:600]}")
