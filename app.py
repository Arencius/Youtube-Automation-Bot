import tkinter as tk
from bot import YoutubeBot

LABEL_FONT = ("Helvetica", 14)
ENTRY_FONT = ("Helvetica", 13)

class App:
    def __init__(self):
        self.main()

    def main(self):
        """ Builds application window. """
        window = tk.Tk()
        window.title('Youtube Bot')
        window.geometry('400x300')
        window.resizable(False, False)

        frame = tk.Frame(window,width=100)
        frame.grid(column=0)

        artist_label = tk.Label(window, text = 'Search for:', font = LABEL_FONT)
        artist_label.grid(row=0, column=1)
        self.artists_entry = tk.Entry(window,font = ENTRY_FONT)
        self.artists_entry.grid(row=1, column=1)

        playlist_name_label = tk.Label(window, text = 'Playlist name:', font = LABEL_FONT)
        playlist_name_label.grid(row=2, column=1)
        self.playlist_name_entry = tk.Entry(window,font = ENTRY_FONT)
        self.playlist_name_entry.grid(row=3, column=1)

        redirect_label = tk.Label(window, text = 'Link to redirect:', font=LABEL_FONT)
        redirect_label.grid(row=4, column=1)
        self.link_entry = tk.Entry(window,font=ENTRY_FONT)
        self.link_entry.grid(row=5, column=1)

        global var
        var = tk.IntVar()
        var.set(0)

        MODES = [('Public playlist', 0),
                ('Private playlist', 1)]

        for text, mode in MODES:
            radiobutton = tk.Radiobutton(window, text=text, variable = var, value=mode,
                            font = ('Helvetica', 13))
            radiobutton.grid(row=mode+6, column=1)

        self.confirm_button = tk.Button(window, text = "Let's go", font = ('Helvetica', 13), command = self.start_program)
        self.confirm_button.grid(row=8, column=1)

        window.mainloop()

    def data_correct(self,artists, playlist):
        """ Checks if provided data is valid (not empty). """
        return len(artists)>0 and len(playlist)>0

    def start_program(self):
        """ Creates the instance of the Bot and runs the program. """

        artists = list(filter(None, self.artists_entry.get().strip().split(',')))
        playlist_name = self.playlist_name_entry.get()
        url = self.link_entry.get()
        bot = YoutubeBot(artists, playlist_name, var.get(), url)

        if self.data_correct(artists, playlist_name):
            bot.run()
            self.confirm_button.config(state='disabled')
        else:
            print('No fields can remain empty')
          

if __name__=='__main__':
    App()
