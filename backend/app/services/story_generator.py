import openai
import logging
from typing import Optional
from app.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoryGenerator:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in settings.")
        openai.api_key = self.api_key

    def generate_story(self, character: Optional[str], theme: Optional[str],
                       duration: int, language: str) -> str:
        try:
            logger.info(f"Generating story | character={character}, theme={theme}, "
                        f"duration={duration}, language={language}")

            base_word_count = settings.get_word_count(duration, language)
            if language == "hi":
                word_count = int(base_word_count * 1.5)
            else:
                word_count = base_word_count
                
            prompt = self._create_prompt(character, theme, word_count, language)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "You are a creative storyteller who writes engaging, imaginative stories "
                        "suitable for children and families. "
                        "Always write in the requested language. "
                        "Make sure the story has a clear beginning, middle, and end."
                        "For Hindi stories, write longer, more detailed stories with rich descriptions."
                    )},
                    {"role": "user", "content": prompt}
                ],
                timeout=60
            )

            if response.choices and len(response.choices) > 0:
                generated_text = response.choices[0].message.content.strip()
                if generated_text:
                    logger.info("Story generated successfully with OpenAI")
                    return self._clean_generated_text(generated_text)

            raise RuntimeError("OpenAI API returned no valid response.")

        except Exception as e:
            logger.exception("Story generation failed")
            raise RuntimeError(f"Story generation failed: {e}")

    def _create_prompt(self, character: Optional[str], theme: Optional[str],
                       word_count: int, language: str) -> str:
        if language == "hi":
            prompt = (
                f"आप एक रचनात्मक कहानीकार हैं। यदि पात्र \"{character}\" किसी फ़िल्म, कार्टून, वेब सीरीज़ "
                "या किताब से जुड़ा हुआ है तो उस पात्र का उपयोग सीधे कहानी में कीजिए, "
                "लेकिन यह मत बताइए कि वह कहाँ से आता है। यदि पात्र ज्ञात नहीं है, "
                "तो उसे एक मौलिक पात्र मानकर कहानी में प्रयोग कीजिए। "
                f"फिर लगभग {word_count} शब्दों की एक विस्तृत, रचनात्मक और रोचक कहानी लिखिए। "
                "कहानी में जीवंत वर्णन, संवाद, और विस्तृत विवरण शामिल करें। "
            )
            if theme:
                prompt += f"कहानी का मुख्य विषय \"{theme}\" होना चाहिए। "
            prompt += (
                "कहानी में स्पष्ट शुरुआत, मध्य और अंत हो। "
                "पात्रों के विचारों, भावनाओं और कार्यों का विस्तृत वर्णन करें। "
                "इसे बच्चों और परिवारों के लिए उपयुक्त बनाएँ। "
                "पूरी कहानी हिंदी में लिखें और कम से कम {word_count} शब्दों की होनी चाहिए।"
            )
        else:
            prompt = (
                f"You are a creative storyteller. If the character \"{character}\" already appears in a "
                "movie, cartoon, web series, or book, use the character naturally in the story, "
                "but do not mention where it comes from. If the character is not known, treat it as an "
                "original character. Then write a creative, engaging story of about "
                f"{word_count} words. "
            )
            if theme:
                prompt += f"The theme of the story should be \"{theme}\". "
            prompt += (
                "The story must have a clear beginning, middle, and end, with challenges, emotions, "
                "and a meaningful resolution. Make it vivid, imaginative, and suitable for children and families. "
                "Write everything in English."
            )
        return prompt

    def _clean_generated_text(self, text: str) -> str:
        text = text.strip()
        if not text.endswith("."):
            text += "."
        return text
