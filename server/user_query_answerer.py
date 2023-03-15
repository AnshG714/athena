"""
Used for answering user queries. 
"""
import prompts
import asyncio
import json
from BaseProcessor import BaseProcessor


class UserQueryAnswerer(BaseProcessor):
    def __init__(self, max_chunk_tokens=2000):
        super().__init__(max_chunk_tokens=max_chunk_tokens)

    def prompt(self):
        return prompts.ANSWER_QUESTION

    def process_results(self, results):
        query_response = []
        for response in results:
            answer = response["choices"][0]["message"]["content"]
            query_response.append(answer)

        return " ".join(query_response)


if __name__ == "__main__":
    user_query_answerer = UserQueryAnswerer()
    context = """From the first days of Operation T4, particular attention was paid to young children, and especially to newborn babies. At Görden near Brandenburg, a state paediatric institution established a Special Psychiatric Youth Department to which children were sent from all over Germany, and killed. One of its aims, a doctor who worked there later recalled, was ‘to put newborns to sleep as soon as possible’, in order specifically to prevent ‘closer bonds between mothers and their children’. The euthanasia programme had begun. At Görden, and at six other institutions throughout Germany, those Germans judged insane were put to death. During the first two years of the war, tens of thousands were to perish in this way, the victims of perverted medical science. In Poland, the Special Task Force troops of the SS had continued the killing of Jews in more and more towns as they came under German control. On September 20 the Operations Section of the German Fourteenth Army reported that the troops were becoming uneasy ‘because of the largely illegal measures’ taken in the Army’s area by the task force commanded by General von Woyrsch. The fighting soldiers were particularly angered that the SS men under von Woyrsch’s command, instead of fighting at the front, ‘should be demonstrating their courage against defenceless civilians’. Field Marshal von Rundstedt immediately announced that von Woyrsch’s SS Task Force would no longer be tolerated in the war zone, and that the anti-Jewish measures already under way in the Katowice area should cease.

    From Danzig, Hitler moved to a hotel at the holiday resort town of Zoppot. There, to a group which included his personal physician, Dr Karl Brandt, the head of his Party Office, Philipp Bouler, and the Chief Medical Officer of the Reich, Dr Leonardo Conti, he set out his plans for the killing of the insane inside Germany itself. The purity of the German blood had to be maintained. Dr Conti doubted whether, medically speaking, there was any scientific basis for suggesting that any eugenic advantages could be produced through euthanasia. But the only serious discussion was about the quickest and least painful method of killing. Backdating his order to September 1, Hitler then gave Bouler and Brandt ‘full responsibility to enlarge the powers of certain specified doctors so that they can grant those who are by all human standards incurably ill a merciful death, after the most critical assessment possible of their medical condition’. The operational centre of the euthanasia programme was to be a suburban house in Berlin, No. 4 Tiergartenstrasse. It was this address which gave its name to the organization itself, known henceforth as ‘T.4’. Its head was the thirty-seven year old Werner Heyde, Professor of Neurology and Psychiatry at the University of Würzburg, who had joined the Nazi Party at its moment of political triumph in 1933. Henceforth, the mental asylums were to be combed for those who could be given ‘a merciful death’. In the words of one Nazi euthanasia expert, Dr Pfannmüller, ‘The idea is unbearable to me that the best, the flower of our youth, must lose its life at the front, in order that feebleminded and asocial elements can have a secure existence in the asylum.’

    Land Forces Committee set out, as the basis for Britain’s military planning, that the war would last ‘for at least three years’. The first twenty divisions should be established within the next twelve months, a further thirty-five divisions by the end of 1941. Meanwhile, the main thrust of Britain’s war effort would of necessity be defensive: September 7 saw the inauguration of the first two convoys of merchant ships, escorted by destroyers, one from the Thames estuary, through the English Channel and into the Atlantic, one from Liverpool into the Atlantic. That day, near the western Polish industrial city of Lodz, the last of the Polish defenders were still seeking to bar the German advance. Their adversaries, SS fighting troops, noted how, that afternoon, at Pabianice, ‘the Poles launched yet another counter-attack. They stormed over the bodies of their fallen comrades. They did not come forward with their heads down like men in heavy rain—and most attacking infantry come on like that—but they advanced with their heads held high like swimmers breasting the waves. They did not falter’. It was not lack of courage, but massively superior German artillery power, which, by nightfall, forced these defenders to surrender. Pabianice was lost. The road to Lodz was open. Inside Germany, those who had opposed the pre-war excesses of Nazism were equally critical of the attack on Poland. But the threat of imprisonment in a concentration camp was a powerful deterrent to public criticism. Before the war, thousands of Germans had fled from tyranny. Once war began, escape became virtually impossible, as Greater Germany’s frontiers were sealed and mounting restrictions imposed on movement and communications. The six months that had passed since the German occupation of Bohemia and Moravia in March 1939 had enabled the Gestapo system to be extended throughout the annexed regions. Two once- independent European capitals, Vienna and Prague, both suffered ruthless Nazi control, with all criticism punished and all independence of spirit crushed. The outbreak of war saw no slackening in the arrest of opponents of the regime; on September 9, Gestapo records show that 630 Czech political prisoners were brought by train from Bohemia to the concentration camp at Dachau, just north of Munich. Few of them were to survive the harsh conditions of work and the brutal treatment.

    Question: Can you tell me a little bit more about T4?
    """
    user_query_answerer.set_context(context)
    print(asyncio.run(user_query_answerer.get_results()))
