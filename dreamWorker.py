from deep_daze import Imagine
import discord
from dotenv import load_dotenv

class DreamParams:
    def __init__(self,
                 image_width: int,
                 num_layers: int,
                 batch_size: int,
                 gradient_accumulate_every: int,
                 epochs: int,
                 iterations: int,
                 save_gif: bool,
                 save_every: int) -> None:
                 self.image_width = image_width
                 self.num_layers = num_layers
                 self.batch_size = batch_size
                 self.gradient_accumulate_every = gradient_accumulate_every
                 self.epochs = epochs
                 self.iterations = iterations
                 self.save_gif = save_gif
                 self.save_every = save_every

class DreamWorker:
    def __init__(self, dreamText: str, dreamParams:DreamParams) -> None:
        self.dreamText = dreamText
        self.dreamParams = dreamParams

    def runDream(self):
        dream = Imagine(
            text=self.dreamText,
            image_width=self.dreamParams.image_width,
            num_layers=self.dreamParams.num_layers,
            batch_size=self.dreamParams.batch_size,
            gradient_accumulate_every=self.dreamParams.gradient_accumulate_every,
            epochs=self.dreamParams.epochs,
            iterations=self.dreamParams.iterations,
            save_gif=self.dreamParams.save_gif,
            open_folder=False,
            save_every=self.dreamParams.save_every
        )
        dream()
        return dream.textpath


class DreamJob:
    def __init__(self, discordContext, dreamText: str) -> None:
        self.discordContext = discordContext
        self.dreamText = dreamText



