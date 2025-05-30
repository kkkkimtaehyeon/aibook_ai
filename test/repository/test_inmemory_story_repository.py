import unittest
from repository.StoryRepository import StoryRepository


class TestInMemoryStoryRepository(unittest.TestCase):

    def setUp(self):
        self.repository = StoryRepository()

    def test_save_context(self):
        # Given
        story_id = "story-1"
        story_context = "테스트 컨텍스트"

        # When
        saved_story = self.repository.save_context(story_id, story_context)

        # Then
        self.assertIsNotNone(saved_story)
        self.assertEqual(story_context, saved_story.context)
        self.assertEqual(0, len(saved_story.sentences))
        self.assertEqual(saved_story, self.repository.repository[story_id])

    def test_save_selected_sentence(self):
        # Given
        story_id = "story-1"
        story_context = "테스트 컨텍스트"
        selected_sentence = "테스트 문장"
        self.repository.save_context(story_id, story_context)

        # When
        updated_story = self.repository.save_selected_sentence(story_id, selected_sentence)

        # Then
        self.assertEqual(1, len(updated_story.sentences))
        self.assertEqual(selected_sentence, updated_story.sentences[0])

    def test_find_by_id_success(self):
        # Given
        story_id = "story-1"
        story_context = "테스트 컨텍스트"
        self.repository.save_context(story_id, story_context)

        # When
        found_story = self.repository.find_by_id(story_id)

        # Then
        self.assertIsNotNone(found_story)
        self.assertEqual(story_context, found_story.context)

    def test_find_by_id_not_found(self):
        # Given
        non_existent_id = "non-existent"

        # When & Then
        with self.assertRaises(ValueError) as context:
            self.repository.find_by_id(non_existent_id)

        self.assertTrue(f"story id '{non_existent_id}' not found" in str(context.exception))

    def test_delete_by_id(self):
        # Given
        story_id = "story-1"
        story_context = "테스트 컨텍스트"
        self.repository.save_context(story_id, story_context)

        # When
        self.repository.delete_by_id(story_id)

        # Then
        self.assertEqual(0, len(self.repository.repository))

    def test_delete_by_id_not_found(self):
        # Given
        non_existent_id = "non-existent"

        # When & Then
        with self.assertRaises(ValueError) as context:
            self.repository.delete_by_id(non_existent_id)

        self.assertTrue(f"story id '{non_existent_id}' not found" in str(context.exception))

    def test_multiple_sentences_added(self):
        # Given
        story_id = "story-1"
        story_context = "테스트 컨텍스트"
        self.repository.save_context(story_id, story_context)

        # When
        self.repository.save_selected_sentence(story_id, "첫 번째 문장")
        self.repository.save_selected_sentence(story_id, "두 번째 문장")
        self.repository.save_selected_sentence(story_id, "세 번째 문장")

        # Then
        story = self.repository.find_by_id(story_id)
        self.assertEqual(3, len(story.sentences))
        self.assertEqual("첫 번째 문장", story.sentences[0])
        self.assertEqual("두 번째 문장", story.sentences[1])
        self.assertEqual("세 번째 문장", story.sentences[2])


if __name__ == "__main__":
    unittest.main()