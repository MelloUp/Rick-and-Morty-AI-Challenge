"""
LLM Evaluation tests for clean architecture.
Tests generative AI features and evaluation framework.
"""
import pytest
import os

from src.config import get_config
from src.database import get_db_connection
from src.repositories import CacheRepository, EmbeddingRepository
from src.services import GeminiService, RickMortyService, SearchService

# Skip tests if Gemini API key is not available
config = get_config()
pytestmark = pytest.mark.skipif(
    not config.gemini.is_available,
    reason="GEMINI_API_KEY not set in environment"
)


@pytest.fixture
def gemini_service():
    """Create GeminiService instance."""
    return GeminiService(config.gemini)


@pytest.fixture
def rick_morty_service():
    """Create RickMortyService instance."""
    db = get_db_connection()
    cache_repo = CacheRepository(db)
    return RickMortyService(cache_repo, config.api)


@pytest.fixture
def search_service(gemini_service, rick_morty_service):
    """Create SearchService instance."""
    db = get_db_connection()
    embedding_repo = EmbeddingRepository(db)
    return SearchService(embedding_repo, gemini_service, rick_morty_service)


class TestLocationSummaryEvaluation:
    """Evaluate location summary generation quality."""

    def test_location_summary_generation(self, gemini_service, rick_morty_service):
        """Test that location summaries are generated successfully."""
        location = rick_morty_service.get_location(1)
        summary = gemini_service.generate_location_summary(location)

        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        print(f"\n\nGenerated Summary:\n{summary}")

    def test_location_summary_factual_consistency(self, gemini_service, rick_morty_service):
        """Evaluate factual consistency of location summaries."""
        location = rick_morty_service.get_location(1)
        summary = gemini_service.generate_location_summary(location)

        source_data = location.to_dict(include_residents=False)
        evaluation = gemini_service.evaluate_factual_consistency(summary, source_data)

        print(f"\n\nFactual Consistency Evaluation:")
        print(f"Score: {evaluation.score}/10")
        print(f"Reasoning: {evaluation.reasoning}")

        assert evaluation.score >= 4, f"Factual consistency score too low: {evaluation.score}"


class TestCharacterDialogueEvaluation:
    """Evaluate character dialogue generation quality."""

    def test_dialogue_generation(self, gemini_service, rick_morty_service):
        """Test that dialogues are generated successfully."""
        char1 = rick_morty_service.get_character(1)  # Rick
        char2 = rick_morty_service.get_character(2)  # Morty

        dialogue = gemini_service.generate_character_dialogue(char1, char2)

        assert dialogue is not None
        assert isinstance(dialogue, str)
        assert len(dialogue) > 0

        print(f"\n\nGenerated Dialogue:\n{dialogue}")

    def test_dialogue_creativity_evaluation(self, gemini_service, rick_morty_service):
        """Evaluate creativity of generated dialogues."""
        char1 = rick_morty_service.get_character(1)
        char2 = rick_morty_service.get_character(2)

        dialogue = gemini_service.generate_character_dialogue(char1, char2)
        evaluation = gemini_service.evaluate_creativity(dialogue)

        print(f"\n\nDialogue Creativity Evaluation:")
        print(f"Score: {evaluation.score}/10")
        print(f"Reasoning: {evaluation.reasoning}")

        assert evaluation.score >= 3, f"Dialogue creativity too low: {evaluation.score}"


class TestCharacterAnalysisEvaluation:
    """Evaluate character analysis generation quality."""

    def test_character_analysis_generation(self, gemini_service, rick_morty_service):
        """Test that character analyses are generated successfully."""
        character = rick_morty_service.get_character(1)
        analysis = gemini_service.generate_character_analysis(character)

        assert analysis is not None
        assert isinstance(analysis, str)
        assert len(analysis) > 0

        print(f"\n\nGenerated Analysis for {character.name}:\n{analysis}")

    def test_character_analysis_factual_consistency(self, gemini_service, rick_morty_service):
        """Evaluate factual consistency of character analyses."""
        character = rick_morty_service.get_character(1)
        analysis = gemini_service.generate_character_analysis(character)

        evaluation = gemini_service.evaluate_factual_consistency(
            analysis,
            character.to_dict()
        )

        print(f"\n\nAnalysis Factual Consistency:")
        print(f"Score: {evaluation.score}/10")

        assert evaluation.score >= 4, f"Factual consistency too low: {evaluation.score}"


class TestEmbeddingQuality:
    """Evaluate embedding generation and semantic search quality."""

    def test_embedding_generation(self, gemini_service):
        """Test that embeddings are generated successfully."""
        text = "Rick Sanchez is a genius scientist who travels across dimensions."
        embedding = gemini_service.generate_embedding(text)

        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)

        print(f"\n\nEmbedding dimension: {len(embedding)}")

    def test_embedding_similarity(self, gemini_service):
        """Test that similar texts have higher cosine similarity."""
        text1 = "Rick is a scientist who travels dimensions."
        text2 = "Rick Sanchez is a genius scientist exploring the multiverse."
        text3 = "Morty is a high school student."

        emb1 = gemini_service.generate_embedding(text1)
        emb2 = gemini_service.generate_embedding(text2)
        emb3 = gemini_service.generate_embedding(text3)

        similarity_1_2 = gemini_service.cosine_similarity(emb1, emb2)
        similarity_1_3 = gemini_service.cosine_similarity(emb1, emb3)

        print(f"\n\nSimilarity (Rick texts): {similarity_1_2:.4f}")
        print(f"Similarity (Rick vs Morty): {similarity_1_3:.4f}")

        assert similarity_1_2 > similarity_1_3, "Similar texts should have higher similarity"


class TestSemanticSearch:
    """Test semantic search functionality."""

    def test_index_character(self, search_service):
        """Test indexing a single character."""
        success = search_service.index_character(1)
        assert success is True

    def test_search_after_indexing(self, search_service):
        """Test semantic search after indexing."""
        # Index a few characters
        for char_id in [1, 2, 3]:
            search_service.index_character(char_id)

        # Perform search
        results = search_service.search("genius scientist", top_k=3)

        assert len(results) > 0
        assert all(hasattr(r, 'character') for r in results)
        assert all(hasattr(r, 'similarity') for r in results)

        print(f"\n\nSearch Results:")
        for r in results:
            print(f"  {r.character.name}: {r.similarity:.4f}")


class TestEvaluationMetrics:
    """Test evaluation metrics and scoring."""

    def test_factual_consistency_metric(self, gemini_service):
        """Test factual consistency evaluation metric."""
        source = {'name': 'Rick Sanchez', 'species': 'Human', 'status': 'Alive'}
        generated = "Rick Sanchez is a human who is currently alive."

        evaluation = gemini_service.evaluate_factual_consistency(generated, source)

        assert evaluation.score >= 0
        assert evaluation.score <= 10
        assert isinstance(evaluation.reasoning, str)

        print(f"\n\nFactual Consistency Score: {evaluation.score}/10")

    def test_creativity_metric(self, gemini_service):
        """Test creativity evaluation metric."""
        creative_text = "Wubba lubba dub dub! Rick burped loudly as he activated his portal gun."

        evaluation = gemini_service.evaluate_creativity(creative_text)

        assert evaluation.score >= 0
        assert evaluation.score <= 10
        assert isinstance(evaluation.reasoning, str)

        print(f"\n\nCreativity Score: {evaluation.score}/10")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
