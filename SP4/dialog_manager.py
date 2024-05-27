from dialog import SpeechCloudWS, Dialog
import asyncio
import logging

from data import *
from utils import *


# Haha
koktavy_voice = "Stanislav210"
# Meme voice == main voice
voice = "Jiri210"


class EndSignal(Exception):
    """
    Exception for ending the dialog
    My first prototype used to return commands (that is still there, but only for "continue", "keep", "reset" etc.)
    Among those commands, there was also "break", which was used to break the loop, but it was getting out of hand
    because user can say the "end" command at any time and sometimes I needed to break more than the main loop
    (e.g. when user has additional questions, that is loop within a loop within a loop within a function...)
    """
    pass


class Frame:
    """
    Class representing the context of the dialog
    """
    def __init__(self):
        """
        Initialize the frame
        """
        self.accident = ""
        self.place = ""
        self.time = ""
        self.yes_no = False
    
    def is_full(self):
        """
        Check if the frame is full
        :return: True if the frame is full, False otherwise
        """
        return self.accident != "" and self.place != "" and self.time != ""
    
    def what_is_missing(self):
        """
        Get the missing information
        :return: List of missing information (as strings for synthesis)
        """
        missing = []
        if self.accident == "":
            missing.append("Typ nehody")
        if self.place == "":
            missing.append("Místo")
        if self.time == "":
            missing.append("Čas")
        return missing
    
    def set_accident(self, accident):
        """
        Set the accident in the frame
        :param accident: Accident
        """
        self.accident = accident
    
    def set_place(self, place):
        """
        Set the place in the frame
        :param place: Place
        """
        self.place = place
    
    def set_time(self, time):
        """
        Set the time in the frame
        :param time: Time
        """
        self.time = time
    
    def set_yes_no(self, yes_no):
        """
        Set the yes/no question in the frame
        :param yes_no: Yes/no question
        """
        self.yes_no = yes_no
    
    def get_accident(self):
        """
        Get the accident from the frame
        :return: Accident
        """
        return self.accident
    
    def get_place(self):
        """
        Get the place from the frame
        :return: Place
        """
        return self.place
    
    def get_time(self):
        """
        Get the time from the frame
        :return: Time
        """
        return self.time
    
    def get_yes_no(self):
        """
        Get the yes/no question from the frame
        :return: Yes/no question
        """
        return self.yes_no


class DialogManager(Dialog):
    """
    Dialog manager class for the dialog system
    """
    async def main(self):
        """
        Main dialog loop
        """
        # Create a frame
        frame = Frame()

        # Welcome the user
        today = datetime.datetime.now()
        today = today.replace(year=today.year - 1)
        await self.synthesize_and_wait(voice=koktavy_voice, text="V V V Ví Vítej Vítejte v v v di di di dia dial alogovém s s sys sys systému. J J Ja Jak V V Vám mo mo mo mohu po po po pomo pomoci?")
        await self.synthesize_and_wait(voice=voice, text=f"Omlouvám se za koktavého kolegu, ujmu se Vás raději já. Vítejte v dialogovém systému. Můžete se mě zeptat na statistiky dopravních nehod v České republice. Pro ukončení dialogu řekněte konec. Upozorňuji, že API pro rok 2024 nefunguje, takže statistiky jsou o rok posunuté dozadu, dnes je tedy jakoby {today.strftime('%d. %m. %Y')}.")

        # Main dialog loop
        while True:
            # Try-catch so that I have easier time breaking the loop
            try:
                await self.synthesize_and_wait(voice=voice, text="Prosím, ptejte se na novou otázku.")

                # Recognize user speech
                words, command = await self.my_recognize()
                # User could have said nothing
                if command == "continue":
                    continue

                # Fill the frame with recognized words
                frame = await self.fill_frame(frame, words)
                await self.display(words)

                # While the context is not full, keep asking for missing information
                while not frame.is_full():
                    # Ask for things that are missing
                    missing = frame.what_is_missing()
                    await self.synthesize_and_wait(voice=voice, text=f"Chybí mi: {', '.join(missing)}. Můžete to doplnit?")

                    # Recognize user speech
                    words, command = await self.my_recognize()

                    # No input
                    if command == "continue":
                        continue

                    # Fill the frame with recognized words
                    frame = await self.fill_frame(frame, words, change_yes_no=False)
                    
                    await self.display(words)
                
                # Answer the question
                await self.answer_question(frame)

                # Additional questions for the user (Python is so lame, no Do-While)
                frame, command = await self.additional_questions(frame)
                while command == "keep":
                    frame, command = await self.additional_questions(frame)
                
                # Reset the frame
                frame = Frame()

                # Rest a bit :)
                await asyncio.sleep(1)
            
            # User wants to end the dialog
            except EndSignal:
                break

    async def my_recognize(self):
        """
        Recognize the user speech and handle the special commands
        (help, end commands)
        :return: Recognized words and command
        """
        result = await self.recognize_and_wait_for_asr_result(timeout=5.)

        # No input
        if result is None:
            await self.display("no-input")
            await self.synthesize_and_wait(voice=voice, text="Nerozumím, můžete to zopakovat?")
            return None, "continue"

        # Recognized words, sometimes there were words with underscores ?! WHY ?!
        words = result["word_1best"].replace("_", " ")

        # End command
        if any([phrase in words for phrase in end_phrases]):
            await self.display(words)
            await self.display("end")
            await self.synthesize_and_wait(voice=voice, text="Děkuji za použití dialogového systému. Mějte se hezky. Ještě Vám něco chce říct koktavý Standa 210.")
            await self.synthesize_and_wait(voice=koktavy_voice, text="Na na na nashle nashle nashledanou, mě mě mějte se se hez hezky!")
            await self.synthesize_and_wait(voice=voice, text="Stando! Pojď už!")
            raise EndSignal

        # Help command
        if any([phrase in words for phrase in help_phrases]):
            await self.display(words)
            await self.display("help")
            today = datetime.datetime.now()
            today = today.replace(year=today.year - 1)
            await self.synthesize_and_wait(voice=voice, text=f"Můžete se mě zeptat na statistiky dopravních nehod v České republice. Pro ukončení dialogu řekněte konec. Upozorňuji, že API pro rok 2024 nefunguje, takže statistiky jsou o rok posunuté dozadu, dnes je tedy jakoby {today.strftime('%d. %m. %Y')}.")
            return words, "continue"

        return words, "done"
    
    async def fill_frame(self, frame, words, change_yes_no=True):
        """
        Fill the frame with recognized words
        :param frame: Frame
        :param words: Words
        :return: Updated frame
        """
        # Detect the yes/no question
        if change_yes_no:
            for phrase in non_yes_no:
                if phrase in words:
                    frame.set_yes_no(False)
                    await self.display("non-yes-no")
                    break
            else:  # First time ever using else with for loop, yay
                frame.set_yes_no(True)
                await self.display("yes-no")

        # Try to find a place in the recognized words
        for place in places:
            if place in words:
                api_place = places_api_map_reversed[place]
                frame.set_place(api_place)
                await self.display(f"{place} -> {api_place}")
                break

        # Try to find an accident in the recognized words
        for accident in accidents:
            if accident in words:
                api_accident = accidents_api_map_reversed[accident]
                frame.set_accident(api_accident)
                await self.display(f"{accident} -> {api_accident}")
                break

        # Try to find a time in the recognized words
        for time in time_array:
            if time in words:
                time_key = time_map_reversed[time]

                # If we found a time, it might be decorated
                decorator_key = None
                for decorator in time_decorators:
                    if decorator in words:
                        decorator_key = time_decorators_map_reversed[decorator]
                # Minulý is substring of Předminulý ... thus we need to check it
                if decorator_key == "lastlast":
                    truly = False
                    for decorator in time_decorators_map["lastlast"]:
                        if decorator in words:
                            truly = True
                            break
                    if not truly:
                        decorator_key = "last"

                if decorator_key is not None:
                    time_key = f"{decorator_key} {time_key}"
                
                frame.set_time(time_key)
                print_time = decorator_key + " " + time_key if decorator_key is not None else time_key
                await self.display(f"{print_time} -> {time_key}")
                break
        
        return frame
    
    async def answer_question(self, frame):
        """
        Answer the question based on the frame
        :param frame: Frame
        """
        # Call the API
        api_results, from_time, to_time = api_call(frame)

        await self.display(f"what: {frame.get_accident()}, where: {frame.get_place()}, when: {from_time} -- {to_time}")
        await self.display(f"API result: {api_results}")

        # Synthesize the answer
        text = f"{accidents_speech_map[frame.get_accident()]} {places_speech_map[frame.get_place()]} od {from_time.strftime('%d. %m. %Y')} do {to_time.strftime('%d. %m. %Y')} je {api_results}."
        # If the question was a yes/no question, answer accordingly
        if frame.get_yes_no():
            if api_results != 0:
                text = "Ano."
            else:
                text = "Ne."

        await self.synthesize_and_wait(voice=voice, text=text)
    
    async def additional_questions(self, frame):
        """
        Ask the user for additional questions
        :param frame: Frame
        :return: Updated frame and command
        """
        await self.synthesize_and_wait(voice=voice, text="Máte nějaké doplňující otázky?")

        # Python has no Do-While sadly, my C-soul is hurting
        words, command = await self.my_recognize()
        # While the user said nothing, keep asking
        while command == "continue":
            words, command = await self.my_recognize()

        await self.display(words)

        # Check if the user wants to reset the frame and has no additional questions
        for no_phrase in no_phrases:
            if no_phrase in words:
                return frame, "reset"
        
        await self.display("FRAME KEEP")

        # Update the frame
        frame = await self.fill_frame(frame, words)

        # Answer the question
        await self.answer_question(frame)
        # Keep asking for additional questions
        return frame, "keep"


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)-10s %(message)s', level=logging.DEBUG)
    SpeechCloudWS.run(DialogManager, address="0.0.0.0", port=8888)
